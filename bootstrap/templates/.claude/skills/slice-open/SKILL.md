---
name: slice-open
description: Open a slice — ask which one to start (naming the next in the queue), draft its work order from the queue and the specification, create the branch and a draft pull request, and stop for the human to approve before any code is written. Use at step 2 of the slice loop, or when the user says to start a slice.
---

# Open a slice

Step 2 of the loop in `docs/process/DEVELOPMENT-PROCESS.md`. **You are drafting, not deciding.**
The work order is one of the things this process never delegates; your job is to remove the
friction, not the judgement.

Invoked as `/slice-open <ID>`, or with no argument to be asked which one.

## 1. Ask which slice

Read the generated queue block in `docs/process/SLICE-QUEUE.md` first, whatever the argument. The
**next in queue** is the highest-ranked slice whose status is `queued` and whose `depends_on` are
all `done`. **In team mode, also skip any whose `touches` collide with an active slice, and stop if
the WIP limit is already reached.**

With no argument: **ask which slice to start.** Do not pick one. Name the next in queue as the
default, say why it is next (its position, and that its dependencies are done), list the two or
three that follow it, and wait for the answer. Something like:

> Next in queue is **SL-D3 — RLS policies** (#4; depends on SL-D1, SL-D2, both done). After it:
> SL-D4, SL-D5. Which slice should I open? Say *next* to take SL-D3, or give an id.

With an id: read that work order if it exists, otherwise create it. **If the id is not the next in
queue, say so** — name the one that is, and whether the chosen slice's dependencies are all `done`.
An unfinished dependency is a stop, not a note: the slicer decides whether to run out of order, and
the run is written into `SLICE-QUEUE.md` §Out-of-order runs before the work order is drafted.

## 2. Read before you draft

- `docs/spec/BRD.md` — the requirements this slice will claim, in full.
- Every foundation spec that governs the area.
- `docs/process/COVERAGE.md` — what those requirements already have behind them. A requirement
  already `●` is one to check rather than re-claim.
- The last two slice summaries — the *Surprises* sections are where the traps are.
- `CLAUDE.md` — the conventions.

## 2a. Read the plan against those requirements, and name every conflict

**Reading the requirements is not the same as reading the plan against them**, and the second is
the step that gets skipped. Do it before the work order is written, not at the plan read.

- **List what the slice touches** — its `satisfies` and `partial`, **plus every `INV-*` invariant
  governing the areas this slice changes** (`touches:` in team mode, the files and surfaces you are
  about to name in solo). An invariant is a shape rather than a capability, so it sits in no
  requirement area you would think to search, and it may well be `○` in the ledger with no slice
  claiming it. That is not evidence it does not apply.
- **Ask of each one: would this plan make it false?** Not *does the plan mention it*. A plan that
  never mentions a constraint is the normal way one gets broken.
- **A conflict is the slicer's to resolve, not the drafter's.** Name the requirement, the part of
  the plan, and what the two answers would be — then stop and ask. Do not resolve it inside the work
  order, do not soften the requirement's reading, and never take the interpretation that happens to
  make your plan work. The person who wrote the plan is the last one who should choose between it
  and a requirement that inconveniences it.
- **Where a `reviewed` detail file exists** under `docs/process/requirements/`, read that
  requirement's stories and its *Observable behaviour* too. They are the only place the requirement
  is written as something that can be **wrong**, and a plan that cannot produce those situations
  has found its conflict early. A `draft` file is one agent's reading — treat it as a prompt for a question, not
  as the requirement.
- **Say *no conflicts found* out loud.** A silent check reads exactly like one that never happened.

This is `DoD-12`. The failure it exists to catch is a slice whose own requirements were all read
carefully, none of which pointed at the invariant the plan quietly made false — an amount of money
stored in one country's minor units, say, against an invariant that says country-specific facts are
configuration. Every requirement the slice claimed had been read. None of them named it.

## 3. Draft the work order

Copy `docs/process/templates/work-order.md` to `docs/process/work-orders/<N>.md` and fill it.

Front matter first, and it is the **only** claim site:

- `satisfies` — only what this slice will *prove with a test*. When in doubt, `partial`.
- `depends_on` — what must be `done` first. The queue order is derived from this.
- `adr` — name a record for every decision with a credible rejected alternative. **Write the ADR
  now**, before implementation; `ledger.py check` fails while the file is missing.
- `size` — your estimate, against the tiers in `DEVELOPMENT-PROCESS.md` §2.1. **If it looks like it
  exceeds the top tier, stop and propose a split** rather than writing a justification.
- `demo` — `script` or `ui`.

Then the body. Two sections carry the weight:

**Acceptance criteria.** Numbered, independently checkable, and precise enough that each becomes a
test name. Write them as the behaviours a test would assert, including the adversarial ones — what
happens on the second submit, what another tenant sees, what an empty list returns. *If a criterion
cannot become a test name, it is not written precisely enough yet; rewrite it rather than
softening it.*

**The demo.** A script with no identifier for the reader to substitute — capture what the slice
creates with `--json` and `jq`. Or, for a user interface, numbered single-action steps ending in
`**Expected:**` and something specific enough to be wrong.

## 4. Branch and draft pull request

```bash
git checkout dev && git pull --ff-only          # `git pull` only where a remote exists
git checkout -b slice/<PHASE><N>-<slug>
git add docs/process/work-orders/<N>.md
git commit -m "docs(process): work order for <ID>"
git push -u origin slice/<PHASE><N>-<slug>
gh pr create --draft --base dev --title "<ID> — <title>" --body-file docs/process/work-orders/<N>.md
```

**Check the repository's shape first**, with `git remote` and `git branch --list dev`. Bootstrap
leaves the tree committed on `dev`; it cannot create a remote. If there is none, do the branch and
the commit, skip the push and the pull request, and say plainly that the draft PR is waiting on a
remote — do not invent one and do not fall back to committing on `dev`.

The work order **is** the pull request description, so the diff arrives against a stated intent
instead of having to explain itself.

In team mode, set `owner:` and `status: in-progress` in the same commit — two people cannot claim
one slice, because the second commit conflicts.

## 5. Stop

Report: the slice, what it claims, the size estimate, the acceptance criteria as a list, **the
conflict check from step 2a — the requirements read against the plan, and every conflict found or
the explicit absence of any** — and any open question you could not resolve from the specification.

Then **stop and wait.** The next step is a human reading and approving the work order, and after
that a file-level plan that a human reads before any code exists. Do not begin implementing.
