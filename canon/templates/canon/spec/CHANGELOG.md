# Changelog

> **Role:** every amendment to the specification and the plans, one line each, newest first. The
> only history this repository keeps outside git. **A register:** one table, and `X-*` is the one
> amendment family across every document — the milestone plan, a foundation spec and a register
> all log here.
>
> **A row is a line, and the check holds it to one.** `Touches` names the identifiers or the
> version it changed, and each must exist. `Change` says what, in a sentence. `Cause` says who or
> what asked for it, and cites the ADR or the slice summary that carries the reasoning — the
> reasoning itself never goes in a cell. The commit that made the change carries `Amends: X-NNN` in
> its trailer, so `git log --grep` finds it and nothing has to be backfilled here.
>
> A version bump is a row too: `Touches` is the version tag, and the rows introduced by it say so
> under `Since`.
>
> Delete this blockquote.

| ID | Date | Touches | Change | Cause | By |
|---|---|---|---|---|---|
| X-001 | <YYYY-MM-DD> | v0.1 | <The specification set is written.> | <Bootstrap.> | <name> |
