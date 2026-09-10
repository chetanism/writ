# Business Requirements Document — **<PROJECT>**
### <ONE LINE ON WHAT IT IS>

| Field | Value |
|---|---|
| **Document** | <PROJECT> — Business Requirements Document |
| **Version** | 0.1 (Draft) |
| **Status** | For review |
| **Date** | <YYYY-MM-DD> |
| **Owner** | <NAME> |
| **Audience** | <WHO READS THIS> |

> **Role:** the source of truth for scope, requirements and constraints. Everything else in this
> repository may reference it and may not contradict it.
> **Precedence:** this document > `MILESTONE-PLAN.md` > `process/SLICE-QUEUE.md` > everything else.
> **Requirement identifiers are stable.** Reference them; never renumber them.
>
> Delete every section that does not apply to this project, and say in §15 that you did. Delete
> this blockquote.

---

## 1. Executive summary

<Two paragraphs. What this is, who it is for, and what changes for them.>

## 2. Context

### 2.1 Problem statement
### 2.2 Who has this problem
### 2.3 What they do today instead
### 2.4 Commercial model

## 3. Vision and differentiators

### 3.1 Differentiators, ranked

| ID | Differentiator | Why it is hard to copy |
|---|---|---|
| DIF-1 |  |  |

### 3.2 Explicit non-differentiators

<Where deliberately at parity. Naming these prevents the most wasted effort.>

## 4. Strategic decisions and constraints

### 4.0 Index

> This index is the declaration site for every `D-*`. Later sections elaborate; they do not
> re-declare.

| ID | Decision | Where |
|---|---|---|
| **D-1** |  | §4 |

## 5. Success metrics

### 5.1 Business
### 5.2 Product
### 5.3 Platform and reliability

## 6. Personas and actors

### 6.1 Human personas

| ID | Persona | Goal | Frustration today |
|---|---|---|---|
| PER-1 |  |  |  |

### 6.2 System actors

<Every non-human that calls in or gets called. These are the ones that get forgotten.>

## 7. Domain model and invariants

### 7.1 Core entities

<The nouns, and how they relate. One paragraph and a list, not a diagram.>

### 7.2 Invariants — binding on all implementation

> An invariant is a property that must always hold. Violating one is a defect, not a style
> preference. Name the layer that enforces it; an invariant enforced only by convention is a hope.

| ID | Invariant | Enforced by |
|---|---|---|
| **INV-1** |  |  |

## 8. Scope and phasing

### 8.1 Module scope matrix
### 8.2 Milestones

| ID | Milestone | Exit criterion |
|---|---|---|
| M0 | Foundations |  |

### 8.3 Acceptance criteria for first release

| ID | Criterion |
|---|---|
| GA-01 |  |

## 9. Functional requirements

> **Notation.** `[V1]` first launch · `[V2]` later · `[R]` roadmap. Requirements are numbered per
> area and are stable identifiers — do not renumber.

### 9.1 <Area name> — `FR-<AREA>`

| ID | Requirement | Phase |
|---|---|---|
| FR-<AREA>-01 | <One sentence, behaviour not implementation.> | V1 |

## 10. Non-functional requirements

> Each one gets a number and a way to measure it. A non-functional requirement with no measurement
> is a mood, and it will be reported as satisfied by whoever is asked.

### 10.1 Availability — `NFR-AVL`

| ID | Requirement | Phase |
|---|---|---|
| NFR-AVL-01 |  | V1 |

### 10.2 Performance and capacity — `NFR-PRF`
### 10.3 Data, retention and recovery — `NFR-DAT`
### 10.4 Security — `NFR-SEC`
### 10.5 Observability — `NFR-OBS`
### 10.6 Maintainability and change safety — `NFR-MNT`

## 11. Compliance and regulatory requirements

> If the domain has none, say so here in one sentence and delete the table. An empty compliance
> section reads as an oversight; a sentence saying it was considered does not.

| ID | Requirement | Source |
|---|---|---|
| CMP-01 |  |  |

## 12. External dependencies

| ID | Dependency | Lead time | What is blocked until it lands |
|---|---|---|---|
| DEP-01 |  |  |  |

## 13. Risks

| ID | Risk | Mitigation |
|---|---|---|
| RSK-01 |  |  |

## 14. Assumptions

> Stated so that they are falsifiable. The day one turns out to be wrong, someone must be able to
> find it.

| ID | Assumption |
|---|---|
| ASM-01 |  |

## 15. Out of scope

| ID | Not building | Why, and where it would land |
|---|---|---|
| OOS-01 |  |  |

## 16. Open questions

| ID | Question | Decider | Needed by |
|---|---|---|---|
| OQ-01 |  |  |  |

## 17. Glossary

<Only words that mean something specific here.>
