# AI Research Tools (geek/researcher)

## Summary

A stage-to-tool mapping for AI-augmented research pipelines: assign each research stage
(exploration, deep research, competitor intel, sentiment, market data, trend analysis,
interview analysis) to the AI tool best suited for it, then orchestrate with Claude
subagents using Haiku for mechanical dispatch and Sonnet for multi-source synthesis.

## Why

No single AI tool covers all research stages. Tools that try to cover everything produce
shallow, biased results and lose source attribution. Matching tool to stage improves
citation quality, reduces hallucination risk, and makes the pipeline auditable.
95% of researchers now use AI tools regularly (2025); the key differentiator is
task-specific tool assignment, not general-purpose chat.

## When To Use

- Building or instrumenting a multi-stage research pipeline for a geek/agent project
- Selecting the right tool before starting any structured literature or market sweep
- Producing synthesis reports from heterogeneous sources (news, academic, market data)
- Citation tracking and source verification is required

## When NOT To Use

- Primary source collection requiring human judgment (expert interviews, observation)
- Legally sensitive research where AI hallucination risk is unacceptable
- Real-time data requiring live API access beyond what exposed tools support
- Tasks where source provenance must be court-admissible or regulatory-grade

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-stack.xml` | Stage-to-tool mapping, workflow steps, best-practice rules |
| `content/02-agentic-patterns.xml` | Orchestrator pattern, prompt templates, CLI/SaaS table, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/research-dispatch.py` | Claude SDK dispatcher for multi-source synthesis |
| `templates/research-prompt.txt` | XML prompt template for research and synthesis tasks |

## Scripts

none
