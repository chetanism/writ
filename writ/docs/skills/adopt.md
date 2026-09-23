# `/writ:adopt`

**Puts the process around a codebase that already exists — surveying its git history, reading its
tests as the requirements document they already are, recording its debt honestly, and enforcing
absolutely nothing on day one.**

| | |
|---|---|
| **Run it** | Once, on a repository that already has code — especially one other people are still working in |
| **Produces** | A `writ/` tree, a survey, a debt register, `scripts/survey.py`, and **an enforcement perimeter with every rule switched off** |
| **Commits to** | `docs/adopt-writ` — not `dev`. It is a documentation branch, because that is all it is |
| **Never** | Turns a rule on over somebody else's directory |

## The reframe

**Agents read code well. Document only what the code cannot say about itself.**

Greenfield, the documents come first and say what to build. Here the code exists and already has
opinions, so the question is not *how do we write this codebase down* — it is **what does an agent
need that reading the source will not give it?** There are five such things, and none of them is in
the source:

1. Which of three similar modules is the live one.
2. What is deprecated but still called.
3. Why something is the way it is.
4. What breaks **invisibly** when this is touched.
5. Where the edge of *safe to change* is.

A survey that produces forty pages describing the architecture has failed — the agent could have
read that, and now there are two descriptions to keep in step. Two pages of *this is dead, this is
load-bearing, this must never break, these three things are strange for a reason* is worth ten
times as much per line.

## The trap it is built to avoid

**Do not survey everything first.** Reverse-engineering every requirement before starting produces
two hundred rows nobody has read, a coverage ledger at zero, and abandonment in three weeks. Worse,
it is *convincing* while it happens: the directory fills up, and looking like coverage is exactly
the failure this process is written against.

So: **document an area as part of the first slice that touches it.** Two tiers — *the map* (areas,
invariants, gate roles, debt, `CLAUDE.md`; one sitting) and *the territory* (the register rows and
detail files, pulled by the work that needed them).

## What only this skill ships

| | |
|---|---|
| **`scripts/survey.py`** | Reads the codebase's shape out of its git history — churn, co-change, quiet files, who is the only person to have touched a directory. **The one body of evidence an agent has no access to,** because it is not in the working tree |
| **`writ/spec/debt.md`** | `DEBT-NNN` rows: things true of the code that should not be. Filled *before* requirements, because a specification reverse-engineered from working code otherwise promotes every old bug to a requirement |
| **A `Provenance` column** | `decided` (somebody chose this) versus `observed` (read off code that runs). `/requirement-detail` on an `observed` row is what promotes it — and reliably, as a side effect, what finds bugs |
| **`≈ inherited` coverage** | A requirement with tests and no claiming slice. Distinct from `◐ partial`, which is a promise somebody made and did not keep |
| **`kind: characterisation`** | A slice that changes no behaviour and pins what the code already does. The only kind that may declare `demo: none` |
| **The enforcement perimeter** | `enforce` in the ledger config: which paths each rule is in force over. It starts empty |
| **`out_of_order: backfill`** | An adopted codebase is built ahead of its requirements by definition. Every inherited requirement is a backfill queue in `COVERAGE.md`, most urgent first, rather than a red build; a requirement that has caught up is locked, and a milestone cannot be marked `done` until its requirements have caught up |

## Arriving in a team that has not agreed to it

**Every rule starts off, and you climb the ladder one rung at a time.** The failure this is shaped
around is not technical: turn every rule on over somebody else's directory and their pull requests
start failing for rules that arrived in a commit they never read. That is how a process is deleted
from a repository inside a week, and being right about the rules does not save it.

| | Rung | Who is affected |
|---|---|---|
| 0 | Survey, `CLAUDE.md`, area map, debt register. Nothing in CI | Nobody else |
| 1 | Your own slices | Nobody else — **the team just sees better pull requests, which is the only marketing that works** |
| 2 | The annotation harvest | Nobody else |
| 3 | **A second person, by pairing on a slice** | One colleague, by choice |
| 4 | Perimeter on, one area | Anyone touching that directory |
| 5 | Team mode — WIP limits, collisions | Everyone running the loop |

**Rung 3 before rung 4, and hold that firmly.** Do not block other people's work until at least two
people run the loop, or the process is one person's pet that blocks everyone else and dies the week
they go on holiday.

**The annotation harvest (rung 2) is the highest-return move in the whole adoption and it is
mechanical.** Your suite already contains hundreds of tests that are a requirements document
somebody wrote. Adding `[FR-012]` to a describe block is seven characters and cannot break
anything. On an existing codebase, **coverage is earned by naming the tests you already have.**

## See also

[`../references/12-survey.md`](../../references/12-survey.md) — what to document and what the code
already says. [`../references/13-adoption.md`](../../references/13-adoption.md) — the perimeter, the
ladder, and the three things that decay.
