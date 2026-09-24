# Day one

**Seventy-six files land in your repository. Six of them are yours this week; the other seventy
are infrastructure, blank registers, or things you invoke rather than read.** Nothing here asks you
to read the process document front to back — that is what the agent does.

If the tree looked like a lot when the interview finished, this page is the triage.

---

## The six

| File | You | What it is |
|---|---|---|
| `CLAUDE.md` | read once | The map the agent loads every session. If it is wrong, everything downstream is wrong. |
| `writ/spec/BRD.md` | **write** | What you are building, in prose, for a person. The interview drafts it; you fix it. |
| `writ/spec/requirements/*/index.md` | **write** | The registers. A requirement exists because it is a row in one of these tables and for no other reason. |
| `writ/process/work-orders/…/NNN.md` | **write, per slice** | One page before any code: why the slice exists, what it decides, numbered acceptance criteria. `/slice-open` drafts it. |
| `writ/process/SLICE-QUEUE.md` | read | What is next, ordered from the dependencies in work-order front matter. Generated — do not edit it. |
| `writ/process/COVERAGE.md` | read | Whether you are actually done. Generated — do not edit it. |

Two of the six are generated, which is the point: the two documents you would most want to trust
are the two nobody is allowed to write by hand. See [a worked example](example/README.md) for what
they look like filled in.

**The two commands that matter this week** are `/slice-open` and `/slice-close`. Everything else
can wait until you hit the situation it exists for.

---

## The other seventy

| How many | Where | What to do about it |
|--:|---|---|
| 24 | `.claude/skills/` | **Never read these.** They are instructions to an agent. You type `/slice-open`; the file is how it knows what that means. |
| 20 | `writ/spec/` | The registers: risks, assumptions, open questions, debt, out-of-scope, personas, dependencies, compliance, the glossary. **Most start empty and staying empty is a valid state.** Each exists so that when you do need to write a risk down, there is exactly one place it goes. |
| 6 | `writ/process/templates/` | Copied by skills when they need them. You will never open one. |
| 7 | `writ/process/` | The process document and why its definition of done is shaped as it is, the manual regression script, the queue, and the work-order tree. Read `DEVELOPMENT-PROCESS.md` when you disagree with something, not before. |
| 9 | `scripts/` | The traceability tool, the velocity report, the falsification runner and their tests. Stdlib-only Python, no dependencies. |
| 3 | `writ/maintenance/` | Backlogs the standing passes reconcile — cleanup, security, audits. Empty until `/cleanup` or `/security-audit` runs. |
| 2 | `.github/workflows/` | The gate and the traceability check. Wired up already; the only thing you may need to fill in is your stack's install and test commands. |
| 1 | `.claude/settings.json` | Switches off the agent's co-author trailer and session link. Leave it. |
| 2 | `writ/decisions/` | Where ADRs go. Empty until you reject an alternative worth remembering. |
| 1 | `writ/qa/` | Manual test scenarios, if you run that track. |

---

## What the first week actually looks like

1. **Read `CLAUDE.md`**, and fix anything the interview got wrong about your project. Five minutes,
   and it is the highest-leverage five minutes in the whole process.
2. **Fix the BRD and the registers.** The interview drafted requirements from two paragraphs you
   gave it. Some are wrong. This is the step where spending judgement pays, and the only one where
   nobody can do it for you.
3. **`/slice-open`** on the first row of the queue. Argue with the work order before any code
   exists — that is the cheapest moment to change your mind about anything.
4. **Build it,** with the agent, against acceptance criteria that become test names.
5. **`/slice-close`.** The ledger regenerates, and `COVERAGE.md` tells you what you actually
   proved rather than what the work order claimed.
6. **`python3 scripts/ledger.py stats`** at the end of the week. It never fails a build; it just
   tells you where you are.

Then repeat. Everything else in this kit — the requirement detail track, manual scenarios, the
security pass, change requests, product docs — is a thing you turn on when you feel its absence,
and [Changing the process](changing-the-process.md) is how you turn any of it off.

---

Next: [How to use it](using-it.md) for the loop in full, or
[a worked example](example/README.md) to see the artefacts before you make your own.
