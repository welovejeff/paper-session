Status: Implemented
Date: 2026-08-28
Outcome: the `onramps` PR — `build.sh` emits `paper-session-paste.md`, CI checks it against source, and README §Install carries the paste channel and its ledger row

# The paste channel (chat AI with no skills runtime)

## Scope

Whether this repository can serve the users whose AI is a chat product with no
Agent Skills runtime — ChatGPT, Gemini, Copilot chat, Perplexity, Le Chat,
DeepSeek, Grok, Poe — in what form, and what has to be built. It is a
distribution question. It decides no printed rule; see `evidence.md`.

## Sources

- Local files, read and measured on this tree, 2026-08-28: `README.md`
  §Install and its ledger, `build.sh`, `.github/workflows/verify.yml`,
  `paper-session/SKILL.md`, `paper-session/references/prompt-craft.md`,
  `paper-session/references/page-patterns.md`,
  `paper-session/references/design.md`,
  `paper-session/references/evidence.md`, `scan-back/SKILL.md`, `CLAUDE.md`,
  `CHANGELOG.md`, `research/README.md`.
- `research/0001` (what the CLI track does and does not reach) and
  `research/0002` (the setup-card path this brief routes into).
- `research/0004`, `0005`, and `0006`, read for the sequencing dependency
  named at the end of this brief.
- Every byte and word count below was taken with `wc` and `python3` against
  these files on that date, not estimated.

## Findings

1. **Every documented install route is unusable on these surfaces, and the
   ledger already says so by omission.** README §Install offers three routes,
   not two — upload a `.skill` bundle, `npx skills add`, and the "**No
   Node?**" clone-and-unzip block (`README.md:65-71`) — and all three
   terminate in a runtime that discovers a `SKILL.md`. The compatibility
   ledger has four rows, and its catch-all reads "**Anything else that reads
   `SKILL.md` folders**". A product that reads no such folder is excluded by
   construction rather than by oversight. (Runtime support is a moving target,
   and the list of named surfaces above is a snapshot taken on the date in
   Sources: re-check each one at implementation time rather than trusting it.
   That caution is this brief's own. 0001's unknown #1 is not a precedent for
   it — it reads "Live registry/discovery behavior can change quickly; verify
   commands against the latest `vercel-labs/skills` README before release
   messaging", which is about the CLI's command surface and registry, not
   about whether a chat product supports Agent Skills.)

2. **The return half already works there and needs nothing built.**
   `scan-back/SKILL.md` is one file, 17,481 bytes and 2,932 words, and it
   references no script, no reference document, no font, and no Python — the
   grep for `references/`, `scripts/`, `reportlab`, `pdfplumber`, and `.py`
   returns nothing. It is already a paste. Only the forward half is blocked,
   which is why this brief is about one artifact and not two.

3. **The forward half has exactly one branch that needs neither `reportlab`
   nor the verify gate: the setup card.** `prompt-craft.md` §10 ("Dictating
   instead of printing") specifies a card the human copies into a notebook,
   and `SKILL.md` Step 4 closes its card branch with "Step 5 does not apply to
   a card; the budget count is the gate." That single line is what makes the
   card path safe to hand to a host that cannot run `pdfplumber`: the gate it
   would be skipping does not exist on that path, so nothing is being waived.
   §10 also supplies the register — "A notebook is natively what this design
   system labors to produce" — so the channel does not have to apologize for
   what it cannot render.

4. **Three documents are sufficient, and their size is measured, not
   guessed.** `SKILL.md` (16,180 bytes / 2,606 words) carries the procedure,
   the seven compressed rules, and the Step 4 card branch;
   `prompt-craft.md` (15,847 / 2,551) carries §10 in full plus the wording
   rules; `page-patterns.md` (27,696 / 4,394) carries the pattern library and
   its "Notebook translation" gate, which is the section that decides which
   patterns survive a hand copy. Concatenated as they stand: **59,723 bytes,
   9,551 words, 385 lines**. The one deletion Option A′ makes — `SKILL.md`'s
   YAML frontmatter block and the blank line after it, 1,115 bytes and 170
   words — brings the shipped body to **58,608 bytes, 9,381 words, 380
   lines**, roughly 15,000 tokens at the conventional four-bytes-per-token
   approximation (no tokenizer was available on this machine; treat the token
   figure as an approximation and the byte and word figures as exact). With
   the 1,503-byte preamble specified below, the shipped artifact is **60,111
   bytes and 9,618 words**.

5. **`evidence.md` stays out, and the anti-pattern lists plus `prompt-craft`
   carry the load.** It is 76,480 bytes and 10,615 words — larger than the
   other three combined: all four are 136,203 bytes and 20,166 words, so
   including it would more than double the paste for the layer that is *least*
   operative at generation time. The dependency runs one way (`SKILL.md` →
   references → `evidence.md`), and what a host actually has to obey is
   already stated as rules upstream: `SKILL.md`'s seven numbered rules, its 22
   anti-pattern bullets, `scan-back`'s 9, and `prompt-craft.md`'s own promise
   in its line 3, the second paragraph — "the short justification is kept with
   each rule so it can be reasoned about rather than followed blindly." A
   pasted host is
   following rules, not adding them, and "what this does NOT support" is
   written for someone deciding whether a new rule is licensed. Leaving the
   largest, least-operative file out is also the only way to preserve the
   *shape* of progressive disclosure once the runtime that implements it is
   gone.

6. **`design.md` stays out for a different reason.** It is a typographic spec
   — point sizes, gray values, rule weights — for a PDF that cannot be
   produced on these surfaces. Pasting 15,676 bytes of it invites the host to
   render a "sheet" as a markdown table or ASCII layout, which is the failure
   mode the card format exists to avoid.

7. **Leaving `design.md` out opens one real seam: the ink key.** The canonical
   pen protocol is `design.md` §9, and the only restatement that travels in
   the paste is incidental — one clause inside `page-patterns.md`'s weekly
   review entry ("strike kills, green go, blue do, red review"). §10's DO THIS
   asks the host to offer a pen legend, and on an unprinted page the cascade
   is handwritten legend > defaults, so the defaults matter. The reading side
   is intact: `scan-back/SKILL.md` Step 1 states the protocol, and a
   paste-channel user pastes that file anyway for the return trip. **The fix
   is not a third copy.** `CLAUDE.md` specifies the protocol in exactly two
   places on purpose and bans duplicate copies of a reference doc; adding a
   restatement to `prompt-craft.md` would create a third thing to keep in
   sync. Whether a host dictates a usable legend without `design.md` is
   unknown #6.

8. **Byte-faithfulness is the whole engineering argument.** A mechanical
   concatenation can be checked against its sources the way the `.skill`
   bundles already are — `verify.yml`'s `bundles-match-source` job unzips each
   bundle and `diff -r`s it against the source tree, on the stated grounds
   that "if someone hand-edits a bundle, or edits the source and forgets
   `./build.sh`, the two drift apart and installed users get something nobody
   reviewed." A paste artifact emitted by a deterministic build step inherits
   that check exactly: whether the step is `cat a b c` or `awk … | cat b c`,
   the artifact is still a pure function of the sources, and the check is
   still a diff. Anything hand-written is not, and cannot be (see Options).

9. **A pure `cat` does not produce a clean document, and one of the two
   reasons is not cosmetic.** All three sources end with exactly one newline
   (checked), so no separators are needed and no two documents run together.
   But `paper-session/SKILL.md` does not open with its H1. It opens with a
   1,114-byte YAML frontmatter block, and `# Paper Session` is line 6. Two
   things follow. Cosmetically, in a concatenation the opening `---` reads as
   a thematic break and the closing `---` reads as a setext underline for the
   `name:` and `description:` lines above it, so those two render as one
   enormous H2 in any CommonMark renderer — the description value alone is
   1,070 bytes. Substantively — and this is the cost that
   matters — the highest-weighted position in the pasted file is then runtime
   trigger metadata addressed to a loader that is not present, whose first
   substantive clause is "Generates a printable PDF worksheet (reportlab)".
   That is the opposite of where the instruction line has to route the host,
   and it sits above it in the same message. Deleting that block is the one
   transformation this brief adopts; see Option A′. With the block gone every
   document in the paste opens on its own H1, and the simple version of this
   finding — a clean concatenation needing no separators — becomes true.

   **A second problem survives the deletion and cannot be filtered.** The
   pasted text issues live orders against documents the paste omits.
   `SKILL.md:87`: "Read `references/design.md` and implement it exactly."
   `page-patterns.md:103`: the PRIVATE marker "is specified in design.md §9;
   print it exactly." Counted across the three files, `design.md` is named 3
   times and `evidence.md` 6, with 8 further "Sources: evidence brief"
   citations, plus `/mnt/skills/public/pdf/SKILL.md` and
   `scripts/verify_layout.py`. Stripping those would mean rewriting source
   prose, which is the fourth-layer failure Option B is rejected for. The
   preamble has to name them as dead pointers instead, and it must not claim
   flatly that everything needed is stated below while the text below orders
   the host to go read a file that is not there. The preamble specified in the
   Recommendation spends a paragraph on exactly this.

10. **This strains two invariants and the brief has to say so. First, the
    duplicate-copy ban.** `CLAUDE.md`:
    "Do not reintroduce duplicate copies of a reference doc anywhere in the
    tree" — adopted after loose root copies drifted from the bundled ones. A
    root-level file containing all of `SKILL.md`, `prompt-craft.md`, and
    `page-patterns.md` is, on its face, that. The defense is that the ban is
    anti-drift, not anti-copy: `paper-session.skill` (1.29 MB) is already a
    committed root-level copy of the entire source tree, exempt because it is
    generated and CI-enforced. The paste artifact has the same standing only
    if it gets the same enforcement, which is why finding 8 is a requirement
    rather than a nicety. `CLAUDE.md`'s layout block must name the artifact so
    the exemption is written down rather than inferred.

    **Second, the install single-source rule, and this one is not fully
    discharged.** `CLAUDE.md` puts install directions in README §Install
    "only", and `README.md:85` restates it: "so there is exactly one place to
    keep true." It is tempting to claim compliance because the preamble
    carries a link and no commands, but for this track the instruction line
    *is* the install procedure, it lives inside the artifact, and the
    Recommendation also has README quote it. That is a hand-maintained
    duplicate of a load-bearing string, created by a brief whose central
    argument is that hand-maintained duplicates drift — and `git diff` catches
    the artifact drifting from `build.sh` while nothing catches README
    drifting from the artifact. The exposure is real and the fix is cheap: the
    string is a fixed literal, so CI can compare the two copies byte for byte,
    which is the technique this brief already relies on and not a prose grep.
    The Recommendation's `verify.yml` section specifies that check.

11. **What the channel does not promise, stated plainly.** (a) A pasted
    protocol has **no authority over the host's system prompt**; it is user
    text, and a host tuned to be maximally helpful may pre-fill a generative
    zone or volunteer a duration in spite of 22 anti-pattern bullets telling
    it not to. (b) The user gets a **card, not a PDF** — no typography, no
    grayscale channel, no printed ink key. (c) There is **no verify gate**,
    though per finding 3 the card path never had one. (d) `evidence.md`'s
    unprinted-page entry already governs the honesty here: "**No study tests a
    dictated scaffold or a hand-copied AI worksheet**", and Cluster 10
    "predicts transcription as the loop's most likely abandonment point, and
    predicts that the people who finish it will rate it poorly." The paste
    channel routes more people onto exactly that path. It adds no new
    evidentiary claim and is owed no new source; it raises the stakes on an
    admitted one.

## Options

**A. A build-time, mechanically concatenated, byte-faithful paste** — the
three files in reading order behind a generated preamble whose last line is a
sentinel, with no transformation of any kind. Sound, and rejected only in
favor of A′, which is A plus one deletion.

**A′. The same, with exactly one mechanical, source-derived deletion:
`SKILL.md`'s anchor-delimited YAML frontmatter block. Recommended.** Finding 9
is the reason. The distinction that matters is not verbatim-versus-not; it is
**rewritten by a human** versus **filtered by the build**, and this brief's
own reasoning separates those two everywhere else. A build-time filter is not
a fourth authored layer: it is deterministic, it regenerates from source on
every build, it holds no prose of its own, and it is checkable by exactly the
technique that carries A — a diff of the committed artifact against the
pipeline's output, `awk … | cat … | diff` in place of `cat … | diff`. It
therefore inherits the whole anti-drift argument of finding 8 without
inheriting any of Option B's. The price is that "verbatim" becomes "verbatim
apart from one named deletion", which the preamble states and CI enforces.

The filter is capped at one rule, deliberately: an anchor-delimited block at
the very top of one named file, removed whole. It touches no prose, makes no
judgment about content, and is described in the artifact itself. **A second
transformation is out of scope for this brief** — the next one that looks
tempting (stripping the dangling `design.md` and `evidence.md` pointers,
finding 9's second half) is prose editing wearing a filter's clothes, and it
is on the not-built list below.

**B. A hand-written condensed forward prompt.** Rejected, on three grounds.
First, it is a **fourth document layer** under a contract `CLAUDE.md` states
as strictly one-way: rules are authored in a reference, sourced in
`evidence.md`, and condensed into `SKILL.md` — "adding a rule to `SKILL.md`
means condensing it from a reference rather than inventing it there", and "if
you change a rule, change it in both places or the skill will contradict its
own reference mid-session." A condensed paste prompt is a second, parallel
condensation of the same references, with no defined position in that chain
and a third place for every rule change to be forgotten. Second, this repo has
already run this experiment: the current layout "was adopted after the loose
root copies of the reference docs drifted from the bundled ones." Third, its
only proposed safeguard — a prose check in `build.sh` or CI — is the exact
technique `verify.yml` documents as unworkable, in its own words: "Those are
semantic rules, and a prose grep cannot distinguish stating a rule from
breaking it — the first attempt at this tripped on the very line forbidding
time limits." What condensation would buy is a smaller paste; at 60,111 bytes
the artifact is already inside the context of every current model behind the
named products, and the constraint that actually bites is the input box, not
the window (unknown #1). A permanently drifting layer is too high a price for
bytes.

**C. Host the text and tell the user to have the model fetch a URL.**
Rejected: browsing is off, unreliable, or paywalled across these surfaces, and
it makes the forward half depend on a network fetch the user cannot debug. The
paste is the one capability all eight demonstrably have.

**D. Do nothing.** Rejected: this is the largest population the project
excludes, the return half already works for them today, and the forward half
needs a file, not a feature.

**E. One combined paste, all four documents in a single file.** Rejected, and
worth recording because it looks like a free win — 77,592 bytes, one copy step
for the user instead of two. It is rejected for the same reason `SKILL.md` Step 6
exists: the forward half's job is to hand over and stop. A host holding
`scan-back/SKILL.md` in the same message is holding Step 1 transcription
instructions for pages that do not exist yet, and the failure mode is a host
that narrates the return trip, or worse, invents its content. The return paste
is also the one that has to work in a *different* chat — `scan-back`'s orphan
path exists because scans come back to a context that no longer holds the
session — so binding it to the forward message is the wrong coupling as well
as the wrong timing.

## Risks / unknowns to validate

This list is the implementation PR's test plan.

1. **The paste ceiling, per surface.** Paste the artifact into each named
   product as one message and record what happens: accepted as text,
   truncated, or silently converted to an attachment — and whether the model
   then acts on it. The probe must test the *tail*, since `page-patterns.md`
   is last, and it must key on something that appears **only** in the tail.
   The obvious probe fails that test: "what is the one restriction on machine
   handles in a notebook?" is answered from `page-patterns.md:111`, but the
   same rule is stated in `paper-session/SKILL.md:94` and
   `prompt-craft.md:115`, so a host that received only the first document
   passes it. Use instead: **"Which two patterns do not translate to a
   notebook at all?"** The answer — reaction margins and cut-apart cards — is
   stated only in `page-patterns.md:127-130`, the final section of the final
   document; both patterns are described earlier in that same file, but
   nothing outside those four lines says they do not translate. A host that
   names both received the tail. If a surface caps the paste, the documented
   split is on document boundaries only — 16,568 / 15,847 / 27,696 bytes,
   three messages worst case, never mid-document (the first figure is the
   1,503-byte preamble plus the 15,065-byte frontmatter-stripped `SKILL.md`).
2. **Fidelity of the card against a real runtime.** Run one identical Deep
   brief on each surface and against `paper-session` installed in Claude Code,
   then diff the cards on four mechanical checks: COPY THIS word count inside
   50-75, every handle four words or fewer, the `I PROPOSE` caption present as
   a literal, and no handle on a page carrying a generative zone. The brief
   must be **one fixed string, identical across every run, and recorded
   verbatim in the Validation section** — otherwise the runs are not
   comparable and a second person cannot repeat them. Use a task the library
   has a clear route for and that is not one of the named session formats, so
   the host has to choose patterns rather than recall a kit: *"I'm
   re-sequencing an eight-session studio course; session eight lands flat and
   I don't know whether the problem is session eight or session three. I
   can't print."*
3. **Whether the host obeys the bright lines it has no reason to.** On the
   same runs, count violations of three anti-patterns: a dictated time limit
   or suggested duration, a pre-filled generative zone, any scoring rubric.
   This is finding 11(a) measured rather than asserted. **Threshold, so the
   ledger row is not written from an impression:** five runs per surface with
   the unknown-2 brief, counting each of the three violation types
   independently. Zero violations across five runs is a clean row; one or two
   total is a row that names the violation; three or more, or any violation
   type appearing in a majority of runs, is a row that says the surface does
   not reliably hold the lines. A public ledger row is the output either way —
   a failing surface is documented, never quietly shipped and never quietly
   dropped.
4. **Photo reading, per surface.** Photograph one filled notebook page under
   warm indoor light carrying black, blue, red, and green marks, a strike, a
   circle, an arrow, and a marginal note whose *position* carries the meaning.
   Paste `scan-back/SKILL.md`, attach the photo, ask for the Step 1 read, and
   score three things: hue attributed correctly per mark, strike distinguished
   from circle, and spatial arrangement (which zone or column a mark sits in)
   recovered rather than flattened to a list. **Pass conditions**, one per
   score, since "recovered" needs a definition: every mark's ink named
   correctly with no cross-assignment between blue and black; strike and
   circle reported as different operations on their targets, not both as
   "marked"; and the spatial score passes only if the read names the zone or
   column each mark sits in *and* the marginal note is attached to the line it
   sits beside rather than appended as a free-floating item. A read that
   returns a flat bulleted list of transcribed strings fails the third score
   however accurate the strings are. Blue and black are both on the page
   deliberately — `evidence.md` Cluster 11 has them as the least separable
   pair in a phone photo.
5. **ChatGPT's Python tool.** Run `import reportlab, pdfplumber` in a code
   interpreter session; on `ImportError`, attempt `pip install reportlab
   pdfplumber` and record whether it fails on network isolation. Record the
   answer either way. **A positive result does not unlock the print path in
   this PR**: the eight IBM Plex TTFs are 2.4 MB of binary and cannot travel
   through a paste, so a PDF built there would fall back to Helvetica and
   break `design.md`'s font spec. If the tool has both libraries, the
   follow-on — uploaded fonts plus `design.md`, a genuine print path on a
   non-skills surface — is a later brief, not this one.
6. **The ink-key seam (finding 7).** Ask a paste-only host to produce the card
   for a session whose pages want two inks, and check whether the legend it
   offers matches the protocol `scan-back` will read back. If it does not, the
   answer is a coupling decision, not a patch to the artifact.
7. **The artifact does not disturb the other two tracks.** 0001's validation
   established, and confirmed in the CLI's own `src/skills.ts`, that discovery
   walks *immediate* root-level subdirectories for a `SKILL.md`, so a
   root-level markdown file should be invisible to it — but "should" is why
   this is on the list. The check must run against a tree that actually
   contains the artifact, which `main` does not until this merges, so
   `npx skills add welovejeff/paper-session --list` in its plain form tests
   the wrong tree and cannot gate anything. Run it in a form that resolves to
   the PR branch or to a local checkout; which forms the CLI accepts for that
   is itself part of what this unknown tests. **If no pre-merge form resolves,
   #7 leaves the merge gate** and becomes a post-merge confirmation with a
   one-line rollback (delete the artifact, rebuild, commit), which is
   proportionate given the mechanism is already source-confirmed.
8. **Whether the §10 branch actually fires from a pasted instruction line.**
   Unknowns 2 and 3 both presuppose a card was produced; nothing above scores
   whether the host takes the card fork at all. The trigger in `SKILL.md:89`
   and `prompt-craft.md:102` is the *user* saying they cannot print, "in any
   phrasing" — so a host reading §10 literally could decide that a sentence
   about the host's own PDF capability is not that trigger, and the path it
   falls back to is Steps 4-5, which is the ASCII-sheet failure mode finding 6
   excludes `design.md` to avoid. The instruction line below is written to
   close that — it asserts both facts, the user's and the host's — but the
   test is what settles it. Score three cases per surface: the line pasted
   exactly; the line paraphrased ("no printer here, and you can't give me a
   PDF anyway"); and the line omitted entirely, the user saying only what they
   are working on. Record for each whether the host produced a card, a PDF
   attempt, or a rendered pseudo-sheet in the chat. The third case is the
   realistic one and the one whose answer decides whether the README needs to
   say the sentence is not optional.

## Recommendation

Ship option A′ in one PR.

**The artifact.** `paper-session-paste.md`, at the repository root, committed
like the `.skill` bundles and for the same reason — a chat-app user with no
terminal has to be able to open one raw link and copy the file. Lowercase, so
it sits with the build artifacts rather than with the ALL-CAPS documents.

**The preamble**, emitted verbatim by `build.sh` (1,503 bytes; its last line
is the sentinel, and the CI check below keys on that literal line rather than
on a byte offset):

```
<!-- paper-session paste channel — generated by build.sh from repository source; do not edit -->

Paste this whole file into the chat. Then say what you are working on, and add this sentence: "I can't print, and you can't make a PDF here, so dictate the setup card for me to copy by hand — there is nothing to annotate."

This is the `paper-session` skill for chat products that cannot install skills. It is three documents from https://github.com/welovejeff/paper-session#install, in reading order: `SKILL.md`, then `references/prompt-craft.md`, then `references/page-patterns.md`. They are copied byte for byte with exactly one deletion: `SKILL.md`'s YAML frontmatter block, which is install metadata addressed to a runtime that is not here.

Two source documents are deliberately absent: `references/design.md`, a typographic spec for a PDF that cannot be produced here, and `references/evidence.md`, the sourcing layer. The text below still points at both, and at `scripts/verify_layout.py` and a PDF skill path. Those pointers are dead here and are not instructions to you: the card path produces no PDF and has no verify gate, and every rule that governs a card is stated in full below. Follow the rules; ignore the file paths.

The return half of the loop is a second paste: `scan-back/SKILL.md`, one file, into the same chat when the photographed pages come back.

<!-- source begins; everything below this line is generated from the three files above and is checked byte for byte in CI -->
```

The fourth paragraph is not politeness. Finding 9 established that the pasted
text orders the host to read `design.md` and `evidence.md`, files the paste
omits on purpose; a preamble that claimed everything needed was stated below,
full stop, would be falsifiable from inside the artifact in under a minute.
Naming the dead pointers is the honest form and is also the one that keeps a
host from inventing a substitute for the spec it was told to read.

The instruction line earns each of its clauses. "I can't print" *is* the §10
trigger, in the user's own voice: §10 fires on the user saying they cannot
print, in any wording, and never on the skill asking, and a sentence that only
asserted something about the host's capability leaves a literal reader room to
decide the trigger never fired — which drops it back onto Steps 4-5 and the
ASCII-sheet failure mode. "And you can't make a PDF here" then forecloses the
host trying anyway. "So dictate the setup card for me to copy by hand" names
the output, so the host does not invent a substitute artifact. "There is
nothing to annotate" forecloses §10's first fork, which points a
tablet-and-stylus owner at annotating the PDF directly — correct advice
everywhere except here, where no PDF can exist. The line is addressed to the
human but is read by the model on paste, which is the point of putting it
inside the file rather than only in the README. Whether it fires, including
when the user paraphrases or forgets it, is unknown #8.

**`build.sh`** gains a step that runs after the bundle loop: verify all three
sources exist and fail loudly by name if one does not (same shape as the
existing `SKILL.md` name check), write the preamble from a quoted heredoc,
append the body, and print one summary line in the existing format (`built
paper-session-paste.md — 3 documents, N bytes`). No new tool dependency; `cat`,
`awk`, and a heredoc.

The body is emitted by one function, and that function is the *only* place the
transformation exists:

```bash
paste_body() {
  # SKILL.md's YAML frontmatter is install metadata for a runtime the paste
  # channel does not have, and it would sit above the instruction line as the
  # first thing the host reads. Drop the block and the blank line after it;
  # nothing else is touched, here or in the other two files.
  awk 'NR==1 && $0=="---" { infm=1; next }
       infm && $0=="---"  { infm=0; gap=1; next }
       gap  && $0==""     { gap=0;  next }
       !infm              { gap=0; print }' paper-session/SKILL.md
  cat paper-session/references/prompt-craft.md \
      paper-session/references/page-patterns.md
}
```

**On partial runs.** `./build.sh scan-back` and `./build.sh paper-session` are
both documented in `CLAUDE.md`, so "every full run" is not a sufficient rule —
editing `prompt-craft.md` and running `./build.sh paper-session` would refresh
the bundle and leave the paste stale on disk, to be discovered only in CI.
All three sources live under `paper-session/`, so: **a run that includes
`paper-session` regenerates the paste; `./build.sh scan-back` alone does
not.** It costs nothing and removes the trap.

`build.sh` also gains a `--paste-body` mode that writes `paste_body` to stdout
and exits without touching any file. It exists so CI can check the committed
artifact against the current sources without holding a second copy of the awk
— a duplicated mechanism being the exact thing this brief argues against.

**`verify.yml`** gains three steps in the existing `bundles-match-source` job,
which is already the place where "committed artifact matches source" is
enforced. **Step order is load-bearing**: the content check must be placed
*before* the existing `build.sh reproduces the bundles cleanly` step. That step
runs `./build.sh`, which rewrites `paper-session-paste.md` on disk; a content
check placed after it would compare the artifact CI just built against the
sources CI just built it from and could never fail. The existing bundle check
is ordered ahead of `./build.sh` for the same reason.

```yaml
- name: The paste artifact's body is exactly what build.sh emits
  run: |
    ./build.sh --paste-body > /tmp/paste-body
    sed -n '/^<!-- source begins;/,$p' paper-session-paste.md | tail -n +2 \
      > /tmp/committed-body
    diff /tmp/committed-body /tmp/paste-body \
      || { echo "::error::paper-session-paste.md does not match source — run ./build.sh and commit"; exit 1; }
    test -s /tmp/committed-body \
      || { echo "::error::paper-session-paste.md has no sentinel line"; exit 1; }

- name: The instruction line is identical in the artifact and README
  run: |
    line=$(grep -o 'I can.t print, and you can.t make a PDF here[^"]*' paper-session-paste.md | head -1)
    test -n "$line" || { echo "::error::instruction line missing from the artifact"; exit 1; }
    grep -qF "$line" README.md \
      || { echo "::error::README quotes a different instruction line than the artifact ships"; exit 1; }
```

The extraction keys on the **sentinel line itself**, not on a byte count of
the freshly built body. That is deliberate: it makes the sentinel load-bearing
rather than decorative, and it makes the failure legible — a missing or
renamed sentinel fails with its own message instead of silently shifting the
comparison window. The second step is finding 10's second strain: a fixed
literal compared byte for byte across two files, which is the technique
`verify.yml` trusts, not the prose grep it rejects.

Freshness is the third addition, appended to the existing `build.sh reproduces
the bundles cleanly` step:

```bash
git ls-files --error-unmatch paper-session-paste.md
git diff --exit-code -- paper-session-paste.md
```

Both lines are needed. `git diff --exit-code` catches a stale committed
artifact — a changed preamble, say, which the content check does not look at —
but it reports nothing at all for a file that was generated and never
`git add`ed, and an untracked artifact is exactly the state a hurried
maintainer leaves behind. `git ls-files --error-unmatch` fails on that case by
name. Together with the content check the artifact has the same standing the
bundles have: faithfulness, freshness, and existence, all mechanical.

**`README.md` §Install** gets the download link, the instruction line quoted
once, and a fifth ledger row: *Chat AI with no skills runtime — ChatGPT,
Gemini, Copilot chat, Perplexity, Le Chat, DeepSeek, Grok, Poe* / *paste
`paper-session-paste.md`, then `scan-back/SKILL.md`* / status written from
unknowns 1-4 and 8, and honest by default until they resolve: a hand-copied
card, no PDF, no verify gate, untested per surface. The row must note that
Copilot appears twice in the ledger in two different forms — the CLI-routable
IDE agent in row three, the chat surface here. Install directions stay in that
section only, per the single-source rule; the artifact's preamble carries a
link to it and no commands. The instruction line is the one string that
genuinely lives in two places — it is the install procedure for this track and
it has to ship inside the artifact the host reads — so it is quoted in README
byte for byte and CI compares the two copies (finding 10, second strain).

**`CLAUDE.md`** gets `paper-session-paste.md` in the layout block, marked
BUILD ARTIFACT alongside the `.skill` files, plus the one sentence finding 10
requires: the duplicate-copy ban is anti-drift, and this copy is exempt
because CI proves it cannot drift.

**One `CHANGELOG.md` entry, in 0001's form.** The changelog "describes what
changes about the sheets a person receives", and nothing about any sheet or
card changes here. That reads at first like a reason to add nothing, and 0001
— the other pure distribution brief — shows it is not: `CHANGELOG.md:52-55`,
under `## [0.2.0] — 2026-08-12`, announces the CLI install and closes
"Nothing about the sheets themselves changed." That is a pure-distribution
entry which goes out of its way to say no sheet changed, which is exactly this
brief's situation, and `research/README.md` allows it, saying a brief's
implementation "may earn an entry there". Follow the precedent: one bullet
under `## [Unreleased]` → `### Added`, naming the paste channel and the two
files to paste, closing with one sentence saying the card it produces is the
card `prompt-craft.md` §10 already specified, unchanged. A reader scanning the
changelog for "can I use this yet" is the audience for the entry, and
answering them is the whole point of the channel.

**Nothing is owed to `evidence.md`.** This recommendation changes no printed
rule: the card it routes to is the one §10 already specifies, unmodified. The
brief cites `evidence.md`'s unprinted-page entry in finding 11 and adds
nothing to it. Two conditionals, stated so the implementation does not drift
into them: if the PR wants to claim anywhere that a pasted card is equivalent
to one produced by an installed skill, that is a claim about the artifact and
needs a source, and there is none — the honest form is the ledger's status
column, not a rule. And if paste-channel sessions later land in Part Three,
that tier's entry format (date, capacity, patterns, what came back, misreads)
needs a host field, since a card produced by a foreign model is not the same
artifact; that edit belongs in `evidence.md` in its own register — a field
report, below the lab evidence, never the support for a rule.

**Explicitly not built:** a `scan-back-paste.md` (scan-back is already one
self-contained file; generating a copy would be a duplicate with no
concatenation to justify it); a single combined paste (option E); any
condensed, rewritten, or summarized version of any source document; **any
build-time transformation beyond the one frontmatter deletion** — in
particular, no filtering of the dangling `design.md`, `evidence.md`,
`verify_layout.py`, or PDF-skill pointers, which is prose editing however it
is implemented; a fourth reference; a hosted-URL install; a prose linter of
any kind; a PDF path for non-skills surfaces (see unknown 5); a third
statement of the pen protocol; any change to `design.md`, `evidence.md`, or
the three pasted files themselves; and any user-facing claim that the paste
channel delivers the same thing an installed skill does.

Merging this brief makes it Accepted; the implementation PR tests the unknowns
first, appends a dated Validation section, and flips the header in that same
PR, per `research/README.md`.

**Unknowns 1 and 8 gate the merge of the implementation PR.** A paste that
arrives truncated, or an instruction line that does not reliably route the
host onto the card fork, invalidates the channel rather than qualifying it,
and both are testable before anything lands. Unknown 7 gates it only if a
pre-merge form of the command resolves; on its own terms it is otherwise a
post-merge confirmation with a one-line rollback, as stated there. Unknowns
2-6 are recorded honestly in the ledger row whatever they say.

**Sequencing, because this brief is the one that creates the coupling.**
`research/0004` (page size) and `research/0005` (the non-visual return) are in
the same unmerged batch as this brief, and both edit files this one turns into
a byte-checked artifact: 0004 changes `SKILL.md` line 74 and the named-format
entries in `page-patterns.md`; 0005 rewrites `prompt-craft.md` §10's trigger,
`SKILL.md` Step 4's card branch, and the "Notebook translation" gate. (`0006`
touches only `design.md`, which the paste omits, so it is unaffected.) The CI
check will do its job and fail any sibling PR that edits a source without
rebuilding the paste — that is the system working, not a defect — but a
stranger should not have to learn the dependency from a red build. Two
consequences, stated here rather than discovered: whichever of these lands
last owns a `./build.sh` run and a re-commit of `paper-session-paste.md`, and
0005's widened §10 trigger changes the sentence this brief's instruction line
is written against, so if 0005 lands first the instruction line and unknown 8
are re-read before this implementation begins.

---

## Validation — 2026-08-28, implementation PR

Everything above this line is the brief as accepted. Option A′ shipped:
`build.sh` emits `paper-session-paste.md` from the three sources with the one
frontmatter deletion, `verify.yml` checks the committed artifact against
`--paste-body` and the instruction line against README, and §Install carries the
download link, the quoted sentence, and the fifth ledger row. Three of the
Recommendation's snippets came out differently in the writing, and every byte
and word figure in the brief is stale — this brief landed in a batch that
edited all three of its sources.

### What shipped as specified

- **`paste_body()` is the only place the transformation exists**, and
  `./build.sh --paste-body` writes it to stdout and touches no file, so CI
  reads that awk filter rather than holding a second copy of it. Verified: the
  flag emits 64,715 bytes and leaves the tree unchanged.
- **A run that includes `paper-session` regenerates the artifact**;
  `./build.sh scan-back` alone does not.
- **Freshness is both lines.** `git ls-files --error-unmatch` and then
  `git diff --exit-code`, appended to the reproduce-cleanly step, so an
  untracked artifact fails by name and a stale one fails separately.
- **The content check is ordered ahead of the step that runs `./build.sh`**,
  for the reason the brief gives: a content check after it would compare the
  artifact CI just built against the sources CI just built it from.
- **Finding 2's load-bearing half survived the growth.** `scan-back/SKILL.md`
  still references no script, no reference document, no font, and no Python:
  the grep for `references/`, `scripts/`, `reportlab`, `pdfplumber`, and `.py`
  returns nothing. It is still one paste. Only its size moved.
- **Unknown 1's tail probe is still a tail probe.** "Which two patterns do not
  translate to a notebook at all?" is still answerable only from
  `page-patterns.md`'s closing section: both patterns are described earlier in
  that file, at `:21` and `:53`, and nothing outside `:129-130` says they do
  not translate.

### Corrections to the Recommendation's snippets

1. **CI runs `test -s` before `diff`; the brief's YAML had the order
   inverted.** With `diff` first, an empty `/tmp/committed-body` fails the diff
   and reports `does not match source — run ./build.sh`, so the emptiness check
   below it can never produce its own message and the sentinel is decorative
   after all — the opposite of what the brief argued for. Shipped order:
   extract, assert non-empty, then diff.

2. **A `test -f` guard was added ahead of the `sed`, which the brief did not
   specify.** `sed -n … | tail -n +2` swallows sed's exit status through the
   pipe, so an absent artifact arrives at the emptiness check looking exactly
   like a corrupted one and reports `has no sentinel line` for a file that is
   simply not there. Absence and corruption now report differently, which is
   the difference between "run `./build.sh`" and "something ate the preamble".

3. **The instruction line is extracted through the preamble's own wrapper, not
   through the sentence.** The brief's
   `grep -o 'I can.t print, and you can.t make a PDF here[^"]*'` hardcodes the
   sentence it is trying to compare, so a reworded sentence extracts nothing
   and the step fails as "instruction line missing" rather than as the README
   mismatch it exists to catch. Shipped:
   `sed -n 's/.*add this sentence: "\(.*\)"$/\1/p'`, which keys on the fixed
   wrapper `build.sh` owns and leaves the sentence itself free to change.
   Verified: the extraction returns the 126-character sentence and `grep -qF`
   finds it byte-identically in `README.md`.

### Every measurement in the brief is superseded

Taken with `wc` and `python3` against this tree on 2026-08-28, the same way the
originals were. The preamble is the one figure that did not move: still exactly
1,503 bytes, because `build.sh` emits it verbatim.

Bytes and words, brief figure first, this tree's second:

- **`scan-back/SKILL.md`** (finding 2) — 17,481 / 2,932 → **24,384 / 4,192**.
- **`paper-session/SKILL.md`** (finding 4) — 16,180 / 2,606 → **19,316 /
  3,110**.
- **`references/prompt-craft.md`** (finding 4) — 15,847 / 2,551 → **17,997 /
  2,949**.
- **`references/page-patterns.md`** (finding 4) — 27,696 / 4,394 → **28,588 /
  4,553**.
- **The three concatenated as they stand** — 59,723 / 9,551 / 385 lines →
  **65,901 / 10,612 / 394 lines**.
- **The frontmatter deletion** — 1,115 / 170 → **1,186 / 182**. The block
  itself is 1,185 bytes and the blank line after it is the 1,186th.
- **The shipped body** — 58,608 / 9,381 / 380 lines → **64,715 / 10,430 / 389
  lines**.
- **The shipped artifact, preamble included** — 60,111 / 9,618 → **66,218 /
  10,667**.
- **`references/evidence.md`** (finding 5) — 76,480 / 10,615 → **85,803 /
  12,175**; all four documents together, 136,203 / 20,166 → **151,704 /
  22,787**. Finding 5's argument is unchanged and slightly stronger:
  `evidence.md` is still larger than the other three combined.
- **`references/design.md`** (finding 6) — 15,676 bytes → **19,408**.
- **One combined paste** (option E) — 77,592 bytes → **90,602**.
- **The document-boundary split** (unknown 1) — 16,568 / 15,847 / 27,696 →
  **19,633 / 17,997 / 28,588**, still three messages worst case and still never
  mid-document.

At the same four-bytes-per-token approximation, and with the same warning
attached — no tokenizer was available on this machine either — the artifact is
roughly 16,500 tokens rather than 15,000. Option B's rejection is unaffected:
the artifact is still inside the context of every current model behind the
named products, and the constraint that bites is still the input box, not the
window.

Several of these figures move again before the batch closes. `research/0004` is
still `Draft` and its recommendation edits `SKILL.md` and the named-format
entries in `page-patterns.md`; whoever lands it owns a `./build.sh` run and a
re-commit of the artifact, exactly as the sequencing note says.

### Nothing on the unknown list was tested

The brief said unknowns 1 and 8 gate the merge of this PR. **They did not run,
and the header flipped anyway** — the same admission `0002` had to make, for
the same structural reason: all eight unknowns terminate in a foreign chat
product, and not one of the eight named surfaces is reachable from the
environment that implements this. What ships is a mechanically checked artifact
and a ledger row written to be honest about that, not a tested channel.

1. **The paste ceiling, per surface.** Unrun. The probe and the
   document-boundary split are re-measured above; nothing was pasted anywhere.
2. **Card fidelity against a real runtime.** Unrun. The fixed brief string the
   unknown requires is left exactly as written, so the runs stay comparable
   whenever someone makes them.
3. **Whether the host obeys the bright lines.** Unrun, so the ledger row is
   written from finding 11(a) asserted rather than counted — which the unknown
   says it must not be, and which the row says in its own words.
4. **Photo reading, per surface.** Unrun.
5. **ChatGPT's Python tool.** Unrun.
6. **The ink-key seam.** Unrun, and it moved slightly: `0005` added §10 to
   `design.md` in this same batch, so the file the paste omits now carries the
   document-metadata spec as well as the ink key. Neither travels. The seam is
   unchanged in kind and one section wider.
7. **The artifact does not disturb the other two tracks.** Unrun — no
   pre-merge form of `npx skills add … --list` was attempted. By the unknown's
   own terms it therefore leaves the merge gate and becomes a post-merge
   confirmation with the one-line rollback stated there.
8. **Whether the §10 branch fires from a pasted instruction line.** Unrun, and
   the most consequential of the eight, because the ASCII-sheet failure mode it
   guards against is the one the channel cannot survive.

### The sequencing note held, on one wrong reason

`0005` landed first, and it did rewrite `prompt-craft.md` §10's trigger,
`SKILL.md` Step 4's card branch, and the "Notebook translation" gate — so the
instruction line was re-read against the widened trigger, as the note requires.
It needs no change: §10 now fires when the user says they cannot print **or**
cannot read the printed sheet, and "I can't print" is still the first of those
two, in the user's own voice, which is the property the line was written for.

The note's reason for excluding `0006` was wrong. It says `0006` "touches only
`design.md`, which the paste omits". `0006` touches no reference document at
all — it replaces three font files and adds a build guard. The conclusion held;
the premise did not.
