# AI-Assisted Persona Building

## Summary

Synthesize data-backed user personas from multi-source inputs (analytics CSVs, interview transcripts, survey exports) using a two-pass agent pipeline: a Sonnet subagent clusters behavioral patterns and produces draft persona JSON, then a validation agent checks each persona for JTBD consistency and flags fabricated fields. Human researchers approve before personas enter any design system.

## Why

Assumption-driven personas produce design decisions that miss real user behavior. AI behavioral clustering on actual data produces personas grounded in evidence, with quantified pain points and JTBD statements. Two-pass validation catches hallucinations before they propagate.

## When To Use

- You have real user data (analytics events, interview transcripts, survey CSVs) to cluster
- You need to synthesize personas from multi-source data faster than manual affinity mapping
- A product team wants data-backed personas replacing assumption archetypes
- Updating stale personas after a major product pivot or new market entry
- Running a JTBD framing exercise alongside persona creation

## When NOT To Use

- Zero real user data exists — AI will hallucinate plausible-sounding but false personas
- Product is in pre-discovery with no interviews or analytics yet
- Regulatory context prohibits feeding user data to third-party LLMs (HIPAA, GDPR special categories)
- Only 1–2 archetypes needed from a single homogeneous segment — manual synthesis is faster

## Content

| File | What's inside |
|------|---------------|
| `content/01-persona-process.xml` | 5-step data-driven process; JTBD integration; modern persona components vs traditional |
| `content/02-agent-pipeline.xml` | Two-pass clustering pipeline; data preprocessing rules; validation agent prompts |
| `content/03-anti-patterns.xml` | Gotchas: hallucinated demographics, thin clusters, JTBD extraction from passive text, stale personas |

## Templates

| File | Purpose |
|------|---------|
| `templates/normalize-interviews.py` | Preprocessing script: interview JSON → normalized records for LLM input |
| `templates/prompt-cluster-personas.txt` | Sonnet prompt for behavioral clustering and persona draft generation |
| `templates/prompt-validate-personas.txt` | Validation agent prompt to check JTBD consistency and flag fabricated fields |
