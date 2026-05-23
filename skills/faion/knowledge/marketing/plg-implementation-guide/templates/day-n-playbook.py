# purpose: Day-N freemium-to-paid playbook generator with PQL gating
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~400-1000 tokens when loaded as context

"""
day_n_playbook.py — schedule freemium-to-paid Day-N message queue.

All generated messages have approved=False. A human reviewer must flip
approved=True via the campaign platform (Customer.io, Klaviyo, etc.)
before any message is sent. Never auto-send.

Matches the Freemium-to-Paid playbook in content/02-playbooks.xml.
"""
from datetime import datetime, timedelta, timezone


PLAYBOOK = [
    (0,  "in_app",  "limit_notification"),        # Day 0: in-app at 80% limit
    (2,  "email",   "limit_value_email"),          # Day 2: email with value + social proof
    (5,  "in_app",  "remaining_capacity_reminder"),# Day 5: in-app remaining capacity
    (7,  "email",   "discount_offer_20pct"),       # Day 7: 20% off first 3 months
]


def schedule(user_id: str, trigger_ts: datetime) -> list[dict]:
    """
    Generate a Day-N message queue for one user starting at trigger_ts.

    Args:
        user_id    : unique user identifier
        trigger_ts : datetime when limit-80%-hit event fired (UTC)

    Returns:
        List of message dicts. All have approved=False.
    """
    return [
        {
            "user_id": user_id,
            "send_at": (trigger_ts + timedelta(days=d)).isoformat(),
            "channel": channel,
            "template": template,
            "approved": False,  # human review required before send
        }
        for d, channel, template in PLAYBOOK
    ]


if __name__ == "__main__":
    queue = schedule("user_123", datetime.now(timezone.utc))
    for msg in queue:
        print(msg)
