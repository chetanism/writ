# Perturbation operators

**Draw from this list; do not invent.** A model asked to "be creative" revisits the same three
cases every run, which is the opposite of what a random walk is for. Each step of a walk draws an
operator and a target, records both in the transcript beside the counter that produced them, and
states what should be true **anyway** before running anything.

Every operator has the same shape:

> **What it perturbs** — the thing changed relative to the happy path.
> **What must hold anyway** — the invariant the perturbation must not be able to break.
> **What a defect looks like** — so the run can tell a finding from an expected refusal.
> **Applies when** — the condition under which this operator is worth drawing at all.

A refusal is not a finding. **A refusal with the wrong code, the wrong status, a leaked detail, or
a side effect left behind is.**

> **Tuned at bootstrap.** An operator whose *Applies when* the project does not satisfy is deleted
> outright, not left in with a note — a list that contains inapplicable entries is a list that gets
> redrawn past, and the redraw budget is what pays for depth. Each surviving operator's *holds
> anyway* clause is rewritten to name **this project's** mechanism, and the identifier it comes
> from. Delete this blockquote once that is done.

---

### 1 · Duplicate
**Perturbs** the assumption that a request arrives once. Send the identical request twice — same
idempotency key if there is one, then again with a fresh one.
**Holds anyway** the work happens once per key; a fresh key is a second, genuine request.
**Defect** two records for one key; a replay whose status or body differs from the original; a
replay that re-runs the side effect.
**Applies when** always. A user double-clicks, a client retries, a network redelivers.

### 2 · Concurrency
**Perturbs** the assumption that steps are serial. Fire the same request twice at once (`&` …
`wait`), or two different requests that claim one record.
**Holds anyway** one winner, decided **inside the write's own predicate** rather than by a
read-then-write in application code.
**Defect** two winners; a loser that gets a server error instead of its documented conflict answer.
**Applies when** anything can be claimed, leased, or transitioned by more than one actor.

### 3 · Reorder
**Perturbs** arrival order. Do two steps in the other order — the later state before the earlier
one, a batch backwards, the credential after the thing it authorizes.
**Holds anyway** the final state does not depend on arrival order, because it is decided by a rule
over the set of what arrived rather than by whichever wrote last.
**Defect** a final state that depends on order outside a documented exception; an error on the
out-of-order arm that the in-order arm does not produce.
**Applies when** state arrives from more than one source, or asynchronously.

### 4 · Delay
**Perturbs** timing. Wait past a lease, a session window, a retry floor, a recovery window, a
rate-limit refill, a retention boundary.
**Holds anyway** the boundary is evaluated **where it is written down** — inside the query, inside
the policy — not against a clock read into application memory first.
**Defect** a record restorable on one side of a boundary and not the other for reasons unrelated to
the boundary; a lease that never expires; a published retry hint that is wrong.
**Applies when** anything expires, leases, throttles, or is retained for a period.

### 5 · Skip
**Perturbs** completeness. Omit a step the happy path always does — a required header, a
prerequisite record, a setup call.
**Holds anyway** the refusal names **the missing thing specifically**, and writes nothing.
**Defect** a server error; a partially-written state; a refusal that names something else.
**Applies when** always.

### 6 · Substitute
**Perturbs** identity. Swap an identifier for one of: another actor's, a well-formed one that never
existed, a soft-deleted one, one with the wrong prefix or type, a cursor from another route.
**Holds anyway** a malformed identifier is refused **before** any query runs; the answers that the
design says are indistinguishable really are.
**Defect** the four answers being distinguishable where the design says they are one; any of them
reaching a record.
**Applies when** always. This is where authorization leaks show up as timing or wording.

### 7 · Boundary
**Perturbs** size and count. A limit at 0, 1, the maximum, the maximum + 1. A page whose result set
is **exactly** the limit. A body at the cap and one byte over. An empty string, a single space, the
longest permitted identifier.
**Holds anyway** the documented limit is the enforced limit.
**Defect** an off-by-one visible only at the edge; a "more results" flag wrong on an exact multiple;
a limit enforced at a different number than published.
**Applies when** anything is paginated, capped, or measured.

### 8 · Malform
**Perturbs** shape. An extra field the contract does not name; a wrong content type; a missing
required header; a truncated body; a signature over different bytes.
**Holds anyway** an unknown field is a **rejection**, never silently dropped — silently dropping it
is what a successful escalation attempt looks like from the outside.
**Defect** a success with the field ignored; a server error; an error message echoing something
that came out of an exception.
**Applies when** anything crosses a trust boundary as structured data.

### 9 · Interrupt
**Perturbs** liveness. Stop a process mid-flight — between accept and act, between an action and
its confirmation, mid-retry — then start it again.
**Holds anyway** at-least-once: the work is picked up again, the consumer is idempotent, and
nothing external is done twice, because the record leaves its pending state only after the external
side answered.
**Defect** work stuck forever; a duplicate external call; a job marked complete with the work
undone.
**Applies when** there is a background worker, a queue, or any multi-step operation that can be
interrupted between steps.

### 10 · Mutate underneath
**Perturbs** assumptions held across steps. Change state a request in flight depends on — revoke
the credential, soft-delete the owner, delete the target, close the window, erase the subject —
**between** two steps that assume it.
**Holds anyway** the next request re-reads under its own policy and refuses cleanly; work whose
subject has gone is skipped rather than performed.
**Defect** a stale read serving the old state; a server error; an action taken on erased content.
**Applies when** authorization or lifecycle state is mutable while work is in flight.

### 11 · Repeat until the limit
**Perturbs** the bound. Drive a bounded thing to its bound — the rate limiter, the retry budget,
the attempt cap, a page past the last cursor.
**Holds anyway** the bound is where it is documented, the transition at the bound is the documented
one, and crossing it is not a server error.
**Defect** an unbounded loop; a bound differing from the published number; an exhausted retry that
throws instead of recording a verdict.
**Applies when** anything is bounded, budgeted or throttled.

### 12 · Clock
**Perturbs** time as data. A timestamp well in the past or the future; two events with the same
timestamp; a timestamp that disagrees with arrival order.
**Holds anyway** a supplied timestamp is stored as supplied and never quietly replaced with the
current time; ordering decisions use the ordering rule, not the clock.
**Defect** an arrival time written into a column meaning something else; a state decision that
depends on a caller-supplied timestamp.
**Applies when** timestamps arrive from outside, or ordering is derived from time.

### 13 · Cross-boundary
**Perturbs** isolation. Do everything above with a **second** tenant's, account's or user's
identifiers, in both directions, at every privilege level the system has.
**Holds anyway** every isolation invariant in the specification.
**Defect** any observation of the other side's data, shape, or existence.
**Applies when** the system has a tenancy, account or ownership boundary. **Delete this operator
entirely if it does not** — and if it does, this is the operator that must never produce a finding,
and the one worth spending steps on for exactly that reason.

### 14 · Read the evidence
**Perturbs** nothing — it is the step that follows several of the others. After any of the above,
read what the system *recorded*: the audit trail, the outbox or queue, the event log, the server
logs.
**Holds anyway** the record agrees with what happened, and contains no secret, no credential, no
unredacted personal data.
**Defect** a missing audit row where access widened; a log line carrying a token; evidence that
contradicts the observed outcome.
**Applies when** the system records anything at all. A correct-looking outcome with a missing audit
row is a finding the response body cannot show you.

---

## Drawing

```bash
. .claude/skills/manual-test/env.sh
# one operator for step 7
grep -E '^### ' .claude/skills/manual-test/reference/operators.md \
  | sed 's/^### //' \
  | python3 .claude/skills/manual-test/draw.py "$MT_SEED" 7 --pick
```

Increment the counter for **every** draw and record it. Two draws sharing a counter are the same
draw, which is how a replay silently stops being one.

## Weighting

Not every operator suits every target. Draw an operator, and if it cannot be applied to the current
target, record that — `step 12: drew 'clock', not applicable to the settings route, redrew at
counter 13` — and draw again with the next counter. **Never silently substitute**: the record of
what was skipped is how the next run knows where the walk has thin cover.
