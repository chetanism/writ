---
name: change-request
description: Raise one change to the requirement registers after launch — draft the rows to add, amend or withdraw, read them against the invariants for conflict, list what goes stale, and stop for the specification's owner to decide; then apply an accepted request to the registers, the changelog and the index. Use when a new requirement arrives, an existing one must change, or the user says to raise or apply a change request.
---

# Raise, and apply, one change request

The process in `writ/spec/changes/README.md`. **You are drafting, not deciding.** What the product
should do is the specification owner's; what you produce is one page about one change that they
can say yes or no to.

Invoked as `/change-request` to raise one, or `/change-request apply CR-NNN` once it is accepted.

**It is the detail interview pointed at a change.** Read the registers, put the change in front of
the owner as rows, ask the handful of questions whose answers change the rows, and write the file
once you both know what it says. Generating a page and asking somebody to find the wrong line is
the shape this replaces.

## 0. One change at a time

**One request per invocation.** Given several, do the first and stop. A request that adds a
requirement, amends a neighbour and withdraws a third is one request if they are one job and three
if they are not; ask which.

## 1. Refuse the ones that are not yours

- **A change to the narrative** — `writ/spec/BRD.md` is re-cut at a milestone boundary, not one
  request at a time. Say so, and offer to raise the register change the narrative would need.
- **A decision rather than a change** — a choice between alternatives with no new row behind it is
  an ADR. Say so.
- **A question rather than a change** — something nobody has answered is a row in
  `writ/spec/questions.md`. Add it there and stop.
- **Before launch** — the registers are still being written and a change request is ceremony on
  top of an edit. `writ/spec/changes/README.md` says when the track starts; before that, amend the
  register, add the changelog line, and stop.

## 1a. Get onto the request's branch

**One request, one branch**, `cr/<id lowercased>` — `cr/cr-012`. The dirty-tree rule and the four
cases are `/requirement-detail`'s step 1a, unchanged; a request is settled over more than one
sitting the same way a detail file is. Where there is no remote, the branch is local and the pull
request waits, and you say so.

## 2. Read, and read only this

| Read | For |
|---|---|
| The area's register, `writ/spec/requirements/<AREA>/index.md`, **and the neighbouring areas'** | The next free number, the rows this touches, and where the fence runs |
| `writ/spec/invariants.md`, the ones governing the area | The conflict read — would this change make one false |
| `writ/INDEX.md` | Which of the touched identifiers have detail files, scenarios, open questions — what goes stale |
| `writ/spec/milestones.md` | Which milestone this can be aimed at |
| `writ/spec/changes/`, the open requests | Whether somebody is already changing the same rows |

Do **not** read the narrative BRD for the answer. If the request needs something the registers do
not say, that is a question for the owner, not something to look up.

## 3. Read the change back as rows, before writing anything

**Do not write the file yet.** Put the change in front of the owner as the rows it would become:

```
CR-012 · a second location · target M2 · requested by <who>, because <evidence>

add     FR-ORG-12   A tenant may open a second location, with its own address and hours.
amend   FR-ORG-08   … (the full new text) …
withdraw FR-ORG-03  superseded by FR-ORG-12

Conflict  INV-003 says … ; this change would … — NEEDS A RULING
Stale     FR-ORG-08's detail file (reviewed), its scenarios (reviewed), Q-014 (open)
Missing   <what the request does not say and the slicer will hit>
```

The conflict line is the point of the exercise. **A conflict is the owner's to resolve**: name the
invariant, the row, and the two answers, and stop. Never take the reading that makes the change
work, and say *no conflicts* out loud when there are none.

**A request raised from a reconciliation** — a detail file's *Reconciliation* row decided
`change-request`, because the build got something right that the requirement got wrong — says so
in *The job*, citing the detail file and the slice. The row names this request, so write the
request first; once it is applied, the amended quote fails the detail file until it is re-read, and
that re-reading is where the row's conflict is closed (`DEVELOPMENT-PROCESS.md` §12.1).

## 4. One round of questions, and only what changes the rows

Two to four, in the shape of `CLAUDE.md` §*Asking me to decide* — lettered options, each with what
it leads to and why it is or is not recommended, one marked recommended. The ones worth asking are
almost always: which milestone, whether an amend is really a withdraw plus an add, and who must be
turned away by the new row. Never ask what the registers already answer.

## 5. Write it

Copy `writ/process/templates/change-request.md` to `writ/spec/changes/CR-NNN-<slug>.md`, the
next free number. Fill the four sections; the *Changes* table is what the check reconciles later,
so the identifiers in it are exact and the `add` rows carry the full sentence that will become the
register row. **Do not touch the registers.** A draft changes nothing.

Run `python3 scripts/ledger.py check`, commit, push, open the pull request with the file as its
body, and report in a dozen lines: the rows, the conflict read, what goes stale, the questions for
the owner.

## 6. Apply, once accepted

`/change-request apply CR-NNN`, on the request's branch, and only when the front matter says
`accepted` with `approved_by` and `decided_on` filled by the owner. Then, mechanically:

1. **The registers.** Each `add` row goes into its area's register with `Since: CR-NNN`, `Status:
   active` and the target milestone. Each `amend` row replaces the cell text and sets `Since:
   CR-NNN`. Each `withdraw` sets `Status: withdrawn`. Nothing else in the register changes.
2. **The changelog.** One row in `writ/spec/CHANGELOG.md`: the date, `Touches` naming the request
   and every identifier, one sentence, the cause citing the request.
3. **The index.** `python3 scripts/ledger.py`, then `check`. It refuses an accepted request whose
   rows are not there, so a green check is the proof the request is applied.
4. **The commit**, with `Amends: X-NNN` in its trailer, so `git log --grep` finds it.

Then report: the request now reads *applied* in `writ/INDEX.md`; the identifiers to detail with
`/requirement-detail`; the detail files and scenarios that the check will now ask to be re-read;
and what the slicer should expect to cut.

**Never apply a draft.** A register row saying `Since: CR-NNN` while the request is unaccepted
fails the check, and rightly: the whole track exists so that the owner's yes is what changes the
specification.
