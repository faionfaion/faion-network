# Agent Integration — Continuous Discovery

## When to use
- Product is past initial PMF and decisions have started feeling arbitrary; recurring discovery is needed to keep direction grounded.
- A delivery team has the bandwidth to allocate ~15–20% to discovery without halting feature work.
- High-velocity environment (multiple releases per week) where one-off discovery cycles cannot keep up.
- After a major launch, to monitor activation/retention while iterating.

## When NOT to use
- Pre-PMF: continuous discovery dilutes effort across a wide problem space; concentrated discovery sprints work better.
- Solo founder with no recurring user pool yet — there is nothing to "continuously" sample.
- Frozen feature scope with imminent contractual deadline; discovery findings cannot be acted on.
- Teams without analytics + a research repository; insights evaporate without storage.

## Where it fails / limitations
- Discovery theatre: weekly interviews held but never tied back to decisions. Tracks attendance, not impact.
- Insights buried in transcripts; without taggable storage, the same lesson is "rediscovered" quarterly.
- Discovery and delivery teams diverge — discovery becomes a wishlist generator nobody implements.
- Sample bias: same 5 power users interviewed every week ⇒ confirmation chamber.
- Heavy on synchronous interviews; behavioural data and support signals are under-used.

## Agentic workflow
Schedule three loops. Daily: a behaviour-watcher agent diffs analytics dashboards (PostHog, Mixpanel, Amplitude) and drops anomalies into a digest. Weekly: an interview-prep agent picks 5 candidate users by segment, drafts an interview guide tied to current opportunities; after sessions, a transcription/synthesis agent extracts themes and tags them in a research repository (Dovetail/Notion). Sprint cadence: an opportunity-mapper agent updates the opportunity-solution tree feeding the roadmap. Humans run the actual interviews and decide which experiments graduate to delivery.

### Recommended subagents
- `faion-idea-generator-agent` — generates experiment hypotheses from the latest week's themes.
- `faion-mlp-impl-planner-agent` — promotes validated opportunities into roadmap initiatives.
- `faion-spec-reviewer-agent` — reviews experiment briefs for testability before launch.
- `faion-task-creator-agent` — turns approved experiments into trackable backlog items.

### Prompt pattern
```
System: You are a discovery synthesizer. Input: array of interview snippets,
support ticket excerpts, and analytics anomalies. Output JSON:
  {themes:[{label, evidence:[{source, quote_or_metric}], confidence:0..1}],
   opportunities:[{label, parent_theme, jtbd, severity:lo|md|hi}],
   suggested_experiments:[{hypothesis, method, sample_n, success_metric,
   kill_threshold}]}
Forbid summarising more than 5 themes. Reject opportunities lacking
  >=2 distinct evidence sources.
```

```
System: You are a discovery cadence auditor. Given last 30 days of activity,
return: {interviews_completed, themes_logged, experiments_run,
shipped_decisions_traced_to_themes, leakage_pct}.
Flag if shipped_decisions_traced_to_themes < 50% of feature releases.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `posthog` API | Programmatic dashboard diffs, anomaly alerts | https://posthog.com/docs/api |
| `mixpanel-api` | Same for Mixpanel; cohort comparisons | https://developer.mixpanel.com |
| `amplitude-sdk` | Behavioural cohorts → discovery prompts | https://www.docs.developers.amplitude.com |
| `dovetail` API | Push tagged research notes from agents | https://developers.dovetail.com |
| `whisper.cpp` / `openai whisper` | Local transcription for interview audio | https://github.com/openai/whisper |
| `airtable-cli` | Cheap research repo if Dovetail is overkill | https://airtable.com/developers/web/api |
| `productboard` API | Map opportunities → features | https://developer.productboard.com |
| `n8n` / `make` | Cron the daily/weekly discovery loops | https://n8n.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Dovetail | SaaS | Yes (REST) | Best-in-class research repository, taggable. |
| Condens | SaaS | Yes (REST) | Cheaper Dovetail alternative. |
| Productboard | SaaS | Yes (REST) | Native opportunity-solution tree support. |
| Pendo | SaaS | Yes (REST) | In-app surveys + analytics in one. |
| Hotjar | SaaS | Limited (REST read) | Recordings + heatmaps; agents consume not control. |
| Maze | SaaS | Yes (REST) | Rapid unmoderated testing for weekly cadence. |
| User Interviews | SaaS | Yes (REST) | Source recurring participants automatically. |
| Reveal | OSS | Partial | Self-host research repo. |
| PostHog | OSS / SaaS | Yes (REST) | Open-source product analytics; agent-controllable. |

## Templates & scripts
See `README.md` for the activity/frequency table and Discovery → Delivery integration outline. Helper that flags discovery-decision leakage:

```python
# leakage = released features that have no tagged opportunity in repo
import sys, json
data = json.load(open(sys.argv[1]))  # {releases:[{id,title,opp_ids:[]}], opps:[{id,...}]}
opp_ids = {o["id"] for o in data["opps"]}
unlinked = [r for r in data["releases"] if not (set(r.get("opp_ids", [])) & opp_ids)]
total = len(data["releases"])
ratio = len(unlinked) / total if total else 0
print(f"releases={total} unlinked={len(unlinked)} leakage={ratio:.0%}")
sys.exit(1 if ratio > 0.30 else 0)  # >30% = discovery disconnected from delivery
```

## Best practices
- Tag every interview snippet to an opportunity in a single repo. Without tagging, continuous discovery is just continuous chatter.
- Recruit a rolling panel of 30–50 users with rotation; never let the same 5 dominate.
- Ship one experiment per sprint, even tiny ones — cadence beats perfection.
- Combine interviews + behavioural data + support tickets for triangulation; one source alone is biased.
- Maintain an opportunity-solution tree (Teresa Torres) and require new ideas to attach to a node.
- Hold a monthly "what changed in user behaviour" review using analytics diffs, not anecdotes.
- Time-box weekly interviews to 30 minutes and 5–7 questions; longer sessions degrade signal.
- Keep a "decisions" log per quarter linking shipped features to discovery insights — this is the leakage check.

## AI-agent gotchas
- Synthesis agents over-summarise: many distinct quotes collapse into 2–3 generic themes. Set minimum themes and require evidence count per theme.
- Sentiment classifiers give false certainty on small samples; refuse confidence > 0.8 below n=15.
- Without explicit redaction, agents leak interviewee PII into shared tools. Add a scrubber step before pushing to any external repo.
- Behaviour anomaly detection trips on weekend/holiday seasonality; require comparison against trailing 4 weeks, not 7 days.
- Agents tend to recommend "schedule more interviews" as a remedy for any gap; force them to consider behavioural data and support tickets first.
- Continuous discovery agents running 24/7 produce alert fatigue; route digests to humans only on threshold breaches.
- Translation drift: interviewing in non-English languages and translating via LLM loses nuance; keep originals in the repo.
- Long-context cost: do not feed full transcripts every week. Index once, retrieve relevant chunks per query.
- Human checkpoint mandatory before treating an opportunity as validated; LLMs are credulous about user statements that contradict observed behaviour.

## References
- Teresa Torres — *Continuous Discovery Habits* (canonical text + producttalk.org).
- Marty Cagan — *Empowered* and *Discovery Discovery* posts on svpg.com.
- Tomer Sharon — *It's Our Research* (research repository practices).
- Productboard — opportunity-solution tree guide: https://www.productboard.com/glossary/opportunity-solution-tree/
- ReOps Community — research operations standards: https://researchops.community
- NN/g — continuous research: https://www.nngroup.com/articles/continuous-discovery/
