# tmux Power User Templates

Copy-paste ready tmux configurations, scripts, and session templates.

## Template 1: Complete .tmux.conf

```bash
# ~/.tmux.conf — Power User Configuration

# ============================================================
# PREFIX
# ============================================================
# Use Ctrl+A instead of Ctrl+B (easier to reach)
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# ============================================================
# GENERAL
# ============================================================
# Enable mouse (scroll, click, resize, select)
set -g mouse on

# Vi mode for copy
setw -g mode-keys vi

# Start window/pane numbering at 1
set -g base-index 1
setw -g pane-base-index 1

# Renumber windows when one is closed
set -g renumber-windows on

# Increase scrollback buffer
set -g history-limit 50000

# Faster escape time (for vim)
set -sg escape-time 10

# Focus events (for vim autoread)
set -g focus-events on

# ============================================================
# KEYBINDINGS
# ============================================================
# Reload config
bind r source-file ~/.tmux.conf \; display "Config reloaded"

# Split windows (intuitive keys)
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# New window in current directory
bind c new-window -c "#{pane_current_path}"

# Navigate panes with Ctrl+arrows (no prefix needed)
bind -n C-Up select-pane -U
bind -n C-Down select-pane -D
bind -n C-Left select-pane -L
bind -n C-Right select-pane -R

# Resize panes with prefix + H/J/K/L
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# Window navigation with Alt+number
bind -n M-1 select-window -t 1
bind -n M-2 select-window -t 2
bind -n M-3 select-window -t 3
bind -n M-4 select-window -t 4
bind -n M-5 select-window -t 5
bind -n M-6 select-window -t 6
bind -n M-7 select-window -t 7
bind -n M-8 select-window -t 8
bind -n M-9 select-window -t 9

# Swap windows
bind -r "<" swap-window -d -t -1
bind -r ">" swap-window -d -t +1

# ============================================================
# COPY MODE
# ============================================================
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-selection-and-cancel
bind -T copy-mode-vi C-v send-keys -X rectangle-toggle
bind -T copy-mode-vi MouseDragEnd1Pane send-keys -X copy-selection-and-cancel

# ============================================================
# STATUS BAR
# ============================================================
set -g status-position bottom
set -g status-style "bg=colour235,fg=colour248"
set -g status-interval 5

# Left: session name
set -g status-left-length 30
set -g status-left "#[fg=colour0,bg=colour4,bold] #S #[fg=colour4,bg=colour235,nobold] "

# Right: system metrics + time
set -g status-right-length 120
set -g status-right '#(~/.tmux-system.sh) #[fg=colour240]| #[fg=colour248]%H:%M '

# Window list
setw -g window-status-format " #I:#W "
setw -g window-status-current-format "#[fg=colour235,bg=colour4] #I:#W #[fg=colour4,bg=colour235]"
setw -g window-status-separator ""

# Pane borders
set -g pane-border-style "fg=colour240"
set -g pane-active-border-style "fg=colour4"

# Message style
set -g message-style "bg=colour4,fg=colour0"

# ============================================================
# TERMINAL
# ============================================================
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",xterm-256color:RGB"
set -ga terminal-overrides ",*256col*:RGB"

# ============================================================
# PLUGINS (TPM)
# ============================================================
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

# Resurrect settings
set -g @resurrect-capture-pane-contents 'on'
set -g @resurrect-strategy-vim 'session'

# Continuum settings (auto-save every 15 min, auto-restore on start)
set -g @continuum-restore 'on'
set -g @continuum-save-interval '15'

# Initialize TPM (MUST be at the very bottom)
run '~/.tmux/plugins/tpm/tpm'
```

## Template 2: Status Bar Script

File: `~/.tmux-system.sh`

```bash
#!/bin/bash
# tmux status bar — system metrics with color coding
# Colors change from cyan -> yellow -> orange -> red as usage increases

cyan="#[fg=colour6]"
yellow="#[fg=colour3]"
orange="#[fg=colour208]"
red="#[fg=colour1]"
dim="#[dim]"
r="#[default]"

# CPU (from load average, normalized to CPU count)
ncpu=$(nproc 2>/dev/null || echo 1)
cpu_pct=$(awk '{printf "%d", $1 * 100 / '"$ncpu"'}' /proc/loadavg)

# Memory (from /proc/meminfo)
mem_pct=$(awk '/MemTotal/{t=$2} /MemAvailable/{a=$2} END{printf "%d", (t-a)*100/t}' /proc/meminfo)

# Disk (root partition)
disk_pct=$(df -h / | awk 'NR==2{print $5}' | tr -d '%')

# Color selection based on thresholds
mc="$cyan"; [ "$mem_pct" -ge 50 ] && mc="$yellow"; [ "$mem_pct" -ge 70 ] && mc="$orange"; [ "$mem_pct" -ge 90 ] && mc="$red"
cc="$cyan"; [ "$cpu_pct" -ge 50 ] && cc="$yellow"; [ "$cpu_pct" -ge 70 ] && cc="$orange"; [ "$cpu_pct" -ge 90 ] && cc="$red"
dc="$cyan"; [ "$disk_pct" -ge 50 ] && dc="$yellow"; [ "$disk_pct" -ge 70 ] && dc="$orange"; [ "$disk_pct" -ge 90 ] && dc="$red"

printf "%sM:%s%s%%%s %sC:%s%s%%%s %sD:%s%s%%%s" \
    "$dim" "$mc" "$mem_pct" "$r" \
    "$dim" "$cc" "$cpu_pct" "$r" \
    "$dim" "$dc" "$disk_pct" "$r"
```

## Template 3: NERO Platform Session Template

File: `~/bin/tmux-nero.sh`

```bash
#!/bin/bash
# tmux-nero.sh — Create NERO platform tmux session with predefined layout

SESSION="nero"

# Kill existing session if it exists
tmux has-session -t "$SESSION" 2>/dev/null && tmux kill-session -t "$SESSION"

# Create new session
tmux new-session -d -s "$SESSION" -c "$HOME/workspace"

# Window 1: Main workspace
tmux rename-window -t "$SESSION:1" "workspace"
tmux send-keys -t "$SESSION:1" "cd ~/workspace" Enter

# Window 2: Services status
tmux new-window -t "$SESSION" -n "services"
tmux send-keys -t "$SESSION:services" "systemctl --user status 'nero-*'" Enter

# Window 3: Logs (split into 3 panes)
tmux new-window -t "$SESSION" -n "logs"
tmux send-keys -t "$SESSION:logs" "journalctl --user -f -u nero-core" Enter
tmux split-window -h -t "$SESSION:logs"
tmux send-keys "journalctl --user -f -u nero-channel-web" Enter
tmux split-window -v -t "$SESSION:logs"
tmux send-keys "journalctl --user -f -u nero-channel-tg" Enter

# Window 4: Infrastructure
tmux new-window -t "$SESSION" -n "infra" -c "$HOME/workspace/repos/nero-infra"
tmux send-keys -t "$SESSION:infra" "docker ps" Enter

# Window 5: Git (all repos)
tmux new-window -t "$SESSION" -n "git" -c "$HOME/workspace/repos"

# Select first window
tmux select-window -t "$SESSION:1"

# Attach
tmux attach -t "$SESSION"
```

## Template 4: Generic Dev Session Template

File: `~/bin/tmux-dev.sh`

```bash
#!/bin/bash
# tmux-dev.sh — Generic development session
# Usage: tmux-dev.sh <session-name> <project-dir>

SESSION="${1:-dev}"
DIR="${2:-$(pwd)}"

tmux has-session -t "$SESSION" 2>/dev/null && {
    tmux attach -t "$SESSION"
    exit 0
}

# Main window: editor
tmux new-session -d -s "$SESSION" -c "$DIR"
tmux rename-window -t "$SESSION:1" "edit"

# Second window: terminal
tmux new-window -t "$SESSION" -n "term" -c "$DIR"

# Third window: logs/tests (split)
tmux new-window -t "$SESSION" -n "run" -c "$DIR"
tmux split-window -h -t "$SESSION:run" -c "$DIR"

# Go to edit window
tmux select-window -t "$SESSION:1"
tmux attach -t "$SESSION"
```

## Template 5: tmux Setup Script (One-Liner)

```bash
#!/bin/bash
# setup-tmux.sh — Install tmux + TPM + config in one go

set -euo pipefail

echo "=== tmux Setup ==="

# Install tmux
if ! command -v tmux &>/dev/null; then
    echo "Installing tmux..."
    sudo apt install -y tmux
fi
echo "tmux version: $(tmux -V)"

# Install TPM
if [ ! -d ~/.tmux/plugins/tpm ]; then
    echo "Installing TPM..."
    git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
fi

# Create config (write .tmux.conf)
echo "Writing ~/.tmux.conf..."
# (paste Template 1 content here)

# Create status bar script
echo "Writing ~/.tmux-system.sh..."
# (paste Template 2 content here)
chmod +x ~/.tmux-system.sh

# Create session template
mkdir -p ~/bin
echo "Writing ~/bin/tmux-nero.sh..."
# (paste Template 3 content here)
chmod +x ~/bin/tmux-nero.sh

echo ""
echo "=== Setup Complete ==="
echo "Start tmux and press prefix + I to install plugins"
echo "  tmux new -s main"
echo "  Ctrl+A, I"
```

## Template 6: .tmux.conf Minimal (Quick Start)

For servers where you just need basics without plugins:

```bash
# ~/.tmux.conf — Minimal config (no plugins)

set -g prefix C-a
unbind C-b
bind C-a send-prefix

set -g mouse on
setw -g mode-keys vi
set -g base-index 1
set -g history-limit 50000
set -sg escape-time 10

bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
bind r source-file ~/.tmux.conf \; display "Reloaded"

bind -n C-Up select-pane -U
bind -n C-Down select-pane -D
bind -n C-Left select-pane -L
bind -n C-Right select-pane -R

set -g default-terminal "screen-256color"
set -ga terminal-overrides ",xterm-256color:RGB"

set -g status-bg colour235
set -g status-fg colour248
set -g status-left " #S "
set -g status-right " %H:%M "
```
