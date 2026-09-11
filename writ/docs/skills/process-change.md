# `/process-change`

**Changes the development process itself — one change at a time, read back as the table of files it
lands in before anything is edited, recorded in `DEVELOPMENT-PROCESS.md` §15, then checked.**

| | |
|---|---|
| **Run it** | When a rule does not fit your team, when a part should be switched off, tightened or widened, or when something should be added to the definition of done |
| **Produces** | The change, landed in every file it touches, plus its record in §15 — on a `process/` branch through a pull request |
| **Refuses to** | Decide. **Edit `scripts/ledger.py`. Switch a check off to get a green run.** |

## Why it exists

**A process change almost always lands in more than one file, and landing in only some of them is
worse than not changing it at all.**

A rule changed in the prose and not in `scripts/ledger.config.json` is a documented rule the build
does not enforce. Changed in the config and not the prose, it is an enforced rule nobody agreed to.
Both are silent, both surface weeks later as a build failure no document explains, and both are
**the exact failure this process exists to prevent, committed by the people running it.**

The interview is the easy half of this skill. The landing table is the half that earns it.

## The landing table

Before editing anything, it puts the change in front of you as the files it would touch:

```
smaller slices · requested by Priya · because the last six S slices all came in over tier

edit   scripts/ledger.config.json            size_budget  S 150 → 100, M 400 → 250
edit   writ/process/DEVELOPMENT-PROCESS.md  §2.1 the tiers · §15 the record
none   CLAUDE.md                             the map does not carry the tiers
none   .github/workflows/                    the check reads the config

Costs    stats compares each slice against the tier in force when it closed, so the
         estimate-accuracy series has a discontinuity at this commit, not a trend
Breaks   nothing. No open work order carries a size that is now out of tier
Ask      1. Do the new tiers apply to the four slices already claimed, or from here?
```

**The `none` rows are findings, not filler** — writing *this file does not change* is how you
notice the file that does. And **if the table has one row, it looks again**: a genuine one-file
process change exists, but the second row is usually §15.

## It argues the other side, once

**Every rule in the process was written against a specific failure**, and the skill names that
failure before it proposes a change. Two outcomes, and it does not get to pick which:

- The rule is wrong for your team — it was written for a different shape of project. Change it.
- The rule is doing its job in a way that is uncomfortable on purpose. It says so plainly, says
  what happens in three months without it, **and then does what you decide anyway.**

It says it once. A skill that relitigates a decision is one people stop invoking — and then the
change happens anyway, with no record at all, which is strictly worse.

## The three with no switch

§15 names three parts of the process with no switch: the declaration rule, `/context-compact`, and
the by-hand demo. **None is forbidden.** Asked to remove one, the skill gives the warning and an
*alternative remedy* rather than a refusal — bend the declaration rule by adding registry rows;
replace `/context-compact` with a different remedy, not with no remedy; change what the demo *is*
rather than whether it happens. Then it records whatever you decide.

**A decision to drop one of these, written down, is far better than the same decision made by
attrition.**

## The two fences

**It never edits `scripts/ledger.py`.** The config the tool reads, yes; the tool itself, never. A
skill that can edit the thing that checks it can make any process change pass. A change that
genuinely needs the tool changed is a slice, with a work order and a review.

**It never turns a check off as a side effect of another change.** If the change makes
`ledger.py check` fail, that is a finding to report, not a cleanup task — switching it off to get a
green run is how a process gets hollowed out one convenience at a time, and in the diff it looks
exactly like tidying up.

A third, specific to an adopted repository: **widening `enforce` is its own change and never a side
effect.** Turning `work_order` on over a directory means other people's pull requests start failing
for a rule that arrived in a commit they did not read.

## What it reports

What changed and where, what it costs, what it deliberately did not touch — and the line that
matters most, which a diff cannot say: **what the team now does differently.** *From the next
slice: S is 100 lines, not 150. Nothing already claimed changes.*

## See also

[Changing the process](../changing-the-process.md) — the same ground for a person rather than an
agent, with twenty common changes and the switch behind each.
[`/change-request`](change-request.md) — the symmetric skill, for changing what the **product**
does rather than how work is done.
