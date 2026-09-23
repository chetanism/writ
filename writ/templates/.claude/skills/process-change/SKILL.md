---
name: process-change
description: Change this repository's own development process — one change at a time, landed in every file it touches, recorded in DEVELOPMENT-PROCESS.md §15, and verified. Use when a rule does not fit the team, when a part should be switched off, tightened or widened, when a definition-of-done row, identifier family or gate role should be added, or when the user says to change, tune or turn down the process.
---

# Change the process

`writ/process/DEVELOPMENT-PROCESS.md` is this team's document, not a library's. It was written to
be changed as the team learns what actually works here, and a team that has never changed it is
usually a team that has stopped reading it. **You are drafting, not deciding** — a process change
binds everybody who works in this repository, so what you produce is a proposal somebody says yes
to.

Invoked as `/process-change`.

**The failure this exists to prevent is a change that lands in some of its files and not the rest.**
A rule changed in the prose and not in `scripts/ledger.config.json` is a documented rule the build
does not enforce. Changed in the config and not the prose, it is an enforced rule nobody agreed to.
Both are silent, both are discovered weeks later by somebody whose build fails for a reason no
document explains, and both are the exact failure this whole process exists to prevent — committed
by the people running it. The interview below is the easy half of this skill. **The landing table
in step 4 is the half that earns it.**

A process change is nobody's slice. It consumes no WIP, advances no requirement and closes no
issue.

## 0. One change at a time

**One change per invocation.** Given several, do the first and stop. *Smaller slices and drop the
scenario track* is two changes: they have different costs, different people care about them, and
bundled they get one answer that was really only about one of them.

## 1. Refuse the ones that are not yours

- **A change to what the product does** — a requirement added, amended or withdrawn. That is
  `/change-request`, and it changes the specification rather than the process. Say so and offer it.
- **A choice between alternatives with no rule behind it** — that is an ADR in `writ/decisions/`.
- **A change to the code** — including to tooling the project owns. That is a slice.
- **A one-off exception.** *Skip the demo just for this slice* is not a process change; there is
  nothing to write down. The honest options are to do it and say so plainly at close, or to change
  the rule for everybody. **A rule with a private exception is a rule that has been switched off
  without a record**, which is the one outcome §15 was written to avoid.
- **A change to `scripts/ledger.py`.** Never, from this skill. See step 6.

## 1a. Get onto the change's branch

**One change, one branch**, `process/<slug>` — `process/smaller-slices`. The dirty-tree rule and
the four cases are `/requirement-detail`'s step 1a, unchanged. Where there is no remote, the branch
is local and the pull request waits, and you say so.

## 2. Read before proposing anything

| Read | For |
|---|---|
| `writ/process/DEVELOPMENT-PROCESS.md`, **the section that states the rule, and §15** | What the rule actually says, and what has already been turned down and why |
| `scripts/ledger.config.json` | The machine half of the same rule — every switch, path, budget, family and glob |
| `CLAUDE.md` | Whether a session is told anything about this rule at the start of every task |
| `.claude/skills/<the skill that performs the step>/SKILL.md` | The step as it is actually carried out |
| `.github/workflows/` | What the gate really runs, which is not always what §5 says it runs |
| `python3 scripts/ledger.py stats` | **Before any change about sizing, cadence, coverage or a backlog** |

That last row is not optional. Most process complaints are about a number — the slices feel too
big, the audit feels overdue, the detail track feels stalled — and the number is already measured.
A change proposed against the measurement is a different conversation from one proposed against an
impression, and occasionally the measurement ends the conversation.

## 3. Say what the rule is for, before saying how to change it

**Every rule here was written against a specific failure.** Name it, in a sentence or two, and say
whether it applies to this team. There are two honest outcomes and you do not get to pick which:

- **The rule is wrong for this team.** It was written for a different shape of project, or the
  failure it prevents is one this team cannot have. Change it.
- **The rule is doing its job, in a way that is uncomfortable on purpose.** Say that plainly, say
  what happens in three months without it, and then **do what they decide anyway.** It is their
  process.

**Say it once.** Never argue the same point twice: a skill that relitigates a decision is one
people stop invoking, and then the change happens anyway with no record at all — which is strictly
worse than the change they asked for.

## 4. Read the change back as a landing table, before editing anything

**Do not edit anything yet.** Put the change in front of them as the files it would touch:

```
faster warnings · requested by Priya · because the slow fortnight in August went unflagged for a month

edit   scripts/ledger.config.json            velocity  drop_ratio 0.5 → 0.6, trailing_weeks 3 → 2
edit   writ/process/DEVELOPMENT-PROCESS.md  §15 the record
none   CLAUDE.md                             the map does not carry the thresholds
none   .github/workflows/                    velocity never runs in the gate

Costs    a two-week average is noisier: one holiday week now trips the flag
Breaks   nothing. The check reports; it never fails a merge
Ask      1. Apply from the next /maintenance run?
            a. Yes (recommended) — nothing is in flight that it changes.
            b. Replay it over the last two months first — shows how often it would have fired.
```

Four things about that table:

- **`none` rows are findings, not filler.** Writing *this file does not change* is how you notice
  the file that does.
- **If the table has one row, look again.** A genuine one-file process change exists — a cadence,
  a threshold — but it is rarer than it looks, and the second row is usually §15.
- **`Breaks` is where you name work already in flight**: an open work order, a detail file under
  review, a claimed slice whose rules would change underneath it.
- **`Ask` is at most two questions**, in the shape of `CLAUDE.md` §*Asking me to decide* — lettered
  options, each saying why it is or is not recommended, one marked recommended.

Then stop and wait.

## 5. The three with no switch

`DEVELOPMENT-PROCESS.md` §15 names three parts with no switch. **They are not forbidden** — nothing
here is forbidden — but each is load bearing for something else, so a request to remove one gets a
warning and an alternative rather than a refusal:

| Asked to remove | Say | Offer |
|---|---|---|
| **The declaration rule** | Every tool, check and generated file reads it; removing it is a rewrite, not a setting | It bends by adding rows to `writ/spec/ID-REGISTRY.md` — new families, widths and owners, all Markdown. Ask what they actually need to declare |
| **`/context-compact`** | `DoD-8` adds a line to `CLAUDE.md` every slice and nothing else removes one; without a remedy that file only grows, and it is read at the start of every session | A different remedy, not no remedy — a bigger budget, a quarterly pass, a rule that `DoD-8` replaces rather than appends |
| **The by-hand demo** | It is enforced by nothing, so there is nothing to switch off: it stops the day somebody stops doing it, and no build ever goes red | Change what the demo *is* — shorter, recorded, played by one person for three slices — rather than whether it happens |

Then do what they decide, and record it in §15 like anything else. **A decision to drop one of
these, written down, is far better than the same decision made by attrition.**

## 6. Two things this skill never does

**1. It never edits `scripts/ledger.py`.** The config it reads, yes; the tool itself, never. A
skill that can edit the thing that checks it can make any process change pass, and at that point
nothing in this repository means anything. A change that genuinely needs the tool changed is a
slice, with a work order and a review, like any other code.

**2. It never turns a check off as a side effect of another change.** If applying the change makes
`ledger.py check` fail, that is a finding: report which check, what it is now unhappy about, and
stop. Switching it off to get a green run is how a process gets hollowed out one convenience at a
time — and it looks, in the diff, exactly like tidying up.

One more, specific to this repository's perimeter: **widening `enforce` is its own change and never
a side effect.** Turning `work_order` on over a directory means other people's pull requests start
failing for a rule that arrived in a commit they did not read. If that is the change, say it out
loud as the change, and say whether a second person has actually run a slice yet.

## 7. Write it, then record it, then check it

Apply **every row** of the table — the `none` rows are the ones you have already confirmed need
nothing, so what is left is exactly the set to edit. Then the record, which is the step people skip:

- **A row in §15**: what changed, why, and what it costs. If the change turned something on rather
  than off, it still goes here — §15 is the register of *what this team decided about its own
  process*, not only of what it removed.
- **One line in `CLAUDE.md`**, where the change touched a gate role or a check, so the next session
  reads *we chose this* rather than *this seems to be broken.*

Then verify:

```bash
python3 scripts/ledger.py          # regenerate
python3 scripts/ledger.py check    # must exit 0
python3 scripts/test_ledger.py     # if the change touched anything the tool reads
python3 scripts/ledger.py stats    # and read it — the numbers should still mean what you think
```

A non-zero exit means a document you just changed disagrees with one you did not. **That is the
check doing its job, and it is never fixed by relaxing it** (step 6).

Commit, push, and open the pull request with the landing table as its body. A process change is
reviewed by whoever the change binds.

## 8. Report

A dozen lines, and one of them is the one that matters:

- What changed, and in which files.
- What it costs, restated from the table — the reviewer should not have to reconstruct it.
- What it deliberately did **not** touch.
- **What the team now does differently.** This is the part a diff cannot say and the part everybody
  needs. *From the next slice: S is 100 lines, not 150. Nothing already claimed changes.*

Then say where it is recorded, so the next person arguing about this rule finds the last argument
before starting a new one.
