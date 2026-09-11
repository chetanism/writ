# `/context-compact`

**The only thing in the entire process that ever takes a line *out* of `CLAUDE.md` — moving whole
sections into the documents that own them, leaving a one-line pointer behind, and losing no fact.**

| | |
|---|---|
| **Run it** | When `ledger.py check` warns the agent map is over budget. **A trigger, not a cadence** |
| **Produces** | A shorter `CLAUDE.md`, content relocated into the documents and skills that own it, on a branch |
| **Never** | Deletes a fact. Everything moves; nothing evaporates |

## Why this exists

**`CLAUDE.md` is read at the start of every session, so every line in it is paid for on every task,
forever.**

`DoD-8` adds to it each time a slice establishes a convention. Nothing else ever takes anything out.
Left alone for a milestone, the document every session begins with costs more than it earns — and
because the cost is spread across every task, nobody ever notices it as a problem with a cause.

So: a budget in `ledger.config.json`, a warning at `warn_chars`, a failing check at `max_chars`,
and this pass as the remedy. **A budget with no remedy is a rule people learn to route around** —
which is why this is one of the three parts of the process with no switch.

## What it does

1. **Measures first**, so the before and after are numbers rather than impressions.
2. **Decides what belongs** — an agent map says where things are and what the conventions are, not
   what the requirements say or how the process works.
3. **Moves a whole section** into the document that owns it — the process document, a foundation
   spec, a skill — and leaves a one-line pointer.
4. **Verifies** that no fact was lost and that the check now passes.
5. **Delivers** through the shared maintenance loop.

## The test for a line in `CLAUDE.md`

**Would an agent write the wrong code without this line?** If the answer is no, it belongs
somewhere a reader goes looking rather than somewhere every session pays for.

## See also

[`/maintenance`](maintenance.md), where it runs last — after cleanup, documentation and the audit
have each had their chance to add to the map.
