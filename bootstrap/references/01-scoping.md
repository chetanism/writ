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

## What the BRD must end up containing

Adapt the section list to the project; drop what does not apply and say that you did.

| § | Section | Why it earns its place |
|---|---|---|
| 1 | Executive summary | The one paragraph everyone reads |
| 2 | Context | The problem, who has it, what they do today instead |
| 3 | Vision and differentiators | Ranked. The ones marked here get extra care in every slice |
| 4 | Strategic decisions | Numbered, with rationale. Everything downstream may reference but not contradict them |
| 5 | Success metrics | How you will know. Business, product, and platform |
| 6 | Personas and actors | Humans *and* systems. The system actors are the ones that get forgotten |
| 7 | Domain model and invariants | The core objects, and the rules that are defects to violate |
| 8 | Scope and phasing | Which milestone, and the milestone's exit criteria |
| 9 | Functional requirements | Per area, `\| ID \| Requirement \| Phase \|`, one sentence each |
| 10 | Non-functional requirements | Availability, performance, data, security, observability, maintainability |
| 11 | Compliance | Only if the domain has any. Say so explicitly if it does not |
| 12 | External dependencies | What you do not control, and how long each takes to unblock |
| 13 | Risks | With mitigations, not just names |
| 14 | Assumptions | Falsifiable statements |
| 15 | Out of scope | The section that saves the most work |
| 16 | Open questions | With a decider and a date |
| 17 | Glossary | Only the words that mean something specific here |

## Writing requirement tables

- **One sentence per requirement.** If it needs two, it is two requirements or it belongs in a
  foundation spec.
- **Numbered per area, and stable forever.** `FR-ACC-07` means one thing for the life of the
  project. Renumbering breaks every test name, commit trailer and ledger row that references it.
- **Phase column** — `V1` / `V2` / later. This is what makes the milestone plan possible.
- **Behaviour, not implementation.** "Sign-up sends a verification email" is a requirement.
  "Sign-up uses SES" is a decision, and it belongs in an ADR.
- **A requirement a test could not fail** is not a requirement. "The system is easy to use" is a
  design principle; give it a `UX-*` family or drop it.

## Deciding the areas

The area code inside `FR-<AREA>-NN` is a three-letter tag, and choosing them badly is expensive
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
