# <AREA> — foundation spec

> **Status:** draft · accepted <YYYY-MM-DD>.
> **Role:** the shape everything downstream inherits for <AREA>. A slice that must depart from this
> amends it and adds the line to `CHANGELOG.md` in the same change, rather than deciding locally.
> **Precedence:** the registers > `BRD.md` > `MILESTONE-PLAN.md` > this document.
>
> Copy this file once per shape that everything else inherits — a data model, a public API surface,
> an external port. If the project has no such shape, delete it and say so in the milestone plan.

## Index

> The declaration site for this document's decisions. Later sections elaborate; they do not
> re-declare. Give the family a two-letter prefix of its own and add it to `ID-REGISTRY.md`.

| ID | Decision | Where | Since | Status |
|---|---|---|---|---|
| <XX>-01 |  | §2 | v0.1 | active |

## 1. What this document fixes, and what it leaves open

<One paragraph each way. The second is as important as the first.>

## 2. <The first shape>

<The substance. Tables, not prose, wherever a table works. Name the enforcement mechanism for
every rule: a database constraint, a generated policy, a lint rule, a test — or "review", stated
honestly.>

## 3. <The second shape>

## 4. Rules that bind every consumer

> The short list a slice author must not violate without amending this document.

1.
2.

## 5. Open questions and amendments

Open questions are rows in `questions.md` with this document as their scope. Amendments are lines
in `CHANGELOG.md` touching the decision they changed, whose `Since` then names the amendment.
Neither lives here: a specification that is also its own history is neither.
