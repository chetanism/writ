# Identifier registry

> **Role:** the single declaration of every identifier family used across this repository — what it
> means, which document owns it, where in that document it is declared, and whether it is
> *traceable* (something a slice can claim coverage of).
>
> **Precedence:** `BRD.md` > `MILESTONE-PLAN.md` > `SLICE-QUEUE.md` > everything else.
>
> **This document declares families, not identifiers.** The identifiers themselves are read from
> the documents that own them. A hand-maintained list of every requirement is exactly the artefact
> that rots. A row is added here when a whole new *kind* of identifier appears, which is rare.

## The declaration rule

> **An identifier is declared if and only if it is the first cell of a table row, inside the
> section named below, under a table whose header row begins `| ID |`.**

- Section scope runs from the named heading to the next heading of the same or higher level, so
  subsections are included and siblings are not.
- A section of `*` means the whole document.
- Headings are matched loosely — `§9` finds `## 9. Functional requirements` — so the registry stays
  readable.
- Bold and backticks are stripped, so `| **INV-1** |` and `| INV-1 |` declare the same identifier.
- **Elaboration is not a second declaration.** A later section discussing an identifier in prose is
  a reference.
- Anything else — a mention, a cross-reference, a heading — is a **reference**. References are
  checked by the ledger against what was declared.

## Families

> Delete the rows that do not apply. Add one per identifier kind this project actually uses. Mark
> `Traceable` **yes** only where a slice may claim it and a test may prove it.

| Family | Pattern | Owner (relative to `canon/`) | Declared in | Kind | Traceable |
|---|---|---|---|---|:--:|
| `FR` | `FR-<AREA>-NN` | `spec/BRD.md` | §9 Functional requirements | requirement | yes |
| `NFR` | `NFR-<AREA>-NN` | `spec/BRD.md` | §10 Non-functional requirements | requirement | yes |
| `CMP` | `CMP-NN` | `spec/BRD.md` | §11 Compliance and regulatory requirements | requirement | yes |
| `INV` | `INV-N` | `spec/BRD.md` | §7.2 Invariants | invariant | yes |
| `D` | `D-NN` | `spec/BRD.md` | §4.0 Index | decision | yes |
| `G` | `G-NN` | `spec/MILESTONE-PLAN.md` | §2 Gates | milestone gate | yes |
| `DoD` | `DoD-N` | `process/DEVELOPMENT-PROCESS.md` | §4 Definition of done | process rule | yes |
| `PER` | `PER-N` | `spec/BRD.md` | §6.1 Human personas | persona | no |
| `RSK` | `RSK-NN` | `spec/BRD.md` | §13 Risks | risk | no |
| `ASM` | `ASM-NN` | `spec/BRD.md` | §14 Assumptions | assumption | no |
| `OOS` | `OOS-NN` | `spec/BRD.md` | §15 Out of scope | exclusion | no |
| `OQ` | `OQ-NN` | `spec/BRD.md` | §16 Open questions | open question | no |
| `X` | `X-NN` | `spec/MILESTONE-PLAN.md` | §9 Amendments | amendment | no |
| `SL` | `SL-<PHASE>N` | `process/SLICE-QUEUE.md` | * | slice | no |
| `ADR` | `ADR-NNNN` | `decisions/` | * | decision record | no |

## Traceable and non-traceable

**Traceable** means a slice's front matter may claim it and a test may annotate it.
`process/COVERAGE.md` is built from the traceable families and nothing else.

A non-traceable family is not lesser. It means the identifier names something other than a unit of
work: a risk is *mitigated*, not satisfied; a persona is *served*; a slice is *done*, and its own id
is how the ledger records that.

**A family whose owner is a directory cannot be traceable** — there is no `| ID |` row to read.

## Adding a family

1. Add a row above.
2. Declare the identifiers in the owning document as an `| ID |` table inside the named section.
3. Run `python3 scripts/ledger.py`. A family declared traceable that yields no identifiers fails
   the check — that is this registry's own integrity test, and it is why the fourth column is a
   section and not a prose hint.

**Never teach a parser a new prefix.** Adding a family is a row here and nothing else.
