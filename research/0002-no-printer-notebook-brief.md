Status: Implemented
Date: 2026-08-12
Outcome: PR #7 — implementation of this brief

# No-printer notebook fallback

## Scope

How `paper-session` and `scan-back` should serve a user who cannot print:
whether the loop survives without the printed artifact, in what form, and
what each skill must change. It decides no printed rule — see `evidence.md`.

## Sources

- A three-designer adversarial panel (minimal / full / skeptic) plus a judge
  synthesis, commissioned 2026-08-12 for this brief; this brief is the record.
- Local files: both `SKILL.md`s and their anti-pattern lists, the
  `paper-session/references/` set, and `CLAUDE.md`'s invariants and couplings.

## Findings

1. **Minimal**: a hidden capability — one recognition rule, then a dictated
   copy-down brief transcribed into any notebook: numbered handles, a hard
   copy budget, the chat-held brief as scan-back's answer key. Its governing
   insight sets the voice: the notebook is natively what the design system
   labors to produce — a mostly-empty page where the pen is the
   highest-contrast element — so the mode never apologizes.
2. **Full**: a second first-class output target with its own
   `references/notebook.md` translation table and MACHINE-caption voice
   convention. Rejected as a mode — the reference wants to become a second
   design system, and advertisement invites printer-owners to cannibalize the
   designed artifact. Two organs kept: copy load in words, never minutes;
   "number all lines BEFORE writing anything" replacing slot-count gravity.
3. **Skeptic**: the printed artifact IS the AI's contribution —
   provenance-by-typography, defixation-by-layout — and naive hand-copying
   deep-encodes what the fixation evidence says should be glanced at and
   left. Its frame wins: reactive-only trigger, triage, a pattern gate,
   floor-not-peer framing, Light handed to chat.
4. **The judge's synthesis** — skeptic's frame, minimal's mechanics, full's two
   organs — is the plan of record:
   - **Trigger is reactive only** — the user states they cannot print, in any
     phrasing, before or after a PDF exists; after, the skill regenerates as
     a brief without comment and never suggests finding a printer. Never
     asked about proactively; "never have a printer" earns one offer to
     remember the default. The triage may point tablet-plus-stylus owners at
     annotating the PDF directly — scan-back already reads a stylus layer.
   - **The output is a setup card** — one fenced monospace chat message (the
     machine stays Mono on screen), two strictly separated parts. COPY THIS
     (hard budget: ~50–75 handwritten words Deep, one phone screen Light):
     title and intent line verbatim — now the loop's only anchor — corner page
     numbers, one prompt per page. DO THIS is read, never copied: structure as
     pen gestures, plus an optional self-written pen legend at cascade rung 1.
   - **Machine content crosses only as numbered handles**, ≤4 words, under a
     hand-copied THE MACHINE SAYS caption, on reaction/selection pages —
     never one carrying a generative zone; hand-copying is deeper exposure
     than glancing. Full items stay in chat for scan-back to expand. At most
     one inline machine line, in quotation marks — quotes are the notebook's
     Mono. Over budget means too print-shaped: simplify, don't dictate more.
   - **Light defaults to chat.** Three gut calls get offered in the
     conversation, without guilt; a one-screen Light brief only on request.
   - **scan-back gains one Step 1 subsection**: unprinted pages are valid
     returns; the chat-held brief is the answer key; transcription is not
     endorsement (the copied scaffold carries no intent — only marks on it
     do); all ink is the human's — dominant ink is the default channel, hue
     semantics need two or more inks; the cascade collapses to handwritten
     legend > defaults; a struck-as-written category block matching the brief
     is a spent fence, not kills; corner numbers order pages; orphans anchor
     on the handwritten header, one re-anchoring question unchanged.
   - Patterns that don't translate (reaction margins, cutting a bound
     notebook) are substituted, never faked.
5. **This creates a third unshared cross-skill coupling** — the brief
   conventions written by paper-session and read by scan-back — alongside the
   pen protocol and the footer promise. `CLAUDE.md` must name it.

## Options

The three proposals in findings 1–3 are the options. None ships pure; the
synthesis in finding 4 is the recommendation.

## Risks / unknowns to validate

This list is the implementation PR's test plan.

1. **Copy abandonment.** Does anyone transcribe and return pages; is 50–75
   words too tight for a real Deep session, or more than humans will copy.
2. **Handle fidelity.** Do people copy the numbered handles; do their
   abbreviations stay matchable against the chat-held brief; how often do
   returns arrive orphaned, where the answer-key diff is impossible.
3. **Unprinted-page scan accuracy.** The real round trip: copy a generated
   brief into an actual notebook, fill it in pen, photograph it in bad light,
   hand it to scan-back. Does strike-as-written read as a fence, not kills.
4. **Light chat-handoff reception.** Respectful triage, or the skill
   declining to serve — do any Light users want the brief when offered.
5. **The third unsynced coupling.** Do the conventions (handles, THE MACHINE
   SAYS, quotes-as-Mono, strike-as-written, corner numbers) hold across two
   skills with no shared file.
6. **Single-ink blue ambiguity.** Does the dominant-ink rule swallow a
   genuine blue instruction on a page written entirely in blue.

## Recommendation

Ship the synthesis in one PR touching: `paper-session/SKILL.md` (a ~12–15-line
branch in Step 4; Step 5 explicitly N/A for briefs, replaced by the budget
check; the Step 6 close "Copied? Put the screen away. Go think."; the
frontmatter phrase "works without a printer — say so"; three new anti-pattern
lines), `references/prompt-craft.md` (new "Dictating instead of printing"
section, from which SKILL.md condenses — the one-way dependency holds),
`references/page-patterns.md` (a short "Notebook translation" gate),
`references/evidence.md` (appended entry: no study tests dictated scaffolds;
hand-copying-as-encoding stays a flagged hypothesis; the grayscale rationale
does not transfer to unprinted pages), `scan-back/SKILL.md` (the "Unprinted
pages" subsection plus one anti-pattern line; frontmatter untouched),
`CLAUDE.md` (name the coupling), `README.md` (two lines, framed as the
floor), `CHANGELOG.md` (one entry), and both `.skill` bundles via
`./build.sh`. Validation runs the round trip in unknown 3 before this header
flips.

Explicitly not built: a `references/notebook.md` or any second design system;
any edit to `references/design.md`; a proactive printer question or
in-session advertisement; rendering the PDF anyway as a reference; dictating
machine lists, proposals, or drafts verbatim, or handles on generative pages;
copy load in minutes; a brief-linter in v1; invented substitutes for patterns
that don't translate; any user-facing claim that hand-copying deepens
engagement; promotion to a co-equal mode or alternative output formats;
loosening scan-back's trigger; QR codes, session IDs, or machine-readable
anchors on the notebook side.

## Validation — 2026-08-12, implementation PR

Everything above this line is the brief as accepted. This section records what
shipped and what the flagged unknowns still owe.

### What was implemented

The synthesis in finding 4, across the files the recommendation names:
`paper-session/SKILL.md` (the Step 4 branch, the budget check standing in for
Step 5, the Step 6 close, the frontmatter phrase, three anti-pattern lines),
`paper-session/references/prompt-craft.md` (the "Dictating instead of printing"
section SKILL.md condenses from), `paper-session/references/page-patterns.md`
(the notebook-translation gate), `paper-session/references/evidence.md` (a
closing Part Two entry, "The unprinted page"), `scan-back/SKILL.md` (the
"Unprinted pages" subsection and one anti-pattern line), `CLAUDE.md` (the
setup-card coupling named), `README.md`, `CHANGELOG.md`, and both `.skill`
bundles via
`./build.sh`. Nothing on the not-built list was built.

### Nothing on the risk list was validated

The brief promised the round trip in unknown 3 would run before this header
flipped. It did not run, and the header flipped anyway. The reason: **none of
the six unknowns can be answered in the environment that implements them.**
Every one of them terminates in a person — someone who cannot print, copying a
generated card into their own notebook, filling it in pen, and sending the
pages back.

1. **Copy abandonment.** Needs a real user deciding whether 50–75 words is
   worth writing out, and a real Deep session to test the budget against.
   Unmeasured.
2. **Handle fidelity.** Needs real abbreviations from a real hand, diffed
   against a real chat-held brief, and a count of how many returns arrive
   orphaned. Unmeasured.
3. **Unprinted-page scan accuracy.** Needs a photographed notebook page. No
   round trip was run, so whether strike-as-written reads as a spent fence
   rather than kills is untested — the single unknown the brief said would
   gate this flip.
4. **Light chat-handoff reception.** Needs Light users who were offered the
   work in conversation and either took it or asked for the brief anyway.
   Unmeasured.
5. **The third unshared coupling.** The conventions were written into both
   skills in this PR, but authoring them consistently on one day is not
   evidence that they survive a real return or the next edit to either file.
6. **Single-ink blue ambiguity.** Needs a page written entirely in blue. The
   dominant-ink rule ships as specified, unverified.

All six are field questions. `paper-session/references/evidence.md` Part Three
(field reports) is where their answers land, in that tier's format: date,
capacity, patterns used, what came back or where it stopped, and anything the
scan-back pass misread. The threshold there already governs what happens next —
three independent reports agreeing on the same failure justify a pattern-review
issue. Until entries accumulate, the notebook fallback ships as a reasoned
design with no completion data behind it, which is the standing the printed
sheets have too: Part Three is still empty.

### Correction: the caption the card dictates

The Findings above say the handles sit under a hand-copied `THE MACHINE SAYS`
caption. That is wrong, and it was wrong when written: the panel that produced
this brief ran before the caption change, and the brief inherited a name the
design system had already retired. The card dictates `I PROPOSE`, the same
first-person caption the printed sheets carry, and `scan-back` reads that
caption as the provenance mark. The body above is left as written per the
append-only rule; the implementation ships the corrected caption.
