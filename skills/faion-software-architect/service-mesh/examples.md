# Service Mesh Examples

Real-world configurations for common service mesh scenarios.

## Example 1: E-commerce Platform (Istio)

### Scenario

- 25 microservices
- High traffic (10k RPS peak)
- PCI-DSS compliance (mTLS required)
- Canary deployments
- Full observability

### Architecture

```
                    Internet
                        │
                        ▼
              ┌─────────────────┐
              │  Istio Gateway  │
              │   (LoadBalancer)│
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌───────────┐  ┌───────────┐  ┌───────────┐
│  frontend │  │  checkout │  │   api     │
│  (React)  │  │ (Node.js) │  │  (Go)     │
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌───────────┐  ┌───────────┐  ┌───────────┐
│  catalog  │  │  payment  │  │  inventory│
│ (Python)  │  │  (Java)   │  │  (Go)     │
└───────────┘  └───────────┘  └───────────┘
```

### Installation

```bash
# Install Istio with production profile
istioctl install --set profile=default \
  --set values.pilot.resources.requests.cpu=500m \
  --set values.pilot.resources.requests.memory=2Gi

# Enable namespace injection
kubectl label namespace production istio-injection=enabled

# Install addons
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.24/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.24/samples/addons/grafana.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.24/samples/addons/jaeger.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.24/samples/addons/kiali.yaml
```

### Gateway Configuration

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: ecommerce-gateway
  namespace: production
spec:
  gatewayClassName: istio
  listeners:
    - name: https
      port: 443
      protocol: HTTPS
      tls:
        mode: Terminate
        certificateRefs:
          - name: ecommerce-tls
      allowedRoutes:
        namespaces:
          from: Same

---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: frontend-route
  namespace: production
spec:
  parentRefs:
    - name: ecommerce-gateway
  hostnames:
    - "shop.example.com"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: frontend
          port: 80
```

### mTLS Configuration (Strict)

```yaml
# Cluster-wide strict mTLS
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT

---
# Destination rule for mTLS
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: default
  namespace: production
spec:
  host: "*.production.svc.cluster.local"
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
```

### Canary Deployment (90/10 Split)

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: checkout
  namespace: production
spec:
  hosts:
    - checkout
  http:
    - route:
        - destination:
            host: checkout
            subset: stable
          weight: 90
        - destination:
            host: checkout
            subset: canary
          weight: 10

---
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: checkout
  namespace: production
spec:
  host: checkout
  subsets:
    - name: stable
      labels:
        version: v1
    - name: canary
      labels:
        version: v2
```

### Circuit Breaker

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: payment
  namespace: production
spec:
  host: payment
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
      baseEjectionTime: 60s
      maxEjectionPercent: 50
```

### Authorization Policy (Zero Trust)

```yaml
# Default deny all
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  {}

---
# Allow frontend to call checkout
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend-to-checkout
  namespace: production
spec:
  selector:
    matchLabels:
      app: checkout
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/production/sa/frontend"]
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/*"]

---
# Allow checkout to call payment
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: allow-checkout-to-payment
  namespace: production
spec:
  selector:
    matchLabels:
      app: payment
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/production/sa/checkout"]
      to:
        - operation:
            methods: ["POST"]
            paths: ["/charge", "/refund"]
```

---

## Example 2: SaaS API Platform (Linkerd)

### Scenario

- 12 microservices
- Moderate traffic (2k RPS)
- Simplicity prioritized
- Multi-tenant API
- Quick deployment

### Architecture

```
              ┌─────────────────┐
              │  NGINX Ingress  │
              │   + Linkerd     │
              └────────┬────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌───────────────┐            ┌───────────────┐
│  API Gateway  │            │  Admin Portal │
│   (Node.js)   │            │   (React)     │
└───────┬───────┘            └───────────────┘
        │
   ┌────┴────┬────────┬────────┐
   │         │        │        │
   ▼         ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│users │ │billing│ │reports│ │audit │
└──────┘ └──────┘ └──────┘ └──────┘
```

### Installation

```bash
# Install Linkerd CLI
curl -sL https://run.linkerd.io/install | sh

# Generate certificates (production)
step certificate create root.linkerd.cluster.local ca.crt ca.key \
  --profile root-ca --no-password --insecure

step certificate create identity.linkerd.cluster.local issuer.crt issuer.key \
  --profile intermediate-ca --not-after 8760h --no-password --insecure \
  --ca ca.crt --ca-key ca.key

# Install CRDs
linkerd install --crds | kubectl apply -f -

# Install control plane
linkerd install \
  --identity-trust-anchors-file ca.crt \
  --identity-issuer-certificate-file issuer.crt \
  --identity-issuer-key-file issuer.key \
  | kubectl apply -f -

# Install viz extension
linkerd viz install | kubectl apply -f -

# Verify
linkerd check
```

### Namespace Injection

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: saas-api
  annotations:
    linkerd.io/inject: enabled
```

### Service Profile (Retries & Timeouts)

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: users.saas-api.svc.cluster.local
  namespace: saas-api
spec:
  routes:
    - name: GET /api/users/{id}
      condition:
        method: GET
        pathRegex: /api/users/[^/]+
      timeout: 5s
      retryBudget:
        retryRatio: 0.2
        minRetriesPerSecond: 10
        ttl: 10s
    - name: POST /api/users
      condition:
        method: POST
        pathRegex: /api/users
      timeout: 10s
      # No retries for POST (not idempotent)
```

### Traffic Split (Canary)

```yaml
apiVersion: split.smi-spec.io/v1alpha1
kind: TrafficSplit
metadata:
  name: users-canary
  namespace: saas-api
spec:
  service: users
  backends:
    - service: users-stable
      weight: 900
    - service: users-canary
      weight: 100
```

### Server Authorization

```yaml
apiVersion: policy.linkerd.io/v1beta2
kind: Server
metadata:
  name: users-api
  namespace: saas-api
spec:
  podSelector:
    matchLabels:
      app: users
  port: http
  proxyProtocol: HTTP/2

---
apiVersion: policy.linkerd.io/v1beta2
kind: ServerAuthorization
metadata:
  name: users-authz
  namespace: saas-api
spec:
  server:
    name: users-api
  client:
    meshTLS:
      serviceAccounts:
        - name: api-gateway
          namespace: saas-api
```

---

## Example 3: Real-time Analytics (Cilium)

### Scenario

- High throughput (50k RPS)
- Low latency critical (<5ms)
- Network policies required
- Kafka-based event streaming
- Kubernetes network policies

### Architecture

```
              ┌─────────────────┐
              │  Cilium Ingress │
              └────────┬────────┘
                       │
              ┌────────┴────────┐
              │   API Servers   │
              │     (Go)        │
              └────────┬────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌───────────────┐            ┌───────────────┐
│    Kafka      │            │    Redis      │
│  (3 brokers)  │            │   (cluster)   │
└───────┬───────┘            └───────────────┘
        │
   ┌────┴────┬────────┐
   │         │        │
   ▼         ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐
│ingest│ │process│ │query │
└──────┘ └──────┘ └──────┘
        │
        ▼
┌───────────────┐
│  ClickHouse   │
└───────────────┘
```

### Installation

```bash
# Install Cilium CLI
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-amd64.tar.gz
tar xzvf cilium-linux-amd64.tar.gz
sudo mv cilium /usr/local/bin/

# Install Cilium with service mesh
cilium install --version 1.16.0 \
  --set kubeProxyReplacement=true \
  --set encryption.enabled=true \
  --set encryption.type=wireguard

# Enable service mesh features
cilium hubble enable --ui

# Verify
cilium status
cilium connectivity test
```

### L7 Network Policy (Kafka-specific)

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: kafka-policy
  namespace: analytics
spec:
  endpointSelector:
    matchLabels:
      app: kafka
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: ingest
      toPorts:
        - ports:
            - port: "9092"
              protocol: TCP
          rules:
            kafka:
              - role: produce
                topic: "events"
    - fromEndpoints:
        - matchLabels:
            app: processor
      toPorts:
        - ports:
            - port: "9092"
              protocol: TCP
          rules:
            kafka:
              - role: consume
                topic: "events"
                clientID: "processor-*"
```

### HTTP L7 Policy

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: api-policy
  namespace: analytics
spec:
  endpointSelector:
    matchLabels:
      app: api
  ingress:
    - fromEntities:
        - world
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
          rules:
            http:
              - method: GET
                path: "/api/v1/.*"
              - method: POST
                path: "/api/v1/events"
                headers:
                  - "Content-Type: application/json"
```

### Transparent Encryption (WireGuard)

```yaml
apiVersion: cilium.io/v2
kind: CiliumClusterWideNetworkPolicy
metadata:
  name: encrypt-all
spec:
  endpointSelector: {}
  nodeSelector:
    matchLabels: {}
  egress:
    - toEntities:
        - cluster
      authentication:
        mode: required
```

### Hubble Observability

```bash
# Enable Hubble
cilium hubble enable

# Port forward UI
cilium hubble ui

# View flows
hubble observe --namespace analytics

# Export to Prometheus
cilium hubble enable --ui \
  --set hubble.relay.prometheus.enabled=true \
  --set hubble.ui.enabled=true
```

---

## Example 4: Hybrid Cloud (Istio Multi-cluster)

### Scenario

- Services across AWS and GCP
- Unified service mesh
- Cross-cluster mTLS
- Centralized observability

### Architecture

```
         ┌─────────────────────────────────────────────┐
         │              Istio Control Plane            │
         │                (Primary - AWS)              │
         └─────────────────────┬───────────────────────┘
                               │
         ┌─────────────────────┴───────────────────────┐
         │                                             │
┌────────┴─────────┐                      ┌────────────┴────────┐
│   AWS EKS        │                      │    GCP GKE          │
│   Cluster        │◀────── mTLS ────────▶│    Cluster          │
│                  │                      │                     │
│ ┌─────────────┐  │                      │  ┌─────────────┐    │
│ │  frontend   │  │                      │  │  backend    │    │
│ │  checkout   │  │                      │  │  inventory  │    │
│ │  payment    │  │                      │  │  shipping   │    │
│ └─────────────┘  │                      │  └─────────────┘    │
└──────────────────┘                      └─────────────────────┘
```

### Primary Cluster (AWS)

```bash
# Install as primary
istioctl install --set profile=default \
  --set values.global.meshID=mesh1 \
  --set values.global.multiCluster.clusterName=aws-cluster \
  --set values.global.network=network1

# Create remote secrets for GCP
istioctl create-remote-secret \
  --name=gcp-cluster \
  --context=gcp-context \
  | kubectl apply -f - --context=aws-context
```

### Remote Cluster (GCP)

```bash
# Get primary's discovery address
DISCOVERY_ADDRESS=$(kubectl --context=aws-context \
  -n istio-system get svc istio-eastwestgateway \
  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Install as remote
istioctl install --set profile=remote \
  --set values.global.meshID=mesh1 \
  --set values.global.multiCluster.clusterName=gcp-cluster \
  --set values.global.network=network2 \
  --set values.global.remotePilotAddress=$DISCOVERY_ADDRESS
```

### Cross-cluster Service Discovery

```yaml
# ServiceEntry for cross-cluster service
apiVersion: networking.istio.io/v1
kind: ServiceEntry
metadata:
  name: inventory-gcp
  namespace: production
spec:
  hosts:
    - inventory.production.svc.cluster.local
  location: MESH_INTERNAL
  ports:
    - number: 80
      name: http
      protocol: HTTP
  resolution: DNS
  endpoints:
    - address: inventory.production.svc.gcp-cluster.local
      network: network2
```

### Locality Load Balancing

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: inventory
  namespace: production
spec:
  host: inventory.production.svc.cluster.local
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
    loadBalancer:
      localityLbSetting:
        enabled: true
        failover:
          - from: us-west-2
            to: us-central1-a
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 30s
      baseEjectionTime: 30s
```

---

## Example 5: Minimal mTLS Only (Istio Ambient)

### Scenario

- Just need encryption (mTLS)
- Minimal overhead critical
- No L7 features needed
- Quick setup

### Installation

```bash
# Install Istio Ambient
istioctl install --set profile=ambient

# Label namespace for ambient
kubectl label namespace production istio.io/dataplane-mode=ambient

# Verify ztunnel running
kubectl get pods -n istio-system -l app=ztunnel
```

### Namespace Configuration

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    istio.io/dataplane-mode: ambient
```

### Optional: Add L7 Features (Waypoint)

```bash
# Deploy waypoint for namespace (only if L7 needed)
istioctl waypoint apply --namespace production

# Or for specific service
istioctl waypoint apply --namespace production --service-account myservice
```

### Waypoint Configuration

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: production-waypoint
  namespace: production
  labels:
    istio.io/waypoint-for: service
spec:
  gatewayClassName: istio-waypoint
  listeners:
    - name: mesh
      port: 15008
      protocol: HBONE
```

---

## Observability Dashboard Examples

### Prometheus Queries

```promql
# Request rate
sum(rate(istio_requests_total{reporter="destination"}[5m])) by (destination_service)

# Error rate
sum(rate(istio_requests_total{reporter="destination",response_code=~"5.*"}[5m])) by (destination_service)
/ sum(rate(istio_requests_total{reporter="destination"}[5m])) by (destination_service)

# P99 latency
histogram_quantile(0.99,
  sum(rate(istio_request_duration_milliseconds_bucket{reporter="destination"}[5m]))
  by (destination_service, le)
)

# mTLS percentage
sum(istio_requests_total{connection_security_policy="mutual_tls"})
/ sum(istio_requests_total)
```

### Grafana Dashboard JSON (Key Panel)

```json
{
  "title": "Service Latency P99",
  "type": "timeseries",
  "targets": [
    {
      "expr": "histogram_quantile(0.99, sum(rate(istio_request_duration_milliseconds_bucket{reporter=\"destination\"}[5m])) by (destination_service, le))",
      "legendFormat": "{{destination_service}}"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "ms",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "green", "value": null},
          {"color": "yellow", "value": 100},
          {"color": "red", "value": 500}
        ]
      }
    }
  }
}
```

---

## Common Patterns Reference

| Pattern | Istio | Linkerd | Cilium |
|---------|-------|---------|--------|
| mTLS | PeerAuthentication | Default on | encryption.enabled |
| Canary | VirtualService | TrafficSplit | N/A (use Flagger) |
| Circuit breaker | DestinationRule | ServiceProfile | N/A |
| Retry | VirtualService | ServiceProfile | N/A |
| Authorization | AuthorizationPolicy | ServerAuthorization | CiliumNetworkPolicy |
| Rate limiting | EnvoyFilter | N/A | CiliumNetworkPolicy |
