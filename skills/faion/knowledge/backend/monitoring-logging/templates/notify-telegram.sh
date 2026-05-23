#!/bin/bash
# notify-telegram.sh
# Send a message to Telegram
# Usage: ./notify-telegram.sh "Message text"
#        echo "Message" | ./notify-telegram.sh
#
# Requires: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in environment or ~/.env

set -euo pipefail

# Load credentials from workspace .env if not already set
if [ -z "${TELEGRAM_BOT_TOKEN:-}" ] && [ -f "$HOME/workspace/.env" ]; then
    eval "$(grep -E '^TELEGRAM_(BOT_TOKEN|CHAT_ID)=' "$HOME/workspace/.env" 2>/dev/null || true)"
fi

BOT_TOKEN="${TELEGRAM_BOT_TOKEN:?Set TELEGRAM_BOT_TOKEN in ~/.env or environment}"
CHAT_ID="${TELEGRAM_CHAT_ID:?Set TELEGRAM_CHAT_ID in ~/.env or environment}"

# Get message from argument or stdin
if [ -n "${1:-}" ]; then
    MESSAGE="$1"
else
    MESSAGE=$(cat)
fi

# Truncate if too long (Telegram limit is 4096 chars)
if [ "${#MESSAGE}" -gt 4000 ]; then
    MESSAGE="${MESSAGE:0:3990}...(truncated)"
fi

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="$MESSAGE" \
    -d parse_mode="Markdown" \
    -d disable_web_page_preview="true" > /dev/null
