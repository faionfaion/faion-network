# Cron Automation Examples

## Example 1: NERO Platform Cron Jobs

The NERO platform runs 12+ cron jobs covering monitoring, backups, content, and maintenance.

### Current Crontab

```cron
# Config sync
*/15 * * * * /home/nero/workspace/scripts/sync-claude-md.sh >/dev/null 2>&1

# FLOW monitoring
0 * * * * /home/nero/workspace/scripts/flow-hourly.sh >> /var/log/nero-flow.log 2>&1
5 6,9,12,15,18,21 * * * /home/nero/workspace/scripts/flow-summarize.sh >> /var/log/nero-flow.log 2>&1
0 22 * * * /home/nero/workspace/scripts/flow-send-daily.sh >> /var/log/nero-flow.log 2>&1
0 7 * * 1 /home/nero/workspace/scripts/flow-send-weekly.sh >> /var/log/nero-flow.log 2>&1
15 7 1 * * /home/nero/workspace/scripts/flow-send-monthly.sh >> /var/log/nero-flow.log 2>&1
20 7 1 1,4,7,10 * /home/nero/workspace/scripts/flow-send-quarterly.sh >> /var/log/nero-flow.log 2>&1
25 7 1 1 * /home/nero/workspace/scripts/flow-send-annual.sh >> /var/log/nero-flow.log 2>&1

# Content
5 8 * * * /home/nero/workspace/scripts/morning-ai-news.sh >> /var/log/nero-news.log 2>&1

# Maintenance
0 3 * * 0 /home/nero/workspace/scripts/check-upstream.sh >> /var/log/nero-upstream.log 2>&1

# Startup
@reboot sleep 5 && /home/nero/workspace/scripts/startup-heartbeat.sh >> /var/log/nero-startup.log 2>&1
```

### Schedule Visualization (24h)

```
Hour  Jobs
00    flow-hourly
01    flow-hourly
02    flow-hourly
03    flow-hourly, check-upstream (Sun)
04    flow-hourly, docker-prune (Sun)
05    flow-hourly, restic-check (Sun)
06    flow-hourly, flow-summarize
07    flow-hourly, flow-weekly (Mon), flow-monthly (1st), flow-quarterly, flow-annual
08    flow-hourly, morning-ai-news
09    flow-hourly, flow-summarize
10    flow-hourly
11    flow-hourly
12    flow-hourly, flow-summarize
13    flow-hourly
14    flow-hourly
15    flow-hourly, flow-summarize
16    flow-hourly
17    flow-hourly
18    flow-hourly, flow-summarize
19    flow-hourly
20    flow-hourly
21    flow-hourly, flow-summarize
22    flow-hourly, flow-daily
23    flow-hourly
```

---

## Example 2: sync-claude-md Script

Synchronizes CLAUDE.md files across the workspace every 15 minutes.

```bash
#!/bin/bash
# sync-claude-md.sh
# Sync CLAUDE.md from repos to a central location
# Schedule: */15 * * * *

set -euo pipefail

REPOS_DIR="$HOME/workspace/repos"
CENTRAL="$HOME/workspace/claude-docs"

mkdir -p "$CENTRAL"

for repo in "$REPOS_DIR"/*/; do
    repo_name=$(basename "$repo")
    claude_md="$repo/CLAUDE.md"

    if [ -f "$claude_md" ]; then
        # Only copy if changed
        if ! diff -q "$claude_md" "$CENTRAL/${repo_name}-CLAUDE.md" &>/dev/null 2>&1; then
            cp "$claude_md" "$CENTRAL/${repo_name}-CLAUDE.md"
        fi
    fi
done
```

---

## Example 3: Morning AI News Script

Fetch and summarize AI news daily at 8:05 AM.

```bash
#!/bin/bash
# morning-ai-news.sh
# Fetch AI news headlines and send to Telegram
# Schedule: 5 8 * * *

set -euo pipefail

SCRIPT_NAME="morning-ai-news"
LOG_FILE="/var/log/nero-news.log"
LOCK_FILE="/tmp/${SCRIPT_NAME}.lock"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') [$SCRIPT_NAME] $1" >> "$LOG_FILE"; }

exec 9>"$LOCK_FILE"
flock -n 9 || { log "Skipping (locked)"; exit 0; }

trap 'if [ $? -ne 0 ]; then log "ERROR: Failed"; fi' EXIT

source "$HOME/workspace/.env" 2>/dev/null || true

log "Fetching AI news..."

# Use Claude API to summarize news
# (This is a simplified example - actual implementation may use
#  web scraping, RSS feeds, or news APIs)
HEADLINES=$(curl -sf "https://hn.algolia.com/api/v1/search?query=AI+LLM&tags=story&hitsPerPage=5" 2>/dev/null | \
    python3 -c "
import sys, json
data = json.load(sys.stdin)
for hit in data.get('hits', [])[:5]:
    print(f\"- {hit.get('title', 'No title')}\")
    print(f\"  {hit.get('url', '')}\")
" 2>/dev/null || echo "Could not fetch news")

if [ -n "$HEADLINES" ] && [ "$HEADLINES" != "Could not fetch news" ]; then
    MSG="*AI News $(date '+%Y-%m-%d')*

$HEADLINES"

    echo "$MSG" | /usr/local/bin/notify-telegram.sh 2>/dev/null || true
    log "News sent to Telegram"
else
    log "No news to send"
fi
```

---

## Example 4: Upstream Check Script

Weekly check if upstream repos have updates.

```bash
#!/bin/bash
# check-upstream.sh
# Check if GitHub repos have upstream changes not yet pulled
# Schedule: 0 3 * * 0 (Sunday 3 AM)

set -euo pipefail

REPOS_DIR="$HOME/workspace/repos"
LOG_FILE="/var/log/nero-upstream.log"
UPDATES=""

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') [upstream] $1" >> "$LOG_FILE"; }

log "Checking upstream repos..."

for repo in "$REPOS_DIR"/*/; do
    [ -d "$repo/.git" ] || continue
    repo_name=$(basename "$repo")

    cd "$repo"

    # Fetch without merging
    git fetch origin 2>/dev/null || { log "  $repo_name: fetch failed"; continue; }

    # Check if behind
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null || echo "unknown")

    if [ "$LOCAL" != "$REMOTE" ] && [ "$REMOTE" != "unknown" ]; then
        BEHIND=$(git rev-list HEAD..origin/main 2>/dev/null | wc -l || echo "?")
        UPDATES="${UPDATES}  $repo_name: ${BEHIND} commits behind\n"
        log "  $repo_name: $BEHIND commits behind"
    fi
done

if [ -n "$UPDATES" ]; then
    source "$HOME/workspace/.env" 2>/dev/null || true
    MSG="*Upstream Updates Available:*
$(echo -e "$UPDATES")"
    echo "$MSG" | /usr/local/bin/notify-telegram.sh 2>/dev/null || true
    log "Notification sent"
else
    log "All repos up to date"
fi
```

---

## Example 5: Cron Job with Retry Logic

A cron job that retries on failure with exponential backoff.

```bash
#!/bin/bash
# external-sync.sh
# Sync data with external service, retry on failure
# Schedule: 0 */6 * * * (every 6 hours)

set -euo pipefail

SCRIPT_NAME="external-sync"
LOG_FILE="/var/log/nero-${SCRIPT_NAME}.log"
LOCK_FILE="/tmp/${SCRIPT_NAME}.lock"
MAX_RETRIES=3
RETRY_DELAY=30

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') [$SCRIPT_NAME] $1" >> "$LOG_FILE"; }

exec 9>"$LOCK_FILE"
flock -n 9 || { log "Skipping (locked)"; exit 0; }

source "$HOME/workspace/.env" 2>/dev/null || true

do_sync() {
    # Replace with actual sync logic
    curl -sf --max-time 60 "https://api.example.com/sync" \
        -H "Authorization: Bearer $API_TOKEN" \
        -o /dev/null
}

for attempt in $(seq 1 $MAX_RETRIES); do
    log "Attempt $attempt/$MAX_RETRIES..."

    if do_sync; then
        log "Sync successful"
        exit 0
    fi

    if [ $attempt -lt $MAX_RETRIES ]; then
        delay=$((RETRY_DELAY * attempt))
        log "Failed, retrying in ${delay}s..."
        sleep $delay
    fi
done

log "ERROR: All $MAX_RETRIES attempts failed"
/usr/local/bin/notify-telegram.sh "CRON FAIL: $SCRIPT_NAME failed after $MAX_RETRIES attempts" 2>/dev/null || true
exit 1
```

---

## Example 6: Crontab Backup and Restore

Backup crontab as part of the configuration management.

```bash
#!/bin/bash
# backup-crontab.sh
# Backup current crontab to workspace configs
# Schedule: run after any crontab change, or daily

set -euo pipefail

BACKUP_DIR="$HOME/workspace/configs"
mkdir -p "$BACKUP_DIR"

# Backup current crontab
crontab -l > "$BACKUP_DIR/crontab.txt" 2>/dev/null || echo "# No crontab" > "$BACKUP_DIR/crontab.txt"

# Backup with timestamp for history
DATED_DIR="$BACKUP_DIR/crontab-history"
mkdir -p "$DATED_DIR"
crontab -l > "$DATED_DIR/crontab-$(date +%Y%m%d).txt" 2>/dev/null || true

# Keep last 30 days
find "$DATED_DIR" -name "crontab-*.txt" -mtime +30 -delete 2>/dev/null || true

echo "Crontab backed up to $BACKUP_DIR/crontab.txt"
```

### Restore

```bash
# Restore crontab from backup
crontab ~/workspace/configs/crontab.txt

# Verify
crontab -l
```
