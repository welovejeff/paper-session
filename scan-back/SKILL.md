---
name: scan-back
description: "Ingest completed paper-session worksheets and resume the interrupted workflow. Use whenever the user uploads scans or photos of handwritten pages, PDFs from a phone scanning app, or images of filled-in worksheets, especially ones generated earlier by the paper-session skill. Trigger on uploads of handwritten pages even without any accompanying message, and on phrases like 'here's my worksheet', 'scanned it back', 'done thinking', 'here are my pages'. The job: read the handwriting, honor it as the authority, synthesize it into next steps, and continue the original work."
---

# Scan-Back

The return half of the paper loop. The user went off-screen with a printed artifact, did the thinking that was theirs to do, and is now handing the results back. Everything downstream of this moment should be built on what they wrote, not on what the AI previously proposed.

The session context normally lives in the current chat (or project context): the pages were designed by the `paper-session` skill earlier in this same conversation, so the original intent, the sheet structure, and the task being resumed are already known. Do not ask the user to re-explain a session the chat already holds.

**The orphan path.** Deep sessions come back days later, and scans realistically arrive in a fresh chat, a compacted context, or the phone app — anywhere the originating session is gone. Never bluff continuity. When the chat does not contain the session, reconstruct what the sheet itself carries: the header prints the title, date, and intent line; the footer prints capacity and page count; the zones name their own activities. Read all of it, state plainly what the pages cannot tell you, and ask exactly one re-anchoring question — the single thing synthesis genuinely needs, usually which task this unblocks or where the results should land. One question, then proceed. The intent line exists for this moment: `paper-session` writes it so a cold reader can resume from it.

## Step 1: Read the pages

Read every page visually and carefully. Pages sometimes arrive as a PDF annotated directly on a tablet rather than a photographed printout: treat the stylus layer exactly like pen ink, hue and all — the loop works, and paper simply remains the recommendation, since off-screen is the point. Phone scans arrive imperfect: uneven lighting, slight rotation, pages out of order within a multi-page PDF, occasionally a page photographed twice. Handle all of this silently; reorder pages by matching them to the sheet structure from earlier in the chat — or, on an orphaned scan, to the printed footer numbering — and never ask the user to rescan unless a page is genuinely unreadable.

Transcribe the handwriting faithfully:
- Capture everything: answers in the designated zones, margin notes, arrows, crossings-out, items circled or struck through, drawings, and anything written in the open territory. Margin scribbles and the free-association zone frequently contain the most valuable material; treat them as first-class input, not noise.
- Preserve the human's actual words. Do not paraphrase during transcription; polish comes later, if ever.
- Crossed-out text matters: it shows a considered-and-rejected path. Note it as rejected, not absent.
- If a word is truly illegible, mark it as [illegible] and infer nothing. Ask about it only if it sits somewhere consequential.
- Spatial arrangements are data. If cards were arranged and photographed, the order and grouping in the photo IS the answer. If items were placed on a 2x2, their positions are the rankings.

**The pen protocol.** The printed layer is always grayscale, so any chromatic ink is the human, and hue plus a small mark vocabulary carry intent. Resolve the active legend by this cascade, highest authority first: (1) a legend handwritten anywhere on the pages redefines its channels for the session; (2) the ink key printed on the sheet; (3) the defaults: black = general notes; red = needs review, stop, or delete (an explicit invitation to interrogate); green = approved, yes, move forward (execute, never relitigate); blue = an instruction to the AI, do this on return.

Default marks, any ink (ink modifies mark: a red strike is an emphatic kill): strikethrough = considered rejection; circle = elevate, this matters; ? = explain or expand on return; ! = priority; star = keep beyond this task, worth suggesting capture to the user's own systems; arrow = sequence or causation between the connected items; @name = route to that person, tool, or system; TLDR: = treat that line as the zone's headline answer.

Judge hue by cluster, not pixel: phone lighting shifts color, and blue vs. black is the common ambiguity. When ink is ambiguous, default to black (the lowest-stakes reading) unless content signals otherwise; ask only if the distinction would change the next step. A sheet in a single ink with no marks is fully valid: the protocol adds intent, its absence subtracts nothing. If the user has customized the legend in conversation, their definitions replace the defaults everywhere.

## Step 2: The authority rule

Where the human's handwriting conflicts with what the AI proposed earlier in the chat, the handwriting wins, silently and completely. If the AI proposed a priority order and the human re-ranked it, the re-ranking is now the priority order. Do not relitigate, do not note disappointment, do not "gently push back" on settled judgments. The entire architecture exists to put the human's judgment in charge; honor it.

Blank zones are also information: the human chose not to answer, ran out of time, or the prompt missed. Note blanks factually, without guilt-tripping.

## Step 3: The interrogation pass (before synthesis, held to a high bar)

Anything in the review channel (red by default) clears the bar automatically: it is the human explicitly requesting engagement, so respond to every such item with genuine pushback, stress-testing, or the review it asks for; where red marks a deletion, honor it as a kill, not a debate. Blue-channel instructions are not interrogation material: queue them as tasks to execute in the continuation. Beyond red, check for issues that would materially change the next steps. Surface something only if resolving it moves the work forward:

- **Consequential contradictions.** Two answers on the pages that cannot both be true, or a written answer that conflicts with a real constraint established earlier (a deadline, a budget, a dependency). Not stylistic tension; genuine conflict with downstream impact.
- **High-stakes blanks.** An unanswered prompt that the very next step depends on. Low-stakes blanks get noted, not chased.
- **Ambiguity at a fork.** Handwriting that legitimately reads two ways at a point where the two readings lead to different plans.

Cap it: at most 2-3 questions, asked once, together, plainly. If nothing clears the bar, ask nothing. Never generate commentary for its own sake, never audit the human's reasoning quality, never point out that they contradicted something from a previous month unless it changes what to do next.

## Step 4: Synthesize and continue

This is the default destination: synthesize and keep moving.

1. **Reflect back briefly** what the pages say: the decisions made, the rankings, the concepts generated, the surprises from the margins. Short; a compressed mirror, not a report. The human already knows what they wrote; this step just confirms it was read right.
2. **Fold it into the workflow.** Resume the original task with the paper results as ground truth: update the plan, re-order the roadmap, build on the chosen concept, draft the thing the session unblocked.
3. **Propose the next concrete step** and, where the task allows, just take it. The best version of this skill makes the scan feel like the workflow never paused; it just went quiet while the human thought.

If the pages contain material worth preserving beyond this task (a durable principle, a decision with long-term weight), note that it may be worth saving to the user's own systems, but do not lecture about it.

## Anti-patterns

- Treating margin notes or the open-territory zone as noise to skip
- Paraphrasing the human's words during transcription
- Relitigating a judgment the human settled on paper
- Asking the user to describe what they wrote instead of reading it
- Interrogation without consequence ("interesting that you ranked X low")
- A long transcription dump as the response; the transcription serves the synthesis, not the other way around
- Stalling at "here's what I read, what would you like to do?" when the original workflow makes the next step obvious
- Improvising the missing context on an orphaned scan instead of reconstructing from the printed header and asking the one re-anchoring question
