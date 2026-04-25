# Agent Integration — FinOps: Cloud Cost Optimization

## When to use
- Monthly cloud bill > $5K and growing faster than revenue / usage; rightsizing has measurable ROI.
- Multiple environments (dev/stage/prod) with no per-team cost attribution; tagging gap is high.
- AI/ML workload introduction (GPU spend) where idle utilization is the dominant cost driver.
- Pre-RI / pre-Savings-Plan commitment decision: need 6+ months of usage analysis to size a 1- or 3-year commit.
- Setting up FinOps Inform → Optimize → Operate phases for a new BU or product team.

## When NOT to use
- Pre-PMF startup with < $1K / month bill — engineering time is more expensive than the savings.
- Workload is on a fixed-price contract (e.g., enterprise EA with no metered burst) — cost optimization actions don't lower the invoice.
- Compliance / sovereignty constraints lock you to a single SKU family with no spot or alternative-arch options.
- Very spiky workloads where rightsizing recommendations are noise (a one-week sample lies; agents will cut prod capacity).

## Where it fails / limitations
- Cost Explorer / Billing API has a 24-48h delay; agents driving same-day decisions will use stale data.
- Rightsizing recommendations from cloud providers ignore application-level SLOs — an agent that auto-applies them will cause incidents.
- Spot instance interruption rate varies by region/AZ/family in ways that historical data does not predict (AWS reclaims based on real-time capacity).
- Tagging policies are eventually-consistent across services (ECS, Lambda, EBS) — coverage reports lag reality.
- Savings Plans / RIs are non-cancellable; an LLM purchase recommendation without a human gate is a financial-risk event.
- Multi-cloud cost normalization (USD vs UoM differences) is non-trivial; do not let agents compare AWS m6i to GCP n2 by raw price.

## Agentic workflow
Frame FinOps as a read-heavy loop: agent pulls Cost Explorer / Billing Export / CUR data → joins with utilization metrics (CloudWatch, Stackdriver) → produces ranked recommendations → human approves → agent files PR / Jira ticket / Terraform change. Never let the agent execute purchase commitments, terminate prod resources, or modify Auto Scaling group bounds without an approval gate. The "operate" phase (anomaly response, idle-resource shutdown in non-prod) is the safe automation surface; the "optimize" phase (commitments, architecture changes) requires human sign-off.

### Recommended subagents
- A `finops-analyst` subagent (define inline) — read-only on billing APIs + utilization, outputs ranked recommendations as structured JSON (no execution rights).
- `faion-sdd-executor` — converts approved recommendations into Terraform / Pulumi diffs through quality gates.
- A `finops-anomaly-watcher` subagent — daily cron, diff today's spend vs 7-day MA per tag dimension, alert if > 2σ.

### Prompt pattern
```
Read role: AWS Cost Explorer + CloudWatch.
Output JSON only:
{ "recommendations": [
    {"id": "...", "service": "EC2", "current_monthly_usd": ..., "estimated_savings_usd": ...,
     "action": "rightsize|RI|spot|terminate", "risk": "low|medium|high",
     "evidence": {"avg_cpu_pct": ..., "p95_cpu_pct": ..., "sample_days": ...}}
]}
Do NOT call any write API. Skip recommendations with sample_days < 14.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `aws ce get-cost-and-usage` | Pull cost data with grouping/filters | https://docs.aws.amazon.com/cli/latest/reference/ce/ |
| `aws compute-optimizer get-ec2-instance-recommendations` | Native rightsizing | https://docs.aws.amazon.com/compute-optimizer/ |
| `gcloud billing` + BigQuery export | GCP cost analysis via SQL | https://cloud.google.com/billing/docs/how-to/export-data-bigquery |
| `az consumption usage list` | Azure metered usage | https://learn.microsoft.com/en-us/cli/azure/consumption |
| `kubecost` / `opencost` CLI | K8s cost allocation per namespace/pod | https://www.opencost.io/ |
| `infracost` | Pre-merge cost diff for Terraform / Pulumi | https://www.infracost.io/ |
| `cloudcustodian` (`custodian`) | Policy-as-code: tag enforcement, idle shutdown | https://cloudcustodian.io/ |
| `aws-nuke` (non-prod only) | Reap untagged / orphan resources in dev accounts | https://github.com/rebuy-de/aws-nuke |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| AWS Cost Optimization Hub | SaaS (built-in) | Yes — API | Aggregates Compute Optimizer + Trusted Advisor |
| GCP FinOps Hub + BigQuery export | SaaS | Yes — SQL API | Best agent surface (queryable) |
| Azure Cost Management | SaaS | Yes — REST API | Cost views by subscription / tag |
| CloudZero | SaaS | Yes — REST API | Unit economics ("cost per customer") |
| Vantage | SaaS | Yes — REST API | Multi-cloud + SaaS cost normalization |
| Kubecost / OpenCost | OSS / SaaS | Yes — Prom + REST | K8s allocation; pair with Prometheus agent |
| nOps | SaaS | Yes — REST API | Spot orchestration + commitment management |
| Spot.io (NetApp) | SaaS | Yes | Automated spot/RI mix; high-risk write surface |
| Sedai | SaaS | Yes — agent-driven | Autonomous optimization; vet before granting write rights |
| Apptio Cloudability | SaaS | Yes | Enterprise; heavyweight |

## Templates & scripts
See `templates.md` for tagging policy, RI coverage report, and spot-eligibility scoring. Inline daily anomaly-detection script (AWS):

```bash
#!/usr/bin/env bash
set -euo pipefail
START=$(date -u -d '8 days ago' +%F)
END=$(date -u -d 'today' +%F)
aws ce get-cost-and-usage \
  --time-period "Start=$START,End=$END" \
  --granularity DAILY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --output json > /tmp/cost.json
python3 - <<'PY'
import json, statistics, sys
d = json.load(open('/tmp/cost.json'))
by_svc = {}
for day in d['ResultsByTime']:
    for g in day['Groups']:
        svc = g['Keys'][0]
        cost = float(g['Metrics']['UnblendedCost']['Amount'])
        by_svc.setdefault(svc, []).append(cost)
for svc, vals in by_svc.items():
    if len(vals) < 8: continue
    today, hist = vals[-1], vals[:-1]
    mu, sd = statistics.mean(hist), statistics.pstdev(hist) or 0.01
    z = (today - mu) / sd
    if z > 2:
        print(f"ANOMALY {svc}: today=${today:.2f} mean=${mu:.2f} z={z:.1f}")
PY
```

## Best practices
- Drive everything off tags. No tag → it's waste by definition. Enforce at IaC layer (Cloud Custodian / Sentinel / OPA), not after-the-fact.
- Set commitment coverage target = 70% of baseline, not 100%. The last 30% of variance kills RI economics.
- Separate "always-on" workloads (RIs/SPs) from "elastic" (on-demand) from "interruptible" (spot). Tag accordingly so reports stay clean.
- Build the FinOps loop on a weekly cadence, not real-time. Cost data lag + commitment irreversibility punish fast loops.
- Track unit economics (cost per request, cost per active user, cost per GPU-hour) — absolute spend is a vanity metric.
- Keep a "kill list" of canonical waste patterns: idle EBS, unattached EIPs, stale snapshots > 90d, NAT Gateway egress without VPC endpoints, cross-AZ chatter, oversized RDS.
- Use Graviton / ARM as a default for new workloads where the runtime supports it; opt-out, not opt-in.
- AI workloads: monitor `gpu_utilization`, not just `cpu_utilization`. P95 GPU < 60% = rightsizing candidate.

## AI-agent gotchas
- LLM hallucinates spot interruption rates and RI break-even points. Always force the agent to cite the source row from the billing API; reject recommendations with no `evidence` field.
- Cost Explorer dimensions vs Cost & Usage Report (CUR) columns drift; agents trained on stale docs use deprecated dimension names. Ground in current API schema via tool description.
- Currency / tax handling: AWS reports unblended USD; Azure can be local currency including VAT. Agent comparing them without normalization gives wrong recommendation.
- Savings Plans calculator returns a recommendation in raw $/hr; agents misread the unit and over-commit. Add explicit `commitment_usd_per_hour` and `commitment_term_months` fields, never let the agent invent them.
- Anomaly detection on weekends: traffic-shaped workloads have legitimate Sat/Sun dips; naive z-score fires false positives. Use day-of-week-aware baseline.
- Untagged-resource reaping is the most dangerous automation. Always run in dry-run + Slack approval before write. Never give an agent `Action: ec2:TerminateInstances` on a prod account.
- LLM rounding: $0.013/hr × 730h ≈ $9.49 — model writes "$10" as "saves $10/month" then aggregates. Force two-decimal precision and integer arithmetic where possible.
- "FinOps for AI" certification (2025) introduced new vocabulary (Tokens / Inference Unit cost) — confirm agent uses current taxonomy.

## References
- FinOps Foundation Framework — https://www.finops.org/framework/
- AWS Cost Optimization Pillar (Well-Architected) — https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/
- Google Cloud FinOps Hub — https://cloud.google.com/cost-management
- OpenCost spec — https://www.opencost.io/docs/specification
- Infracost — https://www.infracost.io/docs/
- Cloud Custodian — https://cloudcustodian.io/docs/
- AWS Compute Optimizer — https://docs.aws.amazon.com/compute-optimizer/latest/ug/
- FinOps for AI (FOCUS spec) — https://focus.finops.org/
