# `/product-guide`

**Writes the living usage guide for the product's own users, from the code: one directory per
persona, each task walked step by step through the real screens. What to click, type or run, never
what the product is.**

| | |
|---|---|
| **Run it** | When something a user sees or does has changed, and at a phase gate. `/maintenance` does not run it |
| **Produces** | `docs/documentation/guides/`, updated only where user-visible behaviour changed, on a branch through a pull request |
| **Refuses to** | Explain what the product is or how it is built — that is [`/product-docs`](product-docs.md), linked. Document a screen that is not built. Fork a page for a role that only lacks a button. Write outside `guides/` |
| **Installed** | Offered in phase 9, selected by default when the personas include somebody outside the team who uses the product |

## Two halves, and the line between them

**`/product-docs` is for the team building the product; this is for the people using it.** One
document addressed to both serves neither, and until this skill existed nothing in a writ project
was written for a customer, an operator or an integrator at all. Once a product has users, that gap
is the first thing a support team or a first customer runs into.

| | `/product-docs` | `/product-guide` |
|---|---|---|
| Reader | The team | The product's users |
| Says | What it is and how it is built | What to click, type or run, and what you see when it worked |
| Lives in | `docs/documentation/` | `docs/documentation/guides/` |

**The test for a sentence is whether it tells somebody what to do with the product open.** If it
does not, it belongs in the other half, and it gets a link rather than a second copy. Both live in
one site, so the build checks the links between them.

## One directory per persona

The personas come from `writ/spec/personas.md`: people who use the product, never the system actors
or the team. Personas who do the same jobs in the same application share a directory.

- **UI first.** Every persona is walked through the screens. The API appears only for a persona
  whose job is to integrate the product, and even there a step that has a screen is shown on it.
- **A role differs by a missing control, noted inline.** Roles map onto permission scopes, and a
  scope usually removes a button rather than changing the steps around it. So *"(owners only — for
  other roles the button is not shown)"* goes on the step, from the permission check in the code, and
  the page is not forked.
- **No interface at all** leaves one persona: the developer who integrates it.

## Every task page has the same shape

Before you start · the numbered steps, each label quoted exactly as the product shows it · what you
see when it worked · what each error message the product can give here means · what to do next.
Every quoted label is checked against the source before the pass is committed — a label the code
does not contain is a step nobody can follow.

## Why it is not in `/maintenance`

**The guide moves when what a user sees moves, and at no other time.** A cleanup, a refactor or a
dependency bump changes nothing on a screen, so a guide pass on the maintenance clock would mostly
find an empty scope. It is delivered through the same `delivery.md` as the passes, with its own
marker, `docs: update product guide`, so each run finds where the last one stopped.

## See also

[`/product-docs`](product-docs.md) · [`/maintenance`](maintenance.md) for `delivery.md` ·
[`/test-scenarios`](test-scenarios.md), which walks the same screens for a tester rather than a user
