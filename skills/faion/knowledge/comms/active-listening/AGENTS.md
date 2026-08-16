# Active Listening

## Summary

**One-sentence:** Generates a RASA-structured interview question flow plus transcript annotation that ensures speakers feel understood before any response.

**One-paragraph:** Active listening (RASA: Receive, Appreciate, Summarize, Ask) is a structured reactive practice that produces two artefacts: a pre-conversation script (open-only questions, paraphrase starters, silence cues) and a post-conversation annotated transcript (RASA labels, dominance flags, skipped-step markers). Output target is Level 5 empathic listening where both content and emotional register are captured. Agents do not execute the conversation live — they scaffold the script and analyze the transcript afterwards.

**Ефективно для:**

- Requirements gathering with skeptical stakeholders who withhold detail when not heard.
- Customer discovery calls where embedded assumptions in closed questions kill signal.
- Conflict de-escalation prep where the listener needs a reflective formula before going in.
- Post-session coaching reviews that surface where Summarize was skipped or interviewer dominated.

## Applies If (ALL must hold)

- Requirements gathering sessions with stakeholders or clients.
- 1-on-1 meetings where trust or engagement is at risk.
- Customer discovery interviews (especially with skeptical interviewees).
- Conflict situations where one party feels misunderstood.
- Performance discussions or coaching conversations.

## Skip If (ANY kills it)

- Real-time agent conversations — agents cannot perform empathic listening live; they can scaffold it but not execute it.
- High-stakes interpersonal conflicts — a script-driven approach risks feeling mechanical and backfiring.
- Situations where a direct answer is needed and the other party is not emotionally engaged.
- Asynchronous text threads where silence and pace cues are absent.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Conversation goal | one-sentence brief | session owner |
| Interviewee profile | role + context paragraph | CRM / session owner |
| Transcript (post-pass only) | speaker-labeled text | recorder / Fireflies / Otter |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[stakeholder-communication]] | upstream — defines who and why before script generation |
| [[mom-test]] | upstream — bias-free interview discipline that pairs with RASA |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: rasa-full-cycle, open-question-discipline, level-5-target, reflective-formula, mirror-only-no-interpretation, silence-3-to-5s | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for RASA script + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 4-step procedure (scope → generate → review → annotate) | 700 |
| `content/05-examples.xml` | essential | Worked RASA script for a slow-deployment stakeholder session | 400 |
| `content/06-decision-tree.xml` | essential | Routes by signal (live vs prep, conflict vs requirements) to a rule | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate-rasa-script` | sonnet | Light judgement on phrasing + assumption checks. |
| `annotate-transcript` | haiku | Mechanical label + word-count flags. |
| `coach-skip-summarize` | sonnet | Tone-sensitive reflection, not mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-rasa-question-flow.txt` | Prompt to generate a RASA-structured interview script for a given goal |
| `templates/prompt-transcript-annotation.txt` | Prompt to annotate a transcript with RASA labels and quality flags |
| `templates/speaker-ratio.py` | Python snippet to measure interviewer word-share from a transcript |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-active-listening.py` | Validate the RASA script artefact against the output schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[stakeholder-communication]]
- [[mom-test]]
- [[conflict-resolution]]
- [[feedback]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts with "is this a live conversation or pre/post analysis", then routes by stakes and conflict level to either a script generation rule, a transcript annotation rule, or a skip conclusion when the methodology cannot apply (live execution).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-rasa-question-flow.txt`

```text
Generate a RASA-structured question flow for: <CONVERSATION_GOAL>.
Interviewee profile: <ROLE/CONTEXT>.

Output format:
- Receive: [opening statement to set attention and signal full focus]
- Appreciate: [2-3 acknowledgment phrases to use during the conversation]
- Summarize: [3 paraphrase starters keyed to likely themes]
- Ask: [5 open follow-up questions]

Constraints:
- No yes/no questions
- No "Is...", "Do you...", or "Did you..." openers
- No leading questions that embed assumptions
- Questions must be ordered from broad to specific
```

### `templates/prompt-transcript-annotation.txt`

```text
Annotate this conversation transcript using RASA labels and quality flags.

For each interviewer turn:
1. Label as R (Receive), A (Appreciate), S (Summarize), or Ask (open question)
2. Flag if it is a closed question (yes/no answerable)
3. Flag if it contains a leading assumption

After annotation, provide:
- RASA step coverage: which steps were skipped or underused
- Word-share check: flag any 3-turn window where interviewer speaks > 20% of words
- Top 3 recommendations for the next session

Transcript:
<TRANSCRIPT>
```

### `templates/speaker-ratio.py`

```python
def speaker_ratio(transcript: list[dict]) -> dict[str, float]:
    """
    Measure word-share per speaker from a labeled transcript.

    Input:
        transcript: list of {"speaker": "INTERVIEWER"|"INTERVIEWEE", "text": "..."}

    Output:
        dict mapping speaker name to word-share float (0.0 to 1.0)

    Rule: if ratio["INTERVIEWER"] > 0.20 in any 3-turn window, flag as dominated.
    """
    from collections import defaultdict
    counts: dict[str, int] = defaultdict(int)
    for turn in transcript:
        counts[turn["speaker"]] += len(turn["text"].split())
    total = sum(counts.values()) or 1
    return {k: round(v / total, 3) for k, v in counts.items()}


def check_dominance(transcript: list[dict], window: int = 3) -> list[int]:
    """
    Return start indices of 3-turn windows where INTERVIEWER word-share > 20%.
    """
    dominated = []
    for i in range(len(transcript) - window + 1):
        window_turns = transcript[i:i + window]
        ratio = speaker_ratio(window_turns)
        if ratio.get("INTERVIEWER", 0) > 0.20:
            dominated.append(i)
    return dominated


# Usage example:
# transcript = [
#     {"speaker": "INTERVIEWER", "text": "How does that affect your team?"},
#     {"speaker": "INTERVIEWEE", "text": "It slows everything down..."},
# ]
# print(speaker_ratio(transcript))
# print(check_dominance(transcript))
```
