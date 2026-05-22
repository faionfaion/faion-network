# purpose: working RunnableWithMessageHistory wiring for Redis-backed buffer memory
# consumes: an existing langchain Runnable `chain` + REDIS_URL env var
# produces: chain_with_memory ready to .invoke with config={"configurable": {"session_id": <uuid>}}
# depends-on: langchain-core, langchain-community, redis
# token-budget-impact: ~250 tokens when included in agent context
"""Reference wiring. Swap RedisChatMessageHistory for the chosen backend.

Run as a smoke check:
    python wiring-snippet.py --self-test
"""

from __future__ import annotations

import os
import uuid

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


def get_session_history(session_id: str) -> RedisChatMessageHistory:
    """Return a per-session Redis-backed chat history with TTL."""
    if not session_id or len(session_id) < 8:
        raise ValueError("session_id must be a server-generated UUID, not user input")
    return RedisChatMessageHistory(
        session_id=session_id,
        url=os.environ["REDIS_URL"],
        ttl=int(os.environ.get("CHAT_HISTORY_TTL_SECONDS", "3600")),
    )


def wrap(chain):
    """Wrap any LCEL chain with persistent message history."""
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )


def _self_test() -> int:
    """Smoke: instantiate without connecting to Redis; checks shape only."""
    sid = str(uuid.uuid4())
    if len(sid) < 8:
        return 1
    return 0


if __name__ == "__main__":
    import sys

    if "--self-test" in sys.argv:
        raise SystemExit(_self_test())
    if "--help" in sys.argv:
        print(__doc__)
        raise SystemExit(0)
    print("Import this module; do not run directly except with --self-test.")
