# Direction C — Free × typography and composition

Two pages, `landing.html` and `interior.html`, opened directly in a browser at 1400px.
Interior is **Install**, chosen because it holds the compatibility ledger, which is the
content this direction claims to serve better than any other and the content most easily
ruined.

What is held constant with the printed system: the three-voice law (one face asks, one
face is the machine, tracked caps is furniture), the withholding rule, no clock anywhere,
pages decompress downward, open territory closes every page, colour never the sole
carrier of meaning. What is varied: two of the three faces, the ground, and the colour
channel.

---

## The bet

The sheet is grayscale because the pen must be the loudest thing on it, and no reader
will ever put a pen on a website — so this direction supplies the pen itself: every
colour on the site is ink, the site's own opinions are spoken *only* as pen marks in the
margin, and a margin note is physically too short to be canned.

That is the whole departure, and it buys two things keeping the constraint cannot.
**One:** the website stops being a blank sheet that nobody will fill and becomes the
sheet coming back, which is the half of the loop the product is named for and the half
the current site under-sells. **Two:** it puts a hard cap on the site's voice. The
wordiness the maintainer flagged is a structural fault — nothing stops prose expanding —
and this direction narrows it with a container rather than with editing. The site's own
editorial voice on `landing.html` is **158 words** across five margin notes, plus a
39-word placeholder stamp and the ink key. A margin note has nowhere to grow.

The container is not airtight, and the critique found where it leaks. See *What it gives
up*, item two: the ledger's own cells are the site talking, and they are the longest
prose on either page.

The departure from IBM Plex is a second, smaller bet: a website set in the sheet's own
faces is claiming to be a sheet. It isn't. It is the argument for one, and it has to be
able to quote the sheet as an object. So the site gets its own asking voice and its own
furniture, and keeps **Plex Mono** as the single shared face — because the machine's
words really are the same words in both places. Put a specimen on this page and it reads
as a foreign object, which is exactly what it is.

---

## The mechanism

**Atoms.** Ground `oklch(0.968 0.004 95)`, ink `oklch(0.235 0.008 250)` — both toned,
neither pure, chroma under 0.02. Four inks at *identical* lightness and chroma,
`oklch(0.42 0.14 h)`, h = 27 red / 152 green / 258 blue, black is the ink itself; hue is
the only variable, which is the pen protocol's own claim and the craft floor's rule
turning out to be the same rule. Contrast on ground: 8.3 / 7.0 / 7.9 : 1. On the dark
plate the same three at `oklch(0.80 0.13 h)`. Type: Newsreader asks, Archivo is
furniture, IBM Plex Mono is the machine. Scale 0.6875 / 0.875 / 0.9375 / 1.0625rem, then
a jump to `clamp(1.45…1.95rem)` and `clamp(2.1…4.4rem)` — five steps, two of which are a
rounding apart, and nothing in the midrange where lead paragraphs get written. Rules
3 / 2 / 1px, with the sheet's writing guide floored at `max(0.75px, 0.5pt)` because 0.5pt
at screen scale is below the rendering floor and the *relationship* is what transfers,
not the arithmetic.

**Molecules.** The **pen note**: a 2px left rule in the ink, the mark glyph
(`•` `?` `!` `✓` `→`), the ink named in tracked caps, then at most three sentences of
Mono. The **machine plate**: dark ground, `VERBATIM · <source>` in a hairlined caps
header, repository text underneath, nothing around it. The **rail**: `01` in Mono over a
tracked-caps section name, 8.5rem wide, never violated. The **exit**: caps, blue, 2px
underline, three of them on the whole site.

**Organisms.** The page grid is `8.5rem / 34rem / 19rem` inside a 78rem wrap: rail,
content, margin. The rail names the section, so the heading has nothing to argue and
reverts to a question; the margin holds the opinion, so the content column holds only
quoted material. The four-part `label → h2 → prose → aside` stack has no slot to live in.
The **ledger** is words plus a mark plus a hue, never a tick, never a colour alone, with
Greptile-style definitions set *above* the table so the reader can check the claim; one
row of five is green, and the page says so. The three evidence figures are quoted
too, under one `VERBATIM · README §Why paper` label, because a number with a condition
line attached is the repository's sentence and not mine. The **specimen spread** renders
the sheet from `references/design.md` at `--pt: 0.16340cqw` (612pt = 100cqw), giving ~0.77 of print
size at 1400px, twice: printed, and returned. The returned copy is the transcription
`scan-back` produces, not a drawing of handwriting — no script face, no wobble, nothing
imitating a hand, and it is stamped as a rendering with the real photograph's path
(`site/static/hero.jpg`) named as missing.

**Templates.** Masthead, 3px datum, a right-aligned caps line under it saying the colour
is ink, numbered sections in ascending air (3.5 / 5 / 6 / 7.5 / 9rem), a full-size serif
question over a 2px rule as the terminator, and then **nothing** — `clamp(11rem, 34vh,
24rem)` of empty ground under the last question before the footer rule, which is the only
place on a website where a page can actually decompress. Then the ink key and a colophon.
No navigation below the last question, no next-page link, no newsletter, no repository
star. Both pages carry `PAGE 0N OF 02`; the last one says
`END`. Focus rings are ink, deliberately — blue is spoken for.

---

## What it gives up

**It is louder than the product.** A dark plate and three saturated inks on a light ground
is more visual event than `design.md` permits anywhere, on any page, ever. The site
out-designs the artifact, and a visitor who is sold by this page and then prints a sheet
gets something quieter than what convinced them. Directions A and B do not have that
problem because they never leave the printed register. This one buys its clarity with a
gap between the advertisement and the thing. On `interior.html` the cost is at its worst:
three route plates side by side is the largest black mass on the site, on the page whose
subject is a piece of paper.

**The container leaks exactly where the content is hardest.** The bet says the site may
ask and annotate but never explain, and that prose therefore has nowhere to accumulate.
That holds for the argument and fails for the ledger. The four status definitions (131
words) and the five ledger cells (147 words) on `interior.html` are the site's own
sentences, in Mono, off-plate, unmarked — 278 words of ordinary explanatory prose, more
than the two pages' margin notes put together. The critique found them restating each
other almost line for line ("*the forward half produces a hand-copied card rather than a
PDF*" in the definition; "*the forward half produces a hand-copied card, never a PDF*" in
the row two hundred pixels below) and they have been cut apart so each says one thing
once. But the hole is structural, not editorial: a ledger is a page where the site's job
*is* to make a claim, and this direction has no ink for that. The next page that needs one
will open it again.

**It teaches a protocol nobody asked to learn.** The colour is only meaningful once the
ink key is read, and the ink key is in the footer. A caps line under the datum now says
the colour is ink before the reader meets any, which is orientation, not the key. A reader
who scans and leaves has seen a pretty page with three accent colours — precisely the
generic outcome the provocation warned about, arrived at by a non-generic route.

**A visitor gets no exit for 4,000 pixels.** Open territory closes the page, so the links
close it too: there is no navigation in the masthead and none until section 04. That is
the printed page's gravity honoured literally on a surface where people arrive from a link
and leave in nine seconds. I think it is right. I can't prove it isn't just stubborn.

**It gives up the shared identity.** Two of three faces are new, so the site and the sheet
are no longer the same object. Someone who loves the sheet meets a stranger. And Newsreader
at 4.4rem is one bad decision away from being the oversized-display-serif move the
research told me to refuse; the only thing holding it back is the rule that every serif
line is a question, which is a rule a second author can break without noticing.

**It renders a returned sheet that is cleaner than any real one.** Specimen B is legible,
straight, and correctly spelled. Real returned pages are crooked and half-illegible. When
the maintainer finally shoots the photograph, the honest artifact will look worse than my
drawing of it, and the drawing will retroactively read as a lie. The page now says so once
— in red, beside the spread — rather than three times in three places, which is the most
this can be answered without the photograph. It is a reduction of the charge, not a reply
to it.

**The margin is a desktop device, and it is a narrower desktop than I claimed.** The
three-column grid used to hold down to 832px, where the pen column was 230px wide and Mono
set at 24 characters a line — a squeezed tower nobody would read. It now collapses at
1024px, so everything below a laptop gets the stacked layout: the notes keep a 34rem
measure so they still read as asides, but the one place the copy cap was enforced by
layout is gone on every phone and most tablets. At 420px the specimen spread drops to
~0.46 of print size and its type is texture rather than words.

## Where it would break

**`/limitations`.** Six numbered items, each needing real nuance about replication
failures and ecological validity, on a page where the site's voice is a three-sentence
margin note. Either the device is abandoned for one page — inconsistency the reader will
read as evasion, on the page where evasion costs most — or genuine nuance gets crushed
into slogans, which is the boast-by-negation failure the project bans in its own
anti-pattern list. And a page whose every mark is red reads as an error state, not as
honesty.

**A screen-reader user.** Hue carries nothing to them, and every ink is named in words
inside the mark, so the meaning survives. The hierarchy used to not survive — a pen note
and a plate arrived as two paragraphs in a row with no signal that one was an aside and
one a quotation. Plates are now `<blockquote>` and pen notes carry `role="note"`, which is
the cheap 80% of it. The expensive 20% is unwritten: the plate's source label is a
`<span>` inside the quotation rather than a `<cite>` beside it, so the attribution is read
as part of the quote.

**Anyone printing the website.** Dark plates, on a site about printing. The irony is
load-bearing and I have no defence for it beyond a print stylesheet I did not write.

**The pattern library page.** Twenty-plus named patterns, each with an evidence note and
contraindications. That is a page that is nothing but content, and this direction's whole
mechanism is a container that keeps content out of the site's voice — it has no answer for
a page where the content *is* the site's job. The Waka Waka index would carry it, and it
would look like a different site.

---

## The copy position

**The site is allowed to ask, and to annotate. It is not allowed to explain.**

Three layers, and each one may only say a certain kind of thing. Serif asks: every serif
line on both pages ends in a question mark, no exceptions, verified. Mono on a plate
speaks only the repository's own words, marked with their source, and is never introduced,
summarised, or followed up — the reader can read. Everything the site itself thinks is a
pen mark: an ink, a mark, and at most three sentences.

Two consequences worth wanting, one of them only mostly true. First, the site rarely
states a product claim in its own voice — the one rule, the anatomy law, the three
numbers, the install directions all arrive as quotations, so the page cannot drift from a
repository that keeps moving. Rarely, not never: the ledger is the exception, and the
exception is 278 words long. Second, honesty stops being a disclaimer. *No study tests this artifact* and *installs cleanly, loop untested* are not
buried in a hedged paragraph; they are red marks, in the same ink the product tells you to
use for exactly that, sitting in the margin where a person would have put them. The most
credible sentences the project has are now the most visible things on the page, and they
are visible because of a colour law the product wrote.

What died to get there: every lead paragraph, every caption describing the thing above it,
every `Ends with:` formula, the 204-word defence of a design decision nobody asked about,
and all twelve `<details>` disclosures. Most were not edited out; there was nowhere left
to put them. The ones the critique had to cut by hand — a blue note that was not an exit,
a caption announcing "*the same page twice*" directly above two captions saying PRINTED
and RETURNED, "*no account, no install, nothing to agree to*" — are the measure of how far
a container gets you, which is far, and not all the way.

---

## What the critique changed

The direction is unchanged. Seven things in it were not good enough.

1. **The blue note at the top of `landing.html` was not an exit.** The ink key declares
   that blue marks what you can do from this page; the loudest blue on the page was a
   description of the product. Now black, and cut from 26 words to 17. Blue on the site
   now appears only on exits — and the specimen beside it still shows blue in its *sheet*
   sense, which is what makes the remap legible rather than borrowed.
2. **The colour orientation was an opinion doing furniture's job.** "*This page is set in
   three voices, and the colour on it is ink*" is not an aside, it is a legend. It is now
   a tracked-caps line under the datum, where infrastructure lives.
3. **The specimen said "not a photograph" three times** — a red note above the spread, the
   stamp, and a second red note beside the stamp. Once, in red, beside the spread. The
   stamp lost 16 words and the margin next to it is now empty, which is the argument.
4. **The three evidence figures were the site explaining in Mono.** They are the README's
   own sentences with the seams showing. Restored verbatim, labelled as a quotation, and
   the three caps labels that repeated the first clause of each quote are gone.
5. **The ledger restated its own definitions.** Four definitions and five rows saying the
   same four things twice, one screen apart. Every row now carries only what its status
   does not already say, and `Supported` became `Supported, not verified` so both pages
   use one vocabulary. No claim moved up.
6. **The page preached decompression and did not decompress.** The closing question had
   80px under it and then a footer. It now has up to 24rem of nothing. This is the single
   most on-thesis change and it was a two-line fix.
7. **The three-column grid held 200px past its own competence.** Between 832 and 1050px
   the pen column was 230px of 15px Mono. The grid now collapses at 1024px and the notes
   keep a 34rem measure when they fall inline.

Cut in total: about 160 words of site-written prose. Nothing was added except one caps
line and the terminator’s air.
