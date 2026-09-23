# How to use it

> **Skim rule for this page.** Every section opens with one bold paragraph that is the whole answer.
> The prose under it is why, and what goes wrong without it. If you are in a hurry, read the bold
> lines only — they are written to make sense read on their own, end to end, in about four minutes.

---

## 1. Setting it up

### Choose one of three skills

**`/writ:solo` for a new project one person is building, `/writ:team` for a new project several
people are building, `/writ:adopt` for a codebase that already exists.** Pick once; they are not
variants of each other.

The split is not cosmetic. `team` designs roles, handoffs, WIP limits and CODEOWNERS into the
process from the start, and retrofitting a pipeline onto a process that assumed one pair of hands
is harder than choosing correctly on day one. `adopt` solves a different problem entirely: the code
is already the most reliable document in the room, so the job is not writing the codebase down but
writing down [what the code cannot say about itself](../references/12-survey.md).

All three are user-invoked only. Claude never starts one on its own.

### Arrive with two paragraphs, or with nothing

**A finished specification is welcome and not required. Two paragraphs about what you are building
is a valid input — the interview writes the rest with you.**

Expect two or three rounds of questions if you arrive with a written BRD, and six to ten if you
arrive with an idea. The questions are batched and numbered, and you can answer *I do not know* to
any of them: an unanswered question becomes a row in `writ/spec/questions.md` with an owner, which
is a far better outcome than a guess that everything downstream then gets built against.

The one thing to resist is inventing numbers. An availability target nobody gave you is worse than
none, because the architecture, the test plan and the on-call rota all get sized against it and
nobody remembers it was made up.

### What the interview actually does

**Ten phases, roughly an hour, ending with a committed tree on a branch.** You answer questions; it
writes documents; nothing is silently decided.

| Phase | What it settles |
|---|---|
| 0 | Where things go, what the tree is called, whether any skill name collides with one you already have |
| 1 | The BRD — obtained, or built from what you can tell it |
| 2 | Scope: what this is, what it is explicitly not, who it is for |
| 3 | Security, conditioned on your domain — it asks the questions your profile earns and skips the rest |
| 4 | Reliability: availability, recovery, idempotency, backpressure, scale, what you can observe |
| 5 | The stack and the gate roles — **and it runs each command rather than believing your README** |
| 6 | The specification set is written: registers, invariants, foundation specs, the registry |
| 7 | Slicing: the queue, dependency-ordered, sized, with slice zero shipping the tooling first |
| 8 | The process is emitted — config, workflows, `CLAUDE.md`, the loop skills |
| 9 | The standing passes, tuned to your cadence |
| 10 | The requirement detail track, if you want it |

If the session runs out before it finishes, it does not start again from question one:
`.writ-interview.md` is appended after every phase, found at phase 0 next time, and deleted at the
commit.

### What you get at the end

**A `writ/` tree, a CI gate, a traceability tool, fourteen skills tuned to your answers, and a
commit on `dev` — or, for an adoption, on `docs/adopt-writ` with every rule switched off.**

The full listing is in [the reference](../README.md#what-you-get). The parts to know on day one:

- `writ/spec/` — what the product is. One kind of thing per file: a narrative BRD that declares
  nothing, then a register per kind of declaration with `Since` and `Status` columns.
- `writ/process/` — how work is done. `DEVELOPMENT-PROCESS.md` is the one document to read; the
  queue and the coverage ledger under it are generated and never hand-edited.
- `CLAUDE.md` — the agent's map of the repository. It is read at the start of every session, so it
  has a budget and a pass that enforces it.
- `scripts/ledger.py` — stdlib-only Python, single file. It generates, it checks, and it reports.

Everything produced is your project's own. The kit reads its templates from the plugin's install
directory, so there is nothing to delete afterwards and nothing of the kit to edit by mistake.

### Before the first slice

**Add a git remote and branch protection if there is not one yet, and run the gate once.**

`/slice-open` works without a remote, but the draft pull request and the CI gate are two of the
three things that make the loop cheap, and they sit idle until there is somewhere to push. Run
`python3 scripts/ledger.py check` once by hand so that you have seen it pass before you have a
reason to care whether it passes.

---

## 2. The loop

**Seven steps per slice. Two of them are a skill, three are a human's, and the middle is an agent's
to do and yours to read.** This is the whole day-to-day of the process.

| # | Step | Who | Output |
|---|---|---|---|
| 1 | Pick | You | One slice from the queue |
| 2 | Work order | You + `/slice-open` | One page, the branch, the draft PR |
| 3 | Plan | Agent proposes, **you read** | A file-level implementation plan |
| 4 | Implement | Agent | Code and tests in one pass |
| 5 | Verify | Automated | The gate |
| 6 | Play | **You, by hand** | The demo from step 2, executed |
| 7 | Close | You + `/slice-close` | Summary, ledger, commit, merge |

### Step 1 — Pick

**Take the next slice in the queue unless you have a reason not to, and the queue is generated so
it is never out of date.**

The order comes from `depends_on` in each work order's front matter, topologically sorted. Nobody
maintains the table; there is exactly one place a dependency is claimed and the table is derived
from it. That matters more than it sounds: in the process this was extracted from, the queue was
hand-maintained, and its sizes and phase labels drifted until nobody trusted the order.

### Step 2 — Write the work order (`/slice-open`)

**Twenty minutes, one page, before any code. It fixes which requirements are advanced, what changes
in the published contract, the size, the numbered acceptance criteria, the demo, and what is out of
scope.**

This is the step that carries the process. Three things happen here that happen nowhere else:

**The acceptance criteria become the test names at step 4.** That is the only mechanism keeping a
work order honest rather than decorative. If a criterion cannot become a test name, it is not
written precisely enough yet — and finding that out now costs a sentence, where finding it out at
review costs the slice.

**The plan is read against the requirements for conflict, not just for coverage** (`DoD-12`). The
question is not *which requirements does this advance* — the front matter answers that — but
*would this plan make one of them false?* The requirement a plan breaks is almost never one the
plan claims: it is an invariant, and an invariant is a shape rather than a capability, so it belongs
to no requirement area anybody would think to search. `/slice-open` reports the result either way,
because a silent check reads exactly like one that never happened.

**Any decision with a credible rejected alternative gets an ADR before implementation begins**, and
the check enforces the ordering. A decision recorded afterwards is a justification. The record is
only worth keeping if it precedes the code it governs.

*What it buys you:* every argument that would otherwise happen in a pull request review happens on
one page, before anybody has written code they are now attached to.

### Step 3 — Read the plan

**The cheapest comprehension the process offers, and the one step with no artefact at all.**

The agent proposes a file-level plan; you read it. A plan you cannot follow is a signal — either
the slice is too large or the design is wrong — and saying so costs a conversation. Saying it at
step 5 costs the slice.

This is the step people skip, and skipping it is how a project ends up with three months of code
nobody has ever read. It takes four minutes.

### Step 4 — Implement

**The agent writes code and tests in one pass, with the acceptance criteria as the test names.**

This is the part everybody already knows how to do, and the only note worth making is that the
tests are not a separate task afterwards. A criterion, its test and its annotation `[FR-ACC-01]`
arrive together or the ledger will not count them.

### Step 5 — Verify

**The gate runs. It is the boring step and it should stay boring.**

Lint, types, tests, the invariant suite, contract validation, and `ledger.py check` — which is
where the process itself is verified: stale generated files, undeclared identifiers, a work order
naming an ADR that does not exist, an unresolved placeholder, a slice marked done with no summary.

### Step 6 — Play the demo, by hand

**Non-negotiable, never delegated, and not enforced by anything — which is exactly why it is
written down this firmly.**

Automated tests prove the system does what you told it to do. Step 6 is where you find out **what
you told it.** The gap between those two is where most shipped defects live, and no amount of
coverage closes it.

The tool checks that a demo *section* exists and carries no unresolved placeholder. It cannot check
that anybody ran it, and it never will. That is the design, not a gap: see
[§4.1 of the process document](../templates/writ/process/DEVELOPMENT-PROCESS.md) — *the checkable
things are checked so that attention is left over for the things that cannot be.*

### Step 7 — Close (`/slice-close`)

**It drafts the summary from the actual diff, regenerates the ledger and the queue, walks the
definition of done item by item, and hands you the merge command.**

The definition of done is twelve rows. Three belong to the gate, three are half the tool's, and the
rest are nobody's but yours — so `/slice-close` walks them **one at a time and says `[you]` out
loud** on the rows that are yours, rather than reporting the table as met. A definition of done
reported in aggregate is one nobody is applying, and the rows most likely to be waved through are
precisely the ones no build will ever fail on.

*What it buys you:* the summary in the pull request is written from the diff rather than from
memory, the coverage ledger is regenerated rather than asserted, and the thing you merge is the
thing you described.

---

## 3. Beside the loop

**Three skills run one phase *ahead* of the queue, block no merge, and consume no WIP.** They exist
because a requirement in a BRD is one line — enough to build against, nowhere near enough to test
against by hand.

| | |
|---|---|
| [`/requirement-detail FR-ACC-01`](skills/requirement-detail.md) | Works out with you what one requirement actually means, then writes its detail file. **A conversation, not a delivery** |
| [`/test-scenarios FR-ACC-01`](skills/test-scenarios.md) | Turns that file into scenarios a tester runs through the product's own screens |
| [`/requirement-verify FR-ACC-01`](skills/requirement-verify.md) | At a phase gate: is the behaviour that file describes actually there? Report-only, four verdicts |

The order in which one requirement's documents arrive is fixed; the moment each arrives is not.
Slices and requirements are many-to-many, so a slice never waits on every requirement it touches
being detailed, and a detail file never waits on a slice. What keeps the order honest is that each
document is the input the next one reads, and `/slice-open` says out loud which of them exist yet.

The load-bearing check in this track: **a detail file that quotes its requirement differently from
the register fails the build, character for character.** That is what turns an amendment to a
requirement into a red gate rather than a slow, silent divergence.

---

## 4. Outside the loop

**Four standing passes and a manual-test harness. None is anybody's slice, none closes an issue,
and none consumes WIP.**

They exist because a gate cannot detect the three ways a project rots *between* slices: a file
nobody has touched since the finding in it was introduced, a suite that is green while nobody has
looked at the product in three weeks, and the agent map growing by a line a slice until the
document every session starts from costs more than it earns.

| | Cadence |
|---|---|
| [`/cleanup`](skills/cleanup.md) | As often as you agreed — behaviour-preserving, scoped to what changed since the last pass |
| [`/product-docs`](skills/product-docs.md) | At a phase gate — the product as it is today, never a changelog |
| [`/security-audit`](skills/security-audit.md) | On a cadence, and after any dependency change |
| [`/context-compact`](skills/context-compact.md) | **On a trigger, not a clock** — when `ledger.py check` warns the agent map is over budget |
| [`/maintenance`](skills/maintenance.md) | All four in order, each merged before the next starts |
| [`/manual-test`](skills/manual-test.md) | When the suite is green and nobody has played with the product — a state no gate can detect |
| [`/change-request`](skills/change-request.md) | After launch, the only way a register changes |
| [`/process-change`](skills/process-change.md) | When a rule does not fit — the only way **this process** changes |

`/context-compact` is the one with a trigger rather than a cadence, and it is the only thing in the
process that ever takes a line *out* of `CLAUDE.md`. `DoD-8` puts one in every time a slice
establishes a convention; without the remedy you have a file that only grows and is read at the
start of every session. **A budget with no remedy is a rule people learn to route around.**

---

## 5. Cadence

**Per slice: the loop. Per phase: the ledger, the queue ahead, the scenarios that turned ready, and
`ledger.py stats`. Per milestone: measure against the exit criterion, never against the number of
merged slices.**

```bash
python3 scripts/ledger.py          # regenerate COVERAGE.md, INDEX.md and the queue
python3 scripts/ledger.py check    # verify all of it, plus every process check — CI runs this
python3 scripts/ledger.py stats    # is the process still being followed? reports, never fails
```

The third one is the one people forget, and it answers a question nothing else here asks. `check`
asks whether the documents agree with each other, at one moment. `stats` asks whether the process
is still being followed — which is what goes wrong slowly and invisibly: a month where throughput
halved and nobody said so, the audit nobody has run since the spring, the detail track that stopped at
requirement nine, the backlog that only grows.

**It never fails.** An instrument that can fail a build is a gate wearing a different name, and
these are numbers to look at together rather than thresholds to route around.

---

## Getting the most out of it

The difference between a team running this well and one running it as ceremony is about six habits.

### Let the agent read the tree, not your open tabs

**Point the agent at `writ/` before every non-trivial task and it will plan against the
specification instead of against whichever three files you happened to have open.**

This is the single largest return in the kit and it costs nothing. `CLAUDE.md` already tells a
session where things are; the habit worth building is naming the specific documents — *read
`writ/spec/invariants.md` and the detail file for FR-ACC-01 before you plan this* — because a
plan built against the invariants rarely needs the second attempt that a plan built against the
code does.

### Spend your judgement at step 2, not at review

**An hour of argument on a work order is worth a day of argument on a diff.**

The work order is the cheapest place in the whole process to change your mind. Nobody is attached
to anything yet, nothing has to be rewritten, and the disagreement is about what the software
should do rather than about somebody's code. Teams that adopt this successfully get louder at step
2 and quieter at step 7.

### Keep slices small enough to demo in two minutes

**If the demo takes longer than two minutes to play, the slice was too big — and velocity will
tell you afterwards, but the demo tells you before.**

Nobody estimates or records a slice's size. `python3 scripts/velocity.py` reads it from git: code
and Markdown added per merge and per week, and a flag when a week falls well below the ones before
it or when the writing starts to outweigh the code. `/maintenance` runs it with `--check`. The
thresholds are in the `velocity` block of `scripts/ledger.config.json` — your numbers, to adjust.

### Write the ADR when you notice the alternative, not when the slice closes

**The test is not *was this hard* — it is *was there a credible thing we did not do?***

Most ADRs never get written because the decision did not feel like one at the time. The moment to
catch it is the moment you say "we could also…" out loud. Three sentences and a rejected
alternative is a complete ADR; nobody needs the essay.

### Say `[you]` out loud

**When `/slice-close` walks the definition of done, answer the human rows honestly, including when
the answer is no.**

Half of the definition of done cannot be checked by anything. A slice closed with `DoD-5` waved
through is worse than one closed with `DoD-5` marked *not done — demo not played, will play
tomorrow*, because the first one is invisible and the second one is a fact somebody can act on.

### Run `stats` at every phase gate and read it as a team

**Four numbers in that report are about the process rather than the product, and they are the early
warning for everything that kills an adoption.** A detail track that stopped at requirement nine, a
backlog that only grows, an audit three months old, a `CLAUDE.md` at 90% of budget — each of those
is cheap to fix at the phase gate it first appears in and expensive to fix two milestones later.

---

## When something does not fit

**Change it.** Every part has a switch, each switch is listed with what it costs, and
`/process-change` is what lands a change in every file it touches rather than only the one you
happened to think of.

That is a page of its own: **[Changing the process](changing-the-process.md)**, and the skill has
one too: **[`/process-change`](skills/process-change.md)**.
