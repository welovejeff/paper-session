# Paper Session: Four Directions for the Website

The site at `site/` was read and judged **super wordy and very canned AI looking**. Four
directions were commissioned against that verdict, on a 2×2: **anchored or free** by
**typography and composition or structure and behaviour**. Anchored stays inside the sheet's
law (IBM Plex, grayscale, three voices unblended). Free may leave it and has to say what
leaving buys.

Each direction is two working HTML pages and a written argument, in
`site/design/<slug>/`. Each was critiqued and revised before it got here, so none of them is
arguing from a defect you can point at. Every direction chose **Install** or **the return
trip** as its interior page rather than an easy win, because the compatibility ledger is the
site's hardest content and its most credible sentence.

The deliverable is `site-directions.pdf` — fifteen Letter pages, built by
`build_directions_pdf.py`, verified by `paper-session/scripts/verify_layout.py`.

## 1. A — Anchored × typography and composition · *The apparatus talks*

**Stance.** The site does not have a typeface problem or a copy problem. It has no grid and
no apparatus, so its labels grew into sentences. Restore a datum you can point at and a
named furniture set, and half the prose deletes itself.

**Atoms.** Five declared type steps and nothing off-scale; rule ladder 5 / 3 / 1px, holding
the print relationship 2 / 1.6 / 0.5pt rather than its arithmetic; zero chroma anywhere,
including the focus ring.
**Molecules.** Rail, hairline, body — one continuous vertical datum running the page, every
band a rail label beside one object.
**Organisms.** A 154px serif question against the datum; three evidence figures with `Held
steady` set where a numeral should be; `Fig. 1`, a complete Deep sheet in live HTML off the
print spec's own numbers carrying the committed specimen verbatim; six absences as a spec
table; a ledger closing on `ROWS VERIFIED END TO END 1 / 5` and `OUTSIDE SESSION REPORTS ON
FILE 0`.
**Templates.** Masthead → datum → bands → open territory → footer sitemap and colophon.
`PRINTED. GO THINK.` on the landing page only, because the interior has printed nothing.

**Weakest where:** it is Bureau at nearly 100% with no Basement voice, and every effect it
owns is scale against a datum, which a phone takes away. It also keeps a second, ungated copy
of the print spec in CSS: `CLAUDE.md` forbids duplicate copies of a reference doc and
`build.sh` fails on coupling drift, and nothing watches the website. `Fig. 1` had already
drifted in three places before it shipped.

## 2. B — Anchored × structure and behaviour · *Six rows and an end*

**Stance.** A website for a product whose success is you closing the tab has to be finite,
addressable, and visibly over. Every page is one bounded screen with a datum rule at the
top, a closing rule at the bottom, a folio under it, and nothing after that.

**Atoms.** Four type sizes with a deliberate hole where a lead paragraph would get written;
rules 4 / 2 / 1px; no accent hue defined, so the focus ring is ink.
**Molecules.** The band (12.5rem tracked-caps rail, full-height hairline, content); the index
row (mono numeral, serif statement, caps destination, whole row a link); the status cell, a
word in a 1px box, never a tick and never behind a disclosure widget.
**Organisms.** The index: six numbered first-person preconditions that are the table of
contents and the router at once, 122 words on one screen. The two-track install grid, where
the rule that neither track may be favoured is enforced by column width. The ledger, closing
on a 5rem `1` beside `OF FIVE ROWS CARRIED A PAGE ALL THE WAY ROUND`.
**Templates.** `min-height: 100dvh` sheets, folioed `Sheet 1 of 2`, `Sheet 2 of 2 · END`. One
behaviour: the running head reports which sheet holds the viewport.

**Weakest where:** the door routes and does not argue. `d = 0.93`, `58%` and *confidence held
steady* all sit behind row 06. It demotes the ≥50%-for-the-pen law to deference rather than
acreage, which is a real reading of the rule and still a demotion. Its folio publishes six
pages when five do not exist, so it cannot ship half-built. And `evidence.md` has no home
under a chassis whose whole claim is that pages end.

## 3. C — Free × typography and composition · *The site supplies the pen*

**Stance.** The sheet is grayscale so the pen can be the loudest thing on it, and no reader
will ever put a pen on a website. So the site supplies the pen: every colour on it is ink,
and the site's own opinions are spoken only as margin notes in the sheet's own protocol,
where they physically cannot grow.

**Atoms.** Newsreader asks, Archivo is furniture, Plex Mono stays because the machine's words
are the same words in both places. Four inks at `oklch(0.42 0.14 h)`, h = 27 / 152 / 258 —
identical lightness and chroma, hue the only variable, which is the pen protocol and the
contrast floor turning out to be one rule.
**Molecules.** The pen note (2px ink rule, mark glyph, ink named in caps, at most three
sentences). The machine plate (dark ground, `VERBATIM · <source>`, repository text, no
gloss). The exit: caps, blue, three on the whole site.
**Organisms.** An `8.5rem / 34rem / 19rem` rail-content-margin grid, so the rail names the
section, the content column holds only quoted material, and the margin holds the opinion. The
specimen spread: the same sheet printed, and returned, at ~0.77 of print size, with the
returned copy set as `scan-back` transcribes it rather than as a drawing of a hand.
**Templates.** Numbered sections in ascending air, a full-size serif question over a 2px
rule, then `clamp(11rem, 34vh, 24rem)` of nothing, then the ink key.

**Weakest where:** it is louder than the product. A dark plate and three saturated inks is
more visual event than `design.md` permits anywhere, so a visitor sold by this page prints
something quieter. The container also leaks where the content is hardest: the ledger's
definitions and cells are 278 words of ordinary explanatory prose, more than every margin
note on both pages combined. And the returned specimen is cleaner than any real returned
sheet, so the eventual photograph will make the drawing look like a lie.

## 4. D — Free × structure and behaviour · *The page is a sheet*

**Stance.** Stop describing the loop and complete the half a static page is capable of. Hand
the visitor a real sheet for the paper already on their desk, then end.

**Atoms.** Three type sizes and no midrange, so there is nowhere to write a lead paragraph;
rules 3 / 2 / 1px; three pen accents that appear on exactly one page, because the channel is
the pen's and it speaks where the pen does.
**Molecules.** A 13ch datum rail, corner crop marks around the sheet, a running head with a
position counter and no clock, mono machine blocks cited to their README section.
**Organisms.** The sheet, in the DOM at Letter proportions with a print stylesheet set to
`design.md`'s numbers, under a two-radio switch: state 01 knows nothing about you, state 02
has done work and puts five of the project's own claims in an `I PROPOSE` column against an
empty `YOU DECIDE`. Both states print as a single 612×792 page and both pass
`verify_layout.py`. Invoking print ends the document, leaving *Printed. Go think.* in Mono
and the `scan-back` link.
**Templates.** Two pages, both terminating in a 34vh empty band with nothing below it but the
position counter.

**Weakest where:** the gate ran by hand, twice, in one engine, on content that never changes
— Firefox and Safari lay the same CSS out differently and nothing checks them. The stop fires
on a cancelled print dialogue, because `afterprint` is the only signal a page gets, which is
a platform ambiguity built on rather than a stance. The `I PROPOSE` column proposes claims
about paper-session to somebody who came about their own work. And the site has room for two
pages, so six documents have nowhere to go.

## What all four agree on

No hero paragraph, no chip filter, no call to action above the fold, no upgraded
compatibility claim, and the ledger printed with its terms defined above the table in every
one of them. All four also name **the pattern library** as the page they cannot carry. That
is the strongest shared finding in the set: whatever wins here still owes that page a home,
and none of the four solved it.

## The open question

**How much is the website allowed to *be* the thing, rather than argue for it?**

A and B argue for it from inside the sheet's law. C and D leave that law to get closer to the
artifact, and each says plainly what the trip cost — C gives up the shared identity and has
no ink for a claim it has to make, D moves the verify gate outside the machinery that owns
it.

A second question sits under it, and B is the only direction that answers it out loud:
**is the front door allowed to withhold the evidence?** B puts `d = 0.93` behind a click on
the grounds that a door that also argues is a page that scrolls. A, C and D all put the three
numbers on the first page.

Pick a direction, name a hybrid, or redline any page. If it is a hybrid, take whole organs —
that is the instruction that produced `design.md`, and averaging these four produces the safe
middle the printed sprint was explicitly told to avoid.
