# Contributing back to writ

**Projects improve writ's process by living with it.** A faster tool, a check that caught real
defects, a template that reads better — when one of those would help other writ projects, the
project offers it back. **As an issue, never a pull request:** writ's maintainers decide what to
take and re-derive it in writ's own shape, exactly as a project does in the other direction with
[`/writ:update`](updating.md).

## From a project

```
/writ:contribute
```

It finds what your project has that writ does not, discards your own customisations and anything
writ already has, reads the candidates back for you to choose, builds the case with evidence,
strips everything private, and files the issue only after you have read it.
[`/writ:contribute`](skills/contribute.md) has the detail.

**The issue is public.** The skill removes names, people, hosts, credentials, customer data and
project-only identifiers, and shows you the exact text before filing — read it.

### Without the plugin

Paste this into Claude in your project:

```
I want to offer writ (https://github.com/chetanism/writ) an improvement from this project, as a
GitHub issue — not a pull request. Check writ's CHANGELOG.md and its issues first, so we do not
file something it already has. Help me choose what is general enough, then draft an issue with:
What, Why, Evidence (measurements, defects caught), In the project (paths and short excerpts),
and Suggested shape for writ. Remove every client name, person, hostname, credential, customer
detail and project-only identifier. Show me the exact title and body, and file it with
`gh issue create --label contribution` only when I say yes.
```

## In writ's repository

A maintainer opens a session in writ's repository and runs:

```
/accept-contribution <issue number>
```

It reads the issue as a proposal, checks it against writ's changelog and existing issues, tests the
evidence where it can, and recommends taking it, taking part of it, or declining — then builds only
what the maintainer agrees to: generalised, with tests, every affected document updated, and a
changelog entry carrying `From: #<N>`. The pull request closes the issue, and the issue gets a
comment with the outcome either way.

## The round trip

```
project  --/writ:contribute-->  issue on writ  --/accept-contribution-->  W-NNN in CHANGELOG.md
   ^                                                                              |
   +------------------------------- /writ:update ---------------------------------+
```

The contributing project's next `/writ:update` finds the entry citing its issue and reports it as
already here; every other writ project is offered it like any other enhancement.
