# `bootstrap/` — not part of this project

> **Ignore this directory for every Connect development task.**

This is a portable kit for setting up the *next* project's development process. It was extracted
from Connect's own `docs/` tree and generalised; it is here so it can be copied out, not because
Connect uses it.

Concretely, when working on Connect:

- **It is not a workspace package.** No `package.json`, nothing to build, nothing to test. `pnpm`
  and Turborepo do not see it.
- **It contributes to no slice's size budget.** A change here is never part of a Connect slice, and
  it does not belong in a Connect work order or slice summary.
- **Its templates deliberately contain requirement-shaped strings** — `FR-ACC-01`, `[DoD-7]`,
  `INV-1` — that mean nothing in Connect. They are examples inside a template. Connect's own ledger
  does not reach them: it scans `apps|packages|tooling` for `*.test.ts` and
  `docs/process/work-orders/*.md`, and none of those paths is under `bootstrap/`.
- **It is excluded from `oxfmt` and `oxlint`** via `ignorePatterns` in `.oxfmtrc.json` and
  `.oxlintrc.json`, so the YAML and JSON templates keep the shape a reader needs to see.
- **The Python here is not a Connect dependency.** `scripts/ledger.py` is stdlib-only and runs
  standalone; Connect's own traceability tooling remains `tooling/generators`.

If you were asked to change Connect, nothing in here is in scope. If you were asked to improve the
bootstrap kit, read `bootstrap/README.md` first.
