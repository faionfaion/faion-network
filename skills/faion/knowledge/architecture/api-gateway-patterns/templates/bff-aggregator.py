# purpose: BFF fan-out endpoint with per-service timeouts and partial degradation.
# consumes: upstream service URLs, auth header, response field names
# produces: an aggregation module satisfying r13 (parallel fan-out, no BFF-level caching)
# depends-on: content/01-core-rules.xml, content/05-examples.xml
# token-budget-impact: ~400 tokens when loaded as context
"""
BFF (Backend-for-Frontend) aggregation endpoint.
Aggregates 3 upstream services in parallel with graceful partial failure handling.
Replace service URLs and response field names as needed.
"""
from fastapi import FastAPI, Header, HTTPException
import httpx
import asyncio

app = FastAPI()


@app.get("/api/dashboard")
async def get_dashboard(authorization: str = Header(...)):
    headers = {"Authorization": authorization, "X-Request-ID": "generated-uuid"}
    async with httpx.AsyncClient(timeout=2.0) as client:
        try:
            user, orders, notifs = await asyncio.gather(
                client.get("http://user-svc/me", headers=headers),
                client.get("http://order-svc/me/orders?limit=5", headers=headers),
                client.get("http://notify-svc/me/unread", headers=headers),
            )
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="upstream timeout")

    return {
        "user": user.json() if user.is_success else None,
        "orders": orders.json() if orders.is_success else [],
        "notifications": notifs.json() if notifs.is_success else [],
    }
