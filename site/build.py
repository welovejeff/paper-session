#!/usr/bin/env python3
"""Build the paper-session promotional site.

Static site generator, Python standard library only. No Node, no jinja2, no
third-party anything: this repo's dependency list is reportlab + pdfplumber and
the website is not allowed to add a third.

The rule this script exists to enforce
--------------------------------------
Nothing on the site is hand-copied from the repo. The install commands, the
bundle links, the ledger's verdicts and the whole text of scan-back/SKILL.md
(behind its copy button) are READ FROM THE SOURCE FILE at build time and
converted to HTML here. CLAUDE.md binds install directions to README §Install
and nowhere else; this file is what makes that mechanical instead of a
promise. If you are about to type a repo command into a template, add an
extractor here instead. Whole repo documents are linked on GitHub, not
embedded.

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

# Where the site is served. Only absolute URLs use it (canonical links, og:url,
# og:image, the redirect pages' canonical); every link a visitor follows stays
# relative through {{ base }}, so a preview served under a subpath still works.
SITE_URL = "https://paper-session.com/"

# The page that carries the honest limits. Named once, because build.py
# generates links into it and a template must never guess at the slug.
RESEARCH_SLUG = "research"

# Retired slugs, and where each one now lands (relative to the site root; a
# fragment is allowed, "" is the front page). Every old link keeps working: the
# build writes dist/<old>/index.html as a meta-refresh page, the strict link
# checker follows its <a>, and a fragment target must exist as an id on the
# page it names. A retired slug may never come back as a live page; the build
# refuses that rather than letting a redirect shadow a real page.
REDIRECTS = {
    "get-a-sheet": "",
    "first-session": "how-it-works/",
    "scan-back": "install/#scan-back",
    "no-printer": "install/#no-printer",
    "evidence": RESEARCH_SLUG + "/",
}

# Repo files copied into dist/, source -> dist-relative path. None today: the
# specimen PDF is not published, because the site offers no generic printable
# sheet (see site/README.md, "Retired pages redirect").
ASSET_FILES: dict[str, str] = {}
# The one specimen render a page shows: How it works, "As printed". Copy only
# what a page uses; an unlinked sheet render at a site URL is a generic sheet
# by another name.
ASSET_GLOBS = {
    "docs/sheet-deep-react.png": "sheets/",
}
# Repo paths that must resolve to a site asset rather than to GitHub when they
# appear as a link or image in extracted markdown.
ASSET_LINK_MAP: dict[str, str] = {}

# Hero photograph: the maintainer drops one of these into site/static/.
HERO_CANDIDATES = ("hero.jpg", "hero.jpeg", "hero.png", "hero.webp")

# Hero film: when site/static/film.mp4 is present it takes the hero slot, with
# an optional poster frame and WebVTT captions beside it. Without the MP4 the
# landing page falls back to the hero photograph.
FILM_FILE = "film.mp4"
FILM_POSTER_CANDIDATES = ("film-poster.jpg", "film-poster.jpeg", "film-poster.png", "film-poster.webp")
FILM_CAPTIONS_FILE = "film-captions.vtt"

# The text the primary call to action copies, and the file it opens with
# JavaScript off. The visitor pastes it into the AI chat they already use.
COPY_INSTRUCTIONS_FILE = "copy-instructions.txt"

# The worked example on How it works ("As photographed"): a photograph of a
# real completed page, shown beside the specimen render of the same sheet.
EXAMPLE_CANDIDATES = (
    "return-example.jpg",
    "return-example.jpeg",
    "return-example.png",
    "return-example.webp",
)

# Pages the site plans to have. A page exists as soon as a template with the
# matching slug lands in site/templates/; until then build.py emits a marked
# stub so no link on the site dangles. Page authors: drop in your template and
# your stub disappears. The site is four pages: the front page (no nav entry;
# the wordmark is its link) and these three, in this nav order.
PLANNED_PAGES = [
    {
        "slug": "how-it-works",
        "title": "How it works",
        "nav_label": "How it works",
        "nav_order": "10",
        "description": "One session from start to finish: a page is printed, "
        "you think on paper, and the work picks up from your handwriting.",
    },
    {
        "slug": "install",
        "title": "Install",
        "nav_label": "Install",
        "nav_order": "20",
        "description": "Both halves of the loop in the AI you already use, "
        "so it can print a page and read your handwriting back.",
    },
    {
        "slug": RESEARCH_SLUG,
        "title": "Research",
        "nav_label": "Research",
        "nav_order": "30",
        "description": "What has been tested, what has not, and what we do "
        "not know yet.",
    },
]

# The masthead's last item, after the planned pages: the repository itself.
NAV_EXTERNAL = [("GitHub", REPO_URL)]


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
# Inline markdown -> HTML
# --------------------------------------------------------------------------
#
# Pages link to whole repo documents instead of embedding them, so there is no
# block-level converter: repo text reaches a page as an escaped string or, for
# a line of links, through inline_md (bold / italic / strikethrough / code /
# links / images).

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


def fenced_blocks(md: str) -> list[str]:
    """The body of every fenced code block in `md`, in order, fences removed."""
    blocks: list[str] = []
    lines = md.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        fence = re.match(r"^\s*(`{3,}|~{3,})\s*([\w+-]*)\s*$", lines[i])
        if not fence:
            i += 1
            continue
        marker = re.escape(fence.group(1)[0])
        body: list[str] = []
        i += 1
        while i < len(lines) and not re.match(rf"^\s*{marker}{{3,}}\s*$", lines[i]):
            body.append(lines[i])
            i += 1
        blocks.append("\n".join(body).strip("\n"))
        i += 1
    return blocks


def install_command(blocks: list[str], needle: str, key: str) -> str:
    """The escaped text of the first README §Install fenced block holding `needle`."""
    for block in blocks:
        if needle in block:
            return esc(block)
    raise BuildError(
        f"README §Install has no fenced code block containing “{needle}”, so "
        f"{key} has nothing to show and the site will not type the command itself."
    )


def github_anchor(heading: str) -> str:
    """The id GitHub gives a markdown heading: lowercased, punctuation dropped,
    spaces to hyphens. Emphasis and code markers go first; underscores stay,
    because GitHub keeps them."""
    text = re.sub(r"`([^`]*)`", r"\1", heading)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*~]+", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def repo_doc_url(relpath: str, key: str, heading: str | None = None) -> str:
    """A GitHub link to a repo document, and to one of its headings if named.

    Pages link to whole documents rather than embedding them. The link is built
    here, not typed into a template, so a moved file or a renamed heading stops
    the build instead of shipping a link into a 404 or a dead anchor. The
    anchor is computed from the heading as it is actually written, so an
    appended parenthetical follows through on its own.
    """
    text = read_repo(relpath, required=False) if (ROOT / relpath).exists() else None
    if text is None:
        raise BuildError(
            f"{relpath} is missing, so {key} would link to a page GitHub cannot show."
        )
    if heading is None:
        return BLOB_URL + relpath
    target = normalize_heading(heading)
    for _, _, found in iter_headings(text):
        norm = normalize_heading(found)
        if norm == target or norm.startswith(target):
            return BLOB_URL + relpath + "#" + github_anchor(found)
    raise BuildError(
        f"{relpath} has no heading starting “{heading}”, so {key} would link "
        f"to an anchor that does not exist."
    )


# --------------------------------------------------------------------------
# Repo content -> template context
# --------------------------------------------------------------------------


def build_repo_context() -> dict[str, str]:
    """Every piece of repo content the site is allowed to show.

    Add an entry here when a page needs repo content. Do not type repo prose
    into a template, and do not embed a whole document: link it with
    repo_doc_url() instead.
    """
    ctx: dict[str, str] = {}

    readme = read_repo("README.md")
    assert readme is not None

    # --- README §Install: commands, bundles, ledger verdicts ----------------
    install = extract_section(readme, "Install", "README.md", required=True)
    assert install is not None
    span = find_first_table(install)
    if span is None:
        raise BuildError(
            "README §Install has no compatibility table.\n"
            "  The Install page shows each row's verdict from it and links the "
            "full table; it may not invent one."
        )
    # The ledger's own subheading, directly above the table: the anchor the
    # Install page links to for the full table on GitHub.
    ilines = install.split("\n")
    ledger_heading = ""
    for k in range(span[0] - 1, -1, -1):
        if re.match(r"^#{2,6}\s+", ilines[k]):
            ledger_heading = re.sub(r"^#{2,6}\s+", "", ilines[k]).strip()
            break
        if ilines[k].strip():
            break
    headers, rows = parse_table(install)
    if not rows:
        raise BuildError("README §Install ledger parsed to zero rows.")
    ctx.update(render_install_keys(install, ledger_heading, headers, rows))

    # --- scan-back/SKILL.md, behind the Install page's copy button ----------
    # The body only, front matter dropped: the part a chat needs pasted.
    scanback = read_repo("scan-back/SKILL.md")
    assert scanback is not None
    _, body = strip_front_matter(scanback)
    if not body.strip():
        raise BuildError("scan-back/SKILL.md is empty after front matter.")
    ctx["repo_scanback_raw"] = esc(body)
    words = len(body.split())
    ctx["repo_scanback_words_approx"] = f"{round(words / 100) * 100:,}"
    ctx["repo_scanback_raw_url"] = RAW_URL + "scan-back/SKILL.md"

    # --- the skill's stop line ----------------------------------------------
    forward = read_repo("paper-session/SKILL.md", required=False)
    stop = (
        re.search(r'"(Printed\.\s*Go think\.)"', strip_front_matter(forward)[1])
        if forward
        else None
    )
    ctx["repo_stop_line"] = esc(stop.group(1)) if stop else ""

    # --- links to whole repo documents ---------------------------------------
    # The site links documents instead of embedding them. Each link is checked
    # against the file (and the heading, when it names one) at build time.
    ctx["repo_readme_install_url"] = repo_doc_url(
        "README.md", "repo_readme_install_url", "Install"
    )
    ctx["repo_evidence_doc_url"] = repo_doc_url(
        "paper-session/references/evidence.md", "repo_evidence_doc_url"
    )
    ctx["repo_evidence_limits_url"] = repo_doc_url(
        "paper-session/references/evidence.md",
        "repo_evidence_limits_url",
        "What the research does NOT support",
    )
    ctx["repo_formats_doc_url"] = repo_doc_url(
        "paper-session/references/page-patterns.md",
        "repo_formats_doc_url",
        "Named session formats",
    )
    ctx["repo_dictation_doc_url"] = repo_doc_url(
        "paper-session/references/prompt-craft.md",
        "repo_dictation_doc_url",
        "10. Dictating instead of printing",
    )

    return ctx


def render_install_keys(
    install: str,
    ledger_heading: str,
    headers: list[str],
    rows: list[list[str]],
) -> dict[str, str]:
    """README §Install, cut down to what the Install and Research pages show.

    Every value is the README's own text or href, or a count of its rows.
    Nothing is paraphrased, and a missing source is a failed build rather than
    an empty slot.
    """
    out: dict[str, str] = {}

    # The three commands, each the whole fenced block that holds it.
    blocks = fenced_blocks(install)
    out["repo_install_npx_cmd"] = install_command(
        blocks, "npx skills add", "repo_install_npx_cmd"
    )
    out["repo_install_clone_cmd"] = install_command(
        blocks, "git clone", "repo_install_clone_cmd"
    )
    out["repo_install_pip_cmd"] = install_command(
        blocks, "pip install", "repo_install_pip_cmd"
    )

    # The two bundles, from the paragraph that links them, with its hrefs.
    bundle_link = re.compile(r"\[([^\]]+)\]\(([^)\s]+\.skill)\)")
    paragraph = next(
        (
            block
            for block in re.split(r"\n\s*\n", install)
            if len(bundle_link.findall(block)) >= 2
        ),
        None,
    )
    links = bundle_link.findall(paragraph) if paragraph else []
    hrefs = [href for _, href in links]
    if not (
        any(h.endswith("/paper-session.skill") for h in hrefs)
        and any(h.endswith("/scan-back.skill") for h in hrefs)
    ):
        raise BuildError(
            "README §Install has no paragraph linking both paper-session.skill "
            "and scan-back.skill, so repo_bundle_links_html has nothing to offer."
        )
    # Each one a button, so the chat-app track reads as a first-class route
    # beside the terminal track's code blocks (CLAUDE.md: neither is favoured).
    out["repo_bundle_links_html"] = " ".join(
        inline_md(f"[{label}]({href})").replace("<a ", '<a class="btn" ', 1)
        for label, href in links
    )

    # One verdict per ledger row: the agent cell as plain text, and the bold
    # phrase that opens "The loop today", verbatim. A row with no bold phrase
    # there ("Same as above") carries the row above's verdict.
    wanted = "the loop today"
    column = next(
        (i for i, h in enumerate(headers) if plain_text(h).lower() == wanted), None
    )
    if column is None:
        raise BuildError(
            "the README ledger has no “The loop today” column, so "
            "repo_ledger_verdicts_html has no verdicts to show."
        )
    items: list[str] = []
    verdicts: list[str] = []
    previous = ""
    for row in rows:
        agent = plain_text(row[0]) if row else ""
        cell = row[column] if column < len(row) else ""
        bold = re.match(r"^\s*\*\*(.+?)\*\*", cell)
        if bold:
            previous = plain_text(bold.group(1))
        elif not previous:
            raise BuildError(
                "the first README ledger row opens “The loop today” with no "
                "bold verdict, so there is nothing for later rows to inherit."
            )
        verdicts.append(previous)
        items.append(
            f'<li><span class="verdicts__agent">{esc(agent)}</span> '
            f'<span class="verdicts__verdict">{esc(previous)}</span></li>'
        )
    out["repo_ledger_verdicts_html"] = (
        '<ul class="verdicts">' + "".join(items) + "</ul>"
    )
    # Counted from the same verdicts the Install page lists, never asserted in
    # prose: "exactly one row is verified" is the kind of sentence that goes
    # quietly false the day a second row lands.
    out["repo_ledger_verified_count"] = str(
        sum(1 for v in verdicts if v.lower().startswith("verified end to end"))
    )
    out["repo_ledger_row_count"] = str(len(rows))

    if not ledger_heading:
        raise BuildError(
            "the README ledger has no heading of its own, so "
            "repo_ledger_anchor_url has no anchor to link to."
        )
    out["repo_ledger_anchor_url"] = (
        BLOB_URL + "README.md#" + github_anchor(ledger_heading)
    )
    return out


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
    # Template comments are notes for maintainers. They stay in the template
    # and never ship: a public page source is no place for dev notes or the
    # retired slugs they mention.
    meta["body"] = re.sub(
        r"[ \t]*<!--.*?-->[ \t]*\n?", "", raw[match.end() :], flags=re.S
    ).lstrip("\n")
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
    """The masthead list: every page with a nav_label, then the repository.

    Shown on every page, the front page included. The front page has no
    nav_label; the wordmark is its link.
    """
    items = []
    for page in pages:
        label = page.get("nav_label")
        if not label:
            continue
        target = base + ("" if page["slug"] == "index" else f"{page['slug']}/")
        current_attr = ' aria-current="page"' if page["slug"] == current else ""
        items.append(f'<li><a href="{target}"{current_attr}>{esc(label)}</a></li>')
    for label, href in NAV_EXTERNAL:
        items.append(
            f'<li><a class="nav__ext" href="{esc(href)}">{esc(label)}</a></li>'
        )
    return "<ul class=\"nav__list\">" + "".join(items) + "</ul>"


def redirect_page(old: str, target: str, title: str) -> str:
    """A standalone page at /<old>/ that sends the visitor to `target`.

    Meta refresh plus a real link: GitHub Pages cannot answer with a 301, the
    link works where refresh is disabled, and the strict link checker follows
    the link like any other. The canonical drops the fragment, which search
    engines ignore in a canonical anyway.
    """
    relative = "../" * (old.count("/") + 1) + target
    canonical = SITE_URL + target.partition("#")[0]
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="color-scheme" content="light dark">\n'
        '<meta name="robots" content="noindex">\n'
        "<title>Moved · Paper Session</title>\n"
        f'<link rel="canonical" href="{esc(canonical)}">\n'
        f'<meta http-equiv="refresh" content="0; url={esc(relative)}">\n'
        "</head>\n"
        "<body>\n"
        f'<p>This page has moved to <a href="{esc(relative)}">{esc(title)}</a>.</p>\n'
        "</body>\n"
        "</html>\n"
    )


def check_redirect_slugs(pages: list[dict[str, str]]) -> None:
    """A retired slug may never also be a live page."""
    live = {page["slug"]: page for page in pages}
    for old in REDIRECTS:
        if old in live:
            raise BuildError(
                f"/{old}/ is both a live page ({live[old]['template_name']}) and "
                f"a retired slug in REDIRECTS; remove one of them."
            )


def write_redirects(dist: Path, pages: list[dict[str, str]], strict: bool) -> int:
    """Emit one redirect page per retired slug, and check where each one lands.

    A target must be a live page, and a fragment target must exist as an id on
    it, because a redirect into the top of the wrong section is a quiet dead
    end. (A retired slug that is also a live page never gets this far:
    check_redirect_slugs refuses it before any page is written.)
    """
    live = {page["slug"]: page for page in pages}
    for old, target in REDIRECTS.items():
        path, _, fragment = target.partition("#")
        slug = path.strip("/") or "index"
        page = live.get(slug)
        if page is None:
            raise BuildError(
                f"the redirect from /{old}/ points at /{path}, which is not a "
                f"live page."
            )
        title = "the front page" if slug == "index" else page["title"]
        dest = dist / old / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(redirect_page(old, target, title), encoding="utf-8")
        print(f"  wrote {old}/index.html  (redirect -> /{target})")

        if fragment:
            built = dist / output_path_for(slug)
            if f'id="{fragment}"' not in built.read_text(encoding="utf-8"):
                message = (
                    f"the redirect from /{old}/ lands on /{target}, but "
                    f"{page['template_name']} has no element with "
                    f'id="{fragment}".'
                )
                if strict:
                    raise BuildError(message)
                warn(message)
    return len(REDIRECTS)


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
            "  To build the site anyway, with How it works leaving the "
            "render out, pass --allow-missing-assets."
        )
        if not allow_missing:
            raise BuildError(message)
        warn(message)

    # Counted from what actually landed in dist/, not from the pattern that
    # was supposed to produce it: a page must never show an image that is not
    # there.
    ctx["sheet_count"] = str(sheet_count)

    hero = next((name for name in HERO_CANDIDATES if (STATIC / name).exists()), "")
    ctx["hero_present"] = "1" if hero else ""
    ctx["hero_file"] = hero

    film = FILM_FILE if (STATIC / FILM_FILE).exists() else ""
    poster = next((name for name in FILM_POSTER_CANDIDATES if (STATIC / name).exists()), "")
    captions = FILM_CAPTIONS_FILE if (STATIC / FILM_CAPTIONS_FILE).exists() else ""
    ctx["film_present"] = "1" if film else ""
    ctx["film_file"] = film
    ctx["film_poster_present"] = "1" if poster else ""
    ctx["film_poster_file"] = poster
    ctx["film_captions_present"] = "1" if captions else ""
    ctx["film_captions_file"] = captions

    # The one-click "copy instructions for your AI" payload: the same file
    # ships as a static download and is embedded in every page for the
    # clipboard button, so there is exactly one copy of the text. It is the
    # site's primary call to action, so its absence fails the build.
    copy_src = STATIC / COPY_INSTRUCTIONS_FILE
    if not copy_src.exists():
        raise BuildError(
            f"site/static/{COPY_INSTRUCTIONS_FILE} is missing, and it is the "
            f"text the site's primary call to action copies."
        )
    copy_text = copy_src.read_text(encoding="utf-8")
    if re.search(r"</script", copy_text, re.I):
        raise BuildError(
            f"site/static/{COPY_INSTRUCTIONS_FILE} contains “</script”, which "
            f"would end the <script type=\"text/plain\"> that carries it."
        )
    ctx["copy_instructions"] = copy_text

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
#
# google-chrome first, deliberately. On GitHub's ubuntu runners /usr/bin/chromium
# is the snap build, and snap confinement cannot reach a --user-data-dir or a
# --print-to-pdf target outside $HOME. It does not refuse; it blocks, so the
# failure arrives as a 120s timeout with no diagnostic. Chrome is unconfined and
# preinstalled there. Locally, where chromium is a normal package, either works —
# and the gate writes its temp files inside the workspace now regardless.
CHROMIUM_NAMES = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
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
    with tempfile.TemporaryDirectory(prefix="ps-chrome-", dir=out.parent) as profile:
        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            # CI runners give a container a 64MB /dev/shm, which Chromium's
            # renderer exhausts and then blocks on forever rather than failing.
            # Without this the gate does not error, it HANGS — the local build
            # passes in seconds and the same commit times out on the runner.
            "--disable-dev-shm-usage",
            "--disable-software-rasterizer",
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

    with tempfile.TemporaryDirectory(prefix="ps-gate-", dir=dist.parent) as tmp:
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

LINK_RE = re.compile(r'(?:href|src|poster)="([^"]+)"')


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
    check_redirect_slugs(pages)
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
        ctx["is_home"] = "1" if page["slug"] == "index" else ""
        ctx["nav"] = render_nav(pages, page["slug"], base)
        ctx["repo_url"] = REPO_URL
        ctx["hero_url"] = base + (asset_ctx["hero_file"] or "")
        ctx["film_url"] = base + (asset_ctx["film_file"] or "")
        ctx["film_poster_url"] = base + (asset_ctx["film_poster_file"] or "")
        ctx["film_captions_url"] = base + (asset_ctx["film_captions_file"] or "")
        ctx["example_photo_url"] = base + (asset_ctx["example_file"] or "")
        # The four live pages and the primary call to action's text file,
        # base-relative like every other internal link.
        ctx["how_it_works_url"] = base + "how-it-works/"
        ctx["install_url"] = base + "install/"
        ctx["research_url"] = base + RESEARCH_SLUG + "/"
        ctx["copy_instructions_url"] = base + COPY_INSTRUCTIONS_FILE
        # Absolute, for the <head> only: canonical, og:url, og:image.
        ctx["site_url"] = SITE_URL
        ctx["page_url"] = SITE_URL + (
            "" if page["slug"] == "index" else f"{page['slug']}/"
        )
        ctx["og_image_url"] = (
            SITE_URL + asset_ctx["hero_file"] if asset_ctx["hero_present"] else ""
        )
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

    write_redirects(dist, pages, strict)
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
        help="warn instead of failing when the sheet render How it works shows "
        "(docs/sheet-deep-react.png) is absent (another agent may be "
        "regenerating it)",
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
