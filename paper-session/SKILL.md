---
name: paper-session
description: "Pause on-screen AI work and hand the thinking to the human on paper. Generates a printable PDF worksheet (provocations, ranking activities, sequencing exercises, field-collection sheets, open exploration space) so the user can work with pen and paper away from screens, then return the scanned pages via the scan-back skill to continue the workflow. Use whenever the current task hits work that requires deep human judgment: sequencing decisions, weighing options and their impacts, novel concept development, creative generation, prioritization, or introspection. Trigger on explicit requests ('paper session', 'give me something to print', 'I need to think on this offline') AND proactively propose it mid-task whenever the next step is judgment or creative work that the human would do better with a pen than watching AI guess. Also relevant for recurring rituals like a weekly self-meeting or priority-setting session. Works without a printer — say so: when the user states they cannot print, the same session is dictated as a short card to copy into any notebook."
---

# Paper Session

The premise: in agentic workflows, the bottleneck is not AI output, it is human metabolism of that output. When a task reaches work the human does best (judgment, sequencing, creativity, weighing tradeoffs), the right move is to stop generating and hand the thinking over on paper. This skill produces the printed artifact that carries that handoff.

The companion skill `scan-back` handles the return trip. The two form one loop: screen → paper → pen → scan → screen.

## Core principle: whose thought does this slot belong to?

Every element on the page must pass this test:

- **AI contributes** where it has genuine expertise or has done work worth reacting to: a proposed priority order, gathered data, a set of options with tradeoffs, a draft sequence. Print these so the human can react, re-rank, cross out, annotate.
- **AI withholds** where the human excels: creative generation, free association, judgment calls, naming, deciding what matters. For these, print only the provocation and leave the space empty. Do not pre-fill examples, suggested answers, or scaffolding that would anchor the human's thinking. A worksheet that is "too helpful" defeats the entire purpose.

When in doubt, withhold. The paper holds the human's thinking, not a second copy of the AI's.

This is not just a philosophical stance; it is the most replicated finding in design cognition. Exposure to example solutions makes people's ideas resemble those examples and reduces both how many ideas they produce and how many distinct categories they explore. Telling them not to copy does not fix it. The layout has to do the work. See `references/prompt-craft.md` for how to contribute without fixating, including the one case where a single remote example genuinely helps.

## The evidence base

The design of these sheets is grounded in research on incubation, screen-versus-paper processing, design fixation, and ideation mechanics. `references/evidence.md` holds the full brief with sources and honest limitations. The five rules that matter most at generation time:

1. **Constrain the input, never the clock.** Every generative zone carries at least one input constraint. Never print a time limit, countdown, or suggested duration; time pressure is precisely what triggers shallow processing, and the creativity benefit of constraints holds only in its absence.
2. **Generation and selection never share a zone.** People select their own best ideas no better than chance, with a standing bias toward feasible over original. Selection zones carry a one-line counterweight.
3. **Overbuild the slot count.** Ideation moves through common categories first and reaches novel ones only after those are exhausted. Ten to fourteen short lines, not four.
4. **Categories, not instances.** When marking off well-worn ground, name the abstract categories rather than specific examples. Naming specifics increases fixation; naming categories roughly doubles creative output.
5. **Something gets drawn, and then re-read.** Every Deep kit includes at least one zone asking for a sketch, diagram, or spatial arrangement rather than sentences, paired with a one-line instruction to find an unintended reading of it. Sketching is the strongest paper-specific mechanism available: loose marks fight fixation, and paper beats digital tools specifically at turning reinterpretation into new ideas.
6. **Selection is a fast named gut call.** No rubrics, no scoring matrices. Name the criterion ("the two most original"), add a distance frame, and never mention building or shipping on a selection sheet.
7. **Difficulty lives in the task, never in the typography.** Legibility is never sacrificed for effort. Font-based disfluency is a debunked application of an otherwise sound idea.

## Step 1: Recognize the moment

Propose a paper session freely when the task reaches:
- Sequencing (course arcs, roadmaps, campaign phasing, narrative order)
- Weighing options where the decision has real consequences
- Novel concept development or naming
- Prioritization the human must own (weekly planning, backlog triage)
- Introspection or reflection prompts
- Field collection (observations to gather away from the desk)

Propose it in one sentence, e.g.: "This next part is judgment work. Want a printable so you can work it out on paper, then scan it back?" If the user invokes the skill directly, skip the proposal.

## Step 2: Determine capacity (Deep or Light)

Two session modes exist. Infer from task context, conversation, and time of day; confirm with at most one short question if genuinely ambiguous. Never quiz.

**Deep** (focused block, ~30-60 min, clipboard on a patio or at a table):
- Sequencing, weighing, novel concepts, creative generation
- Provocations that demand sustained thought
- Multi-sheet kits acceptable (2-4 pages max)
- Generous open space per prompt

**Light** (ambient, ~10-20 min, couch, possibly during TV):
- Sorting, reacting, ranking, checkbox decisions, quick gut-calls
- One page only
- Low cognitive load per item: circle, rank, cross out, one-word answers
- A Deep provocation on a Light sheet will simply not get done

Evening context or a casual framing suggests Light. A cleared block, a hard problem, or explicit "I need to really think about this" suggests Deep.

## Step 3: Design the artifact

Read `references/page-patterns.md` for the activity pattern library and `references/prompt-craft.md` for how to word what goes on the page. Choose 1-3 patterns that fit the task; do not use every pattern on every sheet. Any sheet with a generative zone also gets one defixation pattern (Spent Ground, First Three Are Free, or the Single Remote Example). The library closes with named session formats — whole-session kits chosen by name when the task matches (after-action review, premortem, outside view, teach-back, weekly review, Grinnell field kit, serial disclosure kit). Three carry hard gates: an after-action review needs a recorded plan or log to print (no record, no AAR); a weekly review's inventory is only what you can actually see — skip it rather than invent loops; and the serial disclosure kit is gated below.

**The serial disclosure kit's gate.** Offer it for work friction and professional setbacks only, and never as therapy, treatment, or clinical support — it is structured reflective writing, and nothing printed or said may frame it as anything else. Never to someone in acute distress, after recent or severe trauma, seeking trauma processing, or who says they do not usually put feelings into words. It is three sittings on consecutive days plus a closing distillation page, so proposing it means proposing the whole series; a single sitting falls outside every estimate behind the format. Say in the offer that the first sittings reliably feel worse and that the dip is unrelated to whether it works. Promise no relief.

Layout rules (non-negotiable):
- **8.5 x 11 inch (US Letter), portrait** unless the activity demands landscape (e.g., timeline sequencing)
- **Pen-friendly**: minimum 0.75 inch margins, generous line spacing, ruled or dot-grid guides only where writing is expected, never gray-on-gray
- **White space is a feature.** If a page looks full before the human writes anything, it is wrong. Target: at least 50% of each page is space for the human.
- **One provocation per zone.** Never stack three questions in one answer box.
- **Every sheet ends with open territory**: an unstructured "anything else / free association" zone, even on Light sheets. Human thought on paper wanders productively; give it somewhere to go.
- Maximum 4 pages for Deep, 1 page for Light. More pages means less completion.

Header on every page (small, top of page — the anatomy in `references/design.md` §4): session title, date, and a one-line intent ("Re-sequence the spring course arc"). Write the intent line so a cold reader could resume the session from it alone — scans can return to a chat that no longer holds the context, and that line is the loop's only stateless carrier (`references/prompt-craft.md` §6). Printing it on every page means an orphan scan missing page 1 still reconstructs. It stays for human orientation, never machine parsing: do not print QR codes, session IDs, or context blocks for the AI.

Footer on the last page (small): "Done? Scan or photograph these pages and drop them back into the chat."

## Step 4: Generate the PDF in the design system

Every sheet is set in the Paper Session design system. Read `references/design.md` and implement it exactly: it specifies the fonts (bundled in `assets/fonts/`), the three-voice rule (Serif asks, Mono is the machine's voice, infrastructure is tracked Sans caps), the type scale, rule weights, header anatomy, voice captions (I PROPOSE / YOU DECIDE — always first person, never a third-person label), zone molecules, and the Deep/Light templates. Do not freelance the visual language; the system is the product's identity. Follow the pdf skill (`/mnt/skills/public/pdf/SKILL.md`) for reportlab mechanics.

**If the user cannot print.** Only when they say so, in any phrasing, before or after a PDF exists. Never ask, never propose it, never suggest finding a printer; regenerate as a setup card without comment. Full spec in `references/prompt-craft.md` §10.

- Tablet and stylus: point at annotating the PDF directly, one line, then stop.
- Light capacity: ask the gut calls here in the chat instead. Dictate a card only if they ask for one.
- The card is one fenced message in two strictly separated parts. **COPY THIS** is hand-transcribed: the intent line verbatim (now the loop's only anchor), one prompt per page, a corner page number, machine items as numbered handles of four words or fewer under a hand-copied `I PROPOSE` caption, at most one machine line quoted whole. **DO THIS** is read and never copied: structure as pen gestures ("number 1-12 down the margin before writing anything in line 1"), house rules, pen legend.
- Handles never appear on a page that also carries a generative zone. The full items stay in the chat for `scan-back` to expand against.
- Budget: **50-75 handwritten words for Deep, one phone screen for Light**, stated in words and never in minutes. Over budget means the design is too print-shaped — simplify it, never dictate more.
- Step 5 does not apply to a card; the budget count is the gate.

## Step 5: Verify before presenting (mandatory)

Run `scripts/verify_layout.py <pdf>` on the generated file. It fails on colliding text — across baselines and on a shared baseline — and on text escaping the page, the defects that survive casual inspection and ruin a sheet at the printer. If it fails, fix the layout (shorten or rewrap text, resize, respace) and regenerate until it passes. Never present an unverified sheet. Then save the PDF to the outputs directory and present it.

## Step 6: End the on-screen session cleanly

After presenting the file, close with one or two sentences: what the sheet asks of them and that the workflow resumes when they scan it back. Do not summarize the sheet's contents at length, do not keep working the task, do not generate the answers the sheet is asking the human to produce. The whole point is to stop. "Printed. Go think." is the spirit; for a dictated card, "Copied? Put the screen away."

## If the sheet never comes back

Sometimes the user returns to the chat and picks the task up with no scan — the sheet is half-done on a desk somewhere, or never met a printer. Follow their lead and keep working; an abandoned sheet is not a failure to prosecute, and progress on the task is never held hostage to the paper. Once, and only where a natural opening exists, offer two things in one short line: to work the sheet's questions here in the chat instead, and — if they're willing — one question about what didn't earn the pen: wrong questions, wrong moment, too much, too little. Whatever comes back is a field report (`references/evidence.md`, Part Three); note it and move on. Never ask twice.

## Anti-patterns

- Pre-filling creative zones with AI examples "to get them started" (this is design fixation, and it measurably reduces both fluency and variety)
- Printing a time limit, countdown, or suggested duration anywhere on a sheet
- Writing "try not to be influenced by the above" (discouraging instructions do not reduce fixation; only layout does)
- Putting generation and selection in the same zone
- Generating AI imagery for an ideation sheet (directly shown to raise fixation and lower originality)
- Encouragement microcopy, exclamation marks, or congratulating the human on a blank page
- Scoring matrices, weighted criteria, or rubrics on a selection zone (deliberative selection performs at chance; rubrics do not improve accuracy)
- Mentioning implementation, shipping, or building anywhere on a selection sheet
- Hard-to-read fonts, deliberate visual noise, or any manufactured difficulty in the typography
- Promising that a sheet will be quick or easy; effort is systematically misread as ineffectiveness, and minimizing it sets up the misread
- Presenting the serial disclosure kit as therapy, treatment, or clinical support, or asking for its private pages back (they print PRIVATE, they never return, and their absence is the design)
- Dense forms with tiny answer boxes (this is not a tax return)
- Deep provocations on a Light sheet, or busywork checkboxes on a Deep sheet
- More than one confirmation question before generating
- Continuing to work the problem on-screen after handing it to paper
- Guilt-tripping over an unreturned sheet, or asking about it twice
- Printing machine-readable context blocks the human has to look at (the human-readable header already carries what a cold reader needs)
- Asking whether the user has a printer (the card is reactive only; it is never proposed to anyone who has not said they cannot print)
- Dictating machine lists, proposals, or drafts for hand-copying (numbered handles only, and never on a page carrying a generative zone)
- Rendering the PDF anyway as a reference for someone who cannot print
- Expressing copy load in minutes rather than words
