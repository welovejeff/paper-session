# Prompt: Paper Session Design System — Research, Brief, Four Directions

Copy everything below the line into a fresh Claude design session. Attach `paper-session.skill` and `scan-back.skill` (or paste both SKILL.md files) so the constraints travel with it.

---

You are the design lead for a print design system called Paper Session. It is the visual language for AI-generated, human-completed worksheets: a skill pauses on-screen AI work and prints an artifact (provocations, ranking activities, sequencing card kits, field logs) that a person completes with a pen, away from screens, then scans back to resume the workflow. The attached SKILL.md files are the product spec. Read them first; every design decision must serve them.

Your job runs in three phases. Stop for my review at the end of Phase 2 before starting Phase 3.

## Non-negotiable constraints (inherit these, do not relitigate)

- US Letter 8.5x11, printed grayscale on a consumer inkjet. Assume mediocre toner economy: no heavy ink fills, no full-bleed blacks, no large tint panels.
- The human's handwriting must be the highest-contrast element on the completed page. Printed matter sits back; pen sits forward.
- Minimum 50% of every page is empty space for the human. White space is the product, not the absence of one.
- One provocation per zone. Every sheet ends in unstructured open territory.
- Pages will be photographed with a phone in imperfect light. The system must survive scanning: no light gray type below scan legibility, no elements that confuse edge detection, generous margins (0.75in minimum).
- Two capacities exist, Deep and Light, and the system must make them feel visibly different at arm's length.
- The design must be buildable programmatically (reportlab or HTML-to-PDF). No effects that require manual design work per sheet.

## Phase 1: Research

Study three source pools and pull principles, not screenshots to copy.

**Pool A, the prior art of the loop.** Gradescope's template-and-region architecture (the blank template as a negative for extracting human ink). Rocketbook's destination-symbol system and where its generic pages fail. reMarkable's restraint philosophy (capture stays quiet, intelligence stays off the surface). BERG's Little Printer (charm and dailiness in a printed artifact). Dynamicland (paper as a first-class computational object). For each: what did their surface design get right or wrong for a human writing by hand?

**Pool B, the print lineages that already solved handwriting-on-forms.** Go where the craft actually lives: Swiss/international-style forms and Josef Müller-Brockmann grid discipline. Japanese stationery systems (Kokuyo Campus, Midori, MUJI) and their line-weight restraint. Field Notes and the utilitarian American memo book tradition. IDEO Method Cards and Oblique Strategies as precedent for one-provocation-per-card. Standardized test and ballot design (the science of unambiguous answer zones). Zine and DIY show-flyer culture (Dischord-era) as precedent for an opinionated, human, anti-corporate voice on cheap paper. Not all of these belong in the final system; map what each does that we can steal.

**Pool C, adjacent digital patterns.** Use /mobbin-search (or equivalent) for: journaling and guided-reflection apps, habit and priority trackers, and document-scanning flows. The question for this pool is narrow: how do the best digital products signal "this space is yours" versus "this is the system talking," and what is the print translation of that signal?

## Phase 2: The brief (stop here for review)

Synthesize the research into a design brief, max two pages, containing:
1. Five named design principles for the system, each stated as an opinion that could be disagreed with. "Clean and modern" is not an opinion. "The printed layer whispers so the pen can shout" is.
2. The tension map: the three hardest tradeoffs the system must resolve (e.g., personality vs. scan reliability, structure vs. open territory, warmth vs. authority) and your recommended position on each.
3. A typographic hypothesis: candidate typeface families (must be freely licensable and embeddable in programmatic PDF generation), a proposed scale, and a rule for how AI-contributed text is visually distinguished from prompts and from zones awaiting the human.
4. What each research pool contributed, in one paragraph each.

Present the brief and wait for my feedback before Phase 3.

## Phase 3: Four directions

Develop 4 genuinely divergent design directions. Divergent means a different answer to the tension map, not the same layout in four typefaces. For each direction deliver:

1. A name and a one-paragraph stance.
2. Two full specimen pages as rendered PDFs: one Deep sheet (use the "two-column react" plus "one provocation per page" patterns from the skill's pattern library) and one Light sheet ("rank-and-circle"). Same content across all four directions so the design is the only variable.
3. The atomic inventory for that direction: atoms (rules, answer guides, checkboxes, type styles, spacing units), molecules (provocation zone, rank row, AI-contribution block, open territory), organisms (the named sheet patterns), templates (Deep kit, Light sheet).
4. One honest paragraph on where the direction is weakest.

Do not average the four into a safe middle. I will pick a direction or a hybrid, and the winner becomes `design.md`: a single file with the atomic system fully specified (exact point sizes, line weights, spacing units, grayscale values, zone anatomy) written so a code-generation model can implement any sheet in the system from it without seeing the specimens.
