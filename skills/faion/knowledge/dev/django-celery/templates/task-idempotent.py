# purpose: Celery task template with idempotency, retry, time limits
# consumes: See content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
# task-idempotent.py — Canonical idempotent Celery task pattern
# Input:  user_id (int, primitive)
# Output: bool — True if action was performed, False if already done

import requests
from celery import shared_task


@shared_task(
    name="emails.send_welcome",
    bind=True,
    max_retries=5,
    autoretry_for=(requests.RequestException,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    soft_time_limit=300,   # fires SoftTimeLimitExceeded
    time_limit=360,        # hard SIGKILL
    acks_late=True,
    task_reject_on_worker_lost=True,
)
def send_welcome(self, user_id: int) -> bool:
    """
    Send welcome email to user.

    Idempotent: checks welcome_email_sent before acting.
    Uses DB-level atomic UPDATE WHERE not_done to prevent race conditions.
    """
    from apps.users.models import User

    user = User.objects.only("id", "email", "welcome_email_sent").get(pk=user_id)

    if user.welcome_email_sent:
        return False  # already sent, safe to return

    # Perform the side effect
    _send_welcome_email(user.email)

    # Atomic guard: only mark done if it was False (handles concurrent retries)
    updated = User.objects.filter(pk=user_id, welcome_email_sent=False).update(
        welcome_email_sent=True
    )
    return bool(updated)


def _send_welcome_email(email: str) -> None:
    """Send the actual email. Raises requests.RequestException on failure."""
    response = requests.post(
        "https://api.email-provider.com/send",
        json={"to": email, "template": "welcome"},
        timeout=30,
    )
    response.raise_for_status()
