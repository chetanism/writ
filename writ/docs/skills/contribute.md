# `/writ:contribute`

**Offers writ something your project built that other writ projects could use — as a GitHub issue
on writ's repository, never a pull request. You read the exact text before anything is filed.**

| | |
|---|---|
| **Run it** | In a writ project, when you have improved the process in a way worth sharing. `/writ:contribute` |
| **Produces** | An issue on writ's repository in the shape of a changelog entry — what, why, evidence, the files, a suggested shape for writ — or a comment with your evidence on an issue that already exists |
| **Refuses to** | Open a pull request, push code, attach whole files, or file anything you have not read in full |

## What it does

1. **Finds what your project has that writ does not** — from your record of process changes, the
   history of your process files, and where your files differ from writ's templates.
2. **Discards what is not a contribution**: your own customisations (commands, names, thresholds),
   anything writ's changelog already has, anything writ's issues already carry.
3. **Reads the candidates back as a table** with its honest read of each — general, general with
   changes, or project-specific — and you choose.
4. **Builds the case** for each: the evidence, what writ would have to change, whether to name your
   project (by default it does not).
5. **Drafts the issue and strips everything private** — names, people, hosts, credentials, customer
   data, identifiers that only mean something inside your project.
6. **Shows you the exact text, and files it only on your yes.** Without `gh`, it hands you the text
   to paste.

## What happens next

A writ maintainer runs `accept-contribution` on the issue in writ's own repository. It is checked
against what writ already has, the evidence is tested where it can be, and what is taken is
re-derived in writ's shape — generalised, with tests and a changelog entry citing your issue. The
issue gets a comment with the outcome either way. Your next [`/writ:update`](update.md) reports the
entry as already here.

## See also

[Contributing back to writ](../contributing.md) — the whole round trip.
