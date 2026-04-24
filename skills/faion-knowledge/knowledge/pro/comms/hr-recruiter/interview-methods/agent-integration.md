# Agent Integration — Interview Methods

How to drive the interview-methods bundle (structured interviews, behavioral Qs, scorecards, technical assessments, references, debriefs) with Claude subagents and ATS / interviewing tooling. Pairs with `README.md`, `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.

## When to use

- Standing up an interview process from scratch for a new role family (define competencies → questions → scorecards → debrief).
- Auditing an existing process whose interview-to-offer rate is outside the 15-25% band.
- Calibrating interviewers across geographies/timezones where in-person calibration sessions are impractical.
- Rolling out structured interviews after a hiring manager swap, before legacy bias re-anchors.
- Generating role-specific question banks plus behavioral anchors when HR has neither an I/O psych nor a recruiting ops team.

## When NOT to use

- Single-hire one-off (founder hiring a co-founder, exec search) — the overhead exceeds the benefit; use a structured 2-step trust-and-reference loop instead.
- Roles where the only valid signal is portfolio review (e.g., illustrators) — assessment and reference checks dominate.
- Volume retail / hourly hiring at scale — use realistic job previews, not panel interviews.
- Highly regulated roles (clinical, legal) where the questionnaire is statutorily fixed — no agent rewriting.

## Where it fails / limitations

- LLMs over-produce competencies (8-12) when 4-6 is the predictive sweet spot. Force a hard cap.
- Generated questions cluster in leadership/communication and under-cover technical depth — explicit weighting required.
- Behavioral anchors written by an LLM are often lifestyle adjectives ("driven", "strong"), not observable behaviors.
- Bias remains in the *questions an agent picks* — historical hires bias the bank toward what already worked.
- Cross-cultural pragmatics: STAR storytelling style varies by region; agent scoring assuming US-grad-style narrative will under-rate non-Western candidates.
- Reference-check questions, if auto-emailed by an agent, can violate FCRA / GDPR if consent is not captured — never automate the send.

## Agentic workflow

Drive the bundle as a five-stage pipeline owned by `faion-recruiter-agent`. Stage 1 (competency definition) is opus — it interrogates the JD + leveling rubric and emits a 4-6 row competency table with weights. Stage 2 (question generation) is sonnet, parameterized per competency with a hard count cap. Stage 3 (scorecard) is sonnet — produces behavioral anchors per competency on a 1-5 scale. Stage 4 (calibration pack) is sonnet — generates 3 mock candidate answers (strong / borderline / weak) per question for interviewer practice. Stage 5 (debrief synthesis) is opus — only after independent scores are submitted, never before. Human-in-loop at: competency sign-off, legal review of question bank, every actual hiring decision.

### Recommended subagents

- `faion-recruiter-agent` — orchestrator; owns the full pipeline and ATS writes.
- `general-purpose` reviewer (sonnet, fresh context) — adversarial pass for legally risky questions and bias smell-tests; must not see the original draft rationale.
- `faion-employer-brand-agent` — drafts candidate-facing artefacts (interview prep guide, what-to-expect emails) consistent with EVP.
- `faion-domain-checker-agent` — irrelevant; do not invoke.

### Prompt pattern

Competency definition:
```
You are designing a structured interview per skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/interview-methods/README.md.
Role: <title>, Level: <IC/M/D>, JD: <pasted>. Leveling rubric: <pasted or "none">.
Output exactly 4-6 competencies with weights summing to 100%. For each, write a 2-line definition in observable behaviors (no adjectives like "driven"). Return only the markdown table.
```

Bias / legal review (fresh context):
```
Audit this question bank for: protected-class proxies, hypothetical-only items, double-barrel, leading wording, items that cannot be scored against the supplied rubric. For each issue: quote the line, name the defect, propose a one-line fix. Refuse other commentary.
```

Debrief synthesis (post-scoring only):
```
Inputs: N independent scorecards (attached). Do not reweight. Surface: (1) competencies with score variance >= 2, (2) evidence cited vs impression-only language, (3) candidate-vs-candidate ranking on each weighted competency. Output a 1-page brief plus a "questions to resolve before decision" list. No hire recommendation.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Version interview kits + scorecards as repo artefacts | cli.github.com |
| `greenhouse-cli` (community) / Greenhouse Harvest API | Pull/push jobs, scorecards, scheduling | developers.greenhouse.io |
| `lever-cli` (unofficial) / Lever API v1 | Manage opportunities, feedback forms | hire.lever.co/developer/documentation |
| `ashby` API (REST) | Newer ATS, structured-interview-native | developers.ashbyhq.com |
| `workable` API | JD CRUD, candidate moves | workable.readme.io |
| `pandas` + `scipy.stats` | IRR / Cohen's kappa across interviewer scores | pypi |
| `pdftotext` / `unstructured` | Resume + scorecard ingestion | poppler-utils; unstructured.io |
| `op` (1Password CLI) | Pull ATS API tokens without committing secrets | developer.1password.com/docs/cli |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Greenhouse | SaaS ATS | Yes (Harvest REST + webhooks) | Strong scorecard + structured-interview primitives. |
| Lever | SaaS ATS | Yes (REST + webhooks) | Feedback forms map cleanly to scorecards. |
| Ashby | SaaS ATS | Yes (REST + webhooks) | Built for structured interviews; native rubric scoring. |
| Workable | SaaS ATS | Yes (REST) | SMB-friendly; agent can author JDs end-to-end. |
| BrightHire | SaaS | Yes (REST + webhook on interview-recorded) | Records, transcribes, tags STAR components — ideal for agent post-processing. |
| Metaview | SaaS | Yes (REST) | Live note-taking; export structured JSON of moments. |
| GoodTime | SaaS | Yes (REST) | Scheduling automation; agent can request slots. |
| HireVue | SaaS | Yes (REST) | Async video interviews; agent can extract transcripts only — never auto-score (regulatory). |
| Karat | SaaS | Limited | Outsourced technical screens; expect human-only loop. |
| CodeSignal / HackerRank / CoderPad | SaaS | Yes (REST + webhook on submission) | Live + take-home coding; agent can push problem packs. |
| Checkr / Certn | SaaS | Yes (REST) | Background checks; consent flow is human-only by law. |
| Modern Hire / Plum | SaaS | Partial | Assessments; bias audits required if used. |

Agent-friendliness rule: prefer ATS with REST + per-stage webhook. Polling burns tokens and racks up rate limits.

## Templates & scripts

See `templates.md` for: structured interview design doc, scorecard, debrief checklist. `examples.md` covers role-specific kits (engineer, PM, designer).

Inline helper — inter-rater agreement (run after each loop, gate the debrief if kappa is low):

```python
# irr_check.py — Cohen's kappa across interviewer scores per competency
import sys, json
from itertools import combinations
from sklearn.metrics import cohen_kappa_score

def kappa_matrix(scores):
    # scores: { interviewer: { competency: int 1..5 } }
    interviewers = list(scores)
    competencies = list(next(iter(scores.values())))
    out = {}
    for c in competencies:
        ks = []
        for a, b in combinations(interviewers, 2):
            ks.append(cohen_kappa_score([scores[a][c]], [scores[b][c]],
                                        labels=[1,2,3,4,5], weights="linear"))
        out[c] = round(sum(ks)/len(ks), 2) if ks else None
    return out

if __name__ == "__main__":
    data = json.load(sys.stdin)
    result = kappa_matrix(data)
    json.dump({"kappa_per_competency": result,
               "gate": "PASS" if all((v or 0) >= 0.4 for v in result.values()) else "RECALIBRATE"},
              sys.stdout, indent=2)
```

Pipe scorecard JSON in. If gate is RECALIBRATE, route to interviewer-training before allowing a hire decision.

## Best practices

- Cap competencies at 4-6 with weights summing to 100; more dilutes signal.
- Lock the question bank per role-level for at least 6 months — every change resets calibration baselines.
- Force independent scorecard submission *before* the debrief channel opens (technical lock, not policy).
- Behavioral anchors must be observable verbs ("re-architected payment retry to cut failures from 12% to 3%"), never traits.
- Pair every behavioral question with a "what would you do differently" follow-up — it doubles signal on metacognition.
- Include a take-home or live work-sample for any role above L3; interviews alone explain ~20% of performance variance, work samples nearly double that.
- Run a 2-week pilot of a new question bank with internal employees first — flush legally risky and ambiguous items.
- Track per-interviewer "hire rate when sole positive" — outliers indicate calibration drift, not necessarily good taste.
- For panels, always include at least one interviewer outside the hiring manager's reporting line.

## AI-agent gotchas

- Agents will silently inject protected-class proxies ("Are you willing to relocate with family?"). Always run the bias-review pass with a fresh context.
- LLM-generated scorecards conflate "5 = exceptional" with "5 = matches us" — force the rubric to reference observable outcomes, not similarity to existing team.
- An agent given a transcript will happily score the candidate. Block that path: scoring is human-only. Agents may extract STAR components, summarize evidence, flag missing-action vs missing-result — never assign the number.
- Auto-scheduling agents will book over candidates' working hours / time zones unless given availability constraints; always require a confirmation token from the candidate before sending the calendar invite.
- Reference-check questions sent by agent without a logged consent record are an FCRA / GDPR violation in EU, US, UK. Generate the email; do not send it.
- "Hiring committee" prompts often lead the LLM to adopt a "balanced" tone that softens No-Hire signals — explicitly instruct the agent to preserve dissent verbatim.
- Calibration drift is invisible without metrics. Re-run the IRR check monthly; LLMs cannot detect the slow consensus they create.
- Mandatory human-in-loop checkpoints: (1) competency + question sign-off (legal/HRBP), (2) every interview score, (3) every hire decision, (4) reference-check send.

## References

- Google re:Work — "Hiring: Use Structured Interviewing" (rework.withgoogle.com/guides/hiring-use-structured-interviewing).
- Schmidt & Hunter (1998) — "The Validity and Utility of Selection Methods in Personnel Psychology" (the source for structured-interview validity coefficients).
- Smart, G. — "Who: The A Method for Hiring".
- SHRM — "Conducting Effective Interviews" toolkit.
- EEOC — "Pre-Employment Inquiries" guidance (eeoc.gov).
- Greenhouse — "Structured Hiring 101" (greenhouse.io/structured-hiring).
- Internal: `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/structured-interview-design/agent-integration.md`.
- Internal: `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/star-interview-method/agent-integration.md`.
