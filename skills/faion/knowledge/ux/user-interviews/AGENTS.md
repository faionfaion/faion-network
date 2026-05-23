# User Interviews

## Summary

**One-sentence:** Produce a user-interview artefact (research-question deck + interview guide + per-session notes + insight statements) with verbatim quote citations and a sanitised-transcript log.

**One-paragraph:** One-on-one conversations with users or potential users to understand needs, behaviours, motivations, pain points. Inputs: research objectives + user-segment profile + recruitment pool. Output: a deck of 5-10 research questions, a neutrality-reviewed interview guide, per-session notes separating observation from inference, and insight statements each citing a verbatim quote from sanitised transcripts. 5-8 participants per segment is the saturation threshold.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Discovery, design, or post-launch research where the question is "why".
- A recruitment pool of 5-8 participants per relevant segment is reachable.
- Privacy compliance allows recording + AI processing (with consent).

## Skip If (ANY kills it)

- Quantitative goal (frequency, statistical significance) — use surveys.
- Agent-as-facilitator — interviews are human-facilitated.
- Participants cannot consent to AI processing.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Research objectives | doc | PM / UX |
| User segment profile | doc | UX |
| Recruitment pool (5-8 per segment) | list | UX ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/journey-mapping` | Interview quotes feed journey-map cells. |
| `solo/ux/ux-ui-designer/usability-testing` | Findings refine the next round of interviews. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules + skip-this-methodology fallback | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the interview artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | medium | 6-step procedure: objectives → guide → recruit → run → synthesise → human-validate | ~600 |
| `content/05-examples.xml` | medium | Worked example: 5 quotes feeding 3 insight statements | ~500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-guide` | sonnet | Open-ended question composition. |
| `review-neutrality` | opus | Detect leading or closed phrasing in the guide. |
| `synthesise-quotes-to-insights` | sonnet | Cluster verbatim quotes into insight statements. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-guide.md` | Interview guide skeleton with neutrality checklist. |
| `templates/session-notes.md` | Per-session notes skeleton (observation vs inference). |
| `templates/transcribe-sessions.sh` | Local whisper-based transcription + redaction. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-interviews.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[journey-mapping]]
- [[usability-testing]]
- [[prototyping]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, recruitment reachable, consent obtained) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
