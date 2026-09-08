# Python

A second worked example, to show what changes between ecosystems and what does not.

## Gate roles

| Role | Command |
|---|---|
| format | `ruff format --check .` |
| static analysis | `ruff check .` |
| types | `mypy --strict src` (or `pyright`) |
| unit | `pytest -m "not integration"` |
| integration | `pytest -m integration` |
| contract | `python -m app.openapi --check` if there is a published API |
| traceability | `python3 scripts/ledger.py check` |

## Project shape

- **`uv` or Poetry, with a committed lockfile** and `--frozen` in CI. `.python-version` pins the
  runtime for both local and CI.
- `src/` layout, so tests import the installed package rather than the working directory.
- Pin the tool versions exactly in the dev dependency group.
- `ruff` covers both roles; `TID251` is the equivalent of a restricted-import rule, and its message
  should carry the rationale exactly as a lint message would elsewhere.

## Tests

Split by marker rather than by filename, since pytest makes markers first-class:

```toml
[tool.pytest.ini_options]
markers = ["integration: needs a database or another live service"]
addopts = "--strict-markers"
```

Annotate with the requirement id in the test name or its first docstring line — both are matched by
the default pattern:

```python
def test_refuses_a_duplicate_address():
    """[FR-ACC-01] refuses a second account for the same address."""
```

Ledger configuration:

```json
"tests": {
  "globs": ["tests/**/*.py", "src/**/test_*.py"],
  "exclude": [".venv/**"],
  "annotation": "\\[(?P<id>[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9.]+)+)\\]"
}
```

## Database

- **Alembic migrations are ordered and immutable** once applied. The same rule holds: add a new
  revision, never edit an applied one, and expand/contract only.
- SQLAlchemy sessions do not make tenancy safe on their own. If there is a tenancy invariant, put
  it in Postgres row-level security and set the context with `SET LOCAL` inside the transaction —
  the ORM is a convenience, not a boundary.
- Isolate integration tests by minting a tenant per test rather than truncating between them.

## The dev CLI

`argparse` with a dict of subcommands, or Typer if the project already depends on it. Same rule:
one registry, help generated from it, and a `--json` flag on anything a demo script needs to
capture an identifier from.

## Async

If the service is async, decide once and write it down: no blocking call in an async path, and one
named place where sync work is offloaded. Left implicit, this becomes the first production
incident that is hard to diagnose.
