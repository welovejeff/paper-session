# Direction A — Anchored

Two pages, same chassis: `landing.html` (the front door) and `interior.html` (Install, with the
compatibility ledger). Grayscale, IBM Plex only, three voices unblended, no image files.

Interior chosen deliberately: the ledger is the site's hardest content and its most credible
sentence. If an apparatus can carry *"installs cleanly, loop untested"* without a hedging
paragraph around it, the apparatus is proved. Get-a-sheet and the paste page are easier wins.

---

## The bet

The current site does not have a typeface problem or a copy problem; it has no grid and no
apparatus, so its labels turned into sentences — put back a datum you can point at and a named
furniture set, and half the prose deletes itself with nothing lost.

## The mechanism

**Atoms.** Five named steps and nothing off-scale: `--fs-ask`
`clamp(3.15rem, 11.2vw, 10.5rem)`, `--fs-fig` `clamp(2.1rem, 3.5vw, 3.4rem)`, `--fs-body`
`1.0625rem`, `--fs-sec` `0.9375rem`, `--fs-label` `0.6875rem` tracked `.155em`. It was
drafted as three, which was not true of the file: exits, footer nav, table cells, status
boxes and the tally were sitting at `0.8125`, `0.75`, `0.875` and `0.625rem`. A page that
refuses to upgrade a compatibility claim does not get to upgrade its own type-scale claim,
so the strays were folded into the five and the five are declared in the colophon. Rule
ladder 5px / 3px / 1px, which preserves the print
relationship 2pt / 1.6pt / 0.5pt rather than its arithmetic (3px / 2px / 1px collapses the
ratio and puts the hairline at the rendering floor). Paper `oklch(0.968 0.007 95)`, ink
`oklch(0.235 0.008 250)`, secondary `oklch(0.45 …)` at 6.8:1 on paper, hairlines `oklch(0.82 …)`.
Zero chroma spent on anything: no accent, no pen hues, no coloured focus ring — the ring is
2px of ink at 3px offset. Grays are re-derived for screen contrast and the print numbers are
not transcribed, because print gray 0.42 under ambient light and screen gray on a backlit
panel are different physical objects.

**Molecules.** Rail + hairline + body: `grid-template-columns: 176px minmax(0,1fr)`, the
content column carrying its own `border-left`, bands contiguous, so one continuous vertical
datum runs the whole page and stops where open territory begins. Every section is
`rail(label) → one thing`. No band contains a label *and* a heading *and* a paragraph saying
the same thing three ways.

**Organisms.** The ask: one serif question at 154px on a 1400px viewport, top-left against the
datum, the explanatory sentence and the two exits pushed to the bottom of the first screen with
~180px of nothing between them. Evidence: three columns, hairline-divided, Sans SemiBold figure
above a condition line — and the third column sets `Held steady` at figure scale where a
numeral should be, so the punchline is the composition. `Fig. 1`: a whole Deep sheet set in
live HTML off `--s: 1.44px` per print point, every size written `calc(9.2 * var(--s))`, so the
page proves the numeric spec transfers rather than asserting it; 8 mono items, 8 empty ruled
slots, a rotated gutter hint, and the bottom third genuinely empty under the closing rule. Its
content is the repository's committed specimen verbatim — the same eight sessions, the same
intent line, the same 12 Aug 2026 date `docs/specimen.py` prints — because a figure arguing
that the numbers transfer cannot be running invented copy.
`Not printed`: six absences as a spec table, terms left of a sub-datum, reasons at eight words —
never six lines of shouted negations. `Plate 1`: the unshot photograph, dashed, four crop marks,
naming its own path. Ledger: terms defined above the table Greptile-style, status as a boxed
word in the ledger's own vocabulary, tally row under a 3px closing rule reading
`ROWS VERIFIED END TO END 1 / 5` and `OUTSIDE SESSION REPORTS ON FILE 0`.

**Templates.** Masthead → 5px datum → bands hanging off one vertical hairline → open territory
(label, 3px rule, empty band) → numbered footer sitemap, colophon, position counter `1 / 2`.
`PRINTED. GO THINK.` sits in the bottom-left of that band on the landing page only: the
interior page has printed nothing, and a sign-off repeated on every page is a slogan rather
than a rule. Nothing sits below open territory except the
apparatus. No next-article, no related links, no newsletter, no repo-star CTA.

**Voice, declared rather than assumed.** Serif appears in exactly two places across two pages,
both of them questions. Mono is text read out of the repository and nothing else. Tracked caps
is furniture. The site's own speaking voice is Plex Sans regular at body size — a fourth
register, admitted in the colophon, because the print system has no running prose and pretending
otherwise is how the current site diluted Serif into marketing copy.

## What it gives up

**Warmth, and the Basement 60%.** Bureau at nearly 100%. There is not one funny line on either
page. A visitor who arrives unsure what an agentic workflow is meets a 154px question with no
illustration, no photograph, no product screenshot and no warm sentence, and a real population
reads that as academic rather than as confident. The winning print system is a hybrid for a
reason; this is only half of it.

**One instrument, and a phone takes it away.** Every effect here is scale against a datum. On a
1400px screen the question is 154px and the page is unmistakable. At 420px it is 50px, the rail
becomes a hairline caption, and `Fig. 1` becomes a sideways scroll of a Letter page at
`--s: 1.05px`. The direction is therefore strongest exactly where a reader is least likely to
first meet it. Raising the mobile floor from 41px to 50px helps and does not fix it; nothing
short of a second composition would.

**A second, ungated copy of the print spec.** `Fig. 1` restates `design.md`'s point sizes, rule
weights and grays in CSS, and nothing checks it. This is the failure mode the repository
already legislates against: `CLAUDE.md` forbids duplicate copies of a reference doc, and
`build.sh` fails the build when a cross-skill coupling drifts. Nothing watches the website. The
proof is that it had already drifted before it shipped — the footer set `Scan it back to
continue.` in sentence case where §5 specifies tracked caps, the open-territory label was
lowercase where §7 specifies caps, and the eight items were invented rather than the committed
specimen's. Those are fixed. The next spec change will break it again silently, and the honest
options are a generator or a screenshot; this direction chose the version that reads best and
rots fastest.

**A fourth register the print system does not have.** Serif asks, Mono quotes, tracked Sans caps
is furniture — and then the site's own sentences need somewhere to live, so they are Plex Sans
regular. It is now stated in the colophon rather than implied, but stating a rule-break is not
the same as not breaking it. A sheet enforces three voices because it prints no running prose;
a website cannot, and this one does not pretend the difference away.

**The middle.** With no lead size there is nowhere for a second-tier explanation, so anything
needing 120 words becomes a table or gets cut, and some of it should not have been cut.

**Hedging, entirely.** Every claim across the two pages is either verbatim repository text or a
sentence someone can be wrong about in public.

**The ledger's speed.** The site being replaced answers *what are you using?* with filter chips.
This one prints all five rows, defines its four status terms above the table, and makes you
read. That is more honest and slower, and slower is a real cost on the one page whose job is
to get someone installed.

## Where it would break

Three places, worst first.

**The pattern library.** Roughly thirty named patterns, each with a mechanism, a contraindication
and an evidence cluster. Five steps and a rail handle a *ledger* of thirty rows beautifully and
handle the *body* of one pattern badly: the moment a page needs a run of explanatory paragraphs
with internal structure, this system has body and secondary and nothing else, and thirty screens of
undifferentiated 17px Sans against a hairline is the tax-document failure. It needs a fourth
size it is not allowed to have, or it needs those pages to become an index that links out.

**Emotionally heavy content.** The serial disclosure kit — a page about professional setbacks,
written to be seen by nobody, that never comes back. A 154px serif provocation and a boxed
status word are the wrong register for it by a wide margin. `design.md` already forbids house
rules on heavy sheets; this direction has no equivalent gear, because its only gear is scale.

**The unshot photograph.** Plate 1 is a dashed rectangle, and the direction is strongest in
that state, which is a warning rather than a virtue. When a real photograph of ink on paper
lands there it will be the highest-contrast object on the page — as the product's own first
conviction demands — and every composition decision above it will need re-weighing, because
the top of the landing page is built on the assumption that nothing competes with the question.
The prose inside the slot has been cut to two lines; the version that shipped first had
imported the old site's placeholder paragraph almost word for word, which is the clearest sign
of where a page stops being written and starts being carried over.

Two smaller strains: the ledger table needs 760px and scrolls inside its own container below
that, and `Fig. 1` on a phone is a full Letter page at `--s: 1.05px`, legible only if you scroll
it sideways. Both are honest, neither is good.

## The copy position

**Say almost nothing in our own voice, and let the apparatus say the rest.**

The landing page carries about 270 words, the interior about 320. The claim about what the
product *is* gets one sentence of thirty words and never gets restated. Every remaining band is
either a table, a figure, a verbatim block, or the repository speaking for itself — the four
paragraphs of README limitation prose become one mono quote, the honest-status disclosure becomes
a status cell, the six design absences become six rows.

The reasoning is the product's own withholding rule turned on its author: the AI contributes only
where it has done work worth reacting to. A caption describing the thing directly above it is the
site pre-filling a zone the reader could fill themselves, and it is the same defect as printing
an example answer. So there are no captions of that kind on either page; the two that exist state
facts you cannot see — that `Fig. 1` is live type rather than a photograph, that its grays were
lifted for screen.

Three things follow, and they are the whole style sheet. No sentence explains the sentence before
it. No claim is softened by a clause admitting it might not be true — a limitation gets its own
row instead. And nothing anywhere says a session is quick, short, or easy, which is not a stylistic
preference but the rule from `prompt-craft.md` §9 applied to the marketing surface that would
otherwise be the first place it broke.
