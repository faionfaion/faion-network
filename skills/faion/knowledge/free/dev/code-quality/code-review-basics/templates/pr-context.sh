#!/usr/bin/env bash
# pr-context.sh — emit review-ready context for an agent.
# Usage: pr-context.sh <owner/repo> <pr-number>
# Requires: gh CLI authenticated
set -euo pipefail

REPO="${1:?owner/repo required}"
PR="${2:?PR number required}"

echo "## PR metadata"
gh pr view "$PR" --repo "$REPO" \
  --json title,body,author,additions,deletions,changedFiles \
  | jq '{ title, author: .author.login, additions, deletions, changedFiles }'

echo ""
echo "## Files changed"
gh pr diff "$PR" --repo "$REPO" --name-only

echo ""
echo "## Failing CI checks (agent must not review if any)"
gh pr checks "$PR" --repo "$REPO" --json name,state,conclusion \
  | jq '[.[] | select(.conclusion == "failure" or .state == "FAILURE")]'

LINES=$(gh pr diff "$PR" --repo "$REPO" | wc -l)
if [ "$LINES" -gt 3000 ]; then
  echo ""
  echo "## WARNING: PR exceeds 400 changed lines ($LINES diff lines)."
  echo "## Instruct author to split before proceeding with agent review."
  exit 0
fi

echo ""
echo "## Diff"
gh pr diff "$PR" --repo "$REPO" | head -2000
