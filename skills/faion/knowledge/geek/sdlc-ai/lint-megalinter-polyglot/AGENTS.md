# MegaLinter as the Polyglot Quality Umbrella in CI

## Summary

Polyglot repositories (three or more languages, e.g., Python + TypeScript + Terraform + Markdown) MUST run `MegaLinter` in CI as a single GitHub Action or GitLab job. MegaLinter auto-detects the languages present, dispatches 100+ underlying linters in parallel via Python multiprocessing, and emits a unified SARIF report so the agent and the security UI both consume one feed. Pick a flavor (`security`, `python`, `javascript`, `terraform`, `dotnet`, `cupcake`) to keep the runner image lean. MegaLinter MUST NOT run as a pre-commit hook — its image is too heavy for the local commit lifecycle; reserve it for CI and let per-language tools (ruff, biome) cover the local hook floor.

## Why

MegaLinter (oxsecurity, fork of GitHub Super-Linter) is the only one-call surface that covers 69 languages, 23 formats and 21 tooling formats — ESLint, ruff, hadolint, terraform fmt, ansible-lint, yamllint, markdownlint, shellcheck, golangci-lint, rubocop, php-cs-fixer, sql-lint, dotenv-linter, and more in one shot. The parallel Python multiprocessing engine is meaningfully faster than Super-Linter's sequential bash and produces SARIF that drops directly into GitHub Code Scanning's UI. The "one umbrella in CI, one native tool per language at the hook" split prevents the well-known anti-pattern of running MegaLinter locally (multi-gigabyte Docker pull on every commit) while still giving the agent a unified CI feed to fix from.

## When To Use

- Polyglot repositories with three or more languages or stack zones (Python + TS + Terraform + Markdown is the canonical example).
- Monorepos where each package may use different linters and a single CI job is simpler than per-language workflow shards.
- Repositories that need uniform SARIF output for GitHub Advanced Security or GitLab UltimateSecurity.
- Quarterly hygiene scans that want every linter in one report without per-tool maintenance.

## When NOT To Use

- Single-language repositories — ruff (Python), biome (JS/TS), or golangci-lint (Go) cover the same ground with sub-second startup; MegaLinter's image overhead dwarfs the value.
- Local pre-commit hooks — MegaLinter's image is multi-gigabyte and adds tens of seconds of pull/start time, breaking the sub-second hook contract.
- Throwaway prototype repos with one or two files of code — install ruff or biome and stop.

## Content

| File | What's inside |
|------|---------------|
| `content/01-ci-only-rule.xml` | The "MegaLinter belongs in CI, not in pre-commit" rule and the SARIF-as-uniform-feed contract. |
| `content/02-flavor-selection.xml` | How to pick a MegaLinter flavor based on the repo's stack so the image stays lean. |

## Templates

| File | Purpose |
|------|---------|
| `templates/.mega-linter.yml` | Repo-root MegaLinter config selecting a flavor and SARIF output. |
| `templates/megalinter-action.yml` | GitHub Actions workflow snippet wiring MegaLinter into PR + push with SARIF upload. |
