# Service Mesh

Infrastructure layer for service-to-service communication.

## What is a Service Mesh?

Dedicated infrastructure layer handling:
- Service discovery
- Load balancing
- Encryption (mTLS)
- Observability
- Traffic management

```
┌───────────────────────────────────────────┐
│              Service Mesh                  │
│                                           │
│  ┌─────────┐        ┌─────────┐          │
│  │Service A│        │Service B│          │
│  │ ┌─────┐ │        │ ┌─────┐ │          │
│  │ │ App │ │        │ │ App │ │          │
│  │ └──┬──┘ │        │ └──┬──┘ │          │
│  │ ┌──┴──┐ │ mTLS   │ ┌──┴──┐ │          │
│  │ │Proxy│◀┼────────┼▶│Proxy│ │          │
│  │ └─────┘ │        │ └─────┘ │          │
│  └─────────┘        └─────────┘          │
│        │                  │              │
│        └────────┬─────────┘              │
│                 ▼                        │
│          Control Plane                   │
│    (config, certs, telemetry)            │
└───────────────────────────────────────────┘
```

## Components

### Data Plane
- **Sidecar proxies** - Run alongside each service
- Handle all network traffic
- Envoy is most common

### Control Plane
- **Configuration** - Define routing, policies
- **Certificate management** - Issue/rotate certs
- **Telemetry collection** - Gather metrics

## Popular Service Meshes

| Mesh | Best For |
|------|----------|
| **Istio** | Full featured, complex |
| **Linkerd** | Lightweight, simple |
| **Consul Connect** | HashiCorp ecosystem |
| **Cilium** | eBPF-based, performance |

## Key Features

### mTLS (Mutual TLS)

Automatic encryption between services.

```
Service A ←──mTLS──→ Service B
  │                      │
  Proxy                  Proxy
  (cert A)               (cert B)
```

**Benefits:**
- Encryption in transit
- Service identity verification
- No code changes needed

### Traffic Management

```yaml
# Istio VirtualService - Traffic splitting
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 90
    - destination:
        host: reviews
        subset: v2
      weight: 10  # Canary 10%
```

### Circuit Breaking

```yaml
# Istio DestinationRule
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews
spec:
  host: reviews
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
```

### Retry Policy

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: ratings
spec:
  hosts:
  - ratings
  http:
  - route:
    - destination:
        host: ratings
    retries:
      attempts: 3
      perTryTimeout: 2s
      retryOn: 5xx,reset,connect-failure
```

### Timeout

```yaml
http:
- route:
  - destination:
      host: reviews
  timeout: 10s
```

## Observability

### Distributed Tracing
```
Request → Service A → Service B → Service C
          [span 1]    [span 2]    [span 3]
          └─────────── trace ────────────┘
```

**Tools:** Jaeger, Zipkin

### Metrics
```
istio_requests_total{source="serviceA", destination="serviceB"}
istio_request_duration_milliseconds_bucket{...}
```

**Tools:** Prometheus + Grafana

### Service Graph
Visual representation of service dependencies.

**Tools:** Kiali (for Istio)

## Istio Architecture

```
                    ┌─────────────────────┐
                    │    Control Plane    │
                    │                     │
                    │  ┌───────────────┐  │
                    │  │    istiod     │  │
                    │  │  - Pilot      │  │
                    │  │  - Citadel    │  │
                    │  │  - Galley     │  │
                    │  └───────────────┘  │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │   Pod       │     │   Pod       │     │   Pod       │
    │ ┌────────┐  │     │ ┌────────┐  │     │ ┌────────┐  │
    │ │  App   │  │     │ │  App   │  │     │ │  App   │  │
    │ └────────┘  │     │ └────────┘  │     │ └────────┘  │
    │ ┌────────┐  │     │ ┌────────┐  │     │ ┌────────┐  │
    │ │ Envoy  │  │     │ │ Envoy  │  │     │ │ Envoy  │  │
    │ └────────┘  │     │ └────────┘  │     │ └────────┘  │
    └─────────────┘     └─────────────┘     └─────────────┘
                    Data Plane (Sidecar Proxies)
```

## When to Use

**Good for:**
- Large microservices deployments
- Zero-trust security requirements
- Complex traffic management
- Need for observability

**Not needed for:**
- Small number of services
- Simple traffic patterns
- Tight resource constraints

## Related

- [microservices-architecture.md](microservices-architecture.md) - Service design
- [container-orchestration.md](container-orchestration.md) - Kubernetes
- [security-architecture.md](security-architecture.md) - Security patterns
