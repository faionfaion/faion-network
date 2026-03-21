# Agent Dev Tuning Templates

## Claude Code settings.json (Server-Optimized)

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(python *)",
      "Bash(python3 *)",
      "Bash(pip *)",
      "Bash(pip3 *)",
      "Bash(uv *)",
      "Bash(npm *)",
      "Bash(npx *)",
      "Bash(node *)",
      "Bash(docker *)",
      "Bash(docker compose *)",
      "Bash(systemctl --user *)",
      "Bash(journalctl *)",
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(make *)",
      "Bash(ls *)",
      "Bash(mkdir *)",
      "Bash(cp *)",
      "Bash(mv *)",
      "Bash(rm *)",
      "Bash(cat *)",
      "Bash(grep *)",
      "Bash(rg *)",
      "Bash(find *)",
      "Bash(fd *)",
      "Bash(wc *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(sort *)",
      "Bash(uniq *)",
      "Bash(diff *)",
      "Bash(ssh *)",
      "Bash(rsync *)",
      "Bash(alembic *)",
      "Bash(celery *)",
      "Bash(pytest *)",
      "Bash(ruff *)",
      "Bash(mypy *)",
      "Bash(tmux *)",
      "Bash(gh *)"
    ],
    "deny": [
      "Bash(sudo rm -rf /)",
      "Bash(> /dev/sda)",
      "Bash(mkfs *)",
      "Bash(dd if=/dev/zero of=/dev/*)"
    ]
  }
}
```

## sysctl Configuration for Agents

```ini
# /etc/sysctl.d/60-agent-dev.conf
# Kernel tuning for AI agent development workloads

# === inotify ===
# File watchers for editors, agents, build tools
fs.inotify.max_user_watches = 524288
fs.inotify.max_user_instances = 1024
fs.inotify.max_queued_events = 65536

# === Memory ===
# Low swappiness: prefer RAM, use swap only under pressure
vm.swappiness = 10

# Don't aggressively reclaim dentries/inodes
vm.vfs_cache_pressure = 50

# Allow overcommit (agents allocate more than they use)
vm.overcommit_memory = 0
vm.overcommit_ratio = 80

# === File descriptors ===
# System-wide file descriptor limit
fs.file-max = 2097152

# === Network ===
# Useful for agents making many API calls
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
```

## PAM Limits for Agent User

```bash
# /etc/security/limits.d/nero-agent.conf
# Resource limits for the agent development user

# Open files (for many file watchers and connections)
nero  soft  nofile    65536
nero  hard  nofile    131072

# Processes/threads (for concurrent tools, subprocesses)
nero  soft  nproc     4096
nero  hard  nproc     8192

# Locked memory (for mmap operations)
nero  soft  memlock   unlimited
nero  hard  memlock   unlimited

# Core dumps (disable for security)
nero  soft  core      0
nero  hard  core      0
```

## MCP Server Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/nero/workspace",
        "/srv/nero"
      ]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://nero:${POSTGRES_PASSWORD}@localhost:5432/nero_db"
      }
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

## Agent Session Management Script

```bash
#!/bin/bash
# agent-session.sh
# Create or attach to an agent tmux session with resource monitoring

set -euo pipefail

SESSION="${1:-agent}"
WORKDIR="${2:-$HOME/workspace}"

# Check if session exists
if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "Attaching to existing session: $SESSION"
    tmux attach -t "$SESSION"
    exit 0
fi

echo "Creating new agent session: $SESSION"

# Create session with main window
tmux new-session -d -s "$SESSION" -n "work" -c "$WORKDIR"

# Window 1: Main working area (for claude)
tmux send-keys -t "$SESSION:work" "cd $WORKDIR" C-m

# Window 2: Logs
tmux new-window -t "$SESSION" -n "logs" -c "$WORKDIR"
tmux send-keys -t "$SESSION:logs" "journalctl --user -u 'nero-*' -f --no-hostname" C-m

# Window 3: System monitor
tmux new-window -t "$SESSION" -n "system" -c "$WORKDIR"
tmux send-keys -t "$SESSION:system" "htop --sort-key=PERCENT_MEM" C-m

# Select main window
tmux select-window -t "$SESSION:work"

# Attach
tmux attach -t "$SESSION"
```

## Worktree Management Script

```bash
#!/bin/bash
# worktree.sh
# Manage git worktrees for parallel agent work
# Usage:
#   ./worktree.sh create feature-123
#   ./worktree.sh list
#   ./worktree.sh remove feature-123
#   ./worktree.sh clean

set -euo pipefail

ACTION="${1:?Usage: $0 <create|list|remove|clean> [branch-name]}"
REPO_ROOT=$(git rev-parse --show-toplevel)
REPO_NAME=$(basename "$REPO_ROOT")
WORKTREE_BASE="$(dirname "$REPO_ROOT")"

case "$ACTION" in
    create)
        BRANCH="${2:?Usage: $0 create <branch-name>}"
        WORKTREE_DIR="$WORKTREE_BASE/${REPO_NAME}-${BRANCH}"

        if [ -d "$WORKTREE_DIR" ]; then
            echo "Worktree already exists: $WORKTREE_DIR"
            exit 1
        fi

        # Create branch if it doesn't exist
        if ! git show-ref --verify --quiet "refs/heads/$BRANCH" 2>/dev/null; then
            echo "Creating branch: $BRANCH"
            git branch "$BRANCH"
        fi

        # Create worktree
        git worktree add "$WORKTREE_DIR" "$BRANCH"
        echo "Worktree created: $WORKTREE_DIR"
        echo "  cd $WORKTREE_DIR"
        ;;

    list)
        git worktree list
        ;;

    remove)
        BRANCH="${2:?Usage: $0 remove <branch-name>}"
        WORKTREE_DIR="$WORKTREE_BASE/${REPO_NAME}-${BRANCH}"

        if [ ! -d "$WORKTREE_DIR" ]; then
            echo "Worktree not found: $WORKTREE_DIR"
            exit 1
        fi

        git worktree remove "$WORKTREE_DIR"
        echo "Worktree removed: $WORKTREE_DIR"
        ;;

    clean)
        echo "Pruning stale worktrees..."
        git worktree prune -v
        echo ""
        echo "Remaining worktrees:"
        git worktree list
        ;;

    *)
        echo "Usage: $0 <create|list|remove|clean> [branch-name]"
        exit 1
        ;;
esac
```

## Claude Code Hooks: tmux Save on Prompt

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "tmux capture-pane -p -S -100 > /tmp/claude-last-prompt-$(date +%s).txt 2>/dev/null || true"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/home/nero/workspace/scripts/notify-telegram.sh 'Claude Code session ended on $(hostname)' 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

## Resource-Limited Agent Launcher

```bash
#!/bin/bash
# agent-limited.sh
# Launch Claude Code with resource limits
# Usage: ./agent-limited.sh [memory-limit] [cpu-quota]

MEMORY="${1:-4G}"
CPU="${2:-400%}"

echo "Launching Claude Code with limits: Memory=$MEMORY, CPU=$CPU"

systemd-run --user --scope \
    --property="MemoryMax=$MEMORY" \
    --property="MemoryHigh=$(echo "$MEMORY" | sed 's/G//' | awk '{printf "%.0fM", $1*1024*0.75}')M" \
    --property="CPUQuota=$CPU" \
    --property="TasksMax=512" \
    -- claude
```

## System Tuning Verification Script

```bash
#!/bin/bash
# verify-agent-tuning.sh
# Verify server is properly tuned for agent development

echo "=== Agent Dev Tuning Verification ==="
echo ""

# inotify
WATCHES=$(cat /proc/sys/fs/inotify/max_user_watches)
echo -n "inotify.max_user_watches: $WATCHES"
[ "$WATCHES" -ge 524288 ] && echo " [OK]" || echo " [LOW - should be >= 524288]"

INSTANCES=$(cat /proc/sys/fs/inotify/max_user_instances)
echo -n "inotify.max_user_instances: $INSTANCES"
[ "$INSTANCES" -ge 1024 ] && echo " [OK]" || echo " [LOW - should be >= 1024]"

# File descriptors
FD_LIMIT=$(ulimit -n)
echo -n "ulimit -n (open files): $FD_LIMIT"
[ "$FD_LIMIT" -ge 65536 ] && echo " [OK]" || echo " [LOW - should be >= 65536]"

# Swap
SWAP_TOTAL=$(free -m | awk '/Swap:/ {print $2}')
echo -n "Swap total: ${SWAP_TOTAL}MB"
[ "$SWAP_TOTAL" -ge 4096 ] && echo " [OK]" || echo " [LOW - should be >= 4096MB]"

SWAPPINESS=$(cat /proc/sys/vm/swappiness)
echo -n "vm.swappiness: $SWAPPINESS"
[ "$SWAPPINESS" -le 20 ] && echo " [OK]" || echo " [HIGH - should be <= 20]"

# Linger
LINGER=$(loginctl show-user "$USER" -p Linger --value 2>/dev/null || echo "unknown")
echo -n "Linger: $LINGER"
[ "$LINGER" = "yes" ] && echo " [OK]" || echo " [DISABLED - run: loginctl enable-linger]"

# tmux
echo -n "tmux: "
command -v tmux &>/dev/null && echo "$(tmux -V) [OK]" || echo "NOT INSTALLED"

# Filesystem
MOUNT_OPTS=$(mount | grep " / " | grep -o "noatime" || echo "atime")
echo -n "Root mount: $MOUNT_OPTS"
[ "$MOUNT_OPTS" = "noatime" ] && echo " [OK]" || echo " [CONSIDER: mount with noatime]"

echo ""
echo "=== Done ==="
```
