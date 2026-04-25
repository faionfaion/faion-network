# Agent Integration — Continuous Discovery

## When to use
- Post-MVP product where weekly insight is needed to keep roadmap honest.
- Team has at least one customer-touching channel (interviews, support, in-app, analytics) feeding raw signal.
- Pairing roadmap-design with discovery so the "Now / Next / Later" buckets keep evolving.
- Solo PM/founder needs an automated cadence to compensate for not having a research team.

## When NOT to use
- Pre-PMF / 0-to-1 products — use product-discovery (one-time deep dive) until you have customers.
- Products with < 50 active users — discovery becomes anecdote-driven.
- Heavily regulated environments where every customer touch needs legal review (slows the loop below useful cadence).

## Where it fails / limitations
- "Continuous" without a feedback loop into the roadmap is theater — interviews accumulate, decisions don't change.
- LLM-summarized interviews lose nuance; the summary becomes the source of truth and the verbatim is forgotten.
- Sample bias: weekly interviews recruit the same engaged users; passive segments stay invisible.
- Cadence collapse: weekly slips to monthly slips to "when there's time". Automate or it dies.
- Insight drift: themes get re-named across weeks, longitudinal analysis becomes impossible.

## Agentic workflow
A daily ingest subagent pulls from analytics, support, in-app feedback, app stores, and TG/Slack channels into one normalized feed (re-using feedback-management triage). A weekly synthesis subagent runs theme clustering on the prior 7 days, names themes consistently against a controlled vocabulary, and emits an Opportunity Solution Tree fragment per theme. A weekly interview-prep subagent drafts 3 interview question scripts targeting top opportunities. A bi-weekly roadmap-link subagent diffs current opportunities against the roadmap and proposes adds/removes/re-prioritizations. Human reviews the diffs and decides; agent records the decision and rationale. All artifacts live in `.aidocs/discovery/<week>/`.

### Recommended subagents
- General-purpose `researcher` — runs WebSearch / docs lookups for desk research.
- `faion-mlp-gap-finder-agent` — clusters feedback into opportunity themes (also used by feedback-management).
- `faion-mlp-feature-proposer-agent` — converts opportunities into candidate solutions.
- `faion-mvp-scope-analyzer-agent` — sanity-checks proposed solutions for buildability.
- `faion-mlp-impl-planner-agent` — bridges discovery output into roadmap updates.

### Prompt pattern
```
Weekly synthesis. Inputs: 7 days of triaged feedback rows + analytics deltas.
Output JSON:
{
  "week": "<ISO week>",
  "themes": [
    {
      "id": "T-<slug>",                    // STABLE across weeks (controlled vocabulary)
      "name": "<short>",
      "evidence_count": <int>,
      "verbatim_samples": ["...","..."],   // <= 5
      "segments": ["..."],
      "suggested_opportunity": "<problem statement>",
      "candidate_solutions": ["..."],
      "roadmap_link": "<existing initiative id or null>"
    }
  ],
  "interview_questions": ["...", "..."],
  "decision_required": ["..."]
}
Use only theme_ids from controlled vocabulary at <path>; if a new theme is needed, propose it but flag for human approval.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Dovetail API | Research repo: tag, highlight, cluster | https://developers.dovetail.com |
| ProductBoard API | Insights → opportunities → features | https://developer.productboard.com |
| Pendo API | Behavioural analytics by feature | https://developers.pendo.io |
| Hotjar API | Heatmaps, session recordings | https://help.hotjar.com/hc/en-us/categories/115001323967 |
| Maze API | Rapid prototype testing | https://help.maze.co/hc/en-us/categories/115000060109 |
| Mixpanel / Amplitude / PostHog APIs | Product analytics for behavioural patterns | https://developer.mixpanel.com, https://amplitude.com/docs, https://posthog.com/docs/api |
| `whisper.cpp` / OpenAI Whisper API | Transcribe interview audio | https://github.com/ggerganov/whisper.cpp |
| `n8n` (this workspace) | Schedule discovery automation flows | https://docs.n8n.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Dovetail | SaaS | Yes (REST) | Best research repo for tags/highlights/themes |
| User Interviews | SaaS | Yes (REST) | Recruit participants on cadence |
| Respondent.io | SaaS | Yes (REST) | Same |
| Maze | SaaS | Yes (REST) | Rapid usability tests |
| PostHog | OSS | Yes (REST) | Self-host product analytics |
| ProductBoard | SaaS | Yes (REST) | Insights repo + opportunity tree |
| Notion + structured DB | SaaS | Yes (REST) | Cheapest discovery repo |
| Loom | SaaS | Yes (REST) | Async video interviews |
| Otter.ai | SaaS | Yes (REST) | Transcription |
| n8n | OSS (this workspace runs it) | Yes | Scheduled discovery flows |

## Templates & scripts
The README is sparse on templates; create your own one-pager with these sections: weekly cadence checklist, theme dictionary, opportunity solution tree, interview script template. Scheduling skeleton (≤ 35 lines):

```python
# discovery_cadence.py — emit this week's discovery checklist
import datetime, json, sys

WEEK = datetime.date.today().isocalendar()
checklist = {
    "week": f"{WEEK.year}-W{WEEK.week:02d}",
    "daily": [
        "review support ticket triage digest",
        "scan analytics anomalies (>2 sigma)",
    ],
    "weekly": [
        "run 1-3 user interviews",
        "synthesize last 7 days of triaged feedback into themes",
        "review competitor changelog list",
        "draft interview questions for next week",
    ],
    "biweekly": [
        "diff opportunities vs roadmap; propose changes",
    ],
    "quarterly": [
        "re-baseline theme vocabulary",
        "audit interview sample for segment bias",
    ],
}
print(json.dumps(checklist, indent=2))
```

## Best practices
- Allocate 15–20% of capacity to discovery. Schedule it; it never wins against feature pressure if optional.
- Maintain a controlled vocabulary of themes; new themes require explicit approval to prevent renaming drift.
- Always store verbatim quotes alongside synthesized themes; verbatim is the audit trail.
- Triangulate: behavioural (analytics) + attitudinal (interviews) + market (competitor monitoring). One source alone misleads.
- Tie every roadmap change to ≥ 1 cited opportunity from the discovery repo.
- Recruit across segments deliberately (not just "active users this week"); rotate criteria each week.
- Run a quarterly sample-bias audit: who haven't we talked to in 90 days?
- Pair with Teresa Torres' Opportunity Solution Tree as the artefact connecting discovery to delivery.

## AI-agent gotchas
- LLMs hallucinate themes when given low-volume weeks; require minimum N=evidence_count >= 3 before promoting a theme.
- Theme renaming across weeks destroys longitudinal trend; lock vocabulary in a versioned file, treat changes as schema migrations.
- Interview transcription via LLM loses tone/sarcasm cues; keep audio + raw transcript, not just summary.
- Agents skip "decision_required" — force the field; an empty array is acceptable but must be deliberate.
- Cadence enforcement: schedule via cron / n8n / scheduled trigger, not "remember to run weekly". Missed weeks erode the loop.
- PII redaction before LLM ingestion is mandatory (use password-scrubber-agent or regex pre-pass).
- Human-in-loop checkpoints: (a) any new theme added to the vocabulary, (b) any roadmap change proposed by the diff agent, (c) any outbound message to interviewed users.

## References
- Teresa Torres, "Continuous Discovery Habits" — canonical text for this methodology.
- Teresa Torres' blog https://www.producttalk.org/
- Marty Cagan, "Inspired" — discovery vs delivery distinction.
- Janna Bastow / ProdPad — "Continuous discovery for product teams".
- "The Mom Test" by Rob Fitzpatrick — interview discipline.
- Lenny Rachitsky — interviews with PMs running continuous discovery https://www.lennysnewsletter.com/
