# Load Balancer Health Check Implementation

## Summary

**One-sentence:** Generates /health + /health/live + /health/ready endpoints (Python/Node/Go) with bounded dependency probes + LB probe config (intervals + thresholds).

**One-paragraph:** Health checks are the mechanism by which load balancers remove dead backends from rotation. Implement three endpoints: `/health` (basic process alive, used by LB), `/health/live` (Kubernetes liveness — restarts the pod on failure), `/health/ready` (readiness — removes from LB pool without restart, deep dependency probe). Configure check intervals between 10–30 s with tuned healthy / unhealthy thresholds per backend type and ALWAYS bound the readiness probe with a per-dependency timeout (`5 s` is the typical default).

**Ефективно для:**

- New service behind LB: відразу wired liveness + readiness + deep probe.
- Existing service flapping in pool: розділити /live vs /ready, додати threshold tuning.
- Kubernetes: livenessProbe restart pod, readinessProbe usuwa з LB без restart.
- Deep probe з DB/Redis/Queue — return 503 коли downstream падає.
- gRPC service: `grpc.health.v1.Health/Check` за стандартом.

## Applies If (ALL must hold)

- Implementing a new backend service that will sit behind a load balancer.
- Adding Kubernetes liveness and readiness probes to an existing service.
- Debugging flapping services being incorrectly removed from the LB pool.
- Hardening a service so the LB accurately reflects dependency health.

## Skip If (ANY kills it)

- TCP-only services — use `tcp-check` (HAProxy) or `TCPSocket` probe (K8s).
- Stateless functions (FaaS / Lambda) — platform manages health.
- Database load balancing — use protocol-specific health checks (mysql-check, pgsql-check).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service runtime | Python / Node / Go | repo |
| Dependency list | DB / cache / queue / downstream HTTP | architecture |
| LB technology | HAProxy / Nginx / K8s / cloud | infra |
| SLO for failure detection | seconds | SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lb-haproxy-production]] | Backend health-check syntax (`option httpchk` + `expect`). |
| [[lb-kubernetes-ingress]] | Kubernetes liveness / readiness probe semantics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: liveness-ne-readiness, deep-probe-deps, timeout-bound-probe, threshold-tuned, expect-status-match | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `write-handler` | sonnet | Per-language handler with bounded deps. |
| `wire-probe-config` | sonnet | LB-specific config block. |
| `tune-thresholds` | haiku | Mechanical arithmetic from SLO. |

## Templates

| File | Purpose |
|------|---------|
| `templates/health-handlers.py` | Flask handlers for /health, /health/live, /health/ready with timeouts |
| `templates/probe-config.yaml` | Kubernetes livenessProbe + readinessProbe + startupProbe block |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-health-checks.py` | Validate the health-check artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-haproxy-production]]
- [[lb-nginx-production]]
- [[lb-kubernetes-ingress]]
- [[lb-monitoring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (runtime, dependencies, K8s vs raw LB, latency budget) to a concrete probe shape, each leaf referencing a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/health-handlers.py`

```python
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
```

### `templates/probe-config.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  template:
    spec:
      containers:
        - name: web
          image: registry.example.com/web:1.2.3
          ports:
            - containerPort: 8080
          startupProbe:
            httpGet:
              path: /health/live
              port: 8080
            periodSeconds: 10
            failureThreshold: 30          # tolerate up to ~5 min cold-boot / migrations
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 0        # startupProbe gates this
            periodSeconds: 10
            timeoutSeconds: 2
            successThreshold: 1
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 0
            periodSeconds: 10
            timeoutSeconds: 5             # > sum of bounded dep timeouts (3 s + 2 s)
            successThreshold: 2
            failureThreshold: 3
```
