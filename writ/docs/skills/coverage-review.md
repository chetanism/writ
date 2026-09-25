# `/coverage-review`

**At a phase gate: which rows of the coverage ledger are wrong rather than unbuilt? It judges each
against its register row and hands back claim corrections for a person to apply. Report-only.**

| | |
|---|---|
| **Run it** | At each phase gate, before `/requirement-verify`, or whenever the ledger reads lower than what has been built. `/coverage-review` |
| **Produces** | A dated report and a corrections file under `writ/maintenance/audits/`, on a `docs/` branch |
| **Refuses to** | Edit a work order, a test or the ledger. The corrections are applied by a person with `scripts/claims.py apply` |

## Why it exists

**The ledger is exactly as accurate as its two inputs**: the claims in work orders and the
identifiers in test names. A slice that built a requirement and forgot to claim it, or claimed
`partial` out of caution, leaves that row `≈` or `◐` for good, because no later slice claims work
it did not do. Every input is well-formed, so the gate sees nothing wrong. Coverage under-reports
quietly, and a phase gate reads the wrong number.

On the project this came from, one run after about 150 merged slices moved fourteen rows to `●`
across fifteen merged work orders. It also turned up a defect, a contradiction between two parts of
the specification and three requirements no queued slice owned.

## What it does

1. **Classifies.** `python3 scripts/claims.py classify` sorts the rows worth a second look into four
   buckets, using the ledger's own collector: `inherited` (`≈`, tests and no claim), `partial_only`
   (every claiming slice is done and said `partial`), `claim_no_test` (a `satisfies` with no test)
   and `unclaimed_mentioned` (`○`, but named in a work order, summary or test file). Rows an earlier
   review settled are skipped until their evidence changes.
2. **Judges** each row against its register row, clause by clause, in batches handed to read-only
   readers. There are six verdicts: `DONE`, `MISSED-CLAIM`, `OPEN`, `STANDING`, `NOT-BUILT` and
   `UNCLEAR`.
3. **Re-reads every `DONE` and `MISSED-CLAIM` itself**, because a reader's verdict is a claim like any
   other.
4. **Hands back** the corrections as JSON, the tests that are owed, and every other finding sent to its
   owner. A skip list goes in for the next run.

## The bar for a correction

**The slice built it, a test naming the identifier proves it, and the claim is missing.** The work
order corrected is the slice that *finished* the requirement, not the last one to mention it. A
`claim_no_test` row is never corrected; its test is owed first. An `≈` row no merged slice built is
evidence older than the process, and it becomes `●` through a characterisation slice instead.

## What changes in a merged work order

Only `satisfies:` and `partial:`. `DEVELOPMENT-PROCESS.md` §6.2 allows exactly that, and
`claims.py apply` enforces it. The tool checks every entry before it edits any: the work order is
`done`, the identifier is declared and live, and a move to `satisfies` has a test. It then prints a
commit message that names each identifier and the test that proves it. The body, the criteria and
every other field stay as they were agreed.

## See also

[`/requirement-verify`](requirement-verify.md) is the other half at the same gate. This review asks
whether the ledger's `●` rows are the right ones; that one asks whether a `●` row's behaviour is
really there.
