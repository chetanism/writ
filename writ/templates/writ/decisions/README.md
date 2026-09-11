# Architecture decision records

## What goes here

**Write an ADR when you rejected a credible alternative.** Choosing one identifier scheme over two
others is an ADR. Naming a file is not.

The test: would a competent engineer arriving in six months reconstruct this choice by reading the
code, or would they re-litigate it? If the latter, it needs a record — and *Alternatives rejected*
is the section that does the work.

## When

**Before the implementation the decision governs**, not at the end of the slice. A record written
afterwards is a justification: it knows how the story ended, and it will not honestly represent the
option that was nearly chosen. The work order names the record in its `adr:` front matter, and
`python3 scripts/ledger.py check` fails while the file does not exist.

## Relationship to the strategic decisions

A `D-*` is a row in `spec/strategic-decisions.md` — a product-level decision in one line, citing the
ADR that carries its reasoning. An ADR is discovered by reading this directory. If a decision is
important enough that a future reader must not miss it, it gets a row there as well as a record
here.

**An ADR never contradicts a `D-*`.** If one would, the `D-*` is amended first — through a change
request after launch — and the changelog line names both.

## Rules

1. **Numbered sequentially and immutably.** Numbers are never reused, even when a record is
   superseded.
2. **Never edited after acceptance**, apart from adding a `Superseded by` link in the header. A
   record of what we believed at the time is the whole value; editing it destroys that.
3. **Superseding is a new record** that names what it replaces and says what changed our mind.
4. **One decision per record.** Two decisions is two records.
5. Referenced from the slice summary and from the commit trailer (`Decision: ADR-NNNN`).

## Naming

`NNNN-<the decision, as a sentence>.md` — `0035-a-credential-is-only-as-live-as-its-account.md`.
A title that states the decision as a fact is readable from a directory listing, which is where
most of them are found.

## Status values

| Status | Means |
|---|---|
| `Proposed` | Written, not yet acted on |
| `Accepted` | In force |
| `Superseded by ADR-NNNN` | No longer in force; kept for the record |

## Format

Copy `template.md`. Four sections, and the fourth is not optional.
