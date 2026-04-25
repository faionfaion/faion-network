# Agent Integration — Funnel Optimization Framework

## When to use
- Standing up funnel analysis from zero: defining steps, instrumenting events, computing step-to-step conversion, finding the biggest drop.
- Producing a structured "Funnel Analysis" document that captures definition, current performance, biggest leaks, diagnosis, hypotheses, ICE-scored test plan.
- Running weekly/monthly funnel reviews via the included checklist; need a deterministic process other agents can call.
- Diagnosing a single drop-off step with the README's combined methods (session recordings, heatmaps, surveys, interviews, segment analysis).

## When NOT to use
- Tactic catalog or quick wins (route to `funnel-tactics-basics`).
- Industry/personalization playbooks (route to `funnel-tactics-advanced`).
- Worked examples or benchmark lookup (route to `funnel-basics-examples`).
- Strategy/PLG-model questions (route to `plg-basics`).

## Where it fails / limitations
- The framework assumes you can attribute users across steps (consistent IDs, deterministic events). Fragmented identity (cookieless, anon → identified) breaks the math; agents must validate ID stitching first.
- "Biggest drop" prioritization underweights downstream value; a 50% drop at "viewed pricing" can be less critical than a 10% drop at "added card" if customer LTV concentrates at the bottom. Agents should also report "users-lost-weighted-by-LTV".
- The ICE 1–10 scoring is subjective; without anchoring rubrics, two agents will produce different scores for the same hypothesis. Pin the rubric.
- Common-cause table is a heuristic — real causes need recordings + interviews; agents must not finalize a diagnosis from analytics alone.

## Agentic workflow
A funnel-framework agent runs as a 7-step pipeline aligned with the README's process: `funnel-mapper` writes the step + event spec, `funnel-instrumenter` adds events + verifies in dev, `funnel-analyzer` pulls 30-day data and produces the conversion table, `leak-prioritizer` ranks drops by absolute and LTV-weighted loss, `diagnosis-runner` orchestrates session-recording / heatmap / survey reads to compose root-cause notes, `hypothesis-generator` emits ICE-scored hypotheses using the README's IF/THEN/BECAUSE template, `test-planner` queues experiments. Outputs flow into `funnel-tactics-basics` and `funnel-tactics-advanced` agents for variant authoring.

### Recommended subagents
- `funnel-mapper` — input: product surface; output: ordered steps + event names matching the README's table format.
- `funnel-analyzer` — pulls cohort data from analytics (Mixpanel/Amplitude/PostHog), emits the README's conversion + drop-off table.
- `leak-prioritizer` — scores leaks by absolute users lost AND LTV-weighted lost revenue.
- `diagnosis-runner` — composes Hotjar session-recording summaries + heatmap top-clicks + survey responses into a root-cause note.
- `hypothesis-generator` — emits 3–5 IF/THEN/BECAUSE hypotheses scored with ICE.
- `test-planner` — turns hypotheses into experiment specs with sample size + duration.

### Prompt pattern
```
You are funnel-analyzer. Read knowledge/pro/marketing/conversion-optimizer/funnel-basics-framework/README.md.
Input: { funnel_id, lookback_days: 30, segment_filters: {...} }.
Output JSON matching README's "FUNNEL ANALYSIS" table:
{ steps: [{ step, name, users, conversion_pct, drop_pct }], overall_conversion: 0.XX,
  biggest_leaks: [{ step_pair, users_lost, pct_of_total }] }.
```

```
You are hypothesis-generator. Given the leak step + diagnosis_notes, output 3–5 hypotheses
following: "IF we [change X] THEN [metric] will improve by [Y%] BECAUSE [reason]".
Each gets an ICE entry { impact: 1-10, confidence: 1-10, ease: 1-10, total }.
Anchor confidence to evidence type: own A/B win=9, peer case study=7, framework heuristic=5, intuition=3.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mixpanel` JQL | Cohort + funnel computation | https://developer.mixpanel.com/reference/jql-overview |
| `amplitude` Funnel + Cohort APIs | Funnel pulls, segment slicing | https://www.docs.developers.amplitude.com/analytics/apis/ |
| `posthog` SQL / Insights API | OSS option, full programmatic funnel | https://posthog.com/docs/api |
| `dbt` + warehouse SQL | Funnel as derived models, repeatable + version-controlled | https://docs.getdbt.com/ |
| `hotjar` API | Pull session-recording metadata + survey responses | https://developers.hotjar.com/ |
| `playwright` / `puppeteer` | Reproduce drop-off steps to verify event firing | https://playwright.dev/ |
| `optimizely` / `growthbook` | Wire experiments derived from hypotheses | https://docs.growthbook.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Mixpanel | SaaS | Yes — JQL + Insights | Best for ad-hoc funnel + segment slicing |
| Amplitude | SaaS | Yes | Strong cohort + behavioral analysis |
| PostHog | OSS + SaaS | Yes | Funnel + flags + recordings in one — ideal for agents |
| Hotjar / FullStory / LogRocket | SaaS | Partial | Recordings + heatmaps for diagnosis step |
| Crazy Egg | SaaS | Partial | Heatmaps |
| Heap | SaaS | Yes — autotrack reduces instrumentation effort | Good when steps are unclear up-front |
| Typeform / Hotjar surveys | SaaS | Partial | Exit-intent surveys for qualitative diagnosis |
| Optimizely / VWO / GrowthBook | SaaS / OSS | Yes | Experiment execution from hypotheses |

## Templates & scripts
The README itself includes the canonical "Funnel Analysis" and "Weekly Funnel Review" templates — agents fill these in. Inline LTV-weighted leak scorer:

```python
# weighted_leaks.py — extend README's drop-off table with LTV weighting
from dataclasses import dataclass

@dataclass
class StepDrop:
    step_pair: str
    users_lost: int
    downstream_ltv: float   # avg LTV of users who pass this step

    @property
    def lost_value(self) -> float:
        return self.users_lost * self.downstream_ltv

def prioritize(drops: list[StepDrop]) -> list[StepDrop]:
    return sorted(drops, key=lambda d: d.lost_value, reverse=True)

# Use BOTH README's "users lost %" AND LTV-weighted ranking; report both columns.
```

See `templates.md` (full Analysis + Review template) and `examples.md` in this directory.

## Best practices
- Run the full 7-step process; don't jump to hypotheses without a diagnosis. The README's "Guessing causes" mistake is the #1 agent failure mode.
- Always segment: mobile vs desktop, new vs returning, traffic source. The framework explicitly warns against ignoring segments.
- Anchor ICE confidence scores to evidence type (own data, peer case study, framework heuristic, intuition); without this, scores degenerate.
- Pair every leak with both absolute users-lost AND LTV-weighted loss; the README only shows the first column — extend it.
- Run weekly funnel review on a fixed cadence using the included checklist; treat it as a stand-up artifact.
- For diagnosis, require ≥3 independent signals (e.g., recordings + survey + analytics segment) before locking a root cause.
- Wait for statistical significance before declaring a test winner — the README's "No statistical significance" mistake is a hard rule.

## AI-agent gotchas
- Agents will conflate correlation with causation in diagnosis — the survey-says-X result rarely matches the recording-shows-Y reality. Force triangulation.
- Hypothesis generator will produce vague IF/THEN statements ("improve UX → conversion goes up"). Reject hypotheses that don't name a specific UI change AND a specific metric AND a specific lift band.
- ICE scoring drift across runs: lock the rubric inside the system prompt and surface the rubric in the output JSON for audit.
- Funnel definitions silently change when product evolves; agent should fail loud if events on which past funnels relied have been renamed/removed.
- Weekly review checklist is easy to auto-fill with stale data; require freshness check (data lag < 24h) before publishing.
- Don't auto-commit instrumentation events to production — the agent emits a PR, a human reviews schema + privacy impact.
- Funnel pulls without a cohort lookback control will compare apples to oranges (campaign mix shifts). Force a fixed-cohort window per analysis.

## References
- `README.md` (this directory)
- Mixpanel funnel-analysis guide — https://mixpanel.com/topics/funnel-analysis/
- Amplitude conversion-funnel analysis — https://amplitude.com/blog/conversion-funnel-analysis
- Reforge retention-engagement-growth framework — https://www.reforge.com/blog/retention-engagement-growth-framework
- Optimizely funnel glossary — https://www.optimizely.com/optimization-glossary/funnel-analysis/
- Heap funnel analytics primer — https://heap.io/topics/what-is-funnel-analysis
