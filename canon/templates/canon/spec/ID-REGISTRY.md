# Identifier registry

> **Role:** the single declaration of every identifier family used across this repository — what it
> means, which file or directory owns it, where in that document it is declared, and whether it is
> *traceable* (something a slice can claim coverage of).
>
> **This document declares families, not identifiers.** The identifiers themselves are read from
> the registers that own them. A hand-maintained list of every requirement is exactly the artefact
> that rots; `../INDEX.md` is that list, generated. A row is added here when a whole new *kind* of
> identifier appears, which is rare.
>
> Delete this blockquote.

## The declaration rule

> **An identifier is declared if and only if it is the first cell of a table row, inside the
> section named below, under a table whose header row begins `| ID |`.**

- Section scope runs from the named heading to the next heading of the same or higher level, so
  subsections are included and siblings are not. A section of `*` means the whole document.
- **A directory owner declares in every register file beneath it** — `requirements/<AREA>/
  index.md`, one table each. A file beneath it named for an identifier is an elaboration and
  declares nothing, whatever tables it carries. A family whose files are named by number —
  `decisions/0004-a-thing.md` — is declared by those filenames; one whose files carry `id:` in
  their front matter, by that.
- Headings are matched loosely — `§9` finds `## 9. Functional requirements` — so the registry stays
  readable. Bold and backticks are stripped, so `| **INV-001** |` and `| INV-001 |` are the same.
- **Elaboration is not a second declaration.** A later section discussing an identifier in prose is
  a reference. Every reference is checked against what was declared, and a dangling one fails the
  build naming the file and line.

## The pattern is the width

> `N` runs are fixed widths: `SL-NNN` admits `SL-042` and refuses `SL-42`, and nothing admits
> `SL-042b`. A suffix letter is how a numbering scheme starts lying — a split mints two fresh
> numbers. `<AREA>` is a run of capitals. A lone `N` is any number of digits, for a family that was
> never padded.

## Families

> Delete the rows that do not apply. Add one per identifier kind this project actually uses. Mark
> `Traceable` **yes** only where a slice may claim it and a test may prove it.

| Family | Pattern | Owner (relative to `canon/`) | Declared in | Kind | Traceable |
|---|---|---|---|---|:--:|
| `FR` | `FR-<AREA>-NN` | `spec/requirements/` | * | requirement | yes |
| `NFR` | `NFR-<AREA>-NN` | `spec/requirements/` | * | requirement | yes |
| `INV` | `INV-NNN` | `spec/invariants.md` | * | invariant | yes |
| `CMP` | `CMP-NN` | `spec/compliance.md` | * | requirement | yes |
| `D` | `D-NN` | `spec/strategic-decisions.md` | * | strategic decision | yes |
| `G` | `G-NN` | `spec/MILESTONE-PLAN.md` | §2 Gates | milestone gate | yes |
| `DoD` | `DoD-N` | `process/DEVELOPMENT-PROCESS.md` | §4 Definition of done | process rule | yes |
| `M` | `MN` | `spec/milestones.md` | * | milestone | no |
| `PER` | `PER-NN` | `spec/personas.md` | * | persona | no |
| `DEP` | `DEP-NN` | `spec/dependencies.md` | * | external dependency | no |
| `RSK` | `RSK-NN` | `spec/risks.md` | * | risk | no |
| `ASM` | `ASM-NN` | `spec/assumptions.md` | * | assumption | no |
| `OOS` | `OOS-NN` | `spec/out-of-scope.md` | * | exclusion | no |
| `Q` | `Q-NNN` | `spec/questions.md` | * | open question | no |
| `X` | `X-NNN` | `spec/CHANGELOG.md` | * | amendment | no |
| `CR` | `CR-NNN` | `spec/changes/` | * | change request | no |
| `SL` | `SL-NNN` | `process/work-orders/` | * | slice | no |
| `ADR` | `ADR-NNNN` | `decisions/` | * | decision record | no |

## One family per kind

An open question is a `Q-*` whether it arose in the specification, the milestone plan, a
foundation spec or a slice; the `Scope` column says where. A risk is an `RSK-*` whether it is to
the product or to a milestone's delivery. An amendment is an `X-*` in the one changelog whatever
document it amended. **A kind of thing never gets a second family for having been written down in
a second document.** Foundation specs are the one exception: each declares its own two-letter
decision family, because its decisions are a different kind from the strategic ones.

## Traceable and non-traceable

**Traceable** means a slice's front matter may claim it and a test may annotate it.
`process/COVERAGE.md` is built from the traceable families and nothing else.

A non-traceable family is not lesser. It means the identifier names something other than a unit of
work: a risk is *mitigated*, not satisfied; a persona is *served*; a slice is *done*, and its own id
is how the ledger records that; a change request is *applied* and then *built*, and the index
derives both.

## Adding a family

1. Add a row above.
2. Declare the identifiers in the owning register as an `| ID |` table — with `Since` and `Status`
   columns, so history and retirement have somewhere to go that is not the cell.
3. Run `python3 scripts/ledger.py`. A family declared traceable that yields no identifiers fails
   the check — that is this registry's own integrity test, and it is why the fourth column is a
   section and not a prose hint.

**Never teach a parser a new prefix.** Adding a family is a row here and nothing else.
