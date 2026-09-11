# The gate

## Roles, not tools

A gate is a set of questions, and each one gets exactly one command. Fill the table in phase 5;
a role with no command is a choice, and the process document should say it was made.

| Role | Question | Typical |
|---|---|---|
| format | Is it formatted? | `fmt --check` |
| static analysis | Does it smell? | a linter, warnings denied |
| types | Does it typecheck? | the compiler, strict |
| unit | Does it do what we told it? | fast, no external services |
| integration | Does it do it against the real thing? | a real database in a container |
| contract | Did the published surface change? | a generated document, compared to the committed one |
| traceability | Do the claims hold? | `python3 scripts/ledger.py check` |

## Rules that survive contact with a real project

- **Keep the steps separate in CI**, even though one command runs them all locally. A red cross
  should name the thing that broke.
- **Put the cheap checks first.** Traceability and format take seconds; integration takes minutes.
- **Deny warnings.** A warning nobody fixes is a warning everybody stops reading.
- **Pin tool versions exactly**, not with a caret. A formatter that changes its mind in a patch
  release turns every subsequent diff into noise.
- **Cache by lockfile, and use a version file** (`.nvmrc`, `.python-version`, `.tool-versions`) so
  local and CI cannot disagree about the runtime.
- **No pre-commit hooks.** The gate is CI. A hook that re-runs the same checks more slowly is how
  people learn to pass `--no-verify`. *(If you want a hook, make it one that costs milliseconds and
  checks something CI cannot.)*
- **Hold the unit suite to a time budget** — ten seconds is a good starting number — and treat a
  breach as a defect. A suite slow enough to skip gets skipped.
- **Split unit from integration by filename suffix**, not by directory, so a test sits beside the
  code it tests: `foo.test.*` runs everywhere, `foo.integration.test.*` runs only where there is a
  stack.

## The `paths-ignore` trap

Excluding docs from the main workflow is right — a typo fix should not spin up a database. But:

> **A workflow skipped by `paths-ignore` reports no status at all.** If the gate is a *required*
> status check, every docs-only pull request blocks forever waiting for a check that will never
> run.

Two fixes, and only one of them is correct:

- ✅ Add a second job or workflow that always runs and reports success.
- ❌ Remove the filter, and pay for a database on every typo.

## The complement pattern

There is a second, less obvious consequence. Adding a requirement to the BRD changes the coverage
ledger and touches no code — so the ledger check must run on exactly the pull requests the main
gate skips.

The shape: the main workflow uses `paths-ignore` for docs; a second workflow uses a `paths`
**allow-list** naming precisely the generated artefact's inputs — the spec directory, the work
orders, the committed ledger, and the test files. The traceability check also runs inline in the
main gate, so the two together cover every pull request exactly once.

Both templates ship in `templates/.github/workflows/`.

## Branch protection

On a team, the gate is a required check and `main` takes no direct pushes. On a solo build the same
rule still earns its place: **no change reaches the integration branch except through a pull
request** — including documentation, including one-line fixes. The pull request is the one place a
diff is presented for reading rather than for writing, and reading it is the point.

Branch shape:

```
main                   releasable; only ever receives merges from the integration branch
dev                    integration; the base for every slice, and the default branch
slice/<ID>-<slug>      one per slice
docs/<slug>            specification and process changes that are not a slice
```

Squash into `dev`; merge `dev` into `main` without squashing. **Open the branch and a draft pull
request at work-order time**, before any code — then the diff arrives against a stated intent
instead of having to explain itself.
