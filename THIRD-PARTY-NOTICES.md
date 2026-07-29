# Third-Party Notices

This project distributes third-party material. Each item below keeps its own
license, which is not superseded by the repository's MIT license.

## IBM Plex

**What:** IBM Plex Sans, Serif, and Mono (8 TrueType files).

**Where:** `paper-session/assets/fonts/`, and inside the built
`paper-session.skill` bundle at the same path.

**Copyright:** © 2017 IBM Corp., with Reserved Font Name "Plex".

**License:** SIL Open Font License, Version 1.1. The full text ships alongside
the fonts at `paper-session/assets/fonts/LICENSE-IBMPlex.txt` so it travels
inside every built bundle, as the OFL requires.

**Upstream:** https://github.com/IBM/plex

### Two OFL obligations that apply if you fork this

1. **The license must accompany the fonts.** If you repackage, re-bundle, or
   redistribute the sheets' font files in any form, `LICENSE-IBMPlex.txt` has
   to go with them. `build.sh` includes it automatically; don't strip it.
2. **"Plex" is a Reserved Font Name.** If you modify the font files themselves,
   you must rename them. Note that this constrains *editing the fonts*, not
   setting type with them — generating PDFs is ordinary use and needs no
   renaming.

Selecting a different typeface for a fork is fine and requires no permission,
but `paper-session/references/design.md` specifies IBM Plex by name and by
register (`Sans`, `SansSB`, `SansB`, `Serif`, `SerifSB`, `SerifI`, `Mono`,
`MonoM`), so a substitution means editing that file rather than swapping files
in `assets/fonts/` and hoping.

## Code of Conduct

`CODE_OF_CONDUCT.md` is the Contributor Covenant, version 2.1, available at
https://www.contributor-covenant.org/version/2/1/code_of_conduct.html and
licensed CC BY 4.0.

## Research cited in the evidence brief

`paper-session/references/evidence.md` cites published research with links to
sources. Those papers are the property of their authors and publishers; the
brief paraphrases and summarizes findings and reproduces no substantial portion
of any paper.
