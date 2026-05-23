# purpose: SnapshotStore with version-awareness + fall-back to replay-from-zero
# consumes: DB connection + aggregate (de)serializer
# produces: snapshot read/write API used by the repository
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~300 tokens when loaded as reference

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Optional, Protocol
from uuid import UUID

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Snapshot:
    aggregate_type: str
    stream_id: UUID
    snapshot_version: int
    schema_version: int
    payload: dict


class DB(Protocol):
    def execute(self, sql: str, *args) -> None: ...
    def fetchone(self, sql: str, *args) -> Optional[tuple]: ...


class SnapshotStore:
    def __init__(self, db: DB, current_schema_version: int) -> None:
        self._db = db
        self._schema = current_schema_version

    def get_latest(self, aggregate_type: str, stream_id: UUID) -> Optional[Snapshot]:
        row = self._db.fetchone(
            "SELECT snapshot_version, schema_version, payload "
            "FROM aggregate_snapshots WHERE aggregate_type=%s AND stream_id=%s "
            "ORDER BY snapshot_version DESC LIMIT 1",
            aggregate_type, str(stream_id),
        )
        if row is None:
            return None
        snap_v, schema_v, payload = row
        if schema_v != self._schema:
            log.info("snapshot schema_version %s != current %s; falling back to replay", schema_v, self._schema)
            return None
        try:
            return Snapshot(aggregate_type, stream_id, snap_v, schema_v, json.loads(payload))
        except Exception as exc:
            log.warning("snapshot deserialise failed for %s/%s: %s", aggregate_type, stream_id, exc)
            return None

    def write(self, snap: Snapshot) -> None:
        self._db.execute(
            "INSERT INTO aggregate_snapshots(aggregate_type, stream_id, snapshot_version, schema_version, payload) "
            "VALUES (%s, %s, %s, %s, %s)",
            snap.aggregate_type, str(snap.stream_id), snap.snapshot_version, snap.schema_version,
            json.dumps(snap.payload),
        )

    def invalidate(self, aggregate_type: str) -> None:
        self._db.execute("DELETE FROM aggregate_snapshots WHERE aggregate_type=%s", aggregate_type)
