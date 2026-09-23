---
name: test-all
description: Run the whole test suite on demand — unit tests in parallel, then the stack up, integration tests, and the stack down — timing each part and naming the slowest tests. Report-only; it fixes nothing. Use before closing a slice, after a dependency or configuration change, when the affected-only run may have missed something, or when the user asks to run all the tests or the full suite.
---

# Run the full test suite

While a slice is being built, run **only the tests the change affects** — `<Affected test
command>` — because that is the fast loop and it is what `DEVELOPMENT-PROCESS.md` §3 step 5 means.
This skill is the other half: everything, once, on purpose. CI runs the same thing on every pull
request, so this is how you find out before the push rather than after it.

Invoked as `/test-all`, or `/test-all unit` / `/test-all integration` for one part.

## 1. Say what you are about to run

One line: which parts, and whether the stack needs to come up. **If the working tree has
uncommitted changes, say so** — the result is for the tree as it stands, not for the last commit.

## 2. Run it, cheapest first, timing each part

| # | Part | Command | Notes |
|---|---|---|---|
| 1 | Traceability | `python3 scripts/ledger.py check` | Seconds. A stale ledger fails CI as surely as a red test |
| 2 | Unit | `<Unit test command>` | **In parallel** — the runner's default worker count. Each test owns its own data |
| 3 | Stack up | `<Stack-up command>` | Skip 3–5 when the project has no external state. Use this session's own named stack if the project has one, never a stack another session is using |
| 4 | Integration | `<Integration test command>` | Parallel only where `CLAUDE.md` says the stack allows it; otherwise one file at a time |
| 5 | Stack down | `<Stack-down command>` | **Always**, even after a failure |

Time each part (`time`, or the runner's own summary). **Keep going after a failure** so the report
covers everything — one run that names three broken things beats three runs that name one each —
except that a failing stack-up skips integration, because every integration test would fail for the
same reason.

Ask the runner for its slowest tests: `<Slowest-tests flag>` (for example `--durations=10` for
pytest, or a JSON reporter for vitest).

## 3. Report

```
/test-all — 4m 12s

ledger check   ok        3s
unit           ok       41s   812 tests · 8 workers
integration    FAILED 3m 20s  2 of 164 failed
  - src/orders/refund.integration.test.ts › [FR-PAY-04] refunds a captured payment once
  - src/orders/refund.integration.test.ts › [FR-PAY-05] refuses a second refund

slowest
  38s  src/reports/export.integration.test.ts
  21s  src/billing/invoice.integration.test.ts
```

Then, only where it applies:

- **A failure**: the test's name and requirement identifier, and the first line of the assertion
  message. Do not fix it in this run — say whether it looks like the change on this branch or
  something older, and stop.
- **A slow part**: if unit tests took longer than `<N>` seconds, or one integration file takes more
  than a quarter of the integration time, name it as a finding. Slow tests are why people stop
  running them.
- **A flaky test** — one that fails, then passes on an immediate re-run of that file alone — is a
  finding of its own, never a pass. Name it; do not re-run the suite until it goes green.

## What this never does

- Edit code or tests, or skip, retry or quarantine a test to get a green result.
- Leave the stack running.
- Use another session's stack or database. Two sessions sharing one database break each other's
  migrations and data.
