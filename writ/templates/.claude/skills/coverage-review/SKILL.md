---
name: coverage-review
description: Find the coverage ledger's rows that are wrong rather than unbuilt — a requirement a merged slice built and never claimed, a row every slice marked partial though it is finished, a claim no test backs, a requirement only prose names — judge each against its register row, and hand back claim corrections as a JSON file a person applies. Report-only; it never edits a work order. Use every few slices, at a phase gate, or when the ledger reads lower than what has been built.
---

# Coverage review

`writ/process/COVERAGE.md` is generated from work-order claims and annotated test names, so it is
exactly as accurate as they are. **A slice that built a requirement and did not claim it, or
claimed `partial` out of caution, leaves that row wrong for good** — no later slice claims work it
did not do. The gate cannot see this: every input is well-formed. This review looks for it.

Invoked as `/coverage-review`. Run it every few slices, or at a phase gate before
`/requirement-verify`, which only looks at rows already `●`.

**Report-only.** It writes one dated report and one corrections file under
`writ/maintenance/audits/`, and nothing else — not a work order, not a test, not the ledger. A
correction is applied by a person with `scripts/claims.py apply` (§4). That split is deliberate:
the review is a reader's judgement, and the edit to a merged record is somebody's decision.

## 1. Classify

```bash
python3 scripts/claims.py classify --json --batch 30 --skip <the latest writ/maintenance/audits/coverage-review-*.md>
```

Leave `--skip` off on the first run. It sorts the rows worth a second look into four buckets from
the ledger's own collector, so it cannot disagree with `COVERAGE.md` about what a row is:

| Bucket | What it is | Usually |
|---|---|---|
| `inherited` | `≈` — tests name it, no slice claims it | A missed claim when a merged slice's work order or summary names it; evidence older than the process when none does |
| `partial_only` | `◐` — every claiming slice is done and said `partial`, and tests exist | Still open. Now and then finished and never said so |
| `claim_no_test` | A done slice claimed `satisfies` and no test names it | A test is owed. No claim moves until it exists |
| `unclaimed_mentioned` | `○`, yet a work order, summary or test file names it | Scope-outs, mostly. A test-file mention is one the annotation pattern misses: the ledger cannot see it, and it may not be evidence |

Every row carries a `key`. It changes whenever the claims, tests or mentions behind the row
change, which is how `--skip` knows a settled row has moved and must be judged again.

## 2. Judge

Hand each batch to a **read-only** reader, one bucket at a time. For each row the reader has the
register row's text, the claiming work orders and their summaries, the tests the row lists, and the
code those tests exercise. **Judge the register row clause by clause**: a requirement is finished
when every clause of it is built and a test proves it, not when its headline is.

| Verdict | Means | Goes |
|---|---|---|
| `DONE` | Claimed `partial` everywhere, and every clause is built and proven | a correction to `satisfies` |
| `MISSED-CLAIM` | Built and proven by a merged slice that never claimed it | a correction to `satisfies`, or to `partial` if only some clauses are built |
| `OPEN` | Genuinely unfinished; the ledger is right | the skip list |
| `STANDING` | A constraint honoured by the design, which no single test proves | the skip list, and the report says why |
| `NOT-BUILT` | Named in prose — a scope-out, a later-slice note — and not built | the skip list |
| `UNCLEAR` | The register row is ambiguous enough that two verdicts hold | the specification's owner, as a finding |

**Re-read every `DONE` and `MISSED-CLAIM` yourself, against the register row, before it becomes a
correction.** A reader's `DONE` is a claim like any other. The project this review came from had
two wrong ones: an ADR that *deferred* a feature, read as one that *refused* it, and a requirement
that said *field-level*, met at record level.

**The correction bar**, all three or no correction:

1. **The slice built it.** The work order named is the slice that *finished* the requirement, not the
   last one to mention it. Read the summaries in order.
2. **A test naming the identifier proves it.** `claims.py apply` refuses a move to `satisfies`
   without one. A `claim_no_test` row is never corrected: say which test is owed.
3. **The claim is missing** — absent, or `partial` where it should be `satisfies`.

An `inherited` row no merged slice built is not a correction. It is evidence older than the
process, and a characterisation slice is how it becomes `●` (`DEVELOPMENT-PROCESS.md` §6.2).

## 3. Hand back

Write two files, `<date>` being today as YYYY-MM-DD:

- **`writ/maintenance/audits/coverage-review-<date>.json`** — the corrections, one entry per
  identifier per work order, the path relative to `writ/process/work-orders/`:

  ```json
  [{"work_order": "<milestone>/<phase>/<N>.md", "id": "<requirement id>", "to": "satisfies"}]
  ```

- **`writ/maintenance/audits/coverage-review-<date>.md`** — the report:
  - the bucket counts, and how many rows were skipped as settled;
  - every correction, with the test that proves it and one line on why that slice finished it;
  - the owed tests, from `claim_no_test`, each named as the slice that should write it;
  - everything else the review turned up, **each handed to its owner rather than fixed here** — a
    defect to the slicer as a queue row, a contradiction between two parts of the specification to
    its owner (`/change-request` after launch), a requirement no queued slice owns to the slicer;
  - a `## Skip next run` list, one line per `OPEN`, `STANDING` and `NOT-BUILT` row, in the shape
    `claims.py classify --skip` reads: ``- `FR-ACC-01` · `3f9a01c2` · OPEN``.

A report is a record of this run, never rewritten afterwards. Both files go on a
`docs/coverage-review-<date>` branch off `dev`.

## 4. Stop, and say what the person runs

Report in the terminal: the bucket counts, the corrections, the owed tests and the findings handed
on. Then, **for the person to run on the same branch** — never run it yourself:

```bash
python3 scripts/claims.py apply writ/maintenance/audits/coverage-review-<date>.json
python3 scripts/ledger.py
```

`apply` checks every entry before it edits any — the work order is `done`, the identifier is
declared and live, a move to `satisfies` has a test — and changes only the `satisfies:` and
`partial:` lines. It prints the commit message: commit the work orders and the regenerated ledger
together with it, as its own documentation-only commit (`DEVELOPMENT-PROCESS.md` §6.2), then open
the pull request into `dev`.
