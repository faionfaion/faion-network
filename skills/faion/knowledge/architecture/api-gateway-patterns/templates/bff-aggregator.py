# purpose: BFF fan-out endpoint with per-service timeouts and partial degradation.
# consumes: upstream service URLs, auth header, response field names
# produces: an aggregation module satisfying r13 (parallel fan-out, no BFF-level caching)
# depends-on: content/01-core-rules.xml, content/05-examples.xml
# token-budget-impact: ~400 tokens when loaded as context
"""
BFF (Backend-for-Frontend) aggregation endpoint.
Aggregates 3 upstream services in parallel with graceful partial failure handling.
Replace service URLs and response field names as needed.

Three rules this file must honour, and how the first version broke each:

* PER-SERVICE TIMEOUTS — one `httpx.AsyncClient(timeout=2.0)` is a single
  global budget. Each upstream now gets its own deadline via
  `asyncio.wait_for`, so a slow notifications service cannot eat the budget
  the user profile needed.
* PARTIAL DEGRADATION — a bare `asyncio.gather` raises on the first failure,
  so one refused upstream returned a 500 and the degraded branches below
  never executed. `return_exceptions=True` turns every failure into a value
  the response can degrade on.
* UNIQUE REQUEST ID — `"X-Request-ID": "generated-uuid"` was the literal
  string, so every request shared one id and tracing was impossible. It is
  generated per request, or propagated from the caller when present.
"""
import asyncio
import uuid

import httpx
from fastapi import FastAPI, Header

app = FastAPI()

# Per-upstream deadlines in seconds. Tune per service; the profile is on the
# critical path, the rest can degrade.
UPSTREAMS = {
    "user": ("http://user-svc/me", 1.5),
    "orders": ("http://order-svc/me/orders?limit=5", 1.0),
    "notifications": ("http://notify-svc/me/unread", 0.8),
}


async def _fetch(client: httpx.AsyncClient, url: str, headers: dict, deadline: float):
    return await asyncio.wait_for(client.get(url, headers=headers), timeout=deadline)


@app.get("/api/dashboard")
async def get_dashboard(
    authorization: str = Header(...),
    x_request_id: str | None = Header(default=None),
):
    request_id = x_request_id or uuid.uuid4().hex
    headers = {"Authorization": authorization, "X-Request-ID": request_id}

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *(_fetch(client, url, headers, deadline) for url, deadline in UPSTREAMS.values()),
            return_exceptions=True,
        )
    by_name = dict(zip(UPSTREAMS, results))

    def ok(name: str):
        r = by_name[name]
        return isinstance(r, httpx.Response) and r.is_success

    degraded = [name for name in UPSTREAMS if not ok(name)]
    return {
        "request_id": request_id,
        "user": by_name["user"].json() if ok("user") else None,
        "orders": by_name["orders"].json() if ok("orders") else [],
        "notifications": by_name["notifications"].json() if ok("notifications") else [],
        # The client can render what arrived and label what did not.
        "degraded": degraded,
    }
