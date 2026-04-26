"""
nosql_picker.py — heuristic access-pattern to store recommendation.
Not a substitute for full access-pattern review; use as a starting prompt.

Usage: python nosql_picker.py "user sessions with TTL"
       python nosql_picker.py "time series sensor data 1B rows"
"""
import sys

PATTERNS = [
    # (pattern keywords, recommended_store, rationale)
    ("session cache ttl",           "redis",    "in-memory + TTL native"),
    ("rate limit sliding window",   "redis",    "sorted sets are O(log N)"),
    ("leaderboard counter rank",    "redis",    "ZADD/ZINCRBY atomic"),
    ("event stream consumer group", "redis",    "XADD/XREADGROUP, no broker needed"),
    ("nested aggregate embed",      "mongodb",  "embed + index on hot fields"),
    ("flexible cms content schema", "mongodb",  "schema evolution, partial validate"),
    ("time series billion rows",    "cassandra","partition by (entity, day)"),
    ("audit log append only write", "cassandra","write-optimized LSM"),
    ("recommendation social graph", "neo4j",    "graph traversal beats recursive CTEs"),
    ("relational jsonb occasional", "postgres", "JSONB is good enough; default choice"),
    ("unknown access pattern",      "postgres", "defer NoSQL until pain is measured"),
]


def pick(query: str) -> list[tuple[str, str, str]]:
    q = query.lower()
    return [p for p in PATTERNS if any(w in q for w in p[0].split())]


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not query:
        print("Usage: python nosql_picker.py <access pattern description>")
        sys.exit(1)
    matches = pick(query)
    if not matches:
        print("No match — default: postgres (start here, migrate on measured pain)")
    else:
        for store, _, rationale in matches:
            print(f"{store:10s} | {rationale}")
