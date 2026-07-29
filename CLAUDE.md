# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Not an application. This repo authors **two paired Claude skills** distributed as `.skill` bundles:

- **`paper-session`** — pauses on-screen AI work and generates a printable PDF worksheet (reportlab) so the human does the judgment/creative work with a pen, off-screen.
- **`scan-back`** — ingests photos/scans of the completed pages, transcribes the handwriting, treats it as authoritative, and resumes the interrupted workflow.

They form one loop: screen → paper → pen → scan → screen. The product thesis: in agentic workflows the bottleneck is human metabolism of AI output, not AI output. Everything in the repo exists to make the paper half of that loop good enough that people actually complete it.

A `.skill` file is just a zip whose single top-level directory is the skill name (`paper-session/SKILL.md`, `paper-session/references/…`, `scripts/`, `assets/fonts/`). There is no compiler, no test suite, no package manager.

## Layout

```
paper-session/          # SOURCE: SKILL.md, references/, scripts/, assets/fonts/ (IBM Plex + OFL)
scan-back/              # SOURCE: SKILL.md only
build.sh                # zips both into .skill bundles
paper-session.skill     # BUILD ARTIFACT, committed for install-without-clone
scan-back.skill         # BUILD ARTIFACT
docs/sheet-*.png        # specimen renders used by README
docs/design-history/    # frozen record of how the design system was chosen
```

**The unpacked directories are authoritative; the `.skill` files are generated.** Never hand-edit a bundle and never leave a source edit unbuilt — run `./build.sh`, which also fails if a `SKILL.md` `name:` doesn't match its directory or if the fonts would ship without their license.

This layout was adopted after the loose root copies of the reference docs drifted from the bundled ones. Do not reintroduce duplicate copies of a reference doc anywhere in the tree.

`docs/design-history/` (the commissioning prompt, Phase 2 brief, `0-Direction-Notes.md`, four direction PDFs, `hybrid-specimen.pdf`) is a record of how the system was chosen, not live spec. `paper-session/references/design.md` won and is the single source of truth for visual language; the four direction PDFs are deliberate dead ends kept for the argument.

## Commands

```bash
pip install -r requirements.txt          # reportlab + pdfplumber

./build.sh                               # repackage both bundles after editing source
./build.sh scan-back                     # or just one

ln -s "$PWD/paper-session" ~/.claude/skills/paper-session   # live-edit without rebuilding
ln -s "$PWD/scan-back"     ~/.claude/skills/scan-back

python3 paper-session/scripts/verify_layout.py sheet.pdf    # mandatory before showing a sheet
```

`reportlab` 5.0.0 is present on this machine; `pdfplumber` (required by `verify_layout.py`) is not — install it before generating anything, or the mandatory verification step cannot run. If pip is externally managed here, add `--break-system-packages`.

`verify_layout.py` catches exactly two defects — overlapping words and text escaping the page bounds — because those survive casual inspection and ruin a sheet at the printer. It is deliberately narrow; it does not check the design system.

Regenerating the README specimen images (only if a specimen changes):

```bash
pdftoppm -png -r 110 docs/design-history/hybrid-specimen.pdf docs/tmp && sips -Z 1000 docs/tmp*.png
```

## The three-layer document architecture

`SKILL.md` is procedure only: recognize the moment → pick capacity → design → generate → verify → stop. It delegates every judgment call to a reference and stays short enough to be read at load time.

- `references/page-patterns.md` — the activity pattern library (what zones exist). Choose 1–3 per session.
- `references/prompt-craft.md` — how to word what goes on the page.
- `references/design.md` — the visual system, specified to exact point sizes, gray values, and rule weights so a sheet can be built from it without seeing a specimen.
- `references/evidence.md` — the research every rule traces back to, with an explicit "what this does NOT support" section.

The dependency runs one way: `SKILL.md` → references → `evidence.md`. **A new rule in a reference needs a source in `evidence.md`, and adding a rule to `SKILL.md` means condensing it from a reference rather than inventing it there.** Rules in `SKILL.md` are compressed restatements; if you change a rule, change it in both places or the skill will contradict its own reference mid-session.

## Cross-skill coupling to keep in sync

The **pen protocol** (ink = intent: black notes / red review / green go / blue do; marks: strike, circle, `?`, `!`, star, arrow, `@name`, `TLDR:`) is specified twice — `paper-session/references/design.md` §9 (which prints the ink key) and `scan-back/SKILL.md` Step 1 (which reads it back). Both state the same authority cascade: handwritten legend > printed ink key > defaults. There is no shared file. **Any change to the protocol must be made in both skills**, or the sheet will print a key that scan-back does not honor.

`paper-session` also promises `scan-back` by name in its footer ("SCAN IT BACK TO CONTINUE.") and its closing message. `scan-back` in turn assumes the session lives in the same chat, which is why sheets deliberately print **no** QR codes, session IDs, or machine-readable context blocks.

## Invariants any change must respect

These are load-bearing, not style preferences. Violating one breaks the premise rather than making an uglier sheet.

- **Whose thought does this slot belong to?** AI contributes only where it has done work worth reacting to (a proposed order, gathered options, one remote analogy). Where the human excels, print the provocation and leave the space empty. Pre-filling a creative zone is design fixation — the most replicated finding behind this skill — and it measurably lowers both fluency and variety. When in doubt, withhold.
- **Constrain the input, never the clock.** No time limit, countdown, or suggested duration anywhere on a sheet. Time pressure is the specific trigger for shallow processing, and the creativity benefit of input constraints only holds in its absence.
- **Categories, not instances.** Marking common ground as abstract categories roughly doubles creative output; naming specifics and saying "avoid these" *increases* fixation. Never write "try not to be influenced by the above" — discouraging instructions do nothing, layout does the work.
- **Generation and selection never share a zone.** Selection zones get a named criterion, a distance frame, a feasibility counterweight, and no rubric or scoring matrix; never mention shipping or building on one.
- **Difficulty lives in the task, never in the typography.** Legibility is never traded for effort.
- **Grayscale only, nothing meaningful below 50% gray, no fills or images.** The color channel is reserved entirely for the human's pen, which is what makes the pen protocol readable on the return trip.
- **The pen must be the highest-contrast thing on the finished page**, ≥50% of every page is space for it, pages decompress downward, and open territory closes every sheet.
- **Deep ≤4 pages, Light exactly 1.** Every Deep kit contains at least one dot-grid sketch zone (drawing beats prose on recall and loose marks fight fixation). Light sheets ask only for marks achievable in one pen gesture.
- **Stop when the sheet is handed over.** After presenting the PDF, do not keep working the task or produce the answers the sheet asks for. "Printed. Go think."

Both `SKILL.md` files end with an anti-pattern list. Read it before adding a feature — most tempting additions ("just a few examples to get them started", "a suggested 5 min", a scoring rubric) are already explicitly banned there with the reason.

## Working on this project

Sheets are generated programmatically (reportlab, or HTML-to-PDF) with no per-sheet manual design — that constraint is inherited from the design prompt and is why `design.md` is specified numerically. IBM Plex is bundled in `assets/fonts/` and registered under exact names (`Sans`, `SansSB`, `SansB`, `Serif`, `SerifSB`, `SerifI`, `Mono`, `MonoM`); the three-voice rule maps to them and must not be blended — Serif asks, Mono is the machine, tracked Sans caps is infrastructure, and nothing printed ever imitates handwriting.

`SKILL.md` Step 4 references `/mnt/skills/public/pdf/SKILL.md` for reportlab mechanics. That path exists in the Claude environment where the skill runs, not on this machine.

The evidence base is honest about being assembled from adjacent literatures — no study tests this artifact. When extending the system, prefer adding to `evidence.md` (with the limitation stated) over asserting a rule in `SKILL.md` on intuition. This is an open-source project intended to grow the surface for "do human things" work in agentic thought work; the research grounding is the moat, so keep it auditable.

This is a public repository. `CONTRIBUTING.md` states the bar for outside changes (a rule that alters what gets printed needs a source in `evidence.md`); keep it in step with anything that changes how contributions are reviewed. `CHANGELOG.md` describes what changes about the sheets a person receives, not internal refactors. `CODE_OF_CONDUCT.md` still carries a placeholder where the reporting contact belongs — the maintainer has to fill that in, and no PR should quietly substitute a personal email address.
