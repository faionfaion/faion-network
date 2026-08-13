# Kubernetes Ingress Configuration

## Summary

**One-sentence:** Generates a Kubernetes Ingress / Gateway API config with ≥3-replica controller + PDB + anti-affinity + topology-spread + TLS via cert-manager + per-route annotations.

**One-paragraph:** Kubernetes Ingress requires a controller Deployment with ≥ 3 replicas, a PodDisruptionBudget (`minAvailable: 2`), pod anti-affinity to prevent co-location, topology-spread constraints across AZs, explicit resource requests/limits (TLS and regex are CPU-bound), and per-Ingress annotations for TLS redirect, rate limiting, CORS, body size, and timeouts. Run separate Ingress controllers per traffic class (public / internal / admin) and prefer the Gateway API (`gateway.networking.k8s.io/v1`) over legacy Ingress for new clusters.

**Ефективно для:**

- New Ingress deployment з 3+ replicas + PDB + anti-affinity = "не може впасти за одного pod".
- Annotation-set per controller (nginx.ingress vs haproxy.org vs traefik) — без перемішування.
- TLS via cert-manager + Issuer / ClusterIssuer — no manual cert rotation.
- Separate ingress class per traffic class (public / internal / admin).
- Migration Ingress v1 → Gateway API для traffic splitting + header-based routing.

## Applies If (ALL must hold)

- Deploying a Kubernetes Ingress controller (Nginx, Traefik, HAProxy, Envoy Gateway) and tuning TLS + replicas.
- Migrating legacy Nginx configs to a Gateway API + Envoy stack.
- Setting up separate Ingress controllers per traffic class (public, internal, admin).
- Bare-metal K8s clusters where MetalLB provides the LoadBalancer Service for the Ingress controller.

## Skip If (ANY kills it)

- Managed clouds where the cloud-native LB (ALB Ingress on EKS, GKE Ingress) integrates better.
- Service-mesh routing between internal services — use Istio VirtualService / Linkerd SMI.
- TCP / UDP — Ingress API only handles HTTP(S); use a LoadBalancer Service or HAProxy at L4.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cluster + node count + AZ topology | inventory | infra |
| Traffic classes | list (public/internal/admin) | architecture |
| TLS issuer | cert-manager ClusterIssuer | cert team |
| Controller choice | nginx / haproxy / traefik / envoy | architecture |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lb-nginx-production]] | Underlying Nginx annotation semantics. |
| [[lb-health-checks]] | Backend readiness shape for Ingress probing. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: replicas-min-3, pdb-min-available, anti-affinity-required, topology-spread-azs, annotations-controller-namespaced | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-controller` | sonnet | Decision among nginx / traefik / haproxy / envoy. |
| `emit-controller-manifest` | sonnet | Structured YAML authoring. |
| `lint-annotations` | haiku | Regex audit for controller-namespace mismatch. |

## Templates

| File | Purpose |
|------|---------|
| `templates/controller-deployment.yaml` | Ingress-nginx Deployment + Service + PDB + ServiceAccount |
| `templates/ingress.yaml` | Per-app Ingress with cert-manager + rate-limit + CORS annotations |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lb-kubernetes-ingress.py` | Validate the Ingress artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[lb-nginx-production]]
- [[lb-haproxy-production]]
- [[lb-health-checks]]
- [[lb-high-availability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (managed vs self-hosted, traffic class, Gateway API readiness, controller choice) to a concrete config shape, each leaf referencing a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/controller-deployment.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata: { name: ingress-nginx }
---
apiVersion: v1
kind: ServiceAccount
metadata: { name: ingress-nginx, namespace: ingress-nginx }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: ingress-nginx-controller, namespace: ingress-nginx }
spec:
  replicas: 3
  selector:
    matchLabels: { app.kubernetes.io/name: ingress-nginx }
  template:
    metadata:
      labels: { app.kubernetes.io/name: ingress-nginx }
    spec:
      serviceAccountName: ingress-nginx
      terminationGracePeriodSeconds: 300

      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels: { app.kubernetes.io/name: ingress-nginx }
              topologyKey: kubernetes.io/hostname

      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels: { app.kubernetes.io/name: ingress-nginx }

      containers:
        - name: controller
          image: registry.k8s.io/ingress-nginx/controller:v1.10.0
          args:
            - /nginx-ingress-controller
            - --ingress-class=public
            - --publish-service=ingress-nginx/ingress-nginx
          resources:
            requests: { cpu: "200m", memory: "256Mi" }
            limits:   { cpu: "1",    memory: "512Mi" }
          ports:
            - { name: http,    containerPort: 80,  protocol: TCP }
            - { name: https,   containerPort: 443, protocol: TCP }
            - { name: metrics, containerPort: 10254 }
          livenessProbe:
            httpGet: { path: /healthz, port: 10254 }
            periodSeconds: 10
            failureThreshold: 5
          readinessProbe:
            httpGet: { path: /healthz, port: 10254 }
            periodSeconds: 10
            failureThreshold: 3
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: { name: ingress-nginx-pdb, namespace: ingress-nginx }
spec:
  minAvailable: 2
  selector:
    matchLabels: { app.kubernetes.io/name: ingress-nginx }
---
apiVersion: v1
kind: Service
metadata: { name: ingress-nginx, namespace: ingress-nginx }
spec:
  type: LoadBalancer
  selector: { app.kubernetes.io/name: ingress-nginx }
  ports:
    - { name: http,  port: 80,  targetPort: http }
    - { name: https, port: 443, targetPort: https }
---
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: public
spec:
  controller: k8s.io/ingress-nginx
```

### `templates/ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web
  namespace: prod
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "8m"
    nginx.ingress.kubernetes.io/limit-rpm: "600"
    nginx.ingress.kubernetes.io/limit-connections: "30"
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://app.example.com"
    nginx.ingress.kubernetes.io/cors-allow-methods: "GET,POST,PUT,DELETE,OPTIONS"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "5"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "60"
spec:
  ingressClassName: public
  tls:
    - hosts: [app.example.com]
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port:
                  number: 80
```
