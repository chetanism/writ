---
id: <FR-AREA-NN>
area: <FR-AREA>              # the identifier without its number. It is also the directory
status: draft                # draft | reviewed
written_by: <name>
approved_by: ""              # required once status is reviewed
detail_status: <draft>       # what the detail file read when these cases were written
detail_read_on: <2026-09-10> # the day it was read. Both fail the check once the detail file moves
areas: []                    # the parts of the product a tester works in: settings, the queue, sign-in
---

# <FR-AREA-NN> — manual test scenarios

> Written from `canon/process/requirements/<area>/<id>.md` and from nothing else, with
> `/test-scenarios <ID>`. **The detail file says what the requirement means; this says what somebody
> does about it, at a keyboard, on the day.**
>
> **Everything here is done through the product's own screens.** Whoever runs these has a browser
> and an account, and nothing else — no terminal, no database, no access to the server. Where a
> precondition genuinely cannot be reached that way it goes under *Before you start*, addressed to
> whoever sets the environment up.
>
> **Say what to achieve, not what to click.** *Open the list of the organisation's locations* keeps
> working when the button moves; *click Settings, then Locations, then Add* stops being true the
> week somebody rearranges the menu. The screens are not settled and will keep changing for a while
> yet.
>
> Delete this blockquote.

## The requirement

> <the second cell of the requirement's row in `canon/spec/BRD.md`, verbatim — quoted, never
> reworded. `ledger.py check` compares this against the specification character for character, so
> an amendment fails this file until somebody has re-read it>

## Before you start

> What has to be true before any scenario below can run, and **who makes it true**. A tester who
> gets three scenarios in and discovers they needed a second tenant has lost the session.

| What is needed | Who provides it |
|---|---|
| <an account that can do the job, and what it is allowed to do> | <the test manager, from the product's own staff screens> |
| <a second account that must be refused> | <…> |
| <data that has to exist first> | <…> |

**Not through the screen:** <anything on that list that cannot be set up from the product itself,
and why. `None.` is the usual answer and the better one. This is the one place a command belongs,
and it is somebody else's to run — never the tester's.>

## Scenarios

> One heading per scenario, numbered `S1`, `S2`, … in the order somebody would run them. Each one
> stands on its own: a tester picking `S4` out of the middle must be able to run it.
>
> **`Covers`** — the story or the numbered observable in the detail file this came from, so a
> changed requirement can be traced to the cases that go stale with it.
> **`Type`** — one of `happy path`, `negative`, `permission`, `another tenant`, `repeat`,
> `at once`, `boundary`. A file of nothing but happy paths fails the check.
> **`Where`** — the part of the product, named the way a person would say it, never as a link.
> **`Ready`** — `yes`, or `no` and the slice that will make it so.

### S1 — <what somebody is doing, five words>

**Covers** <story 1> · **Type** <happy path> · **Where** <the part of the product> · **Ready** <yes>

**Given** <who is signed in and what already exists — one line, in the tester's terms>

1. <what to do, described as achieving something rather than as pressing a named control>
2. <…>

**Expect** <what the tester should see. It has to be possible to be **wrong** about it: "it works"
is not an expectation, "the location is in the list with every field as it was typed" is.>

### S2 — <the same job, done wrongly>

**Covers** <story 2> · **Type** <negative> · **Where** <the part of the product> · **Ready** <yes>

**Given** <…>

1. <…>

**Expect** <what is refused, and what the person is told. Name what must **not** happen too: a
refusal that half-wrote the record is a defect the expectation has to be able to catch.>

## Not testable yet

> The scenarios above marked `Ready: no`, each with the slice that unblocks it, so this file can be
> run against a later build without being rewritten. `None — all of it can be run today.` is a real
> entry.

| Scenario | Waiting on |
|---|---|
| <S3> | <SL-F4 — the settings area> |

## Related

<The detail file this was written from, the requirement, and the neighbouring scenario files whose
cases a tester will meet while running these. One line each. Never restate what they say.>

## Runs

> One row per time somebody actually ran this file. `pass`, `fail` or `blocked` — and a `fail` names
> the scenario and what happened, because a result nobody can act on is the same as no run at all.

| Date | Build | Result | By | Notes |
|---|---|---|---|---|
