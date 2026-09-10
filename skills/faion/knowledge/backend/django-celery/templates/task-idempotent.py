# purpose: Celery task template with idempotency, retry, time limits
# consumes: See content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
# task-idempotent.py — Canonical idempotent Celery task pattern
# Input:  user_id (int, primitive)
# Output: bool — True if action was performed, False if already done
#
# The guard is on the CORRECT side of the side effect: claim first, act second.
# The first version read the flag, sent the email, THEN did the atomic UPDATE.
# With acks_late=True and max_retries=5, a worker lost after the send but
# before the UPDATE re-delivers the task, the flag is still False, and the
# user receives the email again — up to six times. The claim below is the
# atomic UPDATE ... WHERE welcome_email_sent = FALSE; whoever wins it owns the
# send, everyone else returns False without touching the provider. If the send
# then fails, the claim is released so the retry can win it again.


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
    Send welcome email to user. Idempotent under retries and redelivery.
    """
    from apps.users.models import User

    # 1. Claim. Exactly one execution turns the flag; concurrent retries lose here.
    claimed = User.objects.filter(pk=user_id, welcome_email_sent=False).update(
        welcome_email_sent=True
    )
    if not claimed:
        return False  # already sent, or being sent by another execution

    user = User.objects.only("id", "email").get(pk=user_id)

    # 2. Act. The provider-side idempotency key is derived from the task, so
    #    even a network-level duplicate of this POST cannot send twice.
    try:
        _send_welcome_email(user.email, idempotency_key=f"welcome:{user_id}")
    except requests.RequestException:
        # 3. Release the claim so the retry can win it. Without this the
        #    first failed attempt would mark the email sent forever.
        User.objects.filter(pk=user_id).update(welcome_email_sent=False)
        raise
    return True


def _send_welcome_email(email: str, *, idempotency_key: str) -> None:
    """Send the actual email. Raises requests.RequestException on failure."""
    response = requests.post(
        "https://api.email-provider.com/send",
        json={"to": email, "template": "welcome"},
        headers={"Idempotency-Key": idempotency_key},
        timeout=30,
    )
    response.raise_for_status()
