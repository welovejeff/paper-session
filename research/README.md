# Research briefs

**How a capability gets added to this repo: research first, then an
implementation PR that answers to the research.**

This folder holds one numbered brief per proposed capability — a distribution
channel, a build change, a verification tool, a restructuring. The brief is
written before any implementation lands; after that, its body is append-only
and its header changes only when its status does — in the common case exactly
once, when the implementation ships. The result is an auditable trail from
question to shipped change, at the cost of one file and a header edit.

## What belongs here, and what doesn't

This folder is for changes to the **project around the skills**: how they are
distributed, built, verified, or maintained.

It is not a second home for research about **what gets printed on a sheet**.
That evidence lives in
[`paper-session/references/evidence.md`](../paper-session/references/evidence.md)
and nowhere else. A brief whose recommendation would change a printed rule must
still land its sources in `evidence.md` — the brief may cite them, never
replace them.

Two other records this folder is not:

- [`docs/design-history/`](../docs/design-history/) — the frozen record of how
  the design system was chosen. Nothing new goes there.
- [`CHANGELOG.md`](../CHANGELOG.md) — what changes about the sheets a person
  receives. A brief's implementation may earn an entry there; the brief itself
  doesn't.

Not everything needs a brief. A typo fix, a faster verifier, a small tooling
tweak: just open the PR. Write a brief when being wrong is expensive — a new
way people get the skills, a layout change, a policy the repo will have to live
with.

## The lifecycle

1. **Research.** Open a brief as `research/NNNN-slug.md` — next number,
   zero-padded, never reused, gaps allowed — with `Status: Draft`. State the
   scope, the sources, the findings, the options, and a recommendation. The
   most valuable section is **risks / unknowns to validate**: name what you
   could not confirm, because that list becomes the implementation PR's test
   plan. Merging the brief to `main` means **Accepted** — the recommendation is
   now the plan of record.

2. **Validate.** The implementation PR's first job is to test the brief's
   flagged unknowns before building on them. Findings go in a dated
   **Validation** section appended to the brief — including everything the
   brief got wrong. Corrections are appended, never edited in; the original
   text stays as written, because the record of what we believed before testing
   is part of the argument.

3. **Implement.** The same PR makes the change, appends the validation, and
   flips the header: `Status: Implemented`, `Outcome:` the change itself. Doing
   all three in one PR makes the merge commit the link between decision and
   change — no tracking issue to maintain, nothing to forget.

4. **Reject or supersede.** If validation kills the recommendation, flip
   `Status: Rejected` and say why in the appendix. Rejected briefs are kept for
   the same reason `docs/design-history/` ships four rejected directions: the
   dead ends are part of the argument. A later brief that reverses an
   implemented one takes a new number, and the two point at each other
   (`Superseded-by:` / a `Supersedes:` line).

## The file format

Every brief opens with this header and nothing above it:

```
Status: Draft | Accepted | Implemented | Rejected | Superseded
Date: YYYY-MM-DD          ← of the last status change
Outcome: —                ← the implementing PR or commit, once there is one
```

Add `Superseded-by: NNNN` only when it is true. No author field — `git log`
answers that.

After acceptance, only the header and appended sections change. The body of an
accepted brief is append-only.

The body has no rigid template. What a useful brief contains: **Scope** (the
question, stated narrowly), **Sources**, **Findings** (numbered, so validation
can refer to them), **Options** if there are real ones, **Risks / unknowns to
validate**, and a **Recommendation** small enough to implement in one PR.

## Why this shape

The format is compressed from the processes that large projects use for the
same job — ADRs, Rust RFCs, Python PEPs, Kubernetes KEPs — with everything
removed that exists to coordinate many parties: no comment periods, no
sponsors, no index file, no separate tracking issues. Numbered filenames give
each decision a citable handle (`research/0001`) and cannot race with a single
maintainer. The one distinction every mature process grew independently is kept
here: **Accepted and Implemented are different states**, because "we decided"
and "it shipped" diverge, and bridging that gap is what this folder is for.
