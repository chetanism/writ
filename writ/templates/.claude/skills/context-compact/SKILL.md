---
name: context-compact
description: Compact CLAUDE.md back under its budget — move whole sections into the documents and skills that own them, leave a one-line pointer behind, and lose no fact — delivered on its own branch through a pull request. Use when `ledger.py check` warns that the agent map is over budget, when CLAUDE.md has grown long or repetitive, or when asked to trim, compact or shorten it.
---

# Compact the agent map

`CLAUDE.md` is read at the start of every session, so every line in it is paid for on every task,
forever. `DoD-8` adds to it each time a slice establishes a convention and nothing takes anything
out; this pass is what takes things out. Invoked as `/context-compact` on its own, or by
`/maintenance` as the last of its four passes.

**This file owns what changes.** `.claude/skills/maintenance/delivery.md` owns the branch, the
commits, the pull request and the merge — read it first, and run this pass inside its loop.

> **You are moving text, not editing it.** Nothing here licenses deciding a convention is wrong, or
> that a rule has lapsed. A line whose truth you doubt goes in the report, unchanged and in place.

## 1. Measure first

```bash
python3 scripts/ledger.py check          # the budget warning, if it is over
wc -c CLAUDE.md                          # the number itself
```

The budget lives in `scripts/ledger.config.json` under `context_budget`: `warn_chars` is where this
pass becomes worth running, `max_chars` is where the build fails. **Under the budget, the scope is
empty** — say so with the number, and go to `delivery.md` step 8. A compaction run with nothing to
compact is how a file loses a section somebody needed.

Record the starting number. The report quotes it against the finishing one.

## 2. What belongs in `CLAUDE.md`, and what does not

The test, for every section and every line:

> **Would an agent write the wrong code without it, on a task that never opens the file it came
> from?**

If yes, it stays — in one line. If it is reference that an agent consults *when it is already doing
that thing* — a procedure, a rationale, an enumeration of cases, a worked example — the document or
the skill that owns that thing is where it belongs, and `CLAUDE.md` keeps a pointer.

**These never leave, whatever the file weighs:** *Project state*, the precedence order, the document
map, the identifier rule, the conventions list and §Git. They are the reason the file is read at
all. If those alone are over `max_chars`, the finding is that the project has outgrown the budget —
say so and propose a number rather than gutting the map.

## 3. Where a section goes

| What it is | Where it goes |
|---|---|
| A procedure with steps | the skill that runs it, under `.claude/skills/` |
| Why one option was chosen over another | an ADR in `writ/decisions/` — **and the line here points at it by number** |
| A rule about how we build — the loop, the gate, sizing, review | `writ/process/DEVELOPMENT-PROCESS.md` |
| A shape everything inherits — an error envelope, an id scheme, a layering rule | the foundation spec `writ/spec/<AREA>-SPEC.md` that owns that area |
| A convention plus its example, its counter-example and its history | the convention stays as **one line**; everything after the first sentence moves to the document that line points at |
| What the product does today | `docs/documentation/` — **`/product-docs` owns it**, so raise it in the report rather than writing there |
| What we used to do, and stopped | delete it. Git holds it, and a superseded rule in the agent map is read as a live one |

A move that has no destination in this table is a move you have not thought through yet. Put it in
the report and leave the section alone.

## 4. The rules of the move

- **No fact is lost.** Every sentence removed is either in the destination file, word for word or
  compressed, or explicitly deleted as superseded and named in the report. A compaction that loses
  a convention is a worse outcome than the file being long.
- **Leave the pointer in the same place the section was.** A reader who knew where to look still
  finds something there: one line saying what the rule is and which file carries it. A section that
  vanishes reads as a rule that was dropped.
- **Never restate.** Once a rule lives in `DEVELOPMENT-PROCESS.md`, `CLAUDE.md` links to it and says
  nothing else about it. Two wordings of one rule is two rules, found the day they disagree.
- **Do not move a fact into a file that is itself read every session.** Check the other entries in
  `context_budget.files` before choosing a destination.
- **The destination keeps its own shape.** A paragraph appended to a register, a table row added to
  a narrative, an ADR edited after acceptance — each breaks a rule `ledger.py check` enforces. If
  the text does not fit any document's shape, it belongs in a new ADR or nowhere.
- **One commit per destination**, so a reviewer reads one move at a time.

## 5. Verify

1. `python3 scripts/ledger.py check` — green, and the budget warning gone. It is the check that
   proves the moves did not break a register, a narrative or a reference.
2. The gate, as `delivery.md` step 4 names it — green. This pass touches no code, so a red gate
   means something else is broken, and this pull request is not the place to find out.
3. **Read `CLAUDE.md` end to end as though you had never seen the repository.** The questions it
   must still answer without opening anything else: where does truth live, what are the
   identifiers, how does work proceed here, what is binding, what must never be done.
4. **Diff the facts, not the lines**: for each removed section, name the file and heading that now
   carries it. A section you cannot point at is one to restore.

## 6. Delivery

`delivery.md` owns the branch, the push, the pull request and the merge. Three obligations are this
pass's own:

1. **Commit with the phrase `compact the agent map`** in the message, and title the pull request
   `docs: compact the agent map DATE`. Unlike the other passes, this marker is not how the next run
   finds its scope — the budget is — but it is how a reader finds where a section went.
2. **The pull request body is a table of moves**: what was removed, where it now lives, and the
   line left behind. Plus the starting and finishing character counts, and the budget.
3. **Report what you did not move** — every section that was over-long with no honest destination,
   every rule whose truth you doubted, and anything belonging to `docs/documentation/`. Those are
   the human's to decide, and a pass that quietly resolves them is the failure this section exists
   to prevent.
