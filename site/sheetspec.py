#!/usr/bin/env python3
"""Derive the site's printable-sheet CSS from paper-session/references/design.md.

Why this file exists
--------------------
`design.md` is the single source of visual truth for every sheet this project
prints. A live HTML sheet on the website needs the same numbers — 612x792pt,
54pt margins, a 2pt datum rule, 21/28pt provocations, gray value 0.45 on the
footer — and there are exactly two ways to get them into CSS.

The first is to type them into a stylesheet. Direction A was killed for doing
that: a hand-written CSS restatement of the print system is a second spec with
no gate, and two specs drift. The day somebody changes a rule weight in
`design.md`, the website keeps printing the old one and nothing anywhere
notices.

The second is this file. It reads `design.md`, extracts the numbers
mechanically, and emits them as CSS custom properties. The site's sheet is then
a *derivation* of the spec rather than a copy of it, and a change to `design.md`
reaches the printed page on the next build. `build.py` renders the resulting
page to PDF and runs the project's own `scripts/verify_layout.py` over it, so
the derivation is checked rather than trusted.

The rule that follows from this: **no number in `site/static/style.css` that
also appears in `design.md` may be typed by hand.** Consume the token. If the
token you need is not emitted here, add an extractor here.

Failure policy
--------------
Loud. Every value this module emits is required. If a table row is renamed, a
prose sentence is reworded, or a cell changes shape, `SpecError` is raised
naming the section and what it expected, and the site build stops. A silent
fallback to a hardcoded default is precisely the drift this file exists to
prevent, so there are no defaults anywhere below.

What is deliberately NOT here
-----------------------------
Strings. `build.py` already extracts the footer line ("SCAN IT BACK TO
CONTINUE.") from design.md §5 for `repo_footer_line`; a second extractor for the
same sentence would be the duplication this module is against. This module
emits geometry, type, gray and rule weights, and the font registration table.

Units
-----
design.md is written in print points. CSS points are fixed at 96 px per inch, so
one point is `calc(96 / 72 * 1px)` and that arithmetic is emitted verbatim
rather than pre-multiplied here — a reader of the generated CSS can see the
conversion instead of taking a decimal on faith. Every length token is written
as `calc(<the number from design.md> * var(--ps-pt))`, so the source number
survives into the stylesheet and can be read back against the spec.

`--ps-pt` defaults to a true point. A screen-rendered sheet rebinds it (see
style.css §21) to a fraction of the sheet's own width, which scales the whole
object without touching a single one of these numbers.

Usage
-----
    from sheetspec import load_spec, emit_css, SpecError
    css = emit_css(load_spec())
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
DESIGN_MD = ROOT / "paper-session" / "references" / "design.md"

# Bundled font directory, relative to the repo root. design.md §1 names the
# files; build.py copies exactly these into dist/fonts/ and fails if one is
# absent, the same way build.sh refuses to ship the fonts without their licence.
FONT_DIR = ROOT / "paper-session" / "assets" / "fonts"
FONT_LICENSE = "LICENSE-IBMPlex.txt"

# Where the copied faces land inside dist/, and therefore what the generated
# @font-face src is relative to (style.css sits at the dist root).
FONT_URL_PREFIX = "fonts/"


class SpecError(Exception):
    """design.md did not have the shape this emitter requires."""


# --------------------------------------------------------------------------
# The contract: every row and value below must exist, or the build stops.
# --------------------------------------------------------------------------

# §2 Type scale. Keys are the slugified Element cell.
REQUIRED_TYPE_ROWS = (
    "sheet-title",
    "voice-captions",
    "section-labels-open-territory-label",
    "metadata",
    "hand-label",
    "intent-line",
    "provocation-standard",
    "provocation-light-sheets",
    "provocation-subline",
    "ai-item-primary",
    "ai-item-secondary-promise",
    "house-rule-aside",
    "footer",
    "slot-numbers",
)

# §3 Rules and guides. Keys are the slugified Element cell.
REQUIRED_RULE_ROWS = (
    "datum-rule",
    "voice-caption-underline",
    "open-territory-rule",
    "structural-hairline",
    "writing-guide",
    "answer-frame",
    "keep-kill-circle",
    "dot-grid",
    "cut-line",
)

# §1 Fonts. Keys are the Register name cell, verbatim.
REQUIRED_REGISTERS = (
    "Sans",
    "SansSB",
    "SansB",
    "Serif",
    "SerifSB",
    "SerifI",
    "Mono",
    "MonoM",
)

# Filename stem -> the family this project self-hosts it under. The site keeps
# its own family names so that the CDN copy of IBM Plex the other pages load
# and the bundled copy the sheet loads cannot silently substitute for one
# another: the sheet's faces are the files design.md registers, on disk.
FAMILY_FROM_STEM = {
    "IBMPlexSans": ("IBM Plex Sans", "Paper Session Sans"),
    "IBMPlexSerif": ("IBM Plex Serif", "Paper Session Serif"),
    "IBMPlexMono": ("IBM Plex Mono", "Paper Session Mono"),
}

# Filename style token -> (CSS weight, CSS style).
STYLE_FROM_TOKEN = {
    "Regular": ("400", "normal"),
    "Medium": ("500", "normal"),
    "SemiBold": ("600", "normal"),
    "Bold": ("700", "normal"),
    "Italic": ("400", "italic"),
}

NUM = r"\d+(?:\.\d+)?"


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------


def _slug(text: str) -> str:
    """Slugify a table's Element cell.

    Deliberately literal: parentheticals and code ticks are dropped, everything
    else survives into the key. A row renamed from "Sheet title" to "Title" is
    then a hard failure with a clear message rather than a token that quietly
    stops being emitted.
    """
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace("`", " ").replace(":", " ")
    text = re.sub(r"[^A-Za-z0-9]+", "-", text)
    return text.strip("-").lower()


def _num(value: str, where: str, what: str) -> str:
    """Return a numeric literal, preserved as written in design.md."""
    match = re.match(rf"^\s*[+]?({NUM})\s*$", value)
    if not match:
        raise SpecError(
            f"design.md {where}: expected a plain number for {what}, "
            f"found {value!r}"
        )
    return match.group(1)


def _need(pattern: str, text: str, where: str, what: str) -> re.Match:
    match = re.search(pattern, text)
    if not match:
        raise SpecError(
            f"design.md {where}: could not read {what}. "
            f"Expected text matching /{pattern}/. The section was reworded, or "
            f"the value moved; update site/sheetspec.py to match the spec "
            f"rather than hardcoding the old number."
        )
    return match


def _sections(md: str) -> dict[str, str]:
    """Split design.md on its numbered `## N. Title` headings."""
    out: dict[str, str] = {}
    heads = list(re.finditer(r"^##\s+(\d+)\.\s*(.+?)\s*$", md, re.M))
    if not heads:
        raise SpecError(
            "design.md: found no `## N. Title` section headings at all. "
            "The file is not the design system this emitter knows how to read."
        )
    for i, head in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(md)
        out[head.group(1)] = md[head.end() : end]
    return out


def _table(body: str, where: str, columns: int) -> list[list[str]]:
    """Return the first GFM pipe table's data rows, as trimmed cells."""
    rows: list[list[str]] = []
    started = False
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if started:
                break
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            started = True
            continue
        if started:
            if len(cells) != columns:
                raise SpecError(
                    f"design.md {where}: table row has {len(cells)} cells, "
                    f"expected {columns}: {stripped!r}"
                )
            rows.append(cells)
    if not rows:
        raise SpecError(f"design.md {where}: expected a table, found none.")
    return rows


# --------------------------------------------------------------------------
# Section readers
# --------------------------------------------------------------------------


def _hhea_metrics(path: Path) -> tuple[int, int, int]:
    """(unitsPerEm, hhea ascender, hhea descender) out of a TrueType file.

    design.md places type by baseline, the way reportlab does. CSS places
    boxes. Turning one into the other needs the font's own vertical metrics,
    and taking them from the files §1 registers keeps even that conversion a
    derivation rather than a constant somebody guessed at.
    """
    try:
        data = path.read_bytes()
        count = int.from_bytes(data[4:6], "big")
        offsets = {}
        for i in range(count):
            rec = 12 + 16 * i
            tag = data[rec : rec + 4].decode("latin-1")
            offsets[tag] = int.from_bytes(data[rec + 8 : rec + 12], "big")
        head, hhea = offsets["head"], offsets["hhea"]
        upm = int.from_bytes(data[head + 18 : head + 20], "big")
        ascender = int.from_bytes(data[hhea + 4 : hhea + 6], "big", signed=True)
        descender = int.from_bytes(data[hhea + 6 : hhea + 8], "big", signed=True)
    except (OSError, KeyError, IndexError, ValueError) as exc:
        raise SpecError(
            f"cannot read the vertical metrics of {path.name}: {exc}. The sheet "
            f"converts design.md's baselines into CSS box offsets using them."
        ) from exc
    if not upm or ascender <= 0 or descender >= 0:
        raise SpecError(
            f"{path.name} reports implausible metrics "
            f"(upm={upm}, ascender={ascender}, descender={descender})."
        )
    return upm, ascender, descender


def _read_metrics(faces: dict[str, dict[str, str]]) -> dict[str, str]:
    """The one vertical rhythm every registered face shares."""
    seen: dict[tuple[float, float], list[str]] = {}
    for register, face in faces.items():
        upm, ascender, descender = _hhea_metrics(FONT_DIR / face["file"])
        key = (round(ascender / upm, 6), round(-descender / upm, 6))
        seen.setdefault(key, []).append(register)
    if len(seen) != 1:
        detail = "; ".join(
            f"{a}/{d} for {', '.join(regs)}" for (a, d), regs in seen.items()
        )
        raise SpecError(
            f"the registered faces no longer share one vertical rhythm ({detail}). "
            f"A sheet cannot place baselines from a single ratio when its faces "
            f"disagree; sheetspec.py needs a per-register metric before the site "
            f"can set type from these files."
        )
    (ascent, descent), _ = next(iter(seen.items()))
    return {"ascent": f"{ascent:g}", "descent": f"{descent:g}"}


def _read_page(body: str) -> dict[str, str]:
    """§0 Non-negotiables: the page box, the margins, the gray floors."""
    where = "§0 Non-negotiables"
    box = _need(
        rf"US Letter portrait \(({NUM}) x ({NUM}) pt\)", body, where, "the page box"
    )
    margin = _need(rf"Margins ({NUM})pt all sides", body, where, "the margins")
    footer = _need(
        rf"Footer sits below the margin at baseline y=({NUM})",
        body,
        where,
        "the footer baseline",
    )
    floor = _need(
        rf"lighter than {NUM}% gray \(fill or stroke gray value ({NUM})\)",
        body,
        where,
        "the 50% meaning floor",
    )
    ceiling = _need(
        rf"up to {NUM}% gray \(({NUM})\)", body, where, "the writing-guide ceiling"
    )
    pen = _need(
        rf"At least ({NUM})% of every page area is space for the pen",
        body,
        where,
        "the pen's share of the page",
    )
    return {
        "page_w": box.group(1),
        "page_h": box.group(2),
        "margin": margin.group(1),
        "footer_baseline": footer.group(1),
        "meaning_floor": floor.group(1),
        "guide_ceiling": ceiling.group(1),
        "pen_share": pen.group(1),
    }


def _read_fonts(body: str) -> dict[str, dict[str, str]]:
    """§1: the register table, turned into self-hosted @font-face material."""
    where = "§1 Fonts and the three voices"
    faces: dict[str, dict[str, str]] = {}
    for register, filename, _role in _table(body, where, 3):
        match = re.fullmatch(r"(IBMPlex(?:Sans|Serif|Mono))-([A-Za-z]+)\.ttf", filename)
        if not match:
            raise SpecError(
                f"design.md {where}: register {register!r} names the file "
                f"{filename!r}, which is not an IBMPlex<Family>-<Style>.ttf "
                f"name this emitter can turn into a @font-face."
            )
        stem, style_token = match.group(1), match.group(2)
        if stem not in FAMILY_FROM_STEM:
            raise SpecError(
                f"design.md {where}: unknown font family stem {stem!r} in "
                f"{filename!r}."
            )
        if style_token not in STYLE_FROM_TOKEN:
            raise SpecError(
                f"design.md {where}: unknown style token {style_token!r} in "
                f"{filename!r}. Add it to STYLE_FROM_TOKEN with its CSS weight "
                f"and style."
            )
        source_family, local_family = FAMILY_FROM_STEM[stem]
        weight, style = STYLE_FROM_TOKEN[style_token]
        faces[register] = {
            "file": filename,
            "source_family": source_family,
            "family": local_family,
            "weight": weight,
            "style": style,
        }
    missing = [r for r in REQUIRED_REGISTERS if r not in faces]
    if missing:
        raise SpecError(
            f"design.md {where}: the register table is missing "
            f"{', '.join(missing)}. The three-voice rule is registered by "
            f"exact name; a renamed register breaks every sheet."
        )
    return faces


def _read_type(body: str, faces: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    """§2: the type scale, one entry per row."""
    where = "§2 Type scale"
    out: dict[str, dict[str, str]] = {}
    for element, font, size, gray, track in _table(body, where, 5):
        key = _slug(element)

        register = font
        caps = False
        if register.lower().endswith(" caps"):
            register = register[: -len(" caps")].strip()
            caps = True
        if register not in faces:
            raise SpecError(
                f"design.md {where}: row {element!r} uses font register "
                f"{register!r}, which §1 does not register."
            )

        size_cell = size
        if size_cell.lower().endswith(" caps"):
            size_cell = size_cell[: -len(" caps")].strip()
            caps = True
        if "/" in size_cell:
            size_txt, leading_txt = (p.strip() for p in size_cell.split("/", 1))
            leading = _num(leading_txt, where, f"the leading of {element!r}")
        else:
            size_txt, leading = size_cell, None
        size_val = _num(size_txt, where, f"the size of {element!r}")

        out[key] = {
            "element": element,
            "register": register,
            "size": size_val,
            "leading": leading,
            "gray": _num(gray, where, f"the gray of {element!r}"),
            "track": _num(track, where, f"the tracking of {element!r}"),
            "caps": caps,
        }
    missing = [k for k in REQUIRED_TYPE_ROWS if k not in out]
    if missing:
        raise SpecError(
            f"design.md {where}: missing required row(s) "
            f"{', '.join(missing)}. Rows are keyed by their Element cell; if "
            f"one was renamed, rename it in REQUIRED_TYPE_ROWS too rather than "
            f"letting the site fall back to a number of its own."
        )
    return out


def _read_rules(body: str) -> dict[str, dict[str, str]]:
    """§3: rule weights, guide leading, and the two range-valued rows."""
    where = "§3 Rules and guides"
    out: dict[str, dict[str, str]] = {}
    for element, weight, gray in _table(body, where, 3):
        key = _slug(element)
        entry: dict[str, str] = {"element": element}

        stroke = re.match(rf"^({NUM})pt", weight)
        if stroke:
            entry["weight"] = stroke.group(1)
        dots = re.match(rf"^dots r({NUM})-({NUM})$", weight)
        if dots:
            entry["radius_min"], entry["radius_max"] = dots.group(1), dots.group(2)
        if not stroke and not dots:
            raise SpecError(
                f"design.md {where}: row {element!r} has weight cell {weight!r}, "
                f"which is neither `<n>pt...` nor `dots r<n>-<n>`."
            )
        dash = re.search(rf"dash ({NUM})/({NUM})", weight)
        if dash:
            entry["dash_on"], entry["dash_off"] = dash.group(1), dash.group(2)

        gray_match = re.match(rf"^({NUM})", gray)
        if not gray_match:
            raise SpecError(
                f"design.md {where}: row {element!r} has gray cell {gray!r}, "
                f"which does not start with a gray value."
            )
        entry["gray"] = gray_match.group(1)
        for name, pattern in (
            ("leading", rf"leading ({NUM})pt"),
            ("radius", rf"radius ({NUM})pt"),
        ):
            found = re.search(pattern, gray)
            if found:
                entry[name] = found.group(1)
        pitch = re.search(rf"pitch ({NUM})-({NUM})pt", gray)
        if pitch:
            entry["pitch_min"], entry["pitch_max"] = pitch.group(1), pitch.group(2)

        out[key] = entry

    missing = [k for k in REQUIRED_RULE_ROWS if k not in out]
    if missing:
        raise SpecError(
            f"design.md {where}: missing required row(s) {', '.join(missing)}."
        )
    if "leading" not in out["writing-guide"]:
        raise SpecError(
            f"design.md {where}: the writing-guide row no longer states its "
            f"leading (expected `leading <n>pt` in the gray cell). Ruled lines "
            f"cannot be spaced without it."
        )
    return out


def _read_header(body: str) -> dict[str, str]:
    """§4: the four header baselines, as drops from the top margin."""
    where = "§4 Header anatomy"
    top = _need(rf"Top edge at y = {NUM} - {NUM} = ({NUM})", body, where, "the top edge")
    drops = {}
    for name, label in (
        ("title", "Sheet title"),
        ("date", "Date line"),
        ("intent", "Intent line"),
    ):
        match = _need(
            rf"{label},[^\n]*?baseline {NUM} - ({NUM})",
            body,
            where,
            f"the {label.lower()} baseline",
        )
        drops[name] = match.group(1)
    drops["body"] = _need(
        rf"Body begins at y {NUM} - ({NUM})", body, where, "where the body begins"
    ).group(1)
    drops["top"] = top.group(1)
    return drops


def _read_molecules(body: str) -> dict[str, str]:
    """§6: the open-territory floors and the constraint box's prompt size."""
    where = "§6 Molecules"
    territory = _need(
        rf"minimum height ({NUM})pt \(Light\) / ({NUM})pt \(Deep\)",
        body,
        where,
        "the open-territory minimum heights",
    )
    prompt = _need(
        rf"at Serif ({NUM})\)",
        body,
        where,
        "the constraint box's prompt size",
    )
    gutter = _need(
        rf"two equal columns, ({NUM})pt gutter",
        body,
        where,
        "the react pair's gutter",
    )
    return {
        "territory_light": territory.group(1),
        "territory_deep": territory.group(2),
        "constraint_prompt": prompt.group(1),
        "react_gutter": gutter.group(1),
    }


# --------------------------------------------------------------------------
# Load
# --------------------------------------------------------------------------


def load_spec(path: Path | None = None) -> dict:
    """Read design.md and return every value the site's sheet needs."""
    source = path or DESIGN_MD
    try:
        md = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise SpecError(
            f"cannot read the design system at {source}: {exc}. The site's "
            f"sheet is generated from it and has no numbers of its own."
        ) from exc

    sections = _sections(md)
    for number, name in (
        ("0", "Non-negotiables"),
        ("1", "Fonts and the three voices"),
        ("2", "Type scale"),
        ("3", "Rules and guides"),
        ("4", "Header anatomy"),
        ("6", "Molecules"),
    ):
        if number not in sections:
            raise SpecError(f"design.md: section §{number} ({name}) is missing.")

    faces = _read_fonts(sections["1"])
    return {
        "digest": hashlib.sha256(md.encode("utf-8")).hexdigest()[:12],
        "source": source,
        "page": _read_page(sections["0"]),
        "faces": faces,
        "metrics": _read_metrics(faces),
        "type": _read_type(sections["2"], faces),
        "rules": _read_rules(sections["3"]),
        "header": _read_header(sections["4"]),
        "molecules": _read_molecules(sections["6"]),
    }


def font_files(spec: dict) -> list[str]:
    """The font filenames design.md registers, in table order, deduplicated."""
    seen: list[str] = []
    for face in spec["faces"].values():
        if face["file"] not in seen:
            seen.append(face["file"])
    return seen


# --------------------------------------------------------------------------
# Emit
# --------------------------------------------------------------------------


def _pt(value: str) -> str:
    """A length token, with the design.md number left visible inside it."""
    return f"calc({value} * var(--ps-pt))"


def _gray_name(value: str) -> str:
    """Name a gray token by its percentage, so 0.5 reads as 50 and not as 05."""
    pct = float(value) * 100
    return f"--ps-gray-{int(round(pct))}"


def emit_css(spec: dict) -> str:
    """Return the generated stylesheet block. Deterministic: same in, same out."""
    page = spec["page"]
    header = spec["header"]
    lines: list[str] = []
    add = lines.append

    add("/* ==========================================================================")
    add("   GENERATED — do not edit, and do not restate any of it by hand.")
    add("")
    add("   Emitted by site/sheetspec.py from")
    add(f"     paper-session/references/design.md  (sha256 {spec['digest']})")
    add("")
    add("   design.md is the single source of visual truth for every sheet this")
    add("   project prints. A CSS restatement of it would be a second spec with no")
    add("   gate, and two specs drift; that is what this block prevents. Every")
    add("   number below is the number in design.md, and the pt->px arithmetic is")
    add("   written out rather than pre-multiplied so it can be checked by eye.")
    add("")
    add("   The page that consumes these tokens is rendered to PDF and run through")
    add("   paper-session/scripts/verify_layout.py on every build. If you need a")
    add("   number that is not here, add an extractor to site/sheetspec.py.")
    add("   ========================================================================== */")
    add("")

    # ---- fonts ----------------------------------------------------------
    add("/* The eight faces design.md §1 registers by exact name, self-hosted from")
    add("   paper-session/assets/fonts/ so the printed sheet is measured on the")
    add("   metrics of the files the spec names rather than on a CDN substitute or")
    add("   a fallback the gate would never notice. */")
    for register in spec["faces"]:
        face = spec["faces"][register]
        add("@font-face {")
        add(f'  font-family: "{face["family"]}"; /* {register} · {face["source_family"]} */')
        add(f'  font-style: {face["style"]};')
        add(f'  font-weight: {face["weight"]};')
        add("  font-display: block;")
        add(f'  src: url("{FONT_URL_PREFIX}{face["file"]}") format("truetype");')
        add("}")
    add("")

    # ---- @page ----------------------------------------------------------
    add("/* The paper. Margin zero on purpose: design.md §0 puts the footer BELOW")
    add("   the margin box at baseline y=30, which a @page margin cannot express,")
    add("   so the sheet element carries the 54pt margins itself. */")
    add(f'@page {{ size: {page["page_w"]}pt {page["page_h"]}pt; margin: 0; }}')
    add("")

    # ---- tokens ---------------------------------------------------------
    # Declared on the sheet as well as on the root, not only on the root. Every
    # length below is written as `calc(<n> * var(--ps-pt))`, and a custom
    # property is substituted where it is DECLARED, not where it is used: with
    # these on :root alone the arithmetic resolves once against the root's
    # --ps-pt and a sheet rebinding that point inherits the already-resolved
    # length, so the screen scale is silently inert. Repeating the declarations
    # on .ps-sheet makes them resolve again in the sheet's own scope. Same
    # specificity, and style.css §21 comes later in the cascade, so §21's
    # rebind still wins.
    add(":root,")
    add(".ps-sheet {")
    add("  /* One printer's point, at the CSS-fixed 96 px per inch. */")
    add("  --ps-pt-px: calc(96 / 72 * 1px);")
    add("  /* Every length below is expressed in --ps-pt. A screen-rendered sheet")
    add("     rebinds this to a fraction of its own width and the whole object")
    add("     scales; print rebinds it to a true point. */")
    add("  --ps-pt: var(--ps-pt-px);")
    add("")

    add("  /* §0 Non-negotiables — the page box and the two gray limits. */")
    add("  /* The bare numbers too: a ratio and a divisor cannot take a unit,")
    add("     and style.css derives the screen scale by dividing the sheet's own")
    add("     width into 612 points. */")
    add(f'  --ps-page-width-pt: {page["page_w"]};')
    add(f'  --ps-page-height-pt: {page["page_h"]};')
    add(f'  --ps-margin-pt: {page["margin"]};')
    add(f'  --ps-page-width: {_pt(page["page_w"])};')
    add(f'  --ps-page-height: {_pt(page["page_h"])};')
    add(f'  --ps-margin: {_pt(page["margin"])};')
    add(
        f'  --ps-text-width: calc(({page["page_w"]} - 2 * {page["margin"]})'
        " * var(--ps-pt));"
    )
    add(
        f'  --ps-text-height: calc(({page["page_h"]} - 2 * {page["margin"]})'
        " * var(--ps-pt));"
    )
    add(f'  --ps-footer-baseline: {_pt(page["footer_baseline"])};')
    add(f'  --ps-meaning-floor-gray: {page["meaning_floor"]};')
    add(f'  --ps-guide-ceiling-gray: {page["guide_ceiling"]};')
    add(f'  --ps-pen-share: {page["pen_share"]}%;')
    add("")

    add("  /* Font metrics, read from the hhea table of the files §1 registers.")
    add("     design.md places type by baseline; CSS places boxes. At line-height 1")
    add("     the baseline sits this far below a line box's top edge, and this far")
    add("     above its bottom, so a spec baseline becomes a box offset. */")
    add(f'  --ps-font-ascent: {spec["metrics"]["ascent"]};')
    add(f'  --ps-font-descent: {spec["metrics"]["descent"]};')
    add(
        "  --ps-baseline-from-top: calc("
        f'(1 - (var(--ps-font-ascent) + var(--ps-font-descent))) / 2'
        " + var(--ps-font-ascent));"
    )
    add(
        "  --ps-baseline-from-bottom: calc("
        f'(1 - (var(--ps-font-ascent) + var(--ps-font-descent))) / 2'
        " + var(--ps-font-descent));"
    )
    add("")
    add("  /* §4 Header anatomy — baselines as drops from the top margin. */")
    add(f'  --ps-header-top: {_pt(header["top"])};')
    add(f'  --ps-header-title-drop: {_pt(header["title"])};')
    add(f'  --ps-header-date-drop: {_pt(header["date"])};')
    add(f'  --ps-header-intent-drop: {_pt(header["intent"])};')
    add(f'  --ps-header-body-drop: {_pt(header["body"])};')
    add("")

    add("  /* §6 Molecules — the open-territory floors, the constraint box. */")
    add(f'  --ps-open-territory-light: {_pt(spec["molecules"]["territory_light"])};')
    add(f'  --ps-open-territory-deep: {_pt(spec["molecules"]["territory_deep"])};')
    add(f'  --ps-constraint-prompt-size: {_pt(spec["molecules"]["constraint_prompt"])};')
    add(f'  --ps-react-gutter: {_pt(spec["molecules"]["react_gutter"])};')
    add("")

    # gray values, deduplicated across §2 and §3
    grays: list[str] = []
    for entry in list(spec["type"].values()) + list(spec["rules"].values()):
        if entry["gray"] not in grays:
            grays.append(entry["gray"])
    grays.sort(key=float)
    add("  /* Gray values, verbatim from §2 and §3. design.md counts them the way")
    add("     reportlab does: 0 is black, 1 is white, so value v is v x 100% white.")
    add(f'     Nothing that carries meaning goes above {page["meaning_floor"]};')
    add(f'     writing guides may reach {page["guide_ceiling"]} because they carry none. */')
    for value in grays:
        pct = f"calc({value} * 100%)"
        add(f"  {_gray_name(value)}: rgb({pct} {pct} {pct});")
    add("")

    add("  /* §1 Font registers. Never blend the voices: Serif asks, Mono is the")
    add("     machine, tracked Sans caps is furniture. */")
    for register, face in spec["faces"].items():
        key = register.lower()
        add(f'  --ps-face-{key}: "{face["family"]}";')
        add(f"  --ps-face-{key}-weight: {face['weight']};")
        add(f"  --ps-face-{key}-style: {face['style']};")
    add("")

    add("  /* §2 Type scale. One group per row of the table. */")
    for key in spec["type"]:
        entry = spec["type"][key]
        register = entry["register"].lower()
        add(f'  /* {entry["element"]} */')
        add(f"  --ps-{key}-family: var(--ps-face-{register});")
        add(f"  --ps-{key}-weight: var(--ps-face-{register}-weight);")
        add(f"  --ps-{key}-style: var(--ps-face-{register}-style);")
        add(f'  --ps-{key}-size: {_pt(entry["size"])};')
        leading = _pt(entry["leading"]) if entry["leading"] else "normal"
        add(f"  --ps-{key}-leading: {leading};")
        add(f'  --ps-{key}-color: var({_gray_name(entry["gray"])});')
        add(f'  --ps-{key}-track: {_pt(entry["track"])};')
        add(f'  --ps-{key}-transform: {"uppercase" if entry["caps"] else "none"};')
    add("")

    add("  /* §3 Rules and guides. */")
    for key in spec["rules"]:
        entry = spec["rules"][key]
        add(f'  /* {entry["element"]} */')
        if "weight" in entry:
            add(f'  --ps-{key}-weight: {_pt(entry["weight"])};')
        add(f'  --ps-{key}-color: var({_gray_name(entry["gray"])});')
        for name in ("leading", "radius"):
            if name in entry:
                add(f"  --ps-{key}-{name}: {_pt(entry[name])};")
        for name in ("radius_min", "radius_max", "pitch_min", "pitch_max"):
            if name in entry:
                add(f'  --ps-{key}-{name.replace("_", "-")}: {_pt(entry[name])};')
        if "dash_on" in entry:
            add(
                f'  --ps-{key}-dash: {_pt(entry["dash_on"])} {_pt(entry["dash_off"])};'
            )
    add("}")
    add("")
    return "\n".join(lines)


def main() -> int:
    try:
        print(emit_css(load_spec()), end="")
    except SpecError as exc:
        print(f"sheetspec: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
