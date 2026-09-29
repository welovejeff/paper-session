# site/

The public website for `paper-session` and `scan-back`, served at
paper-session.com. Fully static, built by one Python script with no
dependencies, published to GitHub Pages.

```bash
python3 site/build.py                 # build to site/dist/
python3 site/build.py --serve 8000    # build, then serve it at localhost:8000
```

`dist/` is a build artifact. It is wiped and rewritten on every run, and it is
git-ignored (`site/.gitignore`). Never edit anything inside it.

---

## What the site is for

A visitor should be able to get in and see what to do. Most will do two
things: watch the film, then copy the instructions into the AI chat they
already use. Everything on the site serves that path. Documentation lives in
the repo and the site links to it.

### Four pages

| URL | Template | Job |
|---|---|---|
| `/` | `index.html` | What it is. The film, then the copy button, then the loop in four lines. |
| `/how-it-works/` | `how-it-works.html` | One session walked through, the page as printed and as photographed, three example lines, coming back. |
| `/install/` | `install.html` | Chat app, terminal, the ledger verdicts, the no-install path (`#no-printer`), and the scan-back file (`#scan-back`). |
| `/research/` | `research.html` | The honest limits in three statements, and the labelled slot where field notes will go. |

Word budgets for site-authored copy: Home ~400, How it works ~300, Install
~250, Research ~300, under 2,000 in total. If a section cannot be said in
three sentences, it belongs in the repo.

### Retired pages redirect

`REDIRECTS` in `build.py` writes a small moved page (noindex, canonical,
0-second meta refresh, and a real link) for each retired slug:

| Old | New |
|---|---|
| `/get-a-sheet/` | `/` |
| `/first-session/` | `/how-it-works/` |
| `/scan-back/` | `/install/#scan-back` |
| `/no-printer/` | `/install/#no-printer` |
| `/evidence/` | `/research/` |

The build refuses a retired slug that comes back as a live page, a target that
is not a live page, and (under `--strict`) a `#fragment` target whose id is
missing. So `install.html` must keep `id="scan-back"` and `id="no-printer"`.

`/get-a-sheet/` was removed on 2026-09-29. It printed a generic sheet that
knew nothing about the visitor's work, so it proposed nothing: a bad version of
a paper session, sitting at the top of the funnel. A real session is built
from the visitor's own work, so every route now leads there. Do not bring back
a generic printable sheet or a "print the specimen" call to action. The sheet
CSS and the print gate (`sheet: true` in front matter) are still in
`build.py` and `static/style.css`; no page declares it, so the gate does not
run.

---

## The single-source rule

**Commands, bundle links, ledger verdicts and the scan-back text come from the
repo at build time. Whole documents are linked, never embedded.**

`CLAUDE.md` binds install directions to README §Install and nowhere else.
`build.py` makes that mechanical: the three install commands, the two `.skill`
links, the ledger verdicts and the full text of
`scan-back/SKILL.md` (behind its copy button) are read out of their source
files and handed to templates as keys. Never type a repo command into a
template.

Everything else from the repo is a link to GitHub. Build those links in
`build.py` with `repo_doc_url()`, which fails the build when the file is gone
or the named heading no longer exists, instead of typing a URL into a
template.

Site copy in the website's own voice (headings, connective sentences, button
labels) you write yourself.

Corollaries:

- No backend, no API keys, no hosted renderer, no analytics that needs a cookie
  banner. If the site dies, nothing in the loop dies with it.
- Standard library only. No Node, no jinja2, no bundler.

---

## Build behaviour you can rely on

| | |
|---|---|
| Idempotent | Same inputs, byte-identical `dist/`. No timestamps. CI builds twice and diffs. |
| Fails loudly | A missing README §Install, a missing command block, a ledger without "The loop today", a repo link whose heading is gone, a missing `copy-instructions.txt`, or an unknown template key stops the build with one clear sentence. |
| Survives mid-edit files | Section lookup forgives heading level, case and appended parentheticals; a genuinely renamed section fails rather than silently blanking. |
| Warns on an absent render | `--allow-missing-assets` downgrades a missing `docs/sheet-deep-react.png` to a warning and sets `sheet_count` to `0`, which `{% if %}` treats as false. |
| Checks its own links | Every internal `href`/`src`/`poster` is resolved against `dist/`. Dangling links warn; `--strict` fails. |

Flags: `--out DIR`, `--allow-missing-assets`, `--strict`, `--serve PORT`.

---

## The page-authoring contract

### 1. A page is one template file

`site/templates/<slug>.html`. Files whose name starts with `_` are partials.
A template contains only the page body; the shell (head, masthead, nav,
footer) comes from `_base.html`. Every page starts with front matter:

```html
<!--page
title: How it works
description: One paper session, start to finish.
nav_label: How it works
nav_order: 10
-->
```

| Key | Required | Meaning |
|---|---|---|
| `title` | yes | `<title>` and `og:title`. Home shows `Paper Session`; other pages show `<title> · Paper Session`. |
| `description` | yes | `<meta name="description">` and `og:description`. One sentence. |
| `nav_label` | no | Include the page in the masthead nav. Home has none; the wordmark is its link. |
| `nav_order` | no | Integer, ascending: How it works 10, Install 20, Research 30. |
| `slug` | no | Defaults to the filename stem. |
| `body_class` | no | Extra class on `<body>` (Home uses `door home`). |

Output is a directory index, so the URL is `/<slug>/`. Always prefix internal
links with `{{ base }}` or use a `*_url` key; nothing is hard-coded to a
domain, so the site also works under a subpath or from the filesystem.

HTML comments in a template are notes for maintainers. `parse_page()` strips
them from the body, so they never reach `dist/`; write them freely, and put
nothing in one that a visitor needs.

### 2. Template syntax

| Construct | Behaviour |
|---|---|
| `{{ key }}` | Insert the value raw. Repo fragments are already HTML-escaped. |
| `{{ key\|e }}` | Insert HTML-escaped. Use inside attributes. |
| `{% if key %}…{% else %}…{% endif %}` | Truthy = non-empty and not `0`/`false`. Nests. |
| `{% include "_partial.html" %}` | Inline another template. |

No loops and no expressions, on purpose. Repetition is generated in `build.py`
and exposed as one key. An unknown `{{ key }}` fails the build.

### 3. Context keys the pages use

Page and site:

| Key | Meaning |
|---|---|
| `base` · `home_url` | Relative path to the site root (`""` / `./` on Home, `../` one level down). |
| `how_it_works_url` · `install_url` · `research_url` | Base-relative page links. Add `#scan-back`, `#no-printer` or `#where-it-stands` to `install_url` for those sections. |
| `copy_instructions_url` | The text file the primary call to action copies; also its href with JS off. |
| `copy_instructions` | The file's text, put on every page by `_base.html` as `#copy-instructions-text`. |
| `nav` · `is_home` · `title` · `description` · `body_class` | Shell. |
| `site_url` · `page_url` · `og_image_url` | Absolute URLs, for head tags only. |
| `repo_url` | `https://github.com/welovejeff/paper-session`. |
| `film_present` · `film_url` · `film_poster_present` · `film_poster_url` · `film_captions_present` · `film_captions_url` | The Home film, from `site/static/film.mp4`, `film-poster.jpg`, `film-captions.vtt`. |
| `hero_present` · `hero_url` | `site/static/hero.jpg`: the film's fallback and the social image. |
| `example_present` · `example_photo_url` | `site/static/return-example.jpg`, the worked page on How it works. |
| `sheet_count` | `1` when `docs/sheet-deep-react.png` was copied to `sheets/`, else `0`. |

Repo content:

| Key | Source | Notes |
|---|---|---|
| `repo_install_npx_cmd` · `repo_install_clone_cmd` · `repo_install_pip_cmd` | README §Install fenced blocks | Escaped. Put directly inside `<pre class="code"><code>` with no whitespace. |
| `repo_bundle_links_html` | README §Install | The two `.skill` links with the README's hrefs. Wrap in `<p class="bundle-links">`. |
| `repo_ledger_verdicts_html` | README ledger | `<ul class="verdicts">`: each agent cell and the bold verdict opening "The loop today", verbatim. |
| `repo_ledger_verified_count` · `repo_ledger_row_count` | README ledger | Counted from the same verdicts `repo_ledger_verdicts_html` lists, never asserted in prose. |
| `repo_ledger_anchor_url` · `repo_readme_install_url` | README | GitHub links to the ledger heading and §Install. |
| `repo_scanback_raw` · `repo_scanback_raw_url` · `repo_scanback_words_approx` | `scan-back/SKILL.md` | The body behind the copy button, the raw file, its word count to the nearest hundred. |
| `repo_stop_line` | `paper-session/SKILL.md` | `Printed. Go think.` |
| `repo_evidence_doc_url` · `repo_evidence_limits_url` | `evidence.md` | The brief, and its "What the research does NOT support" section. |
| `repo_formats_doc_url` | `page-patterns.md` | §Named session formats. |
| `repo_dictation_doc_url` | `prompt-craft.md` | §10, the dictated card. |

That is every key `build.py` provides. The keys the retired pages used (the
embedded README sections, the ledger table and chips, the evidence clusters,
the three numbers, the session formats, the card protocol, the pen-protocol
tables, the specimen gallery) were removed from `build.py` on 2026-09-29,
along with the block-level markdown converter that rendered them. They are in
git history. Do not bring them back: they embedded whole repo documents, and
the site links to those instead.

Only `docs/sheet-deep-react.png` is copied into `dist/` (as
`sheets/sheet-deep-react.png`), because How it works shows it.
`docs/specimen.pdf` and the other renders are not published: an unlinked
printable sheet at a site URL is the generic sheet by another name (see
"Retired pages redirect"). They stopped shipping on 2026-09-29, so an old link
to `/specimen.pdf` now returns 404.

### 4. Adding repo content

Add an extractor to `build_repo_context()` in `build.py`, or a
`repo_doc_url()` call for a link. Helpers: `read_repo`, `extract_section`,
`find_first_table`, `parse_table`, `fenced_blocks`, `strip_front_matter`,
`inline_md`, `plain_text`, `esc`. There is no block-level markdown converter
on purpose: a page that needs a whole section links to it. Use `required=True` only for content a page
cannot do without; everything else gets `required=False` plus an `{% if %}`.

### 5. Partials

None. `_print-note.html` was removed with the pages that handed over a
printable sheet; no page on the site prints anything now.

### 6. Planned pages and stubs

`PLANNED_PAGES` in `build.py` lists `how-it-works`, `install` and `research`.
A planned slug with no template gets a marked stub so no link dangles; write
the template and the stub disappears. `collect_pages()` fails the build if two
templates claim one slug.

---

## The primary call to action

One call to action runs the site: **Copy instructions for your AI**. It copies
`site/static/copy-instructions.txt`, which the visitor pastes into the AI chat
they already use before saying what they are working on. Agents that can run
the skill fetch it and hand over a layout-checked PDF; plain chats build a printable
document in a canvas or artifact, or dictate a card. The photos come back to
the same chat.

The markup, used on Home, How it works, Install `#no-printer` and Research:

```html
<div class="copy-cta">
  <a class="btn btn--primary copy-cta__btn" href="{{ copy_instructions_url }}" data-copy-ai>Copy instructions for your AI</a>
  <p class="copy-cta__status" data-copy-ai-status role="status" aria-live="polite"
     data-done="Copied. Paste it into your AI chat and say what you are working on."></p>
</div>
```

With JS off it is a link to the text file. With JS on, `site.js` copies
instead of navigating and writes the `data-done` sentence into the status
line. Inner pages also carry a quiet masthead copy button (`_base.html`); Home
does not, because its own button is on screen. Keep one filled
`.btn--primary` per page; everything else is an outlined `.btn` or a link.

---

## The design system

Read `paper-session/references/design.md` before you style anything. **The
sheet is the brand**; the site does not get a second identity. Everything in
`static/style.css` traces back to that file, including the rule weights:

```
print 2pt datum rule     ->  --rule-datum: 3px      (2pt = 2.67px at 96dpi)
print 1.6pt closing rule ->  --rule-close: 2px
print 0.5pt hairline     ->  --rule-hair:  1px
print gray value 0.NN    ->  --g-NN
```

### Tokens

```
--g-00 #191c1e   --g-12 #24282a   --g-20 #33383a   --g-30 #4a5052
--g-40 #5c6264   --g-45 #656b6d   --g-50 #7b8183   --g-55 #a0a5a3   --g-60 #c3c6c2
--paper #f1f0ec  --surface #f8f7f4  --surface-2 #eceae5
```

Semantic aliases: `--ink` (g-00), `--ink-2` (g-30, secondary prose),
`--ink-quiet` (g-45, labels; 4.75:1 on `--paper`, the small-text floor),
`--ink-faint` (g-50, 3.5:1; decoration, underlines and rules only),
`--guide` (g-60, hairlines only, never type). Pen channels: `--pen-red`
`--pen-green` `--pen-blue` `--pen-black`. Type: `--font-serif` / `--font-sans`
/ `--font-mono` (IBM Plex). Sizes `--fs-provocation`, `--fs-title`,
`--fs-lead`, `--fs-body`, `--fs-machine`, `--fs-small`, `--fs-label`. Space
`--s1` … `--s9`; layout `--page-max`, `--gutter`, `--measure` (65ch).

### The three voices, never blended

- **Serif asks.** Running prose, provocations, the site's questions
  (`.question`), intent lines (`.intent`), asides (`.aside`).
- **Mono is the machine.** On this site Mono means one thing: these words are
  quoted verbatim from the repository. Wrap them in `.machine`, with a
  `<span class="caption">` naming the source where a visitor needs it (the
  Install ledger and the scan-back file). A single quoted line that the
  sentence before already introduces, like "Printed. Go think." on How it
  works, goes without one: a file path is jargon on a pitch page.
- **Tracked Sans caps is infrastructure.** Nav, `.label`, buttons, footers,
  step numerals.
- Nothing on the site imitates handwriting.

### Structure and components

- `.datum` opens every page; `.open-territory` (a 2px rule, a label, 34vh of
  nothing) closes the inner pages.
- **Decompression downward.** Bands take ascending air, `.air-1` to `.air-4`.
- Layout: `.wrap`, `.measure`, `.band`, `.prose`.
- Home (section 22 and 23 of `style.css`): `.door-grid` / `.door-rail` /
  `.door-body` / `.door-sep` / `.door-margin`, `.door-rows` / `.door-row`
  (`.door-row--plain` has no numeral), `.home-lead`, `.home-steps` (the film
  and the copy step side by side from 64rem, stacked below).
- Shared: `.btn` / `.btn--primary`, `.copy-cta`, `.steps` (`--lines` on Home,
  `--walk` on How it works), `.hiw-figures` with `.sheet`, `.say` / `.says`,
  `.verdicts`, `.bundle-links`, `.status`, `.disclosure`, `.filebox`,
  `.source-entry` (the field-note entry on Research).
- No template contains a `<style>` or `<script>` element. New styles go in
  `static/style.css` section 23.
- `style.css` carries no rules for retired markup. The rules for the retired
  pages (onramps, route cards, the print note, pen swatches, the specimen
  plate, the old door rows and more) were removed on 2026-09-29, checked
  pixel for pixel on all four pages in both themes. They are in git history.
  The sheet's print CSS (section 21, `.ps-sheet*` and `.s-*`) stays on
  purpose.
- Flush left. No centred layouts, no rounded corners, no fills beyond
  `--surface` behind code, no shadows.

### Colour law

Grayscale carries the page. Colour appears only where it encodes pen intent,
and never as the sole carrier of meaning (WCAG 1.4.1). Focus outlines are the
one piece of colour on furniture.

### Themes

The complete light palette lives on bare `:root`; `@media
(prefers-color-scheme: dark)` guarded as `:root:not([data-theme="light"])`
redefines only the tokens; `:root[data-theme="dark"]` redefines them again so
the footer toggle wins both ways. Never declare a colour only inside a media
block.

### Accessibility floor

- Visible 2px `--focus` outline. `prefers-reduced-motion` honoured.
- One `<h1>` per page, headings in order, real landmarks, a skip link, alt
  text on every image. No page scrolls sideways at 320px.
- **Everything works with JavaScript off.** `static/site.js` only reveals and
  wires controls: the copy call to action (a link to the text file without
  JS), the masthead copy button (hidden without JS), the scan-back copy button
  (hidden without JS, and the file sits open on the page), the theme toggle,
  and the film's centred play button (without JS the video's native controls
  play it).

---

## Content rules the project enforces on itself

These are the project's invariants applied to its marketing. A page that
breaks one is wrong even if it converts.

1. **Never say a session is quick, easy, or fast.** No time estimates as a
   selling point. A paper session will feel less productive than the same
   hour on screen, including on the days it is most productive.
2. **No AI-generated imagery.** Photographs of real artifacts, the specimen
   renders, the film, or nothing.
3. **No testimonials, no percentages, no completion statistics, no "trusted
   by".** Part Three of `evidence.md` is empty. When field notes arrive they
   go on Research word for word, with date and context, never smoothed.
4. **No waitlist, no newsletter capture, no star-the-repo CTA above the fold.**
5. **Honest status stays honest.** "Installs cleanly, loop untested" is the
   most credible sentence the project has. Let the ledger speak in its own
   words.
6. **The single primary call to action is "Copy instructions for your AI".**
   The visitor pastes it into the chat they already use and says what they
   are working on, so the first page they print is built from their own work.
   Install is the second path, for people who want the full loop. The generic
   printable sheet was removed on 2026-09-29 because it was a bad version of a
   session.
7. **Voice.** Plain, short sentences, bottom line first, no hype. The AI
   prints and reads back; the person thinks and decides. No em or en dashes in
   anything a visitor reads (copy, titles, alt text, labels, JS strings);
   verbatim repo text is exempt.
8. **Describe a sheet as the repo defines it.** It may carry AI work worth
   reacting to (a proposed order, gathered options). It never pre-fills the
   judgment or creative zones, never carries a timer or suggested duration,
   never a scoring rubric.

---

## Assets

| File | Where it shows |
|---|---|
| `site/static/film.mp4` (+ `film-poster.jpg`, `film-captions.vtt`) | Home, step 1. Narrated, so it plays with sound, from a poster frame and a centred play button. Without the MP4, Home shows `hero.jpg`, and without that a dashed red placeholder. |
| `site/static/hero.jpg` | Film fallback and `og:image`. |
| `site/static/return-example.jpg` | How it works, "As photographed", beside `docs/sheet-deep-react.png` ("As printed"). |
| `site/static/copy-instructions.txt` | The text the primary call to action copies. Required: the build fails without it. |

Drop a replacement in and rebuild; nothing else changes. Update the matching
`alt` text in the template when a photograph changes.

---

## Deploying

`.github/workflows/pages.yml` builds with `--strict` on every push to main
that touches the site or its repo sources, builds a second time and diffs the
two, then publishes `site/dist/` to GitHub Pages. `dist/.nojekyll` is written
by the build. Every internal link is relative, so the site works at a custom
domain, under `welovejeff.github.io/paper-session/`, or from the filesystem.

---

## Troubleshooting

| Message | What to do |
|---|---|
| `could not find the §Install section in README.md` | The heading was renamed or the README is mid-edit. Update the extractor; never restate the section in a template. |
| `... has no heading starting ...` | A `repo_doc_url()` target heading was renamed. Update the heading named in `build.py`. |
| `specimen assets are missing from the repo` | Run `python3 docs/specimen.py`, or build with `--allow-missing-assets`. |
| `<template> uses unknown template keys: …` | Typo, or you need a new extractor in `build_repo_context()`. |
| `internal links point at nothing` | The target page is not planned, or the link is missing its `{{ base }}` prefix. |
| a redirect error | A retired slug has a template again, or `install.html` lost `id="scan-back"` / `id="no-printer"`. |
