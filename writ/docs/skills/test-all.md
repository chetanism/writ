# `/test-all`

**The whole test suite, on purpose: unit tests in parallel, then the stack up, integration tests,
and the stack down. Each part timed, the slowest tests named. Report-only.**

| | |
|---|---|
| **Run it** | Before closing a slice, after a dependency or configuration change, or whenever the affected-only run might have missed something. `/test-all`, or `/test-all unit` |
| **Produces** | A report in the conversation: each part's result and time, every failing test by name and requirement, the slowest tests |
| **Refuses to** | Fix, skip, retry or quarantine a test, or leave the stack running |

## Why it exists

**During a slice you run only what the change affects**, because the full suite is slow enough that
running it after every edit trains people to stop running it. Something has to run everything, on
purpose, before the push rather than after it. CI does it on every pull request; this is the same
run, one command away, while there is still time to fix what it finds.

## What it does that a bare test command does not

- **Keeps going after a failure**, so one run names everything broken rather than the first thing.
- **Times each part and names the slowest tests.** A suite gets slow one file at a time, and
  nobody notices until a run takes ten minutes.
- **Always brings the stack down**, and never uses another session's stack.
- **Treats a flaky test as a finding**, never a pass.

## See also

[`/slice-close`](slice-close.md) — which assumes the full gate is green before it starts, and runs
the falsification tool over just the tests each control should break.
