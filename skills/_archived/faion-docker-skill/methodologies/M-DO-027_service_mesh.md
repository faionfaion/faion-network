# M-DO-027: Service Mesh with Istio

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Advanced
- **Tags:** #devops, #servicemesh, #istio, #kubernetes, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Microservice communication is complex. Implementing retries, circuit breakers, and mTLS in every service is repetitive. Observability across services is fragmented.

## Promise

After this methodology, you will manage service-to-service communication with Istio. Traffic management, security, and observability will be infrastructure concerns.

## Overview

A service mesh provides traffic management, security, and observability for microservices. Istio uses sidecar proxies to intercept all network traffic.

---

## Framework

### Step 1: Istio Installation

```bash
# Download Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.20.0
export PATH=$PWD/bin:$PATH

# Install with demo profile
istioctl install --set profile=demo -y

# Enable sidecar injection
kubectl label namespace default istio-injection=enabled

# Install addons
kubectl apply -f samples/addons/prometheus.yaml
kubectl apply -f samples/addons/grafana.yaml
kubectl apply -f samples/addons/jaeger.yaml
kubectl apply -f samples/addons/kiali.yaml

# Access Kiali dashboard
istioctl dashboard kiali
```

### Step 2: Traffic Management

```yaml
# VirtualService for routing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api
spec:
  hosts:
    - api
  http:
    - match:
        - headers:
            x-version:
              exact: "v2"
      route:
        - destination:
            host: api
            subset: v2
    - route:
        - destination:
            host: api
            subset: v1
          weight: 90
        - destination:
            host: api
            subset: v2
          weight: 10

---
# DestinationRule for subsets
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: api
spec:
  host: api
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

### Step 3: Retries and Timeouts

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api
spec:
  hosts:
    - api
  http:
    - route:
        - destination:
            host: api
      timeout: 10s
      retries:
        attempts: 3
        perTryTimeout: 3s
        retryOn: connect-failure,refused-stream,unavailable,cancelled,retriable-4xx,503
```

### Step 4: Circuit Breaker

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: api
spec:
  host: api
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
        maxRequestsPerConnection: 10
        maxRetries: 3
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 100
      minHealthPercent: 30
```

### Step 5: mTLS Security

```yaml
# Strict mTLS for namespace
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT

---
# Authorization policy
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-policy
  namespace: production
spec:
  selector:
    matchLabels:
      app: api
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              - cluster.local/ns/production/sa/frontend
              - cluster.local/ns/production/sa/worker
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/*"]
```

### Step 6: Ingress Gateway

```yaml
# Gateway
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: main-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: tls-secret
      hosts:
        - "api.example.com"
        - "www.example.com"

---
# VirtualService for gateway
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: external
spec:
  hosts:
    - "api.example.com"
  gateways:
    - main-gateway
  http:
    - match:
        - uri:
            prefix: /api
      route:
        - destination:
            host: api
            port:
              number: 80
    - route:
        - destination:
            host: web
            port:
              number: 80
```

---

## Templates

### Canary Deployment

```yaml
# Deploy v2 with 10% traffic
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api
spec:
  hosts:
    - api
  http:
    - route:
        - destination:
            host: api
            subset: v1
          weight: 90
        - destination:
            host: api
            subset: v2
          weight: 10

---
# Gradually increase to 50%
# Then 100% and remove v1
```

### Fault Injection (Testing)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api
spec:
  hosts:
    - api
  http:
    - fault:
        delay:
          percentage:
            value: 10
          fixedDelay: 5s
        abort:
          percentage:
            value: 5
          httpStatus: 503
      route:
        - destination:
            host: api
```

### Request Mirroring

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api
spec:
  hosts:
    - api
  http:
    - route:
        - destination:
            host: api
            subset: v1
      mirror:
        host: api
        subset: v2
      mirrorPercentage:
        value: 100
```

---

## Examples

### Rate Limiting

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: rate-limit
  namespace: istio-system
spec:
  workloadSelector:
    labels:
      istio: ingressgateway
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: GATEWAY
        listener:
          filterChain:
            filter:
              name: "envoy.filters.network.http_connection_manager"
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.local_ratelimit
          typed_config:
            "@type": type.googleapis.com/udpa.type.v1.TypedStruct
            type_url: type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
            value:
              stat_prefix: http_local_rate_limiter
              token_bucket:
                max_tokens: 100
                tokens_per_fill: 10
                fill_interval: 1s
```

### Observability

```bash
# View mesh topology
istioctl dashboard kiali

# View traces
istioctl dashboard jaeger

# View metrics
istioctl dashboard grafana

# Analyze mesh config
istioctl analyze

# Debug proxy config
istioctl proxy-config routes deploy/api
istioctl proxy-config clusters deploy/api
```

---

## Common Mistakes

1. **No sidecar injection** - Pods need label
2. **Permissive mTLS** - Use STRICT in production
3. **Missing destination rules** - Traffic policies not applied
4. **Resource heavy** - Size sidecars appropriately
5. **Complexity** - Start with basics, add features gradually

---

## Checklist

- [ ] Istio installed
- [ ] Sidecar injection enabled
- [ ] Gateway configured
- [ ] mTLS in STRICT mode
- [ ] Authorization policies defined
- [ ] Traffic policies configured
- [ ] Observability addons deployed
- [ ] Resource limits for sidecars

---

## Next Steps

- M-DO-005: Kubernetes Basics
- M-DO-013: Distributed Tracing
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-027 v1.0*
