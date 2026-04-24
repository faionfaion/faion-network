# tmux Power User Checklist

Step-by-step checklist for setting up tmux from zero to power user.

## Phase 1: Installation

- [ ] **Install tmux**
  ```bash
  sudo apt install -y tmux
  tmux -V
  ```

- [ ] **Install TPM (plugin manager)**
  ```bash
  git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
  ```

## Phase 2: Core Configuration

- [ ] **Create ~/.tmux.conf** with essential settings
  - Prefix: Ctrl+A
  - Mouse support
  - Vi mode
  - Intuitive splits (| and -)
  - Pane navigation (Ctrl+arrows)
  - Window navigation (Alt+1-9)

- [ ] **Set terminal colors**
  ```bash
  set -g default-terminal "screen-256color"
  set -ga terminal-overrides ",xterm-256color:RGB"
  ```

- [ ] **Source config**
  ```bash
  tmux source ~/.tmux.conf
  ```

## Phase 3: Plugins

- [ ] **Add plugins to .tmux.conf**
  ```bash
  set -g @plugin 'tmux-plugins/tpm'
  set -g @plugin 'tmux-plugins/tmux-resurrect'
  set -g @plugin 'tmux-plugins/tmux-continuum'
  ```

- [ ] **Install plugins**
  ```
  prefix + I (capital i)
  ```
  Verify: `ls ~/.tmux/plugins/`

- [ ] **Configure resurrect**
  ```bash
  set -g @resurrect-capture-pane-contents 'on'
  set -g @resurrect-strategy-vim 'session'
  ```

- [ ] **Configure continuum** (auto-save)
  ```bash
  set -g @continuum-restore 'on'
  set -g @continuum-save-interval '15'
  ```

## Phase 4: Status Bar

- [ ] **Create status bar script**
  ```bash
  cat > ~/.tmux-system.sh << 'SCRIPT'
  #!/bin/bash
  # System metrics for tmux status bar
  ncpu=$(nproc 2>/dev/null || echo 1)
  mem_pct=$(awk '/MemTotal/{t=$2} /MemAvailable/{a=$2} END{printf "%d", (t-a)*100/t}' /proc/meminfo)
  cpu_pct=$(awk '{printf "%d", $1 * 100 / '"$ncpu"'}' /proc/loadavg)
  disk_pct=$(df -h / | awk 'NR==2{print $5}' | tr -d '%')

  cyan="#[fg=colour6]"
  yellow="#[fg=colour3]"
  orange="#[fg=colour208]"
  red="#[fg=colour1]"
  dim="#[dim]"
  r="#[default]"

  mc="$cyan"; [ "$mem_pct" -ge 50 ] && mc="$yellow"; [ "$mem_pct" -ge 70 ] && mc="$orange"; [ "$mem_pct" -ge 90 ] && mc="$red"
  cc="$cyan"; [ "$cpu_pct" -ge 50 ] && cc="$yellow"; [ "$cpu_pct" -ge 70 ] && cc="$orange"; [ "$cpu_pct" -ge 90 ] && cc="$red"
  dc="$cyan"; [ "$disk_pct" -ge 50 ] && dc="$yellow"; [ "$disk_pct" -ge 70 ] && dc="$red"

  printf "%sM:%s%s%%%s %sC:%s%s%%%s %sD:%s%s%%%s" \
      "$dim" "$mc" "$mem_pct" "$r" \
      "$dim" "$cc" "$cpu_pct" "$r" \
      "$dim" "$dc" "$disk_pct" "$r"
  SCRIPT
  chmod +x ~/.tmux-system.sh
  ```

- [ ] **Configure status bar in .tmux.conf**
  ```bash
  set -g status-bg black
  set -g status-fg white
  set -g status-interval 5
  set -g status-left " #S "
  set -g status-right-length 120
  set -g status-right '#(~/.tmux-system.sh) '
  ```

## Phase 5: Session Workflow

- [ ] **Learn essential session commands**
  | Action | Command |
  |--------|---------|
  | New session | `tmux new -s name` |
  | Detach | `prefix + d` |
  | List | `tmux ls` |
  | Attach | `tmux a -t name` |
  | Kill | `tmux kill-session -t name` |
  | Switch | `prefix + s` |

- [ ] **Create session template** for your project
  ```bash
  cat > ~/bin/tmux-nero.sh << 'EOF'
  #!/bin/bash
  tmux new-session -d -s nero -c ~/workspace
  tmux rename-window -t nero:0 'main'
  tmux new-window -t nero -n 'logs' -c ~/workspace
  tmux send-keys -t nero:logs "journalctl --user -f" Enter
  tmux new-window -t nero -n 'infra' -c ~/workspace/repos/nero-infra
  tmux select-window -t nero:0
  tmux attach -t nero
  EOF
  chmod +x ~/bin/tmux-nero.sh
  ```

## Phase 6: Advanced Features

- [ ] **Learn copy mode** (vi-style)
  | Action | Key |
  |--------|-----|
  | Enter copy mode | `prefix + [` |
  | Start selection | `v` |
  | Copy | `y` |
  | Paste | `prefix + ]` |
  | Search forward | `/` |
  | Search backward | `?` |

- [ ] **Learn pane management**
  | Action | Key |
  |--------|-----|
  | Zoom pane (fullscreen) | `prefix + z` |
  | Swap panes | `prefix + {` / `}` |
  | Break pane to window | `prefix + !` |
  | Join pane from window | `prefix + j` (custom) |

- [ ] **Configure nested tmux** (if using tmux locally and remotely)

## Phase 7: Verify Everything Works

- [ ] **Test session persistence**
  ```bash
  tmux new -s test
  # Do some work
  # Detach: prefix + d
  tmux a -t test
  # Work should be intact
  ```

- [ ] **Test resurrect**
  ```bash
  # Save: prefix + Ctrl+S
  # Kill tmux server: tmux kill-server
  # Start tmux
  # Restore: prefix + Ctrl+R
  ```

- [ ] **Test status bar** shows metrics correctly

- [ ] **Test mouse** scrolling, pane clicking, selection

## Quick Reference Card

```
Prefix: Ctrl+A

Sessions:  s=list, d=detach, $=rename
Windows:   c=create, n/p=next/prev, &=kill, ,=rename
Panes:     |=hsplit, -=vsplit, z=zoom, x=kill
Copy:      [=enter, v=select, y=copy, ]=paste
Plugins:   I=install, U=update
Resurrect: Ctrl+S=save, Ctrl+R=restore
```
