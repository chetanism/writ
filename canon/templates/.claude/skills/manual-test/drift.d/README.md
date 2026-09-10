# Project drift checks

Anything **executable** in this directory is run by `drift.py`, from the repository root. A non-zero
exit means something an oracle names no longer exists; whatever it printed becomes the detail.

This is the extension point for the checks only this project can make — the ones that need its own
surface. `drift.py` itself only knows what the identifier registry and `canon/decisions/` can tell
it, which is stable but shallow. Add a check here as soon as something becomes enumerable:

| Once the project has | A check worth adding |
|---|---|
| A published route table | every path cited in `areas.md` is served by a declared route |
| An error-code catalogue | every code cited still exists in it |
| A CLI | every verb cited is still in the command registry |
| A generated contract | the oracle's field names still appear in it |

Each is a few lines: enumerate the live thing, grep the reference files for what they claim, and
exit non-zero naming the difference. Keep them **read-only and fast** — `drift.py` runs them before
every session, with a 120-second bound each.

A check that needs the stack up is a check that gets skipped. Prefer one that reads the repository.
