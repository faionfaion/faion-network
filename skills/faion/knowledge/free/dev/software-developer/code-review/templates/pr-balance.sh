#!/usr/bin/env bash
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
