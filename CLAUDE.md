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
build.sh                # zips both into .skill bundles, and concatenates the paste artifact
paper-session.skill     # BUILD ARTIFACT, committed for install-without-clone
scan-back.skill         # BUILD ARTIFACT
paper-session-paste.md  # BUILD ARTIFACT, the paste channel for hosts with no skills runtime
skills.sh.json          # skills-CLI grouping metadata: the two halves offered as one loop
docs/sheet-*.png        # specimen renders used by README
docs/specimen.py, .pdf  # the current specimen: generator + verified build the PNGs render from
docs/design-history/    # frozen record of how the design system was chosen
research/               # numbered research briefs behind capability changes
```

The root-level position of `paper-session/` and `scan-back/` is load-bearing beyond tidiness: `npx skills add welovejeff/paper-session` (documented in README §Install) discovers skills by checking each immediate root-level directory for a `SKILL.md`. Moving either directory deeper silently breaks the one-command install path.

Install directions live in README §Install **only**, alongside a per-agent compatibility ledger that states honest loop status (verified end-to-end on Claude surfaces; installs-but-untested elsewhere). Both install tracks matter equally — the chat-app upload path (`.skill` bundles) and the CLI path — so never let an edit favor one and orphan the other. Other documents link to that section rather than restating commands; that single-source rule is what keeps the directions in sync.

**The unpacked directories are authoritative; the `.skill` files and `paper-session-paste.md` are generated.** Never hand-edit a bundle or the paste artifact, and never leave a source edit unbuilt — run `./build.sh`. It refuses four mistakes: a `SKILL.md` whose `name:` doesn't match its directory, a bundle carrying the IBM Plex fonts without their license, a cross-skill coupling literal that has fallen out of one side (a presence gate only — it catches a deletion, never a semantic desync), and a face that does not carry the weight its name promises — a variable font, a duplicated PostScript name, or three Sans files sharing one set of outlines, each of which prints a voice at the wrong weight and none of which look wrong on screen. A run that includes `paper-session` also regenerates `paper-session-paste.md`, because all three of its sources live in that directory; `./build.sh scan-back` on its own leaves it alone.

This layout was adopted after the loose root copies of the reference docs drifted from the bundled ones. Do not reintroduce duplicate copies of a reference doc anywhere in the tree.

`paper-session-paste.md` is not an exception to that ban; it is the case the ban does not reach. The rule is anti-drift, not anti-copy, and that file is concatenated from its three sources by `build.sh` on every run and diffed against them byte for byte in CI, so it cannot drift out of step — which is also why it is generated rather than written. `paper-session/requirements.txt` is a second copy with no such gate: it duplicates the root `requirements.txt` so that an install which never cloned the repo can install what it runs on, and nothing in `build.sh` or CI compares the two. Change one and change the other in the same edit, by hand.

`docs/design-history/` (the commissioning prompt, Phase 2 brief, `0-Direction-Notes.md`, four direction PDFs, `hybrid-specimen.pdf`) is a record of how the system was chosen, not live spec. `paper-session/references/design.md` won and is the single source of truth for visual language; the four direction PDFs are deliberate dead ends kept for the argument.

`research/` holds the repo's process for capability changes (distribution, build, verification, layout — the project around the skills, never rules about what gets printed, which belong in `evidence.md`): a numbered brief (`NNNN-slug.md`, statuses Draft → Accepted → Implemented / Rejected / Superseded) is researched and merged first, then the implementation PR tests the brief's flagged unknowns, appends a dated Validation section, and flips the header in the same PR. Accepted brief bodies are append-only — corrections go in the appendix, never edited in. The process itself is specified in `research/README.md`; follow it when adding any new capability to this repo.

## Commands

```bash
python3 -m pip install -r requirements.txt          # reportlab + pdfplumber

./build.sh                               # repackage both bundles, and the paste artifact
./build.sh scan-back                     # or just one
./build.sh --check-fonts                 # the font-weight guard alone, building nothing
./build.sh --check-couplings             # the cross-skill presence gates alone

ln -sfn "$PWD/paper-session" ~/.claude/skills/paper-session   # live-edit without rebuilding
ln -sfn "$PWD/scan-back"     ~/.claude/skills/scan-back

python3 paper-session/scripts/verify_layout.py sheet.pdf    # mandatory before showing a sheet
```

`build.sh` needs `zip`, `unzip`, and `python3` on PATH — `python3` because the font-weight guard is a stdlib script rather than a dependency. It checks all three before writing anything, since discovering one missing after the first bundle is rewritten leaves the tree half-built.

Generating sheets needs `reportlab`; `verify_layout.py` needs `pdfplumber`. Check with `python3 -c 'import reportlab, pdfplumber'` rather than assuming either way — if the import fails, install from `requirements.txt` before generating anything, adding `--break-system-packages` where pip is externally managed. Never skip the verification step on the grounds that a dependency is missing; install it.

`verify_layout.py` catches text escaping the page bounds, collisions across different baselines (word level), and collisions on a shared baseline (character level — pdfplumber merges same-line overlapping glyphs into one word, so that case is invisible to the word pass and has its own check). It is deliberately narrow; it does not check the design system.

Regenerating the README specimen images (only if the spec changes):

```bash
python3 docs/specimen.py    # rebuilds docs/specimen.pdf, verifies it, regenerates docs/sheet-*.png
```

The PNG rendering step needs two packages beyond `requirements.txt`: `python3 -m pip install pymupdf pillow`. The script fails with a clear message if they're missing; the PDF build and verify gate need only `requirements.txt`.

## The three-layer document architecture

`SKILL.md` is procedure only: recognize the moment → pick capacity → design → generate → verify → stop. It delegates every judgment call to a reference and stays short enough to be read at load time.

- `references/page-patterns.md` — the activity pattern library (what zones exist). Choose 1–3 per session.
- `references/prompt-craft.md` — how to word what goes on the page.
- `references/design.md` — the visual system, specified to exact point sizes, gray values, and rule weights so a sheet can be built from it without seeing a specimen.
- `references/evidence.md` — the research every rule traces back to, with an explicit "what this does NOT support" section.

The dependency runs one way: `SKILL.md` → references → `evidence.md`. **A new rule in a reference needs a source in `evidence.md`, and adding a rule to `SKILL.md` means condensing it from a reference rather than inventing it there.** Rules in `SKILL.md` are compressed restatements; if you change a rule, change it in both places or the skill will contradict its own reference mid-session.

## Cross-skill coupling to keep in sync

The **pen protocol** (ink = intent: black notes / red review / green go / blue do; marks: strike, circle, `?`, `!`, star, arrow, `@name`, `TLDR:`) is specified twice — `paper-session/references/design.md` §9 (which prints the ink key) and `scan-back/SKILL.md` Step 1 (which reads it back). Both state the same authority cascade: handwritten legend > printed ink key > defaults. There is no shared file. **Any change to the protocol must be made in both skills**, or the sheet will print a key that scan-back does not honor.

The **setup-card conventions** are a second coupling of the same kind, added with the no-printer path (`research/0002`) and widened to the unreadable-page path (`research/0005`). The card is dictated on two triggers, never one — the user says they cannot print, or that they cannot read the printed sheet — and neither question is ever asked of them; the card is the session in linear text, which is what both cases need. Its conventions: the card's `I PROPOSE` caption and quotation marks mark machine content in the human's handwriting, a struck-as-written category block is a Spent Ground fence rather than a set of kills, and corner numbers replace the printed footer numbering. `paper-session/references/prompt-craft.md` §10 writes those conventions and `scan-back/SKILL.md` Step 1 ("Unprinted pages") reads them back, again with no shared file. **A change to either must be made in both**, and note the cascade differs on an unprinted page — legend > defaults, since no printed key exists to sit between them.

`paper-session` also promises `scan-back` by name in its footer ("SCAN IT BACK TO CONTINUE.") and its closing message. `scan-back` prefers the same chat and, when a scan arrives orphaned (fresh chat, compacted context), reconstructs from the printed header and asks exactly one re-anchoring question — which is why the header's intent line is written for a cold reader (`paper-session/references/prompt-craft.md` §6, restated in `paper-session/SKILL.md` Step 3 and `scan-back/SKILL.md`), and why sheets still deliberately print **no** QR codes, session IDs, or machine-readable context blocks.

## Invariants any change must respect

These are load-bearing, not style preferences. Violating one breaks the premise rather than making an uglier sheet.

- **Whose thought does this slot belong to?** AI contributes only where it has done work worth reacting to (a proposed order, gathered options, one remote analogy). Where the human excels, print the provocation and leave the space empty. Pre-filling a creative zone is design fixation — the most replicated finding behind this skill — and it measurably lowers both fluency and variety. When in doubt, withhold.
- **Constrain the input, never the clock.** No time limit, countdown, or suggested duration anywhere on a sheet. Time pressure is the specific trigger for shallow processing, and the creativity benefit of input constraints only holds in its absence.
- **Categories, not instances.** Marking common ground as abstract categories roughly doubles creative output; naming specifics and saying "avoid these" *increases* fixation. Never write "try not to be influenced by the above" — discouraging instructions do nothing, layout does the work.
- **Generation and selection never share a zone.** Selection zones get a named criterion, a distance frame, a feasibility counterweight, and no rubric or scoring matrix; never mention shipping or building on one.
- **Difficulty lives in the task, never in the typography.** Legibility is never traded for effort.
- **Grayscale only, nothing meaningful below 50% gray, no fills or images.** The color channel is reserved entirely for the human's pen, which is what makes the pen protocol readable on the return trip.
- **The pen must be the highest-contrast thing on the finished page**, ≥50% of every page is space for it, pages decompress downward, and open territory closes every sheet.
- **Deep ≤4 pages, Light exactly 1.** The cap counts per human, because what it protects is one person's completion load: the Grinnell field kit reads it per kit rather than per project, and brainwriting rounds reads it per participant, so a six-person session is one page pattern printed six times, not a six-page kit. Every Deep kit contains at least one dot-grid sketch zone (drawing beats prose on recall and loose marks fight fixation); where the sketch cannot be worked — a dictated session worked without sight of a page, and only that — the kit carries the prompt the drawing was there to ask, and nothing takes the drawing's place. A sighted copyist still gets the sketch field. That is a scoping, not a substitution: `evidence.md` names sketching as the largest single loss on that path and licenses no stand-in activity. Light sheets ask only for marks achievable in one pen gesture.
- **Stop when the sheet is handed over.** After presenting the PDF, do not keep working the task or produce the answers the sheet asks for. "Printed. Go think."

Both `SKILL.md` files end with an anti-pattern list. Read it before adding a feature — most tempting additions ("just a few examples to get them started", "a suggested 5 min", a scoring rubric) are already explicitly banned there with the reason.

## Working on this project

Sheets are generated programmatically (reportlab, or HTML-to-PDF) with no per-sheet manual design — that constraint is inherited from the design prompt and is why `design.md` is specified numerically. IBM Plex is bundled in `assets/fonts/` and registered under exact names (`Sans`, `SansSB`, `SansB`, `Serif`, `SerifSB`, `SerifI`, `Mono`, `MonoM`); the three-voice rule maps to them and must not be blended — Serif asks, Mono is the machine, tracked Sans caps is infrastructure, and nothing printed ever imitates handwriting.

`SKILL.md` Step 4 references `/mnt/skills/public/pdf/SKILL.md` for reportlab mechanics. That path exists in the Claude environment where the skill runs, not on this machine.

The evidence base is honest about being assembled from adjacent literatures — no study tests this artifact. When extending the system, prefer adding to `evidence.md` (with the limitation stated) over asserting a rule in `SKILL.md` on intuition. This is an open-source project intended to grow the surface for "do human things" work in agentic thought work; the research grounding is the moat, so keep it auditable.

This is a public repository. `CONTRIBUTING.md` states the bar for outside changes (a rule that alters what gets printed needs a source in `evidence.md`); keep it in step with anything that changes how contributions are reviewed. `CHANGELOG.md` describes what changes about the sheets a person receives, not internal refactors. `CODE_OF_CONDUCT.md` still carries a placeholder where the reporting contact belongs — the maintainer has to fill that in, and no PR should quietly substitute a personal email address.
