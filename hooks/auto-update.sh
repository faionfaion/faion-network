#!/bin/bash
# Auto-update hook for faion-network
# Runs once per session when /faion-net is invoked

CLAUDE_DIR="${HOME}/.claude"
UPDATE_CHECK_FILE="/tmp/faion-network-update-check-$$"

# Skip if no git repo
if [[ ! -d "$CLAUDE_DIR/.git" ]]; then
    exit 0
fi

cd "$CLAUDE_DIR" || exit 0

# Fetch silently (with timeout)
timeout 5 git fetch origin master 2>/dev/null || exit 0

# Compare local vs remote
LOCAL=$(git rev-parse HEAD 2>/dev/null)
REMOTE=$(git rev-parse origin/master 2>/dev/null)

if [[ "$LOCAL" == "$REMOTE" ]]; then
    # Up to date
    exit 0
fi

# Count commits behind
COMMITS_BEHIND=$(git rev-list --count HEAD..origin/master 2>/dev/null || echo "0")

if [[ "$COMMITS_BEHIND" -gt 0 ]]; then
    # Output JSON for Claude to see
    cat << EOF
{
    "message": "🔄 Faion Network: $COMMITS_BEHIND update(s) available",
    "action": "Run ~/.claude/update.sh to update, or continue with current version"
}
EOF
fi

exit 0
