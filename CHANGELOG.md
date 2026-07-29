# Changelog

Notable changes to the `paper-session` and `scan-back` skills. Because these
skills are prose specs rather than code, entries describe what changes about the
sheets a person receives, not internal refactors.

Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- Repository restructured for public release: the unpacked `paper-session/` and
  `scan-back/` directories are now the authoritative source, with `.skill`
  bundles built by `./build.sh`. Previously four reference documents existed
  both loose at the repo root and inside the zip, and they had drifted.
- Reconciled `references/design.md`: the loose root copy was missing the
  mandatory dot-grid sketch zone for Deep kits and the no-printed-time-limit
  rule. The bundled version was correct and is now the only version.

### Added
- MIT license, third-party notices, and the SIL OFL text shipped alongside the
  IBM Plex fonts so it travels inside every built bundle.
- `build.sh`, which fails the build if a `SKILL.md` name doesn't match its
  directory or if the fonts would ship without their license.
- Contributor guide, code of conduct, and issue templates — including a session
  report template, since sheet completion rate is the project's missing metric.

## [0.1.0] — 2026-07-29

First working version of the loop.

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
