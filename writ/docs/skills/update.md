# `/writ:update`

**Offers a project that already runs writ's process the enhancements writ has gained since. The
project decides what to take, and everything taken is adapted to the project rather than copied
over it.**

| | |
|---|---|
| **Run it** | In a project bootstrapped or adopted from writ, whenever writ has moved on. `/writ:update` |
| **Produces** | A branch with the chosen enhancements ported in the project's own names and shape, a line each in the project's record of process changes, and a new `writ_baseline` |
| **Refuses to** | Rename the project's tree or identifiers, overwrite a template the project changed on purpose, edit the kit, or turn a check off to make a ported one pass |

## What it does

1. **Finds where the project stands** — its tree's name (`writ/`, `canon/`, …), its `writ_baseline`,
   and what it deliberately switched off.
2. **Reads writ's [`CHANGELOG.md`](../../CHANGELOG.md)** past that baseline. Each entry says what it
   does, why, which files, and what a project usually adapts.
3. **Checks every entry against the project before asking anything**: already here (perhaps in the
   project's own form), not applicable, or worth offering. Speed claims are measured on the project.
4. **Reads the whole picture back as a table**, so you correct its verdicts first.
5. **Interviews you** about each entry worth offering — port it adapted (and exactly how), port it
   as-is, or skip it — and about the choices each needs: thresholds, commands, paths.
6. **Ports what you chose** on a branch: tools with their tests, templates merged rather than
   replaced, each change recorded in the project's process record.
7. **Runs the project's own checks**, sets `writ_baseline` to the newest entry considered, reports
   taken, adapted, skipped and already here, and stops before anything lands.

## Why it is a skill in the kit, not in the project

A skill copied into each project would freeze at the version the project was bootstrapped with,
and projects that predate it would never get it. In the kit, updating the plugin updates the skill,
and every writ project can run it — including ones from before it existed.

## See also

[Updating a project](../updating.md) — the whole flow, and a prompt to paste where the plugin is not
installed.
