# Changing the process

> **Skim rule for this page.** The bold lead of each section is the answer. The
> [table of common changes](#the-changes-teams-actually-make) is the part to bookmark.

---

## It is not a library. It is your documents.

**Nothing of the kit is installed into your project. The bootstrap writes files, commits them, and
leaves — there is no dependency to upgrade, no version to track, and nothing that will overwrite
your edits.** `DEVELOPMENT-PROCESS.md` is a file in your repository with your team's name on it.
Change it the way you would change any other file you own.

This needs saying because everything about the way the process arrives suggests otherwise. It comes
from a plugin, it has a version number, it generates files, and it has a CI gate that fails when
you get things wrong — all of which reads like a framework whose rules you are obliged to obey.
It is not one. The kit's whole job was the first hour. After that it is out of the picture, and the
process is a document that a team edits as it learns what actually works for it.

**A process nobody can change is one people route around, and routing around it is worse than
changing it** — the change is a decision somebody can find, and the routed-around part looks like
it is still running while everyone quietly ignores it. That asymmetry is why the process ships with
switches, why each switch says what it costs, and why exactly three things are marked as having no
switch at all.

### Expect to change it three times in the first milestone

This is normal and it is the intended use. The changes that come up first, almost every time:

1. **The velocity thresholds are wrong for your team.** They are a guess until you have a month of
   merges; `python3 scripts/velocity.py` shows what normal looks like.
2. **A standing pass runs too often or not often enough.** The bootstrap asked; you answered before
   you knew.
3. **Something in the definition of done does not apply to you,** or something that matters to you
   is not in it.

None of those is a failure of the process. They are the process doing the thing it was built to do:
making its own rules visible enough to argue with.

---

## The short way: `/process-change`

**Your project ships a skill for exactly this.** `/process-change` reads the rule and names the
failure it was written against, reads the change back as the table of files it would land in,
applies it, records it in §15, and runs the check.

```
/process-change
> our S tier is too big — the last six all came in over
```

Its one real job is the table. **A process change almost always lands in more than one file**, and
a change that lands in only some of them is worse than no change at all: a rule changed in the
prose and not in `scripts/ledger.config.json` is a documented rule the build does not enforce, and
the other way round it is an enforced rule nobody agreed to. Both are silent.

Two things it will not do: edit `scripts/ledger.py`, and switch a check off to get a green run.
[Its page](skills/process-change.md) says why.

**The rest of this document is the same ground for a person** — worth reading once so that you know
what the skill is doing, and necessary if you are working with an agent that does not have it.

## How to change it by prompting

**Describe the outcome you want in a sentence, tell the agent to find every place it lands, and
make it show you the list before it edits anything.** That is the whole technique.

The reason for the middle clause is the one thing that makes process changes different from code
changes: **a single process change almost always lands in more than one file**, and a change that
lands in only some of them is worse than no change at all, because the documents now disagree and
the disagreement is silent. The places a process change can land:

| Where | What lives there |
|---|---|
| `scripts/ledger.config.json` | Every switch, path, budget, family and glob the tool reads |
| `writ/process/DEVELOPMENT-PROCESS.md` | The rule as written for people — the loop, the definition of done, the cadence, §15 |
| `CLAUDE.md` | What an agent is told at the start of every session |
| `.claude/skills/<name>/SKILL.md` | The skill that performs the step you changed |
| `.github/workflows/` | What the gate actually runs |
| `writ/spec/ID-REGISTRY.md` | Identifier families — the declaration rule bends here and nowhere else |
| `writ/process/templates/` | The shape of a work order, summary, detail file or scenario file |

### The prompt shape that works

```
Read writ/process/DEVELOPMENT-PROCESS.md and scripts/ledger.config.json first.

I want to <the outcome, in one sentence>.

Before editing anything: list every file that has to change, what changes in each,
and anything this breaks or makes inconsistent. Then stop and wait.
```

Three things are doing work there:

- **Naming the two documents to read first** stops the agent inferring the process from whichever
  file it opened. `DEVELOPMENT-PROCESS.md` is the prose rule; the config is the machine one; a
  change that satisfies one and not the other is the exact failure mode to avoid.
- **Stating the outcome, not the edit.** *Tell me sooner when we slow down* gets you a better
  answer than *change `drop_ratio` to 0.6*, because the agent can tell you that `/maintenance` and
  `stats` both read it, and what a tighter threshold would have flagged in the last two months.
- **Stop and wait.** Process changes are cheap to review as a list and expensive to review as a
  diff across seven files.

### Then verify it, because the process has a gate of its own

```bash
python3 scripts/ledger.py check    # the documents still agree with each other
python3 scripts/ledger.py stats    # and the numbers still mean what you think
```

If the change touched the tool itself, `python3 scripts/test_ledger.py` is in your repository too.
**A process change that has not been checked is a claim, and this process does not accept claims.**

### Record it

**Add a line to `DEVELOPMENT-PROCESS.md` §15 saying what you changed and why.** If it was a gate
role or a check, say the same in `CLAUDE.md`.

This is thirty seconds and it is what makes the difference, six months later, between the next
person reading *we chose not to* and reading *this seems to be broken, I had better fix it.* A
process change with no record gets undone by somebody being helpful.

---

## The changes teams actually make

Every row is a real change with a switch behind it. The prompt column is a starting sentence to
paste into the shape above, not a magic string.

### Turning parts down

| You want | The switch | What it costs | Say |
|---|---|---|---|
| No issue tracker mirror | `tracker: ""` | `/slice-open` stops opening issues; `DoD-9`'s second clause and §8.1 go. **The queue is still the board** | *We are not using GitHub issues. Turn off the tracker mirror everywhere it is assumed.* |
| No requirement detail track | `requirements.dir: ""` | The quote check, and the input `/test-scenarios` and `/requirement-verify` read. `COVERAGE.md` loses a section | *Drop the requirement detail track for now — we are not staffed for it.* |
| No manual scenario track | `scenarios.dir: ""` | The scenarios a tester is handed. The by-hand demo becomes the only human check of a requirement | *We have no manual test team. Turn off the scenario track and tell me what that leaves uncovered.* |
| No change requests | `changes.dir: ""` | The record of who agreed to a change, and the index's *applied* and *built* columns. `Since` stops resolving | *Pre-launch, so no change requests yet. Switch it off and leave a note for when we launch.* |
| Size tiers back on | `size_budget: {"S": 150, "M": 400, "L": 0}` | Nothing — this adds a check. Work orders then declare `size` and `estimated`, and close records `code_lines` | *Bring back declared slice sizes, checked against what each slice measures.* |
| Fewer standing passes | Delete the skill directory and its row in `/maintenance` | That pass. Its backlog stops being reconciled and becomes a list | *We will not run security audits in-house. Remove the pass and say in §15 who does it instead.* |
| Less enforcement, for now | `enforce.default: []` or a per-rule path list | Nothing, until somebody changes code inside the perimeter without a slice | *Only enforce work orders under `src/billing/`. Annotations everywhere.* |
| The whole tool | Delete `scripts/` and the workflows | Everything generated. The documents remain and become hand-maintained | — |

### Tuning it to how you actually work

| You want | Where | Say |
|---|---|---|
| **Different velocity thresholds** | `velocity` in the config | *Run `velocity.py` over the last two months and tell me what thresholds would have flagged the slow weeks without crying wolf on the normal ones.* |
| **A different stack** | `tests.globs` and `tests.annotation`, plus the gate roles in §5 | *We are moving the suite from vitest to pytest. Update the ledger's test globs, the annotation pattern and the gate commands, then prove it by running check.* |
| **A different tracker** (Jira, Linear) | `tracker`, and the `gh` calls in `/slice-open` and `/slice-close` | *Swap GitHub issues for Linear. Keep the shape — one issue per claimed slice, body is the work order, summary as a comment — and change only the calls.* |
| **A new definition-of-done row** | §4's table — **and the third column** | *Add a DoD row: every slice touching the public API updates the OpenAPI document. Put it in the table with what would notice if it did not, and say honestly whether that is the tool or a human.* |
| **A new identifier family** | One row in `writ/spec/ID-REGISTRY.md` | *We need a family for performance budgets, `PERF-NNN`, declared in a new register. Add the registry row, create the register and tell me what the tool now expects.* |
| **A new gate check** | `.github/workflows/gate.yml`, §5 gate roles | *Add a bundle-size check to the gate as a new gate role, and record it in §5 with its threshold and why.* |
| **A different cadence** | §11, and the standing skill itself | *Move `/cleanup` from weekly to every phase gate.* |
| **Promotion from solo to team** | `mode: "team"`, `wip_limit`, then `owner:` and `touches:` on new work orders | *There are three of us now. Promote the process to team mode and tell me what changes for work orders already in flight.* |
| **A renamed tree or skill** | Phase 0 chose it; a `git mv` plus a substitution changes it | *Rename `writ/` to `spec/` everywhere, including the ledger config and `CLAUDE.md`.* |
| **A different agent harness** | `context_budget.files` in the config, and the skills themselves | *We are moving off Claude Code. Add `AGENTS.md` to the context budget, then tell me which of the fifteen skills is harness-specific and what the port actually costs.* |
| **A skill of your own** | A new directory under `.claude/skills/` | *Write a `/release-notes` skill that reads the slice summaries merged since the last tag. Follow the shape of the existing skills.* |

### Changing the prose, not the switches

**Most of `DEVELOPMENT-PROCESS.md` is argument rather than mechanism, and you are allowed to
disagree with it in writing.** If your team decided that step 3 is a fifteen-minute walkthrough
rather than a read, write that down in §3.2. The document's authority comes from your team having
agreed to it, not from where it came from.

The house style, if you want new text to sit beside the old: say the rule, then say what goes wrong
without it, and name the failure specifically rather than in the abstract.
[`../references/07-authoring-style.md`](../references/07-authoring-style.md) is the full account.

---

## The three things to think twice about

Not forbidden — nothing here is forbidden — but each is load bearing for something else, so
changing it is a rewrite rather than a setting.

### The declaration rule

**An identifier is declared if and only if it is the first cell of a table row, under an `| ID |`
header, inside its family's declared section.** Every tool, check and generated file in the process
reads that one rule.

It bends by adding rows to `writ/spec/ID-REGISTRY.md` — new families, new widths, new owners, all
Markdown and no code. It does not bend by being replaced with something more flexible: the rule is
mechanical precisely so that nothing has to interpret a document to know what it declares, and the
moment it needs interpreting, the index, the ledger, the coverage states and the quote check all
lose their footing at once.

### `/context-compact`

**`DoD-8` adds a line to `CLAUDE.md` every time a slice establishes a convention, and nothing else
ever takes one out.** Remove the remedy and you have a file that only grows, read at the start of
every session, paid for on every task forever.

If you do not want the pass, you need a different remedy — not no remedy.

### The by-hand demo

**It is not enforced by anything, which is exactly why it cannot be switched off: there is nothing
to switch.** It stops happening the day somebody stops doing it, and no gate will ever go red.

This is the row most likely to be quietly dropped, and it is the one that catches the defects the
suite cannot: the suite proves the system does what it was told, and the demo is where you find out
what you told it.

---

## And if you are not sure

**Ask the agent to argue the other side before it makes the change.**

```
Before you change anything: what is this rule there to prevent, and what happens
to us in three months if it is gone? Then make the change if it still makes sense.
```

Every part of this process was written against a specific failure, and the reference documents in
[`../references/`](../references/) name them one at a time. An agent that has read the relevant one
can usually tell you within a paragraph whether what chafes is the rule being wrong for you, or the
rule doing its job in a way that is uncomfortable on purpose. Both happen. The second one is
worth knowing before you switch it off.
