#!/usr/bin/env python3
"""idempotent-handler.py — DB-backed idempotency key claim for message consumers.

Uses a processed_messages table with a UNIQUE constraint on (key) to ensure
each message is processed at most once, even under at-least-once delivery.

Schema:
    CREATE TABLE processed_messages (
        key TEXT PRIMARY KEY,
        processed_at TIMESTAMPTZ DEFAULT NOW()
    );

Usage:
    def handler(msg, db):
        key = message_idempotency_key(msg)
        with claim_once(db, key) as fresh:
            if not fresh:
                return  # duplicate, skip silently
            do_work(msg, db)
"""
import hashlib
from contextlib import contextmanager


def message_idempotency_key(msg: dict) -> str:
    """Use producer-supplied key if present; fall back to deterministic hash."""
    if mid := msg.get("idempotency_key"):
        return mid
    body = repr(sorted(msg.items())).encode()
    return hashlib.sha256(body).hexdigest()


@contextmanager
def claim_once(db, key: str):
    """Claim the idempotency key. Yields True if this is the first claim, False if duplicate.

    On success: commits the claim.
    On exception: rolls back the claim so the message can be retried.
    """
    inserted = db.execute(
        "INSERT INTO processed_messages(key) VALUES (%s) ON CONFLICT DO NOTHING RETURNING 1",
        (key,),
    ).fetchone()

    if not inserted:
        yield False  # duplicate message, caller should skip
        return

    try:
        yield True  # fresh claim
        db.commit()
    except Exception:
        db.rollback()
        # Remove the claim so the message can be retried
        db.execute("DELETE FROM processed_messages WHERE key = %s", (key,))
        db.commit()
        raise
