# Agent Integration — A/B Testing Basics

## When to use
- You're starting an experimentation practice and need agents to enforce a hypothesis → design → analyze → decide loop.
- You have ≥1k weekly events on the metric of interest and a clear single change to evaluate.
- Decisions are reversible and the cost of being wrong is low (UI copy, layout, prompts) — perfect A/B turf.
- You want an agent to standardize hypothesis cards across a team so tests stay comparable.

## When NOT to use
- Strategic choices (pricing model, positioning, brand) — too few decisions, too noisy, A/B is the wrong frame.
- Network-effect products where treatment leaks into control (Slack workspaces, marketplaces) — use cluster-randomized or switchback designs.
- Tiny traffic (<100 users/day on the test surface) — the wait time exceeds product-iteration cadence; use qualitative + judgment.
- Highly personalized experiences where every user already gets a different variant.
- Big-bang changes (full redesign) — too many confounders; ship behind a feature flag with a phased rollout instead.

## Where it fails / limitations
- Peeking + early stopping inflates false positives 5-10x; agents that "check daily and call it" produce garbage results.
- Multiple-comparison creep: once you start testing 5 metrics × 3 segments, your real false-positive rate is way above 5%.
- Novelty/primacy effects bias short tests; ship-then-iterate decisions on 3-day tests are unreliable.
- Sample-ratio mismatch (SRM) in traffic split silently invalidates tests — must be checked before any analysis.
- Guardrail metrics regress while primary wins — agents focused on a single metric ship Pyrrhic victories.
- Simpson's paradox in segmented analysis; aggregate winners can be losers per-segment.

## Agentic workflow
An `opus` design agent writes the hypothesis card (if/then/because, primary metric, MDE, sample size, end date) and runs a pre-launch checklist (SRM monitor configured, guardrails defined, no overlapping test). A `sonnet` analyst computes results once the test ends, including SRM check, primary, secondary, and guardrails. An `opus` reviewer makes the ship/kill/retest call and writes the learning summary into the experiment log.

### Recommended subagents
- `faion-growth-agent` (opus) — hypothesis design + ship/kill decisions.
- `faion-conversion-optimizer` agent — surface area selection, copy variants.
- Stats subagent (sonnet) — significance test, CI, SRM check.
- Logger/haiku subagent — append result row to a versioned `experiments.md` log.

### Prompt pattern
```
Draft an A/B test card for: surface={surface}, change={change}.
Format: hypothesis (if/then/because), primary metric, MDE relative,
sample-per-variant, duration days, guardrails (3), kill criteria.
Refuse if MDE is missing or primary metric isn't tied to a business
outcome.
```

```
Test ended with: A n=50000 x=2200; B n=50000 x=2380. Compute SRM
(expected 50/50), z-test for primary, CI. Guardrails: bounce_rate
A=42% B=44%, retention_d7 A=18% B=18.2%. Recommend ship/kill/iterate
with one paragraph reasoning.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `scipy.stats` / `statsmodels` | proportions_ztest, chi-square SRM | `pip install scipy statsmodels` |
| `abracadabra` (Square OSS) | Frequentist + Bayesian A/B in one API | `pip install abracadabra` |
| `expan` (Zalando OSS) | Experiment analysis library | `pip install expan` |
| `feature-flags` SDKs (LaunchDarkly, Statsig, Flagsmith, GrowthBook, Unleash) | Run experiments programmatically | language-specific SDKs |
| Evan Miller calculators | Manual cross-check of agent's math | https://www.evanmiller.org/ab-testing/ |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Statsig | SaaS | Yes (REST + SDK) | Sequential testing, CUPED, console API |
| GrowthBook | OSS | Yes (REST + self-host) | Bayesian default, agent-readable |
| Eppo | SaaS | Yes (REST) | Warehouse-native (BigQuery/Snowflake) |
| LaunchDarkly | SaaS | Yes (REST) | Feature flags + experiments |
| Optimizely Web/Full Stack | SaaS | Partial | Mature; API exists, agent UX heavier |
| VWO | SaaS | Partial | Bayesian engine, REST API |
| Convert.com | SaaS | Yes | Privacy-friendly alternative |
| PostHog Experiments | OSS | Yes (REST) | Bundled with product analytics |

## Templates & scripts
See `templates.md` for hypothesis cards and result tables. Inline pre-launch checklist (agent enforces):

```python
# pretest_check.py — agent runs before launch
def can_launch(card: dict) -> tuple[bool, list[str]]:
    fails = []
    if not card.get("hypothesis_if_then_because"):
        fails.append("missing if/then/because")
    if not card.get("primary_metric"):
        fails.append("no primary metric")
    if not card.get("mde_relative"):
        fails.append("no MDE")
    if card.get("sample_per_variant", 0) < 1000:
        fails.append("sample <1000/variant — underpowered")
    if not card.get("guardrails"):
        fails.append("no guardrail metrics")
    if not card.get("end_date"):
        fails.append("no pre-committed end date")
    if card.get("overlaps_with_active_test"):
        fails.append("overlaps with active test on same surface")
    return (len(fails) == 0, fails)
```

## Best practices
- Pre-register: hypothesis, primary metric, sample size, end date — committed BEFORE traffic flows.
- Always include a sample-ratio mismatch check; if observed split deviates from expected (chi-square p<0.001), invalidate the test.
- Pick ONE primary metric. List secondaries explicitly as "watch only" — they cannot win or lose the test alone.
- Run for at least one full business cycle (typically 1-2 weeks) to absorb day-of-week effects.
- Maintain an experiment log (markdown or Notion) with every test, hypothesis, result, and learning — agents should read it for prior patterns.
- Treat 0.05 < p < 0.10 results as "no result" + "need more data," not as "almost wins."
- Ship with a phased rollout (10% → 50% → 100%) even after a clear win, so you catch regressions in production.

## AI-agent gotchas
- Agents will happily run "directional reads" on under-powered tests; force a minimum-sample gate.
- "Statistical significance" framed as "X% chance B is better" is wrong (frequentist) — require correct phrasing in output.
- Multiple-test fishing: agent runs the same test on 6 metrics and picks the winner — explicit Bonferroni or pre-registered primary required.
- Treatment leakage in social/marketplace products: agent must check whether users in A interact with users in B.
- Date-range bugs are frequent — agent must not include partial first/last days that contain ramp-up traffic.
- Environment-specific bugs: agent runs analysis on dev events; force property/environment scoping.
- LLMs sometimes invent p-values that look reasonable when called without raw counts — always demand n1, x1, n2, x2.

## References
- Ron Kohavi, Diane Tang, Ya Xu, *Trustworthy Online Controlled Experiments*
- Sean Ellis & Morgan Brown, *Hacking Growth*
- Microsoft ExP team papers — https://www.exp-platform.com/Pages/papers.aspx
- Statsig blog (CUPED, sequential) — https://statsig.com/blog
- Evan Miller, "How Not to Run an A/B Test" — https://www.evanmiller.org/how-not-to-run-an-ab-test.html
