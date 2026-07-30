# Paper Session Design System (design.md)

The visual language for every sheet the paper-session skill prints. Bureau chassis, Basement voice at 60%, Field Kit dot grid as an optional zone type, Method Card cut-lines only where cutting is real. Implement any sheet from this file alone; no specimen reference required.

## 0. Non-negotiables

- US Letter portrait (612 x 792 pt). Margins 54pt all sides. Footer sits below the margin at baseline y=30; nothing else crosses the margin box except Deep/Light page notes sharing the footer baseline.
- Grayscale only. Nothing that carries meaning prints lighter than 50% gray (fill or stroke gray value 0.5). Writing guides may print at up to 60% gray (0.6) because they carry no meaning once written over.
- No fills, no tint panels, no textures, no images. Ink is spent on rules and type only.
- The human's pen must be the highest-contrast element on the completed page. If a blank sheet looks finished, reduce it.
- Every sheet decompresses downward: tightest structure at top, open territory always last.
- At least 50% of every page area is space for the pen.

## 1. Fonts and the three voices

IBM Plex, bundled in assets/fonts/. Register exactly:

| Register name | File | Role |
|---|---|---|
| Sans | IBMPlexSans-Regular.ttf | metadata, small labels |
| SansSB | IBMPlexSans-SemiBold.ttf | tracked caps infrastructure |
| SansB | IBMPlexSans-Bold.ttf | sheet titles, voice captions |
| Serif | IBMPlexSerif-Regular.ttf | provocations, prompts |
| SerifSB | IBMPlexSerif-SemiBold.ttf | emphasis within prompts |
| SerifI | IBMPlexSerif-Italic.ttf | intent lines, asides, house rules |
| Mono | IBMPlexMono-Regular.ttf | AI content, secondary |
| MonoM | IBMPlexMono-Medium.ttf | AI content, primary |

The three voices, never blended:
- **The sheet asks: Serif.** All provocations, prompts, and questions. Never used for AI-generated content.
- **The machine reports: Mono.** Every piece of AI-contributed content (proposed priorities, options, sequences, gathered data) is set in Mono, no exceptions. Mono never appears for anything the sheet is asking.
- **The human answers: pen.** No printed element imitates handwriting, ever.
- Infrastructure (labels, captions, wayfinding) is Sans caps with tracking. It is furniture, not a voice.

## 2. Type scale (print points)

| Element | Font | Size/leading | Gray | Tracking |
|---|---|---|---|---|
| Sheet title | SansB | 16 | 0 | 0 |
| Voice captions (THE MACHINE SAYS / YOU SAY) | SansB | 8 | 0.2 | +1.2 |
| Section labels, open-territory label | SansSB | 6.8 | 0.4 | +1.4 |
| Metadata (date line) | Sans | 6.8 caps | 0.4 | +0.8 |
| Intent line | SerifI | 9.5 | 0.3 | 0 |
| Provocation, standard | Serif | 21/28 | 0 | 0 |
| Provocation, Light sheets | Serif | 15/20 | 0 | 0 |
| Provocation subline | SerifI | 10 | 0.4 | 0 |
| AI item, primary | MonoM | 9.2 | 0.12 | 0 |
| AI item, secondary/promise | Mono | 7.6/9 | 0.42 | 0 |
| House rule / aside | SerifI | 8.5 | 0.35 | 0 |
| Footer | SansSB caps | 6.8 | 0.45 | +1.2 |
| Slot numbers | Sans | 8 | 0.5 | 0 |

## 3. Rules and guides

| Element | Weight | Gray |
|---|---|---|
| Datum rule (top of every page, full text width) | 2pt | 0 |
| Voice caption underline | 1.6pt | 0 |
| Open territory rule | 1.6pt | 0 |
| Structural hairline | 0.5pt | 0.55 |
| Writing guide (ruled line) | 0.5pt | 0.55, leading 16pt |
| Answer frame (rank box) | 1pt | 0.15 |
| Keep/kill circle | 0.9pt | 0.2, radius 8pt |
| Dot grid (optional zone type) | dots r0.5-0.6 | 0.6, pitch 12-16pt |
| Cut line (card kits only) | 0.6pt dash 3/2.5 | 0.3 |

Dot grid is used when the activity invites sketching or spatial marks (drawing activities, field logs, arrangement zones). Ruled lines are the default for prose answers. Cut lines appear only on sheets the human will actually cut (card kits); never as decoration.

**Every Deep kit must contain at least one dot-grid sketch zone.** Drawn content outperforms handwritten content on recall across multiple studies, including ones that found no advantage for handwriting over typing. A kit that is entirely ruled lines is leaving the strongest available effect on the table.

**No sheet prints a time limit, countdown, or suggested duration.** Not in the header, not in a zone label, not in the footer. Time pressure is the specific trigger for shallow processing, and the creativity benefit of input constraints holds only when the clock is not also constrained. Constraints belong in the prompt, never on the timer.

## 4. Header anatomy (every page)

Top edge at y = 792 - 54 = 738.
1. Datum rule, 2pt black, x 54 to 558, at y 738.
2. Sheet title, SansB 16, flush left at x 54, baseline 738 - 22.
3. Date line, Sans 6.8 caps tracked, x 54, baseline 738 - 36.
4. Intent line, SerifI 9.5, x 54, baseline 738 - 52. One sentence, written in the sheet's voice.
Body begins at y 738 - 74.

## 5. Voice and microcopy (the Basement layer, dialed to 60%)

- AI-contribution zones are always captioned **THE MACHINE SAYS**. Human zones opposite are captioned **YOU SAY**. These captions are SansB 8, tracked, with the 1.6pt underline.
- Open territory is labeled **SCRIBBLE ZONE** on Light sheets and **OPEN TERRITORY** on Deep sheets, above a 1.6pt rule spanning the text width. No box.
- One house rule per Light sheet is permitted, SerifI 8.5, placed directly above the open territory (e.g. "Rule: something dies tonight. Pick it."). House rules are direct, short, and slightly funny. Zero house rules on sheets carrying emotionally heavy content.
- Footer, every page: left side SansSB 6.8 caps tracked at y 30, text "SCAN IT BACK TO CONTINUE."; right side page note (e.g. "Deep · 1 of 2") Sans 6.8 gray 0.45.
- Language is direct and human throughout. No corporate filler, no exclamation marks, no encouragement-speak. Warmth comes from directness, not enthusiasm.

## 6. Molecules

- **React pair:** two equal columns, 24pt gutter. Left: AI items in Mono (MonoM item line, Mono promise line indented 14pt). Right: numbered empty slots, each = Sans 8 gray 0.5 number + two writing guides indented 18pt. A rotated SerifI 7.5 gray 0.45 hint reading "cross out freely" may sit centered in the gutter.
- **Rank row (Light):** 1pt rank box 22x20pt at left margin; item in Mono 9.6 at x+34; K and X circles (0.9pt, r8, letter centered Sans 6.4) near right; a 0.5pt note guide ~60pt wide ending at the right margin. Column captions RANK / THE MACHINE SAYS / KEEP · KILL / NOTE in SansSB 6.5 tracked gray 0.4 above the first row.
- **Provocation block:** Serif 21/28 flush left, max width text-width minus 60pt, subline SerifI 10 beneath. Everything below is empty until open territory.
- **Constraint box:** 1pt frame sized to physically fit the word budget (about 34pt per line of 12 words at Serif 13). Label above in section-label style.
- **Open territory:** 1.6pt rule full text width, label above the rule, minimum height 96pt (Light) / 108pt (Deep), always the last element before the footer.
- **Card kit sheet (only for cut-apart activities):** 2x4 grid of cards with 0.6pt dashed borders r4, each card = MonoM title line + Serif one-line promise + empty lower half; corner ticks optional; this is the only context where dashes appear.

## 7. Templates

**Deep sheet:** header → (optional) AI contribution organism → primary activity → open territory (≥108pt) → footer. Max 4 pages per session. Provocation pages carry exactly one question.

**Light sheet:** header → single low-effort organism (rank rows, gut-check ladder, reaction margins) → optional house rule → SCRIBBLE ZONE (≥96pt) → footer. Always exactly 1 page. Every mark the sheet requests must be achievable in one pen gesture.

## 8. Mandatory verification

After generating any PDF, run `scripts/verify_layout.py <pdf>` (bundled with the skill). It fails on: (a) glyphs that collide on a shared baseline, (b) any two words whose boxes overlap beyond tolerance across baselines, (c) any text outside the page bounds. On failure, fix the layout (shorten text, rewrap, resize, or re-space) and regenerate until the verifier passes. Never present a sheet that has not passed.

## 9. The pen protocol (color and marks as semantic channels)

The printed layer is grayscale by law (section 0), which reserves the entire color channel for the human. Ink hue and a small set of pen marks carry machine-readable intent on the return trip.

**The protocol is user-definable.** These are defaults, not rules. The authority cascade, highest first:
1. A legend handwritten anywhere on the page (e.g. "green = new concept") redefines that channel for the whole session.
2. The printed ink key on the sheet (which reflects any customization the user has told the skill about).
3. The defaults below.

Default ink channels (traffic-light logic):

| Ink | Meaning | Mnemonic |
|---|---|---|
| Black | General text, notes, context | the default voice |
| Red | Needs review, stop, delete, push back on this | red flags it |
| Green | Approved, yes, move forward | green is go |
| Blue | Instruction to the AI: do this on return | blue is do |

Default marks (work in any ink; ink modifies mark where it makes sense, e.g. a red strike is an emphatic kill):

| Mark | Meaning |
|---|---|
| Strikethrough | Kill it; a considered rejection |
| Circle | Elevate it; this matters |
| ? | Explain, expand, or answer this on return |
| ! | Priority |
| Star | Keep beyond this task; worth capturing to the user's own systems |
| Arrow between items | Sequence or causation; this leads to that |
| @name | Route it to a person, tool, or system |
| TLDR: | Treat this line as the headline answer of the zone |

Printing rules:
- Print the active key once per sheet, right-aligned above the footer baseline, Sans 6 caps at 45% gray, e.g. "INK KEY  RED REVIEW · GREEN GO · BLUE DO · BLACK NOTES". Print the user's customized legend if one exists, never a stale default. Marks are not printed; they live in muscle memory and in scan-back.
- The protocol is optional per session. A sheet completed entirely in black with no marks is fully valid; the channels add intent, their absence subtracts nothing.
- If the user states a custom legend in conversation, adopt it for all future sheets and offer once to remember it.
