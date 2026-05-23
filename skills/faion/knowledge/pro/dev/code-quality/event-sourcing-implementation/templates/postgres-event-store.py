"""
purpose: Python event store with append (optimistic concurrency) + load + snapshot.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (event-sourcing-implementation)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
"""
from __future__ import annotations
import json
from dataclasses import asdict
from typing import List, Optional
from uuid import UUID

import psycopg


class ConcurrencyError(Exception):
    pass


class PostgresEventStore:
    def __init__(self, conn: psycopg.Connection) -> None:
        self.conn = conn

    def append(self, aggregate_id: UUID, aggregate_type: str, events: List[object], expected_version: int) -> None:
        with self.conn.cursor() as cur:
            for i, ev in enumerate(events, start=1):
                try:
                    cur.execute(
                        "INSERT INTO events(event_id, aggregate_id, aggregate_type, event_type, payload, version)"
                        " VALUES (%s, %s, %s, %s, %s, %s)",
                        (str(getattr(ev, "event_id")), str(aggregate_id), aggregate_type, type(ev).__name__,
                         json.dumps(asdict(ev), default=str), expected_version + i),
                    )
                except psycopg.errors.UniqueViolation as e:
                    raise ConcurrencyError(f"stream moved at version {expected_version + i}") from e

    def load_events(self, aggregate_id: UUID, from_version: int = 0) -> list[dict]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT version, event_type, payload FROM events WHERE aggregate_id = %s AND version > %s ORDER BY version",
                (str(aggregate_id), from_version),
            )
            return [{"version": v, "type": t, "payload": p} for v, t, p in cur.fetchall()]

    def load_snapshot(self, aggregate_id: UUID) -> Optional[dict]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT version, state FROM snapshots WHERE aggregate_id = %s ORDER BY version DESC LIMIT 1",
                (str(aggregate_id),),
            )
            row = cur.fetchone()
            return {"version": row[0], "state": row[1]} if row else None

    def save_snapshot(self, aggregate_id: UUID, version: int, state: dict) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO snapshots(aggregate_id, version, state) VALUES (%s, %s, %s)"
                " ON CONFLICT (aggregate_id, version) DO NOTHING",
                (str(aggregate_id), version, json.dumps(state)),
            )
