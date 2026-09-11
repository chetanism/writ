---
id: SL-001
title: borrow and return a copy
phase: P01
kind: feature
size: S
estimated: 120
code_lines: 138
status: done
dep: "—"
owner: ""
issue: 14
depends_on: []
touches: []
satisfies: [FR-LEND-01, FR-LEND-02]
partial: []
adr: []
demo: script
---

# Slice SL-001 — borrow and return a copy

## Why this slice exists

The shelf is currently a paper sheet on the wall, and it is wrong within a week of anybody going
on holiday. Nobody can tell whether a book is out or simply missing, so people buy second copies
of books the office already owns. This slice is the smallest thing that makes the shelf's state
answerable: a copy is either out to a named person or it is not.

## Decisions this slice makes

A loan is a row with a null `returned_at` rather than a status column, so the invariant is a
unique partial index the database enforces, not a rule the application remembers to apply.

## Acceptance criteria

1. Borrowing a copy that is on the shelf records a loan against the borrower and the time.
2. Returning a copy the borrower holds clears the loan and puts the copy back on the shelf.
3. Borrowing a copy that is already out is refused, and says who holds it.

## Demo

`npm run demo:lending` borrows a copy as one person, shows the second borrow refused, returns it,
and shows the copy back on the shelf. Ninety seconds.
