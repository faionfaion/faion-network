# Agent Integration — Structured Interview Design

How to drive the structured-interview-design methodology (competency mapping, question banks, scorecards, calibration, debrief discipline) with Claude subagents and ATS / interview-intelligence tooling. Pairs with `README.md`, `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.

## When to use

- Standing up a new role family's interview kit from a freshly-defined leveling rubric.
- Migrating from unstructured ("just have a chat") interviewing to evidence-based hiring after a quality-of-hire dip.
- Calibrating distributed panels across geographies where in-person calibration is impractical.
- Running an interview-process audit when interview-to-offer rate is outside 15-25%.
- Re-baselining after a swap of hiring managers, before legacy bias re-anchors the team's defaults.

## When NOT to use

- Tiny pools (3-5 candidates total for a niche role) — calibration math has no signal.
- Senior-exec / board-search where multi-stakeholder relational interviewing matters more than rubric scoring.
- Hourly / volume retail — structured assessments + realistic job previews dominate.
- One-off contractor placements — the kit-build cost outweighs the per-hire benefit.

## Where it fails / limitations

- Predictive validity assumes the rubric measures the right competencies; structured interviewing of the wrong things is precise garbage.
- Behavioral anchors written by an LLM read as adjective lists; they need observable verbs to be scoreable.
- Calibration drifts silently as interviewers absorb each other's anchoring during loops.
- Panels of >5 interviewers introduce candidate fatigue without raising signal — the marginal interviewer adds noise.
- Independent scoring "before discussion" is a policy, not a control; without technical lockout, in practice scores leak via Slack.
- Cross-cultural pragmatics: Western-style structured interviews under-rate candidates from cultures that downplay personal credit ("we did" vs "I did").
- Assessment center-style structured interviews require trained assessors; agent-trained-only interviewers will skip the calibration practice and rate raw.

## Agentic workflow

Drive structured-interview design as a six-stage pipeline owned by `faion-recruiter-agent`. Stage 1 (competency definition, opus) — interrogates the JD + leveling rubric and emits a 4-6 row competency table with weights summing to 100. Stage 2 (question generation, sonnet) — 2-3 behavioral + 1 situational + 1 technical-or-motivational per competency, parameterized by role level. Stage 3 (rubric authoring, sonnet) — 1-5 scale per competency with observable behavioral anchors at each level. Stage 4 (round design, opus) — assigns competencies to rounds with no double-coverage and minimum 2 panel members per critical competency. Stage 5 (calibration pack, sonnet) — strong / borderline / weak mock answers per question with the "right" rubric scores. Stage 6 (debrief synthesis, opus) — only post-independent-submission; surfaces variance ≥2, evidence-vs-impression language, ranked candidate comparison.

### Recommended subagents

- `faion-recruiter-agent` — owns the full design pipeline.
- `general-purpose` reviewer (sonnet, fresh context) — adversarial bias / legal risk pass on questions and anchors.
- `faion-domain-checker-agent` — irrelevant; do not invoke.
- `faion-employer-brand-agent` — drafts candidate-side process explanation aligned with EVP.

### Prompt pattern

Competency + weights:
```
You are designing a structured interview kit per skills/faion/knowledge/pro/comms/hr-recruiter/structured-interview-design/README.md.
Role: <title>, Level: <IC3/M1/...>. JD: <pasted>. Leveling rubric: <pasted>. Manager's stated success criteria: <pasted>.
Output exactly 4-6 competencies with integer weights summing to 100. For each: a 2-line definition in observable verbs only (forbidden: "strong", "good", "excellent", any trait adjective). Cite which JD line motivates each.
```

Rubric anchors:
```
For each competency, write behavioral anchors at level 1, 3, 5 (skip 2, 4). Each anchor is one sentence describing an observable action + measurable outcome at that level. Forbidden: traits, comparisons to teammates, "exceeds expectations". Output a markdown table.
```

Calibration pack:
```
For each question, write three mock candidate answers tagged STRONG / BORDERLINE / WEAK, each 80-120 words, with the rubric score the answer should produce per the anchors. The BORDERLINE case must be genuinely ambiguous; no obvious tells.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Greenhouse Harvest API | Push scorecards + question banks into job stages | developers.greenhouse.io |
| Lever API v1 | Same | hire.lever.co/developer/documentation |
| Ashby API | Native rubric + structured-interview primitives | developers.ashbyhq.com |
| Workable API | SMB ATS | workable.readme.io |
| BrightHire / Metaview API | Pull interview transcripts + tagged moments | each provider |
| `pandas` + `scipy.stats` | Inter-rater agreement (Cohen's kappa, ICC) | pypi |
| `gh` | Version-control interview kits as artefacts | cli.github.com |
| `pdftotext` / `unstructured` | Resume + leveling-rubric ingestion | poppler-utils, unstructured.io |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Greenhouse | SaaS ATS | Yes (REST + webhooks) | Strong scorecard + scheduling integration. |
| Ashby | SaaS ATS | Yes | Best-in-class structured-hiring native. |
| Lever | SaaS ATS | Yes | Mature feedback forms. |
| Workable | SaaS ATS | Yes | SMB-friendly. |
| BrightHire | SaaS | Yes (REST + webhook) | Records, transcribes, tags STAR + competency moments. |
| Metaview | SaaS | Yes (REST) | Live note structuring + JSON export. |
| Pillar | SaaS | Yes (REST) | Interview intelligence + coaching. |
| GoodTime / Modernloop | SaaS | Yes | Schedules panels with calibration awareness. |
| Karat / Byteboard | SaaS | Limited | Outsourced structured technical interviews. |
| HackerRank / CodeSignal / CoderPad | SaaS | Yes | Structured technical assessments. |
| Plum / Modern Hire | SaaS | Partial | Validated assessments; mandatory bias audits if used. |

## Templates & scripts

See `templates.md` for: interview design doc, scorecard, debrief checklist, rubric anchors. Worked role examples (engineer, PM) in `examples.md`.

Inline helper — independent-scoring lockout gate (run before debrief opens):

```python
# debrief_lockout.py — only allow debrief when all independent scorecards exist
import sys, json, datetime as dt

def lockout(loop):
    # loop = {"candidate": id, "rounds": [{"interviewer": x, "submitted_at": ts|null, "scores": {...}|null}]}
    rounds = loop["rounds"]
    missing = [r["interviewer"] for r in rounds if not r.get("submitted_at")]
    submitted = [r for r in rounds if r.get("submitted_at")]
    if missing:
        return {"status": "LOCKED", "missing_from": missing,
                "earliest_open": None}
    timestamps = [dt.datetime.fromisoformat(r["submitted_at"]) for r in submitted]
    return {"status": "OPEN", "missing_from": [],
            "all_submitted_at": max(timestamps).isoformat(),
            "scores": {r["interviewer"]: r["scores"] for r in submitted}}

if __name__ == "__main__":
    json.dump(lockout(json.load(sys.stdin)), sys.stdout, indent=2)
```

Pipe loop JSON in. While LOCKED, the agent must not surface aggregate scores or ranking to any panelist; only the recruiter sees who is missing.

## Best practices

- 4-6 competencies, integer weights summing to 100. Any deviation is a smell.
- One competency per question, one question per competency *primary* (others can re-probe).
- Behavioral anchors: observable verb + measurable outcome. "Re-architected payment retry, dropping failures from 12% to 3%" not "strong systems thinker".
- Cap loop at 4-5 interviewers; >5 raises fatigue, not signal.
- Run a 60-min calibration session per new role family; rerun whenever a new interviewer joins.
- Every interviewer scores independently before the debrief — enforce technically (ATS lock), not by policy.
- Track inter-rater agreement (Cohen's kappa per competency); if <0.4 sustained, recalibrate before any more hires.
- Every quarter, audit hire vs no-hire decisions against actual 12-month performance. Recalibrate anchors if predictive validity drifts.
- Behavioral + situational + technical, in that order of weight, for most knowledge work.

## AI-agent gotchas

- Agents conflate "competency" with "trait" and produce non-scoreable rubrics ("emotionally intelligent", "growth-minded"). Force observable verbs.
- LLMs default to 5-point scales for everything; force a justification per competency.
- Generated questions cluster in leadership/communication; weight the prompt to enforce technical/execution coverage.
- Agents will write "exceeds expectations" anchors that are tautological — push for outcomes, not levels.
- Independent-scoring violations are invisible to LLMs; they read submitted scorecards and assume independence. Add a timestamp / Slack-traffic check.
- Calibration packs auto-generated by an LLM are too on-the-nose — borderline cases need real ambiguity, not surface-level mid-cases. Pull real anonymized historical answers when possible.
- Panel composition: agents will assign the same competency to all panelists "for safety", destroying coverage. Constrain at the prompt level.
- Mandatory human-in-loop: (1) competency table approval (HRBP), (2) legal-risk pass on questions, (3) every score, (4) every hire decision, (5) any anchor change after launch.

## References

- Google re:Work — "Hiring: Use Structured Interviewing" (rework.withgoogle.com).
- Schmidt & Hunter (1998) — "Validity and Utility of Selection Methods in Personnel Psychology".
- Levashina, Hartwell, Morgeson, Campion (2014) — "The Structured Employment Interview" meta-analysis.
- McDaniel et al. (1994) — structure-validity meta-analysis.
- HBR — "How to Hire" (Bock, 2016).
- SHRM — "Conducting Effective Interviews" toolkit.
- NYC Local Law 144 — AEDT bias audit framework.
- Internal: `skills/faion/knowledge/pro/comms/hr-recruiter/star-interview-method/agent-integration.md`.
- Internal: `skills/faion/knowledge/pro/comms/hr-recruiter/star-interview-framework/agent-integration.md`.
- Internal: `skills/faion/knowledge/pro/comms/hr-recruiter/interview-methods/agent-integration.md`.
