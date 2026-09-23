---
name: update
description: Offer a project that already runs writ's process the enhancements writ has gained since — read the kit's changelog past the project's baseline, check each entry against what the project already has, interview the user on which to take and how to adapt them, then port only those, in the project's own names and shape. Use when the user asks to update, sync or pull enhancements from writ into a project bootstrapped or adopted from it.
disable-model-invocation: true
---

# Writ — update

You are in a project that got its process from writ some time ago and has lived with it since. Writ
has changed; so has the project. Your job is to **offer** the project what writ learned, and port
what the project decides it wants — **adapted to the project, never copied over it.**

**The project is in charge.** Its tree, its names, its own versions of the templates and skills,
and every divergence it made on purpose are the ground truth. Writ is a source of ideas with working
code attached, not an upstream the project has to track. Taking none of it is a good outcome.

**The kit root is `${CLAUDE_PLUGIN_ROOT}`**, exactly as in `/writ:solo`: `CHANGELOG.md`,
`templates/…` and `references/…` below are read from there. If the variable is not set, the kit
root is two directories above this file.

Load `references/00-interview.md` now; it governs every question below.

## 1. Find where the project stands

Read, and say in three lines what you found:

- **The tree's name.** The `registry` path in `scripts/ledger.config.json` names it — `writ/`,
  `canon/`, `docs/`. **Every `writ/…` path in the kit means that tree here.** Never rename the
  project's tree, its skills or its identifier families to match writ.
- **The baseline.** `writ_baseline` in `scripts/ledger.config.json` is the last changelog entry the
  project has already considered. With no key, the project predates the changelog: offer every
  entry after `W-000`, and expect the survey in step 3 to find much of it already there.
- **The project's own record of process changes** — `DEVELOPMENT-PROCESS.md` §15 or whatever the
  project calls it, and its `CLAUDE.md`. Something the project deliberately switched off is not
  offered back as though it were missing.

If `scripts/ledger.config.json` does not exist, this is not a writ project: stop and say so.

## 2. Read what writ has gained

Read the kit's `CHANGELOG.md` from the newest entry down to the baseline. Each entry says what,
why, the files it touches in the emitted tree, and what a project usually has to adapt.

Where an entry cites a commit and the kit root is a git repository, `git -C <kit root> show <sha>`
gives the full change. Read it when the entry alone does not tell you what the files look like —
not by default.

## 3. Check every entry against the project, before asking anything

**Never ask what you can read.** For each entry, open the project's versions of the files it names
and decide which of these it is:

| Verdict | Means | Evidence to cite |
|---|---|---|
| **Already here** | The project has it, possibly in its own form | The file and line where it lives |
| **Not applicable** | The project's shape makes it moot — a stack it does not use, a rule it switched off, globs that never had the problem | The config key or record entry that says so; a measurement where it is a speed claim |
| **Worth offering** | Missing, and it could help here | What in the project it would change |

An entry with a `From:` line that names an issue this project filed is **already here** — it came
from this project — unless the project wants writ's generalised version in place of its own.

A speed claim is measured on this project before it is offered, where a measurement takes under a
minute. Writ's gain is on writ's example; this project's tree decides whether there is one here.

## 4. Read back, then interview

**First, the whole picture in one table** — every entry, its verdict, one line of evidence. The
user corrects the verdicts before any question about the offered ones: a wrong *already here* is
the cheapest mistake to catch now and the most expensive to find later.

Then ask about the **worth offering** entries, in rounds of at most four, in the shape of the
project's `CLAUDE.md` §*Asking me to decide* (or `references/00-interview.md` where the project has
none). For each entry:

```
3. W-008 — falsification by tool. You falsify by hand today (/slice-close §2a); the tool runs
   only the tests tagged with each control's requirement and restores the file even on Ctrl-C.
   a. Port it, adapted (recommended) — runners set to vitest per package, the plan beside the
      summary, and §2a rewritten to use it.
   b. Port it as writ ships it — the same, with writ's paths; you rename later.
   c. Skip it — it will not be offered again.
```

- **Say what adapting means for this project**, concretely: the names, commands, paths and
  conventions you would change. *"Adapted"* with no detail is not an option anybody can judge.
- **Ask how they want it customised** wherever the entry's *Adapt* line names a choice the project
  has to make — thresholds, runners, what is generated here.
- **A user can answer for a group** — *"skip everything about CI"* — and you apply it.

Stop asking when every offered entry has a decision.

## 5. Port what was chosen, in the project's shape

On a branch, named and landed the way the project's `CLAUDE.md` §Git says.

- **Adapt, do not transplant.** Rename paths to the project's tree, fit the project's commands,
  keep its section numbering and voice, and merge into its version of a template or skill rather
  than replacing the file. Where the project's version is thinner or stricter than writ's, the
  project's wins and you port only the missing piece.
- **Code arrives with its tests.** A ported tool brings its test file, adapted, and it passes before
  anything else is touched.
- **A process change is recorded** where the project records them (§15), one line per entry taken
  or adapted, saying what and why — so the next person reads *we chose this*.
- **Never** edit the kit, rename the project's tree, re-number its identifiers, or switch a check
  off to make a ported one pass. A ported check that fails on the project's existing documents is
  a finding: fix the documents if they are wrong, or say so and ask.

## 6. Verify

Run the project's own checks: `python3 scripts/ledger.py check`, the tests of anything ported, and
the project's gate command where code changed. Report what ran and what it said.

## 7. Record the baseline, report, stop

Set `writ_baseline` in `scripts/ledger.config.json` to the **newest entry considered** — taken,
adapted or skipped — so skipped entries are not offered again. Add the key if it was missing.

Report, one line per entry: **taken**, **adapted** (and how), **skipped** (and why), or **already
here** — plus anything you think writ got wrong for this project. Writ's maintainers read that; a
finding that writ's version was wrong is as useful as a port.

Then stop. How the branch lands — pull request, review, merge — is the project's, and you ask
rather than assume.
