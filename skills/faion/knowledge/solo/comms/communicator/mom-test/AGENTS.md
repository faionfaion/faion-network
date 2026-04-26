# The Mom Test

## Summary

The Mom Test (Rob Fitzpatrick, 2013) is a customer discovery interview protocol with three rules: talk about their life not your idea; ask about past specifics not future hypotheticals; talk less than 20% of the time. It distinguishes genuine problem signals (specific past behavior, current spending, commitments) from worthless compliments ("sounds cool", "I would use this"). Real validation requires commitment — time (beta test), reputation (referral), or money (deposit) — not verbal enthusiasm.

## Why

People lie politely when asked about your idea. They want to be kind, not honest. Future-hypothetical questions ("would you use this?") produce answers based on what they wish they were doing, not what they actually do. Past-behavior questions ("tell me about the last time you dealt with this problem") produce facts. Compliments feel like validation but predict zero buying behavior; commitments predict real behavior.

## When To Use

- Early customer discovery before any code is written — validating that a problem is real and frequent
- Screening interview transcripts to identify genuine signals vs polite noise
- Generating interview question scripts that avoid leading, future-hypothetical, or opinion-seeking phrasing
- Extracting commitment signals (time, money, referrals) from existing interview notes or CRM records
- After 5+ interviews, running a synthesis pass to surface repeated patterns

## When NOT To Use

- Post-launch product analytics — Mom Test is a discovery tool, not a measurement tool
- B2B enterprise procurement where formal RFPs are required — conversational style reads as unprepared
- Quantitative surveys — explicitly qualitative, single-subject methodology
- When you already have paying customers with observable behavior; switch to churn/retention analysis

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Three rules with bad/good question pairs, commitment escalation ladder, red flags in interviews |
| `content/02-process.xml` | Interview structure (Opening/Exploration/Digging/Closing), data points to collect, post-interview processing |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-template.md` | Full interview script with four phases and example probes |
| `templates/signal-classifier.py` | Keyword-based signal classifier for post-interview note processing |
| `templates/prompt-question-gen.txt` | Prompt for generating Mom Test-compliant interview questions |
| `templates/prompt-transcript-analysis.txt` | Prompt for classifying interview transcript statements by signal type |
