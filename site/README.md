# site/

The promotional website for `paper-session` and `scan-back`. Fully static,
built by one Python script with no dependencies, published to GitHub Pages.

```bash
python3 site/build.py                 # build to site/dist/
python3 site/build.py --serve 8000    # build, then serve it at localhost:8000
```

`dist/` is a build artifact. It is wiped and rewritten on every run, and it is
git-ignored (`site/.gitignore`) — never edit anything inside it.

---

## The one architectural rule

**Nothing on this site is hand-copied from the repo.**

`CLAUDE.md` binds install directions to README §Install *and nowhere else*, and
this build script is what makes that rule mechanical rather than a promise.
Every piece of repository content on the site — the install directions, the
compatibility ledger, the whole text of `scan-back/SKILL.md`, the evidence
limitations, the three numbers, even the printed footer line — is read out of
its source file at build time and converted to HTML in `build.py`.

If you are about to type repo prose into a template, stop and add an extractor
to `build_repo_context()` instead. Site copy that is genuinely the website's
own voice (headings, connective tissue, button labels) you write yourself; the
repo's words stay the repo's.

Corollaries:

- No backend, no API keys, no hosted renderer, no analytics that needs a cookie
  banner. If the site dies, nothing in the loop dies with it.
- Standard library only. The repo's dependencies are reportlab and pdfplumber;
  the website is not allowed to add a third. No Node, no jinja2, no bundler.

---

## Build behaviour you can rely on

| | |
|---|---|
| Idempotent | Same inputs, byte-identical `dist/`. No timestamps are emitted. |
| Fails loudly | A missing README §Install, an empty ledger, an unparseable three-numbers block, or an unknown template key stops the build with one clear sentence. It never emits an empty page in place of missing content. |
| Survives mid-edit files | Section lookup is forgiving about heading level, case, and appended parentheticals; a genuinely renamed section fails rather than silently blanking. |
| Warns, doesn't crash, on absent specimens | `--allow-missing-assets` downgrades missing `docs/specimen.pdf` / `docs/sheet-*.png` to warnings and sets `specimen_available` / `sheet_count` empty so templates can say so honestly. |
| Checks its own links | Every internal `href`/`src` is resolved against `dist/` after the build. Dangling links warn; `--strict` makes them fail. |

Flags: `--out DIR`, `--allow-missing-assets`, `--strict`, `--serve PORT`.

---

## The page-authoring contract

### 1. A page is one template file

`site/templates/<slug>.html`. Files whose name starts with `_` are partials, not
pages. A template contains **only the page body** — the shell (`<html>`, head,
masthead, nav, footer) comes from `_base.html`.

Every page template starts with a front-matter comment:

```html
<!--page
title: Get a sheet
description: Print a real specimen sheet. No account, no install.
nav_label: Get a sheet
nav_order: 10
-->
<section class="band air-1">
  <div class="wrap measure">…</div>
</section>
```

| Key | Required | Meaning |
|---|---|---|
| `title` | yes | Browser title and `og:title`. The home page shows `Paper Session`; every other page shows `<title> — Paper Session`. |
| `description` | yes | `<meta name="description">` and `og:description`. One sentence. |
| `nav_label` | no | Include the page in the site nav. Omit and the page exists but is unlisted. |
| `nav_order` | no | Integer, ascending. Defaults to 999. |
| `slug` | no | Defaults to the filename stem. |
| `output` | no | Defaults to `<slug>/index.html` (and `index.html` for slug `index`). |
| `body_class` | no | Extra class on `<body>`. |

Any other key you add is available in the template as `{{ yourkey }}`.

Output is a directory index, so the page's URL is `/<slug>/`. Nothing is
hard-coded to a domain: **always prefix internal links with `{{ base }}`**, which
is the relative path back to the site root (`""` on the home page, `"../"` one
level down). `{{ home_url }}` is the same thing but never empty — use it for a
link to the front page.

### 2. Template syntax

A deliberately tiny substitution templater. Four constructs, that is all:

| Construct | Behaviour |
|---|---|
| `{{ key }}` | Insert the value **raw**. Every repo fragment is already HTML. |
| `{{ key\|e }}` | Insert HTML-escaped. Use inside attributes. |
| `{% if key %}…{% else %}…{% endif %}` | Truthy = non-empty and not `0`/`false`. Nests. |
| `{% include "_partial.html" %}` | Inline another template from `templates/`. |

There are no loops and no expressions, on purpose. If a page needs repetition,
generate the HTML in `build.py` and expose it as one key — that is how the nav,
the chips, the specimen gallery and the three numbers are built.

**An unknown `{{ key }}` fails the build** and prints the key name. That is the
feature: you cannot ship a page with a silently empty region.

### 3. Context keys available in every template

Page and site:

`base` · `home_url` · `page_slug` · `is_home` · `nav` · `title` · `description` ·
`body_class` · `repo_url` · `raw_url` · `specimen_url` · `hero_url` ·
`hero_present` · `hero_file` · `specimen_available` · `sheet_count`
(plus every key from your own front matter). `_base.html` additionally gets
`content`.

Repo content, all pre-rendered HTML unless noted:

| Key | Source | Notes |
|---|---|---|
| `repo_install_html` | README §Install, above the ledger | the install directions themselves |
| `repo_install_note_html` | README §Install, below the ledger table | the "directions live here only" note |
| `repo_ledger_heading` | README §Install | plain text, escaped |
| `repo_ledger_table_html` | README §Install | the full four-row table, in a `.scroller` |
| `repo_ledger_json` | README §Install | JSON: `{headers, rows[{agent, agent_html, install, install_html, loop, loop_html, status, chips}]}`; a row reading "Same as above" inherits the row above it |
| `repo_ledger_chips_html` | derived | `<button class="chip" data-row="N">` set |
| `repo_sheets_html` | README specimen table | three `<figure class="sheet">`, README's own alt text and captions |
| `repo_prompts_html` | README §Using it | the three example prompts, `<ul class="prompts">` |
| `repo_one_rule` / `repo_one_rule_html` | README §The one rule… | the question; the two bullets |
| `repo_pen_protocol_html` | README §The pen protocol | whole section |
| `repo_ink_table_html` / `repo_mark_table_html` | README §The pen protocol | the two tables separately |
| `repo_scanback_html` | `scan-back/SKILL.md` | the whole file, front matter stripped, headings shifted one level |
| `repo_scanback_name` / `repo_scanback_description` | its front matter | escaped text |
| `repo_scanback_raw` | `scan-back/SKILL.md` | escaped markdown, for a copy-paste `<pre>` |
| `repo_scanback_bytes` / `repo_scanback_words` / `repo_scanback_words_approx` | measured | `words_approx` is rounded to the nearest hundred |
| `repo_scanback_raw_url` | derived | raw.githubusercontent URL |
| `repo_paper_session_description` / `repo_paper_session_bytes` | `paper-session/SKILL.md` | |
| `repo_stop_line` | `paper-session/SKILL.md` | `Printed. Go think.` |
| `repo_numbers_html` / `repo_numbers_json` | `evidence.md` §Three numbers | the three figures and one line each |
| `repo_thesis` | `evidence.md` §Three numbers | the thesis sentence, sentence-cased |
| `repo_limitations_html` | `evidence.md` §What the research does NOT support | the numbered list |
| `repo_limitations_count` | derived | how many items that list has |
| `repo_footer_line` | `design.md` §5 | `SCAN IT BACK TO CONTINUE.` |
| `repo_return_half_html` | README §Install | the "the return half travels further" paragraph, alone |
| `repo_paste_route_html` | README §Install | the "if your AI can't install skills at all" paragraph |
| `repo_paste_sentence` / `repo_paste_sentence_html` | README §Install | the load-bearing sentence a paste-channel user types; plain (escaped) and as a blockquote |
| `repo_paste_honesty_html` | README §Install | "the sentence is load-bearing…", including what the paste channel does not get |
| `repo_accessible_path_html` | README §Install | the dictated path for someone who cannot read the printed page |
| `repo_absences_html` | README §What comes out of the printer | "Notice what is **not** there…" |
| `repo_anatomy_html` | README §Anatomy of a sheet | the ASCII sheet diagram, three voices, hard floors |
| `repo_hard_floors_html` / `repo_three_voices_html` | same section | those two paragraphs alone |
| `repo_patterns_html` | README §The pattern library | whole section |
| `repo_specimen_html` / `repo_specimen_json` | `docs/specimen.py` | the three specimen pages' own intent lines, parsed with `ast` from the `header()` calls (a title built from an f-string reports as absent rather than as half a title) |
| `repo_scanback_full_raw` | `scan-back/SKILL.md` | escaped markdown **including** front matter (`repo_scanback_raw` is body-only) |
| `repo_scanback_unprinted_html` | `scan-back/SKILL.md` §Step 1 | the "Unprinted pages" paragraph |
| `repo_dictation_html` | `prompt-craft.md` §10 | the whole dictated-card rule |
| `repo_card_format_html` / `repo_card_budget_html` | `prompt-craft.md` §10 | the two-part card format; the "too print-shaped" budget rule |
| `repo_notebook_translation_html` | `page-patterns.md` §Notebook translation | which patterns survive being copied out |
| `repo_formats_html` / `repo_formats_intro_html` / `repo_formats_count` / `repo_formats_json` | `page-patterns.md` §Named session formats | the whole section; its intro; how many; structured |
| `repo_format_<slug>_html` | same | one key per named format — `repo_format_premortem_html`, `repo_format_after_action_review_html`, `repo_format_teach_back_sheet_html`, … Quote a format's gate instead of paraphrasing it |
| `repo_evidence_intro_html` | `evidence.md`, above Cluster 1 | the brief's opening paragraph |
| `repo_evidence_walking_html` · `repo_evidence_cluster_4_html` · `repo_evidence_cluster_5_html` | `evidence.md` | the sections behind the three front-page figures |
| `repo_evidence_tension_html` | `evidence.md` §The tension you should address head-on | where the brief argues against its own design |
| `repo_evidence_unprinted_html` / `repo_evidence_unread_html` | `evidence.md` | the two paths with no research under them |
| `repo_field_reports_html` | `evidence.md` §Part Three | the empty tier |
| `repo_evidence_clusters_html` / `repo_evidence_cluster_count` | derived | one `<li>` per cluster: its Part, its heading, and any counterweight paragraph quoted verbatim |
| `repo_numbers_linked_html` | derived | the three figures, each linking to `<base>evidence/#number-N`. Use this wherever the figures appear away from the evidence page |
| `repo_ledger_verified_count` / `repo_ledger_row_count` | derived | counted, never asserted in prose — "exactly one row is verified" is the kind of sentence that goes quietly false |
| `repo_example_reply_html` | `docs/worked-example.md` | the unedited reply in the return-trip worked example; empty until the file exists |
| `repo_one_rule` … | | |

`repo_ledger_json` rows now also carry `extra: [{header, value, value_html}]` —
**every ledger column past the third**, so a column added to the README table
(as `Also install` was) reaches the chip answer instead of vanishing. A row whose
cell reads "Same as above" inherits that column from the row above, the same way
the loop status does.

Two more keys come from the asset scan rather than the repo: `example_present`
and `example_photo_url` (the worked-example photograph, `site/static/return-example.jpg`),
alongside `hero_present` / `hero_url`. And `evidence_url` is the URL of the
limitations page, so no template has to hard-code the slug that `build.py`
generates the `#number-N` anchors against.

Keys marked optional in `build.py` come back as empty strings when their source
section is missing (the build warns). Guard them with `{% if %}` if your page
would look broken without them.

### 4. Asking for repo content that isn't in the list

Add it to `build_repo_context()` in `build.py`:

```python
section = extract_section(readme, "The pattern library", "README.md",
                          required=False)
ctx["repo_patterns_html"] = md_to_html(section, heading_offset=1) if section else ""
```

Helpers available: `read_repo(path, required=)`, `extract_section(md, heading,
source, required=)`, `find_first_table`, `parse_table`, `strip_front_matter`,
`md_to_html(md, heading_offset=)`, `inline_md`, `plain_text`, `esc`.

Choose `required=True` only for content whose absence should stop the build —
content a page is fundamentally about. Everything decorative gets
`required=False` plus an `{% if %}` in the template, because other agents edit
these files and a warning is better than a broken deploy.

The markdown converter handles the subset the repo actually uses: ATX headings,
fenced code, GFM pipe tables, ordered/unordered lists with one level of nesting,
blockquotes, thematic breaks, bold, italic, strikethrough, inline code, links
and images. Repo-relative links are rewritten to GitHub blob URLs; `docs/`
specimen assets are rewritten to the site's own copies. Tables come out inside
`<div class="scroller">` so the body never scrolls sideways.

### 5. Partials

`{% include "_print-note.html" %}` — **the production note the site owes every
visitor**: *print at actual size, scaling off*. Browser print dialogs default to
fit-to-page, which shrinks a 54pt-margin sheet by three to six percent and walks
the smallest labels below their measured legibility floor. Include it anywhere
a person is about to print something: the specimen download, the install page,
any page that hands over a PDF. This unglamorous sentence probably protects more
completed loops than any copywriting on the site.

### 6. Planned pages and stubs

`PLANNED_PAGES` in `build.py` lists the pages the site expects to have. Any
planned slug with no template gets an obviously-marked stub page so that no link
on the site points into a hole. **Write `templates/<slug>.html` and the stub
disappears** — you do not need to touch `PLANNED_PAGES` unless you are adding a
page nobody has planned, in which case add it there so others can link to you
before you land.

Currently planned: `get-a-sheet` (10), `no-printer` (20), `scan-back` (30),
`install` (40), `evidence` (50). The order is the landing page's
ascending-commitment order; keep nav and onramps in step.

**All five are written, so the build currently emits no stubs.** Three of them
live under a filename that is not their slug, which is fine and deliberate —
the front matter's `slug:` is what decides the URL:

| Template | Slug and URL |
|---|---|
| `templates/sheets.html` | `get-a-sheet` → `/get-a-sheet/` |
| `templates/return-trip.html` | `scan-back` → `/scan-back/` |
| `templates/limitations.html` | `evidence` → `/evidence/` |

`collect_pages()` fails the build if two templates claim one slug, which is the
intended behaviour: do not add `templates/scan-back.html` or
`templates/evidence.html` alongside the two that already claim those slugs.
`/evidence/` in particular is load-bearing — `build.py` generates the landing
page's three figure links against `EVIDENCE_SLUG` and they land on `#number-1`,
`#number-2` and `#number-3` on that page.

---

## The design system

Read `paper-session/references/design.md` before you style anything. **The sheet
is the brand**; the site does not get a second identity. Everything in
`static/style.css` traces back to that file, including the rule weights:

```
print 2pt datum rule     ->  --rule-datum: 3px      (2pt = 2.67px at 96dpi)
print 1.6pt closing rule ->  --rule-close: 2px
print 0.5pt hairline     ->  --rule-hair:  1px
print gray value 0.NN    ->  --g-NN
```

### Tokens

Neutrals — ink is a cool graphite, paper carries a faint warm bias; deliberately
neither pure mid-grey nor cream:

```
--g-00 #191c1e   --g-12 #24282a   --g-20 #33383a   --g-30 #4a5052
--g-40 #5c6264   --g-45 #656b6d   --g-50 #7b8183   --g-55 #a0a5a3   --g-60 #c3c6c2
--paper #f1f0ec  --surface #f8f7f4  --surface-2 #eceae5
```

Semantic aliases: `--ink` (g-00), `--ink-2` (g-30, secondary prose),
`--ink-quiet` (g-45, labels; 4.75:1 on `--paper`, the small-text floor),
`--ink-faint` (g-50, 3.5:1 — **nothing meaningful goes lighter**: decoration,
underlines and rules only, the screen equivalent of the print system's 50%
floor), `--guide` (g-60, hairlines only, never type).

Pen channels: `--pen-red` `--pen-green` `--pen-blue` `--pen-black`.

Type: `--font-serif` / `--font-sans` / `--font-mono` (IBM Plex, from Google
Fonts, each with a real fallback stack). Sizes `--fs-provocation`, `--fs-title`,
`--fs-lead`, `--fs-body`, `--fs-machine`, `--fs-small`, `--fs-label`.

Space: `--s1` … `--s9`; layout `--page-max`, `--gutter`, `--measure` (65ch).

### The three voices, never blended

- **Serif asks.** Running prose, provocations (`.provocation`), the site's own
  questions (`.question`), intent lines (`.intent`), asides (`.aside`).
- **Mono is the machine.** On this site Mono means exactly one thing: *these
  words are quoted verbatim out of the repository*. Wrap them in `.machine` with
  a `<span class="caption">` naming the source — that caption plus its 2px
  underline is the sheet's own `I PROPOSE` molecule. Never set marketing copy in
  Mono, and never set repo text in anything else.
- **Tracked Sans caps is infrastructure.** Nav, `.label`, buttons, footers,
  table headers. Furniture, not a voice.
- Nothing on the site imitates handwriting. Ever.

### Structure

- `.datum` — the 3px rule that opens the site, as it opens every sheet.
- `.open-territory` — the 2px closing rule, a label, and real emptiness
  (`.open-territory__field`, 34vh of nothing). Close long pages with it.
- **Decompression downward.** Pages run tightest at the top and open out. Bands
  take ascending air: `.air-1` → `.air-2` → `.air-3` → `.air-4` down the page.
  A page that does this is quoting the artifact rather than illustrating it.
- Layout wrappers: `.wrap` (max width + gutter), `.measure` (65ch), `.band`,
  `.stack` / `.stack-4`, `.scroller` for anything wide.
- Components: `.btn` / `.btn--primary`, `.chip`, `.onramps` / `.onramp`,
  `.sheets` / `.sheet`, `.numbers` / `.number`, `.print-note`, `.prose`,
  `.pen-key`, `pre.code`.
- Promoted components (§18 of `static/style.css`), all of them originally
  page-scoped and now shared:
  `.disclosure` (a `<details>` whose summary is infrastructure) ·
  `.status` (a live-region feedback line; the sentence carries the state and
  the coloured rule beside it is redundant) ·
  `.placeholder` / `.placeholder__key` / `.placeholders` (a pending asset —
  dashed, red, and the word "placeholder" always in the text) ·
  `.ruled-list` / `.ruled-list__item` (counter-numbered ruled prose) ·
  `.source-entry` (an anchored claim with its source quoted under it;
  `:target` thickens the rule rather than tinting it) · `.cluster-index` ·
  `.routes` / `.route` (equal peers, no primary, no badge) ·
  `.verdict` + the `.ledger-table` status box · `.specimen-plate` ·
  `.specimen-intents` · `.anatomy` (a named-parts key) · `.filebox` (a long
  verbatim file, wrapped and bounded) · `.say` / `.say__copy` / `.say__hint`
  (a copyable sentence, set in the asking voice because the words are the
  visitor's) · `.note` / `.note--caution` · `.openers` / `.opener` /
  `.situation` · `.sr` (visually hidden) · `.after-lead` / `.after-block` /
  `.after-close` / `.after-note` / `.machine--wide`.
- **No template contains a `<style>` or `<script>` element.** A page body
  cannot reach `<head>`, so a page-scoped `<style>` is non-conforming HTML
  even though browsers honour it, and a second page wanting the same component
  would reinvent it. Anything you would have put inline belongs in
  `static/style.css` (add to §18) or `static/site.js`.
- Flush left. No centred layouts, no rounded corners, no fills or tint panels
  beyond the barely-there `--surface` behind code, no drop shadows.

### Colour law

Grayscale carries the page; the restraint *is* the brand. Colour appears only
where it encodes pen intent — red review, green go, blue do, black notes — and
**never as the sole carrier of meaning** (WCAG 1.4.1; roughly 1 in 12 men have
red-green CVD). The primary button's blue underline is decoration on top of a
label that already says what it does; the hero placeholder is red *and* says
"placeholder" in words. Keep that discipline.

### Themes

Three states, all supported. The complete light palette lives on bare `:root`;
`@media (prefers-color-scheme: dark)` guarded as `:root:not([data-theme="light"])`
redefines only the tokens; `:root[data-theme="dark"]` redefines them again so the
footer toggle wins in both directions. **Never declare a colour only inside a
media block**, and give any new full-bleed surface an explicit token background.

### Accessibility floor

This project cites accessibility research in its own evidence base; a site that
fails the basics would be embarrassing.

- Visible focus: a 2px `--focus` outline with offset. Do not remove it.
- `prefers-reduced-motion: reduce` is honoured globally. Do not add motion that
  ignores it.
- Running text near 65 characters (`.measure`).
- Wide content lives in `.scroller`; the body never scrolls sideways.
- One `<h1>` per page, headings in order, real landmarks (`main`, `nav`,
  `footer`), a skip link, alt text on every image.
- **Everything must work with JavaScript off.** `static/site.js` is progressive
  enhancement only. It un-hides the "what are you using?" chips and collapses
  the ledger table that is otherwise open; it shows the theme toggle; and it
  reveals the copy buttons — the per-sentence ones (`[data-copy]`, paired with
  a `#copy-status` live region on the page) and the whole-file one on the
  return-trip page (`[data-copy-file]`). Every one of those buttons ships
  `hidden` and is revealed only where writing to the clipboard can work, so a
  browser that cannot copy never shows a control that would do nothing. With JS
  off you get the full honest ledger table, the system theme, the whole of
  `scan-back/SKILL.md` sitting open and selectable, and every sentence as plain
  selectable text. That is a perfectly good page.
- Contrast floors are enforced by token, in both themes: `--ink-quiet` (4.75:1
  light / 5.87:1 dark) is the floor for anything that renders as type,
  including ordinal counters. `--ink-faint` is decoration and underlines only,
  and `--guide` never sets a type colour.

---

## Content rules the project enforces on itself

These are not style preferences; they are the project's own invariants applied
to its marketing. A page that breaks one is wrong even if it converts.

1. **Never say a session is quick, easy, or fast.** No time estimates as a
   selling point, no "try it in 90 seconds". `prompt-craft.md` §9 and both
   anti-pattern lists ban it, and effort-read-as-ineffectiveness is the
   documented reason people abandon the method. A paper session will feel less
   productive than the same hour on screen, including on the days it is most
   productive. Do not promise ease and do not apologise for effort.
2. **No AI-generated imagery anywhere.** The skill bans it on sheets; on a
   marketing page it is worse. Photographs of real artifacts, the specimen
   renders, or nothing.
3. **No testimonials** — there are none — and **no completion statistics**;
   Part Three of `evidence.md` is empty. Completion rate is the metric that
   matters and nobody has data yet.
4. **No waitlist, no newsletter capture, no star-the-repo CTA above the fold.**
   No metric of success that counts installs or stars.
5. **Honest status stays honest.** "Installs cleanly, loop untested" is the most
   credible sentence the project has. Never upgrade a claim, and let the ledger
   speak for itself rather than paraphrasing it upward.
6. **The pen half is the product.** The single primary call to action is *get a
   sheet*. A front door reading "AI reads your handwriting" would be selling
   commodity OCR and inverting the thesis; the return trip is the prominent
   second door, for people who already have paper.

---

## Pending assets

Two photographs and one transcript do not exist yet. Every one of them has a
visible, dashed, red placeholder that names its own path on the page, so the
site never quietly renders a hole. Nothing here may be filled with an
illustration or a generated image.

| What | Where it goes | What appears until then |
|---|---|---|
| The hero photograph | `site/static/hero.jpg` (`.jpeg` / `.png` / `.webp` also work; first found wins) | the placeholder panel on the landing page |
| The worked-example photograph | `site/static/return-example.jpg` (same alternatives, `return-example.*`) | the left placeholder on `/scan-back/` |
| The worked-example reply | `docs/worked-example.md`, in the repo | the right placeholder on `/scan-back/` |

Drop each file in and rebuild; the placeholder disappears on its own and no
template changes. The two worked-example slots are paired: the photograph alone
swaps the left panel and leaves the right one asking for the reply.

**Shot list for the worked-example photograph:** a phone shot of a completed
page — handheld, slightly angled, on whatever surface it was filled in on. Two
or three inks, at least one strike, one circled item, a margin note running up
the side. Not a flatbed scan, not a flat-lay, no screen in the frame. **And the
reply must be pasted unedited**, including anything the assistant read wrong: a
worked example that has been tidied up is an advertisement, not evidence. Update
the `alt` text in `templates/return-trip.html` to describe the real photograph
once it exists.

---

## The hero photograph

The landing page opens on a full-bleed photograph of a real sheet. **It does not
exist yet** — the maintainer is shooting it. Until then `build.py` renders a
dashed, red, unmistakable placeholder occupying the same 3:2 slot the
photograph will fill (it grows rather than clipping the note on a narrow
screen).

**To make it live: save the file as `site/static/hero.jpg` and rebuild.** That
is the whole procedure. (`hero.jpeg`, `hero.png` and `hero.webp` also work; the
first one found wins.) Nothing else changes, and the placeholder disappears on
its own.

Shot list:

- **The subject is a completed sheet**, not a blank one. A blank sheet looks
  unfinished on purpose; the finished design is the page with handwriting on it.
- **Two or three inks visible.** A black hand, at least one red strike or
  circle, ideally one blue instruction. The pen must be the highest-contrast
  thing in the frame — that is the whole design principle, photographed.
- **Real marks.** Crossings-out, a margin note running up the side, a slot left
  empty. Not a neatly completed form.
- **Photograph it badly, on purpose.** A table, a kitchen counter, a patio.
  Available light, slight angle, a mug or a pen in frame is fine. Studio
  lighting, a flat-lay grid, or a laptop in shot would all be lying about where
  this happens.
- **No screens in the frame.**
- **Landscape, 3:2**, at least 2400px wide, exported around 200–400 KB (the site
  ships no image pipeline). Leave the lower-left third relatively quiet: the
  headline and buttons sit over it on a dark scrim.
- Update the `alt` text in `templates/index.html` to describe the actual
  photograph once it exists.

---

## Deploying to GitHub Pages

The build has no dependencies, so the workflow is short. The maintainer needs to
add this as `.github/workflows/site.yml` (nothing under `site/` can create it),
and set Settings → Pages → Source to **GitHub Actions**:

```yaml
name: site
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python3 site/build.py --strict
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site/dist
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

`dist/.nojekyll` is written by the build, so Pages serves the directory as-is.
Because every internal link is relative, the site works unchanged at
`welovejeff.github.io/paper-session/`, at a custom domain, or opened from the
filesystem.

---

## Troubleshooting

| Message | What to do |
|---|---|
| `could not find the §Install section in README.md` | The heading was renamed, or the README is mid-edit. Update the extractor; do not restate the section in a template. |
| `README §Install has no compatibility table` | Same. The ledger is rendered, never invented. |
| `specimen assets are missing from the repo` | Run `python3 docs/specimen.py`, or build with `--allow-missing-assets` while someone else regenerates them. |
| `<template> uses unknown template keys: …` | Typo, or you need a new extractor in `build_repo_context()`. |
| `internal links point at nothing` | Either the target page is not planned yet (add it to `PLANNED_PAGES`) or the link is missing its `{{ base }}` prefix. |
