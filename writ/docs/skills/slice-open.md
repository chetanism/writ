# `/slice-open`

**Step 2 of the loop. Asks which slice to start, drafts its work order from the queue and the
specification, opens the branch and a draft pull request — and stops for you to approve before a
line of code is written.**

| | |
|---|---|
| **Run it** | At the start of every slice. `/slice-open SL-014`, or with no argument to be asked |
| **Produces** | `writ/process/work-orders/<milestone>/<phase>/NNN.md`, a tracker issue, a branch, a draft PR |
| **Refuses to** | Decide. *You are drafting, not deciding* — the work order is one of the things this process never delegates |

## What it does

1. **Asks which slice**, naming the next one in the generated queue so the default is the right one.
2. **Reads before drafting** — the queue entry, the requirements it claims, the invariants governing
   the areas it touches, the foundation specs, and any existing decisions.
3. **Reads the plan against those requirements for conflict**, and names every one it finds. Under
   `out_of_order: fail` it stops on a claimed requirement with no detail file and offers a draft
   first; otherwise it says so, and recommends backfilling one that is already built. A
   *Reconciliation* row decided `fix` that names this slice becomes an acceptance criterion.
4. **Drafts the work order**: requirements advanced, contract changes, numbered acceptance
   criteria that each name the requirement they prove, the demo, and what is explicitly out of
   scope. It reads the decisions that govern the area from the ADR table in `writ/INDEX.md`, not by
   searching every record.
5. **Opens the issue, claims on the branch, opens the draft pull request** — recording
   `detail_read_on`, the day it read the detail files, so a later revision of one is caught.
6. **Stops**, opening its report with a two- or three-sentence brief of what the slice will do, in
   plain words, so the approver can tell at a glance it is the slice they meant.

## The two parts that carry the weight

**The acceptance criteria become the test names.** This is the only mechanism keeping a work order
honest rather than decorative. If a criterion cannot become a test name, it is not written
precisely enough yet — and finding that out here costs a sentence.

**`DoD-12`: the plan is read against the requirements for *conflict*, not only for coverage.** The
question is not which requirements this slice advances but whether the plan would make one
**false**. The requirement a plan breaks is almost never one the plan claims — it is an invariant,
and an invariant is a shape rather than a capability, so it belongs to no requirement area a slicer
would think to search.

The shape, from a real project: a decision recorded an amount of money in one country's minor units
with no currency stored anywhere — against a P0 invariant saying country-specific facts are
configuration, never assumptions baked into the product. Every requirement the slice claimed had
been read carefully; none of them pointed at it.

**A conflict is the slicer's to resolve**: the skill names the requirement, names the part of the
plan, names the two answers, and stops. It never takes the reading that makes the plan work — and
it says *no conflicts* out loud when there are none, because a silent check reads exactly like one
that never happened.

## Why it stops

The whole point of step 2 is that it is the cheapest place in the process to change your mind.
Nobody is attached to anything, nothing has to be rewritten, and the disagreement is about what the
software should do rather than about somebody's code. **An hour of argument on a work order is
worth a day of argument on a diff.**

## See also

[`/slice-close`](slice-close.md) — step 7. [`../references/04-slicing.md`](../../references/04-slicing.md)
— slicing criteria, cutting for cohesion, dependency ordering and the demo rule.
