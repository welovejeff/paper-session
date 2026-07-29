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


def check(path):
    problems = []
    with pdfplumber.open(path) as pdf:
        for pno, page in enumerate(pdf.pages, 1):
            # upright and rotated text checked separately; rotated words get
            # merged bboxes from pdfplumber that false-positive against columns
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
