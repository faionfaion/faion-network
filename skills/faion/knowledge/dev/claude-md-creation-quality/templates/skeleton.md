<!--
purpose: Record of how a committed root CLAUDE.md satisfies content/01-core-rules.xml — one section per rule.
consumes: The committed CLAUDE.md and its @-imports, the fresh-clone command run, the secret scan, line-budget and path-existence checks, the reviewer's approval.
produces: A committed record at .product/claude-md-creation-quality/<repo>.md plus its JSON form validated by scripts/validate-claude-md-creation-quality.py.
depends-on: templates/header.yaml, content/02-output-contract.xml, scripts/validate-claude-md-creation-quality.py.
token-budget-impact: ~600 tokens to fill end-to-end.
-->
---
version: 0.1.0
repo: <repo_name>
layout: <layout>
line_budget: <line_budget>
line_count: <line_count>
reviewer: <reviewer_handle>
---

# Root file

- repo: <repo_name>; layout: <layout> (single-package | multi-package)
- line_budget: <line_budget> (declared in the first comment of CLAUDE.md); line_count: <line_count>; within_budget: true
- ci_line_check: true (wc -l fails the build over budget)

# Secrets

- scanner: gitleaks | trufflehog; runs_in_ci: true; runs_in_pre_commit: true; clean: true
- referenced_by_name_only: true (env var or vault item name, never a value)

# Commands

Every invocation verbatim and copy-pasteable; exit 0 on a fresh clone at this commit (r-claude-md-commands-verbatim).

| Invocation | Verbatim | Exit code |
|---|---|---|
| <exact command> | true | 0 |

# Imports

- pasted_repo_content: false

| @path import | Exists | Hop depth (max 5) |
|---|---|---|
| <path> | true | <n> |

# Local scope

- personal_content_in_committed_file: false
- claude_local_md_gitignored: true

# Subdirectory files (multi-package only)

- root_has_per_package_commands: false

| Package | CLAUDE.md path | Exists |
|---|---|---|
| <package> | <subdir>/CLAUDE.md | true |

# Prohibitions

Every never / do-not line states its consequence; emphasis on at most one line in four (r-claude-md-prohibitions-argued).

| Line | Consequence stated | Emphasised |
|---|---|---|
| <never ...: what goes wrong> | true | true \| false |

- emphasis_ratio: <emphasised non-empty lines / non-empty lines, at most 0.25>

# Refs check

- kind: ci-job | pre-commit-hook; location: <path>; all_refs_exist: true

# Reviewer

- reviewer: <reviewer_handle> (named person who approved the PR after the three checks were green)

# Evidence

- <CI run with secret scan, line check and path check>
- <PR URL>
