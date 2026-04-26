"""
health-endpoint.py — FastAPI /health endpoint with parallel DB + Redis checks
Copy into your FastAPI application and adapt check functions to your dependencies.
"""

import time
import asyncio
from fastapi import FastAPI, Response

app = FastAPI()
START_TIME = time.time()


async def check_database():
    try:
        start = time.time()
        async with db_pool.acquire() as conn:
            await conn.execute("SELECT 1")
        return {"status": "ok", "latency_ms": round((time.time() - start) * 1000, 1)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def check_redis():
    try:
        start = time.time()
        await redis_client.ping()
        return {"status": "ok", "latency_ms": round((time.time() - start) * 1000, 1)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/health")
async def health(response: Response):
    checks = {}
    checks["database"], checks["redis"] = await asyncio.gather(
        check_database(), check_redis()
    )

    all_ok = all(c["status"] == "ok" for c in checks.values())
    if not all_ok:
        response.status_code = 503

    return {
        "status": "ok" if all_ok else "degraded",
        "uptime_seconds": round(time.time() - START_TIME),
        "checks": checks,
    }


@app.get("/health/live")
async def health_live():
    """Liveness check — process is alive, no dependency checks."""
    return Response(status_code=200)
