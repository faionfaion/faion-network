# purpose: Dotfiles install script: stow per-tool with conflict-aware backups.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-600 tokens when loaded as context

#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
HOST=$(hostname -s)

for d in bash vim tmux git "host-$HOST"; do
  [ -d "$d" ] || continue
  # back up conflicts
  for f in $(stow -nv -t "$HOME" "$d" 2>&1 | awk '/existing target/{print $NF}'); do
    cp -a "$HOME/$f" "$HOME/$f.bak-$(date -u +%Y%m%d)"
  done
  stow -t "$HOME" "$d"
done

echo done
