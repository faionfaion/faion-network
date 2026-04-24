# Agent Dev Tuning

Server optimization for AI agent development workflows. Covers Claude Code configuration (settings.json, hooks, worktrees), kernel tuning for file watchers, swap and memory management for LLM workloads, OOM killer tuning, process priority, tmux session preservation, MCP server patterns, and parallel agent execution.

## Overview

Running AI agents (Claude Code, Cursor, Copilot) on a VPS requires different tuning than typical web hosting. Agents create many file watchers, spawn subprocesses, consume memory in bursts, and benefit from fast file I/O.

| Concern | Impact | Solution |
|---------|--------|----------|
| inotify limits | Agent can't watch files | Increase `fs.inotify.max_user_watches` |
| Memory spikes | OOM kills during LLM calls | Swap + MemoryMax tuning |
| File descriptor limits | Too many open files | Increase `LimitNOFILE` |
| Session persistence | Lose agent context on disconnect | tmux + linger |
| Parallel agents | Resource contention | CPU/memory quotas per agent |
| Slow file operations | Agent waits on I/O | SSD, noatime, scheduler tuning |

## inotify Limits

File watchers are used by editors, agents, build tools, and hot-reload systems. The default limit (8192) is insufficient for large projects.

### Default vs Recommended

| Setting | Default | Recommended | Purpose |
|---------|---------|-------------|---------|
| max_user_watches | 8,192 | 524,288 | Max inotify watches per user |
| max_user_instances | 128 | 1,024 | Max inotify instances per user |
| max_queued_events | 16,384 | 65,536 | Max queued inotify events |

### Configuration

```bash
# /etc/sysctl.d/60-inotify.conf
fs.inotify.max_user_watches = 524288
fs.inotify.max_user_instances = 1024
fs.inotify.max_queued_events = 65536
```

```bash
# Apply immediately
sudo sysctl -p /etc/sysctl.d/60-inotify.conf

# Verify
cat /proc/sys/fs/inotify/max_user_watches
# 524288
```

### Check Current Usage

```bash
# Count current inotify watches per process
find /proc/*/fd -lname anon_inode:inotify 2>/dev/null | \
    while read fd; do
        pid=$(echo "$fd" | cut -d/ -f3)
        count=$(cat "/proc/$pid/fdinfo/$(basename "$fd")" 2>/dev/null | grep -c inotify)
        comm=$(cat "/proc/$pid/comm" 2>/dev/null)
        echo "$count $comm ($pid)"
    done | sort -rn | head -10
```

## Swap for LLM Workloads

LLM API calls can trigger memory spikes when processing large responses, tool calls, or context windows. Swap provides a safety net.

### Recommended Swap Size

| Server RAM | Swap Size | Rationale |
|-----------|-----------|-----------|
| 8 GB | 4 GB | 50% of RAM |
| 16 GB | 4-8 GB | 25-50% of RAM |
| 30 GB | 4-8 GB | Safety buffer |
| 64+ GB | 4 GB | Minimal, just for OOM prevention |

### Swap Configuration

```bash
# Create swap file
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Persist in /etc/fstab
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Tune swappiness (lower = prefer RAM)
echo "vm.swappiness = 10" | sudo tee /etc/sysctl.d/60-swap.conf
sudo sysctl -p /etc/sysctl.d/60-swap.conf
```

| Setting | Value | Meaning |
|---------|-------|---------|
| vm.swappiness | 10 | Only swap when memory pressure is high |
| vm.vfs_cache_pressure | 50 | Default, balanced inode/dentry cache |

## OOM Killer Tuning

When the system runs out of memory, the OOM killer selects a process to kill. You can influence which processes it targets.

### Per-Process OOM Score

```bash
# Check OOM score for a process
cat /proc/$(pgrep -f nero-core | head -1)/oom_score

# Set OOM adjustment (-1000 to 1000, higher = more likely to be killed)
# Protect critical services
echo -100 | sudo tee /proc/$(pgrep -f nero-core | head -1)/oom_score_adj

# Make a process more likely to be killed
echo 500 | sudo tee /proc/$(pgrep -f jupyter | head -1)/oom_score_adj
```

### In systemd Services

```ini
[Service]
# Protect from OOM (-1000 to 1000)
OOMScoreAdjust=-500

# Or use systemd's OOM policy
OOMPolicy=continue   # Don't kill the entire service on OOM
# OOMPolicy=kill      # Default: kill the service
# OOMPolicy=stop      # Stop the service
```

### systemd Memory Controls

```ini
[Service]
# Hard limit (SIGKILL if exceeded)
MemoryMax=2G

# Soft limit (throttled, not killed)
MemoryHigh=1536M

# Minimum guarantee
MemoryMin=256M

# Swap limit for this service
MemorySwapMax=512M
```

## PAM Limits

Set per-user resource limits for agent workloads.

```bash
# /etc/security/limits.d/nero.conf
nero  soft  nofile    65536
nero  hard  nofile    131072
nero  soft  nproc     4096
nero  hard  nproc     8192
nero  soft  memlock   unlimited
nero  hard  memlock   unlimited
```

| Limit | Purpose | Value |
|-------|---------|-------|
| nofile | Max open file descriptors | 65536 (soft), 131072 (hard) |
| nproc | Max processes/threads | 4096 (soft), 8192 (hard) |
| memlock | Max locked memory | unlimited (for mmap) |

## Claude Code Configuration

### settings.json

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(python *)",
      "Bash(pip *)",
      "Bash(npm *)",
      "Bash(npx *)",
      "Bash(node *)",
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
      "Bash(wc *)",
      "Bash(head *)",
      "Bash(tail *)",
      "Bash(sort *)",
      "Bash(diff *)",
      "Bash(ssh *)",
      "Bash(rsync *)"
    ],
    "deny": [
      "Bash(sudo rm -rf /)",
      "Bash(:(){ :|:& };:)"
    ]
  },
  "env": {
    "CLAUDE_CODE_AGENT": "true"
  }
}
```

### Hooks

Claude Code hooks run scripts at specific lifecycle points.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date '+%H:%M:%S') Bash: $TOOL_INPUT\" >> /tmp/claude-code-audit.log"
          }
        ]
      }
    ],
    "PostToolUse": [],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/home/nero/workspace/scripts/notify-telegram.sh \"Claude Code notification: $NOTIFICATION_MESSAGE\""
          }
        ]
      }
    ]
  }
}
```

## Worktree Patterns for Parallel Agents

Git worktrees let multiple agents work on the same repository simultaneously without conflicts.

```bash
# Create worktree for agent task
git worktree add ../nero-core-feature-123 feature/123

# Agent works in the worktree
cd ../nero-core-feature-123
# ... agent makes changes ...

# Merge back
cd ../nero-core
git merge feature/123

# Clean up worktree
git worktree remove ../nero-core-feature-123
```

### Worktree Management

```bash
# List all worktrees
git worktree list

# Prune stale worktrees
git worktree prune

# Create worktree from specific commit
git worktree add ../nero-core-hotfix HEAD~5
```

## tmux Session Preservation

Agents should run in tmux sessions that persist across SSH disconnects.

### Session Management

```bash
# Create named session for agent
tmux new-session -d -s agent-1 -n "claude"

# Attach to session
tmux attach -t agent-1

# Detach (Ctrl+B, D) -- agent keeps running

# List sessions
tmux list-sessions
```

### tmux Hooks for Agent Context

Save agent context (like prompt history) when tmux events occur:

```bash
# ~/.tmux.conf
# Save pane content on detach
set-hook -g client-detached 'run-shell "tmux capture-pane -t {previous} -p > /tmp/tmux-last-pane.txt"'
```

## MCP Server Patterns

Model Context Protocol (MCP) servers extend agent capabilities.

### Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/nero/workspace"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://nero:pass@localhost:5432/nero_db"
      }
    }
  }
}
```

## Parallel Agent Execution

Running multiple Claude Code instances simultaneously.

### Resource Allocation

| Agent | tmux Session | CPU Quota | Memory | Purpose |
|-------|-------------|-----------|--------|---------|
| Agent 1 | agent-main | 400% | 4G | Primary development |
| Agent 2 | agent-review | 200% | 2G | Code review |
| Agent 3 | agent-docs | 200% | 2G | Documentation |

### Per-Agent Resource Limits (cgroups)

```bash
# Create cgroup slice for agents
sudo mkdir -p /sys/fs/cgroup/user.slice/user-$(id -u).slice/agent-1.scope

# Or use systemd-run for resource-limited execution
systemd-run --user --scope \
    --property=MemoryMax=4G \
    --property=CPUQuota=400% \
    -- claude --session agent-1
```

### tmux Multi-Agent Layout

```bash
#!/bin/bash
# agent-workspace.sh
# Set up tmux with multiple agent sessions

# Main development agent
tmux new-session -d -s agents -n "main"
tmux send-keys "cd ~/workspace/repos/nero-core && claude" C-m

# Code review agent
tmux new-window -t agents -n "review"
tmux send-keys "cd ~/workspace/repos/nero-core && claude --resume review" C-m

# Monitoring agent
tmux new-window -t agents -n "monitor"
tmux send-keys "cd ~/workspace && claude --resume monitor" C-m

tmux attach -t agents
```

## Performance Tuning

### Filesystem Tuning

```bash
# Mount with noatime (reduces write operations)
# /etc/fstab
/dev/sda1 / ext4 defaults,noatime 0 1

# Or remount without reboot
sudo mount -o remount,noatime /
```

### I/O Scheduler

```bash
# Check current scheduler
cat /sys/block/sda/queue/scheduler

# For SSDs, use 'none' (noop) or 'mq-deadline'
echo "none" | sudo tee /sys/block/sda/queue/scheduler

# Persist via udev rule
echo 'ACTION=="add|change", KERNEL=="sd*", ATTR{queue/scheduler}="none"' | \
    sudo tee /etc/udev/rules.d/60-scheduler.conf
```

### Process Priority

```bash
# Run agent with higher priority (lower nice value)
nice -n -5 claude

# In systemd service
[Service]
Nice=-5

# For I/O priority
ionice -c 2 -n 0 claude   # Best-effort, highest priority
```

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "Too many open files" | nofile limit too low | Increase in limits.d and systemd |
| "No space left on device" (inotify) | max_user_watches reached | Increase in sysctl |
| Agent killed during LLM call | OOM with no swap | Add swap, increase MemoryMax |
| Agent slow on large repos | No inotify, falling back to polling | Increase max_user_watches |
| tmux session gone | Server reboot, no linger | Enable linger, use systemd |
| Worktree conflicts | Dirty worktree | Clean or stash before merge |

## Related Methodologies

- `swap-memory-management/` -- detailed swap tuning
- `kernel-tuning/` -- inotify, sysctl, network tuning
- `tmux-power-user/` -- tmux configuration and workflows
- `claude-code-hooks/` -- Claude Code hooks and settings
- `systemd-user-services/` -- service resource limits
