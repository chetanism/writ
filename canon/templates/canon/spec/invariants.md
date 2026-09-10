# Invariants

> **Role:** the properties that must always hold, binding on every implementation. Violating one
> is a defect, not a style preference. **A register:** one table, and nothing else declares an
> `INV-*`. Name the layer that enforces each; an invariant enforced only by convention is a hope.
> **Owner:** <the person who approves invariants>.
>
> Delete this blockquote.

| ID | Invariant | Enforced by | Since | Status |
|---|---|---|---|---|
| INV-001 | <Every row carries a tenant, and a query issued without tenant context returns nothing.> | <row-level security, generated from the table declaration> | v0.1 | active |
