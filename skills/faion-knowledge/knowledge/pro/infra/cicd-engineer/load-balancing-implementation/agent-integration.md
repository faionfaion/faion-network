# Agent Integration — Load Balancing Implementation

## When to use
- Standing up production HAProxy or NGINX in front of a service fleet, on bare metal, VMs, or Kubernetes.
- Picking and configuring an AWS ALB/NLB, GCP Load Balancer, or Azure Front Door / Application Gateway.
- Deploying a Kubernetes Ingress controller (NGINX-Ingress, Traefik, HAProxy Ingress, Envoy Gateway) and tuning health checks, TLS, and replicas.
- Migrating legacy NGINX configs to a Gateway API + envoy-based stack.
- Hardening LB security: TLS 1.2+/1.3, cipher policy, rate limiting, WAF wiring.

## When NOT to use
- Internal service-to-service mesh routing — use a service mesh (Linkerd, Istio, Cilium) skill instead.
- Static-site CDN — use CloudFront/Cloudflare/Fastly directly.
- Single-instance dev workloads — `nginx -t` and `docker run -p` are enough.
- Database load balancing (PgBouncer, ProxySQL, Vitess) — use database-specific patterns, generic LB rules don't fit.
- Replacing a managed cloud LB with self-hosted just to save money before you've outgrown it.

## Where it fails / limitations
- Health check tuning is the #1 footgun: too aggressive thresholds flap services in/out; too lax keeps dead backends in rotation. Tune per service, not globally.
- HAProxy + dynamic backends (K8s endpoints) requires `dataplaneapi`, `runtime API`, or Ingress controller — static config files churn on every pod restart.
- TLS termination at LB removes end-to-end encryption; for PCI/regulated traffic require re-encryption to backend.
- Sticky sessions break autoscaling — agents implementing sticky sessions on stateless services usually mask a real architectural smell.
- Cloud LB quotas: AWS ALB target groups, GCP backend services per LB — agents at scale hit limits silently.
- Path-based routing collisions: NGINX `location` precedence rules vs Ingress path types (Exact/Prefix/ImplementationSpecific) is a frequent silent bug.

## Agentic workflow
Drive LB work through IaC + config templates, not direct edits to running boxes. Workflow: agent renders config from a structured input (backends, paths, TLS source, rate limits), validates with `nginx -t` / `haproxy -c -f` / `ingress-nginx-validate`, runs a synthetic health-check matrix in a staging environment, opens a PR. Cluster-side: prefer Ingress controller + Gateway API CRDs over hand-edited configs. Never `kubectl edit ingress` from the agent — only via Git.

### Recommended subagents
- `faion-sdd-executor-agent` — implement Ingress / config changes with quality gates.
- Custom `lb-config-renderer` — input JSON of services + paths + TLS, output validated NGINX/HAProxy/Ingress YAML.
- Custom `lb-health-validator` — synthetic probe runner; verifies new backends accept traffic before swapping.

### Prompt pattern
"You are an NGINX Ingress author. Input services list `[{name, host, paths, port, tls_secret}]`. Output a single `Ingress` manifest, `pathType: Prefix`, with annotations `nginx.ingress.kubernetes.io/proxy-body-size: 10m`, HSTS, and rate-limit `100r/s` per host. Reject input if any host appears twice. Return YAML only."

"You are an HAProxy config reviewer. Given a `haproxy.cfg` diff, flag: (1) missing `option httpchk`, (2) `balance source` on stateless backends, (3) `timeout client/server` < 30s for HTTP/2, (4) cipher list including any of `RC4|3DES|MD5`. Return JSON `{ok:bool, issues:[{line,severity,message,fix}]}`."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `haproxy -c -f` | Validate HAProxy config | https://www.haproxy.org/ |
| `nginx -t` / `nginx -T` | Validate NGINX, dump effective config | https://nginx.org/en/docs/ |
| `kubectl ingress-nginx` plugin | Diagnose NGINX Ingress | https://kubernetes.github.io/ingress-nginx/kubectl-plugin/ |
| `traefikctl` (`traefik` binary) | Traefik validation/info | https://doc.traefik.io/traefik/ |
| `envoy --mode validate` | Validate Envoy config | https://www.envoyproxy.io/docs/envoy/latest/start/start |
| `awscli` `elbv2` / `gcloud compute backend-services` | Cloud LB ops | AWS / GCP docs |
| `mkcert` / `cfssl` | Local certs for testing | https://github.com/FiloSottile/mkcert |
| `vegeta` / `wrk2` / `oha` | Load testing through the LB | https://github.com/tsenart/vegeta |
| `httpx` (ProjectDiscovery) | Probing TLS, headers, redirects | https://github.com/projectdiscovery/httpx |
| `testssl.sh` | TLS endpoint hardening test | https://testssl.sh/ |
| `keepalived` / `ucarp` | VIP failover for active/passive HA | https://www.keepalived.org/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| HAProxy / HAProxy Enterprise | OSS / SaaS | Yes — Data Plane API + Runtime API | Best raw L4 perf; `dataplaneapi` for dynamic config |
| NGINX / NGINX Plus | OSS / SaaS | Yes — Plus REST API | Reverse proxy + L7; cache built-in |
| Envoy / Envoy Gateway | OSS | Yes — xDS API | Dynamic config, native to mesh |
| Traefik | OSS | Yes — file/CRD providers | Auto TLS via ACME, dynamic |
| Caddy | OSS | Yes — JSON API | Easiest TLS automation |
| AWS ALB / NLB / GLB | SaaS | Yes — Terraform/CDK | ALB L7, NLB L4, GLB for appliances |
| GCP Cloud Load Balancing | SaaS | Yes | Global anycast L7, regional L4 |
| Azure Front Door / App Gateway | SaaS | Yes | Front Door global, App Gateway regional |
| Cloudflare LB / Spectrum | SaaS | Yes — API | Global, integrated WAF |
| F5 BIG-IP / NGINX Plus | Enterprise | Partial — iControl REST | Heavy enterprise, slower iteration |
| MetalLB | OSS | Yes — CRDs | Bare-metal K8s LoadBalancer Service |
| Kong / Tyk / APISIX | OSS/SaaS | Yes — admin API | Combined gateway + LB |

## Templates & scripts
See `templates.md` for HAProxy/NGINX/Ingress templates. Inline staged-rollout pre-flight:

```bash
#!/usr/bin/env bash
# lb-preflight.sh — validate config + smoke-test new backends before swap
set -euo pipefail
CFG=${1:?config path}
HOST=${2:?https host to probe}

case "$CFG" in
  *.cfg) haproxy -c -f "$CFG" ;;
  *.conf|*nginx*) nginx -t -c "$CFG" ;;
  *.yaml|*.yml) kubeconform -strict -summary "$CFG" ;;
  *) echo "unknown config type"; exit 2 ;;
esac

testssl.sh --quiet --color 0 --severity HIGH "$HOST" || { echo "TLS hardening failed"; exit 3; }
oha -n 200 -c 10 -t 30s --no-tui "https://$HOST/healthz" | tee /tmp/oha.txt
grep -E "Success rate.*100\\.00%" /tmp/oha.txt || { echo "healthz failures"; exit 4; }
echo "preflight OK"
```

## Best practices
- One Ingress controller per traffic class (public, internal, admin) — separate Pods, separate ingress class.
- Pod anti-affinity + topology-spread-constraints for the controller; never colocate replicas on one node.
- Pod Disruption Budgets so a node drain doesn't kill all LB pods at once.
- Tune health checks per service: HTTP `/healthz` returning 200 only when ready; readiness != liveness.
- Connection draining / `preStop` lifecycle hook to let in-flight requests complete on rollout.
- Set explicit `resources.requests/limits` on Ingress controller; TLS + regex are CPU-bound, easy to underprovision.
- Rate-limit at the edge (LB), not just in the app — cheap and absorbs floods.
- Always TLS 1.2 minimum, prefer TLS 1.3; use Mozilla SSL Configurator's `intermediate` profile.
- Centralize logs (LB access logs to ELK/Loki) — audit trail and debug gold.
- For bare-metal K8s: HAProxy + keepalived as L4 → MetalLB → NGINX Ingress is the canonical stack.

## AI-agent gotchas
- LLMs love to suggest `worker_connections 100000` blindly; verify against `ulimit -n` and kernel `nofile` first.
- HAProxy `balance` algorithm choice — agents pick `source` for "stickiness" but conflate that with proper session affinity; clarify intent.
- NGINX `location` ordering: agents emit overlapping prefixes; require disjoint or use `=`/`^~` modifiers.
- Ingress annotation drift: `nginx.ingress.kubernetes.io/...` vs `traefik.ingress.kubernetes.io/...`; LLMs mix them. Pin the controller in the prompt.
- TLS cipher copy-paste: 2018 cipher lists still circulate; force the Mozilla SSL Configurator output for current year/profile.
- Health endpoint in app: agents wire `/healthz` but the app returns 200 even when DB is down — push for "deep" health checks via dependency probe.
- HTTP/2 + sticky cookie: NGINX has subtle interactions; verify with `curl --http2 -v`.
- WAF rules generated by LLM frequently false-positive on legit traffic; deploy in `DetectionOnly` first.

## References
- HAProxy docs: https://docs.haproxy.org/
- NGINX docs: https://nginx.org/en/docs/
- NGINX Ingress: https://kubernetes.github.io/ingress-nginx/
- Envoy Gateway: https://gateway.envoyproxy.io/
- Gateway API: https://gateway-api.sigs.k8s.io/
- Mozilla SSL Configuration Generator: https://ssl-config.mozilla.org/
- MetalLB: https://metallb.universe.tf/
- testssl.sh: https://testssl.sh/
