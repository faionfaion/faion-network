#!/bin/bash
# ~/.claude/hooks/post-edit-format.sh
# PostToolUse hook: auto-format files after Claude edits or writes them.
# Supports: Python (ruff), JS/TS/JSON/CSS/YAML (prettier), Go (gofmt), Rust (rustfmt)
# Errors logged to /tmp/claude-hooks.log — never to stderr.

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // empty' 2>/dev/null)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    echo '{"status":"ok"}'
    exit 0
fi

# Skip files larger than 1MB
FILE_SIZE=$(stat -c%s "$FILE_PATH" 2>/dev/null || stat -f%z "$FILE_PATH" 2>/dev/null || echo 0)
if [ "$FILE_SIZE" -gt 1048576 ]; then
    echo '{"status":"ok"}'
    exit 0
fi

EXTENSION="${FILE_PATH##*.}"
LOG="/tmp/claude-hooks.log"

case "$EXTENSION" in
    py)
        if command -v ruff &>/dev/null; then
            ruff format --quiet "$FILE_PATH" 2>>"$LOG"
            ruff check --fix --quiet "$FILE_PATH" 2>>"$LOG"
        fi
        ;;
    ts|tsx|js|jsx|json|css|scss|md|yaml|yml)
        if command -v npx &>/dev/null; then
            npx --yes prettier --write "$FILE_PATH" 2>>"$LOG"
        fi
        ;;
    go)
        if command -v gofmt &>/dev/null; then
            gofmt -w "$FILE_PATH" 2>>"$LOG"
        fi
        ;;
    rs)
        if command -v rustfmt &>/dev/null; then
            rustfmt "$FILE_PATH" 2>>"$LOG"
        fi
        ;;
esac

echo '{"status":"ok"}'
