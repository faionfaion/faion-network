# Agent Integration — Success Metrics Definition

## When to use
- Setting up KPIs for a new product, feature, or campaign before launch.
- Re-baselining metrics quarterly when business goals shift.
- Onboarding a new team and aligning on a single North Star.
- After noticing the team optimizes for vanity numbers (signups, page views).

## When NOT to use
- During exploratory pre-PMF work — set qualitative milestones, not KPIs.
- For one-off experiments — use a single success criterion, not a full AARRR scaffold.
- When data infrastructure is missing; defining metrics without instrumentation creates aspirational dashboards.
- For purely creative/editorial work where the metric becomes a distorting incentive.

## Where it fails / limitations
- North Star chosen for measurability rather than truth (e.g., "page views" instead of "successful task completions") drives the wrong behavior.
- Goodhart's law: any metric that becomes a target stops being a good metric. Always define guardrails.
- AARRR is funnel-shaped — bad fit for cyclical / habit products; consider HEART, RICE, or ICE for those.
- Targets set without a baseline are theatrical; agents will pick round numbers (10%, 20%) that aren't grounded.
- B2B and marketplace metrics need segmentation by tier/cohort; a single MAU number hides churn.

## Agentic workflow
Decompose business goals into a metric tree: Goals → North Star → AARRR primary KPIs → leading indicators + guardrails. Each node is JSON with {definition, formula, source, baseline, target, owner}. Run a separate agent pass to detect vanity-metric patterns and Goodhart traps. Final tree is reviewed by a human; the agent never owns the target number.

### Recommended subagents
- `metric-tree-builder` (sonnet) — decomposes goals into AARRR + guardrails using structured output.
- `vanity-detector` (haiku) — flags metrics where actionability fails the "would we change behavior?" test.
- `target-grounder` (sonnet) — pulls baselines from analytics + benchmark data and proposes ranges, never single numbers.
- `faion-sdd-executor-agent` to lifecycle the metrics framework as a living spec.

### Prompt pattern
```
Role: metric-tree-builder.
Input: business_goals.md, product_type ("saas|marketplace|consumer|media").
Output JSON: {north_star:{name, definition, rationale},
              aarrr:{acquisition:[...], activation:[...], retention:[...], revenue:[...], referral:[...]},
              guardrails:[{metric, threshold, action}]}.
Constraint: max 5 primary KPIs total. Refuse output if North Star fails actionability test.
```

```
Role: vanity-detector.
Input: metric_tree.json.
Task: for each metric, answer "if value drops 50%, what action?"; if "none/notify only", flag as vanity.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt` | Define metric models versioned in git | https://docs.getdbt.com |
| `sqlfluff` | Lint metric SQL definitions | https://sqlfluff.com |
| `cube-cli` | Cube.dev semantic layer for metric definitions | https://cube.dev |
| `metricflow` | Metric definitions framework (Transform→dbt) | https://docs.getdbt.com/docs/build/metricflow-commands |
| `posthog` API | Pull baselines for funnel + retention | https://posthog.com/docs/api |
| `plausible` API | Privacy-friendly traffic baselines | https://plausible.io/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Cube.dev | OSS+Cloud | Yes (REST/GraphQL) | Define metrics once, query everywhere; agent-friendly schema. |
| dbt + dbt Semantic Layer | OSS+Cloud | Yes (CLI + API) | Versioned metric definitions in git. |
| Statsig | SaaS | Yes (API) | A/B + holdouts; pulls metric impact per experiment. |
| Mixpanel | SaaS | Yes (API) | AARRR funnels; agent reads baselines to suggest targets. |
| Amplitude | SaaS | Yes (API) | North Star + retention curves; better for product-led growth. |
| PostHog | OSS+Cloud | Yes (API) | Self-hosted alternative with funnels + cohorts. |
| Looker / Metabase | SaaS+OSS | Yes (Metabase API) | Dashboards rendered from metric tree. |
| Geckoboard | SaaS | Yes (API) | KPI displays; agent-pushed live numbers. |

## Templates & scripts
See `templates.md` for Metrics Framework and per-metric Specification.

Inline North Star sanity checker (Python, ≤30 lines):
```python
import json, sys
TESTS = [
    ("measures_core_value", "Does this metric move when users get value?"),
    ("leads_to_revenue", "Is this metric correlated with paid conversion?"),
    ("understandable", "Can you explain this in one sentence?"),
    ("actionable", "If it drops 20%, do we know what to do?"),
]
star = json.load(open(sys.argv[1]))  # {"name":..., "definition":...}
print(f"North Star: {star['name']}")
for key, q in TESTS:
    ans = input(f"{q} (y/n) ").strip().lower()
    if ans != "y":
        print(f"FAIL: {key} — reconsider North Star.")
        sys.exit(1)
print("OK: North Star passes 4-test check.")
```

## Best practices
- One North Star per product line, not per team. Multiple stars create ambiguity.
- Pair every primary KPI with a guardrail; e.g., growth (KPI) paired with churn (guardrail).
- Define metrics in a semantic layer (Cube/dbt) — single source of truth defeats dashboard drift.
- Set ranges, not single targets. "MRR $40-60k" is more honest than "$50k" and reduces sandbagging.
- Review the tree quarterly; retire metrics nobody asks about — dead metrics rot dashboards.
- Mark each metric Input vs Output; agents naturally over-weight outputs.

## AI-agent gotchas
- LLMs default to feature-style metrics (e.g., "feature X usage") instead of outcome metrics. Force the prompt to ask "what changed for the user?".
- Targets without baselines are hallucinated. Refuse target generation unless baseline is supplied.
- When asked for "industry benchmark", agents fabricate plausible percentages (e.g., "15% activation"). Require a citation URL.
- AARRR template completion is a haiku task; trade-off design ("revenue vs retention guardrails") is opus-grade.
- Human-in-loop checkpoints: (1) North Star choice, (2) target ranges sign-off, (3) guardrail thresholds.

## References
- Sean Ellis & Morgan Brown, "Hacking Growth" (North Star concept).
- Dave McClure, "AARRR Pirate Metrics" (2007 startup metrics talk).
- Goodhart, "Problems of Monetary Management" (1975) — the law.
- Google HEART framework: Happiness, Engagement, Adoption, Retention, Task success.
- Amplitude, "North Star Playbook" — free download with worked examples.
- John Cutler, "12 Signals" essay on outcome vs output metrics.
