# Any stack

Use this when no annex matches. It maps the gate roles onto whatever the project actually uses,
and lists the handful of decisions that are stack-shaped rather than stack-specific.

## Fill the table

Ask, then record the exact command in `DEVELOPMENT-PROCESS.md`:

| Role | Ask | If the answer is "we don't" |
|---|---|---|
| format | What formats the code, and can it check without writing? | Record the choice not to. Reformatting noise will otherwise bury every real diff |
| static analysis | What lints it, and are warnings denied? | Record it. Expect the first bug class to be one a linter catches |
| types | Is there a type checker, and is it strict? | Fine for dynamic languages — lean harder on tests |
| affected | What runs only the tests a change touches? | Fall back to the unit command — but the loop gets slower every month |
| unit | What runs fast tests, in parallel, and what is the time budget? | This is not optional |
| integration | What runs tests against a real database or service, and how is it started? | Only acceptable if the project has no external state |
| contract | Is there a published surface, and is it generated or hand-written? | Skip if nothing external consumes it |
| traceability | `python3 scripts/ledger.py check` | Not optional; it is the point |

## Configure the ledger

Two values in `scripts/ledger.config.json` are the only stack coupling in the whole tool:

```json
"tests": {
  "globs": ["tests/**/*_spec.rb"],
  "exclude": ["vendor/**"],
  "annotation": "\\[(?P<id>[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9.]+)+)\\]"
}
```

The default annotation pattern matches an `[ID]` **anywhere on a line of a test file**, and takes
the quoted string containing it as the proof — which works for essentially every test framework:

```ruby
it '[FR-ACC-01] refuses a duplicate address' do
```
```go
t.Run("[FR-ACC-01] refuses a duplicate address", func(t *testing.T) {
```
```java
@DisplayName("[FR-ACC-01] refuses a duplicate address")
```
```python
def test_refuses_duplicate(self):
    """[FR-ACC-01] refuses a duplicate address."""
```

Tighten it only if the loose form produces false positives — the trade is that a comment mentioning
an identifier then counts as proof. The cheaper defence is the convention: **never put an
annotation-shaped string in a test file unless it names a real test.**

## Decisions that come up in every stack

- **Pin tool versions exactly**, and pin the runtime in a version file the CI setup step reads.
- **One dependency manifest, one lockfile, `--frozen`/`--locked` in CI.**
- **Split unit from integration by filename suffix**, so tests sit beside their source.
- **Isolate integration tests by data, not by database.** Give every test its own tenant, account,
  or namespace. Per-worker database clones are slow and truncation between tests is a race. The
  cost, worth naming: a test may assert containment within its own scope but never a global count.
  **The payoff is parallelism**: tests that share nothing can run at once, and integration is where
  a suite spends its time.
- **Run only the affected tests while working, everything on purpose.** The `affected` role is the
  inner loop; `/test-all` and CI run the lot. Migrations are applied once per run, not per file.
- **One local stack per session**, named, with its own volumes — two sessions on one database break
  each other's migrations. Keep `.claude/worktrees/` out of git and out of every linter.
- **Say how to run a list of test files** in `falsify.runners` in `scripts/ledger.config.json`, so
  `/slice-close` can falsify a slice by running only the tests each control should break.
- **Migrations are ordered, immutable files** with a recorded checksum, applied in filename order,
  one transaction each. Editing an applied migration fails the run; you add a new one.
  Expand/contract only.
- **Check migration safety against the file, never against a database.** Where a rule speaks about
  a runtime property ("a non-empty table"), substitute a textual one that is strictly stronger
  ("a table this file did not create"). It is decidable from the text, needs no stack, and a check
  that needs a stack is a check that gets skipped.
- **A demo-facing command prints exactly one JSON object under a `--json` flag**, so a demo script
  can capture an identifier into a shell variable instead of asking the reader to paste one.
