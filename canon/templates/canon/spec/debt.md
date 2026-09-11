# Known debt

> **Role:** what is true of this codebase and should not be. Not a risk — a risk has not happened
> yet; not an open question — nobody is undecided; not out of scope — this is in the product and
> it is wrong. **A register:** one table.
> **Owner:** <the specification's owner>.
>
> **This register exists so the survey can be honest.** A specification reverse-engineered from
> working code describes what the code does, and some of what the code does is a mistake nobody
> has had time to fix. Without somewhere to put that, the writer has two options and both are
> bad: promote the mistake to a requirement, or leave it out and let the next reader rediscover
> it. A row here is neither — it is the thing written down.
>
> **A slice reads the rows for the area it is about to touch.** That is the whole return on
> keeping this: `DEBT-004` costs nothing to record and saves the afternoon somebody would have
> spent finding out.
>
> **Rows leave by being fixed, not by being tidied.** A row withdrawn because it no longer seems
> important is the register lying. `Status` carries `open`, `accepted` — known, and deliberately
> not being fixed, with the reason in the cell — or `fixed`, naming the slice.
>
> A greenfield project ships this file empty and may never write a row in it; it is the one
> register whose emptiness is good news. Delete this blockquote.

| ID | Debt | Area | Costs | Since | Status |
|---|---|---|---|---|---|
| DEBT-001 | <Sessions are stored in memory, so any deploy signs everybody out.> | <auth> | <A support ticket per deploy; blocks horizontal scaling> | v0 | open |
