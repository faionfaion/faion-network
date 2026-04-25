# Agent Integration — Product Discovery

## When to use
- Before committing engineering capacity to a new feature, product, or market segment.
- When a stakeholder request lacks evidence and you need a structured way to test the assumptions inside it.
- After analytics flags a divergence (drop-off, churn) and the team needs to identify root cause before solutioning.
- When entering an unfamiliar domain (new persona, new geography) and feasibility/value/usability/business risks are unknown.

## When NOT to use
- Pure execution work where the four risks (value, usability, feasibility, business viability) are already addressed.
- Time-bounded compliance / contractual deliverables — discovery cannot move the deadline.
- Trivial features (<2 days) where running an experiment costs more than building.
- When the team will not act on results — discovery without decision power is theatre.

## Where it fails / limitations
- Discovery becomes a permanent stalling phase ("we need more data") — set a hard timebox of 1–4 weeks.
- Skipping risk prioritisation: teams test easy assumptions instead of dangerous ones, missing the lethal risk.
- Confirmation bias: experiments designed to validate not falsify; agents are particularly susceptible.
- Survey-only discovery; users say one thing and do another. Always combine with behavioural evidence.
- Building during discovery — running prototype tests on production code defeats the cheap-fail principle.

## Agentic workflow
A risk-mapper agent reads the proposal and emits an assumption matrix tagging each by risk type (value/usability/feasibility/business) and severity. A method-picker agent matches each high-risk assumption to a discovery technique using the tables in `README.md`. An experiment-designer agent drafts hypothesis + method + success/kill criteria + sample size. After each experiment finishes, a synthesizer agent updates the matrix and recommends Proceed / Pivot / Kill / More Discovery. Humans run user-facing experiments and own the final go/no-go decision.

### Recommended subagents
- `faion-idea-generator-agent` — referenced in `README.md`; designs experiments and brainstorms tests.
- `faion-mvp-scope-analyzer-agent` — translates a "Proceed" decision into MVP scope.
- `faion-spec-reviewer-agent` — reviews experiment designs for falsifiability and ethical issues.
- `faion-task-creator-agent` — converts experiments into trackable backlog items with owners.

### Prompt pattern
```
System: You are a discovery risk mapper. Output JSON only.
For each assumption emit:
  {id, statement, risk_type: value|usability|feasibility|business,
   severity: lo|md|hi, falsifying_evidence_needed,
   recommended_method, est_effort: lo|md|hi}
Sort by (severity desc, est_effort asc). Reject lists where the top 3
  assumptions are not all severity=hi.
```

```
System: You are an experiment designer. For one assumption produce:
  {hypothesis: "If X then Y by Z%", method, audience, sample_n,
   duration_days, success_metric_threshold, kill_threshold,
   ethical_risks, prereq_data_setup}
Refuse to ship without explicit kill_threshold. n must be justified.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `posthog` API | Run feature flags + cohort experiments | https://posthog.com/docs/feature-flags |
| `growthbook` | OSS feature flagging + experimentation | https://github.com/growthbook/growthbook |
| `unleash` | OSS feature flag service | https://github.com/Unleash/unleash |
| `optimizely-cli` | Manage A/B tests programmatically | https://docs.developers.optimizely.com |
| `maze` API | Rapid prototype tests | https://maze.co/api |
| `userinterviews` API | Recruit participants programmatically | https://www.userinterviews.com/api |
| `whisper` (OpenAI) | Transcribe interview audio | https://github.com/openai/whisper |
| `dovetail` API | Push tagged research notes | https://developers.dovetail.com |
| `gsheets` (`gspread`) | Cheap experiment log | https://github.com/burnash/gspread |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Maze | SaaS | Yes (REST) | Unmoderated prototype + concept tests. |
| Useberry | SaaS | Yes (REST) | Cheaper Maze alternative. |
| User Interviews | SaaS | Yes (REST) | Recruitment for interviews. |
| Dovetail | SaaS | Yes (REST) | Synthesis + tagging. |
| Lookback | SaaS | Yes (REST) | Live moderated sessions; recordings via API. |
| GrowthBook | OSS | Yes (REST) | Self-host A/B + feature flag platform. |
| PostHog | OSS / SaaS | Yes (REST) | Analytics + experiments + feature flags. |
| Optimizely | SaaS | Yes (REST) | Enterprise A/B platform. |
| Typeform | SaaS | Yes (REST) | Quick concierge surveys / fake-door tests. |
| Carrd / Framer | SaaS | Yes (REST) | Stand up landing pages for value tests. |

## Templates & scripts
See `README.md` for Discovery Kickoff and Experiment Report templates. Inline gate that fails any experiment design without a kill threshold and proper sample-size justification:

```python
import math, sys, yaml
e = yaml.safe_load(open(sys.argv[1]))
errs = []
required = ["hypothesis","method","success_metric","success_threshold",
            "kill_threshold","sample_n","duration_days"]
for k in required:
    if not e.get(k): errs.append(f"missing field: {k}")
if e.get("success_threshold") == e.get("kill_threshold"):
    errs.append("kill_threshold must differ from success_threshold")
# sanity check sample size for proportion test (rough z-table at 95% power)
baseline = e.get("baseline_rate")
mde = e.get("min_detectable_effect")
if baseline and mde:
    n = math.ceil(16 * baseline*(1-baseline) / (mde**2))
    if e["sample_n"] < n:
        errs.append(f"sample_n {e['sample_n']} < required {n} for MDE {mde}")
if "interview" in e["method"].lower() and e["sample_n"] < 5:
    errs.append("qualitative interviews: minimum 5 participants per segment")
for x in errs: print("FAIL:", x)
sys.exit(1 if errs else 0)
```

## Best practices
- Map risks before designing experiments. Skipping the matrix leads to easy-but-irrelevant tests.
- Allocate 20–30% of total team capacity to discovery, not "leftover time".
- Combine methods to triangulate: interview signals + behavioural metric + a quantitative survey or fake-door test.
- Always set a kill threshold; an experiment without a failure condition cannot teach.
- Timebox each discovery cycle to 1–4 weeks; longer cycles signal scope creep.
- Document assumptions, evidence, and decisions in a single research repository (Dovetail, Notion). Discovery without memory repeats itself.
- Cheap to fail: prototypes over code, scripts over services, fakes over builds.
- Pair discovery with `mvp-scoping`: the MVP slice should aim to validate the next dangerous assumption, not ship a feature.

## AI-agent gotchas
- Agents proposing only happy-path validation; force a "design an experiment to falsify this" prompt variant.
- Hallucinated sample sizes ("100 users should be enough"). Demand a power-calculation justification or a published rule-of-thumb.
- LLMs cannot run interviews or read body language; treat their interview "synthesis" as theme extraction, never as conclusion.
- Confirmation bias loop: agent reads the proposal, generates "supportive" assumptions, then "validates" them. Inject a critic role.
- Without explicit ethics check, agents propose dark patterns (deceptive landing pages, hidden charges) — add a refusal clause for deceptive practices.
- Multi-experiment plans pile up; cap at 1–2 active experiments per discovery cycle, mark others "queued".
- Survey-bias inflation — agents recommend surveys for everything because they are cheap; require behavioural evidence as a tiebreaker.
- Token cost: a full assumption matrix + experiment slate ≈ 6–10k tokens output. Prune by risk severity, not exhaustively.
- Final go/no-go must be human; the LLM may flag "Proceed" on weak evidence because it cannot weigh business consequence.

## References
- Marty Cagan — *Inspired*, *Empowered* (the four risks framework).
- Teresa Torres — *Continuous Discovery Habits*; opportunity-solution tree.
- Eric Ries — *The Lean Startup* (build-measure-learn loop).
- Tomer Sharon — *Validating Product Ideas*.
- David Bland & Alex Osterwalder — *Testing Business Ideas* (44 experiment patterns).
- ReOps Community — discovery operations: https://researchops.community
- SVPG — discovery articles: https://www.svpg.com/articles/
