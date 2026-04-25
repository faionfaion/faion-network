# Agent Integration — Conversion Rate Optimization (CRO)

## When to use
- Established traffic with under-converting funnels (landing → signup, pricing → trial, checkout → purchase).
- A/B testing program with enough volume per variant (≥100 conversions/variant, 2+ weeks duration).
- Form, pricing, or onboarding redesign where research-driven hypotheses outperform opinion-driven changes.
- Quarterly CRO program reviews where wins, losses, and learnings need a librarian.
- Multi-page funnel diagnosis using heatmaps + session recordings + form analytics + exit surveys together.

## When NOT to use
- Low-traffic sites (under ~5k unique visitors/page/month) where statistical significance is unreachable; do qualitative research instead.
- Pre-PMF startups: optimizing the wrong funnel; first nail the message-market fit, then convert.
- Stable, mature funnels with sub-1% lift potential; resources better spent on traffic acquisition or new product.
- Major redesigns: do user research and prototype, not A/B tests.
- Compliance-heavy flows (KYC, medical) where CRO levers conflict with required disclosures.

## Where it fails / limitations
- Stopping tests early ("we have a winner!") at ~80% confidence inflates false-positive rate dramatically.
- Single-test-at-a-time fundamentalism is wrong at scale; mature programs use multivariate / orthogonal tests with proper interaction analysis.
- "Best practices" copied from case studies (urgency timers, social proof above fold) often fail to replicate without local research.
- Heatmap-only research surfaces clicks but not intent; pair with session recordings and surveys to triangulate.
- Test pollution: cross-test contamination, bot traffic, and consent banners that break tracking are common silent killers.
- Winners often regress 30+ days post-launch — declare a "holdback" cell to monitor durability.

## Agentic workflow
A Claude subagent is most useful at three points: (1) reading raw research artifacts (heatmap exports, session recording transcripts, support tickets) and synthesizing the top 10 friction hypotheses; (2) generating PIE/ICE-scored test backlogs from those hypotheses; (3) writing the post-test learning library entry with proper framing of what generalizes vs what does not. Do not let the agent run statistical analysis in production — use proper experimentation tools (Optimizely, GrowthBook) and treat the agent's reading of results as a draft.

### Recommended subagents
- `faion-growth-agent` (referenced in README) — sonnet for hypothesis ideation and prioritization; opus for funnel-wide strategy and confounded-test diagnosis.
- A `cro-research-agent` (suggested) — sonnet for synthesizing qual + quant; haiku for tagging support tickets by friction theme.
- `faion-sdd-executor-agent` — model each test as an SDD task with hypothesis, design, gate, learnings.

### Prompt pattern
```
Synthesize 10 friction hypotheses from <heatmap.csv>, <session-quotes.md>,
<exit-survey.csv>. Each hypothesis = { observation, why-it-matters,
proposed-fix, PIE score, expected lift band }. Cite source line for every
observation. Reject any hypothesis that cannot be cited.
```

```
Given test result <stats>: control 4.2% (n=12,400), variant 4.8% (n=12,310),
duration 18 days, 95% one-sided. Decide: ship / not-ship / extend. List
3 secondary metrics to verify before shipping. Draft a learning-library
entry: hypothesis, change, result, what generalizes, what does not.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `growthbook` (CLI/SDK) | Open-source feature flags + experiments | https://www.growthbook.io/ |
| `posthog-cli` | Query experiments / funnels | https://posthog.com/docs/cli |
| `evan-miller-tools` | A/B sample size + duration calculators (web) | https://www.evanmiller.org/ab-testing/sample-size.html |
| `dbt` | Materialize experiment exposure tables | https://docs.getdbt.com/ |
| `pandas` / `scipy` | Significance + power analysis in notebooks | https://scipy.org/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Optimizely | SaaS | Yes (API) | Enterprise A/B + personalization |
| VWO | SaaS | Yes (API) | Mid-market A/B + heatmaps in one |
| GrowthBook | OSS + SaaS | Yes (API) | OSS feature flags + experiments; warehouse-native |
| Statsig | SaaS | Yes (API) | Feature flags + experimentation, generous free tier |
| LaunchDarkly | SaaS | Yes (API) | Flags first, experiments via add-on |
| Hotjar | SaaS | Yes (API) | Heatmaps + recordings + surveys |
| FullStory | SaaS | Yes (API) | Session recordings + frustration signals |
| Microsoft Clarity | SaaS (free) | Partial | Free heatmaps + recordings |
| Maze | SaaS | Yes (API) | Unmoderated usability testing |
| Typeform | SaaS | Yes (API) | Exit and satisfaction surveys |

## Templates & scripts
See `templates.md` for CRO audit and A/B test brief. Inline sample-size sanity check (binary metric):

```python
# sample_size.py — minimum sample per arm for binary conversion test.
# Two-sided, 95% confidence, 80% power, equal allocation.
import math
def n_per_arm(p1: float, mde_rel: float) -> int:
    p2 = p1 * (1 + mde_rel)
    p_bar = (p1 + p2) / 2
    z_a, z_b = 1.96, 0.84  # 95% / 80%
    num = (z_a * math.sqrt(2 * p_bar * (1 - p_bar))
           + z_b * math.sqrt(p1*(1-p1) + p2*(1-p2))) ** 2
    return math.ceil(num / (p2 - p1) ** 2)
print(n_per_arm(0.04, 0.10))  # 4% baseline, +10% MDE
```

## Best practices
- Research before testing. Run 5 user interviews + 50 session recordings before writing the first hypothesis.
- Test big swings, not pixels. Headline + value-prop changes outperform button color 100:1 over a year.
- Pre-register every test: hypothesis, primary metric, MDE, duration, decision rule. Variances after the fact = false positives.
- Run a holdback cell (95% rollout) for 30 days post-ship to catch novelty regressions.
- Maintain a learning library indexed by hypothesis type and audience segment; reuse failed tests' learnings before re-running.
- Sequence funnel work top-down: fix bounce on landing before optimizing form completion. Fixing leaks downstream of a leak is wasted budget.
- Keep traffic assignment idempotent (hashed user-id), not session-based, or your variants pollute.

## AI-agent gotchas
- LLMs are confidently wrong on statistical claims. Force the agent to cite a sample-size calculator output rather than infer significance.
- "Best practice" recommendations are anti-research. Constrain the agent to cite the specific user-research artifact behind every recommended change.
- Heatmap interpretations from images are unreliable; require structured data (event counts, scroll-depth percentiles) instead.
- The agent will copy hypotheses from training data; force novel hypotheses tied to the local site's friction language ("users said X").
- Test pollution detection (consent banner blocks, bot traffic) is hard for the model — supply the exposure logs and ask explicitly.
- Multi-armed bandit reasoning is shaky in LLMs; use a proper bandit library, treat agent only as a narrator of results.
- Privacy: session recording transcripts often include PII; redact before passing to any LLM endpoint.

## References
- ConversionXL, "What is CRO" — https://conversionxl.com/blog/what-is-conversion-rate-optimization/
- Optimizely, "A/B testing best practices" — https://www.optimizely.com/optimization-glossary/ab-testing/
- Unbounce, "Conversion Benchmark Report" — https://unbounce.com/conversion-rate-optimization/conversion-benchmark-report/
- WiderFunnel, "PIE prioritization framework" — https://www.widerfunnel.com/pie-framework/
- Hotjar, "Heatmaps + recordings playbook" — https://www.hotjar.com/conversion-rate-optimization/
- GrowthBook docs — https://docs.growthbook.io/
- Evan Miller, "How not to run an A/B test" — https://www.evanmiller.org/how-not-to-run-an-ab-test.html
