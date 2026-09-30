# `/context-compact`

**The only thing in the entire process that ever takes a line *out* of `CLAUDE.md` or
`CONVENTIONS.md` — moving whole sections into the documents that own them, taking each convention
back to its rule and citation, leaving a one-line pointer behind, and losing no fact.**

| | |
|---|---|
| **Run it** | When `ledger.py check` warns the agent map or `CONVENTIONS.md` is over budget. **A trigger, not a cadence** |
| **Produces** | A shorter `CLAUDE.md` or `CONVENTIONS.md`, content relocated into the documents and skills that own it, on a branch |
| **Never** | Deletes a fact. Everything moves; nothing evaporates |

## Why this exists

**`CLAUDE.md` is read at the start of every session, so every line in it is paid for on every task,
forever.**

`CONVENTIONS.md` is its other half: the rules set by earlier slices, one section per area, and the
sections a change touches are read before its code. `DoD-8` adds to it each time a slice establishes
a convention. Nothing else ever takes anything out. Left alone for a milestone, the documents every
change begins with cost more than they earn — and because the cost is spread across every task,
nobody ever notices it as a problem with a cause.

So: a budget per file in `ledger.config.json`, a warning at `warn_chars`, a failing check at
`max_chars`, and this pass as the remedy. **Both files are capped**, because a cap on the agent map
alone moves the growth into the file it points at. **A budget with no remedy is a rule people learn to route around** —
which is why this is one of the three parts of the process with no switch.

## What it does

1. **Measures first**, so the before and after are numbers rather than impressions.
2. **Decides what belongs** — an agent map says where things are and what the conventions are, not
   what the requirements say or how the process works.
3. **Moves a whole section** out of `CLAUDE.md` into the document that owns it — the process
   document, a foundation spec, a skill, a section of `CONVENTIONS.md` — and leaves a one-line
   pointer.
4. **Takes each convention back to its rule and its citation**, where the slice summary or ADR it
   cites already carries the story, and replaces a rule that has become a check with the check's
   name.
5. **Verifies** that no fact was lost and that the check now passes.
6. **Delivers** through the shared maintenance loop.

## The test for a line in `CLAUDE.md`

**Would an agent write the wrong code without this line?** If the answer is no, it belongs
somewhere a reader goes looking rather than somewhere every session pays for.

## See also

[`/maintenance`](maintenance.md), where it runs last — after cleanup, documentation and the audit
have each had their chance to add to the map.
