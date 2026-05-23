#!/bin/bash
# purpose: Template fixture for tmux-power-user: tmux-system.sh
# consumes: content/01-core-rules.xml
# produces: executable script
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
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
