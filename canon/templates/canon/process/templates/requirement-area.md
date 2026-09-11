# <FR-AREA> — <Area name>

> **Role:** the requirements of one area, one row each. **A register:** this file carries one
> table and nothing else declares these identifiers. The detail files beside it —
> `<FR-AREA>-NN.md` — say what each one means; `../../../INDEX.md` says what state each is in.
> **Owner:** <the specification's owner>.
>
> **The row is the requirement, verbatim.** A detail file quotes its second cell character for
> character and the check compares them, so the wording here is the wording. Amend it through a
> change request after launch, and never with a marker in the cell — `Since` says when, the
> changelog says what, and `Status` says whether it still stands.
>
> **An adopted project adds a `Provenance` column**, and only an adopted one. `decided` is a row
> somebody chose; `observed` is a row read off code that already runs, which means it describes
> what happens and not necessarily what anybody wanted — every bug old enough to be relied on
> reads exactly like a requirement. `/requirement-detail` on an `observed` row asks whether it is
> right, and that is how one becomes `decided`. `ledger.py stats` counts what is left.
>
> Delete this blockquote.

<Two or three lines on what this area is and where it starts and stops — the neighbouring areas
that own what this one does not.>

| ID | Requirement | Target | Since | Status |
|---|---|---|---|---|
| <FR-AREA>-01 | <One sentence, behaviour not implementation.> | M1 | v0.1 | active |
