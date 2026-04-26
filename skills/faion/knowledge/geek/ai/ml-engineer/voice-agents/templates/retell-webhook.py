"""Retell AI webhook handler for voice agent call events."""
import hashlib
import hmac
import json
import os
from fastapi import FastAPI, HTTPException, Request, Response

app = FastAPI()

RETELL_API_KEY = os.environ["RETELL_API_KEY"]


def verify_retell_signature(payload: bytes, signature: str) -> bool:
    """Verify the X-Retell-Signature header."""
    expected = hmac.new(
        RETELL_API_KEY.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@app.post("/retell/webhook")
async def retell_webhook(request: Request) -> Response:
    """Handle Retell AI call lifecycle events."""
    payload = await request.body()
    signature = request.headers.get("X-Retell-Signature", "")

    if not verify_retell_signature(payload, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    event = json.loads(payload)
    event_type = event.get("event")

    if event_type == "call_started":
        call_id = event["data"]["call_id"]
        # Initialize call state, log start
        print(f"Call started: {call_id}")

    elif event_type == "call_ended":
        call_id = event["data"]["call_id"]
        duration_s = event["data"].get("duration_ms", 0) / 1000
        # Log call, update billing, trigger post-call actions
        print(f"Call ended: {call_id}, duration: {duration_s:.1f}s")

    elif event_type == "call_analyzed":
        call_id = event["data"]["call_id"]
        transcript = event["data"].get("transcript", "")
        # Store transcript, run sentiment analysis, extract entities
        print(f"Call analyzed: {call_id}, transcript length: {len(transcript)}")

    return Response(status_code=204)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
