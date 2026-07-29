# Paper Session Design System: Research Brief (Phase 2)

## Five principles (each is a position, argue with them)

**1. The printed layer whispers so the pen can shout.**
The completed page, not the blank page, is the finished design. Every printed element is set at a contrast level below what a ballpoint produces, so the human's ink is always the loudest thing on the sheet. If a blank specimen looks impressive, it is probably wrong.

**2. Emptiness is designed, not left over.**
White space is the primary material of this system. Every empty zone has an intentional shape, a deliberate entry point for the pen, and a reason for its size. "We ran out of content" emptiness and "this is your territory" emptiness look different, and only the second is allowed.

**3. Three voices, never blended.**
The sheet asks, the machine reports, the human answers. Each voice gets one unmistakable typographic identity, and they never borrow from each other. This is the design system enforcing the skill's core rule: whose thought does this slot belong to. A reader should identify the author of any mark on the page from three feet away.

**4. This is an instrument, not a form.**
No form-number aesthetics, no boxes for boxes' sake, no bureaucratic smell. Guides appear only where a pen genuinely needs them (ruled lines for sustained writing, a frame for a constrained answer) and vanish everywhere else. The reference point is a lab notebook or a method card, never a tax return.

**5. Charm is load-bearing.**
BERG's lesson: a printed object you feel affection for gets used daily; a sterile one gets abandoned. Sterility is a completion-rate bug. But charm lives in voice, numbering, and small typographic details, never in ink-heavy decoration, texture, or illustration. Warm words, cool layout.

## Tension map (three hardest tradeoffs, with positions)

**Personality vs. scan reliability.**
Position: personality is carried entirely by typography and language, never by tint panels, textures, or decoration. Hard floor: nothing semantically meaningful prints below 50% gray. Writing guides may go lighter because they carry no meaning once written over. This keeps every sheet inkjet-cheap and phone-scan-proof while still having a voice.

**Structure vs. open territory.**
Position: the page decompresses downward. Structure concentrates at the top (header, the AI's contribution, the tightest activity), and freedom grows toward the bottom, ending in fully open territory. One consistent gravity across every sheet in the system, so the hand learns the pattern: start guided, end wandering.

**Warmth vs. authority.**
Position: authority in the grid, warmth in the words. Layout is strict (real grid, consistent margins, disciplined scale); language is direct, human, occasionally funny. Never the reverse: a loose layout with corporate language is the worst quadrant and describes most productivity printables.

## Typographic hypothesis

One superfamily, three voices. **IBM Plex** (open license, embeds cleanly in reportlab and HTML-to-PDF):

- **Plex Serif** for provocations and prompts: the sheet's asking voice. Serif reads as considered and human-directed, matching what the best guided journaling apps do with their prompt type.
- **Plex Sans**, small caps or caps-with-tracking, for structural labels, wayfinding, headers, and footer instructions: quiet infrastructure.
- **Plex Mono** for all AI-contributed content (proposed priorities, gathered options, draft sequences): visibly machine output, honest about its origin, and impossible to confuse with either the sheet's voice or the human's pen.

Fallback family if Plex fails a legibility test at small sizes on inkjet: Source Serif 4 + Source Sans 3 + Courier Prime, same three-voice rule.

Proposed scale (print points): 9/11 labels, 11/16 mono AI content, 13/19 serif prompts, 18 to 22 for single-provocation pages, sheet title 16. Rules at 0.5pt, writing guides at 0.75pt in light gray, answer frames at 1pt black. Deep sheets use the full scale; Light sheets drop the serif size one step and enlarge tap targets (rank boxes, circles) for couch-distance legibility.

## What each research pool contributed

**Pool A (the loop's prior art).** Gradescope proved the architecture but its surfaces are bureaucratic; it optimizes for the grader, not the writer, and completion suffers. Rocketbook showed that generic pages plus a symbol system is not a design language; its failure is undifferentiated space. reMarkable's restraint (intelligence off the surface, capture kept quiet) is the closest philosophical sibling and directly feeds Principle 1. BERG's Little Printer contributes Principle 5 wholesale: dailiness plus charm equals retention. Dynamicland validates paper as a first-class object worth designing seriously rather than as a degraded screen.

**Pool B (print lineages).** Swiss form discipline supplies the grid, the scale restraint, and the authority half of the warmth position. Japanese stationery (Kokuyo, Midori) supplies line-weight humility: guides that serve the pen and disappear behind it. Field Notes supplies the utilitarian-object affection that makes something get carried around. IDEO Method Cards and Oblique Strategies are the precedent for one-provocation-per-surface and for trusting a single question to hold a whole page. Ballot and standardized-test design supply the science of unambiguous answer zones (clear entry points, no ambiguity about where a mark goes), which scan-back depends on. The zine tradition is held in reserve as a voice option, not a layout option: its lesson is that cheap paper plus conviction beats expensive paper plus neutrality.

**Pool C (digital patterns).** The best guided journaling apps separate system voice from user space purely through type treatment and emptiness, which confirms the three-voices approach. Their placeholder-text pattern is a warning, not a model: on paper, example text is permanent ink and permanent anchoring, so the system must signal "this is yours" with guides and shaped emptiness only. Ranking UIs contribute the numbered rail and the per-item single-gesture principle for Light sheets.

## Provisional Phase 3 directions (for steering, not yet designed)

1. **Bureau**: full Swiss discipline, maximum authority, charm only in language. Risk: form-smell.
2. **Field Kit**: Field Notes utilitarianism, workmanlike, built to be carried and folded. Risk: too casual for Deep conceptual work.
3. **Method Card**: card-logic throughout, every zone treated as a card, cut-lines as a signature element. Risk: fragmentation on non-card sheets.
4. **Basement Show**: the zine-conviction voice on a disciplined grid, loudest personality, DIY ethos made visible. Risk: personality overwhelming the pen, violating Principle 1.

Awaiting direction before Phase 3.
