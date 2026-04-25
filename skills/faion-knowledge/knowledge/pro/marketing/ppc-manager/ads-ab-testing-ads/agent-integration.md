# Agent Integration — A/B Testing Ads

## When to use
- Running a continuous test cadence (weekly / bi-weekly) across hooks, creatives, and offers with deterministic significance gates.
- Bulk-launching matched ad-set pairs (Control vs Variant) with identical audience, placement, optimization goal, and budget split.
- Maintaining a learning library: every test → result → learning row, surfaced to humans + future prompts.
- Coordinating cross-platform tests where the same hypothesis is tested simultaneously on Meta + Google with comparable success metrics.
- Auto-promoting winners (pause loser, scale variant, queue next test) once significance threshold reached.

## When NOT to use
- Daily/weekly conversion volume <100 per variant. Tests will never reach 95% confidence; ship the better-reasoned option and move on.
- Brand-new accounts with <30 days history. Algorithmic variance dominates creative variance; results are noise.
- Holiday peaks (BFCM, Q4 retail) — exogenous demand swamps treatment effect. Pause testing, run proven creatives.
- Tests where multiple variables changed (hook AND visual). Methodology requires single-variable tests; if business mandates compound, switch to multivariate / Bandit.
- Regulated verticals where ad copy needs legal review per variant — agent cannot self-approve, becomes a bottleneck.

## Where it fails / limitations
- Meta and Google's auto-optimization will reallocate spend mid-test, breaking the equal-split assumption. Methodology says "equal budget split" — only Meta's Experiments tool guarantees this; default ad-set rotation does not.
- "Stop early when significance hits" is a peeking error in classical NHST. Use sequential testing (mSPRT, Bayesian) or pre-commit to a sample size.
- Sample-size calculators assume one test at a time. Running 5 concurrent tests inflates false positives 5x without correction (Bonferroni or BH-FDR).
- Conversion metrics with long lag (B2B 30-90d) cannot be tested at ad level — by the time signal arrives, creatives are stale.
- Platform attribution windows differ (Meta 7d-click, Google 30d-click); naive cross-platform comparison fabricates lifts.

## Agentic workflow
The testing agent runs three roles: (1) test designer — reads a hypothesis backlog (YAML), checks prerequisites (budget, sample-size feasibility, no overlapping tests on same audience), and writes a test brief; (2) launcher — creates matched ad sets via Marketing API with locked parameters and a `test_id` tag; (3) analyst — pulls insights daily, computes significance using a pre-committed method (Bayesian or fixed-horizon), and emits a verdict report. Humans approve the brief and the verdict-to-promotion step. The agent never auto-promotes a winner without sign-off.

### Recommended subagents
- `faion-ads-agent` — Marketing API ad set / experiment CRUD.
- `faion-sdd-executor-agent` — wraps each test as an SDD task: spec (hypothesis + success metric), design (test parameters), test-plan (sample-size + significance method), implementation-plan (launch + monitor + verdict).
- `faion-brainstorm` — generates hypothesis backlog from past test learnings + competitor ad library scrape.

### Prompt pattern
```
Goal: design A/B test for hook variation on campaign C123.
Inputs: hypothesis, control creative, variant creative, primary metric, current baseline rate, MDE.
Validate: sample size feasible at current spend; no overlapping audience test running.
Output: test brief YAML matching templates.md schema; require human approval before launch.
```

```
Goal: compute verdict for test T42.
Method: Bayesian posterior of variant > control, decision rule P > 0.95.
Required data: 7-day insights, conversions per variant, exposures per variant.
Output: {winner, p_variant_better, lift, confidence, recommend_action} — never auto-promote.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `facebook-business` Python SDK | Meta Experiments API + matched ad set creation | `pip install facebook-business` — https://developers.facebook.com/docs/marketing-api/experiments |
| `google-ads-python` | Google Ads Experiments (campaign drafts) | `pip install google-ads` — https://developers.google.com/google-ads/api/docs/experiments/overview |
| `scipy.stats` / `statsmodels` | Frequentist significance, sample-size calc | `pip install scipy statsmodels` |
| `pymc` / `numpyro` | Bayesian A/B testing | `pip install pymc` |
| `growthbook` CLI | OSS A/B test platform with stats engine | https://docs.growthbook.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Experiments | First-party | Yes | Guaranteed equal split; supports A/B/n. ~$200/variant min. |
| Google Ads Experiments (campaign drafts) | First-party | Yes | Drafts + experiments via API; traffic split configurable. |
| GrowthBook | OSS | Yes | Self-host stats engine; integrates with warehouse for off-platform conversions. |
| Optimizely / VWO | SaaS | Partial | Mostly on-site testing; for ad creative use platform-native tools. |
| Statsig | SaaS | Yes | API-driven experimentation; usable for ad creative if event sync wired. |
| Optimizely Sample Size Calc | Free web | Read-only | Embed in agent prompts as a tool call URL. |

## Templates & scripts
Inline: Bayesian verdict for two-variant click test. Use after sample-size threshold reached.

```python
import numpy as np

def bayesian_ab(clicks_a: int, exp_a: int, clicks_b: int, exp_b: int, draws: int = 200_000) -> dict:
    # Beta(1,1) prior; conjugate update with binomial likelihood
    rng = np.random.default_rng(42)
    a = rng.beta(1 + clicks_a, 1 + exp_a - clicks_a, draws)
    b = rng.beta(1 + clicks_b, 1 + exp_b - clicks_b, draws)
    p_b_better = float((b > a).mean())
    lift = float(((b - a) / a).mean())
    return {
        "p_variant_better": round(p_b_better, 4),
        "expected_lift": round(lift, 4),
        "winner": "variant" if p_b_better > 0.95 else ("control" if p_b_better < 0.05 else "inconclusive"),
    }
```

See `templates.md` for the test brief and roadmap structures.

## Best practices
- Pre-register every test: hypothesis, sample size, primary metric, decision rule, stop date. No retroactive metric switching.
- Test offer > hook > creative > visual > CTA in that priority. Lower-impact tests rarely survive multiple-comparisons correction.
- Track holdout cells (5-10% of spend) on proven creatives to detect platform-wide drift versus test-specific regression.
- Keep a tests registry table: `(test_id, hypothesis, control_id, variant_id, status, started_at, verdict, learning)`. Feed it back into the brainstorm loop.
- Use platform-native experiment tools (Meta Experiments, Google campaign drafts) when budget allows — they enforce traffic split and prevent algorithmic peeking.
- Cap concurrent tests per audience to avoid overlap. A user in 3 tests at once is a confound, not a sample.

## AI-agent gotchas
- LLMs eagerly declare winners on small samples. Always require the agent to compute sample size first and refuse to verdict until threshold met.
- "Statistical significance" in Meta UI is not always the same metric as `scipy.stats.ttest_ind` on raw counts. Pin one stats engine and don't mix.
- When variant outperforms by >50%, suspect data leakage (audience overlap, tracking gap) before celebrating. Have agent run an integrity check (impression counts within 5% of expected split).
- Auto-promoting winners is dangerous: the variant might win on CTR but lose on CPA. Require multi-metric guardrails (no regression on secondary metric beyond X%).
- Agents tend to recreate a "test" each week even when last week's winner was inconclusive. Enforce: inconclusive tests extend, not restart.
- Cross-currency / cross-region tests need normalization. Agent must convert revenue to a base currency before computing ROAS lift.

## References
- https://developers.facebook.com/docs/marketing-api/experiments
- https://developers.google.com/google-ads/api/docs/experiments/overview
- https://www.evanmiller.org/sequential-ab-testing.html
- https://www.optimizely.com/sample-size-calculator/
- Kohavi, Tang, Xu — *Trustworthy Online Controlled Experiments* (book)
