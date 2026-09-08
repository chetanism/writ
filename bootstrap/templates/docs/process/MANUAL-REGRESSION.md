# Manual regression

> **What this is.** A standing, ordered list of scenarios a human runs by hand. Each was promoted
> here from a slice's demo because it is worth checking again after later slices change things
> underneath it.
>
> **What this is not.** An archive of every demo ever written. Entries are **deleted** once an
> automated test covers them. This file stops being read the moment it stops being short, and a
> checklist nobody reads is worse than no checklist, because it looks like coverage.

## How it stays alive

| | |
|---|---|
| **Promoted** | At step 7 of the loop, when the demo proved something worth re-checking |
| **Re-run** | By **DoD-10** — a slice that changes behaviour an entry covers re-runs and re-dates it |
| **Retired** | When an automated test asserts the same thing. Note the test name in the commit and delete the entry |
| **Before a milestone closes** | Every entry is run in order, regardless of what changed |

An entry that has not been re-dated in five slices that plausibly touched it is a signal that
either the entry is wrong or DoD-10 is being skipped. Both are worth stopping for.

## Entry format

```markdown
### MR-NN — <short title>

**Covers:** requirement identifiers
**Setup:** the fixture state assumed
**Steps:** numbered, copy-pasteable
**Expected:** what you should see, specifically enough to be wrong
**Last verified:** slice id and date
**Retire when:** the automated test that would replace this
```

---

<!-- Entries below, in the order they should be run. -->

*No entries yet.*
