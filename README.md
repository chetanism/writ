# writ

**An agent-first development process you can drop into a new project or wrap around an old one.**
Distributed as a Claude Code plugin, through the small marketplace that this repository also
carries — which is why the install is two lines rather than one.

---

## In thirty seconds

**Coding agents broke the old bottleneck and created a new one.** Code is no longer expensive to
write; it is expensive to *understand*, and a project now produces more of it per week than anybody
on it can read. `writ` is the paperwork that keeps a codebase legible at that speed — and every
piece of it is machine-checked, so it cannot quietly rot into decoration.

- **Nothing is taken on trust.** A work order *claims*; a test *proves*. A ledger reads both out of
  the tree and reports only what is backed by evidence — and the build fails when a document and
  the code stop agreeing. This is the part no other kit in this space ships.
- **One command sets it up.** `/writ:solo`, `/writ:team` or `/writ:adopt` interviews you and
  writes the whole tree: specification, registers, slice queue, CI gate, and fifteen skills tuned to
  your answers.
- **Work is done in slices.** One page written before any code, numbered acceptance criteria that
  become test names, and a demo somebody plays by hand.
- **It arrives without blocking anyone.** On an existing codebase every rule starts switched off,
  and you turn them on one directory at a time.
- **It is yours to change.** The process ships with switches, `/process-change` lands a change in
  every file it touches, and [Changing the process](writ/docs/changing-the-process.md) is the
  guide.

```bash
claude plugin marketplace add chetanism/writ
claude plugin install writ@nevic-skills
cd ~/projects/your-project && claude
> /writ:solo          # or /writ:team, or /writ:adopt for an existing codebase
```

**Then read [How to use it](writ/docs/using-it.md).** That is the one page that matters after the
interview finishes. Or, before installing anything, look at
**[a worked example](writ/docs/example/README.md)** — one small product's tree, three files a
person wrote, four the tool generated, every line of it copied out of a real run.

---

## Status

**No project has yet run a full milestone through this.** The mechanics are verified — the tool
carries 158 tests, the templates are bootstrapped and checked on every push, and a CI step fails
when a skill has no documentation page or a link does not resolve. The *process* is argued rather
than measured: the reasoning is written out at length in [`writ/references/`](writ/references/), and
reasoning that survived being written down is still not evidence.

Read the confident tone of these documents as the conviction of an argument, not the report of a
trial. If you run it and something does not survive contact with your team, that is the useful
result — and [Changing the process](writ/docs/changing-the-process.md) is the intended response,
not a workaround.

---

## The longer version

Skip this if the summary above already told you whether you want it.

### The problem it is shaped around

Every mechanism here exists because of one failure, and it is worth naming precisely: **velocity
outrunning comprehension.**

An agent can produce a week of work in an afternoon. It is good work — it compiles, the tests pass,
the pull request is tidy. What it is not is *understood*, by anybody, including the person who
asked for it. Do that for three months and you have a codebase where nobody can answer the
questions that decide whether a change is safe:

- Why is this the way it is? Who decided, and what did they reject?
- What is this module for, and is it even still used?
- What breaks invisibly if I touch this?
- Which of these requirements did anybody actually agree to, and which did we back into?

None of those are answered by reading the code. They were answered once, in somebody's head, in a
conversation nobody wrote down. The traditional answer is documentation, and the traditional
outcome is documentation that is wrong within a month — because writing it is voluntary, and
nothing notices when it stops being true.

### The bet

`writ` makes a specific bet: **documents are worth writing only if something checks them.**

So every document in the tree is one of three things. It is *generated* — the coverage ledger, the
index, the slice queue — and regenerating it is how you find out it drifted. It is *declared* under
a rule a tool can apply — a requirement is a row in a table under a header, and nothing else
counts. Or it is *quoted under a check* — a detail file that quotes its requirement differently
from the register fails the build, character for character.

What is left over is deliberately left to a human: whether the demo was really played, whether the
plan really was read against the invariants, whether a decision was recorded at all. The process
says so out loud rather than pretending otherwise. **The checkable things are checked so that
attention is left over for the things that cannot be.**

### What that buys a developer

| You get | Because |
|---|---|
| An agent that writes the right code first time | It reads a specification, the invariants and the decisions before it plans — not just the files you happened to open |
| A pull request somebody can actually review | The work order says what the change is *for* and what it must not do, before the diff exists |
| An honest answer to "are we done?" | Coverage is derived from tests that exist, never from what a work order claimed |
| Six-months-later context | The decisions, the rejected alternatives and the debt are written where the next reader will look |
| A process you did not have to design | Slicing, sizing, gates, handoffs and the definition of done, already argued out and already wired together |

### What it is not for

The kit argues for itself everywhere else, so here is the other side, stated as plainly: **it is a
bet that the project will outlive anybody's memory of it.** Where there is no six months, it is
overhead with no return. Do not run it on a spike, on a fortnight's work, on a codebase that
already has a process people follow, or on a project whose requirements genuinely are not knowable
yet. [`writ/README.md`](writ/README.md#when-not-to-use-it) says why, at length.

### How it differs from the other spec-driven kits

There are a lot of these now and they are worth knowing about: [GitHub Spec
Kit](https://github.com/github/spec-kit), [OpenSpec](https://github.com/Fission-AI/OpenSpec),
[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD), [Agent
OS](https://buildermethods.com/agent-os), AWS Kiro. Most have far more users than this, and most
will get you to a first specification faster.

**They plan; this verifies.** All of them produce documents for an agent to read. None of them
ships anything that fails a build when a document and the code stop agreeing — and the standing
complaint about all of them is precisely that: specifications drift, and the remedies on offer are
reconciliation commands somebody has to remember to run. A check nobody runs is not a check.

The other half of this — requirements in version control, identifiers tagged in source, a build
that goes red on broken coverage — is not new either. It is what
[OpenFastTrace](https://github.com/itsallcode/openfasttrace),
[Doorstop](https://github.com/doorstop-dev/doorstop) and
[StrictDoc](https://github.com/strictdoc-project/strictdoc) have done for years, for avionics and
medical software. What none of them has is any notion of an agent.

| | Gives you | Does not |
|---|---|---|
| Spec Kit, OpenSpec, BMAD, Kiro, Agent OS | A workflow agents follow, and documents to follow it with | Notice when the documents stop being true |
| OpenFastTrace, Doorstop, StrictDoc | A build that fails on broken traceability | Know that agents exist; they are aimed at DO-178C, not at Claude |
| `writ` | Both halves, in one tree | Have any users yet — see [Status](#status) |

Where the others are plainly stronger: Spec Kit has GitHub's brand, the largest community and
support for many more agent harnesses; OpenSpec is lighter than this and brownfield-first by
design; Agent OS mines conventions out of an existing codebase better than the survey here does;
BMAD covers team roles this has no opinion about. **If what you want is a specification workflow
rather than an audit trail, take one of those.** This one is for the case where somebody is going
to ask which test proves a requirement, and a plausible answer will not do.

**On harness portability.** The fifteen skills are Claude Code — and they are the only part that
is. The tree is Markdown, the tool is one stdlib-only Python file with no dependencies, and the
gate is a GitHub Actions workflow. All three work with any agent, or with none at all. A team on a
different harness keeps the whole process and rewrites the skills, which is an afternoon rather
than a migration; `context_budget.files` in the config already takes `AGENTS.md` instead of, or
alongside, `CLAUDE.md`.

---

## Where everything is

| | |
|---|---|
| **[How to use it](writ/docs/using-it.md)** | Running a bootstrap skill, then living in the loop — and what each step buys you |
| **[Updating a project from writ](writ/docs/updating.md)** | Writ keeps improving. `/writ:update` offers what it gained since your project was set up, and ports only what you choose, adapted to your project |
| **[Contributing back to writ](writ/docs/contributing.md)** | Built something other writ projects could use? `/writ:contribute` files it as an issue for writ's maintainers to consider — never a pull request |
| **[Changing the process](writ/docs/changing-the-process.md)** | It is not a static library. How to reshape it by talking to your agent, and which three parts not to touch |
| **[The twenty skills](writ/docs/skills/README.md)** | One page each: what it does, when to run it, what it refuses to do |
| **[Getting the most out of it](writ/docs/using-it.md#getting-the-most-out-of-it)** | The habits that separate a project running this well from one running it as ceremony |
| **[`writ/README.md`](writ/README.md)** | The reference: the full generated tree, the four mechanisms, the tool, every adaptation switch |
| **[A worked example](writ/docs/example/README.md)** | A filled-in tree and what the tool prints about it — the shortest way to see whether you want this |
| **[Day one](writ/docs/day-one.md)** | Seventy-five files arrived. The six that are yours this week, and what the rest are for |
| **[`writ/references/`](writ/references/)** | The reasoning behind each part, written for whoever changes it next |

## Contributing to the kit itself

The kit has its own gate, which it did not have until four blocking defects reached `main` at once:

```bash
python3 writ/templates/scripts/test_ledger.py    # the tool
python3 writ/templates/scripts/test_survey.py    # the survey tool
python3 writ/tests/test_templates.py             # the documents the kit ships
python3 writ/tests/build_example.py --check      # the worked example still matches the tool
```

`.github/workflows/kit.yml` runs those plus manifest, front-matter and documentation-link checks on
every push. Run them before every change to `writ/templates/`.

## Licence

MIT — see [`LICENSE`](LICENSE), and as declared in
[`writ/.claude-plugin/plugin.json`](writ/.claude-plugin/plugin.json).
