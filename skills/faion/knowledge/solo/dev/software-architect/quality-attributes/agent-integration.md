# Agent Integration — Quality Attributes Framework

## When to use
- Drafting NFRs (non-functional requirements) before any architecture work — turn fuzzy "must be fast / secure / reliable" into measurable scenarios with response-measure targets.
- Pre-design phase of a new feature/service: produce a quality-attribute utility tree to drive style + tech choices.
- Architecture review of an existing system: score it against ISO/IEC 25010 characteristics, locate degraded attributes.
- Defining SLI/SLO/SLA pyramid for a service the team is about to operationalize.
- Setting alert thresholds: response measures from QA scenarios convert directly to Prometheus rules and PagerDuty policies.
- Trade-off analysis (ATAM-light) when two architectural approaches both look reasonable.

## When NOT to use
- One-off internal scripts and PoCs — full QA scenarios are bureaucratic theater for code that won't run a week.
- After-the-fact for a system already in production with stable SLOs and existing dashboards — reverse-engineering NFRs adds little.
- Micro-decisions inside a single function (algorithm choice, library swap) — use perf benchmarks, not utility trees.
- When stakeholders cannot supply numeric targets and refuse to commit; vague QAs ("should be reliable") are worse than none — they signal false rigor.

## Where it fails / limitations
- **Number theater:** teams write "p95 < 200ms" with no measurement plan. Without an SLI pipeline the number is decorative.
- **Missing trade-offs:** QA docs list 12 desired attributes as if all are top priority. CAP / latency vs durability / security vs UX conflicts get hand-waved.
- **Static drift:** ISO 25010 categories don't auto-update with deployment changes. After a Kubernetes migration, portability/maintainability targets often invalidate silently.
- **Cost-blind:** the framework rarely asks "what does +1 nine of availability cost?" — leads to over-engineering.
- **6-part scenarios are heavy:** for a solo founder, 60% of the value comes from {stimulus, response measure}. The rest is filler.
- **AI fabrication risk:** LLMs happily emit p99 = 50ms targets they cannot justify. Always require a measurement source.

## Agentic workflow
Run a four-pass pipeline: (1) extractor agent reads spec/PRD and proposes a utility tree of QAs ranked by business impact; (2) scenarist agent expands the top 8–12 nodes into 6-part QA scenarios with concrete response measures; (3) tactic agent maps each scenario to architectural tactics from `README.md` (caching, redundancy, circuit breakers, etc.) and warns about conflicts; (4) SLO-bridge agent converts the highest-priority scenarios into SLI definitions + Prometheus rules + alert routes. Persist as `.aidocs/product_docs/quality-attributes.md` and re-run pass (1) on every spec change.

### Recommended subagents
- `faion-research-agent` (`skills/faion/knowledge/pro/research/researcher/`) — sources comparable industry SLOs (e.g., what Stripe/Shopify publish for similar services) so targets are not invented from scratch.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — convert each accepted scenario into a `todo/` task with the response measure as the acceptance criterion.
- A purpose-built **utility-tree agent** (worth creating): single job is to take a service description and emit the ATAM utility tree as YAML — easier to diff than prose.
- A **trade-off red-team agent**: re-prompt with "given these 12 QAs, list every conflict and the cheapest tactic for each side." Forces explicit prioritization.

### Prompt pattern
Extraction:
```
You are an architect. From the spec in <spec>, produce a quality-attribute
utility tree (ISO/IEC 25010). For each leaf write a 6-part scenario:
source, stimulus, environment, artifact, response, response measure.
Numeric targets only — reject vague verbs. If the spec lacks data,
emit "MISSING: <what to ask>" instead of inventing.
```

Tactic mapping:
```
For each scenario in <utility-tree.yaml>, recommend 1–3 architectural
tactics from quality-attributes/README.md. For every tactic list one
attribute it improves and one attribute it likely degrades. Output as
markdown table with columns: scenario_id, tactic, +attr, -attr, cost_tier.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `k6` | Load test against latency/throughput targets in QA scenarios | https://k6.io |
| `Locust` | Python-driven load testing, easy to script from agent | https://locust.io |
| `Apache JMeter` | Heavy mixed-protocol perf testing | https://jmeter.apache.org |
| `OWASP ZAP` (`zap-baseline.py`) | Headless security scan against confidentiality/integrity scenarios | https://www.zaproxy.org |
| `Trivy` | CVE scan for security QA — agent-callable | https://trivy.dev |
| `slo-generator` (Google) | Convert SLO YAML to Prometheus rules | https://github.com/google/slo-generator |
| `pyrra` | SLO management on Prometheus | https://github.com/pyrra-dev/pyrra |
| `Sloth` | Generate Prometheus SLO rules from spec | https://sloth.dev |
| `Chaos Mesh` / `Litmus` | Validate availability/reliability scenarios via fault injection | https://chaos-mesh.org |
| `claude` (Anthropic CLI) | Run extraction + scenarist passes headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Datadog | SaaS observability | API yes | Best end-to-end SLI/SLO+alerting for a solo team; expensive at scale. |
| Grafana Cloud + Mimir/Loki/Tempo | SaaS / OSS | API yes | OSS-friendly, agents can push metrics + alert rules via Terraform provider. |
| Honeycomb | SaaS observability | API yes | Best-in-class for SLO debugging via BubbleUp; query API is agent-driven. |
| Nobl9 | SaaS SLO platform | API yes | Pure SLO-as-code; ingests SLI from Datadog/Prometheus/etc. |
| Sentry | SaaS APM/errors | API yes | Maps directly to reliability/maintainability QA scenarios. |
| AWS CloudWatch + X-Ray | SaaS | API yes | Default for AWS-heavy stacks; QA scenarios → metric filters + composite alarms. |
| OpenTelemetry Collector | OSS | yes | Vendor-neutral pipeline; agents can reconfigure via OTAP/Helm. |
| Architecture-Tradeoff-Analysis-Method (ATAM) workshops | n/a | n/a | Methodology, not SaaS — use for QA prioritization meetings. |
| arc42 quality.arc42.org | OSS docs | n/a | Free QA tree templates; pair with utility-tree agent. |

## Templates & scripts

`templates.md` ships QA scenario, NFR spec, SLO doc, and alert templates. The gap is auto-conversion of QA scenarios → SLO YAML. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# qa2slo.sh — extract response-measure rows from QA markdown and emit slo-generator YAML.
# Usage: qa2slo.sh quality-attributes.md > slo.yaml
set -euo pipefail
in=${1:?"usage: qa2slo.sh <qa.md>"}
awk '
  /^### Scenario / { sid=$3; gsub(/[^A-Za-z0-9_-]/,"",sid) }
  /^- \*\*Response Measure:\*\*/ {
    sub(/^- \*\*Response Measure:\*\*[[:space:]]*/, "");
    print "spec:"
    print "  service: \"unknown\""
    print "  description: \"" $0 "\""
    print "  indicator:"
    print "    metadata: { name: " sid " }"
    print "    spec:"
    print "      service: unknown"
    print "      description: \"derived from QA scenario " sid "\""
    print "    # TODO: fill SLI ratio_metrics.good/total queries"
    print "  objectives:"
    print "    - displayName: \"" sid "\""
    print "      target: 0.99"
    print "      window: 30d"
    print "---"
  }
' "$in"
```
Pipe into `slo-generator generate` to materialize Prometheus rules.

## Best practices
- Refuse any QA without a numeric response measure. Treat "fast", "scalable", "secure" as bugs in the spec.
- Tie every accepted scenario to (a) a deployed SLI and (b) one architectural tactic. Orphan scenarios rot.
- Cap utility tree at ~12 leaves for solo/small teams. Beyond that, prioritization is fiction.
- Track cost-of-tactic alongside benefit. "Multi-region failover" without a $/month line is wishful thinking.
- Re-score the tree on every quarterly review and after any P1 incident — incident postmortems are the cheapest source of missing scenarios.
- Pair QA scenarios with ADRs: each accepted scenario links to the ADR that locked in the tactic.

## AI-agent gotchas
- LLMs invent precise numeric targets ("p99 < 87ms") with no evidence — pin a rule that any number must come from a benchmark, comparable system, or explicit user input.
- Don't let a single agent both propose and accept QAs. Use a separate critic pass; otherwise it self-confirms.
- Architectural tactics suggested by an LLM tend to compound complexity (microservices + service mesh + saga + event sourcing for a CRUD app). Add a "simplest tactic that meets the measure" instruction.
- Trade-off detection is weak in single-shot prompts; force a structured matrix output (`+attr / -attr / cost_tier`) so conflicts become visible.
- Long QA documents blow context windows. Stream in by characteristic (performance → security → maintainability), then merge.
- Human-in-loop checkpoints: (1) before the utility tree is frozen, (2) before tactics are turned into ADRs, (3) before SLO targets are sent to alerting — these are irreversible without org pain.

## References
- ISO/IEC 25010:2023 — https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
- SEI Quality Attribute Workshop — https://www.sei.cmu.edu/library/quality-attribute-workshop-qaw-third-edition/
- ATAM (Architecture Tradeoff Analysis Method) — https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/
- Google SRE Book, ch. 4 (SLO) — https://sre.google/sre-book/service-level-objectives/
- arc42 Quality Model — https://quality.arc42.org/standards/iso-25010
- Sloth SLO generator — https://sloth.dev
- Pyrra — https://github.com/pyrra-dev/pyrra
- Local methodology: `quality-attributes/README.md`, `templates.md`, `examples.md`
