# purpose: truncate + replay rebuild script per rebuildable-from-zero rule
# consumes: projection + event store
# produces: rebuilt read model
# depends-on: content/01-core-rules.xml, templates/Projection.py
# token-budget-impact: ~200 tokens when loaded as reference

from __future__ import annotations

import argparse
import sys
from typing import Iterable, Protocol


class EventSource(Protocol):
    def read_all_events(self) -> Iterable: ...


class ReadStore(Protocol):
    def truncate(self, table: str) -> None: ...
    def delete_checkpoint(self, name: str) -> None: ...


def rebuild(projection, source: EventSource, store: ReadStore) -> int:
    store.truncate(projection.TABLE)
    store.delete_checkpoint(projection.NAME)
    count = 0
    for position, event in enumerate(source.read_all_events(), start=1):
        projection.handle(event, position=position)
        count += 1
    return count


def main() -> int:
    ap = argparse.ArgumentParser(description="rebuild a projection from offset 0")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.dry_run:
        sys.stdout.write("dry-run OK\n")
        return 0
    sys.stdout.write("instantiate projection + source + store, then call rebuild()\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
