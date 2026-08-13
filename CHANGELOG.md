# Changelog

Notable changes to the `paper-session` and `scan-back` skills. Because these
skills are prose specs rather than code, entries describe what changes about the
sheets a person receives, not internal refactors.

Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- **Brainwriting rounds**, the eighth named format and the first built for a
  table rather than one person. Three to six people, a sheet each, three ideas
  per round, then pass left — no timer, because the passing is triggered by
  finishing rather than by a clock, and the famous five-minute round was never
  isolated as the part that works. Every cell is lightly dot-gridded, so a
  sketch counts as an idea. Selection is exiled to a separate sheet after the
  rounds. Each sheet carries an optional `HAND:` box: fill it if you want a
  follow-up routed back to you, leave it blank if you'd rather the ideas stand
  on their own — nothing asks for a name, and ideas are never attributed to
  their authors either way.
- **The serial disclosure kit**, a seventh named format and the first with
  pages that never come back. Three sittings on consecutive days, then a
  closing distillation page — the only one that returns. The disclosure pages
  print `PRIVATE — THIS PAGE STAYS WITH YOU. IT IS NOT SCANNED.` and
  `scan-back` never requests them, never asks about them, and never reads
  their absence as a blank. Adapted from expressive-writing research with its
  mixed record stated rather than buried: the dose is converted from minutes
  to one full page because nothing prints a clock, and that conversion is
  labeled this project's own untested hypothesis. Offered for work friction
  and professional setbacks only, never as therapy, with the exclusions named
  and the expected short-term mood dip disclosed instead of hidden.
- **The loop works without a printer.** Say you can't print and the same
  session arrives as a short card to copy into any notebook: the prompts and
  the structure, never the machine's lists — those stay in the chat, and a
  hand-copied handle never lands on a page where you're supposed to be
  generating. Light sessions get offered in conversation instead. `scan-back`
  reads a page with no printed layer: your copied scaffold is structure, not
  answers, and with every stroke in one hand the marks carry the intent that
  ink used to. The skill never asks whether you have a printer, and never
  mentions what you're not getting. Design and rationale in
  [`research/0002`](research/0002-no-printer-notebook-brief.md).

## [0.2.0] — 2026-08-12

### Added
- **Six named session formats.** The pattern library gains whole-session kits
  chosen by name — after-action review, premortem, outside view, teach-back,
  weekly review, and the Grinnell field kit (the first multi-day series) —
  each grounded in its own evidence cluster with limitations and
  contraindications stated plainly.
- Both skills can now be installed with one command —
  `npx skills add welovejeff/paper-session` — via the
  [skills CLI](https://github.com/vercel-labs/skills). Nothing about the
  sheets themselves changed.
- **The orphan path.** A scan that returns to a chat that no longer holds the
  session gets reconstructed instead of improvised: `scan-back` reads the
  printed header, says plainly what the pages can't tell it, and asks exactly
  one re-anchoring question before resuming. To make that work, the header's
  intent line is now written so a cold reader could resume the session from it
  alone — it is the loop's only stateless carrier. Sheets still print no QR
  codes, session IDs, or machine-readable context blocks.
- **The sheet that never comes back.** When the user resumes the task with no
  scan, the skill follows their lead without comment, and — once, never twice —
  may offer to work the sheet's questions in the chat instead, plus one
  optional question about what didn't earn the pen. Answers land as field
  reports. Guilt-tripping over an unreturned sheet is now an explicit
  anti-pattern.
- **Tablet round trip, honestly second-best.** A PDF annotated with a stylus
  comes back like any scan: the stylus layer reads exactly like pen ink, hue
  and all. Paper stays the recommendation — off-screen is the point.

### Changed
- **Marks first, hue second.** The pen protocol now states its hierarchy: the
  mark is the primary carrier of intent and ink hue a redundant amplifier, so
  everything that must survive the trip home reads in one black ballpoint. The
  four-ink protocol is the enhancement, not the requirement.
- **Two reading fixes on the return trip.** An ambiguous dark-ink line written
  as an instruction gets confirmed instead of silently downgraded to a note,
  and a degraded capture (heavy blur, shadow banding, rotation) earns one
  retake request even when the text seems readable — on a bad capture,
  apparent readability is not accuracy.
- **The machine stopped talking about itself in the third person.** Zone
  captions are now first person and name what was actually done — **I PROPOSE**
  over the machine's column (or I GATHERED, I MAPPED, I LOGGED), **YOU DECIDE**
  over yours. "THE MACHINE SAYS" is retired. Provenance is unchanged: the "I"
  caption plus Mono type still make the machine's contribution unmistakable.

## [0.1.0] — 2026-07-29

First public version of the loop. Everything below is in the initial commit.

### Added
- **`paper-session`** — recognizes when a task has reached human judgment work,
  picks a Deep (2–4 page) or Light (1 page) capacity, composes sheets from the
  pattern library, generates a verified PDF, and then stops.
- **`scan-back`** — reads photographed pages, transcribes handwriting
  faithfully, treats the pen as authoritative over anything the AI proposed
  earlier, holds an interrogation pass to a high bar, and resumes the original
  work.
- **The pen protocol.** Ink hue and a small mark vocabulary carry intent on the
  return trip, with a three-level authority cascade: a handwritten legend beats
  the printed ink key, which beats the defaults. Entirely optional per session.
- **Design system** (`references/design.md`): US Letter, grayscale, nothing
  meaningful below 50% gray, three unblended voices (Serif asks, Mono is the
  machine, tracked Sans caps is infrastructure, pen is the human), specified to
  exact point sizes so any sheet can be built without seeing a specimen.
- **Pattern library** (`references/page-patterns.md`): defixation, generative,
  weighing and selection, sketch, Light, introspection, and field patterns.
- **Prompt craft** (`references/prompt-craft.md`): how to word what goes on the
  page, including why discouraging instructions don't reduce fixation and
  categories beat instances.
- **Evidence brief** (`references/evidence.md`): sourcing for every rule, plus
  an explicit account of what the research does *not* support — no study tests
  this artifact, and every claim is assembled from adjacent literatures.
- `scripts/verify_layout.py`, the mandatory pre-flight check for overlapping
  text and text escaping the page.
- Design history in `docs/design-history/`: the commissioning prompt, the Phase 2
  brief, and four divergent candidate directions (Bureau, Field Kit, Method
  Card, Basement Show) rendered with identical content so design was the only
  variable. The shipped system is a hybrid — Bureau chassis, Basement voice at
  60%, Field Kit's dot grid as an optional zone type, Method Card's cut lines
  only where cutting is real.
- Repository laid out so the unpacked `paper-session/` and `scan-back/`
  directories are the source and the `.skill` bundles are artifacts built by
  `./build.sh`, with CI enforcing that the two stay in step. MIT license, SIL
  OFL text shipped alongside the fonts, contributor guide, code of conduct, and
  issue templates — including a session report, since sheet completion rate is
  the project's missing metric.
