# Agent Integration — Jobs to Be Done (JTBD)

## When to use
- Re-framing an idea or feature in customer-progress terms before building.
- Diagnosing why a feature flopped: was the job mismatched, or the solution?
- Understanding switching: interview recent switchers (in or out) using the Forces of Progress framework.
- Mapping a complex job into stages (Define → Locate → Prepare → Confirm → Execute → Monitor → Modify → Conclude) to find the highest-pain stage.

## When NOT to use
- You're optimizing an already-validated product on a known job — go to AB tests, retention analysis, growth experiments.
- B2C impulse purchases (snacks, fashion) where the job is "feel good now" — JTBD over-engineers a simple need.
- Pure infrastructure / API tooling where "the job" is technical (matches an SDK contract); persona/feature thinking is faster.
- When you have no recent switchers to interview — JTBD without switching data is hypothesis-spinning.

## Where it fails / limitations
- "Find recent switchers" is hard outside well-trafficked categories. With <5 switcher interviews, JTBD is speculation.
- The Push/Pull/Habit/Fear forces are seductive but not falsifiable in a single interview — agents quote them as if measured.
- Jobs vs. solutions distinction collapses for digital-native categories where the solution shapes the job ("scrolling Instagram" — what's the stable job?).
- Job statements ("When... I want... So I can...") are easy to write and easy to fake. LLMs spit out plausible statements with no interview backing.
- The 8-stage Job Map is overkill for simple jobs (e.g., "send invoice"); applying it indiscriminately produces busywork.
- "Real competition is X" framings (milkshake vs bagels) are great post-hoc stories, weak prospective tools.

## Agentic workflow
Four roles. Switcher-recruiter agent (haiku): drafts outreach copy + screener questions to find recent switchers. Founder/researcher conducts interviews. Forces-tagger agent (sonnet): tags Push / Pull / Habit / Fear quotes from each transcript. Job-statement synthesizer (opus): aggregates ≥5 tagged interviews into 1-3 candidate job statements; for each, lists functional / emotional / social dimensions and the real competitive set. Job-mapper agent (sonnet, optional): expands the chosen statement into 8 stages with pain hot-spots.

### Recommended subagents
- `faion-pain-point-researcher-agent` — README assigns this agent for JTBD work.
- A custom `switcher-recruiter` (haiku) — drafts cold outreach + screener.
- A custom `forces-tagger` (sonnet) — labels quotes as Push/Pull/Habit/Fear with severity.
- A custom `job-statement-synthesizer` (opus) — generates 1-3 candidate statements with dimensional breakdown.
- A custom `job-mapper` (sonnet) — expands chosen statement into 8 stages + pain hot-spots.
- `faion-brainstorm` — diverge over candidate job statements before converging.

### Prompt pattern
```
Read skills/faion-knowledge/knowledge/solo/research/researcher/jobs-to-be-done/README.md.
For category=<X>, draft a switcher-screener with 4 questions. Disqualify anyone who switched
>90 days ago or hasn't completed the new solution's onboarding.
```

```
Tag this transcript. For each substantive turn, label PUSH | PULL | HABIT | FEAR (or NONE)
with severity 1-5 and a verbatim quote. Then propose a draft job statement in
"When ... I want ... So I can ..." form, citing 3 evidence quotes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| User Interviews / Respondent.io API | Recruit screened switchers | https://www.userinterviews.com |
| `otter.ai` / `fathom` API | Transcription + diarization | https://otter.ai/api |
| `airtable-cli` / `notion-cli` | Persist switcher database + tagged quotes | https://airtable.com/developers |
| Anthropic SDK | Force-tagging + statement synthesis | https://docs.anthropic.com |
| `apify` (G2 churn comments) | Mine recent switchers from review sites | https://apify.com |
| `google-sheets-cli` | Lightweight job-map worksheet | https://developers.google.com/sheets/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| User Interviews / Respondent | SaaS | Yes | Source switchers in target category. |
| Wynter | SaaS | Yes | B2B switcher panels for problem framing. |
| Otter / Fathom / Fireflies | SaaS | Yes | Recording + transcript via API/webhook. |
| Dovetail / Reduct | SaaS | Yes | Tag-and-cluster qualitative interviews; API exists. |
| Notion / Airtable | SaaS | Yes | Switcher log + force-tag matrix. |
| ChurnBuster / ProfitWell | SaaS | Yes | Find churned customers (forced firers); follow up with JTBD interview. |

## Templates & scripts
See `templates.md` and the README's three templates (Job Statement, JTBD Interview, Job Map). Inline force-tag aggregator (Python ≤30 lines):

```python
import json, sys, collections
data = json.load(sys.stdin)  # list of tagged transcripts
agg = collections.defaultdict(list)
for t in data:
    for turn in t["turns"]:
        if turn["label"] in {"PUSH", "PULL", "HABIT", "FEAR"}:
            agg[turn["label"]].append(
                {"q": turn["quote"], "sev": turn["severity"], "src": t["interview_id"]}
            )
summary = {f: {"count": len(v), "avg_sev": round(sum(x["sev"] for x in v)/len(v), 2)}
           for f, v in agg.items()}
summary["push_pull_vs_habit_fear"] = (
    sum(x["sev"] for x in agg["PUSH"]+agg["PULL"]) -
    sum(x["sev"] for x in agg["HABIT"]+agg["FEAR"])
)
print(json.dumps(summary, indent=2))
```

A positive `push_pull_vs_habit_fear` value indicates the market favours switching toward your solution; negative means inertia / fear dominates.

## Best practices
- Interview recent switchers within 60-90 days of the switch. Memory decay after that flattens the timeline.
- Capture the trigger ("first thought") moment — most product investments target the wrong stage because they skip the trigger.
- Always tag all four forces. Founders over-index on Push and Pull and forget Habit / Fear; the latter two often dominate for niche B2B.
- Functional + emotional + social dimensions — record all three even if one feels dominant. Emotional and social often explain price tolerance.
- Job statements should be testable: a stranger reading the statement should predict the customer's behaviour in three different scenarios. If not, refine.
- Use the 8-stage Job Map only for jobs with ≥3 distinct steps. Forcing it on simple jobs creates fake pain points.
- Re-run JTBD after major market shifts (LLMs, new platform, regulation). Solutions move; jobs are stable but contexts change.
- Pair with `problem-validation` for evidence weight and `pricing-research` for value capture.

## AI-agent gotchas
- LLMs generate plausible job statements without any interview data. Reject statements not backed by ≥3 verbatim quotes from real switchers.
- Force-tagging agents over-classify excitement as Pull and skepticism as Fear; require past-tense behaviour evidence ("I tried X first") for severity ≥4.
- The "milkshake job" example is so famous LLMs auto-pattern-match it onto any food/drink case. Suppress example-leakage by removing the README example from analyzer prompts.
- Agents conflate persona with job ("the marketing manager wants..."). Job is about progress + circumstance, not role. Lint for persona language.
- "Real competitor is doing nothing / spreadsheets" is a meme answer. Require evidence (competitor mention in interview transcript) before accepting.
- Synthetic-user simulators ("ask GPT to roleplay a switcher") fabricate forces — never substitute for real interviews.
- Human checkpoint: founder reviews the final job statement(s) and competitive set before any roadmap change. Statements drive feature priority — bad statements waste quarters.
- Cross-cultural job framing differs: emotional/social dimensions in collectivist cultures map differently than the Christensen examples; avoid copying Western templates verbatim.

## References
- https://hbr.org/2016/09/know-your-customers-jobs-to-be-done (Christensen)
- https://jtbd.info/ (Tony Ulwick)
- https://jtbd.info/2-the-jobs-to-be-done-handbook-3a3ddc20a23e
- https://www.lennysnewsletter.com/p/jtbd-an-action-guide
- https://www.intercom.com/blog/jobs-to-be-done-knowing-the-difference-between-customer-needs-and-customer-jobs/
- https://strategyn.com/jobs-to-be-done/ (Outcome-Driven Innovation)
