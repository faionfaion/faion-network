"""
FastAPI Prometheus metrics middleware.
Tracks REQUEST_COUNT and REQUEST_LATENCY per method/endpoint/status.
Do NOT add request_id or user_id as labels — cardinality explosion.
"""
from prometheus_client import Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    # Buckets must straddle your SLO thresholds
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        latency = time.time() - start_time

        endpoint = request.url.path  # normalize in production if path params vary
        method = request.method
        status = str(response.status_code)

        REQUEST_COUNT.labels(method, endpoint, status).inc()
        REQUEST_LATENCY.labels(method, endpoint).observe(latency)

        return response


# Register with your FastAPI app:
# app.add_middleware(MetricsMiddleware)
#
# Expose metrics endpoint:
# @app.get("/metrics")
# async def metrics():
#     return Response(generate_latest(), media_type="text/plain")
