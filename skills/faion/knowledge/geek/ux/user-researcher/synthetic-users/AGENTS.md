# Synthetic Users

## Summary

Methodology for using AI-generated research participants to produce directional feedback during early ideation — covering persona simulation, interview analysis, and the mandatory gate of validating key findings with at least 3 real users before any product decision. Synthetic users are directional tools, never confirmatory evidence.

## Why

Real user research is slow and expensive. Synthetic users (Claude, GPT-4, Synthetic Users API, Viewpoints.ai) provide 0-cost, hours-turnaround directional feedback that stress-tests assumptions before committing to a study design. The critical failure mode is sycophancy: AI-generated users skew positive, lack nonverbal signals, and hallucinate domain knowledge in specialist fields. A validation gate to real users is non-negotiable.

## When To Use

- Early ideation: generating directional feedback on concepts before recruiting real participants
- Hypothesis generation: stress-testing assumptions with AI-simulated user archetypes
- Rapid concept testing at zero research budget when timeline is days, not weeks
- Producing illustrative failure scenarios for edge-case personas (low-literacy, non-native speakers)
- Supplementing thin real-user datasets when recruitment would delay a critical decision

## When NOT To Use

- Go/no-go product decisions — synthetic feedback is directional only, never confirmatory
- Demand forecasting or willingness-to-pay studies — AI is trained on text, not economic behavior
- Sensitive population research (healthcare, legal, financial) — bias and hallucination risk is unacceptable
- Any study output presented to investors or regulators as real user evidence
- When you already have access to real users — synthetic users do not improve on real data

## Content

| File | What's inside |
|------|---------------|
| `content/01-methodology.xml` | Valid use cases, validation framework, governance rules, limitations |
| `content/02-simulation-workflow.xml` | Subagent patterns, persona simulation prompt, interview analysis prompt, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/panel-simulation.py` | Run multi-persona synthetic interview panel via Claude API |
| `templates/prompt-persona-sim.txt` | System prompt for synthetic user interview simulation |
| `templates/prompt-transcript-analysis.txt` | Prompt for extracting themes from synthetic interview transcripts |
