# Agent Integration — STAR Interview Method

How to drive the STAR (Situation-Task-Action-Result) behavioral-interview methodology with Claude subagents and recording / ATS tooling. Pairs with `README.md` (framework + question bank), `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.

## When to use

- Behavioral rounds for any role where past behavior is the dominant performance predictor (managerial, cross-functional, customer-facing).
- Calibrating an interviewer team that drifts into hypotheticals ("how would you...") instead of evidence ("tell me about a time...").
- Generating tailored STAR question banks per competency from a JD or leveling rubric.
- Post-interview transcript analysis: did the candidate provide a complete S/T/A/R, or are components missing?
- Coaching internal candidates preparing for promotion panels.

## When NOT to use

- Pure technical screens where the signal lives in code, system design, or work samples — STAR adds noise.
- Roles with < 2 years of experience: candidates lack a deep STAR repertoire; situational + work-sample combinations work better.
- Cultures where narrative storytelling is unfamiliar (some EU/EE/JP candidates) — non-English-native speakers under-perform on STAR style without scoring it controlled-for.
- Crisis / urgency screens where the only viable signal is real-time problem-solving.

## Where it fails / limitations

- Rehearsed STAR answers from coaching sites are common; without probing, the "R" is fabricated. Force quantified results + a "who else was involved I could verify with" follow-up.
- Candidates re-attribute team accomplishments as personal "A". The agent transcript-scorer will accept it unless explicitly prompted to flag pronoun shifts ("we" → "I").
- "R" inflation: 30% gains, 10x improvements, etc. Without a baseline question, the result is undebatable.
- STAR rewards verbal articulation, not necessarily competence. Cross-check with work samples.
- Agent-generated STAR questions cluster on leadership/communication; weak coverage of execution and depth.
- Single-component STAR (just Action) is common in technical contributors — scoring as "incomplete" under-rates strong builders.

## Agentic workflow

Drive STAR as a four-stage pipeline owned by `faion-recruiter-agent`. Stage 1 (question bank generation, sonnet) consumes the competency table and emits 3-5 STAR questions per competency, weighted by importance. Stage 2 (live-interview prompt support, sonnet, low latency) is optional — feeds the interviewer suggested probes when the candidate's answer is missing a component (S/T/A/R parser). Stage 3 (post-interview transcript STAR-extraction, sonnet) tags S/T/A/R spans and missing components per question. Stage 4 (cross-candidate calibration, opus) compares STAR completeness + evidence quality across the loop, never assigns scores. Scoring is always human.

### Recommended subagents

- `faion-recruiter-agent` — owns question generation, transcript extraction, calibration brief.
- `general-purpose` reviewer (sonnet, fresh context) — adversarial check that questions actually elicit past behavior (not hypotheticals or values).
- `faion-employer-brand-agent` — writes the candidate-facing prep email explaining STAR (reduces non-native disadvantage).

### Prompt pattern

Question generation:
```
You are designing a STAR question bank per skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/star-interview-method/README.md.
Competencies + weights: <pasted table>. Role level: <IC3/M1/...>. Output exactly 3-5 questions per competency. Each question: (1) past-tense behavioral framing only, no hypotheticals, (2) probes the specific competency, (3) cannot be answered with values/opinions. Provide 2 follow-up probes per question. Return only the markdown.
```

Transcript STAR extraction (post-interview, never live-scoring):
```
Given this interview transcript, for each question identify spans for Situation, Task, Action, Result. Output JSON: {question, S: span|null, T: span|null, A: span|null, R: span|null, pronoun_shifts: [...], quantified_metrics: [...]}. If a component is missing, return null. Do not score; do not infer.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisper` / `whisperx` | Local transcription of recorded interviews (consent required) | github.com/openai/whisper, github.com/m-bain/whisperX |
| `pyannote-audio` | Speaker diarization (separate interviewer vs candidate) | github.com/pyannote/pyannote-audio |
| `ffmpeg` | Audio extraction from Zoom/Meet recordings | ffmpeg.org |
| `jq` | Reshape STAR-extraction JSON into scorecard rows | stedolan.github.io/jq |
| Greenhouse Harvest API | Push question bank into job stage feedback forms | developers.greenhouse.io |
| Lever API | Same for Lever feedback forms | hire.lever.co/developer/documentation |
| Ashby API | Native rubric upload | developers.ashbyhq.com |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| BrightHire | SaaS | Yes (REST + webhook) | Records interviews, auto-tags moments — ideal data source for STAR extraction agents. |
| Metaview | SaaS | Yes (REST) | Live + post-interview AI notes, exportable JSON. |
| Pillar | SaaS | Yes (REST) | Interview intelligence; competitor to BrightHire. |
| Hume / Otter | SaaS | Yes (REST) | Transcription + speaker labels. |
| Greenhouse | SaaS ATS | Yes | Stage-level feedback forms accept STAR-templated rubric fields. |
| Lever / Ashby | SaaS ATS | Yes | Same. |
| Notion / Coda | SaaS | Yes (REST) | Question banks live as living docs; agents update via API. |
| Loom | SaaS | Yes (REST) | Async candidate-side STAR rehearsal videos. |
| Calendly / GoodTime | SaaS | Yes (REST) | Send STAR prep guide alongside scheduling email. |

## Templates & scripts

See `templates.md` for the question-bank-by-competency, STAR scorecard, and hiring-manager interview guide.

Inline helper — STAR completeness checker (deterministic gate before LLM transcript analysis):

```python
# star_completeness.py — flag transcripts missing components
import sys, json, re

CUES = {
    "S": [r"\b(when|at the time|context was|background)\b", r"\b(20\d\d|last (year|quarter|month))\b"],
    "T": [r"\b(my (role|responsibility|task|goal)|I was responsible|I was asked)\b"],
    "A": [r"\bI (decided|did|built|wrote|led|negotiated|shipped|coded|hired|coached)\b"],
    "R": [r"\b(\d+%|\$\d+|reduced|increased|improved|grew|saved|cut|delivered)\b"],
}

def score(answer):
    flags = {}
    for k, pats in CUES.items():
        flags[k] = any(re.search(p, answer, re.I) for p in pats)
    flags["pronoun_we_only"] = "we " in answer.lower() and " i " not in (" " + answer.lower())
    flags["complete"] = all(flags[k] for k in "STAR")
    return flags

if __name__ == "__main__":
    data = json.load(sys.stdin)  # [{"question": "...", "answer": "..."}]
    out = [{"q": d["question"], **score(d["answer"])} for d in data]
    json.dump(out, sys.stdout, indent=2)
```

Pipe interview transcript JSON in → flag answers without quantified Result, or with "we" only → trigger interviewer probe in next round.

## Best practices

- Always start with "Tell me about a time when..." — never "How would you handle...". The latter is hypothetical, predictive validity is near zero.
- Probe Action, not Result, first. Strong candidates self-quantify; weak ones can't even when prompted.
- Force pronouns in the Action: "What did *you* do versus the team?" Re-attribution catches inflation.
- Ask "what would you do differently" — gates metacognition, often more diagnostic than the original Result.
- Cap to 3-4 STAR questions per 45-minute round. More creates rushed shallow stories.
- Send candidates a 1-page STAR prep brief before the loop. It reduces non-native-speaker disadvantage and lifts the *floor*, not the ceiling.
- When scoring, separate "STAR completeness" from "competency demonstrated". A complete STAR can still show weak competency.
- Keep a per-question "strong / borderline / weak" exemplar pack for new interviewer calibration. Refresh quarterly.
- For panels, assign each interviewer 1-2 competencies; do not ask all interviewers all STAR questions.

## AI-agent gotchas

- Agents readily hallucinate the Result when summarizing transcripts. Force "verbatim quote required for any number cited".
- Transcripts often contain the interviewer's STAR scaffolding ("ok so what was the situation"); agents will treat this as the candidate's S. Always pre-diarize.
- LLMs accept "we" as personal action — explicitly require pronoun-shift detection.
- Generated questions drift to leadership/communication; weight the prompt to force technical/execution coverage.
- Agents will "improve" STAR questions into double-barreled forms ("Tell me about a time you led a team and resolved conflict") — cap one competency per question.
- Live-coaching prompts to the *interviewer* are fine; live-coaching to the *candidate* during a real interview is fraud-equivalent — block by policy.
- Mandatory human-in-loop: (1) every question-bank approval, (2) every score, (3) every hire decision, (4) any decision derived from auto-extracted STAR signals.

## References

- Indeed Career — "How To Use the STAR Interview Response Technique".
- Google re:Work — "Hiring: Use Structured Interviewing".
- SHRM — "Behavioral Interviewing" toolkit.
- Smart, G. — "Who: The A Method for Hiring" (top-grading interview is STAR-like).
- McDaniel et al. (1994) — meta-analysis showing structured behavioral interviews ~2x predictive of unstructured.
- Janz, T. (1982) — original "Patterned Behavior Description Interview".
- Internal: `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/star-interview-framework/agent-integration.md`.
- Internal: `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/structured-interview-design/agent-integration.md`.
