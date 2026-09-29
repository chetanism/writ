# The component inventory

The list `/design-system` cuts the first inventory from, and the states each component owes. **The
first cut is what the queued slices will render**, not this whole list; a component nobody has a
screen for is a component designed against an imagined need.

## The states every interactive component owes

A state the spec does not list is a state nobody designs, and it ships as whatever the browser
does. For each interactive component, the spec's §5 says how each of these looks, or says *not
applicable* and why.

| State | What it must do |
|---|---|
| **Default** | |
| **Hover** | Only as a hint — a touch screen never sees it, so nothing may depend on it |
| **Focus-visible** | A visible ring at non-text 3:1 against every surface it can sit on, at least 2px. `outline: none` with nothing in its place is the most common accessibility defect on the web |
| **Active / pressed** | |
| **Selected / checked** | Not by colour alone — a mark, a weight, a fill change a colour-blind reader can see |
| **Disabled** | Not focusable, or focusable with `aria-disabled` and a reason nearby. Exempt from contrast, which is why a disabled control with no explanation is a dead end |
| **Invalid** | The message in text beside the field, tied with `aria-describedby`; not red alone |
| **Loading / pending** | The control keeps its size, so the layout does not jump; announced to assistive technology |
| **Empty** | For anything that shows a collection: what is shown when there is nothing, and what to do next |
| **Read-only** | Distinct from disabled: it can be focused and copied |

## The inventory

| Component | Variants worth deciding | Keyboard and semantics |
|---|---|---|
| **Button** | primary, secondary, ghost, danger; sm, md, lg; icon-only | A `button` element. Icon-only needs an accessible name. Enter and Space activate |
| **Link** | inline, standalone | An `a` with an `href`. Visibly a link without hover — underline, or 3:1 against surrounding text plus a non-colour cue |
| **Text input, textarea** | sizes; with prefix, suffix, clear | A visible `label`, never a placeholder standing in for one |
| **Select, combobox** | single, multiple, searchable | The native `select` where it suffices; otherwise the ARIA combobox pattern in full, arrow keys and type-ahead included |
| **Checkbox, radio, switch** | | A switch applies at once; a checkbox waits for a submit. Space toggles; arrows move within a radio group |
| **Form field** | | The wrapper: label, hint, error, required marker — one layout for every input |
| **Card, panel** | flat, raised, interactive | An interactive card has one primary target, not a nest of them |
| **Dialog** | modal, confirm, drawer | Focus moves in on open, is trapped while open, returns to the trigger on close; Escape closes |
| **Popover, menu, tooltip** | | A tooltip holds no interactive content and is not the only place information lives. Menus: arrow keys, Escape, focus return |
| **Tabs** | | Arrow keys between tabs, Tab into the panel |
| **Table, data grid** | dense, comfortable; sortable, selectable | A real `table` with `th` and `scope`. Sort state announced with `aria-sort` |
| **Toast, banner, inline alert** | info, success, warning, danger | Toasts announced through a live region, dismissible, and never the only record of something that failed |
| **Badge, tag** | status colours, removable | |
| **Avatar** | image, initials, fallback | |
| **Skeleton, spinner, progress** | | Progress with a value exposes it; a spinner has an accessible name |
| **Navigation** | top bar, side bar, breadcrumbs, pagination | A `nav` landmark each, with a label when there are several. Current page marked with `aria-current` |
| **Empty state** | first use, no results, error | Says what happened and offers the next action |
| **Page layout** | the shell, the content width, the grid | Landmarks: `header`, `nav`, `main`, `footer`. One `h1` |

## What the spec records for each component in the cut

- The variants kept, and the ones deliberately not built.
- Every state from the table above, with the tokens it reads.
- The keyboard behaviour and the accessible name, one line each.
- **The contrast pairs it creates**, added to `$contrast` in the tokens — this is how the check comes
  to cover a component, rather than only the palette.
- Where it lives in the code once it exists.
