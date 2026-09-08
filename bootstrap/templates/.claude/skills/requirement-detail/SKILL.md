---
name: requirement-detail
description: Work out with the reader what one requirement means, then write its detail file — a short read-back, an interview in rounds, and the file last, so a manual test case can be written from it. Use when asked to detail, elaborate or write up a requirement by its identifier, or when preparing a phase's requirements for hand testing.
---

# Detail one requirement

The parallel track described in `docs/process/requirements/README.md`. **You are drafting, not
deciding.** What a requirement means belongs to the specification's owner; what you produce is a
first reading they correct.

Invoked as `/requirement-detail FR-ACC-01`.

**It is a conversation, not a delivery.** Read the requirement, put eight lines in front of the
reader, ask them the handful of questions whose answers change the file, and write it once you both
know what it says. Generating ninety lines and asking somebody to find the wrong three is the shape
this replaces — a reviewer reading a plausible document agrees with it, which is exactly the failure
the whole track exists to avoid.

## 0. One requirement at a time

**One identifier per invocation.** Given an area or a phase, list the identifiers it covers, say
which have files already, and ask which one to start with. Given several identifiers, do the first
and stop.

This is not politeness. A session holding twelve requirements writes twelve files that blur into
each other, and the blurring is invisible in review — which is the failure this whole track exists
to avoid.

## 1. Refuse the ones that are not yours

- **Not declared in the specification** — stop and say so. The identifier may have been withdrawn
  (struck through in `docs/spec/BRD.md`, which un-declares it) or mistyped.
- **Outside the covered families** — `requirements.families` in `scripts/ledger.config.json` names
  them. The rest name mechanisms and process rules, not things a person is asked to exercise. Say
  which requirement the mechanism serves and offer that instead.
- **A file already exists** — read it. If it is `reviewed`, do not rewrite it; propose the specific
  correction and stop. If it is a `draft`, this is the **review conversation** rather than a first
  draft: summarise it in step 3 the same way, add a line saying where you would now write it
  differently, and interview from there. Working through the existing drafts with their owner is
  what this mode is for.

## 2. Read, and read only this

| Read | For |
|---|---|
| The requirement's row in `docs/spec/BRD.md`, **and the rows around it** | Its own words, and where its neighbours' scope begins — that is the *Out of scope* fence |
| The foundation spec that governs the area | The shape the behaviour must take |
| Its row in `docs/process/COVERAGE.md` | Which slices claim it and which tests name it |
| Those slices' work orders and summaries | What was actually built, what was deferred, and to which slice |
| The annotated tests themselves | The behaviour that is really asserted, in its own words |
| `.claude/skills/manual-test/reference/areas.md`, the section covering the area | The oracles — **cite them, never restate them** |
| The surface: the command-line usage, the published contract | Where a person can actually exercise it today |

Do **not** read the other requirements' detail files. Do not read the whole specification.

## 3. Summarise it in eight lines, before writing anything

**Do not write the file yet.** Put the requirement in front of the reader first, short enough to
take in at a glance:

```
FR-ACC-01 · V1 · phase F · ● satisfied by SL-F1, SL-F2

Says      <the specification's own words, one line, quoted>
Surface   <where a person can exercise it today — route, command, screen — and what is not built>
Actors    <who acts, and the one or two who must be refused>
Reads as  <one sentence: what you believe it means in the application>
Unsettled <the two or three things the requirement does not answer>
```

That last line is the point of the exercise. Everything after it is a conversation, not a document
review — the reviewer should never be handed ninety lines and asked to find the three that are
wrong.

## 4. Interview, in rounds of two to four

Ask only questions **whose answer changes the file**. Never ask what the specification already
answers, what the tests already show, or what you could read in the code — those are yours to find
out, and asking them is how an interview becomes an interrogation nobody finishes.

- **Batch two to four at a time, numbered, each with the answer you would pick and why.** The
  reviewer should be able to reply *"1 yes, 2 the second one, 3 ask the owner"*. Use
  `AskUserQuestion` where the answers are a closed set, so it is one click rather than a sentence.
- **Round one is meaning**: the actors who must be refused, the boundary the requirement is silent
  about, the neighbouring requirement the fence runs against.
- **Round two is the observables**: read them back as a numbered list, one line each, and ask which
  are wrong, missing or untestable. This is where a reviewer's real knowledge lands, and it is worth
  more than every other section together.
- **Round three, only if it earns itself**: the boundary and negative cases you are unsure apply.
- Stop when the answers stop changing anything. Three rounds is plenty; if a fourth is needed, the
  requirement is probably two requirements, and that is a finding for its owner.

**Two answers you must not simply take:**

1. **An answer that changes what the product should do** is a specification amendment, not a
   detail-file answer. Say so, write the reviewer's reading into *Open questions* naming them, and
   let them decide whether to amend `docs/spec/BRD.md`.
2. **An answer that contradicts an invariant or a shipped behaviour.** Name the invariant, name the
   two answers, and stop — the same rule the slicer works under (`DoD-12`).

If the reader says to skip the interview, skip it: draft the file and put every question you would
have asked into *Open questions*. A drafted file with five honest open questions is a good outcome.

## 5. Write it

Copy `docs/process/templates/requirement-detail.md` to
`docs/process/requirements/<area>/<id>.md` — the area is the identifier without its number, and the
check fails if the file sits anywhere else.

**The quote is copied, never composed.** `## The requirement` carries the second cell of the
requirement's row, verbatim, as a blockquote; `python3 scripts/ledger.py check` compares it against
the specification character for character, so a paraphrase is a failing build rather than a slow
divergence. Wrapping it across several `>` lines is fine.

Then the rest, in the words of somebody testing the product rather than building it:

- **Observable behaviour is the section that matters.** Every line must be capable of being
  **wrong**. *"The queue updates correctly"* cannot be; *"a second desk advancing the same record
  against a stale version is refused, and the refusal names the version it read"* can be, and a
  tester knows what to do with it. Prefer what a person can see — a screen, a response, a command's
  `--json` object, a row that did or did not appear.
- **Say what is not built yet, and name the slice that builds it.** A requirement claimed by a
  future slice still gets a file; a tester needs to know which half is testable today.
- **Actors: fill the *May not* column properly.** It is the column that is always thin and always
  where the interesting cases are.
- **Boundary and negative cases: delete the template rows that do not apply.** An empty row is
  worse than a missing one. Reach for the five that break real systems — another tenant, an actor
  with no membership or a deactivated one, the same request twice, two people at once, and a value
  at its limit.
- **Out of scope is a fence, not a formality.** Name the neighbouring requirement that owns each
  thing this one does not.

## 6. Do not guess

Where the interview did not settle something a tester would hit — because nobody in the room owns
it, or because the answer would change the product — it goes in **Open questions**, addressed to a
person by name, with the two answers named. Never resolve it in the file — a detail file that
answers a question the specification left open is a specification with no owner, and nobody will
ever know it happened.

Where the specification is genuinely wrong — self-contradictory, or contradicted by an invariant —
that is a finding for its owner, said out loud in your reply, not a correction made here.

## 7. Close the loop without a wall of text

Run `python3 scripts/ledger.py` and `python3 scripts/ledger.py check`, then report **in a dozen
lines or fewer**:

- what changed from what you read back in step 4 — one line each, and nothing that did not change;
- the observables, numbered, one line each;
- the open questions by number, and who each is addressed to;
- the two or three places you are still least sure.

**Never print the file back.** The reviewer has been in the conversation; they do not need it
recited, and a recitation is how the parts nobody discussed get read as agreed.

`status` stays `draft` and `approved_by` stays empty unless the person you have just interviewed
**owns the specification** and says plainly that the file now reads right — then set both, naming
them. Where that is also the person who asked you to draft it, say that `drafted_by` and
`approved_by` are now the same person, which the process accepts and prefers not to. Approval is
theirs to give and never yours to assume.
