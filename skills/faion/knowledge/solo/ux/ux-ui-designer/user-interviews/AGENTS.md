# User Interviews

## Summary

User interviews are one-on-one conversations with users or potential users to understand needs, behaviors, motivations, and pain points. They are qualitative and exploratory — they reveal the "why" behind observed behaviors. 5-8 participants per distinct user segment is the practical threshold for theme saturation.

## Why

Designing without user input replaces understanding with assumptions. Assumptions produce wrong solutions to real problems or correct solutions to non-existent ones. User interviews are the primary method for developing genuine empathy with users before design decisions are made.

## When To Use

- Discovery phase — understand the problem space, user needs, mental models
- Design phase — validate concepts and early-stage ideas before prototyping
- Post-launch — understand how users actually use the product and what frustrates them
- Generating a tailored interview guide from research objectives and user profile descriptions
- Synthesizing interview transcripts or notes into themes and insight statements

## When NOT To Use

- Quantitative goals (frequency, statistical significance) — use surveys or A/B testing
- Conducting the interview itself — an agent cannot replicate human facilitator judgment or rapport
- Replacing user research entirely — agent synthesis requires actual interview data as input
- When participants cannot provide informed consent for AI processing (check privacy regulations)

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Interview types, recruitment criteria, question types, synthesis techniques |
| `content/02-rules.xml` | Question quality rules, neutrality principles, agent synthesis gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-guide.md` | Full interview guide: intro script, warm-up, main topics, probe suggestions, wrap-up |
| `templates/session-notes.md` | Per-session notes: quotes, observations, pain points, needs, behaviors |
| `templates/transcribe-sessions.sh` | Bash script for batch-transcribing recordings with OpenAI Whisper |
