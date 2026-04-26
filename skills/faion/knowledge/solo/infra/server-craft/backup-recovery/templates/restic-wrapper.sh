#!/bin/bash
# restic-wrapper.sh
# Convenience wrapper for restic: pre-loads env from .env, passes all args to restic.
#
# Usage:
#   restic-wrapper.sh snapshots
#   restic-wrapper.sh restore latest --target /tmp/restore
#   restic-wrapper.sh check
#   restic-wrapper.sh forget --keep-daily 7 --keep-weekly 4 --prune
#
# Install: chmod +x ~/bin/restic-wrapper.sh && ln -sf ~/bin/restic-wrapper.sh ~/bin/rw

set -euo pipefail

# Load credentials from .env
if [ -f /home/nero/workspace/.env ]; then
    eval "$(grep -E '^(B2_ACCOUNT_ID|B2_ACCOUNT_KEY|RESTIC_REPOSITORY)=' /home/nero/workspace/.env 2>/dev/null || true)"
    export B2_ACCOUNT_ID B2_ACCOUNT_KEY RESTIC_REPOSITORY
fi

export RESTIC_REPOSITORY="${RESTIC_REPOSITORY:-b2:nero-backups:server}"
export RESTIC_PASSWORD_FILE="/home/nero/.restic-password"

exec restic "$@"
