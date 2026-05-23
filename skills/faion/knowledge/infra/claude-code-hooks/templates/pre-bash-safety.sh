#!/bin/bash
# purpose: PreToolUse hook: block destructive git/system commands.
# consumes: inputs declared in claude-code-hooks/AGENTS.md Prerequisites table
# produces: artefact matching claude-code-hooks/content/02-output-contract.xml
# depends-on: rules in claude-code-hooks/content/01-core-rules.xml
# token-budget-impact: ~200-600 tokens when filled
# ~/.claude/hooks/pre-bash-safety.sh
# PreToolUse hook: block destructive git and system commands.
# Always include "reason" in block actions — without it Claude retries indefinitely.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.parameters.command // empty' 2>/dev/null)

if [ -z "$COMMAND" ]; then
    echo '{"action":"allow"}'
    exit 0
fi

# Block force push to main/master
if echo "$COMMAND" | grep -qEi 'git\s+push\s+.*--force.*\b(main|master)\b|git\s+push\s+-f\s+.*\b(main|master)\b'; then
    echo '{"action":"block","reason":"Force push to main/master is blocked. Use a feature branch or ask the user to confirm."}'
    exit 0
fi

# Block git clean -f (permanently deletes untracked files)
if echo "$COMMAND" | grep -qE 'git\s+clean\s+-f'; then
    echo '{"action":"block","reason":"git clean -f permanently deletes untracked files. Run git clean -n (dry run) first and confirm with the user."}'
    exit 0
fi

# Block rm -rf on root or home directory
if echo "$COMMAND" | grep -qE 'rm\s+-rf\s+(/|~|\$HOME)\s*$'; then
    echo '{"action":"block","reason":"Refusing to delete root or home directory."}'
    exit 0
fi

# Block shutdown/reboot
if echo "$COMMAND" | grep -qE '^\s*(shutdown|reboot|init\s+[06])'; then
    echo '{"action":"block","reason":"System shutdown/reboot blocked. Run manually if needed."}'
    exit 0
fi

echo '{"action":"allow"}'
