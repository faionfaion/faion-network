#!/usr/bin/env python3
"""
query-safe.py — validate LLM-generated SQL before warehouse execution.

Rejects queries that reference columns not present in the known schema.
This prevents the #1 LLM analytics bug: hallucinated column names.

Usage:
  python query-safe.py schema.json < query.sql
  echo "SELECT user_id FROM events" | python query-safe.py schema.json

Schema format (JSON):
  {"events": ["user_id", "event_name", "created_at_utc"], "users": ["id", "plan"]}

Exit codes:
  0 — SQL is safe (all columns known), prints SQL to stdout
  1 — SQL references unknown columns, prints error to stderr
"""
import json
import sys

try:
    import sqlglot
    import sqlglot.exp
except ImportError:
    sys.exit("Error: install sqlglot first: pip install sqlglot")

def main():
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} schema.json < query.sql")

    schema_path = sys.argv[1]
    try:
        with open(schema_path) as f:
            schema = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        sys.exit(f"Schema error: {e}")

    sql = sys.stdin.read().strip()
    if not sql:
        sys.exit("Error: no SQL provided on stdin")

    # Build flat set of known column names (with and without table prefix)
    known = set()
    for table, cols in schema.items():
        for col in cols:
            known.add(col)
            known.add(f"{table}.{col}")

    try:
        parsed = sqlglot.parse_one(sql, read="postgres")
    except Exception as e:
        sys.exit(f"SQL parse error: {e}")

    # Extract all column references
    referenced = {c.name for c in parsed.find_all(sqlglot.exp.Column)}

    unknown = referenced - known - {"*"}
    if unknown:
        print(f"BLOCKED: unknown columns {sorted(unknown)}", file=sys.stderr)
        print(f"Known columns: {sorted(known)}", file=sys.stderr)
        sys.exit(1)

    # Safe — print to stdout for piping to warehouse client
    print(sql)


if __name__ == "__main__":
    main()
