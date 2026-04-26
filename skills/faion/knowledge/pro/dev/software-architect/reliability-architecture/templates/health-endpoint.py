"""
Health check endpoints following Kubernetes probe conventions.

Three endpoints:
  GET /health/live     — liveness: is the process alive? (restart if fails)
  GET /health/ready    — readiness: can the service accept traffic? (remove from LB)
  GET /health/detailed — detailed: human-readable with dependency status

Django / Flask / FastAPI examples below. Adapt to your framework.

Kubernetes probe config (reference):
  livenessProbe:
    httpGet: { path: /health/live, port: 8000 }
    initialDelaySeconds: 10
    periodSeconds: 10
    failureThreshold: 3
  readinessProbe:
    httpGet: { path: /health/ready, port: 8000 }
    initialDelaySeconds: 5
    periodSeconds: 10
    failureThreshold: 3
  startupProbe:
    httpGet: { path: /health/live, port: 8000 }
    initialDelaySeconds: 0
    periodSeconds: 5
    failureThreshold: 24   # allow 2 min for slow startup
"""

import time
import logging
from dataclasses import dataclass, field
from typing import Literal

logger = logging.getLogger(__name__)

HealthStatus = Literal["healthy", "degraded", "unhealthy"]


@dataclass
class DependencyHealth:
    name: str
    status: HealthStatus
    latency_ms: float | None = None
    error: str | None = None


@dataclass
class HealthReport:
    status: HealthStatus
    version: str
    uptime_seconds: float
    dependencies: list[DependencyHealth] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "version": self.version,
            "uptime_seconds": round(self.uptime_seconds, 1),
            "dependencies": [
                {
                    "name": d.name,
                    "status": d.status,
                    "latency_ms": d.latency_ms,
                    "error": d.error,
                }
                for d in self.dependencies
            ],
        }


_start_time = time.monotonic()


def check_database(db_conn) -> DependencyHealth:
    """Check database connectivity with a lightweight query."""
    start = time.monotonic()
    try:
        db_conn.execute("SELECT 1")
        latency_ms = (time.monotonic() - start) * 1000
        return DependencyHealth("database", "healthy", latency_ms=round(latency_ms, 1))
    except Exception as exc:
        return DependencyHealth("database", "unhealthy", error=str(exc))


def check_redis(redis_client) -> DependencyHealth:
    """Check Redis connectivity with PING."""
    start = time.monotonic()
    try:
        redis_client.ping()
        latency_ms = (time.monotonic() - start) * 1000
        return DependencyHealth("redis", "healthy", latency_ms=round(latency_ms, 1))
    except Exception as exc:
        return DependencyHealth("redis", "unhealthy", error=str(exc))


# --- FastAPI example ---

from fastapi import FastAPI, Response  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402

app = FastAPI()
APP_VERSION = "1.0.0"


@app.get("/health/live")
def liveness():
    """
    Liveness: is the process alive and not deadlocked?
    Return 200 unless the process is in an unrecoverable state.
    Keep this check CHEAP — no external dependencies.
    """
    return {"status": "alive"}


@app.get("/health/ready")
def readiness(response: Response):
    """
    Readiness: can the service handle requests right now?
    Check critical dependencies (database). Return 503 to remove from LB.
    """
    # Only check dependencies that are REQUIRED to serve traffic.
    # A degraded cache is not a reason to stop receiving requests.
    # db = get_db()  # inject your DB dependency
    # db_health = check_database(db)
    # if db_health.status == "unhealthy":
    #     response.status_code = 503
    #     return {"status": "not_ready", "reason": db_health.error}
    return {"status": "ready"}


@app.get("/health/detailed")
def detailed_health():
    """
    Detailed: full dependency status for humans and dashboards.
    Not used by Kubernetes probes — exposed for monitoring/ops.
    """
    uptime = time.monotonic() - _start_time
    # dependencies = [check_database(db), check_redis(cache)]
    dependencies: list[DependencyHealth] = []

    overall = "healthy"
    for dep in dependencies:
        if dep.status == "unhealthy":
            overall = "unhealthy"
            break
        if dep.status == "degraded" and overall == "healthy":
            overall = "degraded"

    report = HealthReport(
        status=overall,
        version=APP_VERSION,
        uptime_seconds=uptime,
        dependencies=dependencies,
    )
    status_code = 200 if overall == "healthy" else 503
    return JSONResponse(content=report.to_dict(), status_code=status_code)
