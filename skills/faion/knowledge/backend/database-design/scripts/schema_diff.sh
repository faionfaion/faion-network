#!/usr/bin/env bash
# schema_diff.sh <proposed.sql> <db_url>
# Diffs a proposed DDL file against a live PostgreSQL database and prints the delta.
# Requires: psql, pg_dump (bundled with PostgreSQL), createdb, dropdb.
#
# Usage: ./scripts/schema_diff.sh proposed.sql postgres://user:pass@host/db
# Output: unified diff (current schema → proposed schema). Empty diff = no change.
set -euo pipefail

PROPOSED="${1:?Usage: schema_diff.sh <proposed.sql> <db_url>}"
DB_URL="${2:?Usage: schema_diff.sh <proposed.sql> <db_url>}"
TMPDB="_schema_diff_$$"
TMPDIR_LOCAL=$(mktemp -d)
trap 'rm -rf "$TMPDIR_LOCAL"; dropdb --if-exists "$TMPDB" 2>/dev/null || true' EXIT

# Dump current schema (normalized: strip comments, SET, pg_catalog boilerplate).
pg_dump --schema-only --no-owner --no-privileges "$DB_URL" \
    | grep -vE '^(--|SET |SELECT pg_catalog)' \
    | grep -v '^$' \
    > "$TMPDIR_LOCAL/current.sql"

# Apply proposed schema to a fresh temp database.
createdb "$TMPDB"
psql -d "$TMPDB" -f "$PROPOSED" > /dev/null

# Dump proposed schema.
pg_dump --schema-only --no-owner --no-privileges -d "$TMPDB" \
    | grep -vE '^(--|SET |SELECT pg_catalog)' \
    | grep -v '^$' \
    > "$TMPDIR_LOCAL/proposed.sql"

# Print diff (exit 0 even if diff finds differences).
diff -u "$TMPDIR_LOCAL/current.sql" "$TMPDIR_LOCAL/proposed.sql" || true
