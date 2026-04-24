# tmux Power User

Comprehensive tmux configuration and workflow methodology for developers managing multiple projects and AI agent sessions on remote servers. Covers configuration, plugins, session management, themes, and productivity workflows.

## Scope

- tmux configuration structure and best practices
- Prefix key customization (Ctrl+A)
- Mouse support, vi mode, copy/paste
- Pane and window management (splits, navigation, resizing)
- Session management (create, attach, detach, list)
- Plugin ecosystem (TPM, resurrect, continuum, yank, fzf, thumbs)
- Status bar customization with system metrics
- Color themes (Tokyo Night, Catppuccin, Dracula)
- Session templates for project layouts
- Nested tmux (local + remote)

## Why This Matters

For a solo developer running an AI agent platform on a remote server:

- **Persistent sessions** survive SSH disconnections
- **Multiple panes** let you monitor logs, run agents, and edit simultaneously
- **Session management** keeps project contexts separate
- **Plugins** (resurrect, continuum) auto-save and restore sessions after reboot
- **Status bar** shows system metrics at a glance (RAM, CPU, disk)

## Architecture

```
~/.tmux.conf                      # Main configuration file
~/.tmux/                          # tmux data directory
  plugins/                        # TPM-managed plugins
    tpm/                          # tmux Plugin Manager
    tmux-resurrect/               # Save/restore sessions
    tmux-continuum/               # Auto-save sessions
    tmux-yank/                    # Copy to system clipboard
  resurrect/                      # Saved session data
~/.tmux-system.sh                 # Status bar script (custom)
```

## Key Concepts

### 1. Prefix Key

The prefix key is the gateway to all tmux commands. Default is `Ctrl+B`, but `Ctrl+A` is more ergonomic (closer to home row, same as GNU screen):

```bash
set -g prefix C-a
unbind C-b
bind C-a send-prefix
```

### 2. Mouse Support

Enable full mouse support for clicking panes, resizing, scrolling, and selecting text:

```bash
set -g mouse on
```

### 3. Vi Mode

Use vi-style keybindings in copy mode for efficient text selection:

```bash
setw -g mode-keys vi
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-selection-and-cancel
```

### 4. Splits and Navigation

| Action | Binding | Description |
|--------|---------|-------------|
| Horizontal split | `prefix + \|` | Split left/right |
| Vertical split | `prefix + -` | Split top/bottom |
| Navigate panes | `Ctrl+arrows` | Move between panes |
| Switch window | `Alt+1..9` | Jump to window by number |
| Resize pane | `prefix + H/J/K/L` | Resize in vi directions |

### 5. Sessions

Sessions are the top-level organizational unit in tmux:

| Command | Action |
|---------|--------|
| `tmux new -s name` | Create named session |
| `tmux attach -t name` | Attach to session |
| `tmux detach` or `prefix + d` | Detach from session |
| `tmux ls` | List sessions |
| `tmux kill-session -t name` | Kill a session |
| `tmux switch -t name` | Switch to session |
| `prefix + s` | Interactive session picker |

### 6. Plugins (TPM)

tmux Plugin Manager (TPM) manages plugins:

```bash
# Install TPM
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# In .tmux.conf:
set -g @plugin 'tmux-plugins/tpm'

# Install plugins: prefix + I
# Update plugins: prefix + U
```

#### Essential Plugins

| Plugin | Purpose |
|--------|---------|
| `tmux-resurrect` | Save and restore sessions (survives restart) |
| `tmux-continuum` | Auto-save sessions every 15 minutes |
| `tmux-yank` | Copy to system clipboard (works over SSH) |
| `tmux-fzf` | Fuzzy finder for sessions, windows, panes |
| `tmux-thumbs` | Quick copy of URLs, paths, hashes |

### 7. Status Bar

The status bar shows session info, window list, and custom metrics:

```bash
# Left: session name
set -g status-left " #S "

# Right: system metrics (via script)
set -g status-right '#(~/.tmux-system.sh) '

# Update interval (seconds)
set -g status-interval 1
```

### 8. Colors and Theme

True color support requires proper terminal configuration:

```bash
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",xterm-256color:RGB"
```

### 9. Session Templates

Scripts that create pre-configured tmux layouts for specific projects:

```bash
#!/bin/bash
# Start a new session with predefined layout
tmux new-session -d -s nero
tmux send-keys "cd ~/workspace/repos/nero-core" Enter
tmux split-window -h
tmux send-keys "cd ~/workspace/repos/nero-channel-web" Enter
tmux split-window -v
tmux send-keys "journalctl --user -f -u nero-core" Enter
tmux select-pane -t 0
tmux attach -t nero
```

### 10. Nested tmux

When SSH-ing from a local tmux into a remote tmux:

- Local prefix: `Ctrl+A`
- Remote prefix: `Ctrl+A, Ctrl+A` (send prefix through)
- Or use different prefix for local (`Ctrl+A`) and remote (`Ctrl+B`)

## Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Not installing TPM | Plugins don't work | `git clone` TPM first |
| Forgetting `prefix + I` after adding plugins | Plugin not loaded | Always run after adding to .tmux.conf |
| Wrong TERM setting | Colors broken, artifacts | Use screen-256color with RGB override |
| Mouse mode confuses copy | Can't select text normally | Hold Shift for terminal-native selection |
| resurrect not saving | Sessions lost on restart | Check @resurrect-capture-pane-contents |
| Status bar script not executable | Status shows nothing | `chmod +x ~/.tmux-system.sh` |

## Verification

```bash
# Check tmux version
tmux -V

# Check if TPM is installed
ls ~/.tmux/plugins/tpm/

# Check loaded plugins
tmux list-plugins 2>/dev/null || ls ~/.tmux/plugins/

# Check prefix key
tmux show-option -g prefix

# Check mouse mode
tmux show-option -g mouse

# Test status bar script
~/.tmux-system.sh
```

## Integration Points

| Component | Integration |
|-----------|------------|
| SSH | tmux sessions persist across SSH disconnections |
| systemd | Session templates can be started via systemd timer |
| Claude Code | Run Claude Code agents in dedicated tmux panes |
| Monitoring | Status bar shows system metrics |
| Git | Each project window can show git status |

## References

- [tmux manual](https://man7.org/linux/man-pages/man1/tmux.1.html)
- [TPM](https://github.com/tmux-plugins/tpm)
- [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect)
- [tmux cheat sheet](https://tmuxcheatsheet.com/)
