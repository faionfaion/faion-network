# Code Review

## Summary

**One-sentence:** Produces a code-review pipeline: PR size limit (<400 lines), automated gates (lint/type/test/coverage green before review), agentic pre-review pass, and reviewer focus narrowed to correctness + design.

**One-paragraph:** Produces a code-review pipeline: PR size limit (<400 lines), automated gates (lint/type/test/coverage green before review), agentic pre-review pass, and reviewer focus narrowed to correctness + design. The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

**Ефективно для:** команд, що оперують цим артефактом регулярно і потребують детермінованого формату плюс перевірюваного результату.

## Applies If (ALL must hold)

- Repository hosts a CI pipeline that can post status checks (GitHub, GitLab, Bitbucket).
- The team has agreed on a PR size convention (< 400 lines default).
- Lint / type / test / coverage gates exist or are about to be added.
- Reviewers are humans, not just AI bots.

## Skip If (ANY kills it)

- Solo developer with no review reviewer available (use AI review only as a stopgap; not enough).
- Codebase auto-merges trusted bot PRs (dependency bumps); manual review not applicable.
- Repository is read-only (vendored library) — patches happen upstream.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Output target path | string | constitution / SDD spec |
| Owner (role:person) | string | team roster |
| Trigger event | event/threshold/schedule | constitution |
| Evidence anchor (URL / ticket / commit) | string | upstream context |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/best-practices-2026` | Constitution rules reviewers enforce. |
| `free/dev/software-developer/code-coverage` | Coverage gate the review pipeline consumes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules specific to code-review | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/04-procedure.xml` | medium | Step-by-step procedure (when complexity >= medium) | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree from observable inputs to a rule conclusion | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Pre-review pass (lint/types/coverage/security) | sonnet | Mechanical gates, deterministic. |
| Reviewer-facing summary + risk callout | opus | Cross-file synthesis, design judgement. |
| Auto-suggest doc/test additions | sonnet | Templated. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-balance.sh` | Pre-commit guard: reject PRs over 400 lines unless labeled `large-pr-approved`. |
| `templates/pr-checks.yml` | Required GitHub Actions checks (lint, types, tests, coverage, oasdiff, security). |
| `templates/pr-description.md.j2` | PR description template with risk / scope / test sections. |
| `templates/pr-description.md` | PR description template with risk / scope / test sections. Generated from `templates/pr-description.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-review.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[best-practices-2026]] — see methodology AGENTS.md for context.
- [[code-coverage]] — see methodology AGENTS.md for context.
- [[api-testing]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pr-balance.sh`

```bash
# pr-balance.sh — assign the least-loaded reviewer from CODEOWNERS.
# Usage: pr-balance.sh <PR_NUMBER>
# Requires: gh CLI authenticated
set -euo pipefail
PR="${1:?PR number required}"
REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
OWNERS_RAW="$(gh api "repos/$REPO/contents/CODEOWNERS" -q .content | base64 -d)"

# Extract unique GitHub usernames (skip teams with /)
CANDIDATES=$(echo "$OWNERS_RAW" | grep -oE '@[A-Za-z0-9_-]+' \
             | sed 's/@//' | grep -v '/' | sort -u)

LOWEST=""
LOWEST_COUNT=99999

for user in $CANDIDATES; do
  N=$(gh search prs --repo "$REPO" --review-requested "$user" \
      --state open --json number -q '. | length' 2>/dev/null || echo 0)
  echo "$user: $N pending review(s)"
  if (( N < LOWEST_COUNT )); then
    LOWEST_COUNT=$N
    LOWEST="$user"
  fi
done

[ -n "$LOWEST" ] || { echo "no candidates found in CODEOWNERS"; exit 1; }
gh pr edit "$PR" --add-reviewer "$LOWEST"
echo "assigned $LOWEST ($LOWEST_COUNT pending)"
```

### `templates/pr-checks.yml`

```yaml
name: PR Checks

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linters
        run: make lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: make test

  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check coverage threshold
        run: pytest --cov=src --cov-fail-under=80

  pr-size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Warn on large PR
        run: |
          CHANGED=$(git diff --stat origin/${{ github.base_ref }} | tail -1 | awk '{print $4}')
          if [ "${CHANGED:-0}" -gt 400 ]; then
            echo "::warning::PR has ${CHANGED} changed lines (>400). Consider splitting."
          fi
```
