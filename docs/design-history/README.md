# Design history

**Nothing in this folder is live spec.** It's the record of how the Paper Session
design system was chosen, kept because the rejected options are part of the
argument for the one that shipped.

The live spec is [`paper-session/references/design.md`](../../paper-session/references/design.md).
If a file here disagrees with it, that file is wrong and the disagreement is the
point — these are earlier states of the design.

| File | What it is |
|---|---|
| `paper-session-design-prompt.md` | The brief the design work was commissioned with: three phases, hard constraints, and a requirement that the four directions be genuinely divergent rather than one layout in four typefaces. |
| `paper-session-design-brief.md` | Phase 2 output. Five principles stated as opinions you could disagree with, a tension map with a position on each tradeoff, and the typographic hypothesis that selected IBM Plex. |
| `0-Direction-Notes.md` | Phase 3 notes. Each direction's stance, its atomic inventory, and an honest paragraph on where it is weakest. |
| `1-Bureau.pdf` | Full Swiss discipline. Charm confined entirely to language. Risk: form-smell — with lazy microcopy it becomes a tax document. |
| `2-FieldKit.pdf` | Field Notes utilitarianism, dot grids throughout, everything labeled like equipment. Risk: prints the most ink of any direction and sits closest to the scan-legibility floor. |
| `3-MethodCard.pdf` | Card logic as the whole identity, dashed borders, corner registration ticks. Risk: on sheets nobody will cut, the cut-line promise is decoration. |
| `4-BasementShow.pdf` | Zine conviction on a disciplined grid. A 27pt masthead and a footer that talks like a bandmate. Risk: the masthead competes with the pen for loudest thing on the page. |
| `hybrid-specimen.pdf` | What shipped. |

All four directions render **identical content** so that design was the only
variable. That was deliberate and is worth preserving in any future round.

The shipped system is a hybrid rather than a winner: **Bureau chassis, Basement
voice dialed to about 60%, Field Kit's dot grid kept as an optional zone type for
sketch-inviting activities only, Method Card's cut lines only on sheets that will
actually be cut.** The instruction at the time was explicit that the four should
not be averaged into a safe middle, and the hybrid takes whole organs from each
rather than splitting differences.

The three PNGs in `docs/` are renders of `hybrid-specimen.pdf`, used by the
top-level README.
