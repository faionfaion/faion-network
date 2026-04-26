#!/usr/bin/env bash
# bootstrap-newhire.sh — generate 30-day plan and create GitHub issue
# Usage: bash bootstrap-newhire.sh <name> <role> <start-date> <manager> [buddy]
# Example: bash bootstrap-newhire.sh "Alice Chen" "Senior Engineer" 2026-05-01 "Bob Smith"
set -euo pipefail

NAME="${1:?name required}"
ROLE="${2:?role required}"
START="${3:?start date YYYY-MM-DD required}"
MGR="${4:?manager name required}"
BUDDY="${5:-TBD}"

SLUG=$(echo "$NAME" | tr '[:upper:] ' '[:lower:]-')
OUTDIR="onboarding/$SLUG"
mkdir -p "$OUTDIR"

echo "Generating 30-day plan for $NAME ($ROLE)..."

claude -p "Generate a 30-day onboarding plan for $NAME starting as $ROLE on $START.
Manager: $MGR. Buddy: $BUDDY.
Use the universal 30-day plan template structure:
- Week 1 (Days 1-7): orientation, Day 1 setup, team meetings, Day 7 check-in
- Week 2 (Days 8-14): required training, cross-functional meetings, Day 14 buddy check
- Weeks 3-4 (Days 15-30): deep dive, first task, 30-day milestone
Include ONE specific 30-day milestone appropriate for a $ROLE.
Replace all generic tasks with role-specific ones.
Output clean Markdown." > "$OUTDIR/plan.md"

echo "Created: $OUTDIR/plan.md"

# Create GitHub issue for manager tracking
gh issue create \
  --title "Onboarding: $NAME ($ROLE) — starts $START" \
  --label "onboarding" \
  --assignee "$MGR" \
  --body-file "$OUTDIR/plan.md"

echo "GitHub issue created and assigned to $MGR"
echo ""
echo "Next steps:"
echo "  1. Manager reviews $OUTDIR/plan.md and customizes milestone"
echo "  2. Buddy assignment confirmed: $BUDDY"
echo "  3. IT notified for Day 1 setup"
echo "  4. Calendar invites created for Day 7, 14, 30 check-ins"
