# Agent Integration — FinOps

## When to use
- Cloud bill > $5k/month and growing 20%+ MoM with no per-team visibility.
- AI/ML workloads with GPU costs (training + inference) where utilization is unknown.
- Multi-team / multi-product engineering org needing showback / chargeback.
- Pre-IPO / due-diligence phase requiring credible unit-economics ($/customer, $/transaction, $/inference).
- Reserved Instance / Savings Plan renewal coming up — need data-driven commitment sizing.
- Kubernetes cluster shared across teams where pods are unaccounted ("who owns this Deployment?").

## When NOT to use
- Cloud bill < $1k/month — the FinOps tooling will cost more than the savings; eyeball billing weekly.
- Workloads on flat-fee infra (bare metal, fixed VPS) — there's no elastic cost to optimize.
- Crisis cost-cutting that can't wait — apply blunt instruments first (turn off non-prod overnight, kill orphan resources), then formalize FinOps.
- Strict regulated workloads where security/compliance trumps cost (e.g. dedicated HSMs, isolated tenancy) — don't let an AI-driven "savings" agent touch them.

## Where it fails / limitations
- Tagging hygiene is the foundation; without 95%+ tag coverage, FinOps reports are estimates dressed as facts. Agents producing showback from incomplete tags spread misinformation.
- Anomaly detection algorithms in cloud-native tools (AWS Cost Anomaly Detection, Azure Cost Management) are noisy on monthly cycles and miss slow burns.
- Spot/preemptible savings only materialize if checkpointing is implemented; agents enable spot without checkpointing and the next training run loses 12 hours of work.
- Reserved Instance / Savings Plan over-commitment locks in spend; under-commitment leaves money on the table — agents err in either direction.
- Chargeback can break engineering culture if introduced without context (teams optimize for budget instead of features). Showback first.
- AI cost is volatile per request (token counts vary 10x); FinOps dashboards built on instance-hours hide the real driver — request economics.

## Agentic workflow
FinOps with agents is mostly continuous-loop optimization: tag enforcement, idle detection, rightsizing recommendations, commitment-purchase advice, anomaly triage. Have a daily "billing-snapshot" agent ingest CUR/billing exports → write to a queryable store (Athena/BigQuery/Snowflake). A "tag-auditor" agent flags untagged resources. An "idle-hunter" agent finds candidates (low CPU, no traffic, old snapshots, unattached EBS, idle NAT gateways) and files PRs / Jira tickets — never auto-deletes. Weekly, an "RI/SP-advisor" runs against the last 30/90-day usage to propose commitments. Always require human approval for any action with >$X impact.

### Recommended subagents
- `faion-sdd-executor-agent` — drives optimization tickets (specs ↔ approvals ↔ closeout) through quality gates.
- A custom `finops-tag-auditor` (Sonnet, read-only) — given billing export + tag policy, lists untagged resources by spend with owner-best-guess from CloudTrail.
- A custom `finops-rightsizing-advisor` (Opus) — given utilization metrics, proposes instance-class changes with risk/saving table.
- `password-scrubber-agent` — Cost Explorer credentials and BigQuery service accounts often inline in scripts.

### Prompt pattern
```
Generate weekly FinOps report for <account/org>.
Inputs: 7d + 28d billing exports, tag policy, prior recommendations, current commitments.
Output: (1) top 10 cost movers (week-over-week, with attribution), (2) untagged resource spend, (3) idle-resource candidates with reclaim impact ($, risk), (4) RI/SP coverage + recommendation for next purchase, (5) AI-workload cost per 1k requests, (6) anomaly list with confidence score.
Forbid: any auto-delete; produce tickets/PRs only; mark every recommendation with a reversibility flag (1-way / 2-way door).
```

```
Idle-resource analysis. For each resource: (id, type, account, owner_tag, monthly_cost, last_activity, evidence_metric, recommended_action, blast_radius, rollback_command). Flag any without `owner_tag` for tagging triage.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `aws ce` (Cost Explorer) | Cost & forecast queries | https://docs.aws.amazon.com/cli/latest/reference/ce/ |
| `aws cur` / S3 + Athena | Cost & Usage Report — single source of truth | https://docs.aws.amazon.com/cur/ |
| `aws compute-optimizer` | Rightsizing recs | https://aws.amazon.com/compute-optimizer/ |
| `gcloud billing` / BigQuery billing export | GCP detailed billing | https://cloud.google.com/billing/docs/how-to/export-data-bigquery |
| `gcloud recommender` | Idle/rightsizing recommendations | https://cloud.google.com/recommender/docs |
| `az consumption` / Cost Management exports | Azure billing | https://learn.microsoft.com/azure/cost-management-billing/ |
| `kubectl-cost` (Kubecost CLI) | K8s cost allocation | https://www.kubecost.com/ |
| `infracost` | IaC cost diff in PRs | https://www.infracost.io/ |
| `cloudability-cli` / Apptio APIs | Multi-cloud aggregation | https://docs.apptio.com/ |
| FOCUS spec exporters | Vendor-neutral billing format | https://focus.finops.org/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| AWS Cost Explorer + Cost Optimization Hub | SaaS | Yes | Native; Amazon Q for natural-language cost queries. |
| GCP FinOps Hub 2.0 + Gemini Cloud Assist | SaaS | Yes | Built-in recommender + AI summaries. |
| Azure Cost Management + Copilot | SaaS | Yes | Forecasts + recommendations + budgets. |
| CloudZero | SaaS | Yes | Unit-economics focus, AI cost analytics. |
| Spot.io | SaaS | Yes | Spot/preemptible orchestration with fallbacks. |
| Kubecost / OpenCost | SaaS / OSS | Yes | K8s cost allocation; OpenCost is CNCF. |
| Apptio Cloudability | SaaS | Yes | Multi-cloud showback/chargeback. |
| Densify | SaaS | Yes | ML rightsizing. |
| ProsperOps | SaaS | Yes | Automated commitment management (RIs/SPs). |
| Vantage | SaaS | Yes | Multi-cloud reports + alerts. |
| Infracost | OSS / SaaS | Yes | IaC PR cost gates. |

## Templates & scripts
See `templates.md` for full reports. Inline AWS idle-EBS finder (≤40 lines):

```python
# scripts/finops_idle_ebs.py
import boto3, datetime as dt, json

ec2 = boto3.client("ec2")
ce = boto3.client("ce")
PRICE_PER_GB_MONTH = {"gp3": 0.08, "gp2": 0.10, "io2": 0.125}

def find_unattached_volumes():
    paginator = ec2.get_paginator("describe_volumes")
    out = []
    for page in paginator.paginate(Filters=[{"Name": "status", "Values": ["available"]}]):
        for v in page["Volumes"]:
            age = (dt.datetime.now(dt.timezone.utc) - v["CreateTime"]).days
            if age < 7:
                continue  # ignore freshly detached, may be in flight
            owner = next((t["Value"] for t in v.get("Tags", []) if t["Key"] == "owner"), None)
            cost = v["Size"] * PRICE_PER_GB_MONTH.get(v["VolumeType"], 0.10)
            out.append({
                "id": v["VolumeId"],
                "type": v["VolumeType"],
                "size_gb": v["Size"],
                "age_days": age,
                "owner": owner,
                "monthly_cost_usd": round(cost, 2),
                "recommended_action": "snapshot+delete" if age > 30 else "tag-for-review",
                "rollback": f"aws ec2 create-volume --snapshot-id <pre-delete-snapshot> --availability-zone {v['AvailabilityZone']}",
            })
    return sorted(out, key=lambda x: -x["monthly_cost_usd"])

if __name__ == "__main__":
    print(json.dumps(find_unattached_volumes(), indent=2, default=str))
```

## Best practices
- Tag policy first, optimization second. Without `owner`, `cost-center`, `env`, `data-class` on >95% of resources, every report is fiction.
- Showback (visibility) → Chargeback (accountability) → Optimization (action). Skipping showback breaks trust.
- Run cost gates in CI: `infracost diff` on every IaC PR; block PRs that increase monthly cost > threshold without justification.
- Dual ownership: every workload has a `owner-team` (engineering) and a `cost-owner` (finance/PM); they reconcile monthly.
- Commit to RIs/SPs at 60-70% baseline coverage, never 100% — leaves headroom for autoscale.
- AI-cost specifics: track `$/request`, `$/1k tokens`, `$/training-run`, `cache-hit-rate`. Without these, GPU spend is opaque.
- Set budget alerts at 50/75/90/100% and route to Slack + on-call; not just email.
- Anomalies: alert on absolute $ delta + relative % delta; either alone produces noise.
- Reversibility flag on every recommendation: 1-way doors (terminate prod DB) need human approval; 2-way doors (resize idle dev VM) can be agent-driven.

## AI-agent gotchas
- Agents conflate "low CPU" with "idle" — a service may be I/O bound or use GPU; rightsizing on CPU alone breaks workloads.
- LLMs propose Spot for stateful workloads ("save 70%!") without checkpointing/tolerance — produces a data-loss incident dressed as savings.
- RI/SP recommendations from LLMs assume usage continues linearly; force the agent to call out the assumption ("this assumes >70% steady-state usage continues 12 months").
- AI-cost reports reuse instance-hour primitives; LLMs hide token-economics. Always include token-level metrics for AI workloads.
- Tag-fix automations rewrite owner tags based on stale CloudTrail data — the original creator left the company. Cross-reference HRIS / Backstage catalog before assigning.
- Auto-shutdown of "idle" non-prod hits at 18:00 UTC, breaks an APAC team's morning. Add timezone awareness to schedules.
- Anomaly detection: agents claim a 200% spike but it's a normal monthly batch run. Always train the detector on >60 days of seasonality.
- Human-in-loop checkpoint: any action that terminates resources, modifies RIs, or rotates instance families must be human-approved with an explicit cost-impact diff. Agent emits the ticket; human signs off; agent applies after the click.
- Don't let one agent both detect and remediate; split detection (read-only) from remediation (write, gated). Prevents runaway "savings" loops.

## References
- FinOps Foundation — https://www.finops.org/
- FinOps Framework — https://www.finops.org/framework/
- FOCUS spec — https://focus.finops.org/
- AWS Cost Optimization Hub — https://aws.amazon.com/aws-cost-management/aws-cost-optimization-hub/
- GCP FinOps Hub — https://cloud.google.com/cost-management
- Azure Cost Management — https://learn.microsoft.com/azure/cost-management-billing/
- Kubecost / OpenCost — https://www.kubecost.com/ , https://www.opencost.io/
- Infracost — https://www.infracost.io/
- "Cloud FinOps" (J.R. Storment, Mike Fuller) — O'Reilly
- AI cost benchmarking — https://www.cloudzero.com/blog/ai-costs/
