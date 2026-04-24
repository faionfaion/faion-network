# Agent Dev Tuning Examples

## Example 1: NERO Platform Agent Tuning

The NERO platform server (Hetzner CX53, 16 CPUs, 30GB RAM) is tuned for running Claude Code agents alongside the production platform.

### Resource Allocation

```
Total: 16 CPUs, 30GB RAM, 4GB Swap

Docker infrastructure:  ~6GB RAM, ~4 CPUs
  - postgres:         2-4GB
  - redis:            512MB
  - rabbitmq:         512MB-1GB
  - flower:           256MB

Application services:  ~3.5GB RAM, ~8 CPUs
  - nero-core:        2GB max (Celery, 20 gevent workers)
  - nero-channel-web: 512MB max (uvicorn, 2 workers)
  - nero-channel-tg:  256MB max (aiogram bot)
  - nero-web:         256MB max (serve static)
  - nero-beat:        256MB max (scheduler)
  - nero-autoheal:    128MB max (watcher)

Agent headroom:        ~20GB RAM, ~4 CPUs available
  - Claude Code:      4-8GB per agent session
  - File watchers:    ~50MB for inotify
  - Build tools:      1-2GB for npm/pip installs
```

### Applied Tuning

```bash
# /etc/sysctl.d/60-agent-dev.conf
fs.inotify.max_user_watches = 524288
fs.inotify.max_user_instances = 1024
fs.inotify.max_queued_events = 65536
vm.swappiness = 10
vm.vfs_cache_pressure = 50
fs.file-max = 2097152

# /etc/security/limits.d/nero.conf
nero  soft  nofile    65536
nero  hard  nofile    131072
nero  soft  nproc     4096
nero  hard  nproc     8192

# Swap: 4GB swapfile
/swapfile none swap sw 0 0

# Filesystem: noatime on root
UUID=xxx / ext4 defaults,noatime 0 1
```

### Claude Code Setup

```json
// ~/.claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(python *)",
      "Bash(pip *)",
      "Bash(npm *)",
      "Bash(npx *)",
      "Bash(docker *)",
      "Bash(docker compose *)",
      "Bash(systemctl --user *)",
      "Bash(journalctl *)",
      "Bash(curl *)",
      "Bash(make *)",
      "Bash(ls *)",
      "Bash(mkdir *)",
      "Bash(cp *)",
      "Bash(mv *)",
      "Bash(rm *)",
      "Bash(cat *)",
      "Bash(grep *)",
      "Bash(find *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(sort *)",
      "Bash(diff *)",
      "Bash(rsync *)",
      "Bash(alembic *)",
      "Bash(pytest *)",
      "Bash(ruff *)",
      "Bash(gh *)"
    ]
  }
}
```

### tmux Agent Workflow

```bash
# Daily agent session setup
tmux new-session -d -s dev -n "claude" -c ~/workspace
tmux new-window -t dev -n "logs"
tmux new-window -t dev -n "git"

# In "claude" window: run Claude Code
# In "logs" window: journalctl --user -u 'nero-*' -f
# In "git" window: git operations, deployment

# Detach: Ctrl+B, D
# Reattach: tmux attach -t dev
```

---

## Example 2: Parallel Agent Execution with Worktrees

Running two Claude Code agents simultaneously -- one for feature development, one for code review.

### Setup

```bash
# Main repo
cd ~/workspace/repos/nero-core

# Create worktree for feature work
git worktree add ../nero-core-feature-auth feature/auth-refactor

# tmux session for Agent 1 (feature work)
tmux new-session -d -s agent-feature -c ~/workspace/repos/nero-core-feature-auth
tmux send-keys -t agent-feature "claude" C-m

# tmux session for Agent 2 (review on main branch)
tmux new-session -d -s agent-review -c ~/workspace/repos/nero-core
tmux send-keys -t agent-review "claude" C-m
```

### Resource Limits

```bash
# Agent 1: Feature development (needs more resources)
tmux send-keys -t agent-feature "systemd-run --user --scope --property=MemoryMax=6G --property=CPUQuota=600% -- claude" C-m

# Agent 2: Code review (lighter workload)
tmux send-keys -t agent-review "systemd-run --user --scope --property=MemoryMax=3G --property=CPUQuota=300% -- claude" C-m
```

### Merge Workflow After Agents Finish

```bash
# Switch to main repo
cd ~/workspace/repos/nero-core

# Merge feature branch
git merge feature/auth-refactor

# Clean up worktree
git worktree remove ../nero-core-feature-auth

# Optionally delete the branch
git branch -d feature/auth-refactor
```

---

## Example 3: Celery Worker Tuning for LLM Workloads

The nero-core Celery worker processes LLM API calls with gevent concurrency. Each task can consume 50-200MB during response streaming.

### Configuration

```ini
# nero-core.service
[Service]
ExecStart=/srv/nero/nero-core/.venv/bin/celery \
    -A src.celery_app worker \
    --pool=gevent \
    --concurrency=20 \
    --loglevel=info \
    --without-heartbeat \
    --without-mingle \
    --without-gossip \
    -Q default,process_message,deliver_web,deliver_telegram

# Memory: 20 workers x ~100MB peak = ~2GB
MemoryMax=2G
MemoryHigh=1536M

# CPU: gevent is single-threaded but uses many greenlets
CPUQuota=800%

# Many greenlets + connections
TasksMax=512
LimitNOFILE=65536
```

### Why gevent Over prefork

| Pool | Memory per Worker | CPU Pattern | Best For |
|------|------------------|-------------|----------|
| prefork | 200-500MB | Multi-process | CPU-bound tasks |
| gevent | 5-20MB | Single-thread, async I/O | I/O-bound (API calls) |
| solo | N/A | Single-process | Development |

Gevent is ideal for LLM API calls because:
- Each task mostly waits for the API response (I/O-bound)
- 20 concurrent tasks in ~500MB vs 20 prefork workers in ~4GB
- Context switching between greenlets is nearly free

### Monitoring Gevent Workers

```bash
# Check active greenlets
celery -A src.celery_app inspect active | grep -c "id"

# Check memory per worker process
ps aux | grep "[c]elery" | awk '{print $6/1024 "MB", $0}'

# Check connection count
ss -tnp | grep $(pgrep -f celery | head -1) | wc -l
```

---

## Example 4: tmux Hook for Context Preservation

Save agent session context automatically when Claude Code prompts for input or when the session detaches.

### tmux Configuration

```bash
# ~/.tmux.conf additions for agent context saving

# Save pane content on detach
set-hook -g client-detached 'run-shell "~/workspace/scripts/save-tmux-context.sh detached"'

# Save pane content every 5 minutes
set-hook -g timer 'run-shell "~/workspace/scripts/save-tmux-context.sh periodic"'
```

### Context Save Script

```bash
#!/bin/bash
# save-tmux-context.sh
# Save current tmux pane content for agent context recovery

TRIGGER="${1:-manual}"
CONTEXT_DIR="$HOME/workspace/memory/tmux-context"
mkdir -p "$CONTEXT_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION=$(tmux display-message -p '#S' 2>/dev/null || echo "unknown")
WINDOW=$(tmux display-message -p '#W' 2>/dev/null || echo "unknown")

# Capture last 500 lines of current pane
OUTPUT_FILE="$CONTEXT_DIR/${SESSION}_${WINDOW}_${TIMESTAMP}.txt"
tmux capture-pane -p -S -500 > "$OUTPUT_FILE" 2>/dev/null || true

# Keep only last 50 context files
ls -t "$CONTEXT_DIR"/*.txt 2>/dev/null | tail -n +51 | xargs rm -f 2>/dev/null || true

echo "$(date) Context saved: $OUTPUT_FILE ($TRIGGER)" >> "$CONTEXT_DIR/save.log"
```

---

## Example 5: Pre-Flight Check Before Agent Session

Run system checks before starting a Claude Code session to ensure the environment is ready.

```bash
#!/bin/bash
# pre-agent-check.sh
# Verify system is ready for agent development work

set -euo pipefail

ERRORS=0

check() {
    local desc="$1" test_cmd="$2"
    if eval "$test_cmd" > /dev/null 2>&1; then
        echo "OK   $desc"
    else
        echo "FAIL $desc"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "=== Pre-Agent Flight Check ==="
echo ""

# Infrastructure
check "Docker running" "systemctl is-active docker"
check "PostgreSQL healthy" "docker exec nero-postgres pg_isready -U nero -q"
check "Redis healthy" "docker exec nero-redis redis-cli ping"
check "RabbitMQ healthy" "docker exec nero-rabbitmq rabbitmq-diagnostics -q ping"

# Services
check "nero-core active" "systemctl --user is-active nero-core"
check "nero-channel-web active" "systemctl --user is-active nero-channel-web"

# Resources
MEM_AVAIL=$(free -m | awk '/Mem:/ {print $7}')
check "Memory available (${MEM_AVAIL}MB)" "[ $MEM_AVAIL -gt 4096 ]"

DISK_FREE=$(df / --output=avail | tail -1 | tr -d ' ')
DISK_FREE_GB=$((DISK_FREE / 1048576))
check "Disk free (${DISK_FREE_GB}GB)" "[ $DISK_FREE_GB -gt 10 ]"

WATCHES=$(cat /proc/sys/fs/inotify/max_user_watches)
check "inotify watches ($WATCHES)" "[ $WATCHES -ge 524288 ]"

FD_LIMIT=$(ulimit -n)
check "File descriptor limit ($FD_LIMIT)" "[ $FD_LIMIT -ge 65536 ]"

echo ""
if [ $ERRORS -gt 0 ]; then
    echo "RESULT: $ERRORS checks failed. Fix issues before starting agent."
    exit 1
else
    echo "RESULT: All checks passed. Ready for agent work."
fi
```
