# Agent Integration — DORA Metrics

## When to use
- Engineering org wants a baseline + improvement plan for software delivery performance.
- Quarterly/annual exec reporting: leadership needs a credible answer to "are we shipping faster?".
- Tracking AI-assistant adoption impact (DORA 2025 research shows AI affects stability/throughput; need data).
- Comparing teams' delivery health without falling into "lines of code" or "story points" anti-metrics.
- Justifying platform/CI investments — DORA metrics provide before/after evidence.

## When NOT to use
- Single-person / very small teams — the variance dominates the signal.
- As a stack-rank tool ("Team X is Elite, Team Y is Low — fire the manager"). Goodhart's Law applies hard.
- For non-software work (data pipelines, ML training, content) — definitions don't transfer cleanly.
- When the org doesn't yet have basic CI/CD — measure something else first (build pass rate, deploy automation %).
- As the only health metric — DORA + Reliability + SPACE + developer experience surveys complement each other.

## Where it fails / limitations
- "Deployment" definition is the swamp: deploys to prod-like staging? Feature flag rollouts? Per-service or per-monorepo? Without a written, agent-readable definition, every team measures something different.
- Lead Time conflates "commit to merge" + "merge to deploy" + "deploy to release"; agents collapse them and miss the actual bottleneck.
- Change Failure Rate depends on incident classification — many "rollbacks" are routine config changes, many incidents aren't tied to a deploy. Agents inflate or deflate CFR depending on the incident-system schema.
- MTTR includes detection time + response time + recovery time; agents compute from `incident.opened_at → resolved_at` and miss the silent half-hour before alert fire.
- 2025 research: AI-assistant adoption correlates with -1.5% throughput, -7.2% stability — likely because AI encourages larger batches. Agents must track batch size or DORA improvements are illusory.
- Vendor-tool dashboards (Sleuth/LinearB/Jellyfish) have opinionated definitions that may not match yours; agents take their numbers at face value.
- Elite-vs-Low buckets feel motivating but encourage gaming (artificial micro-deploys to bump frequency).
- "Reliability" as the fifth metric is not yet standardized — implementations vary; agents should expose error budget burn or SLO attainment, not invent their own.

## Agentic workflow
DORA metrics are continuous-collection problems with periodic reporting. Have a "collector" agent ingest from Git (commits, PRs), CI/CD (pipeline runs, deploy events), and incident systems (PagerDuty/Opsgenie/Statuspage) into a normalized event store. A "computer" agent runs daily to recompute the four metrics + reliability per service per team. A "narrator" agent (Opus) produces the weekly summary: which metric moved, why (correlate with deploys, incidents, batch size), and what to investigate. Always show trends over absolute numbers; always include batch-size and AI-adoption signals as confounders. Never let one agent both compute and adjust definitions — separate.

### Recommended subagents
- `faion-sdd-executor-agent` — drives definition specs and dashboard PRs through quality gates.
- A custom `dora-event-normalizer` (Sonnet) — given heterogeneous events, maps to {deploy, change, incident, recovery} schema with a confidence score; flags low-confidence rows for human review.
- A custom `dora-narrator` (Opus, read-only) — given weekly metric snapshot + diff vs prior, produces a 200-word narrative with hypothesized drivers; cites supporting evidence.

### Prompt pattern
```
Compute DORA metrics for service <X>, period <P>.
Inputs: git events (commits with merge_at), deploy events (pipeline `deploy_prod` success), incident events (severity, started_at, restored_at, deploy_correlation), feature-flag events.
Output: (1) Deployment Frequency (deploys/period), (2) Lead Time (p50, p95: merge_at → deploy_prod), (3) Change Failure Rate (incidents-tied-to-deploy / deploys), (4) MTTR (incident_started → restored), (5) Reliability proxy (SLO attainment %), (6) batch size (commits/deploy), (7) AI-assist signal (% PRs with AI co-author tag).
Forbid: counting non-prod deploys, inventing definitions, mixing services without disclosure, hiding small-N caveats (period < 10 deploys → mark as "low confidence").
```

```
Narrate week-over-week change. JSON: {metric, prev, curr, delta, hypothesized_drivers:[{driver, evidence_event_id, confidence}], suggested_investigation, confounders:[batch_size, ai_adoption, incident_severity_mix]}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Pull commits/PRs/runs for collection | https://cli.github.com/ |
| `glab` (GitLab CLI) | Same for GitLab | https://gitlab.com/gitlab-org/cli |
| `pagerduty-cli` / Opsgenie API | Incident export | https://github.com/PagerDuty/pagerduty-cli |
| `gcloud builds list` / `aws codepipeline` / `az pipelines runs list` | Pipeline events | provider docs |
| Four Keys (Google) | Reference implementation | https://github.com/GoogleCloudPlatform/fourkeys |
| `dora-cli` (community) | Local DORA computation from Git/GitHub | https://github.com/samsmithnz/DevOpsMetrics |
| `gh-dora` | DORA from GitHub via gh extension | https://github.com/stephenc/gh-dora |
| `prometheus` + `recording rules` | DORA-style SLIs in metrics store | https://prometheus.io/docs/practices/rules/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sleuth | SaaS | Yes | Native deploy tracking; good API. |
| LinearB | SaaS | Yes | Combines DORA + workflow metrics. |
| Swarmia | SaaS | Yes | Engineering analytics + initiative tracking. |
| Jellyfish | SaaS | Yes | Multi-source aggregation; biased to investment reporting. |
| GitLab Value Stream / DORA | SaaS / OSS | Yes | Free for GitLab native; reports under `/-/analytics/dora`. |
| GitHub Insights / Copilot DORA dashboards | SaaS | Partial | Limited definitions; supplement with custom. |
| Four Keys (Google Cloud) | OSS | Yes | BigQuery-native, deployable. |
| OpsLevel | SaaS | Yes | Service health + DORA. |
| DX (DX team) | SaaS | Yes | Combines DORA with developer experience surveys. |
| Faros AI | SaaS | Yes | Multi-source eng intelligence, GraphQL API. |

## Templates & scripts
See `templates.md` and `examples.md`. Inline DF + Lead Time computation from GitHub deployments (≤40 lines):

```python
# scripts/dora_compute.py
import subprocess, json, datetime as dt, statistics as st

def gh(cmd):
    return json.loads(subprocess.check_output(["gh", "api", "--paginate", cmd]))

REPO = "org/svc"
SINCE = (dt.datetime.utcnow() - dt.timedelta(days=28)).isoformat() + "Z"

deploys = [d for d in gh(f"/repos/{REPO}/deployments?environment=production")
           if d["created_at"] >= SINCE]

# Deployment Frequency
df_per_day = len(deploys) / 28

# Lead Time = merge_at(PR) -> deploy_at
lts = []
for d in deploys:
    sha = d["sha"]
    prs = gh(f"/repos/{REPO}/commits/{sha}/pulls")
    if not prs:
        continue
    merged = dt.datetime.fromisoformat(prs[0]["merged_at"].replace("Z", "+00:00"))
    deployed = dt.datetime.fromisoformat(d["created_at"].replace("Z", "+00:00"))
    lts.append((deployed - merged).total_seconds() / 60)  # minutes

print(json.dumps({
    "deploy_freq_per_day": round(df_per_day, 2),
    "n_deploys": len(deploys),
    "lead_time_min_p50": round(st.median(lts), 1) if lts else None,
    "lead_time_min_p95": round(sorted(lts)[int(0.95 * len(lts)) - 1], 1) if len(lts) > 4 else None,
    "low_confidence": len(deploys) < 10,
}, indent=2))
```

## Best practices
- Write a definitions doc in the repo (`docs/dora-definitions.md`) that humans + agents both read; treat it as ADR.
- Track per-service, not per-team — service ownership shifts; service identity is stable.
- Show trends with confidence intervals or low-N flags; one bad week shouldn't trigger reorgs.
- Pair Deployment Frequency with batch size (commits per deploy). Frequency without small batches is vanity.
- Include the 5th metric (Reliability) as SLO attainment, not invented uptime number.
- Annotate dashboards with deploys, incidents, AI-tool rollouts, team changes — narrative explains the curve.
- Use DORA for retrospectives, not performance reviews. People game what's used to judge them.
- Re-baseline after major org/process changes — comparing to old baseline misleads.
- Connect DORA to business outcomes (revenue, NPS, churn) once trust in definitions is established.

## AI-agent gotchas
- LLMs invent thresholds ("Elite means daily deploys") — anchor every claim to a citation; the official thresholds change yearly in the State of DevOps report.
- Lead-time computation often pulls `pr.created_at` instead of `pr.merged_at`; this inflates lead time and hides queue-after-merge time.
- Agents include hotfix deploys when computing DF (good) but exclude them from CFR (wrong) because they don't open an incident — fix the schema, not the calc.
- Multi-service repos: agents attribute deploys to the wrong service when the deploy event lacks a service label. Force the deploy event to carry `{service, sha, env, success}`.
- AI-coauthored PRs are detectable via co-author trailer or commit-message tags; agents skip the signal and miss the AI-impact dimension.
- "Time-zone aware" matters: deploy at 23:00 UTC vs 06:00 UTC affects DF buckets at month boundaries; pick UTC and stay there.
- Agents recompute history retroactively after a definition tweak — breaks trust. Version the definitions and freeze old data; show "definition v2 from 2026-01-15".
- Human-in-loop checkpoint: any definition change goes to an architect / engineering manager review; never let an agent silently move the goalposts.
- Don't auto-tweet "we are now Elite!" — DORA metrics are about learning, not bragging. Agent-generated celebratory messages are an anti-pattern.
- Don't let the same agent collect events and judge incidents; separate roles to prevent self-serving labeling.

## References
- DORA research / State of DevOps — https://dora.dev/research/
- Accelerate (Forsgren, Humble, Kim) — https://itrevolution.com/product/accelerate/
- Google Cloud "Four Keys" — https://github.com/GoogleCloudPlatform/fourkeys
- DORA 5th metric (Reliability) — https://cd.foundation/blog/2025/10/16/dora-5-metrics/
- GitLab DORA docs — https://docs.gitlab.com/user/analytics/dora_metrics/
- Atlassian DORA guide — https://www.atlassian.com/devops/frameworks/dora-metrics
- SPACE framework (companion) — https://queue.acm.org/detail.cfm?id=3454124
- "AI and DevEx" research (DX) — https://dx.com/research
