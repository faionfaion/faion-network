# Agent Integration — Reliability Architecture

## When to use
- Service has a contractual SLA or a user-facing availability target — you must measure and meet it.
- Frequent incidents driven by a small set of dependencies or failure modes — formal patterns (CB, retry, bulkhead, fallback) replace ad-hoc fixes.
- Pre-launch hardening for a system that will face traffic spikes, untrusted clients, or critical-path dependencies.
- Multi-region / DR planning: RPO and RTO have to be defined and validated, not just claimed.
- Migrating from on-call hero-mode to SRE: SLIs, SLOs, error budgets, runbooks, chaos drills.
- Adding a high-risk dependency (payments, identity, ML inference) where partial failure is the default mode.

## When NOT to use
- Pre-PMF / hobby project — reliability theater while users haven't validated the product is misallocated effort.
- Single-region single-service CRUD with <1k DAU — basic monitoring + a backup is enough; full SRE stack is overkill.
- "Five nines" target with no business case — the cost curve is exponential past four nines, almost no consumer SaaS justifies it.
- Static-site / read-only systems — CDN + origin is the entire reliability story.
- Where business reality dictates "ship features now, fix reliability later" and management owns the trade-off explicitly — formalizing without buy-in is theater.

## Where it fails / limitations
- **SLOs without error budget policy.** Defining 99.9% means nothing if there's no rule for what happens when the budget is exhausted (feature freeze, dedicated incident week, etc.).
- **Retries amplifying outages.** Dumb retries during a partial outage triple the load on the failing service. Without exponential backoff + jitter + circuit breakers, retries make outages worse.
- **Health checks lying.** A /healthz that returns 200 even when the DB is unreachable is the most common cause of "load balancer says everything is fine, customers say nothing works." Liveness vs readiness must be distinct.
- **DR exercises rare or theoretical.** "We have backups" without a quarterly restore test means you don't have backups.
- **Chaos engineering as theater.** Game-day a chaos experiment in pre-prod, declare victory; production behaves differently. Real chaos engineering is in production with a small blast radius.
- **MTTR averaged across noise.** A single 4-hour incident dominates the average; use percentiles or stratify by severity.
- **Cascading failure from shared resources.** Connection pool exhausted by one tenant, thread pool blocked by one slow call — bulkheading is the answer; agents rarely add it.
- **Multi-region added late.** Going active-active after the data layer is deeply single-region usually requires re-architecture, not a cluster move.

## Agentic workflow
Drive reliability work as a four-pass pipeline: (1) an SLO-elicitation agent reads the spec and proposes SLIs / SLOs / error budgets per service tier; (2) a failure-mode agent runs an FMEA-style enumeration: for each dependency, what fails, how is it detected, mitigated, monitored; (3) a pattern-application agent generates circuit-breaker / retry / bulkhead / timeout configurations for each external call (preferably as middleware or via a service mesh); (4) a chaos-experiment agent generates a Litmus / Chaos Mesh / AWS FIS experiment per critical failure mode and wires it into a quarterly schedule. Critical: agents must never autonomously execute chaos experiments in production — always human-gated.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — turn each SLO and failure-mode mitigation into an SDD task with quality gates: every PR adding an external dependency must include timeout, retries, and a circuit breaker.
- A purpose-built **SLO definer** (worth creating): given service tier + traffic stats, output a `slo.yaml` with SLI definitions (PromQL), targets, windows, error-budget policy, alert rules.
- A purpose-built **runbook generator** (worth creating): per critical alert, emit a markdown runbook with detection, diagnosis, mitigation, escalation.
- A purpose-built **chaos-experiment generator**: emit Litmus / Chaos Mesh / AWS FIS templates, blast radius per environment, abort criteria, success measure.
- `password-scrubber-agent` — runbooks routinely embed credentials, customer IDs, support ticket links; scrub before sharing externally.

### Prompt pattern
SLO definition:
```
For service <name> with traffic profile <profile> and tier <tier>,
propose SLIs (latency, availability, error rate, freshness as
applicable). For each SLI: PromQL, target, window, error budget,
burn-rate alert thresholds (fast 2%/1h and slow 5%/6h). Output
slo.yaml. Reject SLOs without a measurable PromQL SLI.
```

Resilience hardening:
```
Audit src/ for external dependency calls (HTTP, DB, broker, cache).
For each call site, list current timeout, retry config, circuit
breaker status, fallback behavior. For any call missing any of these,
propose specific config and the smallest code change. Output a
markdown table.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `prometheus` / `promtool` | Validate SLO recording/alerting rules | https://prometheus.io |
| `slo-generator` (Google) / `pyrra` | Generate SLO Prometheus rules from declarative spec | https://github.com/google/slo-generator ; https://github.com/pyrra-dev/pyrra |
| `sloth` | Generate multi-window/multi-burn-rate Prometheus rules | https://sloth.dev |
| `k6` / `locust` / `wrk2` | Load test SLO compliance under expected traffic | https://k6.io |
| `chaos-mesh` / `litmus` / `aws fis` | Inject failures (latency, partition, kill, disk fill) | https://chaos-mesh.org ; https://litmuschaos.io ; https://aws.amazon.com/fis/ |
| `gremlin` | Commercial chaos platform with safety controls | https://www.gremlin.com |
| `wal-g` / `pgbackrest` / `restic` | Continuous DB backups + restore tests | https://github.com/wal-g/wal-g ; https://pgbackrest.org ; https://restic.net |
| `velero` | k8s cluster + PV backups | https://velero.io |
| `dnscontrol` / `octodns` | Multi-DNS-provider failover automation | https://github.com/StackExchange/dnscontrol |
| `claude` (Anthropic CLI) | Run SLO / hardening / chaos passes headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Datadog SLO / Grafana Cloud SLO / New Relic | SaaS | yes | Managed SLO products with burn-rate alerts. |
| Nobl9 / Lightstep | SaaS | yes | Dedicated SLO platforms with multi-source SLIs. |
| PagerDuty / Opsgenie | SaaS | yes | Incident routing + on-call schedules; required for SLO-driven alerting. |
| StatusPage / Statuspal / Atlassian Statuspage | SaaS | yes | External-facing reliability comms; consume SLO state. |
| Cloudflare / Fastly / AWS Route 53 | SaaS | yes | Health-check-based DNS / Anycast failover; the easy path to multi-region. |
| AWS / GCP / Azure managed databases | SaaS | yes | Multi-AZ + cross-region replicas → RPO/RTO without DIY ops. |
| Temporal.io | OSS + SaaS | yes | Durable execution survives crashes — replaces brittle retry logic. |
| Istio / Linkerd | OSS service mesh | yes | mTLS, retries, timeouts, outlier detection, locality failover at the mesh layer. |
| Resilience4j / Polly / Hystrix-go / `tenacity` | OSS libs | yes | App-layer circuit breakers / retries when mesh isn't an option. |
| Vault / SOPS / AWS KMS | OSS / SaaS | yes | Secrets in DR plans must be retrievable at the failover site. |

## Templates & scripts
The README ships a thorough SLO doc, fault-tolerance pattern catalog, and an availability table. The high-leverage missing piece is a **resilience audit** that scans code for unsafe external calls. Inline drop-in (≤50 lines):

```python
#!/usr/bin/env python3
# resilience_audit.py — flag external calls without timeout/retry.
# Usage: python resilience_audit.py src/
import ast, sys, pathlib

UNSAFE = {
    ("httpx", "AsyncClient"): "default 5s timeout; specify explicit timeout",
    ("requests", "get"): "no default timeout — connections hang forever",
    ("requests", "post"): "no default timeout",
    ("aiohttp", "ClientSession"): "needs ClientTimeout; default is None",
    ("redis", "Redis"): "needs socket_timeout, socket_connect_timeout",
    ("psycopg", "connect"): "needs connect_timeout",
}
errs = []
for f in pathlib.Path(sys.argv[1]).rglob("*.py"):
    src = f.read_text()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = ast.unparse(node.func) if hasattr(ast, "unparse") else ""
            for (mod, name), reason in UNSAFE.items():
                if name in func:
                    kw = {k.arg for k in node.keywords if k.arg}
                    if "timeout" not in kw and "socket_timeout" not in kw \
                            and "connect_timeout" not in kw:
                        errs.append(f"{f}:{node.lineno} {func}() — {reason}")
for e in errs:
    print(e)
sys.exit(1 if errs else 0)
```

Wire into pre-commit on every service repo.

## Best practices
- **SLI before SLO.** Define what you measure (PromQL) before what you target (number). Without a measurable SLI, an SLO is wishful thinking.
- **Burn-rate alerts, not threshold alerts.** Multi-window multi-burn-rate (Google SRE workbook) reduces flapping and false positives.
- **Error budgets drive priorities.** Budget exhausted ⇒ feature freeze; budget healthy ⇒ ship riskier work. Make the policy written and enforced.
- **Retries: exponential + jitter + bounded.** Never retry forever; never retry without backoff; never retry without jitter.
- **Liveness vs. readiness vs. startup probes.** Liveness for crash detection; readiness for traffic admission; startup for slow-booting services. Don't conflate.
- **Bulkhead at the resource layer.** Separate connection pools / thread pools / queue groups per tenant or per dependency. One slow caller can't drain everyone else.
- **Test backups.** Quarterly restore drill from cold backup to a fresh environment, with a recorded runbook. Untested backups are not backups.
- **DR drills with timed RTO/RPO measurement.** Failover should be timed, with the result fed back into the DR document.
- **Chaos in prod, with safety.** Start in pre-prod; graduate to prod with a 1% blast radius, automatic abort on SLO impact.
- **Single team owns the SLO.** Shared SLOs become nobody's responsibility.
- **Runbook per alert.** Alerts without runbooks become noise; alerts with stale runbooks become traps.

## AI-agent gotchas
- **Retries without circuit breakers.** Generated code retries 3x with no breaker; on broker outage every consumer storms the broker. Always pair retries with a circuit breaker.
- **Unbounded retry intervals.** Agents default to fixed-1s retry; use exponential + jitter, max attempts.
- **Health-check theater.** Agents copy the README's `{"status": "ok"}` verbatim; require readiness probes that actually check downstream dependencies (DB ping, broker connection).
- **SLOs without burn-rate.** Agents emit a single threshold alert ("fire when error_rate > 1%"). Use multi-window/multi-burn-rate per the SRE Workbook.
- **Hallucinated PromQL.** Agents invent labels (`http_status_class`) that don't exist on your metrics. Validate against the live registry before merging.
- **Forgotten timeouts.** `httpx.AsyncClient()` without `timeout=` defaults to 5s; `requests` defaults to forever. Always require explicit timeouts.
- **Chaos experiments without abort criteria.** Agents emit `pumba kill` or Litmus YAML with no abort signal; production blast radius unbounded. Hard rule: every experiment has steady-state hypothesis + abort criteria.
- **DR plan without testing cadence.** Agents produce a beautiful DR markdown doc with no scheduled drill. Require a calendared rehearsal in the doc.
- **Retry on non-idempotent endpoints.** Agents retry POST `/charge_payment` on timeout, double-charging customers. Tag idempotency at the API contract level; reject retries on non-idempotent calls.
- **Blast radius optimism.** Generated chaos targets 100% of pods on first run; reduce to 1% with a "promote to higher" gate.
- **No human checkpoint on prod chaos / DR cutover.** These are destructive; never autonomous. Hard human-in-the-loop gate.
- **Cascading retry storm.** Service A retries B; B retries C; C retries D. End-to-end retry budget gets multiplicative. Coordinate retry budgets via `Retry-After` header / token-bucket limits.

## References
- Beyer, B., et al. — "Site Reliability Engineering." O'Reilly, 2016. (Free: https://sre.google/books/)
- Beyer, B., et al. — "The Site Reliability Workbook." O'Reilly, 2018.
- Nygard, M. — "Release It! 2nd ed." Pragmatic Bookshelf, 2018.
- Rosenthal, C., Jones, N. — "Chaos Engineering." O'Reilly, 2020.
- Google — "Multi-window multi-burn-rate alerting." https://sre.google/workbook/alerting-on-slos/
- AWS Well-Architected — Reliability pillar. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html
- Microsoft — "Reliability patterns." https://learn.microsoft.com/azure/architecture/framework/resiliency/reliability-patterns
- ISO/IEC 25010:2023 (Reliability characteristic). https://www.iso.org/standard/78176.html
- Sibling: `pro/dev/software-architect/observability-architecture/` (this batch).
- Sibling: `pro/dev/software-architect/quality-attributes-analysis/` (this batch).
- Sibling: `pro/infra/devops-engineer/`.
