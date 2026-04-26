#!/bin/bash
# add-database.sh — Create a PostgreSQL database + user in the shared Docker instance
#
# Usage: bash add-database.sh <dbname> <username> [password]
# Example: bash add-database.sh meetingtax mtax_user
#
# Password is auto-generated if not provided.

set -euo pipefail

DB_NAME="${1:?Usage: bash add-database.sh <dbname> <username> [password]}"
DB_USER="${2:?Provide database username}"
DB_PASS="${3:-$(openssl rand -base64 24 | tr -d '/+=' | head -c 32)}"

POSTGRES_CONTAINER="${POSTGRES_CONTAINER:-nero-postgres}"

echo "=== Creating database: $DB_NAME ==="
echo "User:     $DB_USER"
echo "Password: $DB_PASS"
echo "Container: $POSTGRES_CONTAINER"
echo ""

docker exec -i "$POSTGRES_CONTAINER" psql -U postgres << SQL
CREATE DATABASE ${DB_NAME};
CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
ALTER DATABASE ${DB_NAME} OWNER TO ${DB_USER};
SQL

echo ""
echo "=== Database created successfully ==="
echo "Connection URL:"
echo "  postgresql://${DB_USER}:${DB_PASS}@localhost:5432/${DB_NAME}"
echo ""
echo "Add to project .env:"
echo "  DATABASE_URL=postgresql://${DB_USER}:${DB_PASS}@localhost:5432/${DB_NAME}"
echo ""
echo "Store the password in 1Password before closing this terminal."
