# Robustness, reliability, scalability

Ground every question in the domain **and** the stack. Ask about consumer lag if there is a queue,
connection pooling if there is a database, cold starts if it is serverless. Generic questions get
generic answers, and a generic answer is not a requirement.

**Refuse to invent a number.** An SLO you made up will be sized against, alerted on, and defended
for years. If the user does not have one, write an open question with a decider and a date.

## 1. Availability, and what it costs

- What is the target — and is it a **promise to a customer** or an internal aspiration? These are
  different numbers and the internal one should be stricter.
- What is an outage? *Ask directly.* Reads failing, writes failing, and slow-but-working are three
  different events and usually only one of them counts.
- What is the maintenance posture — is a planned window acceptable, or must deploys be invisible?
- Where does the target come from? "Three nines" chosen because it sounds right buys you an
  on-call rota you did not budget for. 99.9% is 43 minutes a month; 99.99% is four.

## 2. Data, RTO and RPO

- **How much data may be lost in a disaster?** (RPO.) Answers below fifteen minutes mean
  point-in-time recovery, not nightly dumps.
- **How long may recovery take?** (RTO.) The honest answer is usually "we have never tried",
  which is itself the finding — a restore that has never been rehearsed is a hope.
- What must never be deleted? Those records get an append-only class and age out by dropping a
  partition, not by a `DELETE`.
- What must be deletable on request, and does that mean hidden or gone? Write down which, per
  record class, because retrofitting the distinction is a schema migration and a legal problem.
- Where does data live, and does it have to stay there?

## 3. The core write

Take the single most important write in the system and interrogate it:

- **What happens on a retry?** If the answer is "a duplicate", you need an idempotency key: decide
  its scope, its lifetime, and what a same-key-different-body request returns.
- Is it atomic across more than one system? If yes, you need an outbox — the side effect is written
  in the same transaction as the domain row and drained separately. **Calling the queue directly
  from a request handler is the message-loss window the outbox exists to close**, and it is worth
  making a lint rule the day the queue arrives.
- What is the ordering guarantee, and does anything depend on it?
- What does a partial failure leave behind, and who cleans it up?

## 4. Under load

- What is the **scale envelope for the first year**: requests per second at peak, largest tenant,
  biggest list, widest fan-out, total rows in the largest table? Sized in orders of magnitude, not
  precision.
- What happens when a downstream dependency is slow? Timeout, retry with backoff and jitter,
  circuit breaker, or queue and drain — pick per dependency, not globally.
- What is the backpressure behaviour when the queue grows faster than it drains?
- **What degrades and what fails closed?** Search may degrade to unfiltered results; authorisation
  may not degrade at all. Enumerate this; it is the most useful list in the document.
- Are there noisy-neighbour limits — per tenant as well as per caller? A limit only on the caller
  lets one tenant with many keys drain the shared allowance.

## 5. Observability on day one

Not later. A system you cannot see is a system you debug by guessing.

- **One correlation identifier, minted at ingress, never taken from the client**, on every log line
  and every response.
- **Correlation fields are injected from ambient context, never built at the call site.** A call
  site that assembles them is a call site that will forget one.
- **Redaction is automatic**: phone numbers and emails partial, secret-named fields replaced
  wholesale, free-text content reduced to a length rather than truncated.
- **High-cardinality identifiers go on traces and exemplars, never on metric labels.** Tenant ids
  as a label is the classic way to take down your own metrics backend.
- What are the three or four signals that would page someone, and what is the runbook for each?

## 6. Change safety

- Are schema changes expand/contract only? *They should be.* A migration that renames a column
  breaks the running version.
- What operations must never appear in a migration — a lock-taking `ALTER`, a non-concurrent index
  build, an unqualified `UPDATE`? **Check the list against the migration text, not against a
  database:** the text is available in CI, the database is somebody's laptop, and a check that
  needs a stack is a check that gets skipped.
- How is a bad deploy reverted, and has that been done once on purpose?
- What is the feature-flag story, and who removes stale flags?

## 7. Write it down

Availability → `NFR-AVL-*` · performance and capacity → `NFR-PRF-*` · data, retention and
recovery → `NFR-DAT-*` · observability → `NFR-OBS-*` · maintainability and change safety →
`NFR-MNT-*`.

Each one gets a number and a way to measure it. **A non-functional requirement with no measurement
is a mood**, and it will be reported as satisfied by whoever is asked.
