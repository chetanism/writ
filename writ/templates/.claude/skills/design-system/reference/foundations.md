# Building each scale

The defaults `/design-system` offers first in every question, and the reasoning behind each. A
default is a starting point the reader can see, not a rule; where the project's BRD or brand says
otherwise, it wins and the spec says why.

## Colour

**Build ramps in OKLCH, not in hex.** OKLCH lightness is perceptual, so step 600 of the blue and
step 600 of the red are equally dark, and a semantic token that works on one hue works on the
others. Ramps picked by eye in hex drift: the yellow 600 is far lighter than the blue 600, and
every contrast pair has to be solved again per hue.

| Ramp | Steps | Built by |
|---|---|---|
| **Neutral** | 0, 50, 100, 200 … 900, 950 | Lightness from about 99% to 14%; chroma near 0, tinted toward the brand hue at 0.005–0.015 if neutrals are *cool* or *warm*. The workhorse — most of any interface is neutral |
| **Brand / accent** | 50 … 950 | The brand colour placed at the step whose lightness it has; the rest keep its hue and taper chroma toward both ends, where high chroma leaves the sRGB gamut |
| **Status** | success, warning, danger, info — 50 … 950 each | The same lightness curve as the brand ramp, so `danger.600` and `accent.600` behave alike on a surface |

**Semantic roles** the first cut almost always needs:

| Group | Roles |
|---|---|
| `color.bg` | `canvas` (the page), `surface` (cards, panels), `raised` (menus, popovers), `sunken` (wells, inputs), `inverse` |
| `color.text` | `default`, `muted`, `subtle` (placeholder, disabled — exempt from contrast when disabled, say so), `inverse`, `link`, `on-accent` |
| `color.border` | `default`, `strong` (input edges — non-text 3:1), `focus` (the ring — non-text 3:1 against every surface it can sit on) |
| `color.action` | `primary.bg`, `primary.bg-hover`, `primary.fg`; the same for `secondary` and `danger` |
| `color.status` | `success`, `warning`, `danger`, `info` — each with `fg`, `bg`, `border` |

**Dark is not the light theme inverted.** Surfaces get *lighter* as they rise (canvas 950, surface
900, raised 850) because shadows barely read on dark; saturated accents are pulled one or two steps
lighter and less chromatic, or they vibrate; body text is not pure white — 90–95% lightness is
easier over long reading.

## Typography

| Default | Why |
|---|---|
| **The system stack** (`system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`) unless there is a brand face | Zero download, native rendering, and correct on every platform. A brand face earns its weight when brand is a stated goal |
| **A monospace stack** for code, identifiers and tabular figures | `ui-monospace, "SF Mono", Menlo, Consolas, monospace` |
| **Body at 16px** (14px for dense tools read all day on a desktop) | Below 16px on mobile, iOS zooms into focused inputs |
| **A ratio of 1.2** (minor third) for dense products, **1.25** for most, **1.333** for editorial | Steps: `xs sm md lg xl 2xl 3xl` — seven is enough. More steps than that and nobody can tell two of them apart |
| **Line height** 1.5 for body, 1.2–1.3 for headings, tighter as size grows | Unitless, so it scales with the font size it sits on |
| **Weights** 400, 500, 600, 700 at most | Each weight of a web font is a file |
| **`font-variant-numeric: tabular-nums`** wherever numbers line up in columns | |

Sizes are `rem` in the tokens, so a reader's browser font setting still scales the interface.

## Space

**A 4px base; steps at 0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24** (×4px). The scale is dense at
the small end, where the eye tells 4px from 8px, and sparse at the large end, where it cannot tell
44px from 48px. Semantic names on top for the jobs that recur: `space.inset.sm|md|lg` (padding),
`space.stack.sm|md|lg` (vertical rhythm), `space.gap.*` (between siblings).

**Control heights** are their own tokens — 32px compact, 40px default, 48px for touch-first. The
minimum target size is 24×24 CSS px (WCAG 2.2, 2.5.8); 44×44 is the comfortable touch target.

## Radius, border, elevation

| | Default | Note |
|---|---|---|
| Radius | `none 0`, `sm 4px`, `md 8px`, `lg 12px`, `full 9999px` | *Sharp* halves these, *round* doubles them. Nested corners: inner radius = outer − padding |
| Border width | `1px`, `2px` for focus and emphasis | |
| Elevation | `shadow.sm`, `md`, `lg`, `xl` — each a pair of shadows, a tight one and a soft one | The colour of a shadow is a token too, and dark themes lean on surface lightness instead |
| Z-index | `base 0`, `raised 10`, `dropdown 1000`, `sticky 1100`, `overlay 1300`, `modal 1400`, `toast 1500`, `tooltip 1600` | Named layers, so nobody writes `z-index: 99999` |

## Motion

| Token | Default | Use |
|---|---|---|
| `motion.duration.fast` | 100ms | Hover, press, colour changes |
| `motion.duration.base` | 200ms | Expanding, fading, small moves |
| `motion.duration.slow` | 300ms | Panels, dialogs entering |
| `motion.ease.standard` | `cubic-bezier(0.2, 0, 0, 1)` | Most things |
| `motion.ease.exit` | `cubic-bezier(0.3, 0, 1, 1)` | Leaving |

**Under `prefers-reduced-motion: reduce`, movement goes and opacity stays.** A fade is not a
vestibular trigger; a slide, a zoom or a parallax is.

## Breakpoints

`sm 640px`, `md 768px`, `lg 1024px`, `xl 1280px`, `2xl 1536px`, mobile-first (`min-width`).
Custom properties cannot be read inside a media query, so breakpoints are the one place a literal
is written in source — the check lets `@media` and `@container` lines through for exactly this
reason. Keep them in the tokens anyway, as the one list somebody reads.

## Contrast floors

| What | WCAG 2.2 AA | AAA |
|---|---|---|
| Body text | 4.5:1 | 7:1 |
| Large text — 24px, or 18.66px bold | 3:1 | 4.5:1 |
| Non-text: input borders, focus indicators, icons that carry meaning, chart marks | 3:1 | — |
| Disabled controls, pure decoration, logos | exempt | exempt |

The check computes WCAG 2 ratios. APCA, the candidate for WCAG 3, rates some pairs differently —
mid-tone text on dark backgrounds especially — and a project that wants it records that as an ADR
and checks those pairs by hand until the tool supports it.
