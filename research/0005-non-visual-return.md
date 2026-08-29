Status: Implemented
Date: 2026-08-28
Outcome: the `onramps` PR — the §10 trigger widened to two conditions, the dictated/typed/scribed return admitted in `scan-back` Step 1, and `design.md` §10 document metadata set by the generator

# The non-visual return

## Scope

What the loop owes a person who cannot read the printed sheet, or cannot
write on it in their own hand: whether the existing dictated path already
serves them, what `scan-back` must admit before their pages can come back,
and what the PDF generator should set that costs nothing. It changes no
printed dimension and adds no printed rule, with one exception it does not
hide: the dot-grid sketch invariant has to be scoped for a session nobody can
look at (finding 9, recommendation 1), and that scoping is grounded in the new
`evidence.md` entry specified at the end, where the loss is recorded rather
than substituted for. The evidence question this brief raises is likewise
specified for `evidence.md` and is not answered here.

Out of scope, and named so nobody reads silence as coverage: full PDF/UA
tagging, motor-impairment input design (larger targets, alternative marking
gestures), braille embossing, translation, and anything about the chat
surface the skills run inside, which this repo does not own.

## Sources

- Local files, read for this brief:
  `paper-session/references/prompt-craft.md` §10,
  `paper-session/references/page-patterns.md` ("Notebook translation" and the
  eight named session formats), `paper-session/references/design.md` §9,
  `paper-session/references/evidence.md` (Clusters 1, 2, 3, 4, 6, 7, 10 and 11
  and the walking bonus cluster in full — every cluster finding 9 rules on —
  the cluster list end to end, "What the research does NOT support",
  "The unprinted page", and Part Three),
  `paper-session/SKILL.md` Steps 4-6 and its anti-pattern list,
  `scan-back/SKILL.md` Step 1 in full and its anti-pattern list,
  `paper-session/scripts/verify_layout.py`, `docs/specimen.py`, `CLAUDE.md`,
  `CONTRIBUTING.md` ("Where things go"), `research/README.md`, `research/0002`.
- Direct inspection of `docs/specimen.pdf` and of reportlab 5.0.1 behaviour on
  this machine (commands and results in findings 5 and 6).
- Standards, cited for what they require rather than for an effect size:
  WCAG 3.1.1 (Language of Page), WCAG 2.4.2 (Page Titled), PDF/UA-1's
  requirement that `/ViewerPreferences << /DisplayDocTitle true >>` accompany
  a document title. `evidence.md` Cluster 11 already states the honest
  standing of this kind of citation — standards "encode incident experience,
  not effect sizes" — and that standing is inherited here unchanged.

## Findings

1. **The repo has no accessibility surface at all, and its two adjacent
   groundings are about print.** A search of every `.md` in the tree for
   accessibility, screen readers, blindness, low vision, dyslexia, or motor
   impairment returns nothing but the notebook fallback's own sentences.
   `evidence.md` Cluster 11 does carry two things that read as accessibility
   work — the colour-vision-deficiency rule (roughly 1 in 12 men, Jeong et
   al. 2025, with the derived law that colour is never the sole carrier of
   meaning) and the psychophysical legibility floors (Legge & Bigelow 2011;
   Crossland et al. 2012's 29.6% of 65-84-year-olds without the contrast
   reserve for fluent reading of good print). Both are about a person reading
   ink on paper with their eyes. Neither says anything about a person who
   does not read the page at all.

2. **The setup card is already a linear, screen-reader-native representation
   of a session, and its trigger is the only thing keeping it from that
   audience.** `prompt-craft.md` §10 — read in full for this brief — is
   gated on one condition: "When the user says they cannot print — and only
   then; the question is never asked." Everything under that gate is
   text: an intent line verbatim, one prompt per page, machine items as
   numbered handles of four words or fewer under an `I PROPOSE` caption, at
   most one quoted machine line, and a DO THIS half that describes structure
   as pen gestures. There is no geometry to see, no zone to locate, no
   two-column react molecule to navigate. Extending the trigger to "cannot
   print **or** cannot read the sheet" reaches a blind or low-vision user
   through machinery that already exists, already has a spec, already has a
   `scan-back` reader on the other side, and already carries its own honest
   evidence entry. **This is the cheapest real accessibility work available
   in this repo, and it is prose, not machinery.**

3. **But the card is not a screen-reader feature, and the brief must not
   oversell it.** Two of its parts assume a sighted hand. The COPY THIS /
   DO THIS split is a transcription-cost boundary, and its 50-75-word budget
   exists because hand-copying is expensive; a person typing or brailling has
   a different cost curve. And DO THIS dictates pen gestures — "draw a line
   down the middle," "number 1-12 down the margin before writing anything in
   line 1" — instructions for building a page you can see. The defensible
   claim is narrower and still worth having: the card is the session in
   linear text, which is the input a non-visual worker needs, and what they
   do with it — a braille slate, a typed file, a scribe, a voice memo — is
   theirs to choose. The skill hands over the session and stops, exactly as
   it does for print.

4. **`scan-back` cannot currently accept their return, and the failure is a
   correctness defect rather than a gap.** Step 1 is, end to end, a procedure
   for transcribing handwriting; no sentence in either skill admits a
   dictated, typed, or scribed return. The consequence is not that such a
   return is refused — it is that the nearest matching rule, the one a reader
   lands on when a page carries handwriting that is not the user's, is the
   **Multi-hand returns** section (`scan-back/SKILL.md:34`), and applied to a
   scribe every instruction in it is wrong: hold every sheet as **a single
   pool**, **never attribute an idea to the person who wrote it**, read the
   `HAND:` box for routing and nothing else, and — the sharpest error —
   narrow the authority cascade so "a handwritten legend governs the sheet it
   appears on, not the session, since the hand that wrote it can only speak
   for its own page." A scribe is not a contributor whose ideas get pooled
   with the author's; a scribe's legend speaks for the author, because the
   scribe speaks for the author.

   Be exact about where the mis-routing lives, because the fix is two strings
   and a loose statement of it will not land. The section's *scoping
   sentence* is already format-keyed: "A group format comes back as several
   sheets in several hands." What keys on hand count is the **heading**
   ("Multi-hand returns") and the **cascade sentence** ("on a multi-hand
   return a handwritten legend governs the sheet it appears on"). Those two
   are the whole surface: a reader who arrives at a two-hand return by the
   heading finds a section whose every rule is written for participants, and
   the cascade sentence then fires on hand count by its own wording. Only
   brainwriting rounds is group-only today, and every other named format is
   single-author, so extra hands on those are scribal or clerical, never
   participants.

   Three further sentences are false rather than mis-scoped once a scribe is
   admitted, all in Step 1's "Unprinted pages" subsection and none of them
   reached by fixing the section above:
   - `:36`, the subsection's definitional sentence — "the header and the
     prompts in the human's own hand, **every mark on the page made by the
     same person**." Flatly untrue of a scribed page.
   - `:40`, "**All the ink is the human's**." The rule derived from it — treat
     the dominant ink as the default channel whatever its hue — survives; the
     premise does not, and a scribe working in their own pen is exactly the
     case where the dominant ink is not the author's.
   - `:44`, "**Deviation is authority** … the layout is the human's now."
     With a scribe in the loop a deviation may be the scribe's transcription
     error, which is the one case where deviation is *not* authority. That is
     an open correctness question rather than a wording problem, and
     recommendation 2 answers it rather than leaving it.

5. **The PDFs are untagged, and their metadata ships at reportlab's
   defaults.** Verified against the committed `docs/specimen.pdf`: the
   catalog is `<< /PageMode /UseNone /Pages 28 0 R /Type /Catalog >>` — no
   `/StructTreeRoot`, no `/MarkInfo`, no `/Lang` — and the Info dictionary
   reads `/Author (anonymous) /Creator (anonymous) /Subject (unspecified)
   /Title (untitled)`. A screen reader opening that file is told it is called
   "untitled" and is given no natural language for the speech synthesiser to
   pronounce it in. `docs/specimen.py` never calls a metadata setter; a grep
   for `setTitle`, `setAuthor`, `setLang`, or `/Lang` across `docs/` and
   `paper-session/` returns nothing.

6. **All three metadata fields are one line each in reportlab and were tested
   here.** On reportlab 5.0.1: `canvas.Canvas(path, lang="en-US")` emits
   `/Lang (en-US)` into the catalog; `c.setTitle(...)` emits `/Title`,
   correctly falling back from PDFDocEncoding to UTF-16BE with a BOM on
   non-Latin text (tested with mixed CJK and Cyrillic); and
   `c.setViewerPreference('DisplayDocTitle', 'true')` emits
   `/ViewerPreferences` with `/DisplayDocTitle true`, which is what makes a
   reader announce the title instead of the filename. A private-API fallback
   also works if the `lang=` keyword turns out to be missing from an older
   runtime: `c._doc.Catalog.Lang = pdfdoc.PDFString("en-US")` produced the
   same catalog entry. `pdfplumber` — already a required dependency — reads
   both back: `pdf.doc.catalog.get('Lang')`, which returns bytes (`b'en-US'`),
   and `pdf.metadata['Title']`, which returns a str.

7. **Metadata must never become a continuity anchor, and the reason is a rule
   rather than a physical impossibility.** The invariant bans QR codes,
   session IDs, and machine-readable context blocks *on the page*, and its
   reason is `scan-back`'s orphan path: the printed header must carry
   everything a cold reader needs. Metadata does not strain that invariant on
   its face — it is not on the page, costs no space, and is invisible to the
   pen. But the tempting supporting argument, that a photograph carries no
   metadata so `/Title` *cannot* be read back, is false and this brief must
   not lean on it. `scan-back/SKILL.md:16` accepts "a PDF annotated directly
   on a tablet rather than a photographed printout," and `prompt-craft.md:104`
   routes stylus users to exactly that path. A tablet return is the original
   file with its Info dictionary intact, so on that one path `/Title` is
   readable, and a model looking for continuity would find it. The rule is
   therefore load-bearing rather than decorative: **nothing in either skill
   may ever rely on PDF metadata for continuity, on any return path** —
   because the majority path carries none, and a continuity rule that holds
   only for tablet users is a rule that fails on the day it matters.
   `scan-back` is the skill that would be tempted, so the rule has to be
   written there and not only in `paper-session`.

8. **`/Title` has a privacy edge on one format, and the fix has to be argued
   rather than asserted.** A document title travels with the file into file
   managers, print queues, and cloud previews, in contexts the author did not
   choose. For most sheets the intent line is already printed on every page,
   so putting it in metadata discloses nothing new. The serial disclosure kit
   is the exception: its subject matter is work friction and professional
   setbacks, its pages print `PRIVATE — THIS PAGE STAYS WITH YOU. IT IS NOT
   SCANNED.` (design.md §9 specifies that string and says "print it
   exactly"), and its intent line should not be what a shared printer queue
   displays. Note what the exception is *not*: titling the file with the
   format name is worse than the disease, because "serial disclosure kit" in
   a queue announces that this person is doing expressive writing about
   professional setbacks — a sharper disclosure than most intent lines. Two
   answers are defensible: a neutral constant that names nothing (the
   product name plus the date, "Paper Session — 2026-08-28") or the date
   alone. Recommendation 3 takes the first, because `DisplayDocTitle` makes
   the title the string a reader announces and a bare date announces nothing
   a person can act on.

9. **A dictated or typed return costs the loop its strongest mechanisms, and
   the brief has to say so in full.** Reading `evidence.md` against this path,
   by cluster:
   - **Cluster 2, "Paper beats screens for deliberation"** — lost wholesale.
     Its entire content is a paper-versus-screen contrast (Clinton 2019,
     g = -0.25, with the calibration advantage of g = 0.20 that the file
     calls "the most important number in this entire brief"). A spoken
     answer is neither medium; nothing in the cluster covers it.
   - **Cluster 3, "Handwriting beats typing for thinking"** — lost wholesale,
     and this one is lost by name. The cluster is a handwriting-versus-typing
     comparison; a typed return is literally its control condition, and a
     dictated one is outside it entirely.
   - **Cluster 7, "Sketching (the keystone)"** — lost with no substitute, and
     it is the file's own nomination for "the strongest paper-beats-screen
     mechanism in the entire brief." This is the largest single cost. It also
     collides head-on with an invariant: every Deep kit contains at least one
     dot-grid sketch zone, and a non-visual session cannot. The existing
     notebook path does *not* break that invariant — `page-patterns.md:117`
     calls dot grid "what most notebooks already are," arguably improved — so
     this is the first path in the repo that does, and recommendation 1 has
     to scope the invariant explicitly rather than let an implementer drop it
     by inference.
   - **Cluster 6, "Physical manipulation"** — lost wherever a kit used
     cut-apart cards, though the cluster's own correction already scopes that
     narrowly.
   - **Cluster 11, "The return trip"** — the mark vocabulary goes with the
     page. Strike, circle, `?`, `!`, star, arrow are visual-spatial marks;
     the dropout-ink inversion that lets `scan-back` attribute authorship by
     chroma is void here for the same reason it is already void on an
     unprinted page. What survives is the part Cluster 11 says is primary
     anyway — wording. A spoken "cut that" is a strike.
   - **Cluster 10, "Desirable difficulties, and the adoption problem"** —
     cuts against this path rather than being lost by it. Dictation is the
     least effortful of the three return channels, and the cluster's finding
     is that the effortful strategies are the ones that work and the ones
     people decline. Expect a dictated return to be the shallowest.
   - **Cluster 4, "The cost of staying on screen"** — survives, and cuts both
     ways, which is why it is here rather than left silent. Its Schweisfurth
     result is about an interruption that creates idle time and, in the
     cluster's own closing words, is "an interruption that leaves the problem
     live" — a dictated session does that as well as a printed one does. Its
     Leroy attention-residue half is the caution: a dictated return lands
     back on-screen, in the chat, which is the surface the interruption was
     meant to leave. The thinking is still off-screen at both ends; the
     handover is not, and unknown 7 is where that risk gets tested.
   - **Cluster 1 (offline incubation) and the walking bonus cluster survive,
     and the walk may survive better than it does on paper.** The off-screen
     half of the thesis does not require paper. Cluster 1's incubation effect
     is about stepping away from a loaded problem, not about what you step
     away with: Sio and Ormerod's second finding — longer preparation
     produces a greater incubation effect — is served by a dictated card as
     well as by a sheet, and the card *is* the preparation. Walking's
     d = 0.93 on divergent thinking is the largest effect in the file and
     pairs naturally with dictation. This is the honest reason a non-visual
     session is still this loop and not just a chat: what is lost is the
     paper mechanisms, not the leaving.

   The trade is real and it is the right one. Half the mechanism base buys
   access for people the loop currently cannot serve at all, and the
   alternative is not a better version of the loop for them — it is
   exclusion.

10. **Two of the three changes land on cross-skill couplings `CLAUDE.md`
    names, so both sides move in one PR.** The §10 trigger extension is a
    change to the **setup-card conventions**: `prompt-craft.md` §10 writes
    them and `scan-back` Step 1 "Unprinted pages" reads them, with no shared
    file, and that subsection currently opens by asserting the provenance of
    every unprinted return — "They come from the dictated path — when the
    user cannot print" — which becomes false the moment the trigger widens.
    The scribe clause touches the **pen protocol**, but less than it first
    appears, and the brief should not order a mirrored edit it has not
    checked. The multi-hand narrowing of the legend cascade is specified
    twice, and `design.md` §9 rung 1 is *already* format-scoped — "On a group
    format returning several sheets in several hands, it governs the sheet it
    appears on rather than the table" — so a scribed single-author return
    never satisfies its antecedent, and mirroring a carve-out into it would
    be a no-op on the rule. What design.md needs is smaller: the two sides
    have to end this PR saying the same thing in the same terms, so that the
    next editor of either cannot re-widen one alone. Note also that none of
    this narrowing is printed — the printed ink key is only "INK KEY  RED
    REVIEW · GREEN GO · BLUE DO · BLACK NOTES" (design.md §9) — so a one-sided
    edit produces a reader that does not honour the spec, never a sheet that
    prints a key the reader does not honour.

    The carve-out also has to name which cascade it is narrowing, and the
    answer is both. A dictated or self-copied return is an unprinted return,
    where the cascade is already the short one — handwritten legend >
    defaults, no printed ink key in the middle. But a scribed return need not
    be unprinted: recommendation 1 grants a PDF on request precisely so a
    scribe can work from one, and a scribe filling in a printed sheet
    produces a three-rung page. Write the scribe rule so it holds on either —
    a legend in the scribe's hand outranks whatever sits below it, because the
    scribe speaks for the author — rather than assuming the two-rung case.
    The `/Lang` and `/Title` change touches no coupling.

11. **Four sentences elsewhere in the tree go stale the moment the trigger
    widens, every one of them worded around printing.** Two are
    `paper-session` anti-patterns. `SKILL.md:130` — "Asking whether the user
    has a printer (the card is reactive only; it is never proposed to anyone
    who has not said they cannot print)" — encodes exactly the reactive
    property recommendation 1 promises to keep, in words that do not fire on
    the new trigger. `SKILL.md:132` — "Rendering the PDF anyway as a
    reference for someone who cannot print" — is the same staleness plus a
    live design question the brief has to answer rather than leave to an
    implementer: a non-visual user who *can* print may genuinely want the
    PDF, for a sighted colleague or for a scribe to work from. The third is
    `scan-back/SKILL.md:81` — "Asking the user to describe what they wrote
    instead of reading it" — which is in direct tension with admitting a
    dictated return, where describing *is* the channel and there is nothing
    to read. The fourth is outside both skills: `evidence.md:341` opens the
    closing Part Two entry with "Added with the notebook fallback, which
    serves a user who cannot print by dictating a setup card…", the same
    provenance assertion finding 10 flags in `scan-back`, sitting in a file
    this brief otherwise leaves untouched.

## Options

Two options are real alternatives. Both are rejected, and the second is the
closer call.

**Option A — a screen-reader "text twin": emit a plain-text or HTML rendering
of every sheet alongside the PDF.** Rejected on the record, for four reasons.

1. **It builds a second maintained representation of every sheet.** The
   library is eleven pattern groups and eight named session formats today,
   each specified as geometry — two-column react, rank rows, distribution
   strips, dot-grid bands, the gap column, the constraint box. A twin means
   every one of those gets a second rendering, and every future pattern gets
   two authored forms forever. `CLAUDE.md` already records what happens to a
   duplicated representation in this repo: the loose root copies of the
   reference docs drifted from the bundled ones, which is why the tree now
   forbids duplicate copies of a reference doc anywhere.
2. **The good version of a "twin" already exists, and it is the setup card.**
   The card is the session rendered as linear text with no geometry in it,
   which is the thing a twin is reaching for; a twin instead renders the
   *page*, and so ends up describing an artifact its reader cannot use —
   "two-column react zone, left column, item three." Handing over the
   session's content beats narrating the layout of a sheet nobody on this
   path will look at.
3. **It splits the loop's single artifact in two.** `scan-back` resolves a
   return against one answer key. A twin creates a second candidate for that
   role and a standing question about which one the human worked from.
4. **It is a parallel emitter, which is the expensive kind of accessibility
   work, and this brief exists partly to argue that the cheap kind is
   available.** Two paragraphs of prose and three lines in a generator reach
   further than a second output target, and they cannot drift from a spec
   they *are*.

**Option B — a distinct non-visual mode: a second gate alongside §10 that
inherits the card's content rules but drops its hand-copy machinery.** This is
the real alternative, and the brief has to argue it rather than pretend the
card is the only shape available. Finding 3 concedes that two of the card's
parts assume a sighted hand, and they are not incidental parts: COPY THIS is
defined as the half that "is transcribed by hand and is the only thing that
is," its budget is stated in *handwritten* words, and DO THIS dictates pen
gestures. Widening §10's trigger therefore reuses the card's packaging while
its central mechanism — hand-copying into a notebook — does not necessarily
apply to whoever comes through the new door. Option B keeps §10's content
rules verbatim (intent line verbatim, one prompt per page, numbered handles of
four words or fewer under `I PROPOSE`, at most one quoted machine line, no
handles on a page carrying a generative zone) and replaces the COPY/DO framing
with a single ordered list, the 50-75 handwritten-word budget with an item
cap, and the pen gestures with the structure they encode.

Rejected, for three reasons, and it is close.

1. **Two gates duplicate a spec that is already coupled across two skills.**
   §10's conventions are read back by `scan-back` with no shared file, and
   `CLAUDE.md` names that coupling as one it expects edits to break. A second
   mode makes it three documents to keep in step instead of two, for a
   population this repo has not yet met.
2. **The budget's second job survives the loss of its first, and that job is
   the one an invariant depends on.** The 50-75-word cap exists partly as
   transcription cost, which Option B correctly notes does not bind a person
   typing or brailling. Its other job is capping machine content so that
   copying does not become deep exposure to it — the asymmetry `evidence.md`
   records under "The unprinted page", which is a fixation rule, not an
   ergonomics one. That job binds on every path. An item cap can express it,
   but it is a new number nothing in `evidence.md` grounds, where the word
   budget at least has a stated rationale. Unknown 4 keeps the question open
   in the field instead of guessing at it now.
3. **The pen gestures degrade gracefully; the mode does not need replacing to
   fix them.** "Draw a line down the middle" describes a structure — two
   columns — and a person working in a braille slate or a text file can
   build that structure their own way. Recommendation 1 makes that explicit
   in one line, which is the cheap version of Option B's whole benefit.

If unknown 3 or unknown 4 comes back badly — the card's two-part structure
inaudible, or the budget absurd off the hand-copy path — Option B is what gets
reopened, and it takes a new number rather than an amendment to this one.

Full PDF/UA tagging is **not** rejected here — it is deferred, unresearched.
reportlab's canvas API has no marked-content or structure-tree support in the
version this repo runs against, so tagging means either a second rendering
path or hand-building a structure tree, and neither is a paragraph of prose.
What would settle it is finding 3's unknown: whether anyone in this audience
wants a navigable PDF at all, given that a navigable worksheet is still a
worksheet they cannot write on. If that answer comes back yes, it earns its
own numbered brief.

## Risks / unknowns to validate

This list is the implementation PR's test plan.

1. **reportlab's `lang=` keyword in the environment the skill actually runs
   in.** Verified only against 5.0.1 here; `SKILL.md` Step 4 runs wherever
   the skill is loaded. Test:
   `python3 -c "import reportlab,inspect;from reportlab.pdfgen.canvas import Canvas;print(reportlab.Version,'lang' in inspect.signature(Canvas.__init__).parameters)"`,
   then generate a one-page sheet and confirm `/Lang` and `/Title` appear in
   the catalog and Info dictionary. Note for whoever writes the assertion:
   `pdf.doc.catalog.get('Lang')` returns **bytes** (`b'en-US'`), not a str,
   while `pdf.metadata['Title']` returns a str; compare accordingly. If the
   keyword is absent, the documented fallback is the private-API assignment
   in finding 6, and Step 4 should say which to use rather than leaving it to
   be rediscovered.
2. **Whether a real screen reader announces any of this.** Untestable in this
   repo — it needs a person with a reader. Concretely: open a generated sheet
   in Acrobat Reader with NVDA or VoiceOver, with `DisplayDocTitle` set and
   unset, and record (a) whether the title or the filename is announced, and
   (b) what the on-the-fly auto-tagging pass makes of a real Paper Session
   page — two-column react molecules, rank rows, dot grids, hairline rules.
   The honest prediction is that the reading order is bad and that `/Lang`
   and `/Title` improve the announcement without making the sheet usable.
   Recording that result is the point: it is the evidence for or against ever
   tagging.
3. **Whether the card survives a screen reader as a card.** It is a single
   fenced monospace block, and its structure is two headed halves. Test:
   generate one, read it with a screen reader in the actual chat surface, and
   check whether the COPY THIS / DO THIS boundary is audible at all. If the
   fence flattens, the split needs to be carried by wording rather than by
   layout — which would be a §10 change, not a new mode.
4. **Whether the 50-75-word budget is the right gate off the hand-copy
   path.** The budget is a transcription-cost rule. A user typing or
   brailling pays a different cost, and the budget's second job — capping
   machine content so hand-copying does not become deep exposure to it — has
   nothing to do with the first, and only the second is grounded in
   `evidence.md`. Ships unchanged and binding by default; test whether anyone
   on this path finds it absurdly tight, and never quietly dictate more
   because it felt tight. This is the unknown Option B turns on: a bad answer
   here reopens it, at a new number.
5. **Whether the format-scoped multi-hand trigger still fires for the case it
   was written for.** Re-run the brainwriting return path against the edited
   text: an orphaned scan of six copies of one page pattern, identical footer
   numbering, no chat. Confirm the pooling, non-attribution, and no-ranking
   rules still trigger from the observable signal — several copies of the
   same pattern — rather than from hand count, and that the scribe carve-out
   does not fire on it.
6. **Whether the scribe clause holds across two skills with no shared file.**
   The same unknown `0002` flagged for the setup-card conventions and could
   not close: authoring both sides on one day is not evidence that they
   survive the next edit to either. A vaguer version of this test is worse
   than none, so name the strings. Two literals carry the clause — one for the
   format scoping, one for the scribe rule — and both sides must contain both,
   exactly:
   - `a group format` — in `scan-back/SKILL.md` (the Multi-hand section's
     scoping sentence *and* the sentence that today reads "on a multi-hand
     return") and in `design.md` §9 rung 1.
   - `a scribe speaks for the author` — the scribe carve-out's own sentence,
     required in `scan-back/SKILL.md` and in `design.md` §9 rung 1.

   The check is four `grep -qF` calls in `build.sh`, alongside the `name:`
   and font-license gates it already runs, failing loudly and by name when a
   string goes missing from either side. That is a real discriminator: it
   fails on the actual failure mode, one side being reworded without the
   other. It cannot detect a rule that drifts in *meaning* while keeping the
   phrase, which is `0002`'s residue and stays a field question — but it
   catches the case that has already happened once in this repo. Adding a
   content check to `build.sh` widens its charter, so, like the
   `verify_layout.py` option in recommendation 3, it is a deliberate call for
   the maintainer rather than a side effect: if declined, this reverts to
   `0002`'s answer and resolves only in the field.
7. **Whether a dictated return tempts the model into interviewing.** The
   sharpest behavioural risk in this brief. "Stop when the sheet is handed
   over" is an invariant, and a return channel that lives in the chat invites
   the model to elicit the answers live, question by question, which would
   collapse the loop into ordinary chat and lose the offline half that
   finding 9 says is the part that survives. Test by running one: hand over a
   card, come back with a dictated return, and check the transcript for the
   model asking the sheet's questions rather than receiving their answers.
8. **Whether anyone uses this at all, or prefers a scribe or braille.** A
   completion question, unanswerable here, and `evidence.md` Part Three is
   where it lands, in that tier's format: date, capacity, patterns used, what
   came back or where it stopped, and anything the `scan-back` pass misread.

## Recommendation

Ship three changes in one PR.

**1. Widen the §10 trigger.** In `paper-session/references/prompt-craft.md`
§10, the gate becomes "when the user says they cannot print, or cannot read
the printed sheet — and only then; neither question is ever asked." Keep every
existing property of the mode: reactive only, no apology, no naming of what
they are not getting, no suggestion of an alternative they did not ask for.
Add one short paragraph making finding 3 explicit — the card is the session in
linear text, the human chooses the medium they work in, the budget still binds
by default — and one line stating that the pen-gesture wording in DO THIS is
about the shape of the work, so where a gesture cannot be performed the
structure it describes is what carries over. Condense the trigger change into
`paper-session/SKILL.md` Step 4's existing branch (which today reads "If the
user cannot print") and into the frontmatter phrase that currently reads
"Works without a printer — say so"; the one-way dependency holds, reference
first.

Three consequential details this recommendation owes an implementer, all from
findings 9 and 11:

- **The sketch invariant gets scoped, in writing, in one place.**
  `references/page-patterns.md`'s "Notebook translation" gate gains a sentence
  saying that the same gate governs a session dictated because the sheet
  cannot be read, and that this is the one path where the Deep dot-grid
  requirement does not hold: the gate's existing line that dot grid is "what
  most notebooks already are" is true of a notebook and false of a person who
  cannot see it. Where the sketch zone cannot be worked, the kit carries the
  prompt the sketch was there to ask and nothing stands in for the drawing —
  the loss is recorded in `evidence.md`, not papered over with a substitute
  activity. `CLAUDE.md`'s invariant list gains the matching clause on the
  "Every Deep kit contains at least one dot-grid sketch zone" bullet, because
  that is where the rule actually lives and an unscoped invariant plus a
  scoped reference is the contradiction this repo's three-layer rule exists
  to prevent.
- **Two anti-patterns get reworded around the trigger, not around printing.**
  `SKILL.md:130` becomes reactive-only phrased against both conditions (the
  card is never proposed to anyone who has not said they cannot print or
  cannot read the sheet, and neither question is ever asked). `SKILL.md:132`
  becomes "Rendering the PDF anyway, unasked, for someone who has taken the
  card path."
- **And that rewording answers the question `SKILL.md:132` raises.** A
  non-visual user who can print may want the PDF — for a sighted colleague,
  or for a scribe to work from. The rule is the mode's existing posture,
  unchanged: never render it unasked, never offer it, never name it as
  something they are missing; render it without comment if they ask. That
  keeps the anti-pattern's original point (the PDF is not a consolation
  prize) without refusing a person a file they have a use for.

**2. Admit the non-visual return in `scan-back/SKILL.md` Step 1.** One
paragraph, in the "Unprinted pages" neighbourhood, saying: a return may arrive
dictated in the chat, typed, or written by a scribe; it carries exactly the
authority the user's own hand carries, under Step 2's authority rule
unchanged; **a scribe's hand is not a second participant** — never pool it,
never merge it as a contribution, never ask who held the pen, and a legend the
scribe wrote governs the session, because **a scribe speaks for the author**.
Include the metadata rule from finding 7 here, in the skill that would be
tempted by it: continuity is never read out of a returned file's PDF metadata,
on any path, including a tablet return where the Info dictionary is intact.

The rest of this recommendation is sentence-level, because finding 4 shows a
loose instruction will not land. The exact edits:

- **`:34`, the section heading.** "Multi-hand returns" becomes a
  format-keyed heading — "Group-format returns" — so a reader arriving with a
  two-hand return is not routed here at all.
- **`:34`, the cascade sentence.** "on a multi-hand return a handwritten
  legend governs the sheet it appears on" becomes "on a group-format return."
  Nothing else in the sentence changes; the reasoning that follows it ("since
  the hand that wrote it can only speak for its own page") is correct for a
  participant and stays.
- **`:34`, the scoping sentence, left alone.** "A group format comes back as
  several sheets in several hands" is already right, and the section's
  identification signal on an orphan — several copies of one page pattern
  carrying identical footer numbering — is already stated two sentences later.
  Add only a clause naming what is now excluded: extra hands on a
  single-author format are scribal, and the scribe paragraph governs them.
- **`:36`, the subsection's definitional sentence.** Strike the clause "every
  mark on the page made by the same person," which is false of a scribed
  page. Nothing replaces it: the property that actually defines the
  subsection is already in the same sentence — no printed layer, and so no
  printed ink key and no dropout-ink inversion — and the single-hand case
  becomes the common instance rather than the definition. Correct the same
  sentence's provenance claim in the same edit: "They come from the dictated
  path — when the user cannot print" becomes the two triggers, cannot print
  or cannot read the sheet.
- **`:40`.** "All the ink is the human's" becomes "All the ink is
  handwritten, and on a self-copied page all of it is the human's." The
  dominant-ink rule that follows is unchanged and is what actually does the
  work on a scribed page too.
- **`:44`, the open correctness question, answered.** "Deviation is
  authority" holds unchanged on a self-written page. On a scribed page it
  holds for content and not for structure: a merged column or a prompt
  answered in the wrong place may be the scribe's slip rather than the
  author's choice. The rule is that a scribed structural deviation is read
  as the author's unless the pages themselves contradict it, and it is never
  queried back — asking the author to account for their scribe's layout is
  the interrogation this skill already refuses. Where a deviation changes
  what the next step would be, it goes to the Step 3 pass inside its existing
  question cap, as an ambiguity at a fork, which is what that bar is for.
- **`:81`, the anti-pattern.** "Asking the user to describe what they wrote
  instead of reading it" gets scoped: it bans substituting a description for
  pages that exist, and does not bar a dictated return, which is not a
  description of a page but the page itself.

In `paper-session/references/design.md` §9 rung 1, add the scribe case
explicitly. The rung is already format-scoped, so this changes no rule (finding
10); it makes the scoping unmissable and, with the same two literals present on
both sides, checkable by unknown 6's grep. Write it to hold on both cascades,
the two-rung unprinted one and the three-rung printed one a scribe may be
working from. Add one anti-pattern line to each skill: to
`scan-back`, reading a scribe's hand as a second contributor; to
`paper-session`, interviewing the human through the answers a handed-over
session asked for.

**3. Set the metadata in the generator — spec in the reference, restatement in
the procedure.** This is document-level output anatomy, which
`CONTRIBUTING.md`'s "Where things go" table sends to
`paper-session/references/design.md` ("Point sizes, gray values, rule weights,
page anatomy"). Writing it straight into `SKILL.md` would be the invention the
one-way dependency forbids — the same rule recommendation 1 is careful to obey.
So: a new **§10, Document metadata** in `design.md` (the file currently ends at
§9), specifying three settings —

- construct the canvas with `lang=` set to the language the sheet is written
  in;
- `setTitle` to the sheet's printed title, which every page carries as item 2
  of the mandatory four-item header in §4 — with one exception, the serial
  disclosure kit, whose title is the neutral constant `Paper Session` plus the
  date and never the format name, per finding 8;
- `setViewerPreference('DisplayDocTitle', 'true')`, so the title rather than
  the filename is the string a reader announces.

Then condense those three into `SKILL.md` Step 4 as a restatement pointing at
§10, in the register Step 4 already uses for design rules. State the rule from
finding 7 in `design.md` §10 as well, and mirror it into `scan-back` per
recommendation 2: nothing ever reads continuity out of PDF metadata on any
return path. Rebuild `docs/specimen.pdf` in the same PR — `python3
docs/specimen.py`, which needs `pymupdf` and `pillow` beyond
`requirements.txt` — because finding 5 makes the committed specimen the
evidence that metadata ships at reportlab's defaults, and leaving it unfixed
means the repo's own reference implementation contradicts its new spec.
Leave `verify_layout.py` alone — it is deliberately narrow and does not check
the design system, and a metadata assertion is a design-system check. The
option is real if the maintainer wants enforcement rather than spec
(`pdf.doc.catalog.get('Lang')` and `pdf.metadata['Title']` are both readable
from the existing `pdfplumber` dependency, verified), but taking it widens the
verifier's charter and that should be a deliberate decision, not a side effect
of this PR.

**What this brief owes `evidence.md`, and does not write.** One new closing
entry in Part Two, a sibling to "The unprinted page" and in the same register:
title it for the non-visual return, state that **no study tests a dictated,
typed, or scribed return of a generated worksheet**, and add no source for
that claim because there is none to add. Its body is finding 9, cluster by
cluster and by name — Cluster 2 and Cluster 3 lost wholesale, Cluster 7 lost
with no substitute and the largest single cost, Cluster 6 lost where cards
were used, Cluster 11 reduced to its wording half with the dropout-ink
inversion void exactly as it already is for the unprinted page, Cluster 10
cutting against the path, Cluster 4 surviving but cutting both ways because a
dictated return lands back on-screen, and Cluster 1 and the walking cluster
surviving. It must state plainly that this is a trade of the loop's strongest
mechanisms for access, and that nothing either skill prints or says may tell
a person on this path that they are getting the same thing — the mode does not
apologise and does not claim equivalence. It must also record what the file
still has no source on: screen readers, PDF semantics, and motor impairment,
and that
`/Lang` and `/Title` rest on a standards conformance requirement rather than a
measured effect, with Cluster 11's own standing for standards citations
inherited rather than restated. Do not edit the existing clusters: the loss
statement is a reading of them, not a correction to them. **One sentence in
that file is not a cluster and does need editing**, per finding 11:
`evidence.md:341`, the opening line of "The unprinted page", asserts that the
notebook fallback "serves a user who cannot print", which stops being the whole
truth the moment the trigger widens. Correct it to name both triggers. Nothing
else in that entry moves; the new sibling entry carries everything else.
Completion data from unknowns 2, 3, 7, and 8 lands in Part Three under that
tier's rules, where the three-independent-reports threshold already governs
what happens next.

`CLAUDE.md` gains nothing new in its **coupling** list — both couplings this
touches are already named — but the setup-card entry's parenthetical, which
describes the card as the no-printer path, needs the second trigger added so
the map matches the territory. Its **invariant** list is a different matter and
does gain something: the dot-grid sketch bullet takes the scoping clause from
recommendation 1, because that list is where the invariant lives and a rule
scoped in a reference but absolute in `CLAUDE.md` is a contradiction waiting
for the next contributor. `CHANGELOG.md` gets one entry, written as what
changes for a person receiving a session. `README.md`'s compatibility ledger
is the honest place for one line on what the loop does and does not offer a
non-visual user; it is a ledger of honest status, and this is status. Then
`python3 docs/specimen.py` to rebuild the specimen against the new metadata
spec, and `./build.sh`.

**Explicitly not built:** a text twin or any second rendering of a sheet; PDF
tagging or a structure tree; a `references/accessibility.md` or any second
design system; an accessibility mode, a settings flag, or a stored preference;
any proactive question about the user's vision, hands, or reading; any
in-session advertisement of the path to someone who did not raise it; a
braille or large-print output target; changes to the type scale, gray floors,
or any printed dimension; any relaxation of the dot-grid sketch requirement
beyond the one scoping clause recommendation 1 specifies — it holds absolutely
for printed Deep kits and for dictated-to-notebook ones, and yields only where
the human cannot see the page, where the loss is recorded rather than
substituted for; an audio output of any kind; and any user-facing claim that a
dictated session is equivalent to a paper one.

---

## Validation — 2026-08-28, implementation PR

Everything above this line is the brief as accepted. All three recommendations
shipped, and one of them shipped late enough that it is worth saying so: the
metadata work in recommendation 3 landed in a reconciliation pass after the
rest of the batch, and until it did, `evidence.md` asserted the generator set
three fields it did not set. That is recorded here rather than smoothed over,
because the gap between a reference claiming a behaviour and the generator
having it is exactly the failure this brief's one-way-dependency argument is
about.

Of the eight unknowns, one is resolved and mechanized, one is resolved on this
machine but not in the environment that matters, and six were not run.

### Recommendation 1 — the widened trigger: landed

`prompt-craft.md` §10 opens on the two conditions and only those two, with
neither ever asked, and carries the paragraph finding 3 required — the card is
the session in linear text, the medium is the human's to choose, the budget
still binds by default. The pen-gesture line is there too: "The gesture is how
the shape of the work gets said, not the work itself: where a gesture cannot be
performed, the structure it describes is what carries over."

Condensed, reference first: `paper-session/SKILL.md`'s frontmatter phrase now
reads "Works without a printer, and without reading the page", Step 4's branch
is "If the user cannot print, or cannot read the sheet", and the two
anti-patterns are reworded around the trigger rather than around printing —
`:134` bans asking either question, `:136` is "Rendering the PDF anyway,
unasked, for someone who has taken the card path" with the render-on-request
allowance intact.

The three consequential details all landed. The sketch invariant is scoped in
`page-patterns.md`'s "Notebook translation" gate — "where it is worked without
sight of one … the prompt the drawing was there to ask still carries, and
nothing takes the drawing's place" — and `CLAUDE.md`'s invariant bullet carries
the matching clause, so the reference and the invariant list now say the same
thing. `evidence.md` gained the Part Two sibling entry naming the lost clusters
one by one, and its "The unprinted page" opening sentence was corrected to name
both triggers.

**One thing the reconciliation added that the recommendation did not name.**
The `paper-session` anti-pattern this brief asked for — interviewing the human
through the questions a handed-over session already asked — arrived in
`SKILL.md` before it had a reference to be condensed from, which is the
inversion `CLAUDE.md` forbids. Its counterpart now exists at
`prompt-craft.md:108`: "Once the card is theirs, the questions on it are
answered off-screen and come back on the return trip; walking the human through
them in the chat turns a handover into an interview." A rule stated only in
`SKILL.md` and only in the *other* skill is the shape of drift this repo has
already had once.

### Recommendation 2 — the non-visual return in `scan-back`: landed

Every sentence-level edit the recommendation specified is in place. `:36` is
headed "Group-format returns" and routes on the format explicitly — "What
routes a return here is the format, never the hand count: on a single-author
format an extra hand is scribal or clerical" — with the narrowed cascade
rewritten to "on a group format returning several sheets in several hands".
`:38` admits the dictated, typed, and scribed return with Step 2 unchanged, and
closes "Receive it; never conduct it." `:40` is the scribe paragraph, carrying
the carve-out on both cascades and the sentence that ends "because a scribe
speaks for the author". `:42` drops the false "every mark made by the same
person" clause and names both triggers. `:48` reads "All the ink is
handwritten, and on a self-copied page all of it is the human's". `:52` answers
the deviation question for a scribed page — absolutely for content,
presumptively for structure, never queried back. `:89` scopes the
description anti-pattern, and `:95` adds the scribe-as-second-contributor line.
`design.md` §9 rung 1 carries the scribe case on both cascades.

### Recommendation 3 — the metadata: landed, minus one line

`design.md` gained §10, specifying the canvas `lang=`, `setTitle` to the
sheet's printed title with the serial-disclosure-kit constant as its one
exception, `setViewerPreference('DisplayDocTitle', 'true')`, and the rule that
metadata is never a continuity carrier — mirrored into `scan-back`.
`SKILL.md` Step 4 restates the three, pointing at §10 rather than re-deriving
them. `docs/specimen.py` sets all three and the specimen was rebuilt. Verified
on the committed `docs/specimen.pdf` through the existing `pdfplumber`
dependency: catalog `/Lang` is `b'en-US'`, Info `/Title` is
`'Paper Session — Design Specimen'`, and `/ViewerPreferences` resolves to
`{'DisplayDocTitle': True}`. `verify_layout.py` was left alone, as specified.

Two details worth recording. The specimen takes a document-level name in the
neutral-constant shape rather than a sheet title, because it is neither a sheet
nor a kit but three pages from two sessions; `specimen.py` says so in a comment
so the deviation is not read as a §10 violation. And **the one line of this
recommendation that did not land**: unknown 1 asked that Step 4 say which of
`lang=` and the private-API fallback to use, so the choice is not rediscovered
later. Neither §10 nor Step 4 names a fallback. On reportlab 5.0.1 the keyword
exists and nothing forces the question; the first runtime without it will have
to ask it from scratch.

### The unknowns

**Resolved and mechanized — unknown 6, the scribe clause across two skills.**
This is the one `0002` flagged and could not close. It is closed as far as a
presence gate can close it: `build.sh` gained `check_couplings`, four
`grep -qF` assertions over the two named literals in the two named documents,
run on every build whichever skill is named and exposed standalone as
`./build.sh --check-couplings`. Verified on this tree — `a group format`
appears twice in `scan-back/SKILL.md` and three times in `design.md`,
`a scribe speaks for the author` once in each, and the gate exits 0. Verified
as a real discriminator, too, which is the part a presence gate usually gets
away without: in a scratch copy with the design.md sentence reworded to "a
scribe stands in for the author", the gate exits 1 and names the string and the
file. The meaning-drift half stays what the brief says it is — a field
question.

**Resolved here, not where it matters — unknown 1, `lang=` in the skill's
runtime.** `reportlab 5.0.1` on this machine has `lang` in
`Canvas.__init__`, and the three fields land in the file as shown above. The
unknown was about the environment the skill is *loaded* into, which is not this
one, and the fallback line that would have made the answer portable is the line
that did not land. The brief's note for whoever writes an assertion is
confirmed and still worth keeping: `pdf.doc.catalog.get('Lang')` returns bytes,
`pdf.metadata['Title']` returns a str.

**Partially answered by reading, not by running — unknown 5, the format-scoped
trigger.** The edited text routes on the observable signal rather than on hand
count, in the words quoted under recommendation 2 above, and the scribe
paragraph states in its own sentence that the group narrowing does not reach
it. That is the text doing what it was asked to do. No brainwriting return was
actually run against it, orphaned or otherwise, so the behavioural half is
unmeasured.

**Not run — unknowns 2, 3, 4, 7, and 8.** All five terminate in a person this
environment does not contain: a screen-reader user (2 and 3), someone deciding
whether 50-75 words is absurdly tight on a keyboard or a slate (4), a real
dictated return to check a transcript against (7), and anyone at all on this
path (8). Unknown 7 is the sharpest of them, being the behavioural risk rather
than a completion question, and the two things standing between it and the
failure it names are both prose: `scan-back:38`'s "Receive it; never conduct
it" and the new `paper-session` anti-pattern with its `prompt-craft.md:108`
counterpart. Whether the model obeys them is untested.

`evidence.md` Part Three is where 2, 3, 4, 7, and 8 land, in that tier's format
and under the three-independent-reports threshold that already governs it. Part
Three is still empty. Until it is not, the non-visual return ships as a
reasoned design with no completion data behind it — the same standing the
printed sheets and the notebook fallback have.
