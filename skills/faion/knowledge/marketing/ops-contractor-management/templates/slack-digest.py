"""
Weekly contractor status digest from a Slack channel.

Input:  channel_id (str), contractor_user_id (str), days (int, default 7)
Output: dict with message count, first/last messages, and raw message list

Prerequisites: SLACK_BOT_TOKEN env var with channels:history scope.

Usage:
    digest = weekly_digest("C01234567", "U09876543", days=7)
    print(f"Messages: {digest['msg_count']}")
    for msg in digest['raw']:
        print(msg)
"""

import os
import time

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def weekly_digest(channel_id: str, contractor_user_id: str, days: int = 7) -> dict:
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        return {"error": "SLACK_BOT_TOKEN not set"}

    client = WebClient(token=token)
    oldest = time.time() - days * 86400

    try:
        response = client.conversations_history(
            channel=channel_id,
            oldest=str(oldest),
            limit=200,
        )
    except SlackApiError as exc:
        return {"error": str(exc)}

    messages = [
        m for m in response.get("messages", [])
        if m.get("user") == contractor_user_id and m.get("type") == "message"
    ]

    return {
        "msg_count": len(messages),
        "period_days": days,
        "first": messages[-1]["text"] if messages else None,
        "last": messages[0]["text"] if messages else None,
        "raw": [m["text"] for m in messages],
    }
