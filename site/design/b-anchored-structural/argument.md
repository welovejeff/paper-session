# Direction B — Anchored × Structure and Behaviour

Two pages, same chassis. `landing.html` is the index. `interior.html` is Install, chosen
over the specimen page and the paste page because it is the densest content on the site
and the one carrying the compatibility ledger — if the fixed-page bet survives a five-row
status table and two install tracks that are not allowed to rank each other, it survives
everywhere else.

Constants held from the printed system: Plex Serif asks, Plex Mono reports, tracked Sans
caps is furniture, grayscale carries everything. Nothing imitates handwriting. No time
signal anywhere — no duration, no reading time, no clock in the masthead.

---

## The bet

A website for a product whose success is you closing the tab has to be **finite,
addressable, and visibly over** — so every page here is one bounded screen with a datum
rule at the top, a closing rule at the bottom, a folio under it, and nothing after that.

## The mechanism

**Atoms.** Four type sizes and a gap where the midrange would be: ask 1.85–2.85rem Serif;
row 1.05–1.3rem Serif; body 0.9375rem Sans; label 0.6875rem Sans 600 caps at +0.15em, and
mono at 0.875rem. Nothing between 1.3rem and 1.85rem, because nothing needs to be there
and every rung is a hole a lead paragraph gets written into. Rules: 4px datum / 2px
closing / 1px hairline — the print ladder is 2pt / 1.6pt / 0.5pt, a 4:1 spread between
datum and hairline, and 3/2/1px collapses that to 3:1 with the bottom rung on the
rendering floor; the ratio is translated, not the arithmetic. Neutrals in oklch, warm
paper `0.968 0.006 85`, cool graphite ink `0.255 0.012 250`, label floor `0.460`;
zero accent hues, because the colour channel belongs to a pen and a website has none.
Measured against paper: ink 14.4:1, ink-2 9.1:1, quiet 6.4:1. Focus is a 2px ink outline
at 3px offset, never pen-blue.

**Molecules.** The band: a 12.5rem left rail in tracked caps, a full-height 1px hairline,
content right of it. The rail names the section, so the heading does not have to argue,
so the paragraph under the heading has nothing left to explain — that is where the
existing site's word count went. The index row: `[mono numeral] [Serif statement]
[Sans-caps destination]`, whole row a link, hairline between, right edge landing on the
same datum as every rule and the folio. The verbatim block: a caps key stating the source
(`VERBATIM · README §INSTALL`) over Mono lines. The status cell: words inside a 1px box —
`VERIFIED END TO END`, `INSTALLS CLEANLY, LOOP UNTESTED`, `UNTESTED, PER SURFACE` — never a
tick, never a colour, never behind a disclosure widget.

**Organisms.** The index: six first-person preconditions numbered 01–06, each one click
from its destination. It is table of contents and router collapsed into one object, which
is why the site can state that it has six pages and mean it. The two-track grid:
`repeat(2, minmax(0,1fr))` divided by one hairline — the README's rule that neither
install track may be favoured is enforced by column width, not asserted in a sentence.
The ledger: definitions line first in Serif italic, then five rows, then a tally set
Büro-style — a 5rem `1` beside `OF FIVE ROWS CARRIED A PAGE ALL THE WAY ROUND`. The
project publishes its own low number at display size.

**Templates.** `.sheet` is `min-height: 100dvh`, flex column, with a `1fr` margin above the
closing rule. The band rule runs on through that margin to the closing rule, so a page
whose content stops early reads as a half-filled sheet rather than a build that ran out;
and the slack in a tall window goes into band padding (`clamp(_, 3vh, _)`) before it pools
at the bottom. The one behaviour on the site is the running head reporting which sheet
holds the viewport — no motion, nothing hidden until scrolled to, and without JavaScript
the head reads `INSTALL` and the folio stays the source of truth. The index is one screen;
Install is two, folioed `Sheet 1 of 2` and `Sheet 2 of 2 · END`, snapped at `y proximity`
and unsnapped under `prefers-reduced-motion`. The
page address lives in the rail (`PAGE 04 OF 06`), the sheet address in the folio — exactly
the split the printed footer makes with `Deep · 1 of 2`. Nothing sits below a folio: no
next-page, no related links, no newsletter, no star-the-repo. Navigation lives in the
running head, at the top, where leaving is cheap.

**What is deliberately absent.** No hero photograph slot — the one admissible image is a
photograph of a real completed sheet and the maintainer has not shot it, so this direction
is built to be correct without it rather than reserving a hole for it. No accordions. No
scroll-triggered reveal. No configurator. No `overflow` property anywhere on either
document element: the index fits a screen because a hundred and twenty-two words fit a
screen, and at 200% zoom the page grows and scrolls rather than clipping. Measured
`scrollWidth == clientWidth` at 420, 760 and 1400.

## What it gives up

**Persuasion.** The index routes and does not argue. `d = 0.93`, `58%`, and *confidence
held steady* are the three most convincing objects this project owns and none of them are
on the front door — they sit behind row 06, where a visitor who wants to be convinced has
to click. A reader who arrives cold, curious, and unwilling to click gets thirteen words
of Serif and six sentences that are all about themselves. That is a real conversion cost
and it is the price of the bet: a door that also argues is a page that scrolls.

It also gives up the empty half, and the reason is a reading of the law rather than a
refusal of it. The printed rule reserves ≥50% of a page for the pen; what the rule is
protecting is that the printed layer never competes with the hand. A website has no hand,
so the transposition is not acreage, it is deference: no hero, no photograph, no colour,
no button, no type louder than the sheet the product prints. That the site honours. What
it does not do is label a band `OPEN TERRITORY` and leave it blank, which on the existing
homepage reads as an unfinished build. The margin here is a tenth of the screen, the band
rule runs through it to the closing rule so the space is legibly part of the page, and it
is called `.margin`. A maintainer who wants the 50% law transposed literally should reject
this direction on that point alone: it is load-bearing and it is a demotion.

And it gives up growth. Six index rows is a hard cap. A seventh route means redesigning
the front door, not appending to it.

**The apparatus currently over-claims its own document.** The folio publishes `Index · six
pages` and Install's rail publishes `Page 04 of 06`, but five of the six rows resolve to
the README on GitHub, because five of the six pages are not built. That is the direction's
own form-smell charge turned on itself: numbering that describes nothing real is
decoration. In a prototype it is scaffolding and I have left it, because in the shipped
site those destinations are internal pages and the numbering becomes true. It does mean
this direction cannot be shipped half-built — a five-page site with a six-page folio is
worse than a site with no folio at all, and worse specifically in the way this project
cares about.

**The behavioural budget is one gesture, and that is the ceiling.** The running head
reports position; `scroll-snap-type: y proximity` lands the next sheet cleanly and is
switched off under `prefers-reduced-motion`. Nothing else moves, stores, filters, or
remembers. On an axis named *structure and behaviour* the structure is carrying almost all
of it, and a reviewer expecting the behaviour half to be the argument will find it thin.
The defence is that every behaviour this site could plausibly add — a configurator, a
"which agent are you" filter, a progressive-disclosure ledger — is a way of not committing
to an answer, and the index already committed. But it is a defence, not a rebuttal.

## Where it would break

**A long document with no natural page breaks — `evidence.md` rendered as a site page.**
Sixty citations and six limitations do not divide into bounded screens; the folio would
either lie (`Sheet 7 of 14` on arbitrary cuts) or the page would scroll for a minute under
a chassis whose entire claim is that pages end. The failure is the one the direction
notes call *form-smell*: an apparatus that stops matching what is inside it becomes
decoration, and a folio that numbers nothing real is a broken promise of the same kind as
a cut line on a sheet nobody will cut.

Second: the two-track grid is honest only while there are exactly two tracks. Add the
paste path as a third column and the equal-width argument becomes an equal-width
misstatement, since that path is genuinely unverified and the layout would be claiming
otherwise.

Third, the reader it serves worst: someone who has never heard of this and does not
recognise themselves in any of the six statements. Rarible's routing works because its
five statements exhaust its audience. Mine do not exhaust a stranger's, and a stranger
who fails to find their row has no fallback except the source link in the folio.

## The copy position

**The site is an apparatus, and the apparatus does the talking.** A hundred and
twenty-two words of visible text on the index, skip link, running head and folio included;
three hundred and sixty-nine on Install, most of them ledger cells and shell commands. Nothing on either
page describes anything visible on that page, nothing is stated twice, and no caption
sits under a block explaining the block.
Where the project has already written a true sentence, that sentence appears in Mono with
its source named above it, and this site does not gloss it. Where the site speaks in its
own voice it speaks in Sans — running prose is infrastructure here, which keeps Serif
meaning *a question is being put to you* and keeps the three-voice rule from dying on the
one surface that claims it.

Two consequences worth naming. The register is flat on purpose: no warmth, no
reassurance, no "we've got your back" — short and canned is still canned, and the honest
alternative to marketing prose is a filing, not a friendlier sentence. And the ledger is
written as a record with its terms defined before the table, so a reader can check the
claim instead of trusting it; `INSTALLS CLEANLY, LOOP UNTESTED` is printed in the same
weight, box, and colour as `VERIFIED END TO END`, and the tally publishes `1` rather than
rounding the sentence up.

Across both pages, including the `<title>` elements: zero instances of *not X, but Y*,
zero em dashes, zero triplets, zero time claims, and no caps key that is not the name of a
source — instructions in the site's own voice were moved out of the keys and set in Sans
sentence case, so Mono blocks declare provenance and nothing else. Checked, not asserted.
