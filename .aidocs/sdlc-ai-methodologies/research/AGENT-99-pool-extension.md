# AGENT-99 — Pool Extension (lint- discovery)

Append-only log of fresh candidates discovered during pool-batch loops when AGENT-06 thinned out.

## Discovered 2026-04-26 — lint- additions

### EXT-L1 — `lint-shellcheck-hadolint-iac-floor` — Infrastructure-as-Code Lint Floor

**Category:** lint-

**Rule:** Every repo with shell scripts, Dockerfiles, Compose files, GitHub Actions workflows, Kubernetes manifests, Terraform, or YAML configuration MUST run a per-format infrastructure linter at the same hook tier as code linters: `shellcheck` for `*.sh` and shebang-bash files, `hadolint` for any `Dockerfile*`, `yamllint` (with the `relaxed` profile or stricter) for `.yaml`/`.yml`, `actionlint` for `.github/workflows/`, `tflint` plus `terraform validate` for HCL. Findings block at the same level as code lint findings.

**Why it works:** App-code linters (ruff, biome) only see code. Production outages frequently land via shell quoting bugs (CVE-2014-6271 Shellshock pattern), Dockerfile rootful images (`USER` missing, latest tag, multistage missed), Compose port leaks, Actions workflow privilege escalation (`pull_request_target` mis-use), Terraform drift. shellcheck is the de-facto shell static analyzer (Haskell, MIT) — `bashate` and others have been superseded. hadolint is the Dockerfile equivalent — a Haskell parser that codifies Docker best-practices. yamllint guards spec-compliant YAML formatting (a frequent CI break source). actionlint is the GitHub-published linter for workflow YAML and shell-in-`run:` blocks. tflint adds provider-aware Terraform rules on top of `terraform validate`.

**When to use:** Always. Every repo has at least one Dockerfile/CI workflow/shell script.
**When NOT to use:** Pure Markdown docs repos with no IaC.

**Agent integration:**
- pre-commit + CI both run the IaC linter set; fails are blocking.
- `actionlint` runs on `.github/workflows/**` only — a cheap one-liner that prevents most "works on my fork" surprises.
- Dockerfile findings: agents prefer rule-flagged fixes (`DL3008` pin apt versions, `DL3015` `--no-install-recommends`) over `# hadolint disable`.

**Sources:**
- https://github.com/koalaman/shellcheck
- https://github.com/hadolint/hadolint
- https://github.com/adrienverge/yamllint
- https://github.com/rhysd/actionlint
- https://github.com/terraform-linters/tflint

---

### EXT-L2 — `lint-staged-only-not-whole-tree` — Pre-Commit Linters MUST Run on Staged-Only Diffs

**Category:** lint-

**Rule:** Every linter and formatter wired into a pre-commit hook MUST receive ONLY the staged file set, not the whole tree. Use `pre-commit`'s default behavior (passes file list as args), `lefthook`'s `{staged_files}` template, or `lint-staged` for husky setups. NEVER call `npx eslint .`, `ruff check .`, `biome check .` from a pre-commit hook — those reformat unrelated files, balloon the diff and turn the hook into a 30-second blocker so developers reach for `--no-verify`. CI may run whole-tree once per PR for a final gate.

**Why it works:** A 1500-file monorepo with `eslint .` per commit yields 12-second hooks; the same hook on staged files (3 files) yields 200ms. The lint-staged maintainers report this is the single biggest reason teams turn off husky entirely. The `pre-commit` framework defaults to passing file arguments so most hook authors get this right; the failure mode is when someone wraps a custom command and forgets to forward `$@`.

**When to use:** Always. Even single-file-edit tools like `prettier --write` MUST be scoped to staged files in the pre-commit hook.
**When NOT to use:** CI's final pre-merge gate runs whole-tree to catch drift introduced by partial-stage workflows.

**Agent integration:**
- Agents NEVER add a hook that calls `<tool> .` — they always wire the staged-files token from the framework.
- Agents stage `git add -p` carefully when they touched many files; staged hunks define the lint scope.
- A single "fixed file" hook (e.g., ruff `--fix`) has `pass_filenames: true` so the autofix is scoped.

**Sources:**
- https://pre-commit.com/#filtering-files-with-types-and-files
- https://github.com/lint-staged/lint-staged
- https://github.com/evilmartians/lefthook#staged_files
- https://www.pkgpulse.com/blog/husky-vs-lefthook-vs-lint-staged-git-hooks-nodejs-2026
