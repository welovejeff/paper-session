<!--
Source of truth is the unpacked paper-session/ and scan-back/ directories.
Never hand-edit a .skill file; run ./build.sh and commit the regenerated bundles.
-->

## What changes for the human?

<!-- What does someone holding the sheet do differently? If the answer is
"nothing, but the code is cleaner," say that — it'll be reviewed as a refactor,
which is a perfectly good PR. -->

## Type of change

- [ ] Changes what gets printed on a sheet
- [ ] Changes how `scan-back` reads a page
- [ ] Prose, docs, or tooling only — no change to what a sheet asks of a human
- [ ] Removes or weakens an existing rule

## Evidence

<!-- Required if this changes what gets printed. Cite the source and note its
limitations. Removing or weakening a rule needs less evidence than adding one.
Delete this section for prose/tooling PRs. -->

## Checklist

- [ ] Edited the unpacked source, not a `.skill` bundle
- [ ] Ran `./build.sh` and committed the regenerated bundles
- [ ] `python3 paper-session/scripts/verify_layout.py` passes on any sheet this affects
- [ ] If a rule changed in a reference, checked whether `SKILL.md` restates it and updated both
- [ ] If the pen protocol changed, updated **both** `paper-session/references/design.md` §9 and `scan-back/SKILL.md` Step 1
- [ ] Read the anti-pattern list at the end of the relevant `SKILL.md`

## Printed and filled it in

<!-- For anything that changes a sheet's appearance: print it in grayscale on
cheap paper, fill it in with a pen, photograph it in imperfect light, hand it to
scan-back. Attach the photo. Screen review has missed print and scan defects
before. Delete this section if the change can't affect a printed page. -->

- [ ] Printed it, filled it in, and scanned it back
- [ ] Not applicable
