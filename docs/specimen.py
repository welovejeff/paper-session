#!/usr/bin/env python3
"""Regenerate the README specimen sheets from references/design.md.

Outputs docs/specimen.pdf (three pages), runs the mandatory layout
verifier, and only then renders the three README images:

    page 1  ->  docs/sheet-deep-react.png
    page 2  ->  docs/sheet-deep-provocation.png
    page 3  ->  docs/sheet-light-rank.png

Every coordinate, size, gray value, and rule weight below comes from
paper-session/references/design.md. Change that file first, this file
second. Run from anywhere: python3 docs/specimen.py
"""

import datetime
import subprocess
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
FONTS = ROOT / "paper-session" / "assets" / "fonts"
PDF = DOCS / "specimen.pdf"

# --- geometry (design.md section 0 and 4) ---------------------------------
PAGE_W, PAGE_H = letter          # 612 x 792
M = 54                           # margins, all sides
LEFT, RIGHT = M, PAGE_W - M      # text block x 54..558
TEXT_W = RIGHT - LEFT            # 504
HEADER_Y = PAGE_H - M            # datum rule at 738
FOOTER_Y = 30                    # footer baseline, below the margin box
# Fixed date so the committed specimen is reproducible; the weekday is derived
# so it can never print wrong.
SPECIMEN_DATE = datetime.date(2026, 8, 12)
DATE_LINE = "SESSION PRINTED " + SPECIMEN_DATE.strftime("%a %d %b %Y").upper()
WEEKDAY = SPECIMEN_DATE.strftime("%A")

REGISTER = {
    "Sans": "IBMPlexSans-Regular.ttf",
    "SansSB": "IBMPlexSans-SemiBold.ttf",
    "SansB": "IBMPlexSans-Bold.ttf",
    "Serif": "IBMPlexSerif-Regular.ttf",
    "SerifSB": "IBMPlexSerif-SemiBold.ttf",
    "SerifI": "IBMPlexSerif-Italic.ttf",
    "Mono": "IBMPlexMono-Regular.ttf",
    "MonoM": "IBMPlexMono-Medium.ttf",
}


def register_fonts():
    for name, file in REGISTER.items():
        pdfmetrics.registerFont(TTFont(name, str(FONTS / file)))


def put(c, x, y, s, font, size, gray, track=0.0, align="l"):
    """Draw one string with optional tracking; return (x, visual width).

    Asserts the string stays inside the text block, so an overlong edit
    fails here instead of at the printer.
    """
    w = pdfmetrics.stringWidth(s, font, size) + track * max(len(s) - 1, 0)
    if align == "r":
        x -= w
    elif align == "c":
        x -= w / 2
    assert x >= LEFT - 1 and x + w <= RIGHT + 1, f"outside text block: {s!r}"
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setFillGray(gray)
    t.setCharSpace(track)
    t.textOut(s)
    c.drawText(t)
    return x, w


def rule(c, x0, x1, y, weight, gray=0.0):
    c.setLineWidth(weight)
    c.setStrokeGray(gray)
    c.line(x0, y, x1, y)


# --- shared organisms -----------------------------------------------------

def header(c, title, intent):
    """Datum rule, title, date line, intent line (design.md section 4)."""
    rule(c, LEFT, RIGHT, HEADER_Y, 2)
    put(c, LEFT, HEADER_Y - 22, title, "SansB", 16, 0.0)
    put(c, LEFT, HEADER_Y - 36, DATE_LINE, "Sans", 6.8, 0.4, track=0.8)
    put(c, LEFT, HEADER_Y - 52, intent, "SerifI", 9.5, 0.3)


def footer(c, note):
    put(c, LEFT, FOOTER_Y, "SCAN IT BACK TO CONTINUE.",
        "SansSB", 6.8, 0.45, track=1.2)
    put(c, RIGHT, FOOTER_Y, note, "Sans", 6.8, 0.45, align="r")


def ink_key(c):
    """Active pen-protocol key, once per sheet (design.md section 9)."""
    put(c, RIGHT, 42, "INK KEY  RED REVIEW · GREEN GO · BLUE DO · BLACK NOTES",
        "Sans", 6, 0.45, align="r")


def open_territory(c, label, rule_y):
    """Label above a 1.6pt rule; empty to the footer (design.md section 6)."""
    put(c, LEFT, rule_y + 6, label, "SansSB", 6.8, 0.4, track=1.4)
    rule(c, LEFT, RIGHT, rule_y, 1.6)


def voice_caption(c, x, y, text, underline_w):
    put(c, x, y, text, "SansB", 8, 0.2, track=1.2)
    rule(c, x, x + underline_w, y - 4.5, 1.6)


# --- page 1: Deep, two-column react pair ----------------------------------

SESSIONS = [
    ("The map and the ground rules", "why this field exists; what we won't automate"),
    ("Tools as instruments", "first contact, small wins, no theory yet"),
    ("The brief that resists", "a problem AI answers badly on purpose"),
    ("Taste as a skill", "critique week; judging output, not making it"),
    ("Agents and delegation", "handing off work, keeping judgment"),
    ("Field week", "out of the building; collect, observe, log"),
    ("The human layer", "what stayed human in weeks 1-6, named out loud"),
    ("Ship and defend", "final work presented against its own process"),
]


def page_deep_react(c):
    header(c, "Fall Course: Session Arc",
           "Re-sequence the eight studio sessions so the arc earns its final week.")

    gutter = 24
    col_w = (TEXT_W - gutter) / 2          # 240
    right_x = LEFT + col_w + gutter        # 318
    cap_y = 660

    voice_caption(c, LEFT, cap_y, "I PROPOSE", col_w)
    cap_w = pdfmetrics.stringWidth("YOU DECIDE", "SansB", 8) + 1.2 * 9
    voice_caption(c, right_x, cap_y, "YOU DECIDE", cap_w)

    top, pitch = 634, 56
    for i, (title, promise) in enumerate(SESSIONS):
        b = top - i * pitch
        put(c, LEFT, b, f"{i + 1:02d}  {title}", "MonoM", 9.2, 0.12)
        put(c, LEFT + 14, b - 12, promise, "Mono", 7.6, 0.42)
        put(c, right_x, b, f"{i + 1:02d}", "Sans", 8, 0.5)
        rule(c, right_x + 18, RIGHT, b - 3, 0.5, 0.55)
        rule(c, right_x + 18, RIGHT, b - 19, 0.5, 0.55)

    # rotated gutter hint, centered between the columns
    hint = "cross out freely"
    hw = pdfmetrics.stringWidth(hint, "SerifI", 7.5)
    c.saveState()
    c.translate(LEFT + col_w + gutter / 2 + 3, 428 - hw / 2)
    c.rotate(90)
    t = c.beginText(0, 0)
    t.setFont("SerifI", 7.5)
    t.setFillGray(0.45)
    t.textOut(hint)
    c.drawText(t)
    c.restoreState()

    open_territory(c, "OPEN TERRITORY", 190)
    ink_key(c)
    footer(c, "Deep · 1 of 2")


# --- page 2: Deep, one provocation ----------------------------------------

def page_deep_provocation(c):
    header(c, "Fall Course: Session Arc",
           "One question on the fall course. Take the whole page.")

    lines = ["What can they do in week eight that they",
             "could not do in week one?"]
    max_w = TEXT_W - 60
    for i, line in enumerate(lines):
        assert pdfmetrics.stringWidth(line, "Serif", 21) <= max_w
        put(c, LEFT, 634 - i * 28, line, "Serif", 21, 0.0)
    put(c, LEFT, 584, "Not tool skills. Name the capacity.", "SerifI", 10, 0.4)

    # deliberately, structurally empty until open territory
    open_territory(c, "OPEN TERRITORY", 176)
    ink_key(c)
    footer(c, "Deep · 2 of 2")


# --- page 3: Light, rank-and-circle ---------------------------------------

TASKS = [
    "Draft the Week 3 studio brief",
    "Review compliance grader test results",
    "Prep Thursday pilot readout",
    "Write the credential program memo",
    "Book field week site visits",
    "Clear the developer ticket backlog",
    "Outline the trend report template",
    "One hour: no-agenda reading block",
]


def page_light_rank(c):
    header(c, f"{WEEKDAY} 9:30 · Win the Week",
           "React to the proposed priorities. Rank what stays, kill what doesn't.")

    item_x = LEFT + 34                     # 88
    k_cx, x_cx, r = 450, 472, 8
    note_x = RIGHT - 60                    # 498

    cap_y = 662
    for x, text, align in ((LEFT, "RANK", "l"), (item_x, "I PROPOSE", "l"),
                           ((k_cx + x_cx) / 2, "KEEP · KILL", "c"),
                           (note_x, "NOTE", "l")):
        put(c, x, cap_y, text, "SansSB", 6.5, 0.4, track=1.4, align=align)

    top, pitch = 630, 52
    for i, task in enumerate(TASKS):
        b = top - i * pitch
        c.setLineWidth(1)
        c.setStrokeGray(0.15)
        c.rect(LEFT, b - 6, 22, 20, stroke=1, fill=0)
        put(c, item_x, b, task, "Mono", 9.6, 0.12)
        c.setLineWidth(0.9)
        c.setStrokeGray(0.2)
        for cx, letter_ in ((k_cx, "K"), (x_cx, "X")):
            c.circle(cx, b + 3.3, r, stroke=1, fill=0)
            put(c, cx, b + 1.1, letter_, "Sans", 6.4, 0.2, align="c")
        rule(c, note_x, RIGHT, b - 3, 0.5, 0.55)

    put(c, LEFT, 234, "Rule: something dies tonight. Pick it.",
        "SerifI", 8.5, 0.35)
    open_territory(c, "SCRIBBLE ZONE", 212)
    ink_key(c)
    footer(c, "Light · 1 of 1")


# --- build, verify, render ------------------------------------------------

PAGES = [
    (page_deep_react, "sheet-deep-react.png"),
    (page_deep_provocation, "sheet-deep-provocation.png"),
    (page_light_rank, "sheet-light-rank.png"),
]


def build_pdf():
    register_fonts()
    c = canvas.Canvas(str(PDF), pagesize=letter)
    for draw_page, _ in PAGES:
        draw_page(c)
        c.showPage()
    c.save()


def verify():
    """Mandatory gate (design.md section 8). Never render on failure."""
    verifier = ROOT / "paper-session" / "scripts" / "verify_layout.py"
    subprocess.run([sys.executable, str(verifier), str(PDF)], check=True)


def render_pngs():
    """~110 dpi via PyMuPDF, longest side resized to 1000px via Pillow."""
    try:
        try:
            import pymupdf
        except ImportError:
            import fitz as pymupdf
        from PIL import Image
    except ImportError as e:
        sys.exit(
            f"PNG rendering needs PyMuPDF and Pillow (beyond requirements.txt): "
            f"python3 -m pip install pymupdf pillow  ({e})"
        )

    doc = pymupdf.open(str(PDF))
    zoom = 110 / 72
    for page, (_, name) in zip(doc, PAGES):
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        scale = 1000 / max(img.size)
        img = img.resize((round(img.width * scale), round(img.height * scale)),
                         Image.LANCZOS)
        img.save(DOCS / name)
        print(f"wrote {DOCS / name} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    build_pdf()
    print(f"wrote {PDF}")
    verify()
    render_pngs()
