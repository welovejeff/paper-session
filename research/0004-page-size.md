Status: Draft
Date: 2026-08-28
Outcome: —

# Page size: parameterizing the design system off the page box

## Scope

Whether and how the design system should stop being written against US Letter
in particular. The question is narrow: `references/design.md` fixes the page at
612 x 792 pt in §0 and derives absolute coordinates from it in §4 and §6, and
most of the world prints A4. This brief establishes what actually goes wrong on
A4 today, decides where the page box enters the spec, and specifies the
verifier change that must ship with it. It decides no printed rule on its own
authority. It touches two — the legibility floors (finding 3) and the sourced
slot counts the "what gives" ordering leans on — and for each it says so and
names what `evidence.md` owes.

## Sources

- Local files, read and measured for this brief:
  `paper-session/references/design.md` (§0 lines 7 and 12, §2 line 45, §3
  line 62, §4 lines 76-83, §5 lines 90 and 154, §6 lines 95-102, §9 line 151),
  `paper-session/SKILL.md` lines 74-75 and 130,
  `paper-session/scripts/verify_layout.py`, `.github/workflows/verify.yml`
  lines 115-116, `docs/specimen.py`, `docs/specimen.pdf`,
  `docs/design-history/hybrid-specimen.pdf`,
  `paper-session/references/page-patterns.md` (§Named session formats,
  lines 91-105, and the long list at line 39), `scan-back/SKILL.md`,
  `README.md` lines 190 and 337, `CONTRIBUTING.md` lines 67 and 185-187,
  `CHANGELOG.md` line 104, `research/0002` and `research/0006`.
- Measurements taken for this brief: `docs/specimen.pdf` and
  `docs/design-history/hybrid-specimen.pdf` inspected with pdfplumber (word and
  graphic bounding boxes on every page); the bundled IBM Plex faces read with
  fontTools for `unitsPerEm`, `sxHeight`, and `sCapHeight`; page-box constants
  taken from `reportlab.lib.pagesizes`; the margin check specified below
  prototyped and run against both PDFs.
- `paper-session/references/evidence.md` line 213 (the legibility floors
  passage) and line 207 (the slot-count passage) for the two places this
  touches printed matter.

## Findings

1. **A4 users are degraded, not blocked, and nothing clips.** A4 is
   595.2756 x 841.8898 pt: 16.7244 pt narrower and 49.8898 pt taller than
   Letter. Content on a Letter sheet lives between x 54 and x 558 — measured,
   not assumed: on all three pages of `docs/specimen.pdf` every extracted word
   falls inside x 54.00-558.00, and the graphic *extent* is exactly
   54.00-558.00. Only two objects per page span the full width — the datum rule
   and the open-territory rule; page 1 carries 20 line objects, page 3 carries
   34 (10 lines, 8 rects, 16 curves), and the rest are shorter. The extent is
   what the margin argument needs. Printed at
   actual size and centred on A4, that block lands at x 45.64-549.64, clear of
   both the paper edge and any consumer printer's unprintable border. The
   54 pt margin absorbs the width difference exactly as suspected. Nothing is
   lost to clipping.

2. **The real harm is fit-to-page scaling.** Browsers and print dialogs
   default to fitting an oversized page, and the fit factor here is
   min(595.2756/612, 841.8898/792) = **0.972673**. Every point size on the
   sheet is multiplied by that. Where the dialog fits to the *printable* area
   rather than the media box — common, and the usual browser default — the
   factor is worse: a typical A4 printable width of about 576 pt gives 0.9412.
   So the shipped sheet reaches an A4 user somewhere between 94% and 97.3% of
   its designed size, with no warning and no way for the user to notice.

3. **The smallest type has no headroom to spend.** IBM Plex, read from the
   bundled files — three families in eight faces — has cap height 0.698 em in
   every one of them and x-height 0.516 em in seven of them;
   `IBMPlexSerif-SemiBold.ttf` alone reports 0.522. The ink key is Sans 6 caps
   (§5 line 154), so the arithmetic below runs on the uniform cap height and on
   Sans's 0.516 x-height, and the Serif outlier does not reach it. At the
   40 cm convention
   `evidence.md` uses, its cap height subtends 0.2116° — against the 0.2°
   critical-print-size floor that passage cites, that is 5.8% of headroom. The
   media-box fit leaves 0.2058° (2.9% headroom); the printable-area fit leaves
   0.1992°, below the floor. Measured strictly, on x-height rather than caps,
   6 pt is *already* under the floor on Letter (0.1564°) and the
   Arditi & Cho all-caps finding in the same passage is what licenses it. The
   honest statement is not "A4 breaks legibility" but "the smallest type has
   roughly zero margin by design, A4 scaling consumes what there is, and the
   system currently has no rule that notices." This is the one place the brief
   touches printed matter; see the Recommendation for what `evidence.md` owes.

4. **The hardcoded coordinates, enumerated.** In §0, §4 and §6 the following
   are absolute and must become derived from the page box (`PAGE_W`, `PAGE_H`)
   and the margin (`M`):

   - §0 line 7 — `612 x 792` itself; `Margins 54pt`. The footer baseline
     `y=30` is deliberately **not** on this list. It is referenced to the
     bottom edge, so a taller page leaves it exactly where it is, and since
     `M` is a system constant (see "The metric-margin question") rewriting it
     as `M - 24` would invent a dependency that can never fire — and would
     drag the footer with the margin on the day someone changes `M` anyway.
     It stays absolute, and the parameterization PR should say so in a comment
     rather than leave the next reader to rediscover it. The same holds for
     the ink key's baseline 42 (§5 line 154, `docs/specimen.py` line 106) and
     for the private marker's baseline 30 (§9 line 151).
   - §0 line 12 — "at least 50% of every page area": the ratio is already
     parameterized, but the page area it divides changes (484,704 pt² Letter,
     501,156 pt² A4).
   - §4 line 76 — `y = 792 - 54 = 738` → `PAGE_H - M`.
   - §4 line 77 — datum rule `x 54 to 558`, `at y 738` → `M` to `PAGE_W - M`,
     at `PAGE_H - M`.
   - §4 lines 78, 79, 80 — three `x 54` origins → `M`. The vertical offsets
     (`-22`, `-36`, `-52`) are typographic and relative to the datum; they
     stay absolute.
   - §4 line 81 — `Body begins at y 738 - 74` → relative to the datum, stays
     absolute once the datum is derived.
   - §6 line 95 (react pair) — "two equal columns, 24 pt gutter" gives 240.0 pt
     columns on Letter and 231.6378 on A4. The 14 pt and 18 pt indents are
     typographic and stay.
   - §6 line 96 (rank row) — the 22x20 pt box, the `x+34` offset and the r8
     circles are typographic; the "~60 pt note guide ending at the right
     margin" is right-margin anchored and therefore already derived, but the
     60 pt is measured against a 504 pt line and must be restated as a
     fraction of the measure or explicitly held.
   - §6 line 97 (provocation block) — "text-width minus 60 pt" is already
     derived: 444.0 Letter, 427.2756 A4. This is the model the rest should
     follow.
   - §6 line 98 (constraint box) — "about 34 pt per line of 12 words at
     Serif 13" assumes a 504 pt measure. On 487.2756 the same 12 words can wrap
     to two lines and the box grows.
   - §6 line 99 (open territory) — "full text width" derived; the 96/108 pt
     minima are absolute and stay.
   - §6 line 100 (card kit) — the 2x4 grid's card width derives from the text
     width; r4 and the dash pattern stay.
   - §6 line 101 (round grid) — **"so each cell is 160 pt wide" is the worst
     one**: (504 - 24)/3 = 160.0 exactly on Letter, 154.4252 on A4. Downstream,
     the dot lattice at 12 pt pitch inset 8 pt fits a Letter cell exactly
     (144 pt usable, 12 intervals, 13 dots, zero slack) and leaves 6.4252 pt
     of slack in an A4 cell. Row height 90, gutter 12, and the 72 pt cell floor
     stay absolute. One further value sits in the same sentence and is easy to
     miss because it is not independent: §6 line 101 names "the **28pt break**
     in the dot rhythm" that marks where one turn ends — the 12 pt gutter plus
     two 8 pt insets. It is the one number in this molecule the design
     justifies by eye. Centring the lattice to absorb A4's slack (unknown 5's
     expected answer) makes the effective inset 11.2126 and the break
     34.4252 pt. So the break must be re-derived as `gutter + 2 x inset` and
     the "28pt" literal removed, or the centring rejected; it cannot be left
     standing as a literal beside a variable cell.
   - §6 line 102 (hand box) — **`ending at x 480`** and **"a writing guide from
     x 486 to the right margin at x 558"**: three absolutes, cleanly derived as
     `RIGHT - 78`, `RIGHT - 72`, `RIGHT`.

   Two coordinates outside the named sections carry the same dependency and
   must be swept in the same pass: §5 line 90 (footer baseline `y 30`) and §9
   line 151 (the private marker, same baseline).

5. **`verify_layout.py` is already page-size agnostic — correction one.** The
   bounds check at lines 90-91 tests against `page.width` and `page.height`;
   there is no Letter constant anywhere in the file. A natively-A4 sheet passes
   the mandatory gate today with no change to the verifier. The parameterization
   PR does not have to teach the verifier about A4.

6. **`verify_layout.py` never checks the margin box — correction two, and the
   dangerous one.** Its only geometric test is "inside the page, with 4 pt of
   forgiveness". A sheet built on Letter coordinates and rendered onto an A4
   media box — the exact half-finished state the parameterization work will
   pass through — puts its right edge 37.28 pt from the paper edge instead of
   54, and its datum rule 103.89 pt from the top instead of 54, and **passes
   the gate silently**. It also never looks at graphics at all, only at text,
   so a rule can wander outside the margin box with no word near it and nothing
   fails. The margin check has to land in the same PR as the parameterization,
   not after it.

7. **The margin box has a third licensed exception that §0 does not name.**
   §0 line 7 says nothing crosses the margin box except the footer and the
   page notes sharing its baseline. Measured in `docs/specimen.pdf`, the ink
   key sits at y 40.35-46.35 from the bottom edge (baseline 42;
   `docs/specimen.py` line 106) — below the 54 pt margin line, and §5 line 154
   only says "above the footer baseline". §0's exception list is incomplete as
   written. A margin check built from §0 alone would fail all three committed
   specimen pages. This is a documentation fix, not a change to what prints.

8. **The Deep ≤ 4 pages interaction runs the other way from the obvious
   guess.** Holding M at 54, A4 costs 16.7244 pt of measure (3.318%) and gains
   49.8898 pt of height (7.294% of the text block). A wrapped provocation line
   costs 28 pt at Serif 21/28; a wrapped ruled answer costs 16 pt. A page would
   have to gain roughly two extra wrapped provocation lines before the extra
   height was spent. The round grid's "drop a row rather than shrink one" rule
   is triggered by *vertical* budget, and A4 improves that budget by 0.489 of a
   row — never enough to drop one, sometimes enough to add one. Furthermore the
   two formats that can reach the cap are page-counted, not flow-counted: the
   serial disclosure kit is exactly four pages by structure (three sittings
   plus the distillation, `page-patterns.md` line 103), and the Grinnell field
   kit states its own cap directly — "up to 4 pages per kit", line 101 —
   reached by the journal plus at most two account pages plus the catalog. A
   one-entity Grinnell kit is three pages, so "zero slack" is true only of the
   maximal kit; in neither format can a change of measure add a page. The
   formats that could inflate by flow are the after-action review (2-3 pages,
   line 91) and the premortem, outside view, teach-back and weekly review
   (2 pages each, lines 93-99): the AAR at its stated maximum sits **one** page
   under the cap and the other four sit two. Brainwriting rounds (line 105)
   never states a page count at all — worth naming, because it is the format
   that owns the round grid, the molecule most sensitive to measure, and
   unknown 1 has to settle it. The collision is real in principle and has no
   instance in the current library. It still needs a deterministic answer, because the cap is an
   invariant and the library will grow — see the Recommendation.

9. **One side effect worth naming rather than fixing.** The serial disclosure
   kit's ruled page is the dose, and `page-patterns.md` forbids shrinking it.
   A4's extra 49.8898 pt is about three more ruled lines at 16 pt leading, so
   the A4 dose is slightly *larger*. Growing the dose is not what that rule
   guards against, and no adjustment is warranted; the brief records it so a
   later reader does not read it as a violation.

10. **Page size is stated in five other places besides `design.md`.**
    `paper-session/SKILL.md` line 74 ("**8.5 x 11 inch (US Letter),
    portrait**") — and line **75**, a separate bullet, which is where "minimum
    0.75 inch margins" actually lives. `README.md` line 190 ("Hard floors: US
    Letter portrait, 54pt margins"). `CHANGELOG.md` line 104, which sits inside
    the frozen `## [0.1.0] — 2026-07-29` section (heading at line 89): it is
    released history and must not be edited, only added to above, so it belongs
    on this list as a place page size is *recorded*, not a place to sweep.
    `CONTRIBUTING.md` line 67, which today lists "adding A4 support" among the
    changes that need no citation and "just open the PR" — a line this brief's
    own existence makes stale. And the two places that advertise A4 as a wanted
    contribution (`README.md` line 337, `CONTRIBUTING.md` lines 185-187, which
    also states the premise this brief corrects: "every measurement is in
    points off a 612x792 page"). The one-way dependency in `CLAUDE.md` means
    SKILL.md's two lines are condensed restatements of `design.md` §0 and must
    move with it.

11. **The margin check turns CI red, and the brief has to say how it doesn't.**
    `.github/workflows/verify.yml` lines 115-116 run
    `verify_layout.py docs/design-history/hybrid-specimen.pdf` and assert it
    passes. The margin check specified below was prototyped and run against
    both committed PDFs. `docs/specimen.pdf` passes on all three pages, which
    confirms the calibration claim at the end of that section. The history
    specimen **fails six times**: its page note runs to x 572.40 on pages 1-2
    and x 573.60 on page 3, past the 558 right margin, on the footer baseline.
    `CLAUDE.md` freezes `docs/design-history/`, so the PDF cannot be fixed and
    the CI step cannot simply be re-run. Three resolutions exist — make the
    margin check opt-in behind a flag (which weakens the mandatory gate and
    reopens finding 6), exempt the history specimen in the workflow, or drop
    that CI step. The Recommendation picks one; the point of the finding is
    that a PR shipping the margin check without picking one is a red build.

12. **`scan-back` is untouched — checked, not assumed.** `scan-back/SKILL.md`
    was read for page-box dependencies and has none: it reads marks, ink, zone
    adjacency and the printed header, and never a coordinate, a page
    dimension, or a paper name. Its "margin notes" are the human's marginalia,
    not the margin box. So the pen protocol's two-file coupling and the
    setup-card coupling both survive this change unchanged, and no `scan-back`
    edit belongs in the implementation PR. In this repo that has to be stated
    rather than left for a reviewer to verify.

## Options

**A. Parameterize `design.md` §0/§4/§6 by page box, in that one file.**
Recommended. One page-box block at the top of §0; every absolute in §4 and §6
re-derived from it. No second document.

**B. A parallel A4 spec, an addendum section, or a `references/a4.md`.**
Rejected on the repo's own rules, not on taste. `CLAUDE.md` forbids duplicate
copies of a reference doc anywhere in the tree — that rule exists because the
loose root copies of the references drifted from the bundled ones — and
`design.md` is the single source of visual truth. A parallel spec would also
require every future rule to be written twice, which is the failure the pen
protocol's two-file coupling already demonstrates is expensive.

**C. Do nothing; tell A4 users to print at 100%.** Rejected. It relies on the
user knowing there is something to correct, and finding 2's harm is invisible
by construction. It also leaves A4 output with 25 pt of dead space at the head
and foot from centring, which the design's decompress-downward rule
specifically does not want at the top.

**D. Keep the 504 pt content block exactly as it is and emit it on an A4 media
box, horizontally centred and top-aligned at `PAGE_H - 54`.** This is the real
alternative to A and the one that has to be argued rather than waved at,
because on the brief's own terms it looks better than A almost everywhere. The
sheet is natively A4, so no dialog scales it and finding 2's harm — the entire
measured harm in this brief — never fires. It spends none of what this brief
itself calls the scarce dimension on A4: measure stays 504, react-pair columns
stay 240, round-grid cells stay 160 with zero lattice slack, the constraint
box's "12 words at 34 pt" stays true, and the hand box's x 480/486/558 stay
literal. Unknowns 1, 5 and 6 all dissolve, unknown 2 is satisfied by
construction, and the extra height falls at the foot, which is the direction
§0 line 11 already decompresses. The brief's own metric-margin argument is the
sharpest case for it: if 22.11 pt of lost measure is too much to pay for a
rounder margin number, then 16.72 pt is a lot to pay for a symmetric one.

Rejected anyway, on three grounds that are about the system rather than this
one page box:

- It does not generalize, and the brief's stated plan (below) is that a third
  named box is a one-line change. Option D has no answer for A5, where a 504 pt
  block is wider than the 419.5 pt sheet, and on Legal it would leave a 270 pt
  bottom margin. Option A degrades gracefully into a measured refusal; option D
  simply has no definition off A4.
- It breaks the page's vertical close. The block's foot lands at y 103.89 while
  the footer stays bottom-referenced at y 30, leaving a 74 pt band of nothing
  between the open-territory rule and the footer — and §6 line 99 makes open
  territory "always the last element before the footer". Either the footer
  floats up with the block, which contradicts finding 4's reason for leaving
  y 30 absolute, or the sheet ends in an orphan band.
- It forfeits the one thing A4 gives for free. Finding 8's arithmetic says the
  49.8898 pt of extra height is worth about half a round-grid row and is the
  side of the trade that helps; option D converts all of it into bottom margin.

And the asymmetry is not only cosmetic: §0 line 7 makes "Margins 54pt all
sides" a non-negotiable of the system, and a sheet with 45.64 pt of side margin
against 54 pt of head margin reads to a printer as a mistake rather than a
choice. That is a weaker argument than the three above and is listed last on
purpose.

### The metric-margin question

**54 pt stays 54 pt on every page box.** The margin is a constant of the design
system, not a function of the paper. Four reasons:

- 54 pt is 19.0500 mm — within 0.05 mm of a perfectly conventional 19 mm metric
  margin. The "not a round number" objection is cosmetic and nearly already
  satisfied.
- A 20 mm margin is 56.6929 pt and would cut the A4 measure to 481.8898 pt.
  That is 22.11 pt narrower than Letter instead of 16.72 — **32% more measure
  lost**, paid for nothing but a rounder number, and measure is the scarce
  dimension on A4.
- Holding M constant makes the whole delta a single pair of numbers a
  reader can carry: A4 is 16.7244 narrower and 49.8898 taller. A metric margin
  makes every derived quantity differ by page box for two reasons at once.
- `SKILL.md` line 74 already states the margin in inches ("minimum 0.75 inch").
  One constant keeps one number in both documents.

So `M = 54` is a system constant; `PAGE_W` and `PAGE_H` are the only inputs.

### The specimen

**The committed specimen stays Letter-only.** `docs/specimen.pdf` and the three
`docs/sheet-*.png` do not gain A4 siblings: at 1000 px on the long side a 3.3%
difference in measure carries no information a reader can see, and two
committed artifacts from one generator is the drift this repo has already been
bitten by once. Instead `docs/specimen.py` takes a `--page-box {letter,a4}`
flag, and its default run builds Letter (committed, PNG-rendered) and then
builds an A4 copy to a temporary path solely to push it through the verifier.
The A4 build is a gate, not an artifact.

The Letter output must not change. That is the strongest available check on the
parameterization, and it is the acceptance test: dump every word bbox and every
graphic bbox from `docs/specimen.pdf` before and after, sorted, and `diff` must
be empty. `docs/sheet-*.png` should then need no regeneration at all.

### When the cap and the measure collide

The Deep ≤ 4 pages cap is an invariant and wins outright. What gives, in order,
when a narrower measure would push a kit past it:

1. Optional furniture goes first — the rotated gutter hint, the Light house
   rule, an optional corner tick.
2. Then the count of machine-contributed items in a react pair or rank stack
   drops — **but never below a sourced floor.** This is the brief's second
   touch on printed matter, and it does not get a free pass. Slot counts are
   evidence-backed in this system, not slack: `evidence.md` line 207 grounds
   "the long-list pattern and its uncomfortable slot counts" on Keusch 2014 and
   Meitinger 2024 (many small numbered slots beat one large box), the long list
   at `page-patterns.md` line 39 sets ten to fourteen, and the premortem's six
   to eight (line 93) is a *deliberate, sourced exception* to that rule, not
   headroom. A react pair pairs one human slot to each machine item, so
   dropping machine items drops human slots in lockstep. So: item 2 applies
   only where a format's item count is a design convenience with no stated
   source, it may never take a count below a floor a format or the library
   states, and where the count is sourced the pressure passes straight to
   item 3. `evidence.md` owes a sentence saying so, in the slot-count
   passage's register — see the Recommendation.
3. Then a row of the round grid drops, per the rule §6 line 101 already states.
4. Never the open-territory minima (96/108 pt), never the ≥50% pen floor, never
   a type size, never the margin.

Items 1, 3 and 4 are derived entirely from the non-negotiables already in §0
and §3 and need no new source. Item 2 is the exception, and it is scoped and
sourced above rather than asserted. Rule 4 is the one that matters: the
tempting fix under page pressure is to shave a point off the smallest type, and
finding 3 shows there is nothing there to shave.

### How a sheet gets to be A4

Reactive only, following the precedent `research/0002` set for the no-printer
path: Letter is the default; the user saying "A4", "European paper", "my
printer is A4" or any equivalent switches it, and the skill offers **once** to
remember it. Never asked proactively — a paper-size question spends the user's
attention at exactly the moment the skill exists to stop spending it. Nothing
about the page box prints on the sheet, and no "print at 100%" instruction is
added to the furniture: a natively-A4 sheet has nothing to scale. Discovery is
the weak point of this choice and is flagged below.

The parameterization admits any (width, height), but the skill offers exactly
two named boxes, Letter and A4, because each named box is one more build the
specimen gate has to verify. A third (Legal, A5, B5) is then a one-line change
plus a verify run. A5 in particular will not work at 54 pt margins — its
419.5 pt width leaves a 311.5276 pt measure and 143.7638 pt react-pair columns — so
the parameterization needs a minimum-text-width guard that refuses to generate
rather than shrink type. This brief does not set that threshold; measuring it
is in the test plan.

## The verifier change, specified

Extend `paper-session/scripts/verify_layout.py` with a margin-box check.
Constants:

```
MARGIN     = 54     # design.md §0; overridable with --margin
MARGIN_PAD = 1.25   # half the heaviest rule (the 2pt datum) plus a hair
FOOTER_TOP = MARGIN # the licensed band runs from 18pt to the bottom margin
FOOTER_BOT = 18
```

Per page, over every extracted word **and** every object in
`page.lines + page.rects + page.curves`:

- Convert to bottom-origin: `y_bottom = page.height - obj["bottom"]`,
  `y_top = page.height - obj["top"]`.
- For **every stroked object** — lines, curves and rects alike; the rank box
  (§6 line 96) is a stroked rect sitting at x0 = 54 exactly — inflate the box
  by `obj.get("linewidth", 0) / 2` on all four sides. pdfplumber reports a
  stroked horizontal rule as a zero-height bbox on its centreline, so the 2 pt
  datum rule's 1 pt of bleed past y = `PAGE_H - M` is otherwise invisible to
  the check. The inflation is what makes `MARGIN_PAD` necessary rather than
  redundant: it does not absorb the datum's bleed, it *exposes* it, and the pad
  is then what licenses it. Prototyped, the two settings are not independent —
  with the inflation on and `MARGIN_PAD = 0`, `docs/specimen.pdf` fails 31
  times; at 0.5 it fails 7; at 1.0 (exactly half the heaviest rule) it passes,
  and 1.25 is that value plus the hair the comment claims. Inflating rects as
  well changes nothing on the committed specimen and is the right rule anyway.
- Fail unless `x0 >= MARGIN - PAD`, `x1 <= page.width - MARGIN + PAD`,
  `y_bottom >= MARGIN - PAD`, and `y_top <= page.height - MARGIN + PAD`.
- Except: an object lying entirely inside the footer band
  (`y_top <= FOOTER_TOP + PAD` and `y_bottom >= FOOTER_BOT - PAD`) and inside
  the horizontal margins is licensed. That band covers all three things §0
  should be naming — the scan-it-back line and the private marker at
  baseline 30, the page note on the same baseline, and the ink key at
  baseline 42 (measured extent 40.35-46.35; the footer line and page note
  measure 28.13-34.93, so `FOOTER_BOT = 18` is not tight).
- Report in the existing register: `p{n}: outside margin box: '<text>' at
  (x0, y)`, collected into the same `problems` list, same exit-1 behaviour.
  Graphics carry no text, so name the object kind in that slot instead
  (`line`, `rect`, `curve`) and print the inflated box, not the raw one — the
  raw coordinates of a failing rule look legal and cost the reader a minute.

`--margin` must default to 54 and must not be inferred from the content. A
sheet that is uniformly misplaced would infer its own bad margin and pass,
which is precisely the failure in finding 6.

The check must be calibrated against the committed specimen before anything
else, and the reason is the inflation rather than the coordinates: every page
sits exactly on x 54.00 and x 558.00, which a bare `>= 54` test passes, but
once each stroked object is inflated by half its own weight the datum rule
reads 53.00-559.00 and 737.00-739.00 and fails on all four sides. Prototyped
against `docs/specimen.pdf`, the check as specified passes all three pages.
Against `docs/design-history/hybrid-specimen.pdf` it fails six times — see
finding 11, which is the CI problem this creates and how the Recommendation
resolves it.

## Risks / unknowns to validate

This list is the implementation PR's test plan.

1. **A page budget per named format, computed at both page boxes.** The
   flagged unknown, and it has to be scoped to something a single PR can
   actually run. There is no kit generator in this repo to re-run:
   `paper-session/scripts/` holds only `verify_layout.py`, `docs/specimen.py`
   builds three pages of molecules rather than any named format, and
   `SKILL.md` Step 4 has the model write reportlab per session from
   `design.md`. "Regenerate every kit" would mean authoring eight generators
   first, which is more than one PR and would make the flagged unknown the
   largest thing in it. So the test is arithmetic instead, and it discriminates
   the same claim: for each of the eight named formats in `page-patterns.md`
   §Named session formats — after-action review, premortem, outside view,
   teach-back, weekly review, Grinnell field kit, serial disclosure kit,
   brainwriting rounds — take the format's stated structure zone by zone, cost
   each zone in vertical points at both measures from the §2 and §3 numbers
   (Serif 21/28 for a provocation line, 16 pt leading for a writing guide, the
   §6 molecule dimensions, the 108 pt open-territory minimum), and read off the
   page count. Finding 8 predicts no format gains a page and none loses a
   round-grid row. Any format that does gain one falsifies finding 8, and the
   "what gives" ordering above becomes live rather than precautionary. Two
   things fall out of the same arithmetic and must be recorded with it: **the
   pen fraction at both boxes** for every format, against the ≥50% floor of §0
   line 12 — the floor is measured against a page area that grows 3.39% while
   the measure shrinks 3.32%, and §6 line 101 says explicitly that the round
   grid and the open-territory band "together are what carry this sheet past
   the half-page pen floor", so the brainwriting sheet is the one to check
   first — and **brainwriting rounds' page count**, which the format never
   states (finding 8). Record every number in the Validation section, including
   the ones that matched. Building one real generator for the brainwriting
   sheet, the worst case on both counts, is worth it if the arithmetic lands
   near a boundary; eight are not.
2. **The Letter output must be geometrically unchanged.** Run the bbox-dump
   diff described under "The specimen". A non-empty diff means the
   parameterization changed Letter, and the PR does not ship until it is empty.
3. **The margin check's false-positive rate, on the cases the committed
   specimen does not contain.** Running it against `docs/specimen.pdf` is
   necessary and already done (it passes), but it is a weak test: that file
   exercises four of §6's eight molecules — react pair, rank row, provocation
   block, open territory — and none of the calibration cases that actually sit
   on the margin. The ones that do, and that therefore have to be built to be
   checked, are: the hand box (§6 line 102), whose writing guide ends at x 558
   *exactly*; the round grid (§6 line 101), whose outermost dot column centres
   at x 550 and whose r0.55 dots reach 550.55; the card kit's dashed borders;
   the constraint box frame; and the private marker (§9 line 151), which lives
   on the footer baseline and appears in no committed artifact at all. The
   first two live on the brainwriting sheet and the last on a serial disclosure
   page, so this unknown is downstream of whatever unknown 1 builds. Any
   failure on a correct sheet is a calibration bug in `MARGIN_PAD` or in the
   footer band, not a layout bug. Confirm specifically that the ink key, the
   private marker, the page note, the 2 pt datum rule, the hand-box guide and
   the outermost dot column all pass.
4. **The margin check catches the bug it exists for.** Build one deliberately
   broken sheet — Letter constants on an A4 media box — and confirm the
   verifier fails it. Finding 6 says the current verifier passes it; assert
   both halves in the test.
5. **The round grid's dot lattice on a non-integer cell.** A4 leaves 6.4252 pt
   of slack in a 154.4252 pt cell. Decide and test whether the lattice centres
   in the cell (distributing the slack, a no-op on Letter where slack is zero)
   or keeps the 8 pt inset and lets the right edge run wide. Centring is the
   expected answer precisely because it reproduces Letter exactly; confirm that
   it does. Whichever way it goes, it settles a stated §6 value and must be
   recorded as such: centring makes the effective inset 11.2126 and the
   between-cell break 34.4252 pt against the "28pt break" §6 line 101 prints
   today (finding 4). Report the resulting break at both page boxes and say in
   the Validation section whether the dot rhythm still reads as one turn
   ending — that is the only claim the 28 pt was ever making.
6. **The minimum text width, stated in the design's own terms.** The obvious
   method — shrink the measure until `docs/specimen.pdf` stops passing the
   verifier — does not measure what it claims to. `verify_layout.py` fails only
   on collisions and page escape, so the number it yields is a property of that
   file's sample copy: different Mono item strings move it, and a sheet with
   shorter items would "prove" a narrower floor. The guard has to be derived
   from the molecules instead, and stated as the binding constraint each one
   imposes on the measure: the react pair needs a right column wide enough for
   its 18 pt indent plus a usable writing guide, and a left column wide enough
   to set a MonoM 9.2 item without hyphenation; the rank row needs
   22 + 12 + item + K/X circles + the ~60 pt note guide to fit between the
   margins; the round grid needs three cells at or above whatever cell width
   keeps a 12 pt dot pitch from reading as two columns; the provocation block
   needs `measure - 60` to hold a Serif 21 line of ordinary length. Take the
   largest of those, state it as a single `MIN_TEXT_WIDTH` in §0 with the
   molecule that binds it named, and set the refuse-to-generate rule against
   that. Record the losing molecules and their numbers too, so the next page
   box argues with a table rather than a guess. Second, and separate: with no
   shared generator, "a guard that refuses to generate" is prose in `design.md`
   that a model must obey, not code that can enforce it. The honest form is a
   §0 rule plus a `--min-text-width` assertion in `verify_layout.py` that fails
   any sheet whose datum rule is shorter than the floor — that part *is*
   enforceable, and it is what should ship.
7. **The Letter bbox baseline may move underneath unknown 2.**
   `research/0006-static-sans-weights.md` proposes replacing
   `IBMPlexSans-Regular/SemiBold/Bold.ttf`, which are three distinct files that
   nonetheless all carry an `fvar` table, `usWeightClass` 400 and subfamily
   name "Regular" — confirmed here with fontTools. Replacing them moves every
   Sans bounding box in `docs/specimen.pdf`, and unknown 2's acceptance test is
   a byte-identical bbox dump. Whichever of the two briefs ships second has to
   take a fresh baseline *before* it starts, and must not read 0006's font
   change as a parameterization regression. If both are in flight, take the
   baseline after the font swap.
8. **Discovery.** A reactive trigger means an A4 user who never mentions paper
   gets Letter forever and has no way to know. Whether one line in README's
   compatibility ledger is enough, or whether the handover message needs a
   clause, is unresolved here and is a field question — it terminates in a
   person who did or did not find the switch, so it belongs in `evidence.md`
   Part Three (field reports), not in this folder.

## Recommendation

Ship option A in one PR:

- `paper-session/references/design.md` — a page-box block at the top of §0
  (`PAGE_W`, `PAGE_H`, `M = 54`, the two named boxes and their exact
  dimensions, and the `MIN_TEXT_WIDTH` floor unknown 6 sets), then re-derive
  every absolute enumerated in finding 4 across §0, §4, §5, §6 and §9 —
  including §6 line 101's "28pt break", which must become `gutter + 2 x inset`
  rather than a literal. State in a comment why the footer baseline 30, the
  ink-key baseline 42 and the private marker stay absolute (finding 4). Add
  the missing ink-key clause to §0's margin-box exception list (finding 7).
  Add the "what gives" ordering to §7 beside the page cap.
- `paper-session/scripts/verify_layout.py` — the margin check as specified,
  plus `--margin` and the `--min-text-width` assertion of unknown 6. Nothing
  about A4 needs adding to the bounds check (finding 5).
- `.github/workflows/verify.yml` — resolve finding 11 by **exempting the
  history specimen from the margin check only**, not by weakening the gate and
  not by dropping the step: keep line 116's run as the collision-and-escape
  check it has always been, and pass it an explicit `--no-margin-box` (or run
  the margin check as a separate step over `docs/specimen.pdf` and the A4 build
  instead). `docs/design-history/` is frozen by `CLAUDE.md`, the six failures
  are a page note printed before the margin box was a rule, and a frozen
  artifact is exactly the case an exemption is for. Say so in the workflow, in
  one comment, so nobody later "fixes" the PDF.
- `paper-session/SKILL.md` — lines 74 and 75's layout rules condensed from the
  new §0, and the reactive page-box trigger written into Step 4 in the same
  register `research/0002` used for the no-printer trigger. Condense from the
  reference; do not invent the rule here. Follow 0002's precedent all the way:
  it also shipped an anti-pattern line (line 130, "Asking whether the user has
  a printer"), and the page-box trigger needs its twin — "Asking what paper
  size the user has (the page box is reactive only; Letter is the default and
  nothing asks)" — or nothing in the list stops the next editor adding the
  proactive question this brief just refused.
- `scan-back` — no change; checked and stated in finding 12.
- `docs/specimen.py` — `--page-box`, geometry derived rather than literal, and
  the default run's A4 verify pass.
- `paper-session/references/evidence.md` — the brief's two touches on printed
  matter, each appended in its passage's own register.

  First, **one appended paragraph in the legibility passage** (line 213). It
  must state: that fit-to-page scaling multiplies every
  printed size by the fit factor, with the Letter-to-A4 factor of 0.972673 and
  the printable-area case near 0.94; that the 6 pt ink key's cap height
  subtends 0.2116° at the 40 cm convention against the 0.2° critical-print-size
  floor already cited there, i.e. it ships with essentially no headroom; and
  that native generation at the target page box, rather than scaling, is what
  the parameterization buys. It must also carry that file's
  "what this does NOT support" convention explicitly: no study tests these
  labels at these sizes on this artifact; 40 cm is a convention, not a
  measurement of how anyone holds a worksheet; the Arditi & Cho all-caps
  finding licenses the current 6 pt caps and licenses no reduction; and none of
  this supports shrinking any element to win space, which the "what gives"
  ordering forbids in the other direction.

  Second, **one appended sentence in the slot-count passage** (line 207), for
  the "what gives" ordering's item 2. It must say that the slot counts grounded
  there are floors and not slack — that page pressure may reduce an item count
  only where no format or library rule states one, never below the long list's
  ten to fourteen or the premortem's sourced six to eight — and it must carry
  the "what this does NOT support" convention: nothing here measures what
  happens when a slot count is reduced for layout reasons, and no study
  compares a shorter list against a longer one on the same task in this
  artifact.
- `README.md` (line 190's hard-floors line; delete line 337's A4 gap),
  `CONTRIBUTING.md` (lines 185-187, same, **and line 67**, which today files
  "adding A4 support" under changes that need no citation and no brief — it is
  now the opposite of both, and leaving it is how the next contributor skips
  this file), `CHANGELOG.md` (one **new** entry at the top — an A4 user now
  gets a sheet built for their paper; line 104 sits in the frozen 0.1.0 section
  and is not to be edited, per finding 10), and both bundles via `./build.sh`.
  `build.sh` itself needs no change.

Explicitly not built: a second reference doc, an A4 addendum section, or any
parallel spec; a metric margin; a Letter-sized content block on an A4 media box
(option D); a committed A4 specimen or A4 PNGs; a proactive paper-size
question; any printed "print at 100%" instruction, page-box marker,
or other new furniture on the sheet; any change to a type size, gray value,
rule weight, or the 96/108 pt open-territory minima; page boxes beyond Letter
and A4 in this PR; and any relaxation of the Deep ≤ 4 page cap.

---

## Note — 2026-08-28, the unmerged batch

Everything above this line is the brief as written, and the header stays
`Status: Draft`: nothing in this brief has been implemented and nothing in it
has been contradicted by the tree. One fact arrived after it was written, from
the siblings that landed in the same batch. It belongs on **finding 10's**
list — the places page size is stated outside `design.md` — and unknown 7 is
the precedent for recording a cross-brief constraint here rather than editing
the body it bears on.

**`paper-session/SKILL.md` Step 4 now states the page box a third time, and in
more detail than either line finding 10 names.** The "Reportlab mechanics"
paragraph, added by `research/0005`'s implementation and absent at `1febaaa`,
reads in part: *"Build the page with `canvas.Canvas(path, pagesize=letter)`: US
Letter, 612 x 792 pt, every coordinate in points from a **bottom-left** origin,
so y grows upward and the 54 pt margin box is x 54-558, y 54-738."*

That is one sentence carrying four of the constants finding 4 enumerates —
`PAGE_W`, `PAGE_H`, the margin, and both edges of the derived text block — plus
a hardcoded reportlab page-size constant, in the layer `CLAUDE.md` says holds
only condensed restatements. It makes finding 10's count six places rather than
five, and it is the only one of the six that states the margin box in
coordinates.

**Consequence for this brief's landing:** the parameterization pass must take
that sentence with it, in the same PR that re-derives §0. It cannot be left
alone. If `design.md` §0 gains `PAGE_W`/`PAGE_H` and named page boxes while
Step 4 still tells the model to write `pagesize=letter` and place things inside
x 54-558, the skill contradicts its own reference at the exact point where a
sheet is built — worse than the current state, where the two agree and are
merely both Letter-only. The rewrite has to keep what the sentence is for: it
exists because the sheet has to build wherever the skill is installed, so it
needs the concrete mechanics of whichever page box is in play, not a pointer.
Deriving the margin box from the page box in the same sentence is the shape
that satisfies both.

**Two smaller consequences.** Finding 10's line references are all stale after
this batch — `README.md` 190 → 209 and 337 → 363, `CONTRIBUTING.md` 67 → 77 and
185-187 → 195-197, `CHANGELOG.md` 104 → 172 (still inside the frozen `0.1.0`
section, still not to be edited). And unknown 7 resolved itself in the order it
predicted: `research/0006` shipped first, every Sans bounding box in
`docs/specimen.pdf` moved with the static faces, and the specimen was
regenerated. Unknown 2's byte-identical bbox baseline must therefore be taken
against the post-font-swap specimen on this branch, not against `1febaaa`.
