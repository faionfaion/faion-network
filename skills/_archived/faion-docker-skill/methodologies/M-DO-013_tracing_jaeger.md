# M-DO-013: Distributed Tracing with Jaeger

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #tracing, #jaeger, #observability, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Requests span multiple services. When something is slow, it's hard to identify which service is the bottleneck. Logs don't show the full request path.

## Promise

After this methodology, you will trace requests across services with Jaeger. You'll identify latency bottlenecks and understand service dependencies.

## Overview

Distributed tracing follows requests across microservices. Jaeger collects, stores, and visualizes traces. OpenTelemetry provides the instrumentation.

---

## Framework

### Step 1: Jaeger Setup

```yaml
# docker-compose.yml
version: "3.9"

services:
  jaeger:
    image: jaegertracing/all-in-one:1.52
    ports:
      - "16686:16686"  # UI
      - "4317:4317"    # OTLP gRPC
      - "4318:4318"    # OTLP HTTP
      - "14268:14268"  # Jaeger HTTP
    environment:
      - COLLECTOR_OTLP_ENABLED=true
```

### Step 2: OpenTelemetry Concepts

```
Trace
├── Span (root): HTTP GET /api/users
│   ├── Span: Database Query
│   ├── Span: Cache Lookup
│   └── Span: HTTP Call to Service B
│       └── Span: Service B Handler
│           ├── Span: Validate Input
│           └── Span: Process Request
```

### Step 3: Node.js Instrumentation

```javascript
// tracing.js
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'api-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV,
  }),
  traceExporter: new OTLPTraceExporter({
    url: 'http://jaeger:4318/v1/traces',
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-fs': { enabled: false },
    }),
  ],
});

sdk.start();

process.on('SIGTERM', () => {
  sdk.shutdown().finally(() => process.exit(0));
});
```

```javascript
// app.js - must be first import
require('./tracing');

const express = require('express');
const { trace, SpanStatusCode } = require('@opentelemetry/api');

const app = express();
const tracer = trace.getTracer('api-service');

app.get('/api/users/:id', async (req, res) => {
  // Current span from auto-instrumentation
  const span = trace.getActiveSpan();
  span.setAttribute('user.id', req.params.id);

  // Custom child span
  const dbSpan = tracer.startSpan('database.query');
  try {
    const user = await db.users.findById(req.params.id);
    dbSpan.setAttribute('db.rows_affected', 1);
    dbSpan.end();

    res.json(user);
  } catch (error) {
    dbSpan.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
    dbSpan.recordException(error);
    dbSpan.end();
    throw error;
  }
});
```

### Step 4: Python Instrumentation

```python
# tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

def init_tracing(app):
    resource = Resource.create({
        "service.name": "user-service",
        "service.version": "1.0.0",
        "deployment.environment": os.getenv("ENV", "development"),
    })

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://jaeger:4318/v1/traces")
    )
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Auto-instrument
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument(engine=db.engine)

    return trace.get_tracer("user-service")
```

```python
# app.py
from flask import Flask, request
from opentelemetry import trace

app = Flask(__name__)
tracer = init_tracing(app)

@app.route('/api/users/<user_id>')
def get_user(user_id):
    # Current span from auto-instrumentation
    span = trace.get_current_span()
    span.set_attribute("user.id", user_id)

    # Custom child span
    with tracer.start_as_current_span("validate_user") as child:
        child.set_attribute("validation.type", "existence")
        user = validate_user_exists(user_id)

    return jsonify(user)
```

### Step 5: Context Propagation

```javascript
// Service A - making request
const axios = require('axios');
const { context, propagation } = require('@opentelemetry/api');

async function callServiceB(data) {
  const headers = {};

  // Inject trace context into headers
  propagation.inject(context.active(), headers);

  return axios.post('http://service-b/api/process', data, { headers });
}

// Service B - receiving request (auto-handled by instrumentation)
// The instrumentation extracts the trace context from headers
```

```python
# Python context propagation
import requests
from opentelemetry import propagate

def call_service_b(data):
    headers = {}
    propagate.inject(headers)

    return requests.post(
        'http://service-b/api/process',
        json=data,
        headers=headers
    )
```

### Step 6: Baggage and Custom Attributes

```javascript
// Add baggage (propagated context)
const { propagation, context, baggage } = require('@opentelemetry/api');

// Set baggage
const bag = baggage.setBaggage(
  baggage.getBaggage(context.active()),
  'user.id',
  { value: '12345' }
);
const ctxWithBaggage = baggage.setActiveBaggage(bag);

// Read baggage in downstream service
const userBaggage = baggage.getBaggage(context.active());
const userId = userBaggage.getEntry('user.id')?.value;
```

---

## Templates

### Kubernetes Deployment with Tracing

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  template:
    spec:
      containers:
        - name: api
          image: api-service:1.0.0
          env:
            - name: OTEL_SERVICE_NAME
              value: "api-service"
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: "http://jaeger-collector:4317"
            - name: OTEL_TRACES_SAMPLER
              value: "parentbased_traceidratio"
            - name: OTEL_TRACES_SAMPLER_ARG
              value: "0.1"  # 10% sampling
```

### Sampling Configuration

```javascript
// Custom sampler
const { ParentBasedSampler, TraceIdRatioBasedSampler } = require('@opentelemetry/sdk-trace-base');

const sampler = new ParentBasedSampler({
  root: new TraceIdRatioBasedSampler(0.1),  // 10% of root spans
});

const sdk = new NodeSDK({
  sampler,
  // ...
});
```

---

## Examples

### Express Middleware

```javascript
const { trace, SpanStatusCode } = require('@opentelemetry/api');

function tracingMiddleware(req, res, next) {
  const span = trace.getActiveSpan();

  if (span) {
    // Add request attributes
    span.setAttribute('http.client_ip', req.ip);
    span.setAttribute('http.user_agent', req.get('user-agent'));

    if (req.user) {
      span.setAttribute('user.id', req.user.id);
      span.setAttribute('user.email', req.user.email);
    }
  }

  // Track response
  res.on('finish', () => {
    if (span) {
      span.setAttribute('http.response_content_length', res.get('content-length'));

      if (res.statusCode >= 400) {
        span.setStatus({
          code: SpanStatusCode.ERROR,
          message: `HTTP ${res.statusCode}`,
        });
      }
    }
  });

  next();
}
```

### Database Span

```javascript
async function queryWithTracing(sql, params) {
  const tracer = trace.getTracer('database');

  return tracer.startActiveSpan('db.query', async (span) => {
    try {
      span.setAttribute('db.system', 'postgresql');
      span.setAttribute('db.statement', sql);
      span.setAttribute('db.operation', sql.split(' ')[0].toUpperCase());

      const start = Date.now();
      const result = await pool.query(sql, params);

      span.setAttribute('db.rows_affected', result.rowCount);
      span.setAttribute('db.duration_ms', Date.now() - start);

      return result;
    } catch (error) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
}
```

---

## Common Mistakes

1. **No context propagation** - Traces break between services
2. **Over-sampling** - Storage costs explode
3. **Missing error recording** - Errors not visible in traces
4. **No service naming** - Can't identify services
5. **Sensitive data in spans** - PII in trace attributes

---

## Checklist

- [ ] Jaeger deployed
- [ ] OpenTelemetry SDK configured
- [ ] Auto-instrumentation enabled
- [ ] Context propagation working
- [ ] Custom spans for business logic
- [ ] Error recording implemented
- [ ] Sampling configured
- [ ] Service topology visible

---

## Next Steps

- M-DO-011: Prometheus Monitoring
- M-DO-012: Centralized Logging
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-013 v1.0*
