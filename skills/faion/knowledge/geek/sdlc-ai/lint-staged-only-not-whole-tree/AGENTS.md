# Pre-Commit Linters MUST Run on Staged Files Only

## Summary

Every linter and formatter wired into a pre-commit hook MUST receive ONLY the staged file set, not the whole repository tree. Use `pre-commit`'s default `pass_filenames: true` (the framework already passes the staged list as args), `lefthook`'s `{staged_files}` template, or `lint-staged` for husky setups. NEVER call `eslint .`, `ruff check .`, `biome check .`, `prettier --write .`, or `mypy .` from a pre-commit hook — those rewrite or report on unrelated files, balloon the diff, drag the hook above one second, and push developers and agents toward `--no-verify`. CI runs the whole-tree variant exactly once per PR as the final pre-merge gate.

## Why

Hook latency is the single strongest predictor of bypass behaviour. Lint-staged's maintainers and lefthook's benchmarks show whole-tree hooks on a 1500-file monorepo cost 8–12 seconds per commit while staged-only on 3 files runs in 200ms — the same hook becomes either an invisible floor or a hated blocker depending on this one switch. A whole-tree formatter on a partial-stage commit also rewrites unrelated code that the developer did NOT stage, leaking it into the next commit and breaking `git blame`. The pre-commit framework, lefthook and lint-staged were all designed around this distinction; using them and then bypassing the staged-list is a self-inflicted wound.

## When To Use

- Always — every pre-commit hook in every framework MUST be staged-scoped.
- Especially in monorepos where any hook will encounter thousands of files.
- When wrapping a custom command in a `local` hook (forwarding `$@` is mandatory).
- When migrating a husky setup off `npm run lint` invocations toward `lint-staged`.

## When NOT To Use

- The CI pre-merge gate — that runs whole-tree by design as the final defense.
- One-off "format the entire repo" maintenance commits scheduled as their own PR — these run outside the hook.
- Tools that fundamentally need the whole project graph (e.g., `tsc -p`) — these MAY run scoped to a project but never to a single file; use a separate hook with `pass_filenames: false`.

## Content

| File | What's inside |
|------|---------------|
| `content/01-staged-scope-rule.xml` | The staged-only rule, framework-specific incantations, and the latency budget that justifies it. |
| `content/02-graph-aware-tools-exception.xml` | The narrow exception for project-graph-aware tools (`tsc`, `mypy --strict`, `cargo check`) and how to scope them without going whole-tree. |

## Templates

| File | Purpose |
|------|---------|
| `templates/lint-staged.config.js` | `lint-staged` config wiring biome, prettier, eslint, ruff, mypy with file-glob scoping. |
| `templates/lefthook-staged.yml` | `lefthook` pre-commit using `{staged_files}` and `glob:` filters per language. |
