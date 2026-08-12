# Changelog

Notable changes to the `paper-session` and `scan-back` skills. Because these
skills are prose specs rather than code, entries describe what changes about the
sheets a person receives, not internal refactors.

Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
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
