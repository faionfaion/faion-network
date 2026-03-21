# Agent Dev Tuning Checklist

## Kernel Tuning

### inotify Limits

- [ ] Check current limits: `cat /proc/sys/fs/inotify/max_user_watches`
- [ ] Set max_user_watches to 524288
- [ ] Set max_user_instances to 1024
- [ ] Set max_queued_events to 65536
- [ ] Create `/etc/sysctl.d/60-inotify.conf`
- [ ] Apply: `sudo sysctl -p /etc/sysctl.d/60-inotify.conf`
- [ ] Verify: `sysctl fs.inotify.max_user_watches`

### File Descriptor Limits

- [ ] Check current limits: `ulimit -n`
- [ ] Create `/etc/security/limits.d/nero.conf`
- [ ] Set nofile soft/hard: 65536/131072
- [ ] Set nproc soft/hard: 4096/8192
- [ ] Re-login to apply
- [ ] Verify: `ulimit -n` shows new value

## Memory Management

### Swap

- [ ] Check current swap: `swapon --show`
- [ ] Create swap file if none exists (4-8GB for 30GB RAM server)
- [ ] Set permissions: `chmod 600 /swapfile`
- [ ] Add to /etc/fstab for persistence
- [ ] Set swappiness to 10: `/etc/sysctl.d/60-swap.conf`
- [ ] Verify: `free -h` shows swap

### OOM Tuning

- [ ] Set OOMScoreAdjust in critical service unit files
- [ ] Set MemoryMax for each service (prevent unbounded growth)
- [ ] Set MemoryHigh for soft throttling
- [ ] Verify OOM configuration: `systemctl --user show service -p OOMScoreAdjust`

## Claude Code Configuration

### settings.json

- [ ] Create/update `~/.claude/settings.json`
- [ ] Configure allowed Bash commands (git, python, docker, etc.)
- [ ] Configure denied commands (dangerous operations)
- [ ] Set environment variables if needed

### Hooks (Optional)

- [ ] Configure PreToolUse hooks (audit logging, validation)
- [ ] Configure Notification hooks (Telegram alerts when agent needs attention)
- [ ] Test hooks with a simple agent session

### Project-Level Config

- [ ] Create `.claude/settings.json` in each project
- [ ] Create `CLAUDE.md` with project context
- [ ] Create `.claude/commands/` for custom slash commands (optional)

## MCP Servers (Optional)

- [ ] Configure filesystem MCP server if needed
- [ ] Configure database MCP server if needed
- [ ] Test MCP servers work with agent
- [ ] Document MCP server configurations

## tmux Session Management

- [ ] tmux installed and configured
- [ ] Linger enabled for user: `loginctl enable-linger`
- [ ] Named sessions for agent work
- [ ] tmux config optimized (mouse, scrollback, status bar)
- [ ] Agent sessions persist across SSH disconnect

## Worktree Patterns

- [ ] Understand worktree basics: `git worktree list`
- [ ] Create worktree directory convention (e.g., `../repo-branch-name`)
- [ ] Test worktree creation and merge workflow
- [ ] Set up cleanup procedure for stale worktrees

## Filesystem Tuning

- [ ] Mount with noatime in /etc/fstab
- [ ] Check I/O scheduler for SSD: `cat /sys/block/*/queue/scheduler`
- [ ] Set appropriate scheduler (none/mq-deadline for SSD)

## Parallel Agent Execution

- [ ] Plan resource allocation per agent (CPU, memory)
- [ ] Create tmux sessions/windows for each agent
- [ ] Set up resource limits (cgroups or systemd-run)
- [ ] Test parallel agent execution doesn't cause OOM

## Verification

- [ ] Run Claude Code agent and verify no "too many open files" errors
- [ ] Verify file watching works on large project
- [ ] Confirm agent survives LLM response memory spike
- [ ] Confirm tmux sessions persist after SSH disconnect
- [ ] Monitor resource usage during typical agent session
- [ ] Test multiple agents running simultaneously

## Documentation

- [ ] Document inotify and limit changes in server runbook
- [ ] Document Claude Code configuration decisions
- [ ] Note which hooks are enabled and why
- [ ] Document worktree workflow for the team/future self
