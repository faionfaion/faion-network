#!/usr/bin/env bash
# stale-branches.sh — list remote branches older than N days
# Usage: ./stale-branches.sh [days=2]
# Used by: branch-watchdog agent to identify and close long-lived branches

set -euo pipefail

DAYS=${1:-2}
NOW=$(date +%s)

git fetch --prune origin >/dev/null 2>&1

git for-each-ref \
  --format='%(refname:short) %(committerdate:unix) %(authorname)' \
  refs/remotes/origin \
  | while read -r ref ts author; do
      [[ "$ref" == "origin/main" || "$ref" == "origin/HEAD" ]] && continue
      age_days=$(( (NOW - ts) / 86400 ))
      if (( age_days > DAYS )); then
        printf '%-55s %3d days  %s\n' "$ref" "$age_days" "$author"
      fi
    done
