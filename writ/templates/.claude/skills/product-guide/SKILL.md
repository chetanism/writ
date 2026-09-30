---
name: product-guide
description: Regenerate the living usage guide under docs/documentation/guides/ from the code — one directory per persona, walking the product's own users through its real screens step by step, UI first — updating only what user-visible behaviour changed since the last pass, delivered on its own branch through a pull request. Use when something a user sees or does has changed, or at a phase gate; /maintenance does not run it.
---

# Update the product guide

You are updating the **living usage guide**: what the product's own users do with it, one task at a
time, with the product open in front of them. Like the product documentation, it describes the
product **as it is today** — never a history, never a plan.

Invoked as `/product-guide`. **This file owns what changes.** `.claude/skills/maintenance/delivery.md`
owns the branch, the commits, the pull request and the merge — read it first, and run this file
inside its loop. `/maintenance` does not run this pass: the guide moves when user-visible behaviour
does, not on a maintenance clock.

> **Filled at bootstrap.** The persona table in *Who reads it* comes from `writ/spec/personas.md`,
> and `<DOC BUILD COMMAND>` and `<DOC BUILD OUTPUT>` are the same answer as in
> `product-docs/SKILL.md`. Where the project has no site generator, *Verification* says so instead.
> Delete this blockquote once it is filled.

## The split with `/product-docs`

**Two halves, and the line between them is absolute.**

| | The documentation — `/product-docs` | The guide — this pass |
|---|---|---|
| Reader | The team building the product | The product's users |
| Says | What the product is and how it is built | What to click, type or run, and what you see when it worked |
| Lives in | `docs/documentation/`, except `guides/` | `docs/documentation/guides/` |

**The test for a sentence: does it tell somebody what to do with the product open?** If it does, it
belongs here. If it does not — what an entity is, why a workflow exists, how the data flows — it
belongs in the documentation, and this page **links to it** rather than saying it again. Two copies
of one explanation are two explanations, and they drift apart.

Write only under `docs/documentation/guides/`. A page outside it that needs a link to the guide is
`/product-docs`'s to add; name it in the report.

## Who reads it

**One directory per persona who uses the product**, from `writ/spec/personas.md`:

| Directory | Reader | Their application | Roles |
|---|---|---|---|
| <PERSONA DIRECTORY> | <PER-NN — who they are, in their own words> | <THE SCREENS, APP OR INTERFACE THEY WORK IN> | <THE ROLES INSIDE THIS PERSONA> |

- **Only people who use the product.** A system actor in the register gets no directory, and nor
  does the team building it. They have the documentation.
- **Personas who do the same jobs in the same application share a directory.** Roles inside one
  persona get no directory of their own. See *Roles* below.
- **UI first.** Every persona is walked through the screens. The API appears only for a persona
  whose job is wiring the product into their own system — keys, requests, webhooks — and even there
  a step that has a screen is shown on the screen.
- **No interface at all** — a service, a library — leaves one persona: the developer who integrates
  it. The guide is then their tasks, done through the API.

## Roles differ by a missing control

**Most of the difference between roles is that a control is not there**, not that the procedure is
different. Roles map onto permission scopes, and a scope removes a button far more often than it
changes the steps around it.

So a role difference is **noted inline, on the step it affects**:

> 3. Choose **Refund**. *(Owners and finance only — for other roles the button is not shown.)*

Fork a page for a role only when the steps themselves differ, not when one of them is missing.
Derive each note from the permission check in the code, never from what the role's name suggests.

## Source material and ground truth

1. **The code is the source of truth.** The screens, routes, forms, their validation messages and
   the permission checks say what a user can do, in what order, and what they see. Quote every
   label, button and message **exactly as the product shows it**, in bold.
2. **The jobs come from `writ/`.** A requirement's detail file names the job in the user's own
   words — *when* this happens, *this persona needs to* … — and its test scenarios walk the same
   screens. Use them for what a task is called and why somebody does it. Never copy their steps: the
   code is what the steps are.
3. **Only what is built.** A requirement that is declared and not yet built gets no page. A
   half-built one is documented as far as it goes, and says where it stops.
4. **Conflicts:** if a document contradicts the code, write what the code does and flag it in the
   page:
   > ⚠️ **Conflict:** `the document` says X, but the product does Y. Needs resolution in code or docs.

   List every conflict in the report you hand back.

## Incremental update process

1. Find the most recent guide update commit:
   ```bash
   git log --grep="docs: update product guide" -n 1 --format=%H
   ```
   **Not anchored with `^…$`** — a squash merge appends ` (#N)` to the subject. Confirm the
   candidate actually carried a guide update before accepting it as a baseline.
2. **If a commit is found:** read `git diff <commit>..HEAD --stat` for what a user can see — screens
   and their components, routes, forms and validation, permission checks, messages, the public API
   and its contracts. A change that reaches no user moves no page, so **an empty scope is a normal
   outcome**. Update only the pages it affects, and fix anything you notice is wrong on the way.
3. **If no commit is found (first run):** write the guide from scratch, starting with the one task
   each persona does first.
4. **Removals:** a task the product no longer offers loses its page, and every removal is listed in
   the report, so a human can veto it in review.

## Structure

```text
docs/documentation/guides/
├── index.md             # Who this is for: one line per persona, linking their directory
└── one-persona/
    ├── index.md         # What this persona does with the product, and their tasks in order
    └── one-task.md      # One task per page, titled as the reader would say it: "Invite a teammate"
```

Every task page has the same shape:

1. **Before you start** — the role it needs, and what must already exist.
2. **Steps**, numbered. One action each, with the exact label in bold, and a role note inline where a
   role changes that step.
3. **What you see when it worked.**
4. **If it did not** — the messages the product can show at this point, from the validation and
   error paths in the code, and what each one means for the reader.
5. **Related** — the next task, and a link to the documentation for anything conceptual.

The conventions are the documentation's, because the two share one site: `index.md` as each
directory's landing page, kebab-case filenames, one H1 per file, relative Markdown links only.
**Navigation is read from the filesystem** — a page's sidebar entry is its H1.

## Verification

**With a site generator:** run `<DOC BUILD COMMAND>` before committing. Its output,
`<DOC BUILD OUTPUT>`, is gitignored and stays that way. The build checks every link between the
guide and the documentation, so a dead one fails here rather than in front of a user.

**Without one:** check every relative link and anchor in the pages you touched by reading them.

**Either way, check every quoted label against the code.** Search the source for each bold label
on the pages you touched. A label the code does not contain is a step the user cannot follow.

## Delivery

`delivery.md` owns the branch, the push, the pull request and the merge. Two obligations are yours
alone:

1. **Commit with the subject line `docs: update product guide`**, and give the pull request that
   same title. It is the string step 1 searches for, so it is the only one in this file that must
   not be reworded.
2. Report back, for the pull request description: the pages added and updated per persona, every
   **removal**, every ⚠️ conflict, and every link the documentation should now carry to the guide.
