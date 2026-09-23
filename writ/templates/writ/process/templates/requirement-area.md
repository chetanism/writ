# <FR-AREA> — <Area name>

> **What this is:** the list of requirements for one area of the product, one row each. This table
> is the only place these requirements are defined. The detail files beside it (`<FR-AREA>-NN.md`)
> explain what each one means; `writ/INDEX.md` shows the state of each.
> **Owner:** <the specification's owner>.
>
> **The wording in a row is the requirement.** Detail files copy it exactly and the check compares
> them. After launch, change a row only through a change request — never by marking up the cell.
> `Since` says when a row last changed, the changelog says what changed, and `Status` says whether
> it still applies.
>
> **Only an adopted project adds a `Provenance` column.** `decided` means someone chose this
> behaviour; `observed` means it was read off existing code, so it describes what happens, not
> necessarily what anyone wanted — an old bug looks exactly like a requirement.
> `/requirement-detail` on an `observed` row asks whether it is right, and a yes makes it
> `decided`.
>
> Delete this note.

<Two or three lines on what this area is and where it starts and stops — the neighbouring areas
that own what this one does not.>

| ID | Requirement | Target | Since | Status |
|---|---|---|---|---|
| <FR-AREA>-01 | <One sentence, behaviour not implementation.> | M1 | v0.1 | active |
