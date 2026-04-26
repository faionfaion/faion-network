# Usability Testing

## Summary

Observe real users completing tasks with a product to discover what works, what confuses,
and where users struggle. Generates test plans, session scripts, and structured findings
reports with severity ratings. Use when you need evidence-based validation of design
decisions before or after launch.

## Why

Design assumptions fail silently until users interact with the actual interface. Five
participants in a moderated session reliably surface 85% of critical usability problems
(Nielsen's heuristic), catching issues before development cost compounds. Severity-rated
findings give engineering a prioritized backlog rather than a wishlist.

## When To Use

- A feature or flow has never been tested with real users
- Conversion or task-completion metrics show unexplained drops
- A redesign is complete and ready for pre-launch validation
- Synthesizing recordings or transcripts into structured findings for stakeholders
- Generating test plans from a feature spec or acceptance criteria set

## When NOT To Use

- Nothing testable yet (no wireframe or prototype) — nothing to observe
- Fewer than 3 participants available — no pattern detection is meaningful at that scale
- Large-N quantitative benchmarking (SUS scoring, statistical significance) — use survey instruments instead
- As a substitute for live facilitation — agents cannot observe non-verbal cues or probe nuance

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | 7-step testing process: goals → plan → tasks → recruit → conduct → analyze → report |
| `content/02-rules.xml` | Concrete rules: task wording, participant counts, severity rating, session structure |
| `content/03-examples.xml` | Good and bad task examples; severity classifications; agentic workflow patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-plan.md` | Full test plan template: objectives, methodology, tasks, metrics, schedule |
| `templates/session-script.md` | Facilitator script: intro, pre-test questions, tasks, post-test debrief |
| `templates/finding-format.md` | Finding format: severity, frequency, evidence, recommendation |
| `templates/prompt-synthesize.txt` | LLM prompt for synthesizing session notes into a prioritized findings report |
| `templates/prompt-test-plan.txt` | LLM prompt for generating a test plan from a feature spec |
