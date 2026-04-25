# Agent Integration — AIOps

## When to use
- Reducing alert noise: deduping, correlating, and enriching incidents from Prometheus/Datadog/Splunk so on-call sees signal not spam.
- Root-cause analysis across topology — propagating from a customer-facing symptom back to the service/host/deploy that broke.
- Auto-remediation runbooks (restart, scale, rollback, failover) gated by trust level and human approval.
- Predictive capacity / failure forecasting before a known seasonal spike or a slow-growing leak crosses an SLO.
- Postmortem assistance: timeline assembly from logs/traces/deploys.

## When NOT to use
- Greenfield systems with <90 days of historical data — anomaly baselines need history; rule-based alerts are better at start.
- Compliance-critical paths where "AI suggested it" is not an acceptable audit trail — keep deterministic alerting.
- Hard real-time control loops (μs latency) — AIOps is observability/ops layer, not control plane.
- Fixing a culture problem (unclear ownership, no runbooks). AIOps amplifies whatever incident process exists; it does not create one.
- Replacing SREs — AIOps augments triage, doesn't own decisions.

## Where it fails / limitations
- Garbage-in: noisy or high-cardinality metrics will produce noisy anomalies. Tag hygiene and SLI definition matter more than the model.
- Concept drift: a deploy or product change shifts "normal" — models need retraining triggers tied to deploy events.
- Topology blind spots: anomaly correlation needs a service map (Datadog APM, OpenTelemetry, Service Catalog). Without it, RCA is guessing.
- LLM hallucination on RCA: pattern-matching plausible-sounding but wrong narratives is common; always cite specific metric/log evidence.
- Auto-remediation blast radius: a faulty `kubectl rollout restart` policy can cascade across services; circuit breakers and rate limits are mandatory.
- Vendor lock-in: native AIOps in Datadog/Dynatrace/Splunk works well inside the platform but exporting model logic is hard.

## Agentic workflow
Run AIOps as a tiered loop. Tier 1 — deterministic correlation: dedup, group by service/deploy, route. Tier 2 — ML anomaly detection on multi-signal panels (error rate + latency + saturation), promote only convergent anomalies (≥2 signals). Tier 3 — LLM agent enriches the incident with linked runbook, recent deploys, similar past incidents, and a recommended remediation with a confidence score; human approves; system executes via well-defined remediation actions (restart pod, rollback deploy, scale ASG, failover replica). Each tier has a kill switch and a rate limit. Feed every action's outcome back into a "remediation efficacy" metric to tune trust levels.

### Recommended subagents
- `faion-sdd-executor-agent` — implement the remediation runbook code with quality gates.
- Custom `incident-triage-agent` — reads Alertmanager/PagerDuty + recent CI/CD events, returns enriched incident JSON.
- Custom `rca-correlator-agent` — pulls traces, logs, and topology to propose a root cause hypothesis with evidence URLs.
- Custom `runbook-executor-agent` — executes only from a whitelist of approved remediations, refuses unknown actions.

### Prompt pattern
"You are an incident triage agent. Input: PagerDuty incident JSON + last 30 minutes of metrics for service `{svc}`. Tasks: (1) classify severity, (2) list correlated signals (error_rate↑, latency↑, saturation↑), (3) link the most recent deploy/config change within the last hour, (4) pick ONE remediation from this whitelist: [`rollback_last_deploy`, `restart_pod`, `scale_replicas+2`, `noop_observe`]. Output JSON only: `{severity, signals, suspect_change, remediation, confidence_0_1, evidence_urls}`. Refuse if data is missing — return `noop_observe`."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `promtool` | Validate Prometheus rules, query data | https://prometheus.io/docs/prometheus/latest/command-line/promtool/ |
| `amtool` | Manage Alertmanager silences/routes | https://github.com/prometheus/alertmanager |
| `mimirtool` | Grafana Mimir tenant ops | https://grafana.com/docs/mimir/latest/manage/tools/mimirtool/ |
| `logcli` | Query Loki logs | https://grafana.com/docs/loki/latest/query/logcli/ |
| `tempo-cli` | Query Tempo traces | https://grafana.com/docs/tempo/latest/operations/tempo-cli/ |
| `kubectl events` / `kubectl debug` | K8s event triage | https://kubernetes.io/docs/reference/kubectl/ |
| `k9s` | TUI for K8s incident triage | https://k9scli.io/ |
| `stern` | Multi-pod log tailing | https://github.com/stern/stern |
| `pd-cli` | PagerDuty incidents from terminal | https://github.com/martindstone/pagerduty-cli |
| `dd-cli` (Datadog) | Datadog API automation | https://github.com/DataDog/datadog-ci |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Datadog AIOps (Watchdog) | SaaS | Yes — strong API, webhooks | Native anomaly detection + Bits AI summarization |
| Splunk ITSI / Observability | SaaS | Yes — REST + SOAR | Strongest in log-heavy orgs |
| Dynatrace Davis AI | SaaS | Yes — auto root cause | Best deterministic causal analysis |
| New Relic AIOps | SaaS | Yes — NRQL + webhooks | Good incident intelligence |
| Grafana OnCall + Sift | OSS + SaaS | Yes | Lightweight; pairs with Mimir/Loki/Tempo |
| BigPanda | SaaS | Yes — event correlation API | Vendor-neutral aggregator |
| Moogsoft | SaaS | Yes | ML noise reduction |
| ServiceNow ITOM | SaaS | Yes | Enterprise-heavy, good for ITSM tie-in |
| PagerDuty (with Event Intelligence) | SaaS | Yes — webhooks + API | De-facto on-call routing |
| Robusta (K8s) | OSS | Yes — playbooks-as-code | K8s-specific auto-remediation |
| Keep | OSS | Yes — workflows-as-code | Open-source AIOps orchestration |

## Templates & scripts
See `templates.md` for runbook patterns. Inline minimal anomaly-to-action loop:

```python
# aiops_loop.py — convergent-signal anomaly + whitelisted remediation
import os, json, requests, statistics
from datetime import datetime, timedelta, timezone

PROM = os.environ["PROM_URL"]
WHITELIST = {"rollback_last_deploy", "restart_pod", "scale_replicas+2", "noop_observe"}

def q(expr):
    r = requests.get(f"{PROM}/api/v1/query", params={"query": expr}, timeout=5)
    return float(r.json()["data"]["result"][0]["value"][1]) if r.json()["data"]["result"] else 0.0

def zscore(svc, metric, window="30m"):
    cur = q(f'avg({metric}{{service="{svc}"}})')
    hist = q(f'avg_over_time({metric}{{service="{svc}"}}[7d])')
    sd = q(f'stddev_over_time({metric}{{service="{svc}"}}[7d])') or 1.0
    return (cur - hist) / sd

def triage(svc):
    sigs = {
        "error_rate": zscore(svc, "rate(http_requests_total{status=~\"5..\"}[5m])"),
        "latency_p99": zscore(svc, "histogram_quantile(0.99, http_request_duration_seconds_bucket)"),
        "saturation": zscore(svc, "container_cpu_usage_seconds_total"),
    }
    convergent = sum(1 for v in sigs.values() if v > 3)
    action = "noop_observe"
    if convergent >= 2:
        action = "rollback_last_deploy"
    assert action in WHITELIST
    return {"svc": svc, "ts": datetime.now(timezone.utc).isoformat(), "signals": sigs, "action": action}

if __name__ == "__main__":
    import sys
    print(json.dumps(triage(sys.argv[1]), indent=2))
```

## Best practices
- Define SLIs/SLOs first; AIOps without explicit objectives just produces prettier noise.
- Multi-signal convergence ≥ 2 before paging a human; single-metric anomalies are too noisy.
- Tag every alert with the deploy SHA and config-version of the affected service so RCA correlation is mechanical.
- Trust ladder: recommend → human-approve → auto-execute on low-risk only (restart, scale-up). Never auto-execute scale-down or DB failover without human.
- Postmortem feedback loop: every incident updates anomaly thresholds and runbook efficacy scores.
- Separate "sense" (detect) from "act" (remediate) infrastructure — different deploy cadence, different blast radius.
- Quarterly chaos drill: inject known anomalies and verify the AIOps stack catches them within target MTTD.

## AI-agent gotchas
- LLMs invent metric names ("p99_latency_seconds") that don't exist; always fetch the Prometheus label/metric inventory first and constrain output to that list.
- Time-zone bugs: agents producing time ranges without explicit UTC mismatch with Grafana/Datadog UI; force ISO-8601 with `Z`.
- Confidence scores from LLMs are not calibrated probabilities — never use them as the sole gate for auto-remediation; combine with a deterministic check.
- Recursive paging: a misconfigured agent that posts back to PagerDuty can create alert loops; rate-limit outbound webhooks.
- Token-cost runaway: streaming all logs into an LLM context for triage burns money fast — use sketches (top-K, log patterns via `logreduce`/`drain3`) before LLM.
- Auto-remediation drift: whitelisted actions evolve; pin remediation versions and require code review on changes.
- Chat-channel flooding: an LLM enriching every alert into a Slack thread overwhelms responders — gate by severity.

## References
- Selector — AIOps in 2025: https://www.selector.ai/learning-center/aiops-in-2025-4-components-and-4-key-capabilities/
- Datadog Watchdog & Bits AI: https://www.datadoghq.com/product/watchdog/
- Dynatrace Davis: https://www.dynatrace.com/platform/artificial-intelligence/
- Robusta playbooks: https://docs.robusta.dev/master/
- Keep — open-source AIOps: https://github.com/keephq/keep
- Drain3 log clustering: https://github.com/IBM/Drain3
- Google SRE Workbook — Postmortems: https://sre.google/workbook/postmortem-culture/
