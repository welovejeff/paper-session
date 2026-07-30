#!/usr/bin/env python3
"""verify_layout.py: fail a generated Paper Session PDF if text overlaps or escapes the page.

Usage: python3 verify_layout.py sheet.pdf [more.pdf ...]
Exit 0 = all pass. Exit 1 = failures printed, fix and regenerate.
"""
import sys

try:
    import pdfplumber
except ImportError:
    sys.exit("pdfplumber required: pip install pdfplumber --break-system-packages")

OVERLAP_FRAC = 0.25   # flag if intersection exceeds this fraction of the smaller word's area
EDGE_PAD = 4          # pt of forgiveness at page bounds
CHAR_H_FRAC = 0.4     # horizontal bite out of the narrower glyph before it counts
CHAR_V_FRAC = 0.5     # ... and how much of the shorter glyph must share its band


def boxes_overlap(a, b):
    ix = min(a["x1"], b["x1"]) - max(a["x0"], b["x0"])
    iy = min(a["bottom"], b["bottom"]) - max(a["top"], b["top"])
    if ix <= 0 or iy <= 0:
        return 0.0
    inter = ix * iy
    area_a = (a["x1"] - a["x0"]) * (a["bottom"] - a["top"])
    area_b = (b["x1"] - b["x0"]) * (b["bottom"] - b["top"])
    smaller = max(min(area_a, area_b), 0.01)
    return inter / smaller


def char_collisions(page):
    """Glyphs that physically collide, found at character level.

    The word-level pass below cannot see a same-baseline collision at all:
    pdfplumber merges characters that overlap on a shared baseline into ONE
    word (two strings stamped over each other come back as a single
    'LONGLVAABLEULEHERE'), so there is never a second box to compare. That is
    the likeliest real defect on a react pair or a rank row, where an
    overlong Mono item runs into the column beside it, so it gets its own
    check.

    Rotated glyphs are excluded: each one occupies the same x-range as its
    neighbour, so a rotated run reads as a column of mutual overlaps. The
    vertical-share test would mostly reject them anyway, but the gutter hint
    ("cross out freely") is rotated by design, so this is explicit.
    """
    chars = sorted((c for c in page.chars
                    if c.get("upright", True) and not c["text"].isspace()),
                   key=lambda c: c["x0"])
    problems = []
    active = []
    for cur in chars:
        # sweep line: only glyphs still horizontally in range can collide
        active = [p for p in active if p["x1"] > cur["x0"]]
        for prev in active:
            h = min(prev["x1"], cur["x1"]) - cur["x0"]
            v = min(prev["bottom"], cur["bottom"]) - max(prev["top"], cur["top"])
            if h <= 0 or v <= 0:
                continue
            narrow = min(prev["x1"] - prev["x0"], cur["x1"] - cur["x0"])
            short = min(prev["bottom"] - prev["top"], cur["bottom"] - cur["top"])
            # kerning and italic sidebearings overlap slightly and legitimately,
            # so require a real bite out of the smaller glyph
            if (narrow > 0 and short > 0
                    and h / narrow > CHAR_H_FRAC and v / short > CHAR_V_FRAC):
                problems.append(
                    f"collides: '{prev['text']}' x '{cur['text']}' "
                    f"at ({cur['x0']:.0f},{cur['top']:.0f})")
        active.append(cur)
    return problems


def check(path):
    problems = []
    with pdfplumber.open(path) as pdf:
        for pno, page in enumerate(pdf.pages, 1):
            for p in char_collisions(page):
                problems.append(f"p{pno}: {p}")
            # Word-level pass, for collisions across different baselines.
            # Caveat, not a safeguard: extract_words returns rotated runs as one
            # merged bbox that can span a whole column, and the same-line
            # tolerance below does NOT exclude them — the rotated gutter hint
            # false-positives against left-column words on two of the four
            # Phase 3 specimens. Filter by `upright` here if that starts biting.
            words = page.extract_words(use_text_flow=False, keep_blank_chars=False)
            # page-bounds check
            for w in words:
                if (w["x0"] < -EDGE_PAD or w["x1"] > page.width + EDGE_PAD
                        or w["top"] < -EDGE_PAD or w["bottom"] > page.height + EDGE_PAD):
                    problems.append(f"p{pno}: text escapes page: '{w['text']}'")
            # pairwise overlap
            for i in range(len(words)):
                for j in range(i + 1, len(words)):
                    a, b = words[i], words[j]
                    # same-line neighbors sharing a baseline touch legitimately
                    same_line = abs(a["bottom"] - b["bottom"]) < 2.0
                    frac = boxes_overlap(a, b)
                    if same_line and frac < 0.6:
                        continue
                    if frac > OVERLAP_FRAC:
                        problems.append(
                            f"p{pno}: overlap {frac:.0%}: '{a['text']}' x '{b['text']}' "
                            f"at ({a['x0']:.0f},{a['top']:.0f})")
    return problems


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    failed = False
    for path in sys.argv[1:]:
        probs = check(path)
        if probs:
            failed = True
            print(f"FAIL {path}")
            for p in probs[:20]:
                print(f"  {p}")
            if len(probs) > 20:
                print(f"  ... and {len(probs) - 20} more")
        else:
            print(f"PASS {path}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
