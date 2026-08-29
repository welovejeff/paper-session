#!/usr/bin/env python3
"""build_directions_pdf.py — compose the site design-sprint deliverable.

Four website directions, three pages each (landing render, interior render, the
argument set as type), between a cover, a reading note, and a comparison page.

US Letter portrait, 612x792pt. Grayscale only, nothing meaningful below 50% gray,
no fills. IBM Plex under the project's own registered names.

    python3 site/design/build_directions_pdf.py
    python3 paper-session/scripts/verify_layout.py site/design/site-directions.pdf
"""
import os
import sys

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas

Image.MAX_IMAGE_PIXELS = None

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DESIGN = os.path.join(ROOT, "site", "design")
SHOTS = os.path.join(DESIGN, "shots")
FONTS = os.path.join(ROOT, "paper-session", "assets", "fonts")
SLICES = os.path.join(SHOTS, "_slices")
OUT = os.path.join(DESIGN, "site-directions.pdf")

PW, PH = 612.0, 792.0
M = 54.0
RIGHT = PW - M
COLW = RIGHT - M                      # 504

DATUM_Y = PH - M                      # 738
RUN_Y = DATUM_Y + 6
TITLE_Y = DATUM_Y - 26
META_Y = DATUM_Y - 40
BODY_TOP = DATUM_Y - 62
FOOT_RULE_Y = 62.0
FOOT_Y = 48.0
BODY_BOTTOM = 74.0

# Gray values: 0.0 black, 1.0 white. Nothing meaningful above 0.50.
INK = 0.0
INK2 = 0.30
QUIET = 0.42
FURN = 0.45
HAIR = 0.55                           # rules only, never type

DATE = "SAT 29 AUG 2026"

FACES = {
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
    for name, filename in FACES.items():
        path = os.path.join(FONTS, filename)
        if not os.path.exists(path):
            sys.exit("missing face: " + path)
        pdfmetrics.registerFont(TTFont(name, path))


# ---------------------------------------------------------------- primitives

def rule(c, y, x0=M, x1=RIGHT, w=0.5, gray=HAIR):
    c.setStrokeGray(gray)
    c.setLineWidth(w)
    c.line(x0, y, x1, y)


def tracked(c, x, y, text, font="SansSB", size=6.8, track=1.1, gray=FURN):
    """Tracked Sans caps. Infrastructure, drawn glyph by glyph."""
    c.setFont(font, size)
    c.setFillGray(gray)
    cx = x
    for ch in text:
        c.drawString(cx, y, ch)
        cx += pdfmetrics.stringWidth(ch, font, size) + track
    return cx - track


def tracked_width(text, font="SansSB", size=6.8, track=1.1):
    return (pdfmetrics.stringWidth(text, font, size)
            + track * max(len(text) - 1, 0))


def tracked_right(c, x_right, y, text, **kw):
    w = tracked_width(text, kw.get("font", "SansSB"), kw.get("size", 6.8),
                      kw.get("track", 1.1))
    return tracked(c, x_right - w, y, text, **kw)


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(trial, font, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(c, x, y, text, width, font="Sans", size=10.0, lead=13.5, gray=INK):
    c.setFont(font, size)
    c.setFillGray(gray)
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= lead
    return y


def rich(c, x, y, runs, width, lead=13.5):
    """Wrap a list of (text, font, size, gray) runs as one flowing paragraph."""
    tokens = []
    for text, font, size, gray in runs:
        parts = text.split(" ")
        for i, p in enumerate(parts):
            if p == "" and i:
                continue
            tokens.append((p, font, size, gray))
    line, line_w = [], 0.0
    space = {}
    out_y = y

    def flush(toks):
        nonlocal out_y
        cx = x
        for t, f, s, g in toks:
            c.setFont(f, s)
            c.setFillGray(g)
            c.drawString(cx, out_y, t)
            cx += pdfmetrics.stringWidth(t, f, s) + space.setdefault(
                (f, s), pdfmetrics.stringWidth(" ", f, s))
        out_y -= lead

    for tok in tokens:
        t, f, s, g = tok
        sp = space.setdefault((f, s), pdfmetrics.stringWidth(" ", f, s))
        w = pdfmetrics.stringWidth(t, f, s)
        add = w if not line else w + sp
        if line and line_w + add > width:
            flush(line)
            line, line_w = [tok], w
        else:
            line.append(tok)
            line_w += add
    if line:
        flush(line)
    return out_y


def chrome(c, page_no, total, running, right_running):
    tracked(c, M, RUN_Y, running, size=6.4, track=1.2, gray=FURN)
    tracked_right(c, RIGHT, RUN_Y, right_running, size=6.4, track=1.2, gray=FURN)
    rule(c, DATUM_Y, w=1.4, gray=INK)
    rule(c, FOOT_RULE_Y, w=0.9, gray=0.35)
    tracked(c, M, FOOT_Y, "PAPER SESSION · SITE DIRECTIONS · " + DATE,
            size=6.4, track=1.1, gray=FURN)
    tracked_right(c, RIGHT, FOOT_Y, "%d OF %d" % (page_no, total),
                  size=6.4, track=1.1, gray=FURN)


def head(c, title, meta=None, title_font="SansB", title_size=16.0):
    c.setFont(title_font, title_size)
    c.setFillGray(INK)
    c.drawString(M, TITLE_Y, title)
    if meta:
        tracked(c, M, META_Y, meta, size=6.8, track=1.2, gray=FURN)


# ------------------------------------------------------------------- imagery

def place_shot(c, path, x, y_top, box_w, box_h, gutter=14.0):
    """Draw a full-page capture as large as the box allows. A page too long for
    one column is cut into equal columns that read left to right; a column is
    only added when it buys more than a marginal gain in scale."""
    im = Image.open(path)
    iw, ih = im.size
    options = []
    for n in (1, 2, 3):
        cw = (box_w - gutter * (n - 1)) / n
        options.append((n, cw, min(cw / iw, (n * box_h) / ih)))
    best = max(o[2] for o in options)
    ncol, cw, scale = next(o for o in options if o[2] >= best * 0.88)
    draw_w = iw * scale
    total_h = ih * scale
    used = max(1, min(ncol, -(-int(round(total_h * 100)) // int(box_h * 100))))
    per = total_h / used
    slice_px = ih / used
    os.makedirs(SLICES, exist_ok=True)
    tag = os.path.splitext(os.path.basename(path))[0]
    x0 = x if used > 1 else x + (box_w - draw_w) / 2.0
    for i in range(used):
        top = int(round(i * slice_px))
        bot = int(round((i + 1) * slice_px)) if i < used - 1 else ih
        piece = im.crop((0, top, iw, bot))
        target_px = int(draw_w / 72.0 * 220)
        if piece.width > target_px:
            piece = piece.resize(
                (target_px, max(1, int(piece.height * target_px / piece.width))),
                Image.LANCZOS)
        sp = os.path.join(SLICES, "%s-%d.png" % (tag, i))
        piece.save(sp)
        h_pt = (bot - top) * scale
        cx = x0 + i * (draw_w + gutter)
        c.drawImage(ImageReader(sp), cx, y_top - h_pt, width=draw_w, height=h_pt)
        c.setStrokeGray(HAIR)
        c.setLineWidth(0.5)
        c.rect(cx, y_top - h_pt, draw_w, h_pt, stroke=1, fill=0)
    return used, draw_w, x0


# ------------------------------------------------------------------- content

DIRECTIONS = [
    {
        "key": "A",
        "name": "The apparatus talks",
        "leash": "ANCHORED",
        "axis": "TYPOGRAPHY AND COMPOSITION",
        "shot": "a",
        "landing_note": "Masthead, 5px datum, one 154px serif question against a rail. "
                        "Fig. 1 is a whole Deep sheet in live HTML off the print spec.",
        "interior_note": "Install and the compatibility ledger. Four routes at equal "
                         "weight, status terms defined above the table, a tally under "
                         "the closing rule.",
        "bet_line": "Put back a datum you can point at and a named furniture set, and "
                    "half the prose deletes itself with nothing lost.",
        "bet": "The site has no grid and no apparatus, so its labels grew into "
               "sentences. Restore a datum you can point at and a named furniture set, "
               "and half the prose deletes itself with nothing lost.",
        "mechanism": "Five declared type steps and nothing off-scale. One vertical "
                     "hairline runs the page, and every band is a rail label beside one "
                     "object. Fig. 1 sets a complete Deep sheet in live HTML off the "
                     "print spec's own numbers, carrying the committed specimen "
                     "verbatim. The ledger defines its terms above the table and closes "
                     "on a tally: rows verified end to end, 1 / 5. Outside session "
                     "reports on file, 0.",
        "costs": [
            ("Warmth.",
             "Bureau at nearly 100 per cent, with no Basement voice and not one funny "
             "line. The printed system is a hybrid for a reason, and this is half of "
             "it."),
            ("One instrument, and a phone takes it away.",
             "Every effect is scale against a datum. At 420px the question is 50px, the "
             "rail is a caption, and Fig. 1 is a sideways scroll."),
            ("A second, ungated copy of the print spec.",
             "Fig. 1 restates design.md in CSS and nothing checks it. build.sh fails on "
             "coupling drift; nothing watches the website. It had already drifted in "
             "three places before it shipped."),
            ("A fourth register.",
             "The site's own sentences are Plex Sans regular. Declared in the colophon, "
             "still a rule the sheets do not break."),
            ("The middle.",
             "With no lead size, anything needing 120 words becomes a table or gets "
             "cut, and some of it should not have been."),
            ("The ledger got slower.",
             "Filter chips became five rows you have to read, on the one page whose job "
             "is getting somebody installed."),
        ],
        "breaks": [
            ("The pattern library.",
             "A rail and five steps carry a ledger of thirty rows and carry the body of "
             "one pattern badly. Thirty screens of undifferentiated Sans is the "
             "tax-document failure."),
            ("Emotionally heavy content.",
             "The serial disclosure kit is about professional setbacks. Scale is this "
             "direction's only gear and it is the wrong one there."),
            ("The unshot photograph.",
             "A real one lands in Plate 1 as the highest-contrast object on the page, "
             "and every composition decision above it needs re-weighing."),
        ],
        "copy": "About 270 words on the landing page and 320 on the interior. Every "
                "claim is either verbatim repository text or a sentence somebody can be "
                "wrong about in public.",
    },
    {
        "key": "B",
        "name": "Six rows and an end",
        "leash": "ANCHORED",
        "axis": "STRUCTURE AND BEHAVIOUR",
        "shot": "b",
        "landing_note": "The front door as an index. Six numbered first-person "
                        "preconditions that are the table of contents and the router at "
                        "once, on one screen, in 122 words.",
        "interior_note": "Install as two folioed sheets. Two install tracks at equal "
                         "column width, then the ledger and a tally that publishes the "
                         "project's own worst number at display size.",
        "bet_line": "A site for a product whose success is you closing the tab has to be "
                    "finite, addressable, and visibly over.",
        "bet": "A website for a product whose success is you closing the tab has to be "
               "finite, addressable, and visibly over. Every page is one bounded "
               "screen: datum rule, closing rule, folio, and nothing after that.",
        "mechanism": "Four type sizes with a deliberate hole where a lead paragraph "
                     "would get written. The front door is an index: six numbered "
                     "first-person preconditions, each one click from its destination, "
                     "122 words on one screen. On Install, the rule that neither track "
                     "may be favoured is enforced by column width rather than asserted. "
                     "The ledger closes on a 5rem 1 beside OF FIVE ROWS CARRIED A PAGE "
                     "ALL THE WAY ROUND.",
        "costs": [
            ("The door refuses to argue.",
             "d = 0.93, 58 per cent and confidence held steady all sit behind row 06. A "
             "reader who arrives cold and will not click gets thirteen words of Serif."),
            ("The 50 per cent law is demoted.",
             "Acreage becomes deference: no hero, no colour, no type louder than the "
             "sheet. The band above the closing rule is a tenth of the screen and is "
             "called .margin."),
            ("Growth stops at six rows.",
             "A seventh route means redesigning the front door rather than appending to "
             "it."),
            ("The folio over-claims.",
             "It publishes six pages and five do not exist yet. A five-page site with a "
             "six-page folio is worse than no folio, so this cannot ship half-built."),
            ("The behavioural budget is one gesture.",
             "On an axis named structure and behaviour, structure carries almost all of "
             "it, and the direction knows it is a defence rather than a rebuttal."),
        ],
        "breaks": [
            ("evidence.md as a page.",
             "Sixty citations do not divide into bounded screens. The folio either lies "
             "about arbitrary cuts or the page scrolls under a chassis whose whole "
             "claim is that pages end."),
            ("A third install track.",
             "Equal column width is honest only while there are two. Add the paste path "
             "and the layout claims a parity that path does not have."),
            ("A stranger.",
             "Routing by first-person statement works when the statements exhaust the "
             "audience. Somebody who fits none of the six has only the source link."),
        ],
        "copy": "122 words on the index, 369 on Install, most of them ledger cells and "
                "shell commands. Flat on purpose: short and canned is still canned, and "
                "the alternative to marketing prose is a filing.",
    },
    {
        "key": "C",
        "name": "The site supplies the pen",
        "leash": "FREE",
        "axis": "TYPOGRAPHY AND COMPOSITION",
        "shot": "c",
        "landing_note": "Six numbered sections in a rail, content and margin grid. The "
                        "site's own opinions live only in the margin, written as pen "
                        "marks in the sheet's own protocol.",
        "interior_note": "Install. Three routes on dark machine plates at equal weight, "
                         "status terms defined above the ledger, and one row of five in "
                         "green with the page saying so.",
        "bet_line": "No reader will ever put a pen on a website, so the site supplies "
                    "the pen: every colour on it is ink.",
        "bet": "The sheet is grayscale so the pen can be the loudest thing on it, and "
               "no reader will ever put a pen on a website. So the site supplies the "
               "pen: every colour on it is ink, and its own opinions are margin notes "
               "in the sheet's own protocol.",
        "mechanism": "Two of three faces change. Newsreader asks, Archivo is furniture, "
                     "and Plex Mono stays, because the machine's words are the same "
                     "words in both places. Four inks at identical lightness and "
                     "chroma, hue the only variable. Repository text sits on a dark "
                     "plate with its source named and nothing glossing it. The landing "
                     "page carries the same sheet twice: printed, and returned.",
        "costs": [
            ("It is louder than the product.",
             "A dark plate and three saturated inks is more visual event than design.md "
             "permits anywhere. A visitor sold by this page prints something quieter."),
            ("The container leaks where the content is hardest.",
             "The ledger's definitions and cells are 278 words of ordinary explanatory "
             "prose, more than every margin note on both pages combined."),
            ("It teaches a protocol nobody asked to learn.",
             "The colour means nothing until the ink key is read, and the ink key is in "
             "the footer."),
            ("No exit for 4,000 pixels.",
             "Open territory closes the page, so the links close it too. There is no "
             "navigation until section 04."),
            ("The shared identity goes.",
             "Somebody who loves the sheet meets a stranger, set in two faces the "
             "repository does not own."),
            ("The returned specimen is cleaner than any real one.",
             "When the photograph is finally shot, the drawing will look better than "
             "the truth."),
            ("The margin is a desktop device.",
             "Below 1024px the grid collapses and the layout stops enforcing the cap on "
             "the site's voice."),
        ],
        "breaks": [
            ("The limitations page.",
             "Six items needing real nuance, where the site's voice is a three-sentence "
             "note, and a page whose every mark is red reads as an error state."),
            ("The pattern library.",
             "A page that is nothing but content, under a mechanism built to keep "
             "content out of the site's voice."),
            ("Anyone printing the website.",
             "Dark plates, on a site about printing. The only defence is a print "
             "stylesheet nobody has written."),
        ],
        "copy": "The site may ask and annotate. It may not explain. 158 words of margin "
                "notes on the landing page. No study tests this artifact is a red mark, "
                "in the ink the product tells you to use for exactly that.",
    },
    {
        "key": "D",
        "name": "The page is a sheet",
        "leash": "FREE",
        "axis": "STRUCTURE AND BEHAVIOUR",
        "shot": "d",
        "landing_note": "The sheet on the front door is in the DOM at Letter "
                        "proportions. Two radios switch it between knowing nothing "
                        "about you and having done work. Ctrl+P produces the artifact.",
        "interior_note": "The return trip, chosen because it is the half of the loop "
                         "that already works today on paper the visitor has. It is also "
                         "the one page colour is permitted on.",
        "bet_line": "Stop describing the loop and do the half a static page can do. "
                    "Hand the visitor a real sheet, then end.",
        "bet": "Stop describing the loop and complete the half a static page is capable "
               "of. Hand the visitor a real sheet for the paper already on their desk, "
               "put the sheet that withholds and the sheet that proposes under one "
               "switch, and then end.",
        "mechanism": "The sheet is in the DOM at Letter proportions, with a print "
                     "stylesheet set to design.md's numbers: 54pt margins, 2pt datum, "
                     "108pt open-territory floor. Both states print as a single 612 by "
                     "792 page and both pass verify_layout.py. Two radios and no "
                     "JavaScript: state 01 knows nothing about you, state 02 puts five "
                     "of the project's own claims in an I PROPOSE column against an "
                     "empty YOU DECIDE. Printing ends the document.",
        "costs": [
            ("The verify gate ran by hand.",
             "Twice, in one engine, on content that never changes. Firefox and Safari "
             "lay the same CSS out differently and nothing checks them."),
            ("The stop fires on a cancelled dialogue.",
             "afterprint arrives whether the sheet printed or the visitor pressed "
             "Escape. A platform ambiguity built on, not a stance."),
            ("The machine's column argues about the wrong subject.",
             "The only work this website has honestly done is its own argument, so I "
             "PROPOSE proposes claims about paper-session."),
            ("A switch has to be noticed.",
             "State 01 is the default, and the whole correction rides on one pair of "
             "small tracked-caps labels."),
            ("Below 620px the sheet stops being Letter.",
             "It drops the aspect ratio to stay legible, so a phone never sees the "
             "proportions the argument rests on."),
            ("Room for two pages.",
             "The pattern library, the named formats and the research process have "
             "nowhere to go, and Serif restricted to questions leaves no long-form "
             "register."),
            ("The faces come from a CDN.",
             "The repository ships Plex locally; these pages load it from Google Fonts "
             "and degrade silently when that is blocked."),
        ],
        "breaks": [
            ("The pattern library.",
             "Twenty-odd patterns with evidence clusters is a document. Rendered here "
             "it becomes a list of names."),
            ("The group formats.",
             "Brainwriting rounds is one page pattern printed six times, and a site "
             "built around here is your one sheet cannot express a kit."),
            ("A phone visitor with no printer and no notebook.",
             "Both verbs resolve to paper, and the page has nothing else to offer them "
             "but a link out."),
        ],
        "copy": "411 words in the site's own voice across both pages, counted the least "
                "flattering way, against 25,848 across the seven pages it replaces. "
                "Mono carries the propositions, because a reader is invited to strike "
                "those out.",
    },
]


# --------------------------------------------------------------------- pages

def page_cover(c, total):
    chrome(c, 1, total, "PAPER SESSION · SITE DESIGN SPRINT", "COVER")
    c.setFont("SansB", 21)
    c.setFillGray(INK)
    c.drawString(M, TITLE_Y - 4, "Four directions for the website")
    tracked(c, M, TITLE_Y - 24,
            "COMMISSIONED " + DATE + " · FOUR POSITIONS, NOT FOUR POLISHES",
            size=6.8, track=1.2, gray=FURN)

    y = TITLE_Y - 52
    y = para(c, M, y,
             "The site at site/ was read and judged super wordy and very canned AI "
             "looking. Four directions were built against that verdict, each as two "
             "working HTML pages and a written argument, each critiqued and revised "
             "before it got here. They are renders of real files, not mockups.",
             COLW, size=10.5, lead=14.5, gray=INK)

    y -= 12
    rule(c, y, w=1.6, gray=INK)
    y -= 14
    tracked(c, M, y, "THE 2 × 2 THAT GENERATED THEM", size=6.8, track=1.3, gray=FURN)
    y -= 20

    rail_w, gut = 72.0, 14.0
    cw = (COLW - rail_w - gut) / 2.0
    cx = [M + rail_w, M + rail_w + cw + gut]
    tracked(c, cx[0], y, "TYPOGRAPHY AND COMPOSITION", size=6.5, track=1.1, gray=QUIET)
    tracked(c, cx[1], y, "STRUCTURE AND BEHAVIOUR", size=6.5, track=1.1, gray=QUIET)
    y -= 8
    rule(c, y, w=0.5, gray=HAIR)

    rows = [("ANCHORED", "Stays inside the sheet's law: IBM Plex, grayscale, three "
                         "voices."),
            ("FREE", "Allowed to leave it, and has to say what that buys.")]
    for ri, (label, gloss) in enumerate(rows):
        y -= 18
        top = y
        tracked(c, M, y, label, font="SansB", size=8.0, track=1.4, gray=INK)
        yy = para(c, M, y - 13, gloss, rail_w - 6, font="Sans", size=7.4, lead=9.6,
                  gray=QUIET)
        low = yy
        for ci in range(2):
            d = DIRECTIONS[ri * 2 + ci]
            x = cx[ci]
            c.setFont("SansB", 21)
            c.setFillGray(INK)
            c.drawString(x, top - 6, d["key"])
            c.setFont("SansSB", 10.5)
            c.drawString(x + 22, top - 6, d["name"])
            b = para(c, x, top - 26, d["bet_line"], cw, font="SerifI", size=9.5,
                     lead=12.5, gray=INK2)
            low = min(low, b)
        y = low - 14
        rule(c, y, w=0.5, gray=HAIR)

    y -= 30
    c.setFont("Serif", 13)
    c.setFillGray(INK)
    c.drawString(M, y, "Which of these is the site?")
    y -= 20
    para(c, M, y,
         "The four disagree about what replaces the prose. Page 15 puts the bets side "
         "by side and states the question plainly.",
         COLW, size=9.5, lead=12.5, gray=QUIET)


def page_howto(c, total):
    chrome(c, 2, total, "PAPER SESSION · SITE DESIGN SPRINT", "HOW TO READ THIS")
    head(c, "How to read this", "TWELVE PAGES OF DIRECTIONS, THEN ONE QUESTION")

    y = BODY_TOP
    y = para(c, M, y,
             "Each direction gets three pages: the landing page as rendered, the "
             "interior page as rendered, and its argument set as type. The renders are "
             "full pages at 1400px, reduced. Where a page ran too long for one column "
             "it is cut into columns that read left to right, and the cut is labelled.",
             COLW, size=10.5, lead=14.5)
    y -= 4
    y = para(c, M, y,
             "These are four positions rather than four polishes. They were built to "
             "disagree, so the set is only useful if the disagreements stay visible. "
             "Averaging them produces a safe middle, which is the outcome the printed "
             "design sprint was explicitly instructed to avoid and the outcome this one "
             "is aimed away from too.",
             COLW, size=10.5, lead=14.5)

    y -= 12
    rule(c, y, w=1.6, gray=INK)
    y -= 14
    tracked(c, M, y, "WHAT IS BEING ASKED OF YOU", size=6.8, track=1.3, gray=FURN)
    y -= 20
    asks = [
        ("Read the costs before the bets.",
         "Every argument page gives its cost section more room and a heavier rule than "
         "its bet, on purpose. A page that sells without costing is the rigged vote "
         "this format exists to prevent."),
        ("Judge the position, not the polish.",
         "All four were revised after a critique pass, so none of them is arguing from "
         "a defect you can point at. What is left to choose between is what each one "
         "believes a website for this product is for."),
        ("Two of them break rules the sheets enforce.",
         "C leaves grayscale and leaves IBM Plex. D moves the verify gate outside the "
         "machinery that owns it. Both name the break rather than hiding it. Whether "
         "the website is bound by the sheet's law is a decision only you can make."),
        ("A hybrid is allowed.",
         "The printed system is one. Take whole organs rather than splitting "
         "differences, which is the instruction that produced design.md."),
    ]
    for name, body in asks:
        y = rich(c, M, y, [(name + " ", "SansSB", 10.0, INK),
                           (body, "Sans", 10.0, INK2)], COLW, lead=13.6)
        y -= 4

    y -= 6
    rule(c, y, w=0.5, gray=HAIR)
    y -= 14
    tracked(c, M, y, "WHAT THIS DOCUMENT IS SET IN", size=6.8, track=1.3, gray=FURN)
    y -= 18
    para(c, M, y,
         "IBM Plex, grayscale, US Letter portrait at 54pt margins, verified by "
         "verify_layout.py like any sheet. Serif carries the propositions and the "
         "closing question. Mono is quoted material. Tracked Sans caps is furniture. "
         "The running prose is Plex Sans regular, which is a fourth register the "
         "printed system does not have and does not need, since it prints no prose. "
         "The plates are the exception. C and D use colour, and reproducing them in "
         "gray here would misreport them.",
         COLW, size=9.5, lead=12.8, gray=QUIET)


def page_shot(c, d, which, page_no, total):
    key = d["key"]
    run = "%s · %s × %s" % (key, d["leash"], d["axis"])
    chrome(c, page_no, total, run,
           ("LANDING PAGE" if which == "landing" else "INTERIOR PAGE"))
    head(c, "%s · %s" % (key, d["name"]),
         ("THE LANDING PAGE, AS RENDERED" if which == "landing"
          else "THE INTERIOR PAGE, AS RENDERED"))
    y = META_Y - 16
    y = para(c, M, y, d["bet_line"], COLW, font="SerifI", size=10.0, lead=13.0,
             gray=INK2)
    y = para(c, M, y, d[which + "_note"], COLW, font="Sans", size=9.0, lead=11.8,
             gray=QUIET)
    y -= 14
    rule(c, y, w=0.5, gray=HAIR)
    box_top = y - 12
    box_h = box_top - (BODY_BOTTOM + 14)
    path = os.path.join(SHOTS, "%s-%s.png" % (d["shot"], which))
    used, draw_w, x0 = place_shot(c, path, M, box_top, COLW, box_h)
    if used > 1:
        tracked(c, M, BODY_BOTTOM,
                "ONE PAGE, CUT INTO %d COLUMNS THAT READ LEFT TO RIGHT" % used,
                size=6.4, track=1.1, gray=FURN)
    im = Image.open(path)
    tracked_right(c, RIGHT, BODY_BOTTOM,
                  "RENDERED AT 1400 × %d CSS PX" % (im.size[1] // 2),
                  size=6.4, track=1.1, gray=FURN)


def page_argument(c, d, page_no, total):
    key = d["key"]
    run = "%s · %s × %s" % (key, d["leash"], d["axis"])
    chrome(c, page_no, total, run, "THE ARGUMENT")
    head(c, "%s · %s" % (key, d["name"]), "THE ARGUMENT")

    rail_w, gut = 104.0, 12.0
    cx = M + rail_w + gut
    cw = RIGHT - cx

    y = BODY_TOP + 4

    def section(y, label, weight, gap=13.0):
        rule(c, y, w=weight, gray=INK if weight >= 1.0 else HAIR)
        y -= gap
        w = tracked_width(label, "SansSB", 6.4, 1.0)
        if w > rail_w - 4:
            raise SystemExit("rail label too wide: %s (%.1f)" % (label, w))
        tracked(c, M, y, label, size=6.4, track=1.0, gray=FURN)
        return y

    y = section(y, "THE BET", 1.6)
    y = para(c, cx, y, d["bet"], cw, font="Serif", size=11.0, lead=14.4, gray=INK)
    y -= 16

    y = section(y, "THE MECHANISM", 0.5)
    y = para(c, cx, y, d["mechanism"], cw, font="Sans", size=10.0, lead=13.0,
             gray=INK2)
    y -= 6

    y = section(y, "WHAT IT GIVES UP", 1.6)
    for name, body in d["costs"]:
        y = rich(c, cx, y, [(name + " ", "SansSB", 10.0, INK),
                            (body, "Sans", 10.0, INK2)], cw, lead=13.0)
        y -= 4
    y -= 4

    y = section(y, "WHERE IT BREAKS", 0.5)
    for name, body in d["breaks"]:
        y = rich(c, cx, y, [(name + " ", "SansSB", 10.0, INK),
                            (body, "Sans", 10.0, QUIET)], cw, lead=13.0)
        y -= 4
    y -= 4

    y = section(y, "THE COPY POSITION", 0.5)
    y = para(c, cx, y, d["copy"], cw, font="Sans", size=10.0, lead=13.0, gray=INK2)

    if y < BODY_BOTTOM:
        raise SystemExit("argument %s overflows the page: y=%.1f" % (key, y))


def page_compare(c, total):
    chrome(c, total, total, "PAPER SESSION · SITE DESIGN SPRINT", "THE CHOICE")
    head(c, "The four bets, and the question",
         "ALL FOUR DELETE THE PROSE · THEY DISAGREE ABOUT WHAT REPLACES IT")

    y = BODY_TOP
    gut = 16.0
    cw = (COLW - gut) / 2.0
    cols = [M, M + cw + gut]
    replaces = {
        "A": "Replaces prose with apparatus. A grid, a figure, a table, a tally.",
        "B": "Replaces prose with an index that routes and refuses to argue.",
        "C": "Replaces prose with the pen. The site annotates its own claims.",
        "D": "Replaces prose with the artifact. The page is a sheet you print.",
    }
    for i, d in enumerate(DIRECTIONS):
        col, row = i % 2, i // 2
        x = cols[col]
        top = y - row * 132
        c.setFont("SansB", 16)
        c.setFillGray(INK)
        c.drawString(x, top, d["key"])
        c.setFont("SansSB", 10.0)
        c.drawString(x + 18, top, d["name"])
        tracked(c, x, top - 13, d["leash"] + " × " + d["axis"], size=6.2,
                track=1.0, gray=FURN)
        yy = para(c, x, top - 30, d["bet_line"], cw, font="SerifI", size=9.6,
                  lead=12.4, gray=INK)
        yy = para(c, x, yy - 2, replaces[d["key"]], cw, font="Sans", size=9.0,
                  lead=11.6, gray=INK2)
        yy = para(c, x, yy - 2, "Costs most: " + {
            "A": "warmth, and a phone, which takes its only instrument away.",
            "B": "persuasion. The evidence is behind a click.",
            "C": "the shared identity, and a claim it has no ink to make.",
            "D": "the gate, which here ran by hand in one browser.",
        }[d["key"]], cw, font="Sans", size=9.0, lead=11.6, gray=QUIET)

    y = y - 132 - 108
    rule(c, y, w=0.5, gray=HAIR)
    y -= 13
    tracked(c, M, y, "WHAT ALL FOUR AGREE ON", size=6.6, track=1.2, gray=FURN)
    y -= 17
    y = para(c, M, y,
             "No hero paragraph, no chip filter, no call to action above the fold, and "
             "no upgraded compatibility claim. All four print the ledger with its terms "
             "defined above the table. And all four name the pattern library as the "
             "page they cannot carry, which is the strongest shared finding in the set: "
             "whatever wins here still owes that page a home.",
             COLW, size=9.6, lead=12.8, gray=INK2)

    y -= 14
    rule(c, y, w=1.6, gray=INK)
    y -= 15
    tracked(c, M, y, "THE QUESTION", size=6.6, track=1.2, gray=FURN)
    y -= 26
    c.setFont("Serif", 15.5)
    c.setFillGray(INK)
    for line in wrap("How much is the website allowed to be the thing, rather than "
                     "argue for it?", "Serif", 15.5, COLW):
        c.drawString(M, y, line)
        y -= 19.5
    y -= 6
    para(c, M, y,
         "A and B argue for it from inside the sheet's law. C and D leave that law to "
         "get closer to the artifact, and each says what the trip cost. Answering the "
         "question picks a direction. Refusing it picks a hybrid, and the hybrid is "
         "only worth having if it takes whole organs.",
         COLW, size=9.6, lead=12.8, gray=QUIET)


def main():
    register_fonts()
    total = 2 + len(DIRECTIONS) * 3 + 1
    c = pdfcanvas.Canvas(OUT, pagesize=(PW, PH))
    c.setTitle("Paper Session: Four Directions for the Website")
    c.setAuthor("Paper Session design sprint")

    page_cover(c, total)
    c.showPage()
    page_howto(c, total)
    c.showPage()

    n = 3
    for d in DIRECTIONS:
        page_shot(c, d, "landing", n, total)
        c.showPage()
        n += 1
        page_shot(c, d, "interior", n, total)
        c.showPage()
        n += 1
        page_argument(c, d, n, total)
        c.showPage()
        n += 1
    page_compare(c, total)
    c.showPage()
    c.save()
    print("wrote %s (%d pages)" % (OUT, total))


if __name__ == "__main__":
    main()
