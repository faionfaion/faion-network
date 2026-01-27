# Service Mesh Templates

Copy-paste configurations for common service mesh setups.

## Table of Contents

1. [Istio Templates](#istio-templates)
2. [Linkerd Templates](#linkerd-templates)
3. [Cilium Templates](#cilium-templates)
4. [Observability Templates](#observability-templates)
5. [Flagger (Progressive Delivery)](#flagger-templates)

---

## Istio Templates

### Installation Profile (Production)

```yaml
# istio-operator.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: production
  namespace: istio-system
spec:
  profile: default

  meshConfig:
    accessLogFile: /dev/stdout
    accessLogFormat: |
      {"timestamp":"%START_TIME%","method":"%REQ(:METHOD)%","path":"%REQ(X-ENVOY-ORIGINAL-PATH?:PATH)%","protocol":"%PROTOCOL%","response_code":"%RESPONSE_CODE%","response_flags":"%RESPONSE_FLAGS%","bytes_sent":"%BYTES_SENT%","bytes_received":"%BYTES_RECEIVED%","duration":"%DURATION%","upstream_service_time":"%RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)%","x_forwarded_for":"%REQ(X-FORWARDED-FOR)%","user_agent":"%REQ(USER-AGENT)%","request_id":"%REQ(X-REQUEST-ID)%","authority":"%REQ(:AUTHORITY)%","upstream_host":"%UPSTREAM_HOST%","upstream_cluster":"%UPSTREAM_CLUSTER%","upstream_local_address":"%UPSTREAM_LOCAL_ADDRESS%","downstream_local_address":"%DOWNSTREAM_LOCAL_ADDRESS%","downstream_remote_address":"%DOWNSTREAM_REMOTE_ADDRESS%","route_name":"%ROUTE_NAME%","connection_termination_details":"%CONNECTION_TERMINATION_DETAILS%"}
    defaultConfig:
      tracing:
        sampling: 10  # 10% sampling for production
      proxyMetadata:
        ISTIO_META_DNS_AUTO_ALLOCATE: "true"
        ISTIO_META_DNS_CAPTURE: "true"

    # Enable locality load balancing
    localityLbSetting:
      enabled: true

    # Outbound traffic policy
    outboundTrafficPolicy:
      mode: REGISTRY_ONLY  # Strict mode

  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 500m
            memory: 2Gi
          limits:
            cpu: 1000m
            memory: 4Gi
        hpaSpec:
          minReplicas: 2
          maxReplicas: 5

    ingressGateways:
      - name: istio-ingressgateway
        enabled: true
        k8s:
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
          hpaSpec:
            minReplicas: 2
            maxReplicas: 10
          service:
            type: LoadBalancer
            ports:
              - port: 80
                targetPort: 8080
                name: http2
              - port: 443
                targetPort: 8443
                name: https

  values:
    global:
      proxy:
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 256Mi
```

### Ambient Mode Installation

```yaml
# istio-ambient.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: ambient
  namespace: istio-system
spec:
  profile: ambient

  components:
    ztunnel:
      enabled: true
      k8s:
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
```

### Gateway (Gateway API)

```yaml
# gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: main-gateway
  namespace: istio-system
spec:
  gatewayClassName: istio
  listeners:
    - name: http
      port: 80
      protocol: HTTP
      allowedRoutes:
        namespaces:
          from: All
    - name: https
      port: 443
      protocol: HTTPS
      tls:
        mode: Terminate
        certificateRefs:
          - name: wildcard-tls
            kind: Secret
      allowedRoutes:
        namespaces:
          from: All
```

### HTTPRoute

```yaml
# httproute.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-route
  namespace: production
spec:
  parentRefs:
    - name: main-gateway
      namespace: istio-system
  hostnames:
    - "api.example.com"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /v1
      backendRefs:
        - name: api-v1
          port: 80
          weight: 100
    - matches:
        - path:
            type: PathPrefix
            value: /v2
      backendRefs:
        - name: api-v2
          port: 80
          weight: 100
```

### VirtualService (Traffic Splitting)

```yaml
# virtualservice-canary.yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: myservice
  namespace: production
spec:
  hosts:
    - myservice
  http:
    - match:
        - headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: myservice
            subset: canary
    - route:
        - destination:
            host: myservice
            subset: stable
          weight: 95
        - destination:
            host: myservice
            subset: canary
          weight: 5

---
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: myservice
  namespace: production
spec:
  host: myservice
  subsets:
    - name: stable
      labels:
        version: v1
    - name: canary
      labels:
        version: v2
```

### mTLS Configuration

```yaml
# mtls-strict.yaml
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
# Namespace-specific permissive (for migration)
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: legacy
spec:
  mtls:
    mode: PERMISSIVE
```

### Authorization Policy (Default Deny)

```yaml
# authz-default-deny.yaml
# Deny all by default
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  {}

---
# Allow specific service-to-service
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/production/sa/frontend"]
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/*"]
```

### Circuit Breaker

```yaml
# circuit-breaker.yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: myservice
  namespace: production
spec:
  host: myservice
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
        maxRequestsPerConnection: 100
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 60s
      maxEjectionPercent: 50
      minHealthPercent: 30
```

### Retry Policy

```yaml
# retry-policy.yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: myservice
  namespace: production
spec:
  hosts:
    - myservice
  http:
    - route:
        - destination:
            host: myservice
      retries:
        attempts: 3
        perTryTimeout: 2s
        retryOn: connect-failure,refused-stream,unavailable,cancelled,retriable-status-codes
        retriableStatusCodes:
          - 503
          - 504
      timeout: 10s
```

### Rate Limiting

```yaml
# rate-limit.yaml
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
              name: envoy.filters.network.http_connection_manager
              subFilter:
                name: envoy.filters.http.router
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.local_ratelimit
          typed_config:
            "@type": type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
            stat_prefix: http_local_rate_limiter
            token_bucket:
              max_tokens: 1000
              tokens_per_fill: 100
              fill_interval: 1s
            filter_enabled:
              runtime_key: local_rate_limit_enabled
              default_value:
                numerator: 100
                denominator: HUNDRED
            filter_enforced:
              runtime_key: local_rate_limit_enforced
              default_value:
                numerator: 100
                denominator: HUNDRED
```

---

## Linkerd Templates

### Installation Script

```bash
#!/bin/bash
# install-linkerd.sh

# Generate certificates (production)
step certificate create root.linkerd.cluster.local ca.crt ca.key \
  --profile root-ca --no-password --insecure --not-after 87600h

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

### Namespace with Injection

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  annotations:
    linkerd.io/inject: enabled
    config.linkerd.io/proxy-cpu-request: "25m"
    config.linkerd.io/proxy-memory-request: "64Mi"
    config.linkerd.io/proxy-cpu-limit: "500m"
    config.linkerd.io/proxy-memory-limit: "256Mi"
```

### Service Profile

```yaml
# service-profile.yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: api.production.svc.cluster.local
  namespace: production
spec:
  routes:
    - name: GET /health
      condition:
        method: GET
        pathRegex: /health
      isRetryable: true
      timeout: 1s

    - name: GET /api/users/{id}
      condition:
        method: GET
        pathRegex: /api/users/[^/]+
      isRetryable: true
      timeout: 5s
      retryBudget:
        retryRatio: 0.2
        minRetriesPerSecond: 10
        ttl: 10s

    - name: POST /api/users
      condition:
        method: POST
        pathRegex: /api/users
      isRetryable: false  # POST not idempotent
      timeout: 10s

    - name: DELETE /api/users/{id}
      condition:
        method: DELETE
        pathRegex: /api/users/[^/]+
      isRetryable: false
      timeout: 5s
```

### Traffic Split (Canary)

```yaml
# traffic-split.yaml
apiVersion: split.smi-spec.io/v1alpha1
kind: TrafficSplit
metadata:
  name: api-canary
  namespace: production
spec:
  service: api
  backends:
    - service: api-stable
      weight: 900
    - service: api-canary
      weight: 100
```

### Server Authorization

```yaml
# server-authorization.yaml
apiVersion: policy.linkerd.io/v1beta2
kind: Server
metadata:
  name: api-server
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  port: http
  proxyProtocol: HTTP/2

---
apiVersion: policy.linkerd.io/v1beta2
kind: ServerAuthorization
metadata:
  name: api-authorization
  namespace: production
spec:
  server:
    name: api-server
  client:
    meshTLS:
      serviceAccounts:
        - name: frontend
          namespace: production
        - name: mobile-gateway
          namespace: production
```

### HTTPRoute (Gateway API)

```yaml
# httproute-linkerd.yaml
apiVersion: policy.linkerd.io/v1beta2
kind: HTTPRoute
metadata:
  name: api-route
  namespace: production
spec:
  parentRefs:
    - name: api-server
      kind: Server
      group: policy.linkerd.io
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api
      backendRefs:
        - name: api
          port: 80
      timeouts:
        request: 10s
```

---

## Cilium Templates

### Installation

```bash
#!/bin/bash
# install-cilium.sh

# Install with service mesh and encryption
cilium install --version 1.16.0 \
  --set kubeProxyReplacement=true \
  --set k8sServiceHost=${API_SERVER_IP} \
  --set k8sServicePort=${API_SERVER_PORT} \
  --set encryption.enabled=true \
  --set encryption.type=wireguard \
  --set hubble.relay.enabled=true \
  --set hubble.ui.enabled=true \
  --set hubble.metrics.enabled="{dns,drop,tcp,flow,icmp,http}"

# Wait for cilium to be ready
cilium status --wait

# Test connectivity
cilium connectivity test
```

### CiliumNetworkPolicy (L3/L4)

```yaml
# network-policy-l4.yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: backend-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
        - matchLabels:
            app: api-gateway
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
  egress:
    - toEndpoints:
        - matchLabels:
            app: database
      toPorts:
        - ports:
            - port: "5432"
              protocol: TCP
    - toEndpoints:
        - matchLabels:
            app: cache
      toPorts:
        - ports:
            - port: "6379"
              protocol: TCP
```

### CiliumNetworkPolicy (L7 HTTP)

```yaml
# network-policy-l7.yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: api-l7-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: api
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
          rules:
            http:
              - method: GET
                path: "/api/v1/.*"
              - method: POST
                path: "/api/v1/users"
              - method: PUT
                path: "/api/v1/users/[0-9]+"
              - method: DELETE
                path: "/api/v1/users/[0-9]+"
```

### CiliumNetworkPolicy (Kafka)

```yaml
# kafka-policy.yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: kafka-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: kafka
  ingress:
    - fromEndpoints:
        - matchLabels:
            role: producer
      toPorts:
        - ports:
            - port: "9092"
              protocol: TCP
          rules:
            kafka:
              - role: produce
                topic: "events"
              - role: produce
                topic: "logs"
    - fromEndpoints:
        - matchLabels:
            role: consumer
      toPorts:
        - ports:
            - port: "9092"
              protocol: TCP
          rules:
            kafka:
              - role: consume
                topic: "events"
                clientID: "consumer-*"
```

### Cluster-wide Encryption

```yaml
# encryption-policy.yaml
apiVersion: cilium.io/v2
kind: CiliumClusterWideNetworkPolicy
metadata:
  name: encrypt-all-traffic
spec:
  endpointSelector: {}
  egress:
    - toEntities:
        - cluster
      authentication:
        mode: required
```

### Ingress (Gateway API)

```yaml
# cilium-gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: cilium
spec:
  controllerName: io.cilium/gateway-controller

---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: main-gateway
  namespace: production
spec:
  gatewayClassName: cilium
  listeners:
    - name: http
      port: 80
      protocol: HTTP
    - name: https
      port: 443
      protocol: HTTPS
      tls:
        mode: Terminate
        certificateRefs:
          - name: tls-secret
```

---

## Observability Templates

### Prometheus ServiceMonitor

```yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: istio-mesh
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: istiod
  namespaceSelector:
    matchNames:
      - istio-system
  endpoints:
    - port: http-monitoring
      interval: 15s
      path: /metrics

---
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: envoy-stats
  namespace: monitoring
spec:
  selector:
    matchLabels:
      security.istio.io/tlsMode: istio
  namespaceSelector:
    any: true
  podMetricsEndpoints:
    - port: http-envoy-prom
      path: /stats/prometheus
      interval: 30s
```

### Grafana Dashboard ConfigMap

```yaml
# grafana-dashboard.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: service-mesh-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  service-mesh.json: |
    {
      "dashboard": {
        "title": "Service Mesh Overview",
        "panels": [
          {
            "title": "Request Rate",
            "type": "timeseries",
            "targets": [
              {
                "expr": "sum(rate(istio_requests_total{reporter=\"destination\"}[5m])) by (destination_service)",
                "legendFormat": "{{destination_service}}"
              }
            ]
          },
          {
            "title": "Error Rate",
            "type": "timeseries",
            "targets": [
              {
                "expr": "sum(rate(istio_requests_total{reporter=\"destination\",response_code=~\"5.*\"}[5m])) by (destination_service) / sum(rate(istio_requests_total{reporter=\"destination\"}[5m])) by (destination_service)",
                "legendFormat": "{{destination_service}}"
              }
            ]
          },
          {
            "title": "P99 Latency",
            "type": "timeseries",
            "targets": [
              {
                "expr": "histogram_quantile(0.99, sum(rate(istio_request_duration_milliseconds_bucket{reporter=\"destination\"}[5m])) by (destination_service, le))",
                "legendFormat": "{{destination_service}}"
              }
            ]
          }
        ]
      }
    }
```

### Alerting Rules

```yaml
# alerting-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: service-mesh-alerts
  namespace: monitoring
spec:
  groups:
    - name: service-mesh
      rules:
        - alert: HighErrorRate
          expr: |
            sum(rate(istio_requests_total{response_code=~"5.*"}[5m])) by (destination_service)
            / sum(rate(istio_requests_total[5m])) by (destination_service)
            > 0.05
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "High error rate for {{ $labels.destination_service }}"
            description: "Error rate is {{ $value | humanizePercentage }}"

        - alert: HighLatency
          expr: |
            histogram_quantile(0.99,
              sum(rate(istio_request_duration_milliseconds_bucket{reporter="destination"}[5m]))
              by (destination_service, le)
            ) > 500
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High latency for {{ $labels.destination_service }}"
            description: "P99 latency is {{ $value }}ms"

        - alert: ServiceMeshCertificateExpiry
          expr: |
            (certmanager_certificate_expiration_timestamp_seconds - time()) / 86400 < 7
          for: 1h
          labels:
            severity: warning
          annotations:
            summary: "Certificate expiring soon"
            description: "Certificate {{ $labels.name }} expires in {{ $value | humanizeDuration }}"
```

### Jaeger Configuration

```yaml
# jaeger.yaml
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: jaeger
  namespace: observability
spec:
  strategy: production
  storage:
    type: elasticsearch
    options:
      es:
        server-urls: http://elasticsearch:9200
  collector:
    maxReplicas: 5
    resources:
      limits:
        cpu: 1
        memory: 1Gi
  query:
    replicas: 2
```

---

## Flagger Templates

### Canary with Istio

```yaml
# flagger-canary.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: api
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api

  progressDeadlineSeconds: 600

  service:
    port: 80
    targetPort: 8080
    gateways:
      - main-gateway.istio-system.svc.cluster.local
    hosts:
      - api.example.com

  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10

    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 1m

    webhooks:
      - name: load-test
        url: http://flagger-loadtester.production/
        timeout: 5s
        metadata:
          cmd: "hey -z 1m -q 10 -c 2 http://api-canary.production:8080/"
```

### Blue-Green with Linkerd

```yaml
# flagger-bluegreen.yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: api
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api

  progressDeadlineSeconds: 600

  service:
    port: 80
    targetPort: 8080

  analysis:
    interval: 1m
    threshold: 2
    iterations: 10

    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m

    webhooks:
      - name: acceptance-test
        type: pre-rollout
        url: http://flagger-loadtester.production/
        timeout: 30s
        metadata:
          type: bash
          cmd: "curl -s http://api-canary.production/health | grep ok"

      - name: load-test
        type: rollout
        url: http://flagger-loadtester.production/
        timeout: 5s
        metadata:
          cmd: "hey -z 2m -q 10 -c 2 http://api-canary.production/"
```

---

## Quick Reference

### Namespace Labels

| Mesh | Label | Value |
|------|-------|-------|
| Istio | `istio-injection` | `enabled` |
| Istio Ambient | `istio.io/dataplane-mode` | `ambient` |
| Linkerd | `linkerd.io/inject` | `enabled` |
| Cilium | `cilium.io/service-mesh` | `enabled` |

### Debugging Commands

```bash
# Istio
istioctl analyze
istioctl proxy-status
istioctl proxy-config all <pod>

# Linkerd
linkerd check
linkerd viz tap deployment/<name>
linkerd viz stat deployment

# Cilium
cilium status
cilium connectivity test
hubble observe --namespace <ns>
```
