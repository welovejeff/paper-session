#!/usr/bin/env python3
"""Build the paper-session promotional site.

Static site generator, Python standard library only. No Node, no jinja2, no
third-party anything: this repo's dependency list is reportlab + pdfplumber and
the website is not allowed to add a third.

The rule this script exists to enforce
--------------------------------------
Nothing on the site is hand-copied from the repo. Install directions, the
compatibility ledger, the whole text of scan-back/SKILL.md, the evidence
limitations and the three numbers are READ FROM THE SOURCE FILE at build time
and converted to HTML here. CLAUDE.md binds install directions to README
§Install and nowhere else; this file is what makes that mechanical instead of a
promise. If you are about to type repo prose into a template, add an extractor
here instead.

Usage
-----
    python3 site/build.py                      # build to site/dist/
    python3 site/build.py --serve 8000         # build, then serve dist/
    python3 site/build.py --allow-missing-assets
    python3 site/build.py --strict             # dangling internal links fail

Full authoring contract: site/README.md
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# The sheet's numbers are DERIVED from paper-session/references/design.md, never
# restated here or in static/style.css. See sheetspec.py's docstring for why.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import sheetspec  # noqa: E402  (path set above so this works from any cwd)

# --------------------------------------------------------------------------
# Paths and constants
# --------------------------------------------------------------------------

SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
TEMPLATES = SITE / "templates"
STATIC = SITE / "static"
DIST_DEFAULT = SITE / "dist"

REPO_URL = "https://github.com/welovejeff/paper-session"
BLOB_URL = REPO_URL + "/blob/main/"
RAW_URL = "https://raw.githubusercontent.com/welovejeff/paper-session/main/"

# The page that carries the limitations, and the anchors #number-1..3 the three
# front-page figures link into. Named once, because build.py generates those
# links and a template must never guess at the slug.
EVIDENCE_SLUG = "evidence"

# Repo files copied into dist/ as real downloads, source -> dist-relative path.
ASSET_FILES = {
    "docs/specimen.pdf": "specimen.pdf",
}
ASSET_GLOBS = {
    "docs/sheet-*.png": "sheets/",
}
# Repo paths that must resolve to a site asset rather than to GitHub when they
# appear as a link or image in extracted markdown.
ASSET_LINK_MAP = {
    "docs/specimen.pdf": "specimen.pdf",
}

# Hero photograph: the maintainer drops one of these into site/static/.
HERO_CANDIDATES = ("hero.jpg", "hero.jpeg", "hero.png", "hero.webp")

# The worked example on the return-trip page: a photograph of a real completed
# page. Its partner is docs/worked-example.md, the unedited reply that
# photograph produced. Both are pending assets; see site/README.md.
EXAMPLE_CANDIDATES = (
    "return-example.jpg",
    "return-example.jpeg",
    "return-example.png",
    "return-example.webp",
)

# Pages the site plans to have. A page exists as soon as a template with the
# matching slug lands in site/templates/; until then build.py emits a marked
# stub so no link on the site dangles. Page authors: drop in your template and
# your stub disappears. Nav order is the ascending-commitment order of the
# landing page's onramps.
PLANNED_PAGES = [
    {
        "slug": "get-a-sheet",
        "title": "Get a sheet",
        "nav_label": "Get a sheet",
        "nav_order": "10",
        "description": "Print a real specimen sheet. No account, no install, "
        "nothing to sign up for.",
    },
    {
        "slug": "no-printer",
        "title": "No printer",
        "nav_label": "No printer",
        "nav_order": "20",
        "description": "The dictated path: a card you copy into whatever "
        "notebook you already own.",
    },
    {
        "slug": "scan-back",
        "title": "Scan back",
        "nav_label": "Scan back",
        "nav_order": "30",
        "description": "The return half of the loop, printed here in full so "
        "you can paste it into the AI you already have.",
    },
    {
        "slug": "install",
        "title": "Install",
        "nav_label": "Install",
        "nav_order": "40",
        "description": "Both skills, both tracks, and an honest account of "
        "where the loop stands agent by agent.",
    },
    {
        "slug": "evidence",
        "title": "Evidence",
        "nav_label": "Evidence",
        "nav_order": "50",
        "description": "What the research says, where it stops, and what it "
        "does not support.",
    },
]


class BuildError(Exception):
    """A build failure that should print one clear sentence and stop."""


WARNINGS: list[str] = []


def warn(message: str) -> None:
    WARNINGS.append(message)
    print(f"  warn: {message}", file=sys.stderr)


# --------------------------------------------------------------------------
# Reading the repo
# --------------------------------------------------------------------------


def read_repo(relpath: str, required: bool = True) -> str | None:
    """Read a repo file as text. Other agents may be mid-edit; never guess."""
    path = ROOT / relpath
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        if required:
            raise BuildError(
                f"required repo file is missing: {path}\n"
                f"  The site reads its content from the repo rather than "
                f"restating it, so it cannot be built without this file."
            )
        warn(f"optional repo file missing, skipping what it feeds: {relpath}")
        return None
    except OSError as exc:  # pragma: no cover - unreadable file
        raise BuildError(f"could not read {path}: {exc}")


# --------------------------------------------------------------------------
# Markdown -> HTML (the subset the repo actually uses)
# --------------------------------------------------------------------------
#
# Supported: ATX headings, fenced code, GFM pipe tables, unordered and ordered
# lists (one level of nesting), blockquotes, thematic breaks, paragraphs, and
# inline bold / italic / strikethrough / code / links / images.
# Not supported (and not used by the files we read): setext headings, HTML
# blocks, reference links, footnotes, task lists, definition lists.

BASE_TOKEN = "%%BASE%%"  # replaced per page with that page's relative prefix

_TABLE_DELIM = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")


def is_truthy(value: object) -> bool:
    """One truth test, shared by `{% if %}` and by the sheet gate.

    A front-matter key means the same thing to a template as it does to
    build.py; `sheet: false` must not print a sheet and must not be gated as
    one.
    """
    return str(value).strip() not in ("", "0", "false", "False")


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def slugify(text: str) -> str:
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "section"


def resolve_link(url: str) -> str:
    """Point a repo-relative link somewhere that actually exists."""
    url = url.strip()
    if not url:
        return url
    if re.match(r"^(https?:|mailto:|#|/)", url):
        return url
    path, _, frag = url.partition("#")
    frag = ("#" + frag) if frag else ""
    if path in ASSET_LINK_MAP:
        return BASE_TOKEN + ASSET_LINK_MAP[path] + frag
    if re.match(r"^docs/sheet-.*\.png$", path):
        return BASE_TOKEN + "sheets/" + Path(path).name + frag
    if not path:
        return frag
    return BLOB_URL + path.lstrip("./") + frag


def resolve_image(url: str) -> str:
    path = url.strip()
    if re.match(r"^(https?:|/|data:)", path):
        return path
    if re.match(r"^docs/sheet-.*\.png$", path):
        return BASE_TOKEN + "sheets/" + Path(path).name
    if path in ASSET_LINK_MAP:
        return BASE_TOKEN + ASSET_LINK_MAP[path]
    return RAW_URL + path.lstrip("./")


def inline_md(text: str) -> str:
    """Inline markdown -> HTML. Escapes first, formats second."""
    codes: list[str] = []

    def stash(match: re.Match[str]) -> str:
        codes.append(match.group(1))
        return f"\x00{len(codes) - 1}\x00"

    out = re.sub(r"`([^`]+)`", stash, text)
    out = esc(out)

    def img(match: re.Match[str]) -> str:
        alt, src = match.group(1), match.group(2)
        return (
            f'<img src="{resolve_image(src)}" alt="{alt}" loading="lazy" '
            f'decoding="async">'
        )

    out = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", img, out)

    def link(match: re.Match[str]) -> str:
        label, href = match.group(1), match.group(2)
        target = resolve_link(href)
        external = target.startswith("http")
        rel = ' rel="noopener"' if external else ""
        return f'<a href="{target}"{rel}>{label}</a>'

    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out, flags=re.S)
    out = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", out, flags=re.S)
    out = re.sub(r"~~(.+?)~~", r"<del>\1</del>", out, flags=re.S)
    out = re.sub(
        r"\x00(\d+)\x00",
        lambda m: f"<code>{esc(codes[int(m.group(1))])}</code>",
        out,
    )
    return out


def _split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def md_to_html(md: str, heading_offset: int = 0) -> str:
    """Convert a markdown block to HTML.

    heading_offset shifts every heading level down, so a README `##` embedded
    under a page's own `<h1>` renders as `<h3>` and the outline stays sane.
    """
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    def flush_paragraph(buf: list[str]) -> None:
        if buf:
            out.append(f'<p>{inline_md(" ".join(buf).strip())}</p>')
            buf.clear()

    para: list[str] = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # fenced code
        fence = re.match(r"^\s*(`{3,}|~{3,})\s*([\w+-]*)\s*$", line)
        if fence:
            flush_paragraph(para)
            marker, lang = fence.group(1)[0] * 3, fence.group(2)
            body: list[str] = []
            i += 1
            while i < n and not re.match(rf"^\s*{marker}+\s*$", lines[i]):
                body.append(lines[i])
                i += 1
            i += 1
            code = esc("\n".join(body))
            cls = f' class="lang-{esc(lang)}"' if lang else ""
            if lang == "mermaid":
                # A flowchart in a fence is a diagram, not code the reader runs.
                out.append(
                    '<pre class="code code--diagram" aria-hidden="true">'
                    f"<code>{code}</code></pre>"
                )
            else:
                out.append(f'<pre class="code"><code{cls}>{code}</code></pre>')
            continue

        # blank
        if not stripped:
            flush_paragraph(para)
            i += 1
            continue

        # heading
        heading = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", line)
        if heading:
            flush_paragraph(para)
            level = min(6, len(heading.group(1)) + heading_offset)
            text = heading.group(2)
            out.append(
                f'<h{level} id="{slugify(text)}">{inline_md(text)}</h{level}>'
            )
            i += 1
            continue

        # thematic break
        if re.match(r"^\s*(\*\s*){3,}$|^\s*(-\s*){3,}$|^\s*(_\s*){3,}$", line):
            flush_paragraph(para)
            out.append('<hr class="rule-close">')
            i += 1
            continue

        # table
        if "|" in stripped and i + 1 < n and _TABLE_DELIM.match(lines[i + 1]):
            flush_paragraph(para)
            headers = _split_row(stripped)
            i += 2
            rows: list[list[str]] = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(_split_row(lines[i]))
                i += 1
            head = "".join(f"<th scope=\"col\">{inline_md(c)}</th>" for c in headers)
            body_html = []
            for row in rows:
                cells = "".join(f"<td>{inline_md(c)}</td>" for c in row)
                body_html.append(f"<tr>{cells}</tr>")
            out.append(
                '<div class="scroller"><table><thead><tr>'
                + head
                + "</tr></thead><tbody>"
                + "".join(body_html)
                + "</tbody></table></div>"
            )
            continue

        # blockquote
        if stripped.startswith(">"):
            flush_paragraph(para)
            quote: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append(f"<blockquote>{md_to_html(chr(10).join(quote), heading_offset)}</blockquote>")
            continue

        # list
        item = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
        if item:
            flush_paragraph(para)
            block, i = _consume_list(lines, i)
            out.append(block)
            continue

        para.append(stripped)
        i += 1

    flush_paragraph(para)
    return "\n".join(out)


def _consume_list(lines: list[str], start: int) -> tuple[str, int]:
    """Parse a list (with one level of nesting) starting at `start`."""
    first = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", lines[start])
    assert first is not None
    base_indent = len(first.group(1))
    ordered = bool(re.match(r"\d", first.group(2)))
    tag = "ol" if ordered else "ul"

    items: list[str] = []
    current: list[str] = []
    nested: list[str] = []
    i = start
    n = len(lines)

    def close_item() -> None:
        if current or nested:
            body = inline_md(" ".join(current).strip())
            if nested:
                sub, _ = _consume_list(nested, 0)
                body += sub
            items.append(f"<li>{body}</li>")
            current.clear()
            nested.clear()

    while i < n:
        line = lines[i]
        if not line.strip():
            # a blank line ends the list unless the next line continues it
            if i + 1 < n and re.match(r"^(\s*)([-*+]|\d+[.)])\s+", lines[i + 1]):
                nxt = re.match(r"^(\s*)", lines[i + 1])
                assert nxt is not None
                if len(nxt.group(1)) >= base_indent:
                    i += 1
                    continue
            break
        match = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
        if match:
            indent = len(match.group(1))
            if indent > base_indent:
                nested.append(line[base_indent + 2 :])
                i += 1
                continue
            if indent < base_indent:
                break
            close_item()
            current.append(match.group(3))
            i += 1
            continue
        indent = len(line) - len(line.lstrip())
        if indent > base_indent and (current or nested):
            if nested:
                nested.append(line[base_indent + 2 :])
            else:
                current.append(line.strip())
            i += 1
            continue
        break

    close_item()
    return f"<{tag}>" + "".join(items) + f"</{tag}>", i


# --------------------------------------------------------------------------
# Section extraction
# --------------------------------------------------------------------------


def iter_headings(md: str):
    """Yield (index, level, text) for every ATX heading outside code fences."""
    in_fence = False
    for idx, line in enumerate(md.split("\n")):
        if re.match(r"^\s*(`{3,}|~{3,})", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", line)
        if match:
            yield idx, len(match.group(1)), match.group(2).strip()


def normalize_heading(text: str) -> str:
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text.rstrip(".:!?")


def extract_section(md: str, wanted: str, source: str, required: bool = True) -> str | None:
    """Return the body of the section whose heading matches `wanted`.

    Matching is forgiving on purpose: other agents are editing these files
    right now, so a changed level, changed case, or an appended parenthetical
    should not break the build. A genuinely missing section should.
    """
    target = normalize_heading(wanted)
    lines = md.split("\n")
    found = None
    for idx, level, text in iter_headings(md):
        norm = normalize_heading(text)
        if norm == target or norm.startswith(target):
            found = (idx, level)
            break
    if found is None:
        if required:
            raise BuildError(
                f"could not find the §{wanted} section in {source}.\n"
                f"  The site renders that section from the source file rather "
                f"than restating it, and refuses to emit an empty page in its "
                f"place. Either the heading was renamed (update the extractor "
                f"in site/build.py) or the file is mid-edit."
            )
        warn(f"section §{wanted} not found in {source}; skipping")
        return None
    start, level = found
    end = len(lines)
    for idx, lvl, _ in iter_headings(md):
        if idx > start and lvl <= level:
            end = idx
            break
    return "\n".join(lines[start + 1 : end]).strip("\n")


def extract_paragraph(
    md: str, lead: str, source: str, required: bool = False
) -> str | None:
    """Return the one paragraph whose opening words are `lead`.

    Several load-bearing sentences in the repo are bold-led paragraphs inside a
    larger section rather than sections of their own ("The return half travels
    further than the forward half", "Notice what is not there"). A page that
    wants to quote one of them must be able to reach it without a template
    reconstructing it. Matching ignores markdown emphasis and case, so bolding
    or unbolding the lead does not break the build.
    """
    target = normalize_heading(lead)
    block: list[str] = []
    for line in md.replace("\r\n", "\n").split("\n") + [""]:
        if line.strip():
            block.append(line)
            continue
        if block:
            opening = normalize_heading(re.sub(r"^[>\-*+\d.)\s]+", "", block[0]))
            if opening.startswith(target):
                return "\n".join(block)
            block = []
    if required:
        raise BuildError(
            f"could not find the paragraph beginning “{lead}” in {source}.\n"
            f"  The site quotes it from the source file rather than restating "
            f"it. Either the sentence was reworded (update the extractor in "
            f"site/build.py) or the file is mid-edit."
        )
    warn(f"paragraph “{lead}” not found in {source}; skipping")
    return None


def find_first_table(md: str) -> tuple[int, int] | None:
    """Return (start, end) line indices of the first GFM table in `md`."""
    lines = md.split("\n")
    for i in range(len(lines) - 1):
        if "|" in lines[i] and _TABLE_DELIM.match(lines[i + 1]):
            j = i + 2
            while j < len(lines) and "|" in lines[j] and lines[j].strip():
                j += 1
            return i, j
    return None


def parse_table(md: str) -> tuple[list[str], list[list[str]]]:
    span = find_first_table(md)
    if span is None:
        return [], []
    lines = md.split("\n")
    start, end = span
    headers = _split_row(lines[start])
    rows = [_split_row(line) for line in lines[start + 2 : end]]
    return headers, rows


def strip_front_matter(md: str) -> tuple[dict[str, str], str]:
    """Split a YAML-ish `---` front matter block off a SKILL.md."""
    if not md.startswith("---"):
        return {}, md
    parts = md.split("\n---", 2)
    if len(parts) < 2:
        return {}, md
    head = parts[0][3:]
    body = parts[1].lstrip("\n") if len(parts) == 2 else parts[1].lstrip("\n")
    meta: dict[str, str] = {}
    for line in head.split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"')
    return meta, body


def plain_text(md: str) -> str:
    """Strip inline markdown down to readable text (for JSON / attributes)."""
    text = re.sub(r"`([^`]*)`", r"\1", md)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_~]+", "", text)
    return re.sub(r"\s+", " ", text).strip()


# --------------------------------------------------------------------------
# Repo content -> template context
# --------------------------------------------------------------------------


def build_repo_context() -> dict[str, str]:
    """Every piece of repo content the site is allowed to show.

    Add an entry here when a page needs repo content. Do not type repo prose
    into a template.
    """
    ctx: dict[str, str] = {}

    readme = read_repo("README.md")
    assert readme is not None

    # --- §Install, split into intro / ledger / closing note ----------------
    install = extract_section(readme, "Install", "README.md", required=True)
    assert install is not None
    span = find_first_table(install)
    if span is None:
        raise BuildError(
            "README §Install has no compatibility table.\n"
            "  The landing page renders the ledger from it and the install "
            "page prints it in full; neither may invent one."
        )
    ilines = install.split("\n")
    tstart, tend = span
    # The ledger's own subheading, if it has one, belongs with the ledger.
    hstart = tstart
    for k in range(tstart - 1, -1, -1):
        if re.match(r"^#{2,6}\s+", ilines[k]):
            hstart = k
            break
        if ilines[k].strip():
            break
    ledger_heading = ""
    if re.match(r"^#{2,6}\s+", ilines[hstart]):
        ledger_heading = re.sub(r"^#{2,6}\s+", "", ilines[hstart]).strip()

    intro_md = "\n".join(ilines[:hstart]).strip("\n")
    ledger_md = "\n".join(ilines[tstart:tend]).strip("\n")
    note_md = "\n".join(ilines[tend:]).strip("\n")

    ctx["repo_install_html"] = md_to_html(intro_md, heading_offset=1)
    ctx["repo_install_note_html"] = md_to_html(note_md, heading_offset=1)
    ctx["repo_ledger_heading"] = esc(plain_text(ledger_heading))
    ctx["repo_ledger_table_html"] = md_to_html(ledger_md)

    headers, rows = parse_table(ledger_md)
    ledger_rows = []
    previous_loop = ""
    previous_extra: list[dict[str, str]] = []
    for row in rows:
        cells = (row + ["", "", ""])[:3]
        agent_md, install_md, loop_md = cells
        loop_text = plain_text(loop_md)
        inherits = loop_text.lower().startswith("same as above")
        if inherits and previous_loop:
            source_md = previous_loop
        else:
            source_md = loop_md
            previous_loop = loop_md
        loop_html = md_to_html(source_md).strip()
        loop_text = plain_text(source_md)
        status_match = re.search(r"\*\*(.+?)\*\*", source_md)
        # Every column past the third. The ledger has grown a column once
        # already ("Also install", the per-agent dependency answer); truncating
        # to three silently dropped it from the chip answer on the landing
        # page, which then told people how to install without saying what else
        # they had to install. Nothing is dropped now.
        extra: list[dict[str, str]] = []
        for index in range(3, max(len(row), len(headers))):
            cell_md = row[index] if index < len(row) else ""
            header_md = headers[index] if index < len(headers) else ""
            cell_text = plain_text(cell_md)
            if cell_text.lower().startswith("same as above") and previous_extra:
                inherited = next(
                    (
                        e
                        for e in previous_extra
                        if e["header"] == plain_text(header_md)
                    ),
                    None,
                )
                if inherited:
                    extra.append(dict(inherited))
                    continue
            extra.append(
                {
                    "header": plain_text(header_md),
                    "value": cell_text,
                    "value_html": inline_md(cell_md),
                }
            )
        if not inherits or not previous_extra:
            previous_extra = extra
        ledger_rows.append(
            {
                "agent": plain_text(agent_md),
                "agent_html": inline_md(agent_md),
                "install": plain_text(install_md),
                "install_html": inline_md(install_md),
                "loop": loop_text,
                "loop_html": loop_html,
                "status": plain_text(status_match.group(1)) if status_match else "",
                "chips": ledger_chips(agent_md),
                "extra": extra,
            }
        )
    if not ledger_rows:
        raise BuildError("README §Install ledger parsed to zero rows.")
    # Counted, never asserted in prose: "exactly one row is verified" is the
    # kind of sentence that goes quietly false the day a second row lands.
    ctx["repo_ledger_verified_count"] = str(
        sum(
            1
            for row in ledger_rows
            if row["status"].lower().startswith("verified end to end")
        )
    )
    ctx["repo_ledger_row_count"] = str(len(ledger_rows))

    ctx["repo_ledger_json"] = json.dumps(
        {"headers": [plain_text(h) for h in headers], "rows": ledger_rows},
        indent=None,
        sort_keys=True,
    ).replace("</", "<\\/")
    ctx["repo_ledger_chips_html"] = render_chips(ledger_rows)

    # The sentence the return-trip page is built around, currently reachable
    # only inside the whole §Install blob.
    return_half = extract_paragraph(
        install, "The return half travels further than the forward half", "README.md"
    )
    ctx["repo_return_half_html"] = md_to_html(return_half) if return_half else ""

    # The paste channel's load-bearing sentence, and the honesty that follows
    # it. The no-printer page quotes both rather than paraphrasing them.
    paste = extract_paragraph(
        install, "If your AI can't install skills at all", "README.md"
    )
    ctx["repo_paste_route_html"] = md_to_html(paste) if paste else ""
    # The load-bearing sentence itself, and the honesty that follows it. The
    # sentence is offered as a copy button, so it is also needed as plain text.
    quote = re.search(r"^\s*>\s*(.+)$", install, re.M)
    ctx["repo_paste_sentence"] = esc(plain_text(quote.group(1))) if quote else ""
    ctx["repo_paste_sentence_html"] = (
        md_to_html("> " + quote.group(1)) if quote else ""
    )
    honesty = extract_paragraph(
        install, "The sentence is load-bearing", "README.md"
    )
    ctx["repo_paste_honesty_html"] = md_to_html(honesty) if honesty else ""

    # The path for someone who cannot read the printed page. It lives below the
    # ledger because no ledger row states it, and the no-printer page is where
    # it has to be visible rather than discovered.
    accessible = extract_paragraph(
        install, "Reading the printed page is a requirement", "README.md"
    )
    ctx["repo_accessible_path_html"] = md_to_html(accessible) if accessible else ""

    # --- specimen sheets ----------------------------------------------------
    ctx["repo_sheets_html"] = render_sheets(readme)
    ctx.update(render_specimen(read_repo("docs/specimen.py", required=False)))

    # --- the worked example: a real reply to a real photograph --------------
    # Expected to be absent until the maintainer shoots one, so its absence is
    # a pending asset rather than a warning; the page carries a visible
    # placeholder naming this exact path.
    example_reply = (
        read_repo("docs/worked-example.md", required=False)
        if (ROOT / "docs/worked-example.md").exists()
        else None
    )
    if example_reply:
        _, example_body = strip_front_matter(example_reply)
        ctx["repo_example_reply_html"] = md_to_html(example_body, heading_offset=2)
    else:
        ctx["repo_example_reply_html"] = ""

    # --- §What comes out of the printer, and §Anatomy of a sheet ------------
    printer = extract_section(
        readme, "What comes out of the printer", "README.md", required=False
    )
    absences = (
        extract_paragraph(printer, "Notice what is", "README.md") if printer else None
    )
    ctx["repo_absences_html"] = md_to_html(absences) if absences else ""

    anatomy = extract_section(readme, "Anatomy of a sheet", "README.md", required=False)
    ctx["repo_anatomy_html"] = md_to_html(anatomy, heading_offset=2) if anatomy else ""
    if anatomy:
        floors = extract_paragraph(anatomy, "Hard floors", "README.md")
        voices = extract_paragraph(anatomy, "Three voices, never blended", "README.md")
        ctx["repo_hard_floors_html"] = md_to_html(floors) if floors else ""
        ctx["repo_three_voices_html"] = md_to_html(voices) if voices else ""
    else:
        ctx["repo_hard_floors_html"] = ""
        ctx["repo_three_voices_html"] = ""

    patterns = extract_section(readme, "The pattern library", "README.md", required=False)
    ctx["repo_patterns_html"] = (
        md_to_html(patterns, heading_offset=2) if patterns else ""
    )

    # --- the prompts a person types ----------------------------------------
    using = extract_section(readme, "Using it", "README.md", required=False)
    prompts = ""
    if using:
        fence = re.search(r"```[\w+-]*\n(.*?)```", using, re.S)
        if fence:
            prompts = fence.group(1).strip("\n")
    if prompts:
        lines = [esc(line) for line in prompts.split("\n") if line.strip()]
        ctx["repo_prompts_html"] = (
            '<ul class="prompts">'
            + "".join(f"<li>{line}</li>" for line in lines)
            + "</ul>"
        )
    else:
        warn("no example prompts found in README §Using it")
        ctx["repo_prompts_html"] = ""

    # --- the pen protocol tables -------------------------------------------
    pen = extract_section(readme, "The pen protocol", "README.md", required=False)
    if pen:
        span = find_first_table(pen)
        if span:
            plines = pen.split("\n")
            ctx["repo_ink_table_html"] = md_to_html("\n".join(plines[span[0] : span[1]]))
            rest = "\n".join(plines[span[1] :])
            span2 = find_first_table(rest)
            rlines = rest.split("\n")
            ctx["repo_mark_table_html"] = (
                md_to_html("\n".join(rlines[span2[0] : span2[1]])) if span2 else ""
            )
        ctx["repo_pen_protocol_html"] = md_to_html(pen, heading_offset=1)
    else:
        ctx["repo_ink_table_html"] = ""
        ctx["repo_mark_table_html"] = ""
        ctx["repo_pen_protocol_html"] = ""

    # --- the one rule -------------------------------------------------------
    one_rule = extract_section(
        readme, "The one rule everything else serves", "README.md", required=False
    )
    if one_rule:
        quote = re.search(r"^\s*>\s*(.+)$", one_rule, re.M)
        ctx["repo_one_rule"] = esc(plain_text(quote.group(1))) if quote else ""
        bullets = "\n".join(
            line for line in one_rule.split("\n") if line.strip().startswith("- ")
        )
        ctx["repo_one_rule_html"] = md_to_html(bullets) if bullets else ""
    else:
        ctx["repo_one_rule"] = ""
        ctx["repo_one_rule_html"] = ""

    # --- scan-back, in full -------------------------------------------------
    scanback = read_repo("scan-back/SKILL.md")
    assert scanback is not None
    meta, body = strip_front_matter(scanback)
    if not body.strip():
        raise BuildError("scan-back/SKILL.md is empty after front matter.")
    ctx["repo_scanback_name"] = esc(meta.get("name", "scan-back"))
    ctx["repo_scanback_description"] = esc(meta.get("description", ""))
    ctx["repo_scanback_html"] = md_to_html(body, heading_offset=1)
    ctx["repo_scanback_raw"] = esc(body)
    ctx["repo_scanback_bytes"] = str(len(scanback.encode("utf-8")))
    words = len(body.split())
    ctx["repo_scanback_words"] = str(words)
    ctx["repo_scanback_words_approx"] = f"{round(words / 100) * 100:,}"
    ctx["repo_scanback_raw_url"] = RAW_URL + "scan-back/SKILL.md"
    # The complete file, front matter included. `repo_scanback_raw` is the body
    # only — the right thing to hand a chat — but a page offering "the whole
    # file" should not have to reassemble the YAML, which would silently drop a
    # key the moment someone adds one.
    ctx["repo_scanback_full_raw"] = esc(scanback)
    unprinted = extract_paragraph(body, "Unprinted pages", "scan-back/SKILL.md")
    ctx["repo_scanback_unprinted_html"] = md_to_html(unprinted) if unprinted else ""

    # --- the dictated path: prompt-craft §10 and its notebook translation ---
    promptcraft = read_repo("paper-session/references/prompt-craft.md", required=False)
    dictation = (
        extract_section(
            promptcraft,
            "10. Dictating instead of printing",
            "paper-session/references/prompt-craft.md",
            required=False,
        )
        if promptcraft
        else None
    )
    ctx["repo_dictation_html"] = md_to_html(dictation) if dictation else ""
    if dictation:
        card = extract_paragraph(
            dictation,
            "The card is a single fenced message",
            "paper-session/references/prompt-craft.md",
        )
        budget = extract_paragraph(
            dictation,
            "If a design cannot be dictated inside the budget",
            "paper-session/references/prompt-craft.md",
        )
        ctx["repo_card_format_html"] = md_to_html(card) if card else ""
        ctx["repo_card_budget_html"] = md_to_html(budget) if budget else ""
    else:
        ctx["repo_card_format_html"] = ""
        ctx["repo_card_budget_html"] = ""

    patternlib = read_repo("paper-session/references/page-patterns.md", required=False)
    notebook = (
        extract_section(
            patternlib,
            "Notebook translation",
            "paper-session/references/page-patterns.md",
            required=False,
        )
        if patternlib
        else None
    )
    ctx["repo_notebook_translation_html"] = md_to_html(notebook) if notebook else ""
    formats = (
        extract_section(
            patternlib,
            "Named session formats",
            "paper-session/references/page-patterns.md",
            required=False,
        )
        if patternlib
        else None
    )
    ctx["repo_formats_html"] = md_to_html(formats) if formats else ""
    ctx.update(render_formats(formats))

    # --- paper-session SKILL.md metadata ------------------------------------
    forward = read_repo("paper-session/SKILL.md", required=False)
    if forward:
        fmeta, fbody = strip_front_matter(forward)
        ctx["repo_paper_session_description"] = esc(fmeta.get("description", ""))
        ctx["repo_paper_session_bytes"] = str(len(forward.encode("utf-8")))
        stop = re.search(r'"(Printed\.\s*Go think\.)"', fbody)
        ctx["repo_stop_line"] = esc(stop.group(1)) if stop else ""
    else:
        ctx["repo_paper_session_description"] = ""
        ctx["repo_paper_session_bytes"] = ""
        ctx["repo_stop_line"] = ""

    # --- the three numbers and the thesis -----------------------------------
    evidence = read_repo("paper-session/references/evidence.md")
    assert evidence is not None
    numbers_md = extract_section(
        evidence, "Three numbers", "paper-session/references/evidence.md"
    )
    assert numbers_md is not None
    numbers = []
    for line in numbers_md.split("\n"):
        match = re.match(r"^\s*[-*]\s+\*\*(.+?)\*\*\s*(.*)$", line)
        if match:
            label = match.group(1).strip().rstrip(".")
            rest = match.group(2).strip()
            first_sentence = re.split(r"(?<=[.!?])\s+", rest)[0] if rest else ""
            numbers.append({"label": label, "line": first_sentence})
    if len(numbers) < 3:
        raise BuildError(
            "could not parse three numbers out of evidence.md "
            "§Three numbers for the talk (found "
            f"{len(numbers)}). The landing page will not invent them."
        )
    ctx["repo_numbers_json"] = json.dumps(numbers, sort_keys=True)
    ctx["repo_numbers_html"] = render_numbers(numbers[:3])
    # The same three figures, each one a link to the entry on the evidence page
    # that states its conditions. A figure quoted with no route to its
    # limitations is the one thing this site is not allowed to do.
    ctx["repo_numbers_linked_html"] = render_numbers(
        numbers[:3], link_base=BASE_TOKEN + EVIDENCE_SLUG + "/"
    )

    thesis = re.findall(r"\*\*(.+?)\*\*", numbers_md)
    if thesis:
        fragment = thesis[-1].strip()
        ctx["repo_thesis"] = inline_md(fragment[:1].upper() + fragment[1:])
    else:
        ctx["repo_thesis"] = ""
    if not thesis:
        warn("no thesis sentence found in evidence.md §Three numbers")

    limitations = extract_section(
        evidence,
        "What the research does NOT support",
        "paper-session/references/evidence.md",
    )
    assert limitations is not None
    ctx["repo_limitations_html"] = md_to_html(limitations, heading_offset=1)
    ctx["repo_limitations_count"] = str(
        len(re.findall(r"^\s*\d+\.\s+", limitations, re.M))
    )

    # --- the rest of the evidence brief, section by section -----------------
    # The limitations page renders every one of these verbatim. All optional:
    # evidence.md is one of the files other agents edit, and a warning plus a
    # link is a better failure than a broken deploy.
    EVIDENCE = "paper-session/references/evidence.md"
    for key, heading in (
        ("repo_evidence_walking_html", "Bonus cluster: the physical case (walking)"),
        ("repo_evidence_cluster_4_html", "Cluster 4: The cost of staying on screen"),
        ("repo_evidence_cluster_5_html", "Cluster 5: What makes this urgent now"),
        ("repo_evidence_tension_html", "The tension you should address head-on"),
        (
            "repo_evidence_unprinted_html",
            "The unprinted page (what none of this tests)",
        ),
        (
            "repo_evidence_unread_html",
            "The unread page (what none of this tests, and what it costs)",
        ),
        ("repo_field_reports_html", "Part Three: Field reports"),
    ):
        section = extract_section(evidence, heading, EVIDENCE, required=False)
        ctx[key] = md_to_html(section, heading_offset=2) if section else ""

    # The brief's opening paragraph: everything above the first heading that
    # isn't the title or a rule.
    intro_lines: list[str] = []
    for line in evidence.split("\n"):
        if re.match(r"^#{1,6}\s+", line):
            if intro_lines:
                break
            continue
        if re.match(r"^\s*-{3,}\s*$", line):
            continue
        intro_lines.append(line)
    intro = "\n".join(intro_lines).strip()
    ctx["repo_evidence_intro_html"] = md_to_html(intro) if intro else ""
    if not intro:
        warn(f"no opening paragraph found above the first cluster in {EVIDENCE}")

    ctx.update(render_cluster_index(evidence))

    # --- the sheet's own footer line ----------------------------------------
    design = read_repo("paper-session/references/design.md", required=False)
    footer_line = ""
    if design:
        match = re.search(r'"(SCAN IT BACK TO CONTINUE\.)"', design)
        footer_line = match.group(1) if match else ""
    if not footer_line:
        warn("could not read the printed footer line out of design.md")
    ctx["repo_footer_line"] = esc(footer_line)

    return ctx


def ledger_chips(agent_md: str) -> list[str]:
    """Derive short chip labels from a ledger row's agent cell.

    Mechanical, so a README edit carries straight through: split on the middot,
    drop parentheticals, trim to something that fits on a chip.
    """
    text = plain_text(agent_md)
    text = re.sub(r"\([^)]*\)", "", text)
    parts = [p.strip(" ,") for p in re.split(r"[·•]", text) if p.strip(" ,")]
    chips = []
    for part in parts:
        label = part.strip()
        if len(label) > 20:
            cut = label[:20].rsplit(" ", 1)[0]
            label = (cut or label[:20]) + "…"
        if label:
            chips.append(label)
    return chips or [text[:20]]


def render_chips(rows: list[dict]) -> str:
    """Chip buttons. Hidden until JS unhides them; the table is the fallback."""
    out = []
    for index, row in enumerate(rows):
        for chip in row["chips"]:
            out.append(
                '<button type="button" class="chip" data-row="'
                f'{index}">{esc(chip)}</button>'
            )
    return "".join(out)


def render_numbers(numbers: list[dict], link_base: str = "") -> str:
    parts = []
    for index, number in enumerate(numbers, start=1):
        figure = inline_md(number["label"])
        if link_base:
            figure = (
                f'<a class="number__link" href="{link_base}#number-{index}">'
                f"{figure}</a>"
            )
        parts.append(
            '<li class="number">'
            f'<p class="number__figure">{figure}</p>'
            f'<p class="number__line">{inline_md(number["line"])}</p>'
            "</li>"
        )
    return "".join(parts)


def _literal(node: "ast.AST") -> str:
    """Best-effort text of a string literal or f-string in specimen.py."""
    import ast

    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    # An f-string's computed parts (the printed weekday) cannot be resolved
    # without running the generator, and half a title is worse than none:
    # report it as absent and let the caller omit it.
    return ""


def render_specimen(source: str | None) -> dict[str, str]:
    """The three specimen pages' own titles and intent lines.

    Parsed out of the generator with `ast`, not by hand: `docs/specimen.py` is
    regenerated whenever the design system changes, and a page describing what
    the three sheets contain must not be the one thing on this site that a
    regeneration silently falsifies.
    """
    import ast

    blank = {"repo_specimen_json": "[]", "repo_specimen_html": ""}
    if not source:
        return blank
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:  # pragma: no cover - generator mid-edit
        warn(f"docs/specimen.py does not parse ({exc}); specimen intents omitted")
        return blank
    pages = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Name) and func.id == "header"):
            continue
        args = [a for a in node.args][1:]  # drop the canvas
        if len(args) < 2:
            continue
        title, intent = _literal(args[0]), _literal(args[1])
        if intent:
            pages.append({"title": title, "intent": intent})
    if not pages:
        warn("no header() calls found in docs/specimen.py; specimen intents omitted")
        return blank
    items = "".join(
        "<li>"
        + (
            f'<span class="specimen-intents__title">{esc(page["title"])}</span>'
            if page["title"]
            else ""
        )
        + esc(page["intent"])
        + "</li>"
        for page in pages
    )
    return {
        "repo_specimen_json": json.dumps(pages, sort_keys=True).replace("</", "<\\/"),
        "repo_specimen_html": f'<ol class="specimen-intents">{items}</ol>',
    }


COUNTERWEIGHT_LEADS = (
    "the honest counterweight",
    "the honest counterweights",
    "boundary condition to disclose",
    "contraindications",
)


def render_cluster_index(evidence: str) -> dict[str, str]:
    """One entry per cluster in evidence.md, carrying its own counterweight.

    The point of the index is not navigation. It is that every cluster which
    argues against itself does so on the site too, in the brief's own words —
    so the audit section cannot read as a claim that the brief is unanimous.
    """
    lines = evidence.split("\n")
    part = "Part One"
    entries: list[str] = []
    count = 0
    headings = list(iter_headings(evidence))
    for position, (idx, level, text) in enumerate(headings):
        if level == 1:
            match = re.match(r"^(Part\s+\w+)", text.strip())
            if match:
                part = match.group(1)
            continue
        if not re.match(r"^(bonus\s+)?cluster\b", text.strip(), re.I):
            continue
        end = len(lines)
        for later_idx, later_level, _ in headings[position + 1 :]:
            if later_level <= level:
                end = later_idx
                break
        body = "\n".join(lines[idx + 1 : end])
        quotes = []
        for block in re.split(r"\n\s*\n", body):
            block = block.strip()
            if not block:
                continue
            opening = normalize_heading(block.split("\n")[0])
            if any(opening.startswith(lead) for lead in COUNTERWEIGHT_LEADS):
                quotes.append(md_to_html(block))
        count += 1
        entry = [
            "<li>",
            f'<p class="label">{esc(part)}</p>',
            f"<h3>{inline_md(text)}</h3>",
        ]
        if quotes:
            entry.append(
                '<div class="machine">'
                '<span class="caption">The honest counterweight</span>'
                + "".join(quotes)
                + "</div>"
            )
        entry.append("</li>")
        entries.append("".join(entry))
    if not entries:
        warn("no clusters parsed out of evidence.md; the cluster index is omitted")
        return {"repo_evidence_clusters_html": "", "repo_evidence_cluster_count": ""}
    return {
        "repo_evidence_clusters_html": "".join(entries),
        "repo_evidence_cluster_count": str(count),
    }


def render_formats(section: str | None) -> dict[str, str]:
    """Split §Named session formats into one key per format.

    Each format is a paragraph led by a bold name (`**Premortem.** …`). A page
    that wants to state a format's gate quotes `repo_format_<slug>_html`
    instead of paraphrasing the entry, which is the one thing on a page of
    session openers that can silently drift.
    """
    out: dict[str, str] = {
        "repo_formats_json": "[]",
        "repo_formats_count": "",
        "repo_formats_intro_html": "",
    }
    if not section:
        return out
    lines = section.split("\n")
    lead = re.compile(r"^\*\*([A-Z][^*]{2,60}?)\.\*\*\s")
    starts = [i for i, line in enumerate(lines) if lead.match(line)]
    if not starts:
        warn("no named session formats parsed out of page-patterns.md")
        return out
    out["repo_formats_intro_html"] = md_to_html("\n".join(lines[: starts[0]]).strip())
    entries = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start:end]).strip()
        match = lead.match(lines[start])
        assert match is not None
        name = match.group(1).strip()
        slug = slugify(name)
        key = "repo_format_" + slug.replace("-", "_") + "_html"
        html_block = md_to_html(block)
        out[key] = html_block
        entries.append({"name": name, "slug": slug, "key": key, "html": html_block})
    out["repo_formats_json"] = json.dumps(entries, sort_keys=True).replace("</", "<\\/")
    out["repo_formats_count"] = str(len(entries))
    return out


def render_sheets(readme: str) -> str:
    """The three specimen images, with README's own alt text and captions."""
    span = None
    lines = readme.split("\n")
    for i in range(len(lines) - 1):
        if "docs/sheet-" in lines[i] and "|" in lines[i]:
            for j in range(i, max(-1, i - 4), -1):
                if "|" in lines[j] and _TABLE_DELIM.match(lines[j + 1] if j + 1 < len(lines) else ""):
                    span = j
                    break
            break
    if span is None:
        warn("no specimen table found in README; sheet gallery omitted")
        return ""
    headers = _split_row(lines[span])
    body_rows = []
    k = span + 2
    while k < len(lines) and "|" in lines[k] and lines[k].strip():
        body_rows.append(_split_row(lines[k]))
        k += 1
    if not body_rows:
        return ""
    images = body_rows[0]
    notes = body_rows[1] if len(body_rows) > 1 else [""] * len(images)
    figures = []
    for index, cell in enumerate(images):
        match = re.search(r"!\[([^\]]*)\]\(([^)\s]+)\)", cell)
        if not match:
            continue
        alt, src = match.group(1), resolve_image(match.group(2))
        caption = plain_text(headers[index]) if index < len(headers) else ""
        note = notes[index] if index < len(notes) else ""
        figures.append(
            '<figure class="sheet">'
            f'<img src="{src}" alt="{esc(alt)}" width="773" height="1000" '
            'loading="lazy" decoding="async">'
            f'<figcaption><span class="label">{esc(caption)}</span>'
            f'<span class="sheet__note">{inline_md(note)}</span></figcaption>'
            "</figure>"
        )
    return "".join(figures)


# --------------------------------------------------------------------------
# The templater
# --------------------------------------------------------------------------

INCLUDE_RE = re.compile(r'\{%\s*include\s+"([^"]+)"\s*%\}')
IF_OPEN_RE = re.compile(r"\{%\s*if\s+([a-zA-Z0-9_]+)\s*%\}")
VAR_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*(\|\s*e\s*)?\}\}")


def expand_includes(text: str, origin: str, depth: int = 0) -> str:
    if depth > 8:
        raise BuildError(f"include loop in {origin}")

    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        path = TEMPLATES / name
        if not path.exists():
            raise BuildError(f"{origin} includes missing partial: templates/{name}")
        return expand_includes(path.read_text(encoding="utf-8"), name, depth + 1)

    return INCLUDE_RE.sub(repl, text)


def apply_conditionals(text: str, ctx: dict[str, str], origin: str) -> str:
    """{% if key %} ... {% else %} ... {% endif %}, nesting supported."""
    while True:
        match = IF_OPEN_RE.search(text)
        if not match:
            break
        key = match.group(1)
        pos = match.end()
        depth = 1
        else_at = None
        cursor = pos
        pattern = re.compile(r"\{%\s*(if\s+[a-zA-Z0-9_]+|else|endif)\s*%\}")
        while True:
            token = pattern.search(text, cursor)
            if token is None:
                raise BuildError(f"unclosed {{% if {key} %}} in {origin}")
            word = token.group(1)
            if word.startswith("if"):
                depth += 1
            elif word == "else" and depth == 1:
                else_at = token.span()
            elif word == "endif":
                depth -= 1
                if depth == 0:
                    end = token.span()
                    break
            cursor = token.end()
        if else_at:
            truthy = text[pos : else_at[0]]
            falsy = text[else_at[1] : end[0]]
        else:
            truthy = text[pos : end[0]]
            falsy = ""
        chosen = truthy if is_truthy(ctx.get(key, "")) else falsy
        text = text[: match.start()] + chosen + text[end[1] :]
    return text


def substitute(text: str, ctx: dict[str, str], origin: str) -> str:
    missing: list[str] = []

    def repl(match: re.Match[str]) -> str:
        key, escape = match.group(1), match.group(2)
        if key not in ctx:
            missing.append(key)
            return ""
        value = str(ctx[key])
        return esc(value) if escape else value

    out = VAR_RE.sub(repl, text)
    if missing:
        raise BuildError(
            f"{origin} uses unknown template keys: "
            + ", ".join(sorted(set(missing)))
            + "\n  Available keys are listed in site/README.md. Repo content "
            "keys are defined in build_repo_context() in site/build.py."
        )
    return out


def render(text: str, ctx: dict[str, str], origin: str) -> str:
    text = expand_includes(text, origin)
    text = apply_conditionals(text, ctx, origin)
    return substitute(text, ctx, origin)


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

FRONT_MATTER_RE = re.compile(r"^\s*<!--\s*page\s*(.*?)-->", re.S)


def parse_page(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(raw)
    if not match:
        raise BuildError(
            f"templates/{path.name} has no front matter.\n"
            "  Every page template must start with:\n"
            "    <!--page\n    title: ...\n    description: ...\n    -->"
        )
    meta: dict[str, str] = {}
    for line in match.group(1).split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise BuildError(
                f"templates/{path.name} front matter line is not `key: value`: {line}"
            )
        meta[key.strip()] = value.strip()
    for required in ("title", "description"):
        if not meta.get(required):
            raise BuildError(
                f"templates/{path.name} front matter is missing `{required}:`"
            )
    meta.setdefault("slug", path.stem)
    meta["body"] = raw[match.end() :].lstrip("\n")
    meta["template_name"] = path.name
    return meta


def output_path_for(slug: str) -> str:
    return "index.html" if slug == "index" else f"{slug}/index.html"


def base_prefix_for(output: str) -> str:
    return "../" * output.count("/")


def stub_body(page: dict[str, str]) -> str:
    """A page that is planned but not written yet. Obviously unfinished."""
    return f"""
<article class="band air-2">
  <div class="wrap measure">
    <p class="label">Not written yet</p>
    <h1 class="page-title">{esc(page['title'])}</h1>
    <p class="intent">{esc(page['description'])}</p>
    <p>This page is a placeholder emitted by <code>site/build.py</code> so that
    nothing on the site links into a hole. It disappears the moment a template
    called <code>templates/{esc(page['slug'])}.html</code> exists.</p>
    <p><a href="{{{{ home_url }}}}">Back to the front page</a></p>
  </div>
</article>
""".strip()


def collect_pages() -> list[dict[str, str]]:
    if not TEMPLATES.is_dir():
        raise BuildError(f"no templates directory at {TEMPLATES}")
    pages: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in sorted(TEMPLATES.glob("*.html")):
        if path.name.startswith("_"):
            continue
        page = parse_page(path)
        if page["slug"] in seen:
            raise BuildError(f"two templates claim slug {page['slug']}")
        seen.add(page["slug"])
        pages.append(page)
    for planned in PLANNED_PAGES:
        if planned["slug"] in seen:
            continue
        page = dict(planned)
        page["body"] = stub_body(planned)
        page["template_name"] = f"(stub for {planned['slug']})"
        page["stub"] = "1"
        pages.append(page)
    pages.sort(key=lambda p: (int(p.get("nav_order", "999") or 999), p["slug"]))
    return pages


def render_nav(pages: list[dict[str, str]], current: str, base: str) -> str:
    items = []
    for page in pages:
        label = page.get("nav_label")
        if not label:
            continue
        target = base + ("" if page["slug"] == "index" else f"{page['slug']}/")
        current_attr = ' aria-current="page"' if page["slug"] == current else ""
        items.append(f'<li><a href="{target}"{current_attr}>{esc(label)}</a></li>')
    return "<ul class=\"nav__list\">" + "".join(items) + "</ul>"


# --------------------------------------------------------------------------
# Assets
# --------------------------------------------------------------------------


def copy_assets(dist: Path, allow_missing: bool) -> dict[str, str]:
    ctx: dict[str, str] = {}
    missing: list[str] = []

    if STATIC.is_dir():
        for src in sorted(STATIC.rglob("*")):
            if src.is_dir():
                continue
            rel = src.relative_to(STATIC)
            dest = dist / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
    else:
        warn(f"no static directory at {STATIC}")

    for src_rel, dest_rel in ASSET_FILES.items():
        src = ROOT / src_rel
        if not src.exists():
            missing.append(src_rel)
            continue
        dest = dist / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    sheet_count = 0
    for pattern, dest_dir in ASSET_GLOBS.items():
        matches = sorted((ROOT / Path(pattern).parent).glob(Path(pattern).name))
        if not matches:
            missing.append(pattern)
            continue
        for src in matches:
            dest = dist / dest_dir / src.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            sheet_count += 1

    if missing:
        message = (
            "specimen assets are missing from the repo: "
            + ", ".join(missing)
            + "\n  Regenerate them with:  python3 docs/specimen.py\n"
            "  (Another agent may be rebuilding them right now.)\n"
            "  To build the site anyway, with the downloads marked "
            "unavailable, pass --allow-missing-assets."
        )
        if not allow_missing:
            raise BuildError(message)
        warn(message)

    # Derived from what actually landed in dist/, not from the name of the
    # source that was supposed to produce it: a page must never offer a
    # download that is not there.
    ctx["specimen_available"] = "1" if (dist / "specimen.pdf").exists() else ""
    ctx["sheet_count"] = str(sheet_count)

    hero = next((name for name in HERO_CANDIDATES if (STATIC / name).exists()), "")
    ctx["hero_present"] = "1" if hero else ""
    ctx["hero_file"] = hero

    example = next(
        (name for name in EXAMPLE_CANDIDATES if (STATIC / name).exists()), ""
    )
    ctx["example_present"] = "1" if example else ""
    ctx["example_file"] = example

    write_sheet_spec(dist)
    return ctx


# --------------------------------------------------------------------------
# The sheet spec: design.md -> CSS custom properties
# --------------------------------------------------------------------------


def write_sheet_spec(dist: Path) -> None:
    """Prefix dist/style.css with the block generated from design.md.

    static/style.css is hand-authored and contains no number that also lives in
    design.md; every such number arrives as a `--ps-*` custom property emitted
    by sheetspec.py. Joining them here rather than linking a second stylesheet
    means no template has to know the spec exists, and it means there is exactly
    one place a sheet's numbers can come from.

    The bundled faces travel with it. design.md §1 registers eight files by
    exact name; the generated @font-face rules point at dist/fonts/, so the
    printed sheet is laid out on the metrics of the files the spec names rather
    than on a CDN copy that may not arrive or a fallback face the gate would
    happily measure without complaint.
    """
    try:
        spec = sheetspec.load_spec()
        generated = sheetspec.emit_css(spec)
    except sheetspec.SpecError as exc:
        raise BuildError(
            f"{exc}\n  The site's sheet is generated from design.md and has no "
            f"numbers of its own, so this stops the build rather than falling "
            f"back to a stale copy."
        ) from exc

    source = STATIC / "style.css"
    if not source.exists():
        raise BuildError(f"missing stylesheet: {source}")
    (dist / "style.css").write_text(
        generated + "\n" + source.read_text(encoding="utf-8"), encoding="utf-8"
    )

    fonts_dir = dist / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    wanted = sheetspec.font_files(spec) + [sheetspec.FONT_LICENSE]
    for name in wanted:
        src = sheetspec.FONT_DIR / name
        if not src.exists():
            raise BuildError(
                f"design.md §1 registers {name}, which is not in "
                f"{sheetspec.FONT_DIR}. The sheet cannot be set in a face the "
                f"spec does not ship, and the licence travels with the fonts."
            )
        shutil.copy2(src, fonts_dir / name)


# --------------------------------------------------------------------------
# The verify gate: render every declared sheet and run the project's verifier
# --------------------------------------------------------------------------

# Chromium candidates, in preference order.
CHROMIUM_NAMES = (
    "chromium",
    "chromium-browser",
    "google-chrome",
    "google-chrome-stable",
)

VERIFIER = ROOT / "paper-session" / "scripts" / "verify_layout.py"

# design.md §0: the page box every sheet prints on. Read from the spec rather
# than typed, then asserted against what actually came out of the browser.
MEDIABOX_TOLERANCE_PT = 1.0

MEDIABOX_RE = re.compile(
    r"/MediaBox\s*\[\s*(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s*\]"
)
PAGE_COUNT_RE = re.compile(rb"/Type\s*/Pages\b[^>]*?/Count\s+(\d+)")


def find_chromium() -> str | None:
    for name in CHROMIUM_NAMES:
        found = shutil.which(name)
        if found:
            return found
    return None


def print_to_pdf(browser: str, page: Path, out: Path) -> None:
    """Print one built page to PDF, hermetically.

    No margins: design.md §0 puts the footer BELOW the margin box, so the
    generated @page rule sets margin 0 and the sheet element carries the 54pt
    margins itself. Name resolution is blackholed so the render cannot depend
    on a webfont CDN answering — the faces the sheet uses are on disk beside it,
    and a gate whose result changes with the network is not a gate.
    """
    with tempfile.TemporaryDirectory(prefix="ps-chrome-") as profile:
        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=8000",
            "--host-resolver-rules=MAP * ~NOTFOUND",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={out}",
            page.as_uri(),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if proc.returncode != 0 or not out.exists():
        raise BuildError(
            "chromium could not print the sheet to PDF.\n"
            f"    command: {' '.join(cmd)}\n"
            f"    exit {proc.returncode}\n"
            + "".join(f"    {line}\n" for line in proc.stderr.splitlines()[-12:])
        )


def pdf_page_geometry(pdf: Path) -> tuple[int, tuple[float, float]]:
    """Page count and the first /MediaBox, read without leaving the stdlib."""
    raw = pdf.read_bytes()
    count_match = PAGE_COUNT_RE.search(raw)
    if not count_match:
        raise BuildError(f"{pdf.name}: no page tree in the PDF chromium produced.")
    box_match = MEDIABOX_RE.search(raw.decode("latin-1", "replace"))
    if not box_match:
        raise BuildError(f"{pdf.name}: no /MediaBox in the PDF chromium produced.")
    x0, y0, x1, y1 = (float(v) for v in box_match.groups())
    return int(count_match.group(1)), (abs(x1 - x0), abs(y1 - y0))


def verify_sheets(dist: Path, pages: list[dict[str, str]], strict: bool) -> None:
    """Render every page that declares a sheet and run verify_layout.py on it.

    This is the rule the whole arrangement exists for: a live HTML sheet is
    coupled to design.md and to the project's own verifier, or it does not
    exist. A hand-written CSS restatement of the print system is a second spec
    with no gate, and two specs drift.

    verify_layout.py is the same script SKILL.md makes mandatory before any
    sheet is shown to a human. It catches text escaping the page, words
    colliding across baselines, and glyphs colliding on a shared baseline. It is
    deliberately narrow and does not check the design system; the page box and
    the page count are checked here, because a sheet that has quietly become two
    pages ends with a rule and nothing under it.
    """
    declared = [p for p in pages if is_truthy(p.get("sheet", ""))]
    if not declared:
        return

    names = ", ".join(p["slug"] for p in declared)
    browser = find_chromium()
    if browser is None or not VERIFIER.exists():
        reason = (
            "no chromium on PATH (looked for " + ", ".join(CHROMIUM_NAMES) + ")"
            if browser is None
            else f"the verifier is missing at {VERIFIER}"
        )
        message = (
            f"THE SHEET GATE DID NOT RUN: {reason}.\n"
            f"    {len(declared)} page(s) declare a live sheet ({names}) and "
            f"NONE of them were verified.\n"
            f"    Install chromium and rebuild. A gate that quietly does "
            f"nothing reads as verified, which is worse than no gate."
        )
        if strict:
            raise BuildError(message)
        warn(message)
        return

    spec = sheetspec.load_spec()
    want_w = float(spec["page"]["page_w"])
    want_h = float(spec["page"]["page_h"])

    with tempfile.TemporaryDirectory(prefix="ps-gate-") as tmp:
        for page in declared:
            output = page.get("output") or output_path_for(page["slug"])
            built = dist / output
            pdf = Path(tmp) / f"{page['slug']}.pdf"
            print(f"  gate: printing /{page['slug']}/ with {Path(browser).name}")
            print_to_pdf(browser, built, pdf)

            count, (width, height) = pdf_page_geometry(pdf)
            expected = int(page.get("sheet_pages", "1"))
            if count != expected:
                raise BuildError(
                    f"/{page['slug']}/ printed {count} page(s), expected "
                    f"{expected}.\n    A sheet that spills onto a second page "
                    f"hands the reader a rule with nothing under it. Shorten "
                    f"the content, or declare sheet_pages in the front matter "
                    f"if the extra page is real."
                )
            if (
                abs(width - want_w) > MEDIABOX_TOLERANCE_PT
                or abs(height - want_h) > MEDIABOX_TOLERANCE_PT
            ):
                raise BuildError(
                    f"/{page['slug']}/ printed at {width:.1f} x {height:.1f} pt, "
                    f"but design.md §0 specifies {want_w:.0f} x {want_h:.0f} pt. "
                    f"The @page rule is generated from the spec, so something "
                    f"on the page is overriding it."
                )

            proc = subprocess.run(
                [sys.executable, str(VERIFIER), str(pdf)],
                capture_output=True,
                text=True,
            )
            report = (proc.stdout + proc.stderr).strip().replace(
                str(pdf), f"/{page['slug']}/"
            )
            if proc.returncode != 0:
                raise BuildError(
                    f"verify_layout.py failed on /{page['slug']}/.\n"
                    + "".join(f"    {line}\n" for line in report.splitlines())
                    + "    design.md §8: never present a sheet that has not "
                    "passed. Fix the layout and rebuild."
                )
            for line in report.splitlines():
                print(f"  gate: {line}")


# --------------------------------------------------------------------------
# Link checking
# --------------------------------------------------------------------------

LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')


def check_links(dist: Path, strict: bool) -> None:
    dangling: list[str] = []
    for page in sorted(dist.rglob("*.html")):
        for target in LINK_RE.findall(page.read_text(encoding="utf-8")):
            if re.match(r"^(https?:|mailto:|#|data:|//)", target):
                continue
            path, _, _ = target.partition("#")
            path, _, _ = path.partition("?")
            if not path:
                continue
            resolved = (page.parent / path).resolve()
            if resolved.is_dir():
                resolved = resolved / "index.html"
            if not resolved.exists():
                dangling.append(f"{page.relative_to(dist)} -> {target}")
    if dangling:
        message = "internal links point at nothing:\n    " + "\n    ".join(dangling)
        if strict:
            raise BuildError(message)
        warn(message)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------


def build(dist: Path, allow_missing: bool, strict: bool) -> None:
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir(parents=True)

    print(f"  reading repo content from {ROOT}")
    repo_ctx = build_repo_context()
    asset_ctx = copy_assets(dist, allow_missing)
    (dist / ".nojekyll").write_text("", encoding="utf-8")

    base_template_path = TEMPLATES / "_base.html"
    if not base_template_path.exists():
        raise BuildError(f"missing shell template: {base_template_path}")
    base_template = base_template_path.read_text(encoding="utf-8")

    pages = collect_pages()
    written = 0
    for page in pages:
        output = page.get("output") or output_path_for(page["slug"])
        base = base_prefix_for(output)

        ctx: dict[str, str] = {}
        ctx.update(repo_ctx)
        ctx.update(asset_ctx)
        ctx.update({k: v for k, v in page.items() if k not in ("body",)})
        ctx["base"] = base
        ctx["home_url"] = base or "./"
        ctx["page_slug"] = page["slug"]
        ctx["is_home"] = "1" if page["slug"] == "index" else ""
        ctx["nav"] = render_nav(pages, page["slug"], base)
        ctx["repo_url"] = REPO_URL
        ctx["raw_url"] = RAW_URL
        ctx["specimen_url"] = base + "specimen.pdf"
        ctx["hero_url"] = base + (asset_ctx["hero_file"] or "")
        ctx["example_photo_url"] = base + (asset_ctx["example_file"] or "")
        ctx["evidence_url"] = base + EVIDENCE_SLUG + "/"
        ctx["body_class"] = page.get("body_class", "")

        # Repo fragments carry a base token so one conversion serves every depth.
        for key, value in list(ctx.items()):
            if isinstance(value, str) and BASE_TOKEN in value:
                ctx[key] = value.replace(BASE_TOKEN, base)

        body = render(page["body"], ctx, page["template_name"])
        ctx["content"] = body
        html_out = render(base_template, ctx, "_base.html")

        dest = dist / output
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html_out.strip() + "\n", encoding="utf-8")
        written += 1
        flag = "  (stub)" if page.get("stub") else ""
        print(f"  wrote {output}{flag}")

    check_links(dist, strict)
    verify_sheets(dist, pages, strict)
    print(f"  {written} pages -> {dist}")
    if WARNINGS:
        print(f"  {len(WARNINGS)} warning(s)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", default=str(DIST_DEFAULT), help="output directory")
    parser.add_argument(
        "--allow-missing-assets",
        action="store_true",
        help="warn instead of failing when docs/specimen.pdf or the sheet PNGs "
        "are absent (another agent may be regenerating them)",
    )
    parser.add_argument(
        "--strict", action="store_true", help="treat dangling internal links as errors"
    )
    parser.add_argument("--serve", type=int, metavar="PORT", help="serve dist/ after building")
    args = parser.parse_args(argv)

    dist = Path(args.out).resolve()
    try:
        build(dist, args.allow_missing_assets, args.strict)
    except BuildError as exc:
        print(f"\nbuild failed: {exc}\n", file=sys.stderr)
        return 1

    if args.serve:
        import functools
        import http.server
        import socketserver

        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(dist))
        with socketserver.TCPServer(("", args.serve), handler) as httpd:
            print(f"  serving {dist} at http://localhost:{args.serve}/  (ctrl-c to stop)")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
