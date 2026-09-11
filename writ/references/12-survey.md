# Surveying an existing codebase

## The governing rule

> **Document what the code cannot tell you, and nothing else.**

Greenfield, the documents come before the code and say what to build. Here the code exists and it
already has opinions, so the question is not *how do we write this codebase down* — it is **what
does an agent need that reading the source will not give it?**

Agents read code well. They are bad at exactly five things, and none of the five is in the source:

1. Which of three similar modules is the live one.
2. What is deprecated but still called.
3. Why something is the way it is — the record nobody wrote.
4. What breaks *invisibly* when this is touched.
5. Where the edge of "safe to change" is.

A survey that produces forty pages describing the architecture has failed: the agent could have
read that, and now there are two descriptions to keep in step. One that produces two pages of
*this is dead, this is load-bearing, this must never break, these three things are strange for a
reason* is worth ten times as much per line. It is the same test `CLAUDE.md` is held to — **would
an agent write the wrong code without this line** — applied to a whole tree.

## The trap, which is the obvious plan

Survey everything first. Reverse-engineer every requirement, fill every register, then start.

It produces two hundred rows nobody has read, a coverage ledger at zero, and abandonment in three
weeks, because it is all cost and no return. Worse, it is *convincing* while it is happening: the
directory fills up, and looking like coverage is exactly the failure the requirement track's own
rules are written against.

**Document an area as part of the first slice that touches it.** The whole bet of this process is
that documents are read before code is written; a requirement for a subsystem nobody will touch
this quarter is never read, so writing it now is waste. Documenting at the boundary of change puts
the writing at the moment it is cheapest — somebody is about to read that code anyway — and makes
the work that needed it pay for it.

So: two tiers.

| Tier | When | What |
|---|---|---|
| **The map** | One sitting, before anything else | Areas, invariants, gate roles, debt, `CLAUDE.md`. Enough for an agent to orient and for the tools to run |
| **The territory** | Pulled by work, one area at a time | The register rows, the detail files, the scenarios — written by the slice that needed them |

## Tier one — the map

### Start with git, not with the source

`python3 scripts/survey.py` reads the shape out of the history. It is an input to the interview
and never a finding: a file changed ninety times may be a configuration somebody keeps bumping,
and two files that always move together may both be touched by the formatter.

What each section is for:

| Section | The question it hands you |
|---|---|
| **Areas** | Are these the requirement areas, and what are they called? Survey them in this order |
| **Hotspots** | What keeps bringing people back to this file? The answer is usually a requirement nobody wrote |
| **Coupled** | What rule holds these two together? **A rule neither file states is an `INV-*`** — this is the cheapest way to find one |
| **Quiet** | Is this dead? Stable and abandoned are identical in a log, and only a person can tell you which |
| **One pair of hands** | Who do you interview, and who do you bring into the process second |

History is the right source because it is the one thing an agent has no access to. It is not in
the working tree, so no amount of reading the code recovers it.

### Then read the tests, not the source

**The existing suite is a requirements document somebody already wrote.** Test names, describe
blocks and fixture names say what the system is supposed to do, in the words of the person who
built it, and they are far closer to intent than the implementation is. Read those into candidate
rows before you read a single module.

This also sets up the single highest-return move available (`13-adoption.md` §*The annotation
harvest*): those tests, annotated, are coverage.

### Write down what is wrong before what is required

`writ/spec/debt.md` — `DEBT-NNN`, one row each. A specification reverse-engineered from working
code describes what the code does, and some of what the code does is a mistake nobody has had time
to fix. Without a register for that, the surveyor has two options and both are bad: promote the
mistake to a requirement, or leave it out so the next reader rediscovers it.

Filling this register first is also what makes the survey *honest*, and honesty is what gets the
process adopted. A specification that reads as though the codebase were clean is one every
developer on the team knows to be false on day one.

### Invariants are the highest-value rows and the hardest to recover

An invariant is a shape rather than a capability, so it belongs to no area anybody would think to
search, and it is almost never stated anywhere. You will not read them off the source. You get
them from four places, in rough order of yield:

1. **Coupled files in the survey** — a rule two files share and neither states.
2. **Defensive code.** A guard clause with no obvious caller is a scar. Ask what happened.
3. **Incidents and support tickets.** An invariant is usually somebody's bad week, written down.
4. **The person who has been there longest**, asked *what would you never let a new joiner do?*

Then the brownfield question greenfield never has to ask: **is it currently true?** A greenfield
invariant is guarded by the slice that introduces it. An inherited one is an assertion with an
unknown truth value, and finding out is real work. Record it, mark it unverified, and let a
characterisation slice settle it.

## Provenance — the column that stops a bug becoming a requirement

An adopted register carries a `Provenance` column and a greenfield one does not:

| Value | Means |
|---|---|
| `decided` | Somebody chose this. It is intent |
| `observed` | Read off code that already runs. It is a description |

The distinction is load-bearing. **A requirement read off the code makes every bug old enough to
be relied upon into a requirement**, indistinguishably from the real ones, and six months later
nobody can tell which rows anybody ever agreed to.

`/requirement-detail` on an `observed` row asks the question that promotes it: *is this what it
should do?* That is how `observed` becomes `decided`, and it is also — reliably, and as a side
effect — how the survey finds bugs. `ledger.py stats` counts what is left, and that count is the
real documentation backlog.

## What not to write

- **Anything the code says plainly.** A description of a module's structure is a second copy of
  the module, and the second copy is the one that goes stale.
- **A requirement for behaviour nobody is going to touch.** It will never be read. It can be
  written the day a slice needs it, for the same cost, with better information.
- **An invented number.** An SLO nobody gave you is worse than none, because everything downstream
  gets sized against it. The greenfield rule holds here exactly.
- **A clean story.** If three areas are a mess, the survey says so — in `debt.md`, with rows.

## The order of the sitting

1. `survey.py`, read to the user, section by section. Their corrections are the real map.
2. Areas confirmed and named. These become `writ/spec/requirements/<AREA>/index.md`, mostly empty.
3. Invariants, from the four sources above. These are the rows worth the most per line.
4. Debt, before requirements.
5. The stack and the gate roles — and **run each command** rather than believing the README.
6. `CLAUDE.md`, including a *Project state* paragraph that is true today.

Nothing in tier two happens in this sitting. Say so out loud at the end, because a user who
expects the whole codebase documented will read a correct stopping point as an incomplete job.
