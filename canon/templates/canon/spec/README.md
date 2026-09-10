# The specification, and where each kind of thing lives

**A file holds one kind of thing, and status is a column.** There are five kinds, and each has its
own place. A file that holds two of them is the file nobody can read six months in — the
specification that is also its own history, the plan that is also its risk log.

| Kind | What it is | Where |
|---|---|---|
| **Narrative** | The case for the product: context, problem, personas in prose, objectives, scope, how the day works. No identifier tables | `BRD.md`, `glossary.md` |
| **Registers** | One table of identified items each, with a short preamble. What tools read and what people look up | `requirements/<AREA>/index.md`, `invariants.md`, `compliance.md`, `strategic-decisions.md`, `personas.md`, `milestones.md`, `dependencies.md`, `risks.md`, `assumptions.md`, `out-of-scope.md`, `questions.md` |
| **Plans** | Gates, phases, what is not built, external tracks — tables only | `MILESTONE-PLAN.md`, `../process/SLICE-QUEUE.md` |
| **History** | Dated, append-only, one line per change | `CHANGELOG.md` |
| **Elaboration** | One file per identifier that needs more than a row | `requirements/<AREA>/<id>.md`, `changes/`, `../decisions/`, work orders, slice summaries |

`../INDEX.md` is generated from all of it — one line per identifier, where it is declared and
what state it is in. **Open that first.**

## The rules, and the check behind each

- **A register carries exactly one `| ID |` table.** A narrative carries none. `python3
  scripts/ledger.py check` fails either way round, and the two lists are `registers` and
  `narrative` in `scripts/ledger.config.json`.
- **Status is a column.** A withdrawn or superseded requirement keeps its row and its number,
  says so under `Status`, leaves the coverage ledger and can still be cited. Never a
  strikethrough, never deleted.
- **History is never inline.** No `(new — v3.0)`, no `Amended 2026-…` in a cell. A row's `Since`
  names the version, amendment or change request that introduced it; the changelog says what
  changed; an ADR or a slice summary says why. The check refuses a cell carrying history.
- **One family per kind, across the repository.** Every open question is a `Q-NNN` with a scope
  column, wherever it arose. Every risk is an `RSK-NN`. Every amendment is an `X-NNN` in the one
  changelog. Nothing gets a new family for having been written in a new document.
- **Every identifier resolves.** An identifier mentioned anywhere under `canon/` that no register,
  work order, decision or change request declares fails the check, naming the file and line.
- **Widths are fixed and suffixes do not exist.** `ID-REGISTRY.md` states each family's pattern;
  a three-digit family admits three digits and refuses two, and a split mints two fresh numbers
  rather than a suffix letter.
- **After launch, the registers change only through a change request.** `changes/README.md` is
  that process. A row added with no accepted request behind it fails the check.

## Reading order for somebody new

1. `../INDEX.md`, to see what exists.
2. `BRD.md`, for why.
3. The register for the area you are working in, then its detail files.
4. `MILESTONE-PLAN.md` and `../process/SLICE-QUEUE.md`, for what is being built now and in what
   order.
5. `CHANGELOG.md` only when you need to know how something got to be the way it is.
