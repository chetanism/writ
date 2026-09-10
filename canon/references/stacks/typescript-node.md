# TypeScript / Node

The recipe from the project this kit was extracted from. Every line is a decision that was made
once and then relied on; adopt the ones that fit and record the departures.

## Gate roles

| Role | Command |
|---|---|
| format | `pnpm fmt:check` |
| static analysis | `pnpm lint` (type-aware, `--deny-warnings`) |
| types | `pnpm typecheck` |
| unit | `pnpm test` — held to ten seconds |
| integration | `pnpm test:all` — needs the stack up |
| contract | `pnpm openapi --check` |
| traceability | `python3 scripts/ledger.py check` |

`pnpm gate` runs format, lint, typecheck and unit; CI runs them as separate steps so a red cross
names the thing that broke, then brings the stack up and runs `test:all`.

## Workspace

- **pnpm workspaces + Turborepo.** `apps/*` are deployables, `packages/*` are libraries,
  `tooling/*` is neither and is exempt from the rules that bind deployables.
- **Lint and format run once from the root; typecheck and test fan out per package.**
- **A package resolves a sibling by name** (`@scope/domain`), never by a relative path across a
  package boundary.
- **A stub package carries no `tsconfig.json` and no scripts.** The slice that gives it source adds
  both; until then Turborepo has nothing to run and skips it.
- `engine-strict=true` in `.npmrc` plus `.nvmrc`, so an unsupported Node refuses to install rather
  than warning.

## Language

- `"type": "module"` everywhere, and an `exports` map with no `require` condition. Node accepts
  `require()` of ESM from 22 onward, so *"is it ESM"* is not testable by a failing `require` —
  it is enforced by the manifest, not by a test.
- TypeScript strict. `NodeNext` resolution, which means a `.js` specifier for a `.ts` source file.
- Node's type stripping runs a CLI straight from `.ts` with no build step — at the price of no
  enums, no parameter properties, no `namespace`. **That restriction is transitive**: it binds
  every package the CLI imports at runtime.

## Tools, pinned exactly

`oxlint` and `oxfmt`, both without a caret. A formatter that changes its mind in a patch release
turns every later diff into noise.

Two lint rules do process work, and both carry their rationale in the message:

```jsonc
"no-restricted-imports": ["error", { "paths": [{
  "name": "@scope/queue",
  "message": "Side effects are written to `outbox` in the same transaction as the domain row and drained by the dispatcher. `queue.add()` in a handler is the message-loss window the outbox exists to close."
}]}],
"node/no-process-env": "error"
```

The `no-process-env` override list names the one module allowed to read the environment. **Treat
the length of that list as governed**: adding a third entry is a decision, not a convenience.

`oxfmt` does not touch Markdown, and generated artefacts sit in `ignorePatterns` — a formatter and
a generator writing the same file disagree about it forever.

## Tests

One shared config, re-exported per package:

```ts
// vitest.shared.ts
export const unitConfig = defineConfig({ test: {
  name: 'unit', include: ['src/**/*.test.ts'], exclude: ['**/*.integration.test.ts'] } });
export const integrationConfig = defineConfig({ test: {
  name: 'integration', fileParallelism: false, include: ['src/**/*.integration.test.ts'] } });
```

```ts
// packages/db/vitest.config.ts
export { unitConfig as default } from '../../vitest.shared.js';
```

Split by **filename suffix**, so a test sits beside its source. `globals: false` — import what you
use.

Ledger configuration:

```json
"tests": {
  "globs": ["apps/*/src/**/*.test.ts", "packages/*/src/**/*.test.ts", "tooling/*/src/**/*.test.ts"],
  "exclude": ["**/node_modules/**", "**/dist/**"],
  "annotation": "(?:it|test|describe)[^\\n]*?['\"`]\\[(?P<id>[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9.]+)+)\\]\\s*(?P<proof>[^'\"`]*)"
}
```

That stricter pattern only credits a real test declaration, which is worth having where the
convention is uniform.

## Database, if there is one

- **Postgres, with row-level security if there is a tenancy invariant.** Isolation enforced at the
  data layer beats isolation by application convention, which fails silently the first time
  somebody writes a new query.
- `FORCE ROW LEVEL SECURITY`, and **three roles**: one that owns and migrates, one with DML and no
  DDL and `rolbypassrls = false`, and one for retention that owns nothing.
- **Generate the policy from the table's declaration, never write it.** A per-table hand-written
  policy is where the isolation bug hides.
- Under transaction pooling a plain `SET` leaks to the next client — **tenant context is always
  `SET LOCAL`, inside the transaction that reads it**, written as `set_config(name, value, true)`
  because `SET` takes no bind parameters.
- Migrations over the direct connection, never the pooled one, holding a session advisory lock.
- **Do not export the raw client.** One function that opens a transaction, sets the context, and
  hands out a scoped handle is the only query surface; a query issued without it should raise.

## HTTP, if there is any

- **Schemas defined once and derived** into runtime validation, static types, and the OpenAPI
  document. Fastify with a Zod type provider does this; so do several others.
- **A route is a value**, and one function is the only path to registering it — then an endpoint
  absent from the contract is not expressible, and a declared-but-unregistered route fails at boot
  rather than 404ing in a demo three slices later.
- **Parse the response on the way out.** A field the contract does not name should not be able to
  reach a client.
- **A request schema is strict.** Zod strips unknown keys by default, which is exactly how a
  privilege-escalation attempt looks like success.
- **The correlation id is minted at ingress and never taken from the client.** A client-supplied
  header is recorded under a different name.
- Commit the generated OpenAPI document and validate the *file* in CI.

## The dev CLI

Fifty lines and no framework: a `Command` interface of `summary`, `usage`, `run(args)`, and one
registry object. `--help` is generated from the registry and dispatch reads from it — a registry, a
help text and a dispatch switch are three lists that drift.

**A verb a demo script needs takes `--json`** and prints exactly one object, so `jq -r` puts an
identifier into a shell variable. That is what makes a demo script copy-pasteable.
