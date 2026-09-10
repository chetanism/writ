# BRD intake and scoping

## Accept anything

The instruction to the user is *"give me your BRD"*, and the honest range of what comes back is a
40-page specification down to a Slack message. **All of it is a valid input.** A user who could
already write the document would not be running this.

If what arrives is thin, do not push back and do not ask them to go away and write more. Say you
will build the BRD *from* the interview, and start.

## The one-screen restatement

Before any questions, write back what you understood:

- **What it is** — one sentence, in the user's own vocabulary.
- **Who it is for** — the two or three people who will actually use it.
- **What it must do** — five to nine bullets, behaviour not architecture.
- **What I am guessing** — everything you inferred rather than read.

That last list is the agenda. A user corrects a wrong guess in seconds and would have taken ten
minutes to answer the equivalent question cold.

## What the interview must end up producing

The BRD is **narrative** and the rest are **registers**, one file each — `references/11-registers.md`
says why. Adapt the list to the project; drop what does not apply and say so in `out-of-scope.md`.

| Lands in | Holds | Why it earns its place |
|---|---|---|
| `BRD.md` §1–2 | Executive summary, context | The one paragraph everyone reads; the problem, who has it, what they do today |
| `BRD.md` §3 | Vision and differentiators | Ranked. The ones marked here get extra care in every slice |
| `strategic-decisions.md` | The product-level decisions, one line each, citing an ADR | Everything downstream may reference but not contradict them |
| `BRD.md` §4 | Objectives and success measures | How you will know. Business, product, and platform |
| `personas.md`, `BRD.md` §5 | Personas as rows, and as prose | Humans *and* systems. The system actors are the ones that get forgotten |
| `BRD.md` §7–8, `invariants.md` | The day in the life, the domain, and the rules that are defects to violate | Invariants are the oracles every later test and walk reads |
| `milestones.md`, `BRD.md` §6 | The releases and their exit criteria; the scope line in prose | Which milestone, and what finished means |
| `requirements/<AREA>/index.md` | Per area, `\| ID \| Requirement \| Target \| Since \| Status \|`, one sentence each | The rows a slice claims and a test proves |
| `requirements/NFR-<AREA>/index.md` | Availability, performance, data, security, observability, maintainability | Each with a number, or it is a mood |
| `compliance.md` | Only if the domain has any. Say so explicitly if it does not | An empty register reads as an oversight; a sentence does not |
| `dependencies.md` | What you do not control, and how long each takes to unblock | The milestone plan's external tracks cite these |
| `risks.md` | With mitigations, not just names, and a scope column | One family for product and delivery risks alike |
| `assumptions.md` | Falsifiable statements | The day one is wrong, somebody must find it |
| `out-of-scope.md` | The register that saves the most work | A decision, distinguishable from an oversight |
| `questions.md` | With a decider, a date and a scope | One family, wherever a question arose |
| `glossary.md` | Only the words that mean something specific here | Narrative; declares nothing |

## Writing requirement tables

- **One sentence per requirement.** If it needs two, it is two requirements or it belongs in a
  foundation spec.
- **Numbered per area, and stable forever.** `FR-ACC-07` means one thing for the life of the
  project. Renumbering breaks every test name, commit trailer and ledger row that references it.
- **Target column** — the milestone a row is aimed at, from `milestones.md`. This is what makes
  the milestone plan possible, and it outlives a priority scheme tied to dates.
- **`Since` and `Status` columns** — `v0.1` and `active` on every row at bootstrap. They are where
  history and retirement go later, so that a cell never has to carry either.
- **Behaviour, not implementation.** "Sign-up sends a verification email" is a requirement.
  "Sign-up uses SES" is a decision, and it belongs in an ADR.
- **A requirement a test could not fail** is not a requirement. "The system is easy to use" is a
  design principle; give it a `UX-*` family or drop it.

## Deciding the areas

The area code inside `FR-<AREA>-NN` is a three-letter tag, and each area is one register file, and choosing them badly is expensive
later. Cut them by **the object they act on**, not by team or by screen: `ACC` accounts, `ORD`
orders, `PAY` payments, `NTF` notifications. Between eight and twenty-six areas is the healthy
range; fewer and the tables are unnavigable, more and the boundaries are arbitrary.

## Scope questions that change everything downstream

Ask these even when the BRD looks complete:

1. **Is this multi-tenant?** If yes, tenancy is an invariant and it shapes every table, every
   query and every test. If no, say so in the BRD explicitly, because someone will assume it is.
2. **Does anything need to be undone?** Soft delete, restore windows, and audit trails are far
   cheaper designed in than retrofitted.
3. **Is there money in it?** Money means minor units, a currency code, rounding rules, and a
   reconciliation story. It also usually means compliance.
4. **Is there an integration you do not control?** Its failure modes are requirements, and its
   onboarding time is a dependency with a lead time.
5. **Who is the second user type?** Almost every project has an admin or support persona that
   nobody mentions until the first incident.
6. **What is the largest realistic thing?** The biggest tenant, the longest list, the widest
   fan-out. This is the number phase 4 sizes against.
