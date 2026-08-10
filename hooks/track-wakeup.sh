#!/bin/bash
# PostToolUse hook for ScheduleWakeup — records the next scheduled wakeup
# to /tmp/claude-wakeups.json so statusline can display it.

input=$(cat)

delay=$(echo "$input" | jq -r '.tool_input.delaySeconds // 0' 2>/dev/null)
reason=$(echo "$input" | jq -r '.tool_input.reason // ""' 2>/dev/null)
session=$(echo "$input" | jq -r '.session_id // ""' 2>/dev/null)

# No-op for missing/invalid delay
if [ -z "$delay" ] || [ "$delay" = "0" ] || [ "$delay" = "null" ]; then
    exit 0
fi

now=$(date +%s)
fires_at=$((now + delay))

jq -n \
    --argjson fires_at "$fires_at" \
    --argjson scheduled_at "$now" \
    --argjson delay "$delay" \
    --arg reason "$reason" \
    --arg session "$session" \
    '{fires_at: $fires_at, scheduled_at: $scheduled_at, delaySeconds: $delay, reason: $reason, session_id: $session}' \
    > /tmp/claude-wakeups.json

exit 0
