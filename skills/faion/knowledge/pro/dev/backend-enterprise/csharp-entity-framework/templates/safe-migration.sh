#!/usr/bin/env bash
# purpose: wrapper around `dotnet ef migrations script` blocking destructive ops without approval
# consumes: migration name, project path
# produces: SQL script + pass/fail gate per migration-sql-review rule
# depends-on: content/01-core-rules.xml rule migration-sql-review
# token-budget-impact: ~250 tokens when loaded as context
# safe-migration.sh — generate migration + block on destructive SQL ops
# Usage: bash safe-migration.sh <MigrationName> <project-path>
# Example: bash safe-migration.sh AddUserEmailIndex src/MyApp.Data/
set -euo pipefail

NAME="${1:?migration name required}"
PROJ="${2:?project path required}"

echo "=== Adding migration: $NAME ==="
dotnet ef migrations add "$NAME" --project "$PROJ" --no-build

SCRIPT=$(mktemp --suffix=.sql)
echo "=== Generating idempotent SQL to: $SCRIPT ==="
dotnet ef migrations script --idempotent --project "$PROJ" -o "$SCRIPT"

echo "=== Checking for destructive operations ==="
if grep -iE 'DROP TABLE|DROP COLUMN|TRUNCATE|RENAME COLUMN|CASCADE' "$SCRIPT"; then
    echo ""
    echo "DESTRUCTIVE OPERATIONS DETECTED — human approval required before apply"
    echo "Review: $SCRIPT"
    exit 2
fi

echo "Migration looks safe (auto-check). Review SQL before applying to non-dev environments."
echo "SQL script: $SCRIPT"
echo ""
echo "To apply: dotnet ef database update --project $PROJ"
