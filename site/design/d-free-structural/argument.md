# Direction D — Free / structure and behaviour

**The site hands you a page.** Same content as the other three directions where content
overlaps; the variable here is what the page *does*, not how it is set.

---

## The bet

A site for paper-session should stop describing the loop and do the part of it a static page
is actually capable of: hand the visitor a real sheet for the paper already on their desk, put
the sheet that withholds and the sheet that proposes under one switch so the rule reads off the
object, and then end.

## The mechanism

**Stance.** The website is a session. Not a simulation of one, not a tour of one: the front
door renders an actual single-provocation Deep sheet, in the DOM, at Letter proportions, with
a print stylesheet set to the real numbers from `design.md` (`@page size: letter; margin:
54pt`, 2pt datum rule, 21/28pt provocation, 108pt open-territory floor, footer below the
margin box). Ctrl+P produces the artifact. No account, no download, no PDF, no AI, no install.
The visitor who has a printer gets a sheet; the visitor who does not gets the same six lines
to copy into the notebook they already own — one object, two verbs, no branch.

**Atoms.** Three type sizes only: `--fs-ask` clamp(2.1→4.6rem) serif, `--fs-body` 1rem sans,
`--fs-label` 0.6875rem tracked 0.15em caps. No midrange, so there is nowhere to write a lead
paragraph. Rules: 3px datum, 2px terminal, 1px hairline. Toned neutrals in oklch — paper
0.968/C 0.004, ink 0.245/C 0.008, small-caps floor 0.46 (~4.9:1). Three pen accents at shared
L 0.52 / C 0.14, hue 27 / 152 / 262, and they appear on exactly one page.

**Molecules.** A 13ch left datum rail carrying `01 THE SHEET`, `02 WHEN YOU COME BACK`,
`03 THREE NUMBERS`, `04 WHERE THE LOOP STANDS` — the rail names the section, so the heading
under it has nothing left to argue and was deleted. Corner crop marks around the sheet.
A running head with a position counter (`01 / 02`) and no clock. Machine blocks are
mono, hairline-ruled at the left, and carry a `README §, verbatim` cite; nothing glosses them.

**Organisms.** (a) **The sheet, which has two states, and the difference between them is the
rule the whole system runs on.** State 01, *knowing nothing about you*: datum rule, title, live
date, an intent line that is a real input, First Three Are Free in a 1pt box, one provocation,
ruled guides, OPEN TERRITORY. State 02, *having done work*: a two-column react, `I PROPOSE` in
Mono against an empty `YOU DECIDE`, `Cross out freely.` in the gutter, same territory, same
footer. Two radios, no JS, both states print and both pass the gate. The visitor is never told
what withholding means; they flip between a page that proposes and a page that does not, and
read it off the object.
(b) The verbs, three rows in the aside: *If you can print* / *If you cannot* / *What decides
which of the two* — the third is the install link, argued by the switch rather than by pitch.
(c) The ledger: status words in Mono, never ticks, never colour, with **every** word the table
uses defined in a list above it, so the claim can be checked instead of trusted. (d) The filing:
six numbered rows of what the research does not support, date-stamped, on the interior page.

**Templates.** Two pages, both terminating in a 34vh empty band under a 2px rule labelled
OPEN TERRITORY, with nothing below it but the position counter. Page 2 reads `02 / 02 · END`
and carries no forward link at all; the way back is in the running head, where navigation
belongs, not at the terminal position.

**The behaviours, both of them.** The switch is the first, and it is the only place on the
site where the central rule is demonstrated rather than asserted. The second: invoking print
sets `data-state="ended"` on `<body>`. Every band, the running head, the datum and the terminal
band are removed and replaced by one line in Mono — *Printed. Go think.*, the skill's own
closing message, so it is the machine speaking — plus the `scan-back` link the visitor will
need on the return trip. The site obeys its own stop rule, and it does not merely say so. It is
put away, not destroyed: the scroll position and anything typed into the intent line come back
on Escape or on a full-size control. There is no animation, no scroll trigger, no reveal, and
no progress state anywhere on either page.

**The interior page is the return trip**, chosen over get-a-sheet and install for one reason:
it is the only half of the loop that already works, today, on paper the visitor has and an AI
they already own, with nothing installed. Get-a-sheet would restate the landing page. Install
would make the site about installation. The return trip is also where the pen protocol lives,
which is the only place on the site colour is permitted — the channel is the pen's, so it
speaks where the pen does and nowhere else, with the ink named in words beside every swatch.

**No hero photograph.** This direction does not reserve the slot. A photograph of a sheet is a
picture of the artifact; this page is the artifact, and spending the first screen on a picture
of the thing sitting 400px below it would be the caption problem in image form.

## What it gives up

**The verify gate, which is the project's hardest rule.** `SKILL.md` says never present an
unverified sheet. Both printed states were checked — Chrome's print output is a single
612×792 page in each case and `paper-session/scripts/verify_layout.py` returns PASS on both —
and that is the whole of the guarantee. The gate is meant to run per sheet, at generation time,
against reportlab output; here it ran twice, by hand, in one engine, on content that never
changes. Firefox and Safari lay the same CSS out differently and nothing checks them.
Concretely: a visitor whose browser breaks the provocation one line later pushes OPEN TERRITORY
past the page break, and the last thing out of their printer is a rule with nothing under it.
The second state doubled the surface this applies to. Every other direction shows an image of a
sheet that reportlab made and the gate saw, and is right to.

**The stop fires on a cancelled dialogue, and no browser will say otherwise.** `afterprint` is
the only signal a page gets, and it arrives whether the sheet printed or the visitor pressed
Escape in the preview. That is not a stance, it is an ambiguity in the platform that this
direction chose to build a behaviour on top of, and calling it conviction would be laundering a
bug. What it costs, plainly: somebody who opens the dialogue to check the margins and thinks
better of it gets a page that has ended on them, and has to undo it. The mitigation is that
undoing is free — a control at the same weight as every other control on the site, Escape from
anywhere, scroll position and typed intent line restored. The worst case is one unexpected
keystroke rather than a lost visit. The bet stands: a site about stopping should be willing to
stop. It is still a visitor interrupted for curiosity.

**The machine's column argues about the wrong subject.** State 02 answers the worse version of
this problem — a front door that could only demonstrate withholding, and described the
machine's half in a twenty-word aside — but it answers it with the only work this website has
honestly done, which is its own argument. So `I PROPOSE` proposes five claims about
paper-session, to a visitor who came about their own work. The mechanism is now on the page;
the subject is still the site. Only the installed skill can put your material in that column,
which is the true statement and also the sales pitch, and those being one sentence is
convenient enough to be worth distrusting.

**A switch is a thing that has to be noticed.** State 01 is the default, and a visitor who
never touches the labels sees exactly the site that existed before this was added. The whole
correction rides on one pair of small tracked-caps labels above the sheet.

**Below 620px the sheet stops being Letter.** Held at 612:792 on a phone, the sheet's own type
falls under 8px and the object the page rests on becomes a thumbnail of a sheet — the picture
this direction refuses to print, arriving through the back door. The fix is to drop the aspect
ratio and let the sheet run as long as it needs at 13px, so a phone gets a legible page that is
no longer the right shape. Print output is unaffected. Legibility over proportion is the
project's own rule; it is still a compromise, and it means the phone visitor never sees the
proportions the desktop visitor does.

**It has room for two pages.** The pattern library, the named session formats, the design
history, the research process, CONTRIBUTING — six documents with nowhere to go. And restricting
Serif to questions leaves the site with no long-form register at all, which is fine until
somebody needs to publish an argument.

**Only one of the two pages is printable.** The ink key and the mark vocabulary are exactly
what a person wants lying beside the marked-up pages, and the interior page does not offer
them. Dressed up at 54pt margins it runs to three pages and `verify_layout.py` fails it on a
character collision in the serif-italic notes. That is a font-metrics artifact rather than a
layout error, and it does not matter: the gate does not take excuses. So the site prints a
sheet and nothing else, and the reference the return trip actually needs stays on screen.

**The faces come from a CDN.** The repository ships IBM Plex locally and these pages load it
from Google Fonts. Blocked or offline, the three voices silently become Georgia, Segoe UI and
Menlo, and the one thing on a sheet that cannot be paraphrased degrades without saying so.
Self-hosting is the fix and it is not done here.

## Where it would break

**The pattern library.** Twenty-odd patterns, each with an evidence cluster and its own
contraindications, is a document, and this direction has no document page — only an index, two
sheet states, and a terminal. Rendered here it becomes a list of names, which withholds precisely
what a contributor came for. That is the same failure the direction diagnoses in the site it
replaces, arriving from the opposite side.

**The group formats.** Brainwriting rounds and the Grinnell field kit are one page pattern
printed six times. A site whose whole structure is *here is your one sheet* cannot express a
kit, and would quietly teach that the system is single-sheet.

**A phone visitor with no printer and no notebook.** Both verbs resolve to paper, and they
have none. The page has nothing else to offer them except a link out to a README.

**A screen-reader user in the ended state.** The terminal block is `aria-live`, but the visit
ends on an event they may have triggered while exploring the controls, and the way back is one
unlabelled-looking mono button.

## The copy position

**411 words in the site's own voice across both pages** — counted with a script over every
prose element on both, table cells and definition lists included, which is the least flattering
way to count it. Everything else on the pages is apparatus (rail labels, status words, the
three numbers), the sheets' own printed text, or one of four verbatim repository quotes. The
site this replaces runs 25,848 words over seven pages; its front page alone is 2,057. Three
registers, and the site is only allowed one of them.

- *Serif roman asks, and only asks.* Two questions on the whole site — `What are you agreeing
  with because arguing takes longer?` and `Where your pen contradicts the machine, which one
  is right?` — plus the sheet's own provocation. Serif *italic* is the aside, the same job it
  holds in `design.md` §5, and it is the only place on the site prose is allowed to run: four
  short notes, none of them restating a heading. The closing line the stop state prints —
  *Printed. Go think.* — is the skill's own message, so it is Mono rather than Serif, because
  it is the machine speaking and it is not a question.
- *Mono is the machine, remapped and declared:* on this site it means words the machine
  contributed — three blocks lifted verbatim out of the repository and cited to their section,
  the five propositions in the `I PROPOSE` column of sheet state 02, and the closing
  *Printed. Go think.* No gloss, no caption, no paragraph introducing one and none following.
  The reader can read. The propositions are the site's own claims, set in the one register
  where a reader is invited to strike them out rather than agree with them.
- *Sans is the site,* and it speaks in imperatives (`Paste it. Add the photos. Say nothing
  else.`), in rail labels, and in ledger cells. It never explains a heading and never restates
  a claim, because there is no type size between body and display to write the restatement at.

What follows mechanically: the four-part `label → question → prose → aside` stack is gone,
because the rail is the label and there is no lead size for the prose. No caption on the site
names the thing directly above or below it — the scroll cue is a number, not a repeat of the
rail label it sits over. The honest compatibility claim is a Mono status cell whose every term
is defined in the list above the table, never a hedged paragraph, and never a status word the
list does not carry. And the ban list is never set as a boast — the absences on sheet state 01
are simply absent, and the difference between the two states is left for the reader to notice,
which is the only way this project is allowed to state them.
