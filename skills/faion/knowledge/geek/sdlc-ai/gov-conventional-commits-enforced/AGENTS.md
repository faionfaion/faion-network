# Conventional Commits Enforced at the Hook

## Summary

Every repo enforces Conventional Commits 1.0.0 (`feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `perf`, `build`, `ci`, `style`, `revert`; optional scope; optional `!` for breaking; mandatory `BREAKING CHANGE:` footer when `!` is used) via a `commitlint` `commit-msg` hook plus a CI PR-title check. The CHANGELOG, semver bump, and release notes are derived deterministically from the log; agents never freeform commit subjects. Non-conformant messages are rejected at hook time, before they reach the remote.

## Why

AI agents produce many small commits. Without a hard format the log degrades into "updates", "fixes", "wip" within a sprint, and downstream tooling (release-please, semantic-release, conventional-changelog) cannot infer the next version or generate release notes. Conventional Commits gives the LLM a closed grammar with a small enum and a tiny set of footers, which is the format LLMs follow most reliably; commitlint catches the rare miss before push. The result is a deterministic pipeline from commit message to changelog to npm/PyPI release tag.

## When To Use

- Any team repo that produces releases (libraries, services with semver, monorepos with independent package versions).
- Repos where AI agents create commits autonomously and a human curator does not edit every subject line.
- Projects with downstream consumers expecting semver-correct changelogs (npm, PyPI, NuGet, Maven Central, Helm charts).
- Monorepos using `release-please` / `semantic-release` / `changesets` — these tools refuse to operate without conformant messages.

## When NOT To Use

- Single-developer scratch repos and throwaway prototypes — overhead exceeds benefit.
- Mirror / vendored repos where commits are imported verbatim from upstream.
- Migration-in-progress repos where rewriting historical messages is out of scope; turn it on at a fresh tag and skip backfill.
- Repos that intentionally use squash-on-merge with auto-generated subjects from PR titles — gate the PR title instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-grammar-and-hook.xml` | Subject grammar, hook config, allowed types, breaking-change rules. |
| `content/02-changelog-and-release.xml` | Wire commit grammar into release-please / semantic-release; CHANGELOG as a build artifact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/commitlint.config.cjs` | commitlint rule set with extended Conventional Commits and faion-net types. |
| `templates/lefthook.yml` | `commit-msg` hook running commitlint without npx round-trip. |
