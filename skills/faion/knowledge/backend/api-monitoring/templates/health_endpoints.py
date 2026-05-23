# purpose: Template helper for API Monitoring (health_endpoints.py).
# consumes: see content/02-output-contract.xml inputs for api-monitoring
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
"""
FastAPI health probes: liveness (shallow) + readiness (dependency checks).
Liveness: returns 200 immediately — process alive check only.
Readiness: checks DB, Redis, and critical external APIs.
"""
import json
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import Response
import asyncpg
import aioredis
import httpx

app = FastAPI()

DATABASE_URL = "postgresql://..."
REDIS_URL = "redis://localhost:6379"


@app.get("/health")
async def liveness():
    """Liveness probe — never call DB here (cascade restart risk)."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/health/ready")
async def readiness():
    """Readiness probe — check all critical dependencies."""
    checks: dict = {}

    # Database
    try:
        pool = await asyncpg.create_pool(DATABASE_URL)
        await pool.fetchval("SELECT 1")
        await pool.close()
        checks["database"] = {"status": "ok"}
    except Exception as e:
        checks["database"] = {"status": "error", "error": str(e)}

    # Redis
    try:
        redis = await aioredis.from_url(REDIS_URL)
        await redis.ping()
        await redis.close()
        checks["redis"] = {"status": "ok"}
    except Exception as e:
        checks["redis"] = {"status": "error", "error": str(e)}

    all_ok = all(c["status"] == "ok" for c in checks.values())
    status_code = 200 if all_ok else 503

    return Response(
        content=json.dumps({
            "status": "ok" if all_ok else "degraded",
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat(),
        }),
        status_code=status_code,
        media_type="application/json",
    )
