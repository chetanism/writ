# `/design-system`

**The web interface's design system — tokens for colour, type, space, radius, elevation and motion
in every theme, and the component inventory with every state — designed with you, or recovered
from what the code already uses, and held to by a check in the gate.**

| | |
|---|---|
| **Run it** | Once, as a slice of its own before the first screen: `/design-system`. Again to amend one thing. `/design-system audit` at a phase gate that built screens |
| **Produces** | The tokens file and what is generated from it — CSS, and a Tailwind v4 theme and a TypeScript module where the stack wants them; `writ/spec/UI-SPEC.md` with a `UI-NN` index; an ADR where a choice binds later slices; a specimen page. `audit`: a dated report under `writ/maintenance/audits/` |
| **Refuses to** | Design on `dev` — the tokens are code, so it runs on a claimed slice branch. Put a value in the spec. Lower a contrast floor to make a colour pass. Install a taste skill for you. Report a visual review it could not run. Edit anything in `audit` mode |
| **Installed** | Only when the stack has a web interface. Phase 9 derives it from phase 5 and asks nothing |

## Why it exists

**A design system written down and not checked is a style guide, and a style guide is decoration
within a quarter.** Somebody needs a grey that is not quite any of the greys, writes `#6b6f76` into
a component, and nothing says a word. A year later there are forty greys, the dark theme works on
half the screens, and the focus ring is invisible on the one surface nobody tested.

So each part has one home, and a check holds them together:

| What | Where |
|---|---|
| **The values** | the tokens file, compiled to CSS custom properties — nothing else holds a value |
| **The rules** | `writ/spec/UI-SPEC.md` — principles, how each scale is built, the themes, each component's states and keyboard contract. It names tokens, never values, so it cannot drift from them |
| **The proof** | `python3 scripts/design_tokens.py check`, a step in the gate |

## Correct is not the same as good

The check makes a design system consistent and accessible. It cannot make it look like anything,
and a system built from sensible defaults alone looks like every other one. So **the direction is
settled first**, and the project chooses whose taste decides it.

- **A taste skill, if you want one.** It looks at the skills you already have and offers any about
  visual design. With none, you name one, ask it to help find one, or go without. *Help me find
  one* searches the marketplaces and the web and gives two or three candidates, each with what it
  pushes the design toward, the stack it assumes, where it will fight the tokens, and where it
  comes from. **You install it** — a third-party skill is instructions an agent follows in every
  UI slice, so it is yours to read first. The choice lands in `design.taste` and an ADR.
- **Two rules a taste skill never changes.** Tokens win: whatever it chooses is written into the
  tokens, never hard-coded. And the check never bends: a literal it wants becomes a token or an
  explained exemption, and a contrast failure is changed rather than excused.
- **A direction round** either way — three products it should feel like and one it should not, any
  screenshots, the patterns to ban. It becomes the spec's principles and bans.
- **It looks at the result.** The specimen page is screenshotted in each theme at phone and desktop
  width with whatever browser tool the session has, and read against the principles, the bans and
  the taste skill — for what no script sees. With no browser tool it says it skipped the step.

## What the check fails on

1. **A reference that resolves to nothing**, a loop of references, a colour that does not parse, a
   dimension with no unit, a theme that invents a token the base does not have.
2. **A generated output that is not what the tokens compile to** — the CSS, the Tailwind theme or
   the TypeScript module was edited instead of the source.
3. **A contrast pair below its floor, in any theme.** The tokens declare which foreground sits on
   which background, and the minimum: 4.5:1 for text by default, 3:1 for input borders, focus
   rings and meaningful icons. A dark theme that quietly puts grey text on a grey surface fails
   here rather than in an accessibility complaint.
4. **A raw colour or length in the source** — a hex, an `rgb()` or `oklch()`, a named colour where
   a colour is set, a `px`, `rem` or `em` — inside the `design_values` perimeter. In a stylesheet
   only declarations are read, so an id selector such as `#fab` is not a colour; nor is a link
   target like `href="#add"`. Media and container queries are let through,
   because custom properties cannot be read there. A line that genuinely needs a literal carries
   `design-exempt:` and its reason, so every exception is one `grep` away.

Off, and passing, until the skill's first run names a tokens file — so the step can ship in every
bootstrap without failing a project that has not designed anything yet.

## How it runs

1. **Reads before asking** — the BRD and personas (who, on what, for how long), the compliance
   register (an accessibility obligation is a floor, not a preference), the stack and any component
   library (themed, never replaced), and on an existing codebase `design_tokens.py extract`: every
   literal colour and length in the source, counted, with colours the eye cannot tell apart grouped.
2. **Reads back in ten lines**, with what it is guessing labelled.
3. **Settles whose taste** — the taste skill question above.
4. **Interviews in rounds** — direction, character and density, brand, accessibility and themes,
   the first components — with a recommended default first in every question. On an existing codebase the
   brand round becomes a table of the extracted groups, each confirmed, merged or dropped by you.
5. **Writes the tokens in three tiers** — primitive ramps nothing references directly, semantic roles
   that components and themes use, and component tokens only where no role fits — then builds and
   checks. With Tailwind v4 it also generates an `@theme` block that resets the default palette, so
   `bg-red-500` stops existing and `bg-bg-surface` is a token.
6. **Writes the spec, any ADR, and a specimen page** showing every token and every component state
   in each theme side by side, then looks at it. The specimen is the slice's demo.

## On an existing codebase

The raw-value rule uses the same perimeter as every other rule. `/writ:adopt` writes it empty, so
nothing fails on day one; it starts at the shared component directory once the tokens exist, and
widens one directory per slice, in the order `/design-system audit` ranks them by literals left.

## See also

[`/writ:adopt`](adopt.md) for the perimeter, and [`/process-change`](process-change.md) to turn the
check down — `DEVELOPMENT-PROCESS.md` §15 says what each switch costs.
