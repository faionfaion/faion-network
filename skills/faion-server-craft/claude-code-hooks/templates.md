# Claude Code Hooks Templates

## settings.json with Common Hooks

Complete settings.json with the most useful hooks pre-configured.

```json
{
    "hooks": {
        "PostToolUse": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/post-edit-format.sh",
                "matcher": "Edit",
                "timeout": 10000
            },
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/post-write-format.sh",
                "matcher": "Write",
                "timeout": 10000
            }
        ],
        "PreToolUse": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/pre-bash-safety.sh",
                "matcher": "Bash",
                "timeout": 5000
            }
        ],
        "UserPromptSubmit": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/tmux-save.sh",
                "timeout": 5000
            }
        ],
        "SubagentStart": [
            {
                "type": "command",
                "command": "bash ~/.claude/hooks/tmux-save.sh",
                "timeout": 5000
            }
        ]
    }
}
```

## post-edit-format.sh (Auto-Format on Edit)

```bash
#!/bin/bash
# ~/.claude/hooks/post-edit-format.sh
# Automatically formats files after Claude edits them.
# Supports: Python (ruff), JS/TS (prettier), JSON (prettier)

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // empty' 2>/dev/null)

# Exit early if no file path
if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Skip large files (>1MB)
FILE_SIZE=$(stat -f%z "$FILE_PATH" 2>/dev/null || stat -c%s "$FILE_PATH" 2>/dev/null || echo 0)
if [ "$FILE_SIZE" -gt 1048576 ]; then
    exit 0
fi

EXTENSION="${FILE_PATH##*.}"

case "$EXTENSION" in
    py)
        # Python: ruff format + fix
        if command -v ruff &>/dev/null; then
            ruff format --quiet "$FILE_PATH" 2>/dev/null
            ruff check --fix --quiet "$FILE_PATH" 2>/dev/null
        fi
        ;;
    ts|tsx|js|jsx|json|css|scss|md|yaml|yml)
        # JS/TS/Web: prettier
        if command -v npx &>/dev/null; then
            npx --yes prettier --write "$FILE_PATH" 2>/dev/null
        fi
        ;;
    go)
        # Go: gofmt
        if command -v gofmt &>/dev/null; then
            gofmt -w "$FILE_PATH" 2>/dev/null
        fi
        ;;
    rs)
        # Rust: rustfmt
        if command -v rustfmt &>/dev/null; then
            rustfmt "$FILE_PATH" 2>/dev/null
        fi
        ;;
esac

echo '{"status": "ok"}'
```

## post-write-format.sh (Auto-Format on Write)

```bash
#!/bin/bash
# ~/.claude/hooks/post-write-format.sh
# Same as post-edit but for the Write tool (new files)

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // empty' 2>/dev/null)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

FILE_SIZE=$(stat -c%s "$FILE_PATH" 2>/dev/null || echo 0)
if [ "$FILE_SIZE" -gt 1048576 ]; then
    exit 0
fi

EXTENSION="${FILE_PATH##*.}"

case "$EXTENSION" in
    py)
        if command -v ruff &>/dev/null; then
            ruff format --quiet "$FILE_PATH" 2>/dev/null
            ruff check --fix --quiet "$FILE_PATH" 2>/dev/null
        fi
        ;;
    ts|tsx|js|jsx|json|css|scss|md|yaml|yml)
        if command -v npx &>/dev/null; then
            npx --yes prettier --write "$FILE_PATH" 2>/dev/null
        fi
        ;;
esac

echo '{"status": "ok"}'
```

## tmux-save.sh (Save Tmux State)

```bash
#!/bin/bash
# ~/.claude/hooks/tmux-save.sh
# Saves tmux pane content on user prompt and subagent start.
# Useful for preserving context during long agent sessions.

# Only run if inside tmux
if [ -z "${TMUX:-}" ]; then
    exit 0
fi

# Capture current pane content
SAVE_DIR="$HOME/.claude/tmux-captures"
mkdir -p "$SAVE_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CAPTURE_FILE="$SAVE_DIR/capture_${TIMESTAMP}.txt"

# Capture visible pane content
tmux capture-pane -t "$TMUX_PANE" -p > "$CAPTURE_FILE" 2>/dev/null

# Keep only last 10 captures (cleanup old ones)
ls -t "$SAVE_DIR"/capture_*.txt 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null

echo '{"status": "ok"}'
```

## pre-bash-safety.sh (Git Safety Guard)

```bash
#!/bin/bash
# ~/.claude/hooks/pre-bash-safety.sh
# Blocks dangerous git and system commands.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.parameters.command // empty' 2>/dev/null)

if [ -z "$COMMAND" ]; then
    echo '{"action": "allow"}'
    exit 0
fi

# Block force push to main/master
if echo "$COMMAND" | grep -qEi 'git\s+push\s+.*--force.*\b(main|master)\b|git\s+push\s+-f\s+.*\b(main|master)\b'; then
    echo '{"action": "block", "reason": "Force push to main/master is blocked. Use a feature branch instead."}'
    exit 0
fi

# Block git clean -f (removes untracked files permanently)
if echo "$COMMAND" | grep -qE 'git\s+clean\s+-f'; then
    echo '{"action": "block", "reason": "git clean -f permanently deletes untracked files. Use git clean -n (dry run) first."}'
    exit 0
fi

# Block rm -rf / or rm -rf ~
if echo "$COMMAND" | grep -qE 'rm\s+-rf\s+(/|~|\$HOME)\s*$'; then
    echo '{"action": "block", "reason": "Refusing to delete root or home directory."}'
    exit 0
fi

# Block shutdown/reboot (unless user is explicit)
if echo "$COMMAND" | grep -qE '^\s*(shutdown|reboot|init\s+[06])'; then
    echo '{"action": "block", "reason": "System shutdown/reboot blocked. Run manually if needed."}'
    exit 0
fi

echo '{"action": "allow"}'
```

## post-edit-test.sh (Auto-Run Tests)

```bash
#!/bin/bash
# ~/.claude/hooks/post-edit-test.sh
# Runs related tests after editing Python files.
# Add to PostToolUse with matcher "Edit" if you want auto-testing.

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // empty' 2>/dev/null)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Only for Python files
if [[ "$FILE_PATH" != *.py ]]; then
    exit 0
fi

# Skip test files themselves (avoid infinite loops)
BASENAME=$(basename "$FILE_PATH")
if [[ "$BASENAME" == test_* ]] || [[ "$BASENAME" == *_test.py ]]; then
    exit 0
fi

# Find the project root (look for pyproject.toml or setup.py)
DIR="$FILE_PATH"
PROJECT_ROOT=""
while [ "$DIR" != "/" ]; do
    DIR=$(dirname "$DIR")
    if [ -f "$DIR/pyproject.toml" ] || [ -f "$DIR/setup.py" ]; then
        PROJECT_ROOT="$DIR"
        break
    fi
done

if [ -z "$PROJECT_ROOT" ]; then
    exit 0
fi

# Find corresponding test file
REL_PATH="${FILE_PATH#$PROJECT_ROOT/}"
TEST_DIR="$PROJECT_ROOT/tests"
SRC_BASENAME=$(basename "$FILE_PATH" .py)

# Common test file locations
for test_candidate in \
    "$TEST_DIR/test_${SRC_BASENAME}.py" \
    "$TEST_DIR/${SRC_BASENAME}_test.py" \
    "$(dirname "$FILE_PATH")/test_${SRC_BASENAME}.py"; do
    if [ -f "$test_candidate" ]; then
        cd "$PROJECT_ROOT"
        # Run tests quietly, report only failures
        if [ -d ".venv" ]; then
            .venv/bin/python -m pytest "$test_candidate" -x -q --tb=short 2>&1 | tail -5
        fi
        break
    fi
done

echo '{"status": "ok"}'
```

## post-write-git-stage.sh (Auto-Stage New Files)

```bash
#!/bin/bash
# ~/.claude/hooks/post-write-git-stage.sh
# Automatically git-add newly created files.
# Add to PostToolUse with matcher "Write".

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.parameters.file_path // empty' 2>/dev/null)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Check if file is in a git repo
FILE_DIR=$(dirname "$FILE_PATH")
if git -C "$FILE_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    # Only stage if it's a new untracked file
    GIT_ROOT=$(git -C "$FILE_DIR" rev-parse --show-toplevel)
    REL_PATH="${FILE_PATH#$GIT_ROOT/}"

    STATUS=$(git -C "$GIT_ROOT" status --porcelain -- "$REL_PATH" 2>/dev/null)
    if [[ "$STATUS" == "??"* ]]; then
        git -C "$GIT_ROOT" add "$FILE_PATH" 2>/dev/null
    fi
fi

echo '{"status": "ok"}'
```

## Hook Installation Script

```bash
#!/bin/bash
# install-hooks.sh - Install all Claude Code hooks
set -euo pipefail

HOOKS_DIR="$HOME/.claude/hooks"
SETTINGS_FILE="$HOME/.claude/settings.json"

echo "=== Installing Claude Code Hooks ==="

# Create hooks directory
mkdir -p "$HOOKS_DIR"

# List of hook scripts (assumes they are in the same directory as this script)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

HOOKS=(
    "post-edit-format.sh"
    "post-write-format.sh"
    "tmux-save.sh"
    "pre-bash-safety.sh"
)

for hook in "${HOOKS[@]}"; do
    if [ -f "$SCRIPT_DIR/$hook" ]; then
        cp "$SCRIPT_DIR/$hook" "$HOOKS_DIR/$hook"
        chmod +x "$HOOKS_DIR/$hook"
        echo "  Installed: $hook"
    else
        echo "  Skipped (not found): $hook"
    fi
done

# Verify jq is available
if ! command -v jq &>/dev/null; then
    echo ""
    echo "WARNING: jq not installed. Hooks need jq for JSON parsing."
    echo "Install with: sudo apt install jq"
fi

echo ""
echo "=== Hooks installed to $HOOKS_DIR ==="
echo "Configure hooks in: $SETTINGS_FILE"
echo "See templates for settings.json example."
```
