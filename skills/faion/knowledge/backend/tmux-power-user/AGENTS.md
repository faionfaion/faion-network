# tmux Power User

## Summary

**One-sentence:** Generates a tmux config + named-session script + plugin set (resurrect, continuum, yank) for a multi-host operator — gated by versioned dotfiles.

**One-paragraph:** Solo operators live in tmux: persistent sessions across SSH disconnects, named projects, copy-mode that works on macOS and Linux. This methodology pins a tmux.conf (TPM plugin loader, prefix C-a, mouse on, 100k history), a session-launcher script, and the plugin set. Output: a TmuxPlan + tmux.conf.

**Ефективно для:**

- SSH operator who reconnects to the same VPS dozens of times daily.
- Multi-project workflows where each project deserves a named session.
- Long-running interactive work (claude code, repl, log tailing) that must survive disconnect.
- macOS + Linux operators sharing the same tmux.conf.

## Applies If (ALL must hold)

- Operator runs ≥3 tmux sessions/day.
- SSH connections drop occasionally and work must survive.
- Multiple projects on one host needing per-project sessions.
- Standardising tmux across personal + remote machines.

## Skip If (ANY kills it)

- Operator uses a different terminal multiplexer (zellij, screen) by preference.
- Single-session usage with no copy-mode needs.
- Locked-down env where plugins can't be installed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Operator prefix preference | C-a or C-b | operator |
| Plugin allow-list | list of TPM plugins | TmuxPlan |
| OS list | macos / linux | operator hosts |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| dotfiles-management | tmux.conf is part of the dotfiles repo. |
| shell-productivity | Shell prompt + history coordinate with tmux defaults. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-prefix-not-c-b, r2-tpm-managed-plugins, r3-large-history, r4-named-owner, r5-os-conditional-copy | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the tmux Power User artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: default-prefix-c-b, history-1024-loses, copy-mode-platform-mismatch, plugin-versions-floating | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-tmux-conf` | sonnet | Per-operator key-binding tweaks. |
| `render-session-script` | haiku | Mechanical template fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tmux-power-user.json` | TmuxPlan JSON skeleton. |
| `templates/tmux-power-user.md` | Human-readable audit trail + keybinding cheatsheet. |
| `templates/tmux.conf` | Reference tmux.conf with prefix C-a, mouse on, 100k history, TPM. |
| `templates/tmux-session.sh` | Launcher for a named project session with split layout. |
| `templates/tmux-system.sh` | System tmux session (monitoring, logs). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tmux-power-user.py` | Validate TmuxPlan JSON against the schema. | Pre-apply on each host. |

## Related

- [[dotfiles-management]]
- [[shell-productivity]]
- [[bash-aliases]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tmux-power-user.json`

```json
{
  "artefact_id": "tmux-<operator>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "prefix": "C-a",
  "plugins": [
    "tmux-plugins/tpm@v3.1.0",
    "tmux-plugins/tmux-resurrect@v4.0.0"
  ],
  "history_limit": 100000,
  "os_targets": [
    "linux",
    "macos"
  ],
  "owner": "<@handle>"
}
```

### `templates/tmux.conf`

```conf
# ~/.tmux.conf — Power User Configuration
# Install TPM first: git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
# After adding plugins: press prefix + I to install

# ============================================================
# PREFIX
# ============================================================
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# ============================================================
# GENERAL
# ============================================================
set -g mouse on
setw -g mode-keys vi
set -g base-index 1
setw -g pane-base-index 1
set -g renumber-windows on
set -g history-limit 50000
set -sg escape-time 10
set -g focus-events on

# ============================================================
# KEYBINDINGS
# ============================================================
bind r source-file ~/.tmux.conf \; display "Config reloaded"

# Intuitive splits (inherit current directory)
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# New window in current directory
bind c new-window -c "#{pane_current_path}"

# Pane navigation without prefix
bind -n C-Up    select-pane -U
bind -n C-Down  select-pane -D
bind -n C-Left  select-pane -L
bind -n C-Right select-pane -R

# Pane resize with vi directions
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# Window switching with Alt+number
bind -n M-1 select-window -t 1
bind -n M-2 select-window -t 2
bind -n M-3 select-window -t 3
bind -n M-4 select-window -t 4
bind -n M-5 select-window -t 5
bind -n M-6 select-window -t 6
bind -n M-7 select-window -t 7
bind -n M-8 select-window -t 8
bind -n M-9 select-window -t 9

# Window reordering
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

set -g status-left-length 30
set -g status-left "#[fg=colour0,bg=colour4,bold] #S #[fg=colour4,bg=colour235,nobold] "

set -g status-right-length 120
set -g status-right '#(~/.tmux-system.sh) #[fg=colour240]| #[fg=colour248]%H:%M '

setw -g window-status-format " #I:#W "
setw -g window-status-current-format "#[fg=colour235,bg=colour4] #I:#W #[fg=colour4,bg=colour235]"
setw -g window-status-separator ""

set -g pane-border-style "fg=colour240"
set -g pane-active-border-style "fg=colour4"
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

set -g @resurrect-capture-pane-contents 'on'
set -g @resurrect-strategy-vim 'session'
set -g @continuum-restore 'on'
set -g @continuum-save-interval '15'

# MUST be last line
run '~/.tmux/plugins/tpm/tpm'
```

### `templates/tmux-session.sh`

```bash
# tmux-session.sh
# Generic create-or-attach session launcher — safe to call repeatedly.
#
# Usage:
#   tmux-session.sh <session-name> [project-dir]
#   tmux-session.sh nero ~/workspace/projects/nero
#
# If the session already exists, attaches to it.
# If it does not exist, creates it with a standard 3-window layout.

set -euo pipefail

SESSION="${1:-dev}"
DIR="${2:-$(pwd)}"

# Attach if session already exists (idempotent)
if tmux has-session -t "$SESSION" 2>/dev/null; then
    exec tmux attach -t "$SESSION"
fi

# Create new session
tmux new-session -d -s "$SESSION" -c "$DIR"

# Window 1: editor / main work
tmux rename-window -t "$SESSION:1" "edit"

# Window 2: terminal
tmux new-window -t "$SESSION" -n "term" -c "$DIR"

# Window 3: run/logs (split into two panes)
tmux new-window -t "$SESSION" -n "run" -c "$DIR"
tmux split-window -h -t "$SESSION:run" -c "$DIR"

# Focus on window 1
tmux select-window -t "$SESSION:1"

exec tmux attach -t "$SESSION"
```

### `templates/tmux-system.sh`

```bash
# ~/.tmux-system.sh
# tmux status bar system metrics with color-coded thresholds
#
# Colors: cyan (OK) -> yellow (50%) -> orange (70%) -> red (90%)
# Install: chmod +x ~/.tmux-system.sh
# In .tmux.conf: set -g status-right '#(~/.tmux-system.sh) | %H:%M '

cyan="#[fg=colour6]"
yellow="#[fg=colour3]"
orange="#[fg=colour208]"
red="#[fg=colour1]"
dim="#[dim]"
r="#[default]"

# CPU: load average / core count
ncpu=$(nproc 2>/dev/null || echo 1)
cpu_pct=$(awk '{printf "%d", $1 * 100 / '"$ncpu"'}' /proc/loadavg)

# Memory: from /proc/meminfo
mem_pct=$(awk '/MemTotal/{t=$2} /MemAvailable/{a=$2} END{printf "%d", (t-a)*100/t}' /proc/meminfo)

# Disk: root partition
disk_pct=$(df / | awk 'NR==2 {gsub(/%/, "", $5); print $5}')

# Color selection per metric
mc="$cyan"
[ "$mem_pct" -ge 50 ] && mc="$yellow"
[ "$mem_pct" -ge 70 ] && mc="$orange"
[ "$mem_pct" -ge 90 ] && mc="$red"

cc="$cyan"
[ "$cpu_pct" -ge 50 ] && cc="$yellow"
[ "$cpu_pct" -ge 70 ] && cc="$orange"
[ "$cpu_pct" -ge 90 ] && cc="$red"

dc="$cyan"
[ "$disk_pct" -ge 50 ] && dc="$yellow"
[ "$disk_pct" -ge 70 ] && dc="$orange"
[ "$disk_pct" -ge 90 ] && dc="$red"

printf "%sM:%s%s%%%s %sC:%s%s%%%s %sD:%s%s%%%s" \
    "$dim" "$mc" "$mem_pct" "$r" \
    "$dim" "$cc" "$cpu_pct" "$r" \
    "$dim" "$dc" "$disk_pct" "$r"
```
