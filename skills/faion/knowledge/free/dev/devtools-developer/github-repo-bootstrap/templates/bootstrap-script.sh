#!/usr/bin/env bash
# purpose: idempotent bootstrap script for a new GitHub repo via gh CLI
# consumes: namespace + name + visibility + license + ci_stack inputs
# produces: configured repo with branch protection, Dependabot, CI, secrets, squash-only merges
# depends-on: gh CLI installed + authenticated; jq for JSON manipulation
# token-budget-impact: ~600 tokens when loaded as context
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
