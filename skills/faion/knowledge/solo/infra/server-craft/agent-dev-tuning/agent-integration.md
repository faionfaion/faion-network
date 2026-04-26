# Agent Integration — Agent Dev Tuning

## When to use
- Setting up a VPS to run Claude Code sessions (local or remote SSH)
- Multiple parallel agent instances on the same server are conflicting for resources
- Agents are being killed mid-task due to OOM during large LLM response processing
- Claude Code reporting "too many open files" or inotify watch limit errors on large repos
- Setting up worktree-based parallel task execution for NERO or faion-network agents
- Configuring tmux sessions that persist after SSH disconnects

## When NOT to use
- Local macOS/Windows development machines — inotify is Linux-only; use Watchman or Polling on macOS
- Kubernetes pods running CI agents — node-level tuning is needed, not user-space configuration
- Ephemeral cloud instances that are destroyed after each job — tuning is not worth the setup overhead
- Single-run batch scripts that do not use file watchers — inotify tuning provides no benefit

## Where it fails / limitations
- `systemd-run --scope` for per-agent resource limits requires a live user session (linger must be enabled); fails in cron jobs
- Git worktree conflicts occur when two agents commit to the same branch simultaneously — the second `git commit` succeeds but the push is rejected; must use separate branches per agent
- tmux session capture (`tmux capture-pane`) truncates at buffer limit; long agent outputs are silently cut off
- MCP server processes consume their own file descriptors and inotify watches; must be accounted for in the limit calculations
- `nice -n -5` requires either root or `CAP_SYS_NICE` capability; on standard VPS this will silently clamp to nice 0 for non-root users
- `ionice` with class 1 (realtime) requires root; class 2 (best-effort) with priority 0 is the max available to normal users

## Agentic workflow
A provisioning agent runs the full server tuning sequence: raise inotify limits, create swap, set swappiness, increase nofile PAM limits, and verify all changes. It then creates a `~/.claude/settings.json` with a curated `allow` list for the target project. For parallel agent tasks, each task gets its own git worktree and tmux window; a coordinating agent creates the worktrees, launches subagents in separate tmux panes, monitors completion via sentinel files, and merges results after human review. Resource limits are enforced via `systemd-run --user --scope` wrappers per agent process.

### Recommended subagents
- `faion` (infra/server-craft/kernel-tuning) — inotify, sysctl, BBR for the underlying kernel
- `faion` (infra/server-craft/swap-memory-management) — swap and MemoryMax for agent OOM protection
- `faion` (infra/server-craft/systemd-user-services) — linger, per-service resource limits
- `faion` (infra/server-craft/git-server-workflow) — worktree lifecycle for parallel agents
- `faion` (infra/server-craft/tmux-power-user) — session persistence and multi-agent layout

### Prompt pattern
```
Tune this server for Claude Code agent workloads:
1. Raise inotify: echo 'fs.inotify.max_user_watches=524288\nfs.inotify.max_user_instances=1024' | sudo tee /etc/sysctl.d/60-inotify.conf && sudo sysctl -p /etc/sysctl.d/60-inotify.conf
2. Set nofile: echo 'nero soft nofile 65536\nnero hard nofile 131072' | sudo tee /etc/security/limits.d/nero.conf
3. Enable linger: loginctl enable-linger
4. Create swap if absent: (check swapon --show first)
5. Verify: cat /proc/sys/fs/inotify/max_user_watches && ulimit -n
```

```
Set up parallel agent worktrees for tasks [task-001, task-002, task-003]:
For each task:
  git -C ~/workspace/repos/nero-core worktree add ~/workspace/agents/<task-id> -b agent/<task-id>
Create tmux session 'agents' with one window per task.
Each window: cd ~/workspace/agents/<task-id>
Report worktree paths when done.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `sysctl` | Kernel parameter tuning (inotify, TCP) | procps |
| `loginctl enable-linger` | Keep user services running after logout | systemd |
| `tmux` | Terminal multiplexer for session persistence | `apt install tmux` |
| `git worktree` | Multiple working trees from one repo | git 2.5+ |
| `systemd-run --user --scope` | Resource-limited process execution | systemd |
| `ionice` | I/O scheduling priority | util-linux |
| `nice` | Process CPU priority | coreutils |
| `ulimit` | Per-shell resource limits | bash built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Claude Code | SaaS/OSS client | Yes (CLI) | Primary agent runtime; config in `~/.claude/settings.json` |
| MCP filesystem server | OSS | Yes (npx) | Extends agent file access; each instance uses file descriptors |
| MCP postgres server | OSS | Yes (npx) | DB access for agents; configure in `~/.claude/settings.json` mcpServers block |
| tmux | OSS | Yes (CLI) | Session persistence; agents can be launched via `tmux send-keys` |
| Telegram Bot API | SaaS | Yes (curl/HTTP) | Notification channel for agent task completion events |

## Templates & scripts
See `templates.md` for full `agent-workspace.sh` and `settings.json` templates. Inline agent resource wrapper:

```bash
#!/bin/bash
# run-agent.sh — launch Claude Code with resource limits in a named tmux window
# Usage: bash run-agent.sh <session-name> <window-name> <work-dir> [memory-limit]
SESSION="${1:?session name required}"
WINDOW="${2:?window name required}"
WORKDIR="${3:?work dir required}"
MEM="${4:-4G}"

tmux new-window -t "$SESSION" -n "$WINDOW" 2>/dev/null || true
tmux send-keys -t "${SESSION}:${WINDOW}" \
  "cd $WORKDIR && systemd-run --user --scope --property=MemoryMax=$MEM --property=CPUQuota=400% -- claude" \
  C-m
echo "Agent started in ${SESSION}:${WINDOW} (MemoryMax=$MEM)"
```

## Best practices
- Enable linger (`loginctl enable-linger`) before starting any long-running agent sessions — without it, all user processes including tmux sessions are killed on SSH disconnect
- One git worktree per agent task, one tmux window per worktree — this makes it trivial to inspect, pause, or kill individual agent tasks without affecting others
- Set `CLAUDE_CODE_AGENT=true` in the environment (via `settings.json` env block) — some MCP servers and hooks check for this to suppress interactive prompts
- Keep the `allow` list in `settings.json` explicit and minimal — overly permissive lists (`Bash(*)`) make audit harder and increase blast radius of agent mistakes
- Never share a `.venv` directory between parallel agent worktrees; pip installs from multiple processes into the same venv cause corruption; each worktree that installs packages needs its own venv
- Log agent start time, worktree path, task ID, and completion status to a structured log file for post-session review

## AI-agent gotchas
- Agents must check that tmux is running (`tmux list-sessions`) before calling `tmux send-keys`; the error message when tmux is not running is cryptic and does not mention tmux is absent
- `git worktree add` fails if the target branch already exists as a local branch; agents must use `-b <new-branch>` for new branches or `<existing-branch>` for an existing one — mixing them causes error
- `systemd-run --user --scope` creates a transient unit; the unit disappears when the process exits; agents must not use `systemctl --user status` on the scope name after the process exits
- MCP server processes started by Claude Code share the parent's file descriptor table; raising `nofile` in the Claude Code process is sufficient but only if linger is active and the process started from the user session
- Parallel agents writing to the same log file will interleave lines; each agent must write to a separate log file (`/tmp/agent-<task-id>.log`) or use a file lock

## References
- https://docs.anthropic.com/en/docs/claude-code
- https://docs.anthropic.com/en/docs/claude-code/settings
- https://git-scm.com/docs/git-worktree
- https://www.freedesktop.org/software/systemd/man/systemd-run.html
- https://man7.org/linux/man-pages/man1/tmux.1.html
