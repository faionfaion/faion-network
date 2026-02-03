#!/bin/bash
input=$(cat)

model_id=$(echo "$input" | jq -r '.model.id // empty')
session_id=$(echo "$input" | jq -r '.session_id // empty')
total_cost=$(echo "$input" | jq -r '.cost.total_cost_usd // empty')

# Get remaining percentage directly from API (subtract 16% buffer)
remaining_pct=$(echo "$input" | jq -r '.context_window.remaining_percentage // empty | if . != "" then (tonumber - 16 | if . < 0 then 0 else . end) else . end')
remaining_pct=${remaining_pct%.*}
remaining_pct=${remaining_pct:-50}
used_pct=$((100 - remaining_pct))

r="\033[0m"
dim="\033[2m"
green="\033[32m"
yellow="\033[33m"
orange="\033[38;5;208m"
red="\033[31m"
cyan="\033[36m"

# --- Provider icon ---

bucket="license"
provider_icon="⚡"  # Lightning for License
case "$model_id" in
  *bedrock*|*.anthropic.*) provider_icon="◈"; bucket="bedrock" ;;
  *vertex*)                provider_icon="▲"; bucket="bedrock" ;;
esac

# --- Cost tracking ---

if [ -n "$total_cost" ] && [ "$total_cost" != "null" ]; then
  raw_cost=$(awk "BEGIN {printf \"%.6f\", $total_cost + 0}")
else
  raw_cost="0"
fi

usage_file="$HOME/.claude/usage.json"
lock_file="$HOME/.claude/usage.lock"
session_cost="0.00"

if [ -n "$session_id" ] && [ "$session_id" != "null" ]; then
  (
    flock -w 5 200 || exit 1

    if [ ! -s "$usage_file" ]; then
      echo '{"license":{},"bedrock":{}}' > "$usage_file"
    fi

    jq '.license //= {} | .bedrock //= {}' "$usage_file" > "${usage_file}.tmp" && mv "${usage_file}.tmp" "$usage_file"

    jq --arg b "$bucket" --arg sid "$session_id" --argjson cost "$raw_cost" '
      .[$b][$sid] //= {"base": 0, "current": 0} |
      if $cost < .[$b][$sid].current then
        .[$b][$sid].base += .[$b][$sid].current |
        .[$b][$sid].current = $cost
      else
        .[$b][$sid].current = $cost
      end
    ' "$usage_file" > "${usage_file}.tmp" && mv "${usage_file}.tmp" "$usage_file"

  ) 200>"$lock_file"

  # Aggregate costs
  total_license=0
  total_bedrock=0
  while IFS= read -r f; do
    [ -s "$f" ] || continue
    l=$(jq -r '[.license // {} | to_entries[].value | ((.base // 0) + (.current // 0))] | add // 0' "$f" 2>/dev/null)
    b=$(jq -r '[.bedrock // {} | to_entries[].value | ((.base // 0) + (.current // 0))] | add // 0' "$f" 2>/dev/null)
    total_license=$(awk "BEGIN {printf \"%.6f\", ${total_license} + ${l:-0}}")
    total_bedrock=$(awk "BEGIN {printf \"%.6f\", ${total_bedrock} + ${b:-0}}")
  done < <(find "$HOME" -maxdepth 5 -path '*/.claude/usage.json' -type f 2>/dev/null)

  session_cost=$(awk "BEGIN {printf \"%.2f\", ${total_license} + ${total_bedrock}}")
fi

# --- Context bar (full terminal width) ---

term_width=$(tput cols 2>/dev/null || echo 80)
# Reserve: provider icon (2) + percentage (5: " XX%")
bar_width=$((term_width - 2 - 5))

# Calculate filled vs empty
filled_chars=$((used_pct * bar_width / 100))
empty_chars=$((bar_width - filled_chars))
if [ "$empty_chars" -lt 0 ]; then
  empty_chars=0
fi

# Color based on remaining percentage
if [ "$remaining_pct" -ge 50 ]; then
  bar_color="$green"
elif [ "$remaining_pct" -ge 25 ]; then
  bar_color="$yellow"
elif [ "$remaining_pct" -ge 15 ]; then
  bar_color="$orange"
else
  bar_color="$red"
fi

# Build context bar
ctx_bar="${bar_color}"

# Filled: ● (filled circle)
for ((i=0; i<filled_chars; i++)); do
  ctx_bar+="●"
done

# Empty: ○ (empty circle)
ctx_bar+="${dim}"
for ((i=0; i<empty_chars; i++)); do
  ctx_bar+="○"
done
ctx_bar+="${r}"

# Remaining percentage at the end
pct_color="$green"
[ "$remaining_pct" -lt 50 ] && pct_color="$yellow"
[ "$remaining_pct" -lt 25 ] && pct_color="$orange"
[ "$remaining_pct" -lt 15 ] && pct_color="$red"
ctx_bar+=" ${pct_color}${remaining_pct}%${r}"

# --- System metrics (Linux) ---

mem_pct=$(awk '/MemTotal/{t=$2} /MemAvailable/{a=$2} END{printf "%d", (t-a)*100/t}' /proc/meminfo)
cpu_pct=$(awk '{printf "%d", $1 * 100 / '"$(nproc)"'}' /proc/loadavg)

# Color based on percentage
mem_color="$cyan"
[ "$mem_pct" -ge 50 ] && mem_color="$yellow"
[ "$mem_pct" -ge 70 ] && mem_color="$orange"
[ "$mem_pct" -ge 90 ] && mem_color="$red"

cpu_color="$cyan"
[ "$cpu_pct" -ge 50 ] && cpu_color="$yellow"
[ "$cpu_pct" -ge 70 ] && cpu_color="$orange"
[ "$cpu_pct" -ge 90 ] && cpu_color="$red"

# Count running Claude processes
claude_count=$(pgrep -f "claude" | wc -l | tr -d ' ')

# --- Output ---

echo -e "${provider_icon} ${ctx_bar}"
echo -e "${dim}M:${mem_color}${mem_pct}%${r} ${dim}C:${cpu_color}${cpu_pct}%${r} ${dim}\$${yellow}${session_cost}${r} ${dim}⚙:${cyan}${claude_count}${r}"
