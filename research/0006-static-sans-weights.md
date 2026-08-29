Status: Implemented
Date: 2026-08-28
Outcome: the `onramps` PR — the upstream static Sans faces of finding 9, a four-assertion font guard in `build.sh` and `verify.yml`, and a regenerated specimen. The unknown-1 print test is still open; see Validation.

# The Sans weights the sheets never had

## Scope

`paper-session/assets/fonts/` ships three IBM Plex Sans files under three
names. All three are the same variable font, and reportlab renders all three at
Regular. Every sheet the project has ever produced has printed its titles,
voice captions, and infrastructure labels at the wrong weight. This brief
establishes the defect, argues for replacing the three files with upstream
static TTFs, adds a build guard so it cannot recur, and — the part that makes
this more than a bugfix — asks honestly whether restoring the real weights
threatens the one visual invariant the system is built around.

It decides no printed rule — though unknown 2 names the one way that could
change. If the print test at the end says a remedy is needed, that remedy
changes `design.md`, and its source lands in `evidence.md` — see **What
`evidence.md` would owe**, below.

## Sources

Everything numeric below was measured on this machine on 2026-08-28 with
fontTools 4.63.0, reportlab 5.0.1, and PyMuPDF, against the files in the repo
at commit `1febaaa`. Nothing is quoted from memory.

- The eight files in `paper-session/assets/fonts/` and
  `LICENSE-IBMPlex.txt`.
- `docs/specimen.py`, `docs/specimen.pdf`, `docs/sheet-*.png`.
- `docs/design-history/` — the four direction PDFs, `hybrid-specimen.pdf`, and
  `0-Direction-Notes.md`.
- `paper-session/references/design.md` §0, §1, §2, §3, §9.
- `paper-session/scripts/verify_layout.py`, `build.sh`,
  `.github/workflows/verify.yml`, `THIRD-PARTY-NOTICES.md`.
- Upstream: https://github.com/IBM/plex, release `@ibm/plex-sans@1.1.0`
  (2024-11-13), asset `ibm-plex-sans.zip`.
- SIL Open Font License 1.1, as shipped in `LICENSE-IBMPlex.txt`.

**Ink units, defined once, because every figure below rests on the
definition.** An element is drawn by reportlab onto an otherwise blank 612×792
page, that page is rendered by PyMuPDF at 300 dpi in grayscale, and the result
is summed as Σ(255 − pixel) over every pixel on it. One ink unit is one
grayscale step on one 1/300-inch pixel; a fully black pixel contributes 255.
The unit is arbitrary, the ratios are not, and every ink figure in findings 11,
13, 14, and 15 is that sum under that method. Anyone re-measuring should
reproduce the 2pt datum rule at **4,462,625** first; if that digit matches, the
rest will.

## Findings

1. **The three Sans files are one file, copied three times.** Each of
   `IBMPlexSans-Regular.ttf`, `-SemiBold.ttf`, and `-Bold.ttf` is exactly
   537,244 bytes. Byte-diffed pairwise they differ in **three bytes**, at
   offsets 275, 407, and 431 — and those three sit in two different structures,
   not two fields of one. The `head` table begins at file offset 396, so 407 is
   the last byte of `head.checkSumAdjustment` (404–407) and 431 the last byte
   of `head.modified` (424–431). Offset 275 is not inside `head` at all: it is
   the last byte of the checksum in the table directory's `head` entry, which
   starts at 268. The three `head.modified` values are 3868127773 / 3868127775
   / 3868127776 — three seconds from first to last, with 3868127774 unused, so
   three exports in a row from one source. Nothing else differs. Their MD5s
   differ, so a naive duplicate check would miss this.

2. **All three are variable fonts sitting at their default instance.** Each
   carries `fvar` with a `wght` axis 100–700 defaulting to **400** and a
   `wdth` axis 75–100 defaulting to 100, plus `gvar`, `avar`, `cvar`, `HVAR`,
   `MVAR`, and `STAT`. Each reports `usWeightClass 400`, 1025 glyphs,
   `nameID 1` "IBM Plex Sans", `nameID 2` "Regular", PostScript name
   `IBMPlexSans-Regular`, `Version 3.201`. The named instances for SemiBold and
   Bold exist inside the file; nothing selects them.

3. **reportlab renders the default instance and does not collapse the axis.**
   `pdfmetrics.stringWidth("WHAT ONLY YOU CAN DECIDE", face, 16)` returns
   **219.856 for all three** of `Sans`, `SansSB`, `SansB`. Rasterized at 300
   dpi, the three produce **byte-identical** pixmaps (same SHA-256). The
   comparison faces behave correctly: Serif Regular 234.08 vs Serif SemiBold
   241.28.

4. **It is worse than three faces rendering alike: only one face is ever
   embedded.** `pdfmetrics.registerTypeFace` stores `_typefaces[face.name]`,
   and `face.name` is read from the file's PostScript name. All three Sans
   files say `IBMPlexSans-Regular`, so the second and third registrations
   overwrite the first. A test PDF drawing all five of Sans / SansSB / SansB /
   Serif / SerifSB embeds **three** font subsets, not five:
   `IBMPlexSans-Regular`, `IBMPlexSerif-Regular`, `IBMPlexSerif-SemiBold`.

5. **This is Sans-only.** `IBMPlexSerif-SemiBold.ttf` is a clean static —
   `usWeightClass 600`, no `fvar`, PostScript name `IBMPlexSerif-SemiBold`,
   Version 2.6. `IBMPlexMono-Medium.ttf` likewise — `usWeightClass 500`, no
   `fvar`, Version 2.3. Serif Regular/Italic and Mono Regular are statics too.
   Five of the eight faces are correct; three are the same file.

6. **Every artifact in the repo confirms it.** `1-Bureau.pdf`,
   `2-FieldKit.pdf`, `3-MethodCard.pdf`, `4-BasementShow.pdf`,
   `hybrid-specimen.pdf`, and the committed `docs/specimen.pdf` each embed
   exactly one Sans subset, `AAAAAA+IBMPlexSans-Regular`, and no Sans Bold or
   SemiBold anywhere. (`4-BasementShow.pdf` embeds an `IBMPlexSerif-Bold` that
   is not in `assets/fonts/` today — the direction PDFs were rendered against a
   different font set than the one that shipped.) Re-running
   `docs/specimen.py` unchanged reproduces `docs/sheet-deep-react.png`
   **bit-identically**, so the README images are flat renders too.

7. **What has been printing at the wrong weight**, per `design.md` §2: the
   sheet title (SansB 16, gray 0), the voice captions `I PROPOSE` / `YOU
   DECIDE` (SansB 8, gray 0.2, tracked +1.2), section and open-territory
   labels (SansSB 6.8, gray 0.4, +1.4), the `HAND:` label (SansSB 6.5), the
   footer (SansSB 6.8), and the §9 private-page marker (SansSB 6.8). The
   elements that were already Regular — the date line, slot numbers, the ink
   key — are unaffected.

8. **Neither gate looks at weight.** `build.sh` checks that a `SKILL.md`
   `name:` matches its directory and that `assets/fonts/LICENSE-IBMPlex.txt` is
   inside the built bundle. `.github/workflows/verify.yml` restates both, in
   the steps "Each SKILL.md declares a name matching its directory" and "Fonts
   ship with their license". Neither has ever compared two font files, checked
   a `usWeightClass`, or noticed an `fvar` table. Nothing in the repo would
   catch this happening again.

9. **Upstream statics are reachable, unmodified, and smaller.** From release
   `@ibm/plex-sans@1.1.0`, `ibm-plex-sans/fonts/complete/ttf/`:
   Regular **200,500 B** (`usWeightClass 400`, PostScript `IBMPlexSans`),
   SemiBold **202,632 B** (600, `IBMPlexSans-SmBld`), Bold **200,872 B** (700,
   `IBMPlexSans-Bold`). The full sha256 digests, which is what "verified by
   SHA-256 against the tag" in the recommendation means in practice:

   ```
   975dcda37d80f038dcd143c22e33ca2d97a0cc5a929aace1c749153b0fe1afa5  IBMPlexSans-Regular.ttf
   a20caf8286023a6a7a85e40b1d2a4ae9fc3e3b1f9eda8f4c542dd4986af67bb1  IBMPlexSans-SemiBold.ttf
   9e6c74a889a700d707613d24548fe4ffa6bc59559a0689d2cf9e133bdcdafb2f  IBMPlexSans-Bold.ttf
   ```

   All three are Version 3.005, 1019 glyphs, no `fvar`, and **byte-identical**
   to the same paths under
   `raw.githubusercontent.com/IBM/plex/master/packages/plex-sans/fonts/complete/ttf/`,
   so the tag and the branch agree. Coverage does not regress: the statics map
   895 codepoints against the variable font's 891 and are a strict superset —
   the variable font maps nothing the statics do not. Same 1000 upm.

10. **The bundle gets smaller.** Sans faces: 1,611,732 B → 604,004 B, a
    **1,007,728 B (62.5%) reduction**. Rebuilding `paper-session.skill` with
    the statics, same deflate settings, takes it from 1,281,532 B to
    **674,571 B** — 606,961 B smaller, a 47.4% cut. (`zip` is not installed on
    this machine, so both bundle figures come from Python's `zipfile` at the
    same deflate level. The CLI-built artifact runs a few KB heavier: today's
    committed `paper-session.skill` is 1,286,030 B against `zipfile`'s
    1,281,532 B, a 4,498 B spread. Record the built number in Validation, not
    the predicted one.)

    Both install tracks benefit, but not equally, and one number moves the
    other way. The upload path is the 47.4% above. The CLI path installs the
    `paper-session/` directory, which goes 2,546,418 B → 1,538,690 B, a 39.6%
    cut. The whole working tree goes 4,817,704 B → about 3.20 MB, roughly 34%.
    A `git clone` gets *larger*: the 1.6 MB of variable-font blobs stays in
    history and about 604 KB of new blobs is added on top of it.

11. **Real weights are 50% and 70% more ink, and 2–5% more width.** Measured at
    the exact `design.md` §2 specifications against today's flat render, on
    five named strings so the figures can be checked:
    `WHAT ONLY YOU CAN DECIDE` at the title spec (SansB 16 / gray 0),
    `I PROPOSE` and `YOU DECIDE` at the caption spec (SansB 8 / gray 0.2 /
    +1.2), and `OPEN TERRITORY` and `WHAT THE MACHINE BROUGHT` at the label
    spec (SansSB 6.8 / gray 0.4 / +1.4). SemiBold lands **+49.5% to +50.0%**
    ink across all five. Bold lands **+69.0% to +69.8%** — tight, but a full
    point under 70 at the low end, so these are ~50% and ~70%, not constants.
    Width grows far less, and by how much depends on whether tracking counts:
    untracked set widths grow **+2.4% to +3.4%** (SemiBold) and **+3.5% to
    +4.8%** (Bold), while the same strings as actually set, tracking included,
    grow only **+1.8% to +3.0%** and **+2.6% to +4.3%** — the tracking is a
    constant that the extra width is diluted into, so the tracked labels move
    least. In the 504pt text block a 16pt title goes from 44 to 43 capital
    `N`s, or 35 to 32 capital `W`s.

12. **The regenerated specimen passes both gates unchanged.** With the statics
    dropped in and nothing else touched, `docs/specimen.py` runs clean: every
    `put()` text-block assertion holds and `verify_layout.py` reports PASS on
    all three pages. The visible change is exactly the intended one — the title
    reads as a title rather than a filename, and the captions separate from the
    Mono beneath them.

13. **The design system was selected against a render that never matched its
    own spec.** Finding 6 establishes that all four direction PDFs, the hybrid
    specimen, and `0-Direction-Notes.md`'s per-direction critique were produced
    with flat Sans. The notes' recorded worry about Basement Show — "the
    masthead and slab compete with the pen for loudest-thing-on-the-page" — was
    written about a masthead rendering roughly **41% lighter** than the
    direction specified: Bold is +70% ink over flat, so the flat render carried
    about 59% of the ink the direction asked for. One detail is suggestive
    rather than proven.
    `0-Direction-Notes.md` gives Bureau a **1.4pt** datum rule, and `design.md`
    §3 ships **2pt**. Measured, a 1.4pt full-width rule is 3,110,187 ink units
    and a 2pt rule is 4,462,625, against a flat 16pt title's 2,979,891 — the
    thickening restored a top-of-page hierarchy the missing weight had
    flattened. **This is a hypothesis about why the rule grew, not a claim
    that it did**; nobody wrote down a reason, and the appended record cannot
    now be asked.

14. **The pen-dominance invariant survives, on desk measurement.** `design.md`
    §0 and `CLAUDE.md` both require the pen to be the highest-contrast element
    on the completed page, with "if a blank sheet looks finished, reduce it" as
    the test. Whole-page ink on the three specimen pages rises **+6.8%, +7.3%,
    and +8.5%**; page coverage goes from 1.43/1.12/1.37% of the sheet to
    1.53/1.20/1.48%. The sheet is 98.5% white before and after. Calibrated
    against a 0.7mm ballpoint at the same 300 dpi, the whole change to page 1
    (2.1M ink units) is worth about **237pt of pen path — two short strikes**.
    A sparse pen response (~1,200pt of path, three strikes and a circled item)
    is 10.6M; a light fill (~6,000pt) is 53.2M; a filled Deep page (~20,000pt)
    is 177.2M against a printed layer of 32.9M.

15. **But "highest-contrast" was never a total-ink test, and the heaviest black
    mark on the page is not the one this change touches.** The printed layer
    already carries more total ink than a sparse pen response, before this
    change and after it — so the invariant has to mean per-element contrast,
    which is what the page actually delivers: the pen is solid black, larger,
    unbroken, and off the grid, while most of the printed layer is 6–9.5pt at
    30–50% gray, with MonoM 9.2 at gray 0.12 as the near-black outlier. What
    sits at gray 0 per §2 and §3 is four registers, not one: the 2pt datum rule
    (**4,462,625**), the SansB 16 title, the Serif 21 provocation, and the
    1.6pt caption and open-territory underlines.

    **The title's rank change is real but string-dependent**, which makes it a
    property of a particular title rather than of the page. On the repo's own
    specimen, pages 1 and 2 — "Fall Course: Session Arc" — go 2,117,858 →
    **3,605,130** in real Bold, still 19% *below* the datum rule, no rank
    change at all. Page 3 — "Wednesday 9:30 · Win the Week" — goes 3,033,171 →
    **5,100,588** and does cross it. The finding-11 test string behaves like
    page 3: 2,979,891 → **5,058,730**. One of three specimen pages changes
    rank at the top, not all of them.

    **And a heavier black mark has been printing all along.** Page 2's
    provocation is Serif 21 at gray 0, straight out of §2. Its **first line
    alone measures 6,525,022** ink units, both lines 10,480,113 — 28% heavier
    than the crossing-over title, 46% heavier than the datum rule, the heaviest
    single black mark on any of these sheets, and completely unaffected by this
    change. That is the honest frame for the print test, and it argues *for*
    Path A: a mark heavier than any restored title has been on these sheets
    since the first one, and pen dominance survived it. The title moving into
    that neighbourhood is a change at the top of the page worth looking at, not
    a new category of thing appearing on it.

## Options

**Path A — upstream statics, unmodified (recommended).** Replace the three
files with the release bytes from finding 9, under the same eight filenames.
`design.md` §1's register table is unchanged, `docs/specimen.py`'s `REGISTER`
map is unchanged, and nothing about the fonts is edited.

**Path B — instance the variable font at 600 and 700.** Technically easy:
`fonttools varLib.instancer` produces two statics from the file already
committed. **Rejected on the licence.** `LICENSE-IBMPlex.txt` opens
"Reserved Font Name \"Plex\"", OFL 1.1 defines a Modified Version as "any
derivative made by adding to, deleting, or substituting … or by changing
formats", and clause 3 forbids a Modified Version from using the Reserved Font
Name. Instancing deletes `fvar`, `gvar`, `avar`, `cvar`, `HVAR`, `MVAR`, and
`STAT` and rewrites `glyf`; the output is a Modified Version and may not be
called Plex. Clause 3 limits itself in its own next sentence — "This
restriction only applies to the primary font name as presented to the users" —
which is also how `THIRD-PARTY-NOTICES.md` already states the obligation, so
the compliance cost is smaller than it first looks: only the three instanced
faces need a new primary name, and filenames, the eight internal register names
in `design.md` §1, and prose documentation are not the primary font name. Even
at that size the trade is bad. It buys a rename obligation, an RFN judgment
call, and a `fonttools` build dependency, in exchange for a face that is,
glyph for glyph, one we can download unmodified — in a repo whose CI already
fails a build over the font licence.

**Path B′ — instance at generation time and never redistribute the result.**
Named because the licence does not close it, and nobody should read the
paragraph above as "variable Plex is off limits to this project". Instancing or
subsetting **inside the generation step, with the derived file never
redistributed**, is ordinary use of the font rather than a distributed Modified
Version, and the OFL has nothing to say about it. It loses
anyway, and not on the licence: it puts `fonttools` in the sheet-generation
path of a skill whose only runtime dependency today is reportlab, and it does
so to produce bytes we can simply ship (unknown 5).

**Path C — subset to the glyphs the sheets use.** Same objection, more
sharply: deleting glyphs is squarely the OFL's "deleting", so a subset is a
Modified Version needing a rename. It would also silently cap what a sheet can
print — every language, every dash, every arrow the pen protocol might want —
in exchange for bytes Path A already gives up for free.

**Path D — do nothing, and change `design.md` to say Regular.** Honest, and
worth naming because it is the only option that guarantees the pen-contrast
question stays answered. Rejected: it would delete the three-voice hierarchy's
Sans layer, leave the captions indistinguishable from the metadata, and codify
a rendering accident as intent.

## Risks / unknowns to validate

This list is the implementation PR's test plan.

1. **The print test — the brief's open question, and the only one that cannot
   be answered on this machine.** Everything in finding 14 is a pixel count on
   a screen. The rule it tests is about a completed sheet under a lamp. The
   test, precisely:

   - Apply Path A and run `python3 docs/specimen.py` to regenerate
     `docs/specimen.pdf` and the three PNGs. Keep the pre-change build as well
     — `git show 1febaaa:docs/specimen.pdf > flat-specimen.pdf` — because the
     control below needs it.
   - Print **both** specimens, all three pages each, on a **grayscale** printer
     (not a colour printer set to grayscale, if a mono laser is available), on
     ordinary white office paper, at 100% scale with no fit-to-page.
   - **The control is the blank pair, not a second hand-filled set.** Two
     sheets cannot be filled identically by hand, so an A/B on completed pages
     would compare handwriting rather than type. Blank pages compare exactly,
     and blank is what §0's own test asks about — "if a blank sheet looks
     finished, reduce it". Lay the flat print and the static print of the same
     page side by side under the same lamp and judge them as a pair, page by
     page, before anything is written on either.
   - Complete the three **post-change** sheets by hand with a **ballpoint** —
     the least-inky common pen, so the test runs against the pen's weakest
     case, not a fineliner's best. Fill them the way a real session would: the
     react page's right column, at least one strike and one circle from the §9
     protocol, and something in every open-territory band. A single ink is
     fine; the black-only sheet is the primary design case. The completed-page
     judgment is absolute — does the pen dominate this page — not comparative;
     the comparison already happened on the blanks.
   - Photograph each page with a phone, **handheld, in poor domestic evening
     lighting** — a lamp off to one side, no flash, some shadow across the
     page. Do not correct, crop, or brighten. Photograph one **blank**
     post-change page the same way; the scan-back probe below needs it.
   - Look at the prints at arm's length before photographing them, and answer
     one question in writing: **does the pen dominate, or does the top of the
     page now compete with it?** Look hardest at **page 3**, whose title is the
     one that actually overtakes the datum rule; pages 1 and 2's title stays
     19% below it (finding 15). Keep page 2's Serif provocation in view as the
     standing benchmark — it is the heaviest black mark on any of these sheets,
     it did not move, and if a restored title reads as louder than it, that is
     the finding.
   - Hand the photographs to `scan-back` in a fresh chat. **Degraded means one
     of four countable things**, not an impression: (i) on the blank-page
     photograph, scan-back reports any pen mark at all — the cleanest test that
     bolder print is being read as ink, and the one that needs no matched
     control; (ii) on a completed page, a printed label, caption, or footer is
     transcribed as handwriting; (iii) a printed rule or underline is
     attributed as a pen strike; (iv) scan-back asks for a retake. Record the
     count per page. Zero settles it; anything above zero names the specific
     element a remedy has to fix.

   **If the pen still dominates, nothing changes** and `design.md` is untouched.
   If it does not, the remedy hierarchy, cheapest first: (a) demote the sheet
   title from SansB 16 to **SansSB 16** — measured 4,471,133 ink units against
   Bold's 5,058,730, an 11.6% reduction at *zero* legibility cost, since the
   point size and the gray value do not move; (b) raise the caption gray from
   0.2 toward 0.3, which stays far above the §0 50% floor; (c) thin the datum
   rule from 2pt back toward Bureau's 1.4pt, if finding 13's hypothesis turns
   out to be right and the rule was compensation. **Not on the list: reducing
   any point size.** `evidence.md` closes that door from two directions:
   Cluster 10 bans making a sheet harder to read on purpose — "Difficulty
   belongs in the task, never in the typography" — and Cluster 11's legibility
   floors are what keep the smallest type and the palest grays above threshold
   in the first place.

2. **Text-block overflow that neither gate catches.** Finding 11 costs a 16pt
   title one to three characters. `verify_layout.py` checks the **page** bounds
   with 4pt of pad (lines 16, 88–91), not the 54pt text block: the test fires
   at `x1 > page.width + EDGE_PAD` = 616, so a title may overrun the text
   block's right edge at x=558 by a full **58pt** — the 54pt margin plus the
   4pt pad — and still pass. `docs/specimen.py`'s own `put()` assertion catches
   it for the specimen only — a skill-generated sheet has no equivalent. Test:
   generate a sheet with a title at the old width limit (44 capitals at 16pt)
   and confirm what each gate does. Widening the verifier to know about margins
   is a separate change and out of scope here; the finding belongs in the
   Validation section either way.

   Note where the durable fix would have to live if real weights do overflow
   long titles. `design.md` opens by promising a sheet can be implemented "from
   this file alone; no specimen reference required", so a title budget has to
   be a number in §2 or §4 — which makes it a printed rule, and makes that
   follow-up not the no-printed-rule change this brief is. One more reason the
   widening is its own brief with its own `evidence.md` line.

3. **The Mono and Serif pairs are only assumed clean.** Finding 5 checked their
   `usWeightClass` and the absence of `fvar`, and finding 3 checked one Serif
   width pair. The PR should run the same distinctness assertions across all
   eight faces before writing the guard, not just the three being replaced.

4. **Version skew inside the family — and it is not only a future path's
   problem.** After Path A the Sans faces are Plex 3.005 (2024) while the
   variable file they replace was 3.201 and Serif/Mono are 2.6/2.3. Some
   metrics are stable: 1000 upm, `hhea` 1025 / −275 / 0, capHeight 698 and
   xHeight 516 on Regular. The `OS/2` vertical metrics are not. Outgoing
   variable Regular against incoming static Regular: `sTypoAscender` 1025 →
   **780**, `sTypoDescender` −275 → **−220**, `sTypoLineGap` 0 → **300**,
   `usWinAscent` 1120 → **1025**. Baseline arithmetic in `design.md` §4 is
   unaffected — every position is absolute — and an HTML-to-PDF path would
   notice, but so does the gate this repo already runs on every sheet:
   reportlab's `TTFontFace` reads ascent/descent from those fields (1025/−275 →
   780/−220), writes them into the PDF FontDescriptor, and pdfplumber derives
   its character boxes from them. The Sans title's box top moves 64.40 → 63.52
   at 16pt, so `verify_layout.py`'s collision geometry for Sans shifts by about
   0.9pt **today**, not hypothetically. Finding 12's clean PASS is evidence
   that the shift is harmless across three pages, not a guarantee for
   skill-generated ones. Test: record the full metric table for all eight
   faces, and run the verifier against a deliberately tight Sans-on-Sans
   pairing to establish which way the shift moves a near-collision.

5. **The guard's own dependency cost.** `build.sh` currently needs only `zip`
   and `unzip`, checked up front, and refuses to run without them. Reading
   `usWeightClass` needs a parser. The four assertions below are ~25 lines of
   stdlib `python3` — no fontTools — walking the table directory once and
   reading three fields out of it, but `python3` becomes a third build
   prerequisite, which the tool-check loop must state as clearly as the other
   two and which `CLAUDE.md`'s Commands section has to name. The PR should
   confirm this is acceptable rather than assume it. Note also that `zip`
   itself is not installed on the machine these measurements were taken on, so
   whoever runs the PR has to install it before `./build.sh` will run at all.

## Recommendation

**Path A, plus a guard, in one PR.**

Replace the three Sans files with the release bytes named in finding 9,
verified by SHA-256 against the tag before committing. Same filenames, same
eight register names, no rename, no subsetting, no instancing, no edit to
`design.md` §1.

Add to `build.sh` four assertions over the eight shipped faces, in stdlib
`python3` with no third-party imports:

- **no shipped face carries an `fvar` table** — the most direct statement of
  the defect;
- **their PostScript names (`name` ID 6) are pairwise distinct** — this is the
  property reportlab actually keys on (finding 4), and the one that failed;
- **`usWeightClass` matches what the register implies** — Sans 400/600/700,
  Serif 400/400/600, Mono 400/500 — and the three Sans values are distinct;
- **the three Sans faces have distinct `glyf` table checksums**, read straight
  out of the table directory the other assertions are already walking. This is
  the one that closes the actual failure class, because the first three do not:
  three files correctly renamed and correctly reweighted but never
  re-outlined would pass all of them and still print flat. Measured today, the
  three shipped files all report `glyf` checksum 4293849195 at length 75592;
  the three statics report 3107858753 / 236080091 / 504137152 at 112856 /
  112088 / 112452. This is the single assertion that would have caught the bug
  on the day it landed.

**Where these go matters, and "immediately after the font-licence check" is the
wrong answer.** That check is the last thing in `build.sh` (lines 49–59), it
reads `unzip -Z1 paper-session.skill`, and it is wrapped in
`if [[ -f paper-session.skill ]]` — so `./build.sh scan-back` runs it against
whatever stale bundle happens to be on disk. The font assertions must read the
**source** files in `paper-session/assets/fonts/`, and must run **before** the
zip step, so a bad font never reaches a bundle at all. Put them in the
tool-check region at the top, after the `zip`/`unzip` loop.

Restate the same assertions as a `verify.yml` step named alongside "Fonts ship
with their license", following that job's existing convention of duplicating
`build.sh`'s checks rather than delegating to it.

Then regenerate: `python3 docs/specimen.py` (which rebuilds
`docs/specimen.pdf`, runs the verifier, and rewrites the three
`docs/sheet-*.png` the README uses), and `./build.sh` for both bundles.

**`CHANGELOG.md` owes an entry, and this is exactly what that file is for.**
The changelog's own preamble says entries describe what changes about the
sheets a person receives — and a person's sheet titles, voice captions, and
labels change weight. The entry belongs under a "Fixed" heading in
`[Unreleased]` and should say plainly that the bundled Sans SemiBold and Bold
were the same file as Regular, that every sheet printed before this ran flat,
and that titles and captions now carry the weight `design.md` always specified.
Not a refactor note; the reader looking at an old print and a new one deserves
the sentence that explains the difference.

**Three documents count the gates, and a third gate makes all three stale.**
`CLAUDE.md` (line 34), `README.md` (§Development, the "refuses to ship two
specific mistakes" sentence at line 320), and `CONTRIBUTING.md` (lines 45–47)
each enumerate `build.sh`'s failures as exactly two: name-matches-directory, and
fonts-ship-with-their-licence. Each has to gain the third in this same PR, in
its own register — a clause in CLAUDE.md's sentence, a sentence in README's,
a third item in CONTRIBUTING's list. `CLAUDE.md`'s Commands section also has to
name `python3` as a build prerequisite beside `zip` and `unzip` (unknown 5).
None of this is optional tidying: a repo that documents its gates in three
places and then adds one silently has three wrong documents.

**What `evidence.md` would owe.** Nothing, if the print test passes — Path A
changes no printed rule, it makes the rendering match the rule `design.md` §2
has always stated, so there is no new claim to source. If the test fails and a
remedy from unknown 1 ships, that remedy *is* a printed-rule change and its
source lands in `evidence.md`, not here. The entry that would be needed is an
honest negative, and it belongs in **Cluster 11**, which is where both of the
things it qualifies already live: **no study measures the contrast ratio
between a printed worksheet's type and a pen response on it.** The
pen-dominance law is design law, derived from Cluster 11's dropout-ink
inversion (which establishes that zero-chroma print makes any saturated stroke
provably the human's, and says nothing about printed weight) and Cluster 11's
legibility floors (which set a *minimum* on size and contrast and no maximum —
Cluster 10 is the desirable-difficulties cluster, and what it contributes here
is the separate, absolute ban on deliberate typographic difficulty, not the
floors themselves). Its "what this does not support" line writes itself: the floors license the
current small-caps-and-tracking usage, they do not license inferring a ceiling
on printed weight from them, and the ceiling this project enforces is a design
judgment with no measured basis. Say that, and then the remedy can be argued on
the print in front of the maintainer rather than on a citation that does not
exist.

**Not built here:** any change to `design.md` (the print test decides that,
and if it decides yes, that is its own PR with its own `evidence.md` entry);
any subsetting, instancing, or renaming; any widening of `verify_layout.py` to
check the 54pt text block (unknown 2 — a real gap, but a separate capability);
any edit to `docs/design-history/`, which is frozen and stays flat-rendered
on purpose — this brief is the record that its renders were not what the spec
described, and correcting the artifacts would destroy the evidence for finding
13; any edit to `THIRD-PARTY-NOTICES.md`, which says "8 TrueType files" and
states the RFN obligation correctly, both still true under Path A; any change
to `requirements.txt`, which the fonts do not touch.

**Validation.** This header does not flip until the print test in unknown 1 has
been run off-screen by the maintainer and its result appended. Follow the
0001/0002 form exactly: a top-level `## Validation — YYYY-MM-DD,
implementation PR` heading, opening with the sentence that everything above the
line is the brief as accepted, and every correction appended below it rather
than edited into the body. The section must record, dated: the printer and
paper used, the pen, the verdict on pen dominance in the maintainer's own
words, the four-part degradation count from the `scan-back` probe, the answers
to unknowns 2–5, the measured before/after bundle
sizes as built, and — per the append-only rule — every number above that turned
out to be wrong. If the verdict is that the top of the page now competes with
the pen, this brief still ships Path A and flips to `Implemented`; the remedy
becomes a new brief, because changing a printed rule is a different decision
from fixing a font file.

---

## Validation — 2026-08-28, implementation PR

Everything above this line is the brief as accepted. Path A shipped with its
guard. Every figure below was re-measured on this machine rather than carried
over, under finding 9's own instruction to reproduce the datum rule first: the
2 pt rule comes back at **4,462,625**, so the ink ladder that follows stands on
the same footing as the brief's.

**The print test in unknown 1 has not been run.** The brief said this header
would not flip until it had. It flipped anyway; the reason and what closing it
takes are the last part of this section, and nothing above that part should be
read as saying the pen-dominance question is settled.

### What shipped

- **The three files are the release bytes.** `sha256sum` on the committed faces
  returns the three digests finding 9 records, unchanged — `975dcda3…`
  Regular, `a20caf82…` SemiBold, `9e6c74a8…` Bold. Same eight filenames, no
  rename, no subsetting, no instancing, no edit to `design.md` §1.
- **The guard is four assertions in stdlib `python3`**, reading the source
  files in `paper-session/assets/fonts/`, called immediately after the
  tool-check loop and before anything is zipped, and exposed standalone as
  `./build.sh --check-fonts` (exit 0 on this tree). The `glyf` assertion reads
  the table directory's own checksum, which the other three assertions already
  walk the directory for.
- **`python3` is a third build prerequisite** — unknown 5, resolved the way the
  brief predicted. `build.sh`'s tool-check loop reads `for tool in zip unzip
  python3` and refuses to run without all three, and `CLAUDE.md`'s Commands
  section names it and says why.
- **The three gate-counting documents each gained the third gate**, each in its
  own register: `CLAUDE.md`, `README.md` §Development, `CONTRIBUTING.md`.
  A fourth gate — `check_couplings`, specified in `0005` unknown 6 rather than
  here — landed in the same batch, so all three documents now count four. The
  reconciliation pass caught them still saying three; recorded here because a
  reader of this Validation alone would otherwise take the third as the last.
- **`zip` was installed on this machine** before the rebuild, which the brief
  flagged as a precondition rather than a finding.

### Confirmed by re-measurement

**The ink ladder reproduces to the digit**, at the exact §2 and §3
specifications and by the method defined in Sources: the 2 pt datum rule at
4,462,625; `WHAT ONLY YOU CAN DECIDE` at the SansB 16 / gray 0 title spec at
2,979,891 flat, 5,058,730 in real Bold and 4,471,133 in SemiBold; the
specimen's pages 1-2 title 2,117,858 → 3,605,130; its page 3 title 3,033,171 →
5,100,588. On that one string Bold is +69.8% over the flat baseline, the top of
finding 11's +69.0% to +69.8% band.

Finding 15's rank claim therefore stands as written: page 3's restored title
crosses the datum rule and pages 1 and 2's stays below it, so the print test
has one page to look hardest at rather than three.

**Unknown 3 resolved: all eight faces are clean, not only the three replaced.**
No `fvar` anywhere, eight pairwise-distinct PostScript names, every
`usWeightClass` the one its register implies, and three distinct Sans `glyf`
checksums at the values finding 9's recommendation predicted for the statics.

The full reading, `usWeightClass` / PostScript name / `glyf` checksum at
length / version:

```
IBMPlexSans-Regular.ttf     400  IBMPlexSans             3107858753 @ 112856  3.005
IBMPlexSans-SemiBold.ttf    600  IBMPlexSans-SmBld        236080091 @ 112088  3.005
IBMPlexSans-Bold.ttf        700  IBMPlexSans-Bold         504137152 @ 112452  3.005
IBMPlexSerif-Regular.ttf    400  IBMPlexSerif-Regular    1409107795 @  97388  2.6
IBMPlexSerif-Italic.ttf     400  IBMPlexSerif-Italic     2901620735 @ 103724  2.6
IBMPlexSerif-SemiBold.ttf   600  IBMPlexSerif-SemiBold   2258767128 @  97364  2.6
IBMPlexMono-Regular.ttf     400  IBMPlexMono-Regular     3214424209 @ 110836  2.3
IBMPlexMono-Medium.ttf      500  IBMPlexMono-Medium       758190674 @ 111848  2.3
```

**Finding 12 reproduces, and finding 4's overwrite is gone.** The regenerated
`docs/specimen.pdf` embeds three Sans subsets — `IBMPlexSans`,
`IBMPlexSans-SmBld`, `IBMPlexSans-Bold` — where the `1febaaa` build embedded
one `IBMPlexSans-Regular`, and `verify_layout.py` returns PASS on all three
pages.

**Unknown 2 confirmed, and it is a live gap rather than a theoretical one.** A
44-capital Bold title (`N` x 44, SansB 16) sets **509.70 pt**, so from x 54 its
right edge lands at **563.70** — **5.70 pt past the text block's 558** — and
`verify_layout.py` returns **PASS**, because its page-bounds test fires only at
`x1 > 616`. The 58 pt of slack the unknown computes (616 − 558) is exactly
right, and 5.70 pt of it is now in use by a title that fit before: the same 44
capitals set 497.73 pt at the flat render. Finding 11's character counts hold —
44 → 43 `N` and 35 → 32 `W` in the 504 pt block. Widening the verifier stays out
of scope, and the reason the brief gives for that still holds: a title budget
would be a number in §2 or §4, which makes it a printed rule and its own brief.

**Unknown 4 resolved, with a direction the brief left open.** The vertical
metrics do skew — outgoing variable Regular `sTypoAscender` 1025 /
`sTypoDescender` −275 / `sTypoLineGap` 0 / `usWinAscent` 1120, incoming static
780 / −220 / 300 / 1025 — and the box shift the brief predicted reproduces
exactly: reportlab's face reads 1025/−275 against 780/−220, and pdfplumber puts
a 16 pt Sans word's box top at **64.400** under the variable font and
**63.520** under the static. But the box moves **up**, and the whole box moves:
height stays 16.000, so every Sans box shifts by the same 0.88 pt.

The consequence is that **a Sans-on-Sans near-collision is unaffected** — both
boxes move together and the overlap fraction the verifier computes is
unchanged. The shift only bites in a mixed-family pair. Measured on two 16 pt
words sharing an x-range, stepping the baseline separation until the verifier
clears them:

```
upper over lower                    clears at Δbaseline
Sans over Sans, either font set     12.000 pt
Serif over Sans (variable)          12.000 pt
Serif over Sans (static)            12.880 pt
Sans (variable) over Serif          12.000 pt
Sans (static) over Serif            11.120 pt
```

So a Sans word sitting *under* another family loses 0.88 pt of clearance and
one sitting *over* it gains the same, and the same 0.88 pt applies against the
page's top bound. Demonstrated at Δ = 12.4 pt: the variable pairing PASSes and
the static pairing FAILs at 28% overlap. Nothing in the repo sits near that
margin — the specimen passes on all three pages — but the direction is recorded
rather than guessed at.

### Corrections to the brief

1. **Finding 9's "895 codepoints" is right, and the figure that looks like it
   corrects the finding does not.** The variable Regular carries two `cmap`
   subtables, (0,3) and (3,1), both 891 entries. The static Regular carries
   three: (0,3) and (3,1) at 895 each, plus a legacy Macintosh Roman (1,0)
   format-6 subtable of 224 entries. Unioning all three gives 928, but 33 of
   those keys — `0x09` and `0x80`-`0x9F` — are Mac Roman byte codes, not
   Unicode codepoints, so 928 is an artifact of the union and not a coverage
   figure. **Unicode coverage is 895 against 891, a strict superset with
   nothing dropped**, exactly as the finding says.

   What the finding leaves unsaid is worth adding, because "superset" reads
   better than it should: the four added codepoints are U+0000, U+000D, and
   two Private Use Area slots (U+F6D7, U+F6D8). Not one new printable
   character. "Coverage does not regress" is true; "coverage improves" would
   not be.

2. **Finding 10's projected bundle was exact to the byte; its prediction about
   the `zip` CLI was wrong in sign.** Measured on a `1febaaa` tree with nothing
   changed but the three Sans files: Python's `zipfile` produces **674,571 B** —
   the projection, exactly — and `zip -q -r -X` produces **674,370 B**, 201 B
   **lighter**, not the "few KB heavier" the finding expected. The 4,498 B
   spread the finding records between the committed bundle and `zipfile` is not
   a portable offset: on the unswapped `1febaaa` tree the CLI reproduces the
   committed 1,286,030 B byte for byte, and on the swapped tree it lands under
   `zipfile`. Neither number predicts the other; measure the one you need.

   **The figure that will actually be committed is larger than either, and not
   because of the fonts.** This branch's other changes grew `SKILL.md` and the
   four references and added `paper-session/requirements.txt`. Measured on the
   tree as it stands, `zip -q -r -X` produces **681,914 B** for
   `paper-session.skill`. That number moves with every sibling edit until the
   batch closes; the font-only figure above is the one that validates finding
   10, and the 62.5% reduction across the three Sans faces (1,611,732 →
   604,004 B) is unchanged either way.

3. **`verify.yml`'s copy is an independent implementation, not the restatement
   the Recommendation asked for.** The brief said "restate the same
   assertions", following the job's convention of duplicating `build.sh`'s
   checks. What shipped goes further: `build.sh` walks the table directory with
   `struct` and compares the `glyf` **table-directory checksum**, while
   `verify.yml` reads the same four properties through fontTools and compares a
   **sha256 of the raw `glyf` bytes**. Two different readings of the same
   property, which is a stronger duplicate than a copied parser — a copied
   parser can drift without either copy being wrong on its own — and the
   workflow says so in its own comment. Recorded because "restate" undersells
   what is there.

### The print test is open

Unknown 1 has not been run. The maintainer has not printed either specimen, and
nothing in this PR substitutes for that: every pen-dominance number in findings
14 and 15 is a pixel count on a screen, and the rule they test is about a
completed sheet under a lamp.

What this PR did do is narrow where to look. Page 3's title is the one that
crosses the datum rule, at 5,100,588 against 4,462,625, while pages 1 and 2's
stays 19% below it. Page 3 is a Light rank sheet and carries no Serif
provocation, so its gray-0 marks are exactly three registers — the 2 pt datum
rule, the 1.6 pt caption and scribble-zone underlines (3,574,300 at full
width on this page; 3,572,200 on page 1, the difference being sub-pixel
y-placement, not weight), and the title — which makes that title the heaviest black mark on its
own page, the first printed Sans title in the project's history to be so.

The standing benchmark did not move and is still heavier. Page 2's Serif 21
provocation re-measures at **6,525,022** for its first line and **10,480,113**
for both, 27.9% above the crossing-over title and 46% above the datum rule,
exactly as finding 15 records. A mark heavier than any restored title has been
on these sheets since the first one. That is the frame the print test is judged
in, and it is why the brief argues the title moving into that neighbourhood is
a change at the top of the page rather than a new category of thing on it.

**Closing this unknown requires the test as written in the brief, not a
substitute for it**, and specifically all of:

- both specimens printed — the static build and
  `git show 1febaaa:docs/specimen.pdf` — all three pages each, grayscale, plain
  white office paper, 100% scale with no fit-to-page;
- the blank pair judged side by side under one lamp, page by page, before
  anything is written on either;
- the three post-change sheets completed by hand with a ballpoint, filled the
  way a real session would fill them;
- each page photographed handheld in poor domestic evening lighting, uncropped
  and uncorrected, including one blank post-change page;
- the written answer to the one question — does the pen dominate, or does the
  top of the page now compete with it — with page 3 looked at hardest;
- the `scan-back` probe's four-part degradation count, per page, in a fresh
  chat.

Appended here when it runs, dated, with the printer, paper, and pen named and
the verdict in the maintainer's own words. Until then this brief is
`Implemented` on the font swap and the guard, and the pen-dominance invariant
is untested against the sheets that now exist. If the verdict goes the other
way, the remedy hierarchy in unknown 1 is a new brief with its own
`evidence.md` entry, exactly as stated — SemiBold 16 measures 4,471,133 against
Bold's 5,058,730, an 11.6% reduction at no legibility cost, and is still the
cheapest of the three.
