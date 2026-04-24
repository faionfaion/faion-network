# tmux Power User Examples

Real-world tmux configurations and workflows from the NERO AI platform server.

## Example 1: NERO Server tmux Config (Actual)

**Server:** Ubuntu 24.04, Hetzner CX53

### Current ~/.tmux.conf

```bash
# tmux.conf — Mouse support + productivity settings

# Enable mouse support
set -g mouse on

# Copy mode vi-like bindings
setw -g mode-keys vi
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-selection-and-cancel

# Prefix: Ctrl+A
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# Split windows with | and -
bind | split-window -h
bind - split-window -v

# Navigate panes with Ctrl+arrow
bind -n C-Up select-pane -U
bind -n C-Down select-pane -D
bind -n C-Left select-pane -L
bind -n C-Right select-pane -R

# Window navigation with Alt+number
bind -n M-1 select-window -t 1
bind -n M-2 select-window -t 2
bind -n M-3 select-window -t 3
bind -n M-4 select-window -t 4
bind -n M-5 select-window -t 5

# Status bar
set -g status-bg black
set -g status-fg white
set -g status-interval 1
set -g status-left " #S "
set -g status-right-length 120
set -g status-right '#(~/.tmux-system.sh) '

# Terminal colors
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",xterm-256color:RGB"

# Mouse copy
bind -T copy-mode-vi MouseDragEnd1Pane send-keys -X copy-selection-and-cancel

# Plugins
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

# Resurrect
set -g @resurrect-capture-pane-contents 'on'
set -g @resurrect-strategy-vim 'session'

# Continuum
set -g @continuum-restore 'on'
set -g @continuum-save-interval '15'

# Initialize TPM
run '~/.tmux/plugins/tpm/tpm'
```

### Current Status Bar Script (~/.tmux-system.sh)

```bash
#!/bin/bash
cyan="#[fg=colour6]"
yellow="#[fg=colour3]"
orange="#[fg=colour208]"
red="#[fg=colour1]"
dim="#[dim]"
r="#[default]"

ncpu=$(nproc 2>/dev/null || echo 1)
mem_pct=$(awk '/MemTotal/{t=$2} /MemAvailable/{a=$2} END{printf "%d", (t-a)*100/t}' /proc/meminfo)
cpu_pct=$(awk '{printf "%d", $1 * 100 / '"$ncpu"'}' /proc/loadavg)
disk_pct=$(df -h / | awk 'NR==2{print $5}' | tr -d '%')

mc="$cyan"; [ "$mem_pct" -ge 50 ] && mc="$yellow"; [ "$mem_pct" -ge 70 ] && mc="$orange"; [ "$mem_pct" -ge 90 ] && mc="$red"
cc="$cyan"; [ "$cpu_pct" -ge 50 ] && cc="$yellow"; [ "$cpu_pct" -ge 70 ] && cc="$orange"; [ "$cpu_pct" -ge 90 ] && cc="$red"
dc="$cyan"; [ "$disk_pct" -ge 50 ] && dc="$yellow"; [ "$disk_pct" -ge 70 ] && dc="$red"

printf "%sM:%s%s%%%s %sC:%s%s%%%s %sD:%s%s%%%s" "$dim" "$mc" "$mem_pct" "$r" "$dim" "$cc" "$cpu_pct" "$r" "$dim" "$dc" "$disk_pct" "$r"
```

Output: `M:23% C:5% D:41%` (color-coded based on thresholds)

## Example 2: Daily Workflow

### Morning Startup

```bash
# SSH into server
ssh nero

# Start or attach to main session
tmux a -t nero || ~/bin/tmux-nero.sh
```

### Typical Session Layout

```
Session: nero
  Window 1 "workspace":  [Claude Code agent running]
  Window 2 "services":   [systemctl status]
  Window 3 "logs":       [3 panes: core | web | tg logs]
  Window 4 "infra":      [docker ps, docker compose]
  Window 5 "git":        [git operations across repos]
```

### Working with Multiple Projects

```bash
# Start NERO session
tmux new -s nero -c ~/workspace

# Start MeetingTax session (separate)
tmux new -s mtax -c ~/projects/meetingtax

# Switch between sessions
# prefix + s  -> interactive session picker
# Or: tmux switch -t mtax
```

## Example 3: Log Monitoring Layout

### Three-Pane Log View

```bash
# Create a window with 3 log panes
tmux new-window -n logs

# Pane 1: nero-core logs
tmux send-keys "journalctl --user -f -u nero-core --no-hostname" Enter

# Pane 2: nero-channel-web logs (right side)
tmux split-window -h
tmux send-keys "journalctl --user -f -u nero-channel-web --no-hostname" Enter

# Pane 3: nero-channel-tg logs (bottom right)
tmux split-window -v
tmux send-keys "journalctl --user -f -u nero-channel-tg --no-hostname" Enter

# Go back to first pane
tmux select-pane -t 0
```

Layout:
```
+---------------------------+---------------------------+
|                           |                           |
|   nero-core logs          |   nero-channel-web logs   |
|                           |                           |
|                           +---------------------------+
|                           |                           |
|                           |   nero-channel-tg logs    |
|                           |                           |
+---------------------------+---------------------------+
```

## Example 4: Session Restore After Server Reboot

### What Happens During Auto-Reboot (4 AM, unattended upgrades)

1. tmux-continuum auto-saved session state 15 minutes before reboot
2. Server reboots
3. User SSH-es in and starts tmux
4. tmux-continuum auto-restores the saved session layout
5. All windows and pane splits are recreated
6. Working directories are restored

```bash
# After reboot, just attach:
$ tmux a -t nero
# Session layout is restored automatically!

# If auto-restore didn't work:
# prefix + Ctrl+R  (manual restore)
```

### What Gets Saved/Restored

| Saved | Restored |
|-------|----------|
| Session names | Yes |
| Window names | Yes |
| Window layout | Yes |
| Pane layout (splits) | Yes |
| Working directories | Yes |
| Pane contents (scroll history) | Yes (with capture-pane-contents) |
| Running commands | No (must restart manually) |
| Environment variables | No |

## Example 5: Copy Mode Workflow

### Copying Text from Log Output

```
1. Enter copy mode:           prefix + [
2. Navigate to start of text:  Use vi keys (h/j/k/l, /, ?)
3. Start selection:            v
4. Move to end of selection:   Use vi keys
5. Copy:                       y
6. Exit copy mode:             q
7. Paste:                      prefix + ]
```

### Search in Scroll Buffer

```
1. Enter copy mode:  prefix + [
2. Search backward:  ? (then type search term)
3. Search forward:   / (then type search term)
4. Next match:       n
5. Previous match:   N
```

### Copy with Mouse

```
1. Select text with mouse:     Click and drag
2. Auto-copied on release
3. Paste:                      prefix + ]

# For terminal-native selection (bypassing tmux):
# Hold Shift while selecting with mouse
```

## Example 6: Nested tmux (Local + Remote)

### Setup: Local tmux on Mac/Linux, Remote tmux on server

```bash
# Local .tmux.conf: Ctrl+A as prefix
set -g prefix C-a

# Remote .tmux.conf: also Ctrl+A
# To send prefix to remote: Ctrl+A, Ctrl+A

# Or: use different prefix for local and remote
# Local: Ctrl+A
# Remote: Ctrl+B (default)
```

### Workflow

```bash
# On local machine, in tmux:
# Window 1: local development
# Window 2: ssh nero (enters remote tmux)

# In Window 2 (remote tmux):
# prefix = Ctrl+A (goes to LOCAL tmux)
# Ctrl+A, Ctrl+A = sends Ctrl+A to REMOTE tmux

# To switch remote tmux window:   Ctrl+A, Ctrl+A, n
# To split remote tmux pane:       Ctrl+A, Ctrl+A, |
# To switch local tmux window:     Ctrl+A, n
```

## Example 7: Quick One-Liners

```bash
# Kill all sessions
tmux kill-server

# List all panes across all sessions
tmux list-panes -a

# Send command to a specific pane
tmux send-keys -t nero:logs.0 "journalctl --user -f -u nero-core" Enter

# Capture pane output to file
tmux capture-pane -t nero:logs.0 -p > /tmp/core-logs.txt

# Move pane to another window
# In the pane: prefix + !  (break to new window)

# Join a window as a pane in current window
# prefix + :  then  join-pane -s :2  (joins window 2 as pane)

# Synchronize input to all panes (type in all at once)
# prefix + :  then  setw synchronize-panes on
# Useful for: running same command on multiple servers

# Clear scrollback buffer
tmux clear-history
```
