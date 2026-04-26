"""
OpenTelemetry instrumentation bootstrap for a Python service.

Covers:
- SDK initialisation (traces + metrics)
- W3C TraceContext propagation (B3 format for legacy compatibility)
- Structured logging with trace_id and span_id injection
- Manual span creation pattern

Install:
    pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc \
                opentelemetry-instrumentation-fastapi \
                opentelemetry-instrumentation-requests \
                opentelemetry-instrumentation-logging

Set env vars in your Deployment/pod:
    OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
    OTEL_SERVICE_NAME=payments-api
    OTEL_RESOURCE_ATTRIBUTES=k8s.namespace.name=production
"""

import logging
import os
import json
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


def setup_telemetry(service_name: str | None = None) -> None:
    """
    Initialise OpenTelemetry SDK. Call once at application startup.
    service_name defaults to OTEL_SERVICE_NAME env var.
    """
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    svc = service_name or os.getenv("OTEL_SERVICE_NAME", "unknown-service")

    # Trace provider
    tracer_provider = TracerProvider()
    span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

    # Metrics provider
    metric_exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
    metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=10_000)
    meter_provider = MeterProvider(metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # Propagation: W3C TraceContext primary, B3 for legacy services
    set_global_textmap(CompositePropagator([
        TraceContextTextMapPropagator(),
        B3MultiFormat(),
    ]))


# ---- Structured logging with trace correlation ----

class TraceContextFilter(logging.Filter):
    """Inject trace_id and span_id into every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        span = trace.get_current_span()
        ctx = span.get_span_context()
        if ctx and ctx.is_valid:
            record.trace_id = format(ctx.trace_id, "032x")
            record.span_id = format(ctx.span_id, "016x")
        else:
            record.trace_id = "0" * 32
            record.span_id = "0" * 16
        return True


class JSONFormatter(logging.Formatter):
    """Emit structured JSON logs — one line per record, parseable by Loki."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "trace_id": getattr(record, "trace_id", ""),
            "span_id": getattr(record, "span_id", ""),
            "service": os.getenv("OTEL_SERVICE_NAME", "unknown"),
        }
        # Merge extra kwargs (e.g., logger.info("msg", extra={"user_id": 42}))
        for key, val in record.__dict__.items():
            if key not in logging.LogRecord.__dict__ and not key.startswith("_"):
                log_entry[key] = val
        return json.dumps(log_entry)


def setup_logging() -> None:
    """Configure structured JSON logging with OTel trace injection."""
    handler = logging.StreamHandler()
    handler.addFilter(TraceContextFilter())
    handler.setFormatter(JSONFormatter())
    logging.basicConfig(level=logging.INFO, handlers=[handler])


# ---- Manual span creation pattern ----

tracer = trace.get_tracer(__name__)


def process_payment(payment_id: str, amount_cents: int) -> dict:
    """Example: manual span with attributes and error recording."""
    with tracer.start_as_current_span("process_payment") as span:
        span.set_attribute("payment.id", payment_id)
        span.set_attribute("payment.amount_cents", amount_cents)
        try:
            # ... business logic ...
            result = {"status": "charged", "payment_id": payment_id}
            span.set_attribute("payment.status", "success")
            return result
        except Exception as exc:
            span.record_exception(exc)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
            raise
