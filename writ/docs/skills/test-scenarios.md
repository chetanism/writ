# `/test-scenarios`

**Turns one requirement's detail file into manual test scenarios a tester runs through the
product's own screens — read back as a list and cut before anything is written.**

| | |
|---|---|
| **Run it** | Once a requirement's detail file is approved, ahead of the phase that builds it. `/test-scenarios FR-ACC-01` |
| **Produces** | One scenarios file under `writ/qa/scenarios/`, on its own branch |
| **Refuses to** | Reopen what the requirement means, guess, or write a scenario containing a command |

## What it does

1. **One requirement at a time**, refusing the ones outside its configured families.
2. **Reads the detail file and nothing else.** The argument about what the requirement means was had
   in [`/requirement-detail`](requirement-detail.md) and is not reopened here.
3. **Reads the scenarios back as a list, one line each, before writing** — so the test manager can
   cut them while cutting is free.
4. **One round of questions**, and only the ones that change the file.
5. **Writes it**: happy paths, and the ways somebody gets it wrong.

## The two checks that make it real

**A scenario containing a command fails the build.** A test session done through a CLI is not the
session a user has, and the defects it finds are not the defects users hit. If a scenario cannot be
expressed as things somebody does on a screen, it is an automated test wearing the wrong clothes.

**A file with nothing but happy paths fails too.** The ways somebody gets it wrong are the reason a
human is running this at all; the suite already covers the path where everything goes right.

## Why it is a separate document

The detail file is written for whoever builds the thing. The scenarios file is written for whoever
sits at a keyboard and tries to break it, and it is the session they are handed. They need
different content, arrive at different moments, and are cut by different people — the detail file
by the specification's owner, the scenario list by the test manager.

## See also

[`/requirement-detail`](requirement-detail.md) — the only input.
[`/manual-test`](manual-test.md) — the other half of by-hand testing: an unscripted seeded walk,
where this is a written script.
