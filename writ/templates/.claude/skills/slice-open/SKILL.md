---
name: slice-open
description: Open a slice — ask which one to start (naming the next in the queue), draft its work order from the queue and the specification, create the branch and a draft pull request, and stop for the human to approve before any code is written. Use at step 2 of the slice loop, or when the user says to start a slice.
---

# Open a slice

Step 2 of the loop in `writ/process/DEVELOPMENT-PROCESS.md`. **You are drafting, not deciding.**
The work order is one of the things this process never delegates; your job is to remove the
friction, not the judgement.

Invoked as `/slice-open <ID>`, or with no argument to be asked which one.

## 1. Ask which slice

Read the generated queue block in `writ/process/SLICE-QUEUE.md` first, whatever the argument. The
**next in queue** is the highest-ranked slice whose status is `queued` and whose `depends_on` are
all `done`. **In team mode, also skip any whose `touches` collide with an active slice, and stop if
the WIP limit is already reached.**

With no argument: **ask which slice to start.** Do not pick one. Name the next in queue as the
default, say why it is next (its position, and that its dependencies are done), list the two or
three that follow it, and wait for the answer. Something like:

> **1. Which slice should I open?**
> a. **SL-042 — RLS policies** (recommended) — next in queue (#4, phase P02); SL-040 and SL-041,
>    which it depends on, are both done.
> b. SL-043 — tenant switcher — next after it; also unblocked, but it reads the policies SL-042
>    writes, so it would build on a guess.
> c. Another id — say which, and I will check its dependencies first.

With an id: read that work order if it exists, otherwise create it. **If the id is not the next in
queue, say so** — name the one that is, and whether the chosen slice's dependencies are all `done`.
An unfinished dependency is a stop, not a note: the slicer decides whether to run out of order, and
the run is written into `SLICE-QUEUE.md` §Out-of-order runs before the work order is drafted.

## 2. Read before you draft

- The area registers under `writ/spec/requirements/` — the rows this slice will claim, in full —
  and `writ/INDEX.md` for what already stands behind each. `writ/spec/BRD.md` §7 for the job in
  prose.
- Every foundation spec that governs the area.
- `writ/process/COVERAGE.md` — what those requirements already have behind them. A requirement
  already `●` is one to check rather than re-claim.
- **What the parallel tracks hold, where they hold anything.** One `ls` answers it —
  `ls writ/spec/requirements/<area>/ writ/qa/scenarios/<area>/` — and where a claimed requirement
  has a file, read it; where it does not, say so in one line and move on. Early in a project both
  trees are empty and this is that one line. None of it gates the slice: the tracks run beside the
  loop by design (`DEVELOPMENT-PROCESS.md` §11). It is still said, because a slice about to claim a
  requirement nobody has detailed is the moment `/requirement-detail` is cheapest.
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
  the plan, and what the two answers would be — then stop and ask, in the shape of `CLAUDE.md`
  §*Asking me to decide*: quote the requirement's words, one lettered option per answer with what
  it costs, and which you recommend and why. Do not resolve it inside the work
  order, do not soften the requirement's reading, and never take the interpretation that happens to
  make your plan work. The person who wrote the plan is the last one who should choose between it
  and a requirement that inconveniences it.
- **The accepted decisions over those areas** — the ADR table in `writ/INDEX.md`, one row per
  record with its decision and what it constrains. Open only the three or four that govern. Do
  not grep the decisions directory: an area grep matches body text across every record, and on a
  mature project that was hundreds of thousands of tokens read to find the few that mattered. A
  plan that would reverse an accepted decision needs a superseding record, not a different plan.
- **Where a `reviewed` detail file exists** under `writ/spec/requirements/`, read that
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

Copy `writ/process/templates/work-order.md` to `writ/process/work-orders/<milestone>/<phase>/<NNN>.md`
and fill it. The number is the next free one across the whole repository, zero-padded to three
digits, and the file is named for it; the milestone directory is the one the current milestone plan
was cut into, and the phase directory is the code the front matter declares. The check fails when
any of the three disagree, and refuses a suffix letter — a split is two fresh numbers.

Front matter first, and it is the **only** claim site:

- `satisfies` — only what this slice will *prove with a test*. When in doubt, `partial`.
- `depends_on` — what must be `done` first. The queue order is derived from this.
- `adr` — name a record only for a decision that **binds a later slice** and had a credible
  rejected alternative. A decision that shapes only this slice is a code comment and a row in the
  summary's Decisions table. **Write the ADR now**, before implementation; `ledger.py check` fails
  while the file is missing.
- `demo` — `script` or `ui`.

**Cut for cohesion, not for size.** Never split work that only holds together in one pass; do split
capabilities that are bundled only for convenience. Where `size_budget` in
`scripts/ledger.config.json` names tiers, also fill `size` and `estimated` as the template's
comment describes; with it `{}` — the default — leave them out.

Then the body. Two sections carry the weight:

**Acceptance criteria.** Numbered, independently checkable, and precise enough that each becomes a
test name — so each starts with the `[ID]` it proves, one the front matter claims. `ledger.py check`
fails an open slice whose criterion names none, or names one the front matter does not. Write them as the behaviours a test would assert, including the adversarial ones — what
happens on the second submit, what another tenant sees, what an empty list returns. *If a criterion
cannot become a test name, it is not written precisely enough yet; rewrite it rather than
softening it.*

**The demo.** A script with no identifier for the reader to substitute — capture what the slice
creates with `--json` and `jq`. Or, for a user interface, numbered single-action steps ending in
`**Expected:**` and something specific enough to be wrong.

## 4. Open the issue, claim on the branch, open the draft pull request

**Check the repository's shape first**, with `git remote` and `git branch --list dev`. Bootstrap
leaves the tree committed on `dev`; it cannot create a remote. If there is none, do the branch and
the commit, skip the issue, the push and the pull request, and say plainly that they are waiting on
a remote — do not invent one and do not fall back to committing on `dev`.

**The issue comes first**, where `tracker` in `scripts/ledger.config.json` names one. Its number
goes in the front matter of the commit that claims the slice, and `ledger.py check` fails a claimed
slice that names none. **The issue body is the work order file** — the same bytes, so a reader in
the tracker sees the acceptance criteria and the demo rather than a pointer to them. It is a
mirror, not a second copy to maintain: `/slice-close` re-syncs it from the file before the merge,
and the file is what is right when the two differ. The label is the phase, which slice zero created
(and the size, where size tiers are on).

```bash
gh issue create --title "<ID> — <title>" --label "phase:<phase>" \
  --body-file writ/process/work-orders/<milestone>/<phase>/<NNN>.md
# → set issue: <number> in the work order's front matter; a number, no `#`

git checkout dev && git pull --ff-only          # `git pull` only where a remote exists
git checkout -b slice/<NNN>-<slug>
# set status: in-progress — and in team mode owner: — in the same front matter, then:
python3 scripts/ledger.py
git add writ/process/work-orders/<milestone>/<phase>/<NNN>.md writ/process/SLICE-QUEUE.md writ/process/COVERAGE.md writ/INDEX.md
git commit -m "docs(process): claim <ID>"
git push -u origin slice/<NNN>-<slug>
gh pr create --draft --base dev --title "<ID> — <title>" \
  --body-file writ/process/work-orders/<milestone>/<phase>/<NNN>.md
```

With no tracker configured, skip the `gh issue` line and leave `issue:` empty; everything else is
the same.

The work order **is** the pull request description at open, so the diff arrives against a stated
intent instead of having to explain itself. At close the description becomes the slice summary —
what was built, against what was intended.

In team mode, `owner:` and `status: in-progress` land in the same commit as `issue:` — two people
cannot claim one slice, because the second commit conflicts.

**Run `python3 scripts/ledger.py check` before pushing the claim.** It refuses a claimed slice with
no issue, and in team mode a fourth active slice or two active slices sharing a `touches:` entry —
finding that out here costs a minute rather than a branch.

## 5. Stop

**Open with the brief: what this slice will do, in two or three plain sentences** — what somebody
will be able to do afterwards that they cannot today, and roughly how. No identifiers, no file
paths, nothing the reader has to look up; the rest of the report is where those go. The brief is
what the approver reads first, so it has to be enough to say *yes, that is the slice I meant*.

> **SL-042 — RLS policies.** After this slice, one customer's data can no longer be read by another
> customer, even through a query that forgets to filter. The database enforces it, with a policy
> generated for every table that holds customer data.

Then report: the slice, what it claims, the issue and pull request numbers, the
acceptance criteria as a list, **the conflict check from step 2a — the requirements read against the plan, and every conflict found or
the explicit absence of any** — one line per claimed requirement saying whether its detail file and
its scenarios exist and in what state, and any open question you could not resolve from the
specification.

Then **stop and wait.** The next step is a human reading and approving the work order, and after
that a file-level plan that a human reads before any code exists. Do not begin implementing.
