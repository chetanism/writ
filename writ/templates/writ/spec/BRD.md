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

> **Role:** the case for the product — the problem, who has it, what changes for them, and how
> success is judged. It is **narrative**: it declares no identifiers and carries no tables of
> requirements. Those live in the registers beside it (`README.md` says which), where a tool can
> read them and a person can find them. This document says *why*; the registers say *what*.
> **Precedence:** the registers > this document > `MILESTONE-PLAN.md` > `process/SLICE-QUEUE.md`.
> Where this narrative and a register disagree, the register is right and this is corrected.
> **It freezes at launch.** After the first release the registers are the living truth, changed
> only through `changes/`; this document is re-cut at a milestone boundary if the story changed,
> and never carries a "what changed" section — `CHANGELOG.md` is that.
>
> Delete every section that does not apply to this project, and say so in `out-of-scope.md`.
> Delete this blockquote.

---

## 1. Executive summary

<Two paragraphs. What this is, who it is for, and what changes for them.>

## 2. Context

### 2.1 Problem statement
### 2.2 Who has this problem
### 2.3 What they do today instead
### 2.4 Commercial model

## 3. Vision and differentiators

<What this does that the alternatives do not, ranked, and where it is deliberately at parity.
Naming the non-differentiators prevents the most wasted effort. The strategic decisions this rests
on are the register `strategic-decisions.md`; cite them by identifier rather than restating them.>

## 4. Objectives and success measures

<What must be true for this to have worked, each one measurable. A measure with no number is a
mood, and it will be reported as met by whoever is asked.>

## 5. Who this is for

<The personas in prose — a paragraph each on the job they are doing and the day they are having.
The register `personas.md` carries their identifiers and the one-line row a detail file quotes;
this is where the reader comes to understand them.>

## 6. Scope

### 6.1 In scope for the first release
### 6.2 Deferred, not rejected
### 6.3 Where the line is drawn, and why

<Prose. The itemised exclusions with their identifiers are `out-of-scope.md`; the milestones and
what each delivers are `milestones.md`.>

## 7. How the work gets done

<The day in the life, with and without this product. The one section a new engineer should read
before any register — it is what the requirements are *for*.>

## 8. The domain

<The nouns and how they relate. One paragraph and a list, not a diagram. The invariants that bind
every implementation are the register `invariants.md`.>

## 9. Requirements

The requirements are registers, one per area, under `requirements/<AREA>/index.md`, with a detail
file beside each one that has been worked out. **They are not restated here.** `../INDEX.md`
lists every one with its state; `MILESTONE-PLAN.md` says which are being built now.

## 10. Constraints, compliance and the rest

<Prose on the regulatory and environmental setting: what law applies, what the deployment must
look like, what the product may never do. The itemised requirements this produces are registers —
`compliance.md`, and constraint rows in the relevant area's register.>

## 11. What this document does not carry

Risks are `risks.md`. Assumptions are `assumptions.md`. External dependencies are
`dependencies.md`. Open questions are `questions.md`, whichever document they arose in. Anything
that changed since this was written is `CHANGELOG.md`. Terms are `glossary.md`.
