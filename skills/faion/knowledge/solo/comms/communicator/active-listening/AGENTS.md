# Active Listening

## Summary

A structured listening practice (RASA: Receive, Appreciate, Summarize, Ask) that ensures the speaker feels understood before the listener responds. Combines paraphrasing, mirroring, open questions, and empathic reflection to reach Level 5 empathic listening — understanding both content and emotion.

## Why

People who don't feel heard withhold information, resist decisions, and disengage. Active listening is the single highest-leverage technique for requirements gathering and conflict de-escalation: it costs nothing and directly reduces the "missing information" failure mode. Research shows 80% of communication problems trace to listening failures, not speaking failures.

## When To Use

- Requirements gathering sessions with stakeholders or clients
- 1-on-1 meetings where trust or engagement is at risk
- Customer discovery interviews (especially with skeptical interviewees)
- Conflict situations where one party feels misunderstood
- Performance discussions or coaching conversations

## When NOT To Use

- Real-time agent conversations — agents cannot perform empathic listening live; they can scaffold it but not execute it
- High-stakes interpersonal conflicts — a script-driven approach risks feeling mechanical and backfiring
- Situations where a direct answer is needed and the other party is not emotionally engaged
- Asynchronous text threads where silence and pace cues are absent

## Content

| File | What's inside |
|------|---------------|
| `content/01-rasa-framework.xml` | RASA steps, open vs closed questions, listening levels, reflective listening formula |
| `content/02-techniques-and-barriers.xml` | Paraphrasing, mirroring, silence technique, barriers with fixes, agent workflow patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-rasa-question-flow.txt` | Prompt to generate a RASA-structured interview script for a given goal |
| `templates/prompt-transcript-annotation.txt` | Prompt to annotate a transcript with RASA labels and quality flags |
| `templates/speaker-ratio.py` | Python snippet to measure interviewer word-share from a transcript |

## Scripts

none
