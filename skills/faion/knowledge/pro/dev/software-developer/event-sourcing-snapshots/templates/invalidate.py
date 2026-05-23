# purpose: schema-bump invalidation CLI per schema-bump-invalidation rule
# consumes: aggregate type name
# produces: deleted snapshot rows
# depends-on: content/01-core-rules.xml, templates/SnapshotStore.py
# token-budget-impact: ~150 tokens when loaded as reference

from __future__ import annotations

import argparse
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description="invalidate all snapshots for an aggregate type before deploying a new event schema version")
    ap.add_argument("aggregate_type", help="PascalCase aggregate type (e.g. Order)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sys.stdout.write(
        f"would DELETE FROM aggregate_snapshots WHERE aggregate_type='{args.aggregate_type}'\n"
        if args.dry_run
        else f"connect to DB and run invalidate('{args.aggregate_type}') on SnapshotStore\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
