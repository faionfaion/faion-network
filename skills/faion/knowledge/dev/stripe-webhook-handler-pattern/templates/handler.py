# purpose: Python handler skeleton: verify-then-idempotent-then-enqueue.
# consumes: see content/02-output-contract.xml inputs for stripe-webhook-handler-pattern
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-700 tokens when loaded as context
from __future__ import annotations
import os
import stripe
from fastapi import APIRouter, Request, HTTPException, Header

router = APIRouter()
WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]


@router.post("/webhooks/stripe")
async def stripe_webhook(req: Request, stripe_signature: str = Header(...)) -> dict:
    body = await req.body()
    # 1) verify signature
    try:
        event = stripe.Webhook.construct_event(body, stripe_signature, WEBHOOK_SECRET)
    except Exception:
        raise HTTPException(status_code=400, detail="bad signature")

    # 2) idempotency dedup on event.id
    if await _seen_event(event["id"]):
        return {"ok": True, "deduped": True}

    # 3) fast 2xx: enqueue heavy work
    await _enqueue(event)
    return {"ok": True}


async def _seen_event(event_id: str) -> bool:
    # INSERT INTO stripe_events(event_id) ON CONFLICT DO NOTHING RETURNING 1
    raise NotImplementedError


async def _enqueue(event: dict) -> None:
    # push to SQS / Celery / pg-boss
    raise NotImplementedError
