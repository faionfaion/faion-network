# Agent Integration — Load Balancing Concepts

## When to use
- Choosing between L4 vs L7, picking an algorithm (round-robin, least-conn, ip-hash, least-response-time), and deciding session-persistence strategy before any tool config is written.
- Designing single-region vs multi-region (GSLB) topology and active-active vs active-passive HA.
- Capacity planning: how many backends, what health-check cadence, how sticky sessions impact autoscaling.
- Reviewing an architecture proposal that mentions "we'll just put a load balancer in front" — concept-level sanity check.
- Onboarding new engineers / agents to the vocabulary before letting them touch real configs.

## When NOT to use
- Vendor/tool selection — go to `load-balancing-implementation/` for HAProxy/NGINX/cloud LB specifics.
- TLS/cipher choices — see `ssl-tls-setup/`.
- Service-mesh internal routing — different concern (mTLS, sidecar/sidecarless).
- Database read replicas / write splitters — pattern is similar but tools differ; use DB-specific guidance.
- API gateway feature decisions (auth, quotas, transformations) — gateway is more than a load balancer.

## Where it fails / limitations
- Algorithm choice on paper rarely survives real traffic: round-robin can starve hot CPUs; least-conn is great until backends have wildly different request times.
- Sticky sessions are an anti-pattern for stateless services — agents who recommend them often hide a missing session store (Redis).
- IP hash + NAT/VPN clients = uneven distribution and "thundering herd" on a single backend.
- Health checks at L4 don't catch app-level failures (e.g., DB connection pool exhausted with healthy TCP socket).
- L4 vs L7 is not binary — modern stacks use L4 (NLB/HAProxy) in front of L7 (Ingress/Envoy) and agents conflate the two.
- GSLB DNS TTLs are honored unevenly by clients; failover takes 30s–5min in practice.

## Agentic workflow
This is a "decide before configure" methodology. The agent's job is to convert a business + traffic profile (RPS, conn count, p99 latency target, geographic spread, statefulness, growth curve) into a recommended LB topology document — not config files. Output a short Architecture Decision Record: chosen layer (L4/L7/both), algorithm, persistence policy, health-check depth, HA pattern, expected failure modes. Pair the result with `load-balancing-implementation/` for the actual rollout.

### Recommended subagents
- `faion-sdd-executor-agent` — produce ADR documents, design diffs, review cycles.
- `faion-brainstorm` — diverge/converge on topology options when traffic profile is unusual.
- Custom `lb-architect` — takes traffic profile JSON, returns ADR markdown with explicit trade-offs.

### Prompt pattern
"You are an LB architect. Input: `{p99_target_ms, rps, concurrent_conn, regions, stateful: bool, websocket: bool, tls_termination: edge|reencrypt|passthrough}`. Output an ADR with sections: Decision (one sentence), Layer (L4/L7/L4+L7), Algorithm, Persistence (none|cookie|ip-hash|app), Health Check (TCP|HTTP|gRPC, interval/threshold), HA (single|active-passive|active-active|GSLB), Risks. Refuse if RPS > 100k and `stateful=true` — recommend stateless redesign first."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `vegeta`, `wrk2`, `oha`, `k6` | Drive synthetic traffic to validate algorithm choice | https://k6.io/ |
| `mtr`, `traceroute`, `dig +trace` | Verify GSLB / DNS routing | bundled |
| `dnsperf` | Measure GSLB lookup latency | https://www.dns-oarc.net/tools/dnsperf |
| `iperf3` | L4 throughput baseline | https://iperf.fr/ |
| `tc qdisc` (Linux netem) | Inject latency/loss to test failover | iproute2 |
| `httpx` | L7 probing — TLS, headers, ALPN | https://github.com/projectdiscovery/httpx |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| AWS Route 53 (latency/geo routing) | SaaS | Yes — API | DNS-based GSLB |
| Cloudflare Load Balancing | SaaS | Yes — API | Global anycast + health checks |
| NS1 / Akamai GTM | SaaS | Yes — API | Enterprise GSLB |
| AWS Global Accelerator | SaaS | Yes — API | Anycast L4 in front of regional LBs |
| GCP Global Load Balancer | SaaS | Yes | Single anycast IP, multi-region |
| Azure Traffic Manager + Front Door | SaaS | Yes | DNS GSLB + edge L7 |
| keepalived + VRRP | OSS | Yes | Active/passive VIP failover, classic on-prem |
| Pacemaker/Corosync | OSS | Partial | Heavy cluster manager, niche today |

## Templates & scripts
See `templates.md` for ADR scaffolds and decision trees. Inline traffic-shape sniff for sizing:

```bash
#!/usr/bin/env bash
# traffic-shape.sh — quick traffic profile from access logs to feed LB design
LOG=${1:?nginx access log}
echo "Total reqs:    $(wc -l < "$LOG")"
echo "Unique IPs:    $(awk '{print $1}' "$LOG" | sort -u | wc -l)"
echo "Top 5 paths:"
awk '{print $7}' "$LOG" | sort | uniq -c | sort -rn | head -5
echo "Status mix:"
awk '{print $9}' "$LOG" | sort | uniq -c | sort -rn
echo "p50/p95/p99 req/s (1s buckets):"
awk '{print substr($4,2,20)}' "$LOG" | uniq -c | awk '{print $1}' \
  | sort -n | awk 'BEGIN{c=0} {a[c++]=$1} END{print a[int(c*0.5)],a[int(c*0.95)],a[int(c*0.99)]}'
```

## Best practices
- Decide statefulness first: if you can avoid sticky sessions, the design simplifies dramatically.
- Default to L7 with HTTP health checks for web/API; drop to L4 only when L7 features are unused or you measured the CPU cost.
- Use `least-connections` (or weighted least-conn) over round-robin for variable-cost endpoints; round-robin is fine for uniform short requests.
- Health check depth: a `/healthz` that touches the critical dependency (DB ping with timeout) is worth its cost.
- Thresholds: 2 of 3 consecutive failures, 10s interval, 5s timeout — start there, tune from outage data.
- For zero-downtime deploys: connection draining + readiness probe matched to LB de-register lag.
- Multi-region: prefer anycast (Global Accelerator, Cloudflare, GCP GLB) over DNS-based failover — clients respect TTL poorly.
- Document the chosen pattern in an ADR; revisit when traffic doubles or new region is added.

## AI-agent gotchas
- LLMs default to "round-robin is fairest" — push for least-connections or response-time-aware unless backends are uniform.
- "Sticky sessions" gets recommended for any state issue — flag it and ask whether a Redis/Memcached session store is the real fix.
- L4 vs L7 confusion: agents propose "L4 for performance" then list L7 features (path routing, header rewrite); reject the inconsistency.
- GSLB latency claims: agents quote sub-second failover; real DNS TTL behavior is 30s–5min — set realistic SLOs.
- Health check intervals: agents pick 1s aggressively; on large fleets this DDoSes backends with health probes — scale interval with fleet size.
- Algorithm + autoscaling interaction: ip-hash + frequent scale events causes constant re-distribution; agents miss this.
- Capacity math: agents forget that LB CPU itself becomes the bottleneck for TLS-heavy or regex-heavy L7 — size the LB tier explicitly.

## References
- HAProxy — Layer 4 vs Layer 7: https://www.haproxy.com/blog/layer-4-vs-layer-7-load-balancing
- HAProxy — Sticky sessions deep dive: https://www.haproxy.com/blog/load-balancing-affinity-persistence-sticky-sessions-what-you-need-to-know
- Cloudflare — Algorithms: https://www.cloudflare.com/learning/performance/types-of-load-balancing-algorithms/
- Google Cloud — HTTPS LB best practices: https://cloud.google.com/load-balancing/docs/https/http-load-balancing-best-practices
- AWS Global Accelerator vs Route 53: https://aws.amazon.com/global-accelerator/faqs/
- Brendan Gregg — USE method (for LB capacity reasoning): https://www.brendangregg.com/usemethod.html
