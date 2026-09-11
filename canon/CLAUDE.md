# `canon/` — not part of the host project

> **Ignore this directory for every development task in the repository it sits in.**

This is a Claude Code plugin for setting up the *next* project's development process. It is
installed from here and run inside other repositories; it is not a component of the one that
carries it.

Concretely, when working on the host project:

- **It is not a package.** Nothing here is built, installed, linted or tested as part of the host.
  If the host's formatter or linter walks every file, exclude this directory so the YAML and JSON
  templates keep the shape a reader needs to see.
- **It contributes to no slice, work order or size budget.** A change here is never part of the
  host's process records.
- **Its templates deliberately contain requirement-shaped strings** — `FR-ACC-01`, `[DoD-7]`,
  `INV-003` — that mean nothing in the host. They are examples inside a template. If the host runs a
  traceability tool of its own, keep this directory out of its test globs.
- **The Python here is not a host dependency.** `scripts/ledger.py` is stdlib-only and runs
  standalone.

If you were asked to change the host project, nothing in here is in scope. If you were asked to
improve the bootstrap kit, read `README.md` in this directory first.
