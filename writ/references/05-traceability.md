# Traceability

Four sources, joined by one tool, written down as one generated document. None of them is a list
maintained beside the specification, because a hand-kept traceability matrix always drifts — and a
drifting matrix is worse than none, since it invites false confidence.

```
ID-REGISTRY.md          which families are traceable
  └ each family's declaring section     which identifiers exist
work-orders/**/*.md front matter        what each slice claimed
[ID]-annotated test names               what is actually proven
                    ↓
            COVERAGE.md   (generated)
```

## The registry declares families, never identifiers

This is the load-bearing distinction. A hand-maintained list of every requirement is exactly the
artefact that rots. A list of *kinds* of identifier changes a few times a year.

`writ/spec/ID-REGISTRY.md` carries one table:

```
| Family | Pattern | Owner (relative to `writ/`) | Declared in | Kind | Traceable |
|---|---|---|---|---|:--:|
| `FR` | `FR-<AREA>-NN` | `spec/requirements/` | * | requirement | yes |
```

**Adding a family is a Markdown row — never teaching a parser a new prefix.** The tool hardcodes no
prefix anywhere.

**The pattern is the width.** `N` runs are fixed: `SL-NNN` admits three digits and refuses two, and
nothing admits a suffix letter. An identifier outside its family's pattern fails the check.

**An owner may be a directory.** It declares in every register file beneath it — one `index.md` per
requirement area — and a file beneath it named for an identifier is an elaboration that declares
nothing, whatever tables it carries. A family whose files are named by number, like ADRs, is
declared by the filenames; one whose files carry `id:` in front matter, like change requests, by
that.

## The one declaration rule

> **An identifier is declared if and only if it is the first cell of a table row, under a header
> row beginning `| ID |`, inside the section named in the registry.**

Everything else — a mention in prose, a cross-reference, a heading, a repetition in a later
section — is a **reference**. References are checked against what was declared; they do not declare.

Supporting rules:

- Section scope runs from the named heading to the next heading of the **same or higher level**, so
  subsections are included and siblings are not.
- A section of `*` means the whole document.
- Headings match loosely: `§9` finds `## 9. Functional requirements`. The registry stays readable
  and the matcher does the work.
- Bold and backticks are stripped from cells, so `| **INV-003** |` and `| INV-003 |` are the same
  declaration.
- **Elaborating on an identifier is not a second declaration.** A later section that discusses
  a decision in prose is a reference.
- **`Status` and `Since` are read by name.** A row whose `Status` is `withdrawn` or `superseded`
  is retired: it leaves the ledger, keeps its number, and can still be cited. A `Since` names the
  version, amendment or change request that introduced the row, and must exist. A cell carrying
  history inline — `(new — v3.0)`, `Amended 2026-…`, a strikethrough — fails the check.
- **Every reference resolves.** An identifier-shaped token in prose or inline code anywhere under
  `writ/` must be declared somewhere; fenced blocks and blockquotes are notation. A dangling
  reference fails the build naming the file and line.

The registry's own integrity test: **a family declared traceable that yields no identifiers fails
the check.** That is why the column is a section and not a prose hint.

## Traceable and non-traceable

**Traceable** means a slice may claim it and a test may annotate it. `COVERAGE.md` is built from
the traceable families and nothing else.

A non-traceable family is not lesser. It means the identifier names something other than a unit of
work: a risk is *mitigated*, not satisfied; a persona is *served*; a slice is *done*, and its own
id is how the ledger records that. Risks, personas, assumptions, exclusions, open questions,
amendments, slices and ADRs are all non-traceable in a healthy registry.

## Claims and proof

A work order claims in its **front matter**, and nowhere else:

```yaml
satisfies: [FR-ACC-01, FR-ACC-02]
partial: [INV-003]
```

One claim site means there is nothing to drift. A test proves by carrying the identifier in its
name:

```
it('[FR-ACC-01] refuses a second account for the same address', ...)
```

The tool reads *source text*, not test results. That is deliberate: it reports what the suite
claims to prove, and whether the suite passes is a separate gate step. Conflating the two lets a
skipped test count as evidence with nobody able to tell which of the two failed.

The pattern is matched over the **whole file**. A formatter that wraps a long test name onto its own
line leaves the call on one line and `[ID]` on the next, and a per-line scan loses the annotation in
the one place evidence is counted — silently, and usually on the longest-named tests, which are the
ones proving the most.

**Never put an annotation-shaped string in a test file that is not a real test.** A fixture
containing `it('[FR-ACC-01] …')` credits a requirement with a test that does not exist. Fixtures
belong in a plain module.

## Status

| Mark | Status | Means |
|:--:|---|---|
| ● | satisfied | A work order claims `satisfies` **and** at least one test names it |
| ◐ | partial | A `satisfies` claim with no test, **or** a `partial` claim, **or** tests with no claim |
| ○ | none | Nothing |

A `satisfies` claim with no test behind it is downgraded **and listed separately** under *Claimed
without proof*. This is the whole point of generating the document rather than maintaining it.

## What fails the build, and what only gets reported

**Fatal** — an annotation or claim naming a registered family but an undeclared number (that is a
typo, and typos in traceability are invisible); a traceable family yielding nothing; a family
declared twice; an identifier declared twice in one section; an identifier outside its family's
width or carrying a suffix; a stale generated artefact, `INDEX.md` included; a dependency on an
unknown slice or a cycle; a work order naming an ADR that does not exist, declaring a phase the
config does not list, or filed under a directory or a filename that disagrees with its front
matter; a missing or unusable demo section; an unresolved placeholder; a slice marked done with no
summary; a register with other than one ID table or a narrative with one; a cell carrying history
inline; an empty or unresolvable `Since`; a changelog row undated, touching nothing that exists,
or over the line budget; a reference in prose to an identifier nothing declares; an accepted
change request not applied, or one applied before it was accepted.

**Fatal, where the requirement detail track is installed** — a detail file quoting its requirement
differently from the specification, character for character; one filed in the wrong area directory
or named for an identifier the specification does not declare or no longer declares; a missing
front-matter field or template section; `reviewed` with no approver; a phase disagreeing with the
specification's; a verdict outside `implemented|gap|absent|detail-wrong`; two files for one
requirement. The quote comparison is the load-bearing one — it is what turns an amendment into a
failing build rather than a slow divergence nobody sees. `references/10-requirements.md` is the
reference.

**Reported, not fatal** — an annotation or claim from a family the registry does not carry. That is
either a new document needing a registry row or a reference to a document that owns no identifiers,
and **doing the right thing should not be punished with a red gate.** Both are rendered into
`COVERAGE.md` so the loose end is visible. So is the detail track's backlog: every requirement the
ledger reads as `●` with no reviewed detail file behind it, listed rather than averaged away.
`requirements.require_detail_for_satisfied` turns that list fatal, and it is `false` until the
backlog is cleared — switching it on with one only breaks the gate for work nobody has been asked
for yet.

## The index, the changelog, and change requests

`writ/INDEX.md` is generated beside the coverage ledger and byte-checked like it: one line per
identifier, where it is declared, its status, its coverage, its detail and scenario state, the
questions open against it, and for a change request whether it is applied and built.

`writ/spec/CHANGELOG.md` is the one amendment register. The check holds each row to a line — a
date, `Touches` naming identifiers that exist or a version tag, `Change` and `Cause` under the
length budget — so the reasoning has to go where reasoning lives.

A change request under `writ/spec/changes/` is one file per post-launch change with a `Changes`
table of `add`, `amend` and `withdraw` rows. The check reconciles it against the registers: an
accepted request whose rows are not there with `Since: CR-NNN` fails, and so does a row applied
while the request is still a draft.

## Commit trailers

One commit per slice, squashed. The trailer block makes `git log --grep 'FR-ACC-01'` answer *where
did this requirement get built* with no tooling at all:

```
feat(accounts): refuse duplicate addresses at the database

Sign-up now fails closed on a unique violation rather than checking first,
which removes the race between the check and the insert.

Slice: SL-042
Satisfies: FR-ACC-01, FR-ACC-02
Partial: INV-001
Decision: ADR-0004
Amends: X-017

Closes #14
```

`Closes #14` is last and has no colon — that is the form the issue-closing parser wants. `Amends:`
is present where the slice added a changelog line and absent where it did not. The lines above
are trailers for `git log`.

## Generated artefacts are committed and checked

Write the file, commit it, and have CI regenerate it in memory and compare bytes. Committing it is
what makes a coverage change a reviewable diff instead of a number in a log nobody reads.
