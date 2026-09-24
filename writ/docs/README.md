# Documentation

Seven pages and a skill index. **Read them in this order the first time; afterwards come back to
whichever one matches the question.**

| | Read it when |
|---|---|
| **[Day one](day-one.md)** | The interview just finished and seventy-six files appeared. Which six are yours this week |
| **[A worked example](example/README.md)** | You want to see a filled-in tree and what the tool prints about it, before running anything |
| **[How to use it](using-it.md)** | You are about to run a bootstrap skill, or you have just finished one and are wondering what happens now |
| **[The nineteen skills](skills/README.md)** | You want to know what a specific skill does before you type its name |
| **[Updating a project from writ](updating.md)** | Writ has improved since your project was set up, and you want to pull what fits — on your project's terms |
| **[Contributing back to writ](contributing.md)** | Your project built something other writ projects could use, and you want to offer it back |
| **[Changing the process](changing-the-process.md)** | Something in the process does not fit your team, and you want to know whether you are allowed to change it (you are) and what it costs |
| **[The reference](../README.md)** | You want the full generated tree, the config, the tool's checks, or a switch by name |

Behind all of them sit [`../references/`](../references/) — fourteen documents arguing out each part of
the process, written for whoever changes it next rather than for whoever uses it. You do not need
them to run the process. You will want them the day you disagree with something in it.

## Why the skill pages live here and not beside each skill

A `SKILL.md` is instructions to an agent. These pages are for a person deciding whether to run it.
They are different documents with different readers, and that is the easy half of the reason.

The other half: **the fourteen project skills are emitted tuned to your interview.** Names, gate
commands, stack, cadences and sometimes the skill's own name all differ per project. A generic
README copied into every bootstrapped repository beside a tuned skill would be a second description
of the same thing, immediately less true than the first, maintained by nobody — which is precisely
the failure this process exists to prevent. So the explanations stay with the kit, where there is
one copy and a CI step that fails when a skill has no page or a page names a skill that no longer
exists.

## A reading path for each kind of reader

- **Evaluating it, twenty minutes.** The [root README](../../README.md), then
  [A worked example](example/README.md) — five requirements, three files in, four files out — then
  [How to use it](using-it.md) as far as *The loop*, then
  [`slice-open`](skills/slice-open.md) and [`slice-close`](skills/slice-close.md) to see what a day
  actually looks like.
- **Just finished a bootstrap and the tree looks like a lot.** [Day one](day-one.md). Six files
  matter this week; that page says which, and what the other sixty-three are for.
- **About to bootstrap a new project.** [How to use it](using-it.md) end to end. Have two
  paragraphs about what you are building; that is a sufficient input.
- **Bringing it to a codebase that already exists.** [`adopt`](skills/adopt.md), then
  [`../references/12-survey.md`](../references/12-survey.md) and
  [`../references/13-adoption.md`](../references/13-adoption.md). The adoption ladder in the second
  one is the part that decides whether this survives contact with your colleagues.
- **Already running it and something chafes.** [Changing the process](changing-the-process.md).
