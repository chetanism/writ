# Updating a project from writ

**Writ keeps improving, and your project has kept changing since it was bootstrapped. Pulling
enhancements is a conversation, not a sync:** your project's Claude reads what writ has gained,
checks each against what your project already has, asks you which to take, and ports only those —
adapted to your project's names, commands and conventions.

Your project stays in charge. Nothing is renamed to match writ, nothing you changed on purpose is
overwritten, and taking none of it is a perfectly good outcome.

## With the plugin installed

Update the plugin, then in your project:

```
/writ:update
```

It finds your baseline, reads writ's changelog past it, checks each entry against your tree, shows
you the whole picture as a table, and asks about the ones worth offering. [`/writ:update`](skills/update.md)
has the detail.

## Without the plugin

Paste this into Claude in your project, with the path to a checkout of writ:

```
Writ's enhancements since this project was set up are in <path to writ>/writ/CHANGELOG.md,
newest first. Our baseline is `writ_baseline` in scripts/ledger.config.json — if it is missing,
consider every entry after W-000.

For each entry past the baseline, check our own files first and tell me whether it is already
here (and where), not applicable (and why — measure any speed claim on this repo), or worth
offering. Show me that as one table before asking anything.

Then ask me about the ones worth offering, a few at a time: port it adapted to this project
(say exactly how), port it as writ ships it, or skip it — with your recommendation and why.

Port only what I choose, on a branch. Keep our tree's name, our identifiers and our versions of
templates and skills — merge the missing piece into them rather than replacing them. Bring tests
with any tool. Record each change where we record process changes. Run our checks, set
writ_baseline to the newest entry considered, report taken / adapted / skipped / already here,
and stop before committing.
```

## What your project keeps

- **`writ_baseline`** in `scripts/ledger.config.json` — the last changelog entry the project has
  considered, whether it took it or not. Skipped entries are not offered again.
- **A line per change** in the project's record of process changes, so the next person reads *we
  chose this* rather than wondering where a rule came from.

## For writ's maintainers

Every change to what writ emits gets an entry in [`CHANGELOG.md`](../CHANGELOG.md) in the same
commit, written for a project deciding whether it wants it: what, why, the files, what to adapt.
The template's `writ_baseline` moves to the new entry — a new project already has it — and
`tests/test_templates.py` fails if the two disagree.

When a project reports back what it took and what writ got wrong for it, that report is the best
input writ gets.
