# How to ask

Governs every question in both bootstrap skills. Read it before phase 1.

## The protocol

- **Use `AskUserQuestion`, at most four questions per call.** More than four in one screen and the
  last two get answered carelessly.
- **Number every question**, restarting at 1 each round. The user answers by number.
- **Give every option a one-line consequence**, not a label. "Postgres" is not an option;
  "Postgres — you get transactions and RLS, and you run a server" is.
- **Recommend, and say why in one line.** Put the recommendation first and mark it. A bare menu
  makes the user do your job.
- **Never ask what you can read.** Check the repository, the BRD, and what the user already said
  before asking anything.

## Calibrating depth

Match the number of rounds to what the BRD already settles, and say which mode you are in:

| The BRD is | Rounds | You are |
|---|--:|---|
| A finished specification | 2–3 | Confirming, and finding the gaps its author could not see |
| A structured draft | 4–6 | Filling in requirement-level detail |
| A few paragraphs | 6–10 | Writing the BRD *with* the user, in question form |
| One sentence and a competitor | 8–12 | Starting from the problem, not the solution |

Announce the mode: *"Your BRD settles scope but not the data model, so I expect four rounds."* A
user who knows how long it will take answers more carefully.

## The stop rule

Stop asking when you can write every requirement table **without inventing a fact the user has not
stated**. When you catch yourself about to invent one — a retention period, a rate limit, a role
name, a currency — that is the next question.

Then say so explicitly, and list what you are leaving open. An open question written into the
document with a named decider is a fine outcome. A guess written as a requirement is not: it will
be built, tested, and defended by everything downstream, and nobody will remember it was a guess.

## Coarse to fine

Never open with the data model. The order that works:

1. **What is it, and what breaks if it does not exist?**
2. **Who uses it?** Name two or three concrete people, not segments.
3. **What is the core object?** The noun the product is about. Almost every project has exactly
   one, and every later question hangs off it.
4. **What is that object's lifecycle?** Created how, changed by whom, ends when.
5. **What are the boundaries?** Tenancy, permissions, what one user must never see.
6. **What is out of scope?** Ask directly. The answer is a document section, and it is the section
   that prevents the most work.
7. **What happens when it goes wrong?** Retries, partial failures, the thing that is down.

## Recording an answer you did not get

Three shapes, and they are not interchangeable:

- **Open question** — nobody knows yet. Goes in the BRD's open-questions section with a decider and
  a date it must be answered by.
- **Assumption** — you proceeded on a belief. Goes in the assumptions section, stated as something
  falsifiable, so the day it turns out to be wrong someone can find it.
- **Out of scope** — decided, deliberately, not to do. Goes in the exclusions section with where it
  lands instead.

A thing in none of these is a thing you forgot.

## Surviving the session — the interview record

Ten phases, six to ten rounds of questions in phase 2 alone, and **nothing is written to disk
before phase 6**. That is deliberate — an interview that has already committed to an answer stops
being an interview — but it means a session that dies at phase 7 costs the user every answer they
gave, and a bootstrap somebody has to find two uninterrupted hours for is one that gets put off.

So keep a record. **`.canon-interview.md` at the target root, appended after every phase**, and
deleted at the commit once its content is in the documents.

- **One section per completed phase**, headed `## Phase N — <name>`. Terse: the decisions, one line
  each, in the user's words rather than yours. What was asked and answered, what was left open, and
  anything you would otherwise have to ask twice.
- **Append, never rewrite.** A phase that reopens an earlier answer writes the correction in its own
  section and says which it supersedes; the record is a transcript, not a summary.
- **It is not a deliverable.** It holds answers, and the documents hold the specification. Nothing
  reads it after the bootstrap, which is why it is deleted rather than committed — a second
  home for the same facts is the failure `references/11-registers.md` is entirely about, and it
  would start on day one.
- **Write it before you report the phase**, not after. The report is the thing you are doing when a
  session runs out of room.

### Resuming

**Phase 0 looks for it before anything else.** If it exists, read it and say what it holds — which
phases are recorded, the project name, and the last decision in the last section — then ask, in one
`AskUserQuestion`:

1. **Resume from the next phase** (the default). Do not re-ask anything a section already answers,
   and say which phase you are starting at.
2. **Start over.** Delete the file first and say so, so there is no half-record underneath the new
   one.

If the target already has `<canon>/spec/` **and** an interview record, the earlier run got past
phase 6 and the tree is the better record: report both, and offer to adopt around the tree as
phase 0 already requires. Never resume into a directory a previous run has already written.

## Things to ask that people forget

- What does the user see the first time they open it, with no data?
- Who deletes things, and what does deleting actually mean — hidden, or gone?
- What must be in an audit trail, and who reads it?
- What happens on the second click of a submit button?
- What is the plan for the thing you are integrating with being down for an hour?
- Which of these numbers is a real target and which is a hope?
