# Agent Integration — Service Mesh

## When to use
- Selecting Istio vs Linkerd vs Cilium vs Istio Ambient against documented constraints.
- Generating `VirtualService` / `DestinationRule` / `HTTPRoute` for canary, mirror, or A/B traffic.
- Authoring `PeerAuthentication` + `AuthorizationPolicy` to roll out strict mTLS namespace by namespace.
- Reviewing PRs that change retry, timeout, or circuit-breaker config (frequent foot-gun).
- Migrating from sidecar Istio → Ambient mode.
- Wiring Prometheus + Grafana + Kiali / Linkerd-viz dashboards from mesh metrics.

## When NOT to use
- Clusters with <5 services or low-trust requirements — `cert-manager` + manual TLS is cheaper.
- Latency-critical paths where the mesh budget (1-5ms per hop) is unacceptable.
- Teams that don't yet operate Kubernetes well — mesh failures are hard to debug.
- Single-language stacks where in-process resilience libs (Resilience4j, Polly) cover the same needs.
- Resource-constrained edge clusters — sidecar memory dominates pod footprint.

## Where it fails / limitations
- Agents reflexively pick Istio without comparing Ambient or Linkerd; reject "best mesh" answers without trade-off table.
- mTLS modes (`PERMISSIVE` vs `STRICT`) often confused; agent flips strict too early and breaks ingress-egress edges.
- `AuthorizationPolicy` defaults are deny-by-config but allow-by-namespace — easy to misconfigure.
- Retry policies stack: app retry × Envoy retry × HTTPRoute retry → request amplification.
- Mesh tracing not propagated unless app forwards `b3` / `traceparent` headers — agent often forgets.
- Multi-cluster setups need east-west gateways + trust bundle exchange that agents oversimplify.

## Agentic workflow
Run a mesh-architect to choose the mesh and mode (sidecar/ambient/eBPF) with a written trade-off, then a coder to emit Istio/Linkerd CRDs from a traffic-policy spec, then a reviewer that runs `istioctl analyze` / `linkerd check` and verifies mTLS strict, no permissive PeerAuthentication, retry budgets capped, and AuthorizationPolicies default-deny. Architect on Opus; coder/reviewer on Sonnet.

### Recommended subagents
- `mesh-architect` (Opus) — mesh selection (Istio/Linkerd/Cilium/Ambient), data-plane decision.
- `traffic-policy-coder` (Sonnet) — VirtualService/DestinationRule/HTTPRoute, canary/blue-green configs.
- `mtls-rollout-planner` (Sonnet) — strict-mTLS migration plan, namespace ordering.
- `mesh-reviewer` (Sonnet) — runs `istioctl analyze`, audits AuthorizationPolicy and retry stacking.

### Prompt pattern
```
You are mesh-architect. Cluster: 60 services, 3 clusters, latency budget +2ms,
goals=[mTLS, canary, multi-cluster]. Output:
1) mesh + mode pick + 2 alternatives rejected with reasons,
2) data-plane CPU/memory budget per pod,
3) gateway topology,
4) observability stack,
5) phased rollout (mTLS PERMISSIVE → STRICT) per namespace.
```

```
You are mesh-reviewer. Diff: <patch>. Reject if:
- any PeerAuthentication stays PERMISSIVE in prod namespace > 30 days,
- AuthorizationPolicy missing or `action: ALLOW` without `from.principals`,
- retry budget unbounded (no `numRetries` + `retryBudget`),
- DestinationRule TLS mode != ISTIO_MUTUAL when mesh mTLS is on,
- timeout omitted or > 30s on user-facing routes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `istioctl` | Install, analyze, debug Istio | istio.io/latest/docs/reference/commands/istioctl/ |
| `linkerd` | Install/check/profile, viz | linkerd.io/2/cli/ |
| `cilium` | Install + Hubble (eBPF observability) | docs.cilium.io |
| `consul` | Connect intentions, mesh CLI | consul.io |
| `kubectl-tap` (Linkerd) | Live request introspection | linkerd.io |
| `meshery` | Multi-mesh management | meshery.io |
| `gwctl` | Gateway API resource inspection | gateway-api.sigs.k8s.io |
| `kiali` (web) | Istio service graph + policy | kiali.io |
| `kubectl-istio-debug` | Envoy config dump helpers | istio.io |
| `step-cli` / `cmctl` | Cert lifecycle for mesh roots | smallstep.com / cert-manager.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Istio (sidecar + Ambient) | OSS | Yes | CRDs are well-documented; agent can emit reliably with version pin. |
| Linkerd | OSS + Buoyant Cloud SaaS | Yes | Smaller surface; great default. |
| Cilium Service Mesh | OSS + Isovalent Enterprise | Yes | eBPF; configs simpler but L7 features fewer. |
| Consul Connect | OSS + HCP SaaS | Partial | Intentions DSL; agent OK but verify with `consul intention check`. |
| AWS App Mesh | SaaS | Partial | Going EOL — avoid for new work. |
| Tetrate Service Bridge | SaaS | Partial | Enterprise Istio control plane. |
| Solo.io Gloo Mesh | SaaS + OSS | Partial | Multi-cluster Istio; complex. |
| Flagger | OSS | Yes | Mesh-aware progressive delivery — pairs with Istio/Linkerd. |
| SPIRE / SPIFFE | OSS | Yes | Identity for multi-cluster trust; agent generates registration entries. |

## Templates & scripts
See `templates.md` for canary, mirror, mTLS, and AuthorizationPolicy templates. Inline mesh-rollout safety checks the agent should always emit:

```yaml
# istio-strict-mtls-rollout.yaml — namespace by namespace
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata: {name: default, namespace: ${NS}}
spec:
  mtls: {mode: PERMISSIVE}   # phase 1
---
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata: {name: default, namespace: ${NS}}
spec:
  mtls: {mode: STRICT}       # phase 2 after dashboards green for 7d
---
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: {name: default-deny, namespace: ${NS}}
spec: {}                     # default deny — required pair with STRICT
```

```bash
# mesh-validate.sh
istioctl analyze -n "$NS"
istioctl proxy-status
linkerd check 2>/dev/null || true
kubectl get peerauthentication -A -o jsonpath='{.items[?(@.spec.mtls.mode=="PERMISSIVE")].metadata.name}'
```

## Best practices
- Always emit a roll-back manifest paired with any mTLS change; `kubectl apply -f rollback.yaml` should be a single command.
- Stagger STRICT mTLS by namespace (least-critical first) and keep PERMISSIVE 3-7 days for traffic confirmation via Kiali.
- Enforce default-deny `AuthorizationPolicy` in every namespace when mTLS is STRICT — otherwise mesh is open.
- Cap retry budgets at the gateway (Envoy `retryBudget`) AND per-route (`numRetries`); without budget, retries amplify failures.
- Pair `outlierDetection` with circuit breakers in DestinationRule; one without the other is incomplete.
- Use Istio Ambient + waypoint for "mTLS only, occasional L7" workloads — saves 80% memory.
- Don't run mesh on the control-plane node pool; isolate via taints.
- Always emit observability bindings (PromRule, Grafana dashboard, Kiali health) with policy changes.

## AI-agent gotchas
- Agents conflate `VirtualService` (routing) with `DestinationRule` (subsets, TLS, LB) — they're a pair, not interchangeable.
- Linkerd's traffic-shifting uses `TrafficSplit` (SMI) or new HTTPRoute; agent often emits old SMI on new clusters.
- AuthorizationPolicy `from.principals` requires SPIFFE IDs (`cluster.local/ns/.../sa/...`) not plain SA names.
- Ambient mode waypoint deployments must match service-account scope; agents miss this and policies silently no-op.
- Human checkpoint REQUIRED before: switching PERMISSIVE→STRICT in any prod namespace, deploying egress gateway, changing root CA, enabling multi-cluster east-west.
- Mesh metrics double-counting when both app and Envoy emit RED metrics — disable app-side or label.
- `holdApplicationUntilProxyStarts` not set → init traffic loss during rolling updates.
- Agent picks `randomSampling: 100%` for tracing in prod and OOMs collectors.

## References
- Istio docs: https://istio.io/latest/docs/.
- Linkerd docs: https://linkerd.io/2/.
- Cilium service mesh: https://docs.cilium.io/en/stable/network/servicemesh/.
- Gateway API: https://gateway-api.sigs.k8s.io/.
- "Istio in Action", Christian Posta & Rinor Maloku.
- Tetrate mTLS best practices: https://tetrate.io/blog/mtls-best-practices-for-kubernetes.
- SPIFFE/SPIRE: https://spiffe.io/.
- 2024 mesh perf benchmark: https://arxiv.org/html/2411.02267v1.
