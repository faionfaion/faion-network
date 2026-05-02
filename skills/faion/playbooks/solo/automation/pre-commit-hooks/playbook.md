---
name: pre-commit-hooks
description: Install pre-commit and configure hooks for formatting, linting, whitespace, large-file, and secret detection so bugs are caught before they reach main.
tier: solo
group: automation
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have `pre-commit` installed and a `.pre-commit-config.yaml` wired into your Git repository. On every `git commit`, the hooks will automatically run ruff or Prettier for formatting, ruff or ESLint for linting, trailing-whitespace and large-file checks, and gitleaks for secret detection — blocking the commit if anything fails.

## Prerequisites

- Python 3.9+ installed (`python3 --version`).
- A Git repository initialized (`git init` or cloned).
- For JavaScript/TypeScript hooks: Node 18+ and npm installed.
- For secret detection: internet access to download gitleaks binary on first run (or gitleaks pre-installed at `/usr/local/bin/gitleaks`).
- Familiarity with `git commit` basics (see `git-daily-workflow` playbook).

## Steps

### Install pre-commit

1. Install `pre-commit` into your global Python environment (or project virtualenv):

   ```bash
   pip install pre-commit
   ```

   Verify:

   ```bash
   pre-commit --version
   # pre-commit 3.x.y
   ```

### Create `.pre-commit-config.yaml`

2. Create `.pre-commit-config.yaml` at your repository root. Choose the variant that matches your stack.

   **Python project (ruff formatter + linter + standard checks + gitleaks):**

   ```yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.4.7
       hooks:
         - id: ruff-format
           name: ruff-format (autoformat)
         - id: ruff
           name: ruff (lint + autofix)
           args: [--fix, --exit-non-zero-on-fix]

     - repo: https://github.com/pre-commit/pre-commit-hooks
       rev: v4.6.0
       hooks:
         - id: trailing-whitespace
         - id: end-of-file-fixer
         - id: check-large-files
           args: [--maxkb=500]
         - id: check-merge-conflict
         - id: check-yaml
         - id: check-toml

     - repo: https://github.com/gitleaks/gitleaks
       rev: v8.18.2
       hooks:
         - id: gitleaks
           name: gitleaks (secret detection)
   ```

   **JavaScript / TypeScript project (Prettier + ESLint + standard checks + gitleaks):**

   ```yaml
   repos:
     - repo: https://github.com/pre-commit/mirrors-prettier
       rev: v4.0.0-alpha.8
       hooks:
         - id: prettier
           name: prettier (autoformat)
           additional_dependencies:
             - prettier@3.3.2

     - repo: https://github.com/pre-commit/mirrors-eslint
       rev: v9.6.0
       hooks:
         - id: eslint
           name: eslint (lint)
           files: \.(js|ts|jsx|tsx)$
           additional_dependencies:
             - eslint@9.6.0
             - "@eslint/js@9.6.0"

     - repo: https://github.com/pre-commit/pre-commit-hooks
       rev: v4.6.0
       hooks:
         - id: trailing-whitespace
         - id: end-of-file-fixer
         - id: check-large-files
           args: [--maxkb=500]
         - id: check-merge-conflict
         - id: check-json

     - repo: https://github.com/gitleaks/gitleaks
       rev: v8.18.2
       hooks:
         - id: gitleaks
           name: gitleaks (secret detection)
   ```

   **Mixed Python + JS monorepo:** combine both hook blocks in a single `repos:` list. `pre-commit` runs only hooks whose `files:` pattern matches staged files — Python hooks skip on `.ts` files and vice versa.

### Register the hook with Git

3. Install the hook into `.git/hooks/pre-commit` so Git calls `pre-commit` automatically:

   ```bash
   pre-commit install
   ```

   Expected output:

   ```
   pre-commit installed at .git/hooks/pre-commit
   ```

### Run hooks against all files once

4. Do a full initial run to catch existing issues before the next commit:

   ```bash
   pre-commit run --all-files
   ```

   Hooks may auto-fix some issues (ruff, Prettier). Stage the auto-fixes:

   ```bash
   git add -u
   ```

   Re-run until the output shows all checks passing (no `Failed` lines).

### Commit the config

5. Commit `.pre-commit-config.yaml` to the repository so all contributors get the same hooks:

   ```bash
   git add .pre-commit-config.yaml
   git commit -m "chore: add pre-commit hooks (ruff, checks, gitleaks)"
   ```

## Verify

Run all hooks against the current working tree:

```bash
pre-commit run --all-files
```

Every line in the output should end with `Passed` or `Skipped`. If any line ends with `Failed`, the tool printed the error — fix it and re-run. A clean run looks like:

```
ruff-format (autoformat)....................................Passed
ruff (lint + autofix).......................................Passed
trailing-whitespace.........................................Passed
end-of-file-fixer...........................................Passed
check-large-files...........................................Passed
check-merge-conflict........................................Passed
check-yaml..................................................Passed
gitleaks (secret detection).................................Passed
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `gitleaks` hook exits with `exit code: 1` and prints a findings table | A file staged for commit contains a string that matches a known secret pattern (API key, token, password) | Remove the secret from the file; rotate the credential immediately; use `--baseline-path` if it is a false positive: run `gitleaks detect --report-format json --report-path .gitleaks-baseline.json` and add `args: [--baseline-path=.gitleaks-baseline.json]` to the hook |
| `ruff` exits with `Would reformat` but no changes appear | Hook ran `ruff-format` in check mode instead of write mode | Confirm `ruff-format` hook does NOT have `--check` in `args`; if running in CI use a separate `ruff-format --check` step; locally just let the hook auto-format |
| `pre-commit install` has no effect (hooks not running on commit) | Running `git commit --no-verify` somewhere in scripts or IDE settings | Find and remove `--no-verify` from all commit invocations; this flag silently skips all hooks |
| ESLint hook fails with `Cannot find module 'eslint'` | `additional_dependencies` version not resolved yet | Run `pre-commit clean && pre-commit install` to force a fresh virtualenv build |
| `check-large-files` blocks a binary asset you intentionally need | The 500 KB default is too tight for your project | Increase the threshold: `args: [--maxkb=2048]` or exclude the path: `exclude: ^assets/video/` |
| Hook downloads fail behind a corporate proxy | `pre-commit` and pip both need the proxy | Set `https_proxy` env var or configure `pip.conf` / `.npmrc` with your proxy URL |

## Next

- Wire hooks into CI so the same checks run on pull requests even if a contributor bypasses local hooks — see `github-actions-cicd` playbook.
- Add `detect-secrets` (Yelp) as a second secret-detection layer alongside gitleaks for defence-in-depth: `repo: https://github.com/Yelp/detect-secrets`.
- Explore `commitizen` for enforcing conventional commit messages as a pre-commit hook: `pip install commitizen` and add `cz check --commit-msg-file .git/COMMIT_EDITMSG` to your hooks.

## References

- [knowledge/solo/dev/automation-tooling/best-practices-2026](../../../knowledge/solo/dev/automation-tooling/best-practices-2026) — the hook selection (ruff, gitleaks, standard-checks) and the "run on all files after install" step follow the 2026 automation best-practices checklist for shift-left quality gates.
- [knowledge/solo/dev/automation-tooling/cd-basics](../../../knowledge/solo/dev/automation-tooling/cd-basics) — the pre-commit layer is the first gate in the CD pipeline; this methodology defines where local hooks fit relative to CI checks and why bypassing them (--no-verify) breaks the gate contract.
- [knowledge/free/dev/code-quality/code-review](../../../knowledge/free/dev/code-quality/code-review) — the trailing-whitespace, end-of-file-fixer, and check-merge-conflict hooks automate the low-value mechanical checks from the code review checklist, freeing reviewers for logic and design feedback.
