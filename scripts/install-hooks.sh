#!/usr/bin/env bash
#
# Point this clone's git hooks at the tracked `.githooks/` directory.
#
# Idempotent, safe to run from any directory inside the worktree, and a
# no-op outside a git repository (so a tarball export or a consumer
# install never fails on it). `init.sh`, `scripts/check-validators.sh`
# and `scripts/f066-validate-all.sh` all call it with --quiet, which is
# what makes a fresh clone self-installing whichever of them is run
# first.
set -uo pipefail

QUIET=0
[[ "${1:-}" == "--quiet" ]] && QUIET=1

say() { (( QUIET )) || printf 'install-hooks: %s\n' "$1"; }

ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || {
  say "not a git worktree; nothing to install"
  exit 0
}
cd "$ROOT" || exit 0

if [[ ! -d .githooks ]]; then
  say ".githooks/ is missing; nothing to install"
  exit 0
fi

# Only the hook programs — `.githooks/` also holds data files (the
# seed-blob digest), and making those executable is meaningless noise
# in the mode bits.
for h in .githooks/pre-commit .githooks/commit-msg; do
  [[ -f "$h" ]] && chmod +x "$h"
done

CURRENT=$(git config --get core.hooksPath || true)
if [[ "$CURRENT" == ".githooks" ]]; then
  say "already installed (core.hooksPath=.githooks)"
  exit 0
fi

# A core.hooksPath that merely spells out git's own default (this
# clone had it set to an absolute `<gitdir>/hooks`, holding nothing but
# `.sample` files) is not a customisation anyone chose — treat it as
# unset rather than refusing to install behind it.
DEFAULT_HOOKS=$(cd "$(git rev-parse --git-path hooks)" 2>/dev/null && pwd)
if [[ -n "$CURRENT" ]]; then
  RESOLVED=$(cd "$CURRENT" 2>/dev/null && pwd)
  if [[ -n "$RESOLVED" && "$RESOLVED" == "$DEFAULT_HOOKS" ]]; then
    CURRENT=""
  fi
fi

if [[ -n "$CURRENT" && "$CURRENT" != ".githooks" ]]; then
  printf 'install-hooks: core.hooksPath is %s, not .githooks — leaving it alone.\n' "$CURRENT" >&2
  printf 'install-hooks: run `git config core.hooksPath .githooks` to switch.\n' >&2
  exit 0
fi

git config core.hooksPath .githooks
say "installed (core.hooksPath=.githooks)"
