#!/usr/bin/env bash
# wt-spawn.sh — create a worktree with branch, scope manifest, and runtime env.
# Usage:  source wt-spawn.sh && wt_spawn billing apps/billing/** tests/billing/**

set -euo pipefail

# tracked range for per-worktree ports
WT_PORT_BASE="${WT_PORT_BASE:-4000}"
WT_PORT_MAX="${WT_PORT_MAX:-4999}"

wt_alloc_port() {
  local slug="$1"
  # deterministic hash → port within range
  local hash
  hash=$(printf '%s' "$slug" | cksum | awk '{print $1}')
  echo $((WT_PORT_BASE + hash % (WT_PORT_MAX - WT_PORT_BASE + 1)))
}

wt_spawn() {
  local slug="$1"; shift
  local scopes=("$@")
  local wt_dir="../wt-${slug}"
  local branch="feat/${slug}"

  git worktree add "$wt_dir" -b "$branch"
  printf '%s\n' "${scopes[@]}" > "$wt_dir/WT-SCOPE"

  local port; port=$(wt_alloc_port "$slug")
  cat > "$wt_dir/.wt-env" <<EOF
PORT=${port}
DATABASE_URL=postgres://dev:dev@localhost:5432/app_wt_${slug//-/_}
REDIS_URL=redis://localhost:6379/$((port % 16))
SECRETS_PROFILE=op://dev/wt-${slug}
WT_SLUG=${slug}
EOF
  echo "spawned worktree=${wt_dir} branch=${branch} port=${port}"
}
