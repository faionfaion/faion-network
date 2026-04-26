# User Research at Scale

## Summary

AI-augmented research operations for N >= 500 sessions/week or >= 50 unmoderated tests, running a 9-stage pipeline: intake → sampling → instrumentation → collection → transcription → coding → synthesis → review → publish. Uses a frozen codebook with a separate `proposed_codes` overflow channel to prevent theme drift, and human-in-the-loop checkpoints before synthesis is published.

## Why

Traditional manual research does not scale with product velocity. AI handles throughput (transcription, pattern detection, codebook tagging); humans handle strategy, interpretation, and empathy. The separation is enforced by model assignment: Haiku for mechanical tasks, Sonnet for structured synthesis, Opus for cross-segment pattern mining. Mixing them collapses the quality/cost trade-off.

## When To Use

- N >= 500 sessions/week or >= 50 unmoderated tests where manual coding is the bottleneck.
- Continuous discovery teams needing a weekly pulse (Teresa Torres cadence).
- Product orgs with multiple teams running parallel studies (research-as-platform).
- Localization at scale — same study across 5+ languages, AI handles transcription + translation.
- Survey + behavior + interview triangulation when a single researcher cannot read everything.

## When NOT To Use

- Small N (< 10 deep interviews) — AI noise overwhelms signal; human coding is faster and richer.
- Strategic generative discovery where pattern-recognition beats throughput.
- Sensitive/regulated topics (health, finance, minors) requiring manual consent chains.
- Early-stage startups with < 100 users — you do not have scale problems yet.
- Studies where rapport, body language, or longitudinal trust is the data.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline-and-subagents.xml` | 9-stage pipeline, 10-subagent table (roles/models/inputs/outputs), prompt pattern for theme-coder. |
| `content/02-tools-and-services.xml` | CLI tools (whisperx, ffmpeg, bertopic, presidio), services table, best practices. |
| `content/03-gotchas.xml` | AI limitations: sentiment on non-English, codebook drift, transcript hallucination, cost traps, privacy rules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/codebook.yaml` | Frozen taxonomy: codes with id/label/valence_default/examples, segment axes. |
| `templates/code-batch.sh` | Batch-codes transcript directory via claude CLI, deduplicates, outputs parquet. |

## Scripts

none
