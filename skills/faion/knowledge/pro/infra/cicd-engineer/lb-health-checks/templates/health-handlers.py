# purpose: Flask /health, /health/live, /health/ready handlers with bounded dependency probes
# consumes: see content/02-output-contract.xml inputs (liveness_path, readiness_path, readiness_deps)
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml (liveness-ne-readiness, deep-probe-deps, timeout-bound-probe)
# token-budget-impact: ~500 tokens when loaded as context

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FTimeout

from flask import Flask, jsonify

import psycopg2
import redis

app = Flask(__name__)

DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.environ["REDIS_URL"]

_executor = ThreadPoolExecutor(max_workers=4)


def _check_postgres(timeout_sec: float = 3.0) -> bool:
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=int(timeout_sec))
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
        conn.close()
        return True
    except Exception:
        return False


def _check_redis(timeout_sec: float = 2.0) -> bool:
    try:
        r = redis.Redis.from_url(REDIS_URL, socket_timeout=timeout_sec)
        return bool(r.ping())
    except Exception:
        return False


def _run_with_timeout(fn, timeout_sec):
    fut = _executor.submit(fn, timeout_sec)
    try:
        return bool(fut.result(timeout=timeout_sec + 0.5))
    except FTimeout:
        return False


@app.route("/health")
def health():
    """Basic health — process is running. LB wires here only if no readiness available."""
    return jsonify({"status": "healthy"}), 200


@app.route("/health/live")
def liveness():
    """Liveness — kubelet restarts pod on failure. Keep this cheap and unconditional."""
    return jsonify({"status": "alive"}), 200


@app.route("/health/ready")
def readiness():
    """Readiness — LB removes pod from pool on failure. Probes every critical dependency."""
    checks = {
        "postgres": _run_with_timeout(_check_postgres, 3.0),
        "redis":    _run_with_timeout(_check_redis,    2.0),
    }
    healthy = all(checks.values())
    status = 200 if healthy else 503
    return jsonify({"status": "ready" if healthy else "not ready", "checks": checks}), status


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
