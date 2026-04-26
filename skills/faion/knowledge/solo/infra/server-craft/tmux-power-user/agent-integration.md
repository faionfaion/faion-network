# Agent Integration — tmux Power User

## When to use
- Developer works primarily over SSH and needs persistent sessions that survive disconnection
- Running multiple concurrent AI agent sessions that must stay live without active user supervision
- Building a named-session workflow where each project/context has a dedicated tmux session
- Setting up a monitoring dashboard with persistent panes (htop, logs, docker stats)
- Scripting session layouts that an agent or cron job can create/restore automatically

## When NOT to use
- Local-only workstation development where IDE terminal is sufficient
- Ephemeral CI/CD environments (tmux adds no value in non-interactive pipelines)
- Containerized deployments where the process is PID 1 (tmux makes no sense inside Docker)
- Terminals that don't support 256-color or proper escape sequences (some legacy SSH gateways)

## Where it fails / limitations
- `tmux-resurrect` restore silently skips panes whose working directory no longer exists
- `tmux-continuum` requires `set -g @continuum-restore 'on'` AND a server restart to first activate — often missed
- TPM plugin install (`prefix + I`) requires internet access from the server; fails on air-gapped machines
- Copy-to-clipboard (`tmux-yank`) requires `xclip`/`xsel` on local + SSH agent forwarding or OSC52 terminal support
- Status bar scripts (`~/.tmux-system.sh`) fail silently if not executable — status bar shows empty
- Nested tmux (local + remote) creates prefix confusion; requires explicit prefix-within-prefix discipline
- `set -g default-terminal "screen-256color"` with wrong `$TERM` on connecting client causes color artifacts

## Agentic workflow
Agents can create, query, and control tmux sessions via the `tmux` CLI. A subagent can spin up a named session, send keystrokes to a pane via `send-keys`, and read pane content via `capture-pane`. This enables fully headless agent-driven workflows: launch a process in a session, poll its output, detect completion, and clean up. Claude Code's own long-running tool calls benefit from session persistence when the agent is invoked over SSH.

### Recommended subagents
- `faion-sdd-executor-agent` — can use tmux to run parallel build/test panes during SDD task execution
- `nero-sdd-executor-agent` — NERO-specific agent sessions for long-running AI pipeline tasks

### Prompt pattern
```
Create a tmux session named 'deploy' with this layout:
- Pane 0: run `bash ~/workspace/deploy/deploy-be.sh`
- Pane 1 (split horizontal): tail -f /var/log/faion-api.log
After deploy script exits with code 0, send "All done" to pane 1.
Use tmux send-keys and capture-pane to monitor progress.
```

```
Check if tmux session 'nero' exists. If not, create it with:
- Window 0 "core": cd ~/workspace/repos/nero-core
- Window 1 "logs": journalctl --user -u nero-core -f
- Window 2 "monitor": htop
Attach if running interactively, detach otherwise.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tmux` | Terminal multiplexer | `apt install tmux` |
| `tpm` | tmux Plugin Manager | `git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm` |
| `tmux-resurrect` | Save/restore sessions across restarts | TPM: `tmux-plugins/tmux-resurrect` |
| `tmux-continuum` | Auto-save sessions every N minutes | TPM: `tmux-plugins/tmux-continuum` |
| `tmux-yank` | Copy to system clipboard over SSH | TPM: `tmux-plugins/tmux-yank` |
| `tmux-fzf` | Fuzzy-find sessions, windows, panes | TPM: `sainnhe/tmux-fzf` |
| `xclip` / `xsel` | Clipboard backend for tmux-yank | `apt install xclip` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| tmux | OSS | Yes — full CLI control | Sessions, windows, panes all scriptable |
| tmate | OSS/SaaS | Yes | Remote tmux session sharing; useful for pair-debugging with agents |
| Byobu | OSS | Partial | tmux wrapper with extra keybinds; less scriptable |
| GNU screen | OSS | Partial | Legacy alternative; fewer agent-friendly features |

## Templates & scripts
See `templates.md` for full session layout scripts.

Inline: agent-safe tmux session launcher (≤40 lines):
```bash
#!/bin/bash
# create-or-attach-session.sh
# Usage: ./create-or-attach-session.sh <session-name> [detach]
SESSION="${1:?session name required}"
DETACH="${2:-}"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "Session $SESSION already exists"
else
    tmux new-session -d -s "$SESSION" -n "main"
    tmux send-keys -t "${SESSION}:main" "cd ~/workspace" Enter

    tmux new-window -t "$SESSION" -n "logs"
    tmux send-keys -t "${SESSION}:logs" "journalctl --user -f" Enter

    tmux new-window -t "$SESSION" -n "monitor"
    tmux send-keys -t "${SESSION}:monitor" "htop" Enter

    tmux select-window -t "${SESSION}:main"
    echo "Session $SESSION created"
fi

if [ -z "$DETACH" ]; then
    tmux attach -t "$SESSION"
fi
```

## Best practices
- Name sessions after projects (`nero`, `faion`, `deploy`) not generic names (`dev`, `work`) — unambiguous across reconnects
- Use `prefix + d` to detach rather than closing the terminal — preserves all session state
- Always run `stow tmux` from dotfiles after server rebuild; without .tmux.conf, productivity collapses
- Set `set -g history-limit 50000` — default 2000 lines loses context in long log tails
- Use `set -g renumber-windows on` to keep window numbers contiguous after closing windows
- Script session layouts as `~/bin/tmux-<project>.sh` — document your own project setups
- For agent-controlled panes, use `tmux capture-pane -t <pane> -p` to read current output without TTY
- Test `tmux-resurrect` save/restore before relying on it: `prefix + Ctrl+s` to save, `prefix + Ctrl+r` to restore

## AI-agent gotchas
- `tmux send-keys` with `Enter` at the end executes the command immediately; omit `Enter` to stage without executing
- `tmux capture-pane -p` captures what is currently visible, not the full scroll buffer — use `-S -` for full history
- Agents running via `tmux send-keys` cannot read stdin; interactive prompts (sudo password, confirmation dialogs) will hang
- `tmux new-session -d` (detached) is required for agent use — `-d` prevents the session from attaching to agent's TTY
- If the agent runs inside a tmux session already, nested sessions need a different prefix or `TMUX=` env var cleared
- `tmux kill-session` in an agent is destructive — always verify session name before killing; a typo kills the wrong session
- Status bar script errors don't propagate — they silently display empty; agent must check `chmod +x` and script syntax separately

## References
- [tmux manual](https://man7.org/linux/man-pages/man1/tmux.1.html)
- [TPM — tmux Plugin Manager](https://github.com/tmux-plugins/tpm)
- [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect)
- [tmux-continuum](https://github.com/tmux-plugins/tmux-continuum)
- [tmux cheat sheet](https://tmuxcheatsheet.com/)
- [tmate — remote session sharing](https://tmate.io/)
