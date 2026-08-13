# GitHub Repo Bootstrap

## Summary

**One-sentence:** Emits an idempotent bash script that creates / configures a GitHub repo with sensible defaults via gh CLI in under 20 commands.

**One-paragraph:** Bootstrapping a repo by clicking through the GitHub UI is slow, error-prone, and unauditable. This methodology emits a single idempotent bootstrap script using `gh` CLI: creates the repo, sets visibility, license, default branch, applies branch protection (≥1 reviewer + CI required + no force-push), wires Dependabot, drops CI workflow scaffolding (lint + test), adds issue / PR templates, sets required secrets, and switches merge mode to squash-only. Re-running is safe.

**Ефективно для:**

- Net-new репо: 20-команд скрипт замість 30 кліків в UI.
- Шаблон для starter-kit (10 faion-starters): один bootstrap.sh адаптується.
- Org-wide hygiene audit: запустити bootstrap.sh у dry-run для перевірки drift.
- Disaster recovery: restore repo from scratch with all settings intact.

## Applies If (ALL must hold)

- GitHub is the target platform.
- `gh` CLI is installed + authenticated.
- Org / user owns the namespace (no permission blockers).

## Skip If (ANY kills it)

- GitLab / Bitbucket / Codeberg target — wrong tool.
- Repo already configured + actively used — bootstrap is destructive on already-set rules.
- Enterprise restricts `gh repo create` to a wrapper script — defer to enterprise tool.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo name + namespace | string | owner decision |
| Visibility | enum | private / public / internal |
| License choice | SPDX id | team policy |
| CI stack | string | language detection or owner choice |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: idempotent, gh-cli-primary, squash-only, protect-default-branch, secrets-via-secrets-not-env | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for bootstrap config | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: ui-clickops, secrets-in-env, non-idempotent | 700 |
| `content/04-procedure.xml` | essential | 5-step bootstrap procedure | 700 |
| `content/06-decision-tree.xml` | essential | Visibility + license + ci tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect_stack` | haiku | Lockfile inspection. |
| `draft_bootstrap_script` | sonnet | Per-input customisation. |
| `dry_run` | haiku | Deterministic — runs gh commands with --dry-run. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bootstrap-script.sh` | Idempotent bash bootstrap |
| `templates/dependabot.yml` | Dependabot config template |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-github-repo-bootstrap.py` | Validate bootstrap config + verify gh CLI present | Before running bootstrap |

## Related

- - [[code-review-process]] — branch protection + PR template come from there.
- - [[documentation]] — bootstrap drops a starter AGENTS.md.

## Decision tree

See `content/06-decision-tree.xml`. Branches on visibility (private/public/internal) → license auto-pick; then on detected stack → CI workflow template; then on team-size → required-reviewer count.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/bootstrap-script.sh`

```bash
set -euo pipefail

NS="${1:?namespace required}"
NAME="${2:?repo name required}"
VIS="${3:-private}"           # private | public | internal
LICENSE="${4:-MIT}"
CI_STACK="${5:-python}"        # python | node | go | rust | mixed | none

# 1. Create repo if missing
if ! gh repo view "$NS/$NAME" >/dev/null 2>&1; then
  gh repo create "$NS/$NAME" --"$VIS" --license "$LICENSE" --add-readme --confirm
fi

# 2. Switch merge mode to squash-only
gh api -X PATCH "/repos/$NS/$NAME" -F allow_squash_merge=true -F allow_merge_commit=false -F allow_rebase_merge=false >/dev/null

# 3. Branch protection on default branch
DEFAULT_BRANCH=$(gh api "/repos/$NS/$NAME" --jq .default_branch)
gh api -X PUT "/repos/$NS/$NAME/branches/$DEFAULT_BRANCH/protection" \
  -F required_pull_request_reviews.required_approving_review_count=1 \
  -F enforce_admins=true \
  -F required_status_checks.strict=true \
  -F required_status_checks.contexts[]="ci" \
  -F allow_force_pushes=false \
  -F allow_deletions=false >/dev/null

# 4. Dependabot
mkdir -p .github
[[ -f .github/dependabot.yml ]] || cp templates/dependabot.yml .github/dependabot.yml

# 5. CI scaffold
[[ -f .github/workflows/ci.yml ]] || cp templates/ci-stub.yml .github/workflows/ci.yml

echo "bootstrap done: https://github.com/$NS/$NAME"
```

### `templates/dependabot.yml`

```yaml
# .github/dependabot.yml
# Dependabot config: weekly updates for npm and GitHub Actions.
# Place this file at .github/dependabot.yml in the repo root.

version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "06:00"
      timezone: "Europe/Kyiv"
    open-pull-requests-limit: 10
    versioning-strategy: "increase"
    labels:
      - "dependencies"
      - "javascript"
    commit-message:
      prefix: "chore"
      include: "scope"
    groups:
      dev-dependencies:
        dependency-type: "development"
      production-dependencies:
        dependency-type: "production"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "06:00"
      timezone: "Europe/Kyiv"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "github-actions"
    commit-message:
      prefix: "ci"
      include: "scope"
```
