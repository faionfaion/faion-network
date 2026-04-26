# User Validation Methods

## Summary

A router methodology that covers four validation lenses in a single entry point: JTBD (why users hire products), Persona Building (who users are), Problem Validation (does this problem exist and matter), and Pain Point Mining (where users express frustration publicly). Use this file to route a research question to the correct sub-methodology; each lens has a dedicated directory with full content. Do not use this file as a substitute for running any individual methodology thoroughly.

## Why

Discovery sprints often need multiple validation lenses in sequence. Having a router reduces the cognitive overhead of choosing the right methodology; the routing logic ("what is the user trying to accomplish?" → JTBD) makes methodology selection deterministic. Without a router, researchers default to the methodology they know best rather than the one that answers the current question.

## When To Use

- Running a structured discovery sprint that needs multiple lenses in sequence: JTBD → persona → problem validation → pain mining
- Onboarding to the research toolkit via a single entry point
- Agent orchestration: routing a research question to the correct sub-methodology based on question type
- When a combined workflow is needed (e.g., build personas, then validate the top pain point per persona)

## When NOT To Use

- When one specific methodology already answers the question — go to that methodology's directory directly
- As a substitute for running any individual methodology thoroughly — this file coordinates, not replaces
- When no qualitative data exists yet — start with pain-point-research, not the combined workflow
- When the research question is about usability (watch users act) rather than motivation or pain (interview)

## Content

| File | What's inside |
|------|---------------|
| `content/01-routing-and-workflow.xml` | Routing rules, canonical ordering, combined workflow, methodology router script |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-route.txt` | LLM prompt to identify the correct methodology for a research question |
| `templates/prompt-combined-workflow.txt` | LLM prompt for a combined pain-mining → validation → JTBD workflow |
| `templates/methodology-router.py` | Keyword-based router that maps research questions to methodology names |

## Sub-methodology Directories

| Methodology | Directory | When to route |
|-------------|-----------|---------------|
| JTBD | `../jobs-to-be-done/` | "What is the user trying to accomplish?" |
| Persona Building | (see user-researcher skill) | "Who is the user?" |
| Problem Validation | `../problem-validation/` | "Does this problem really exist and matter?" |
| Pain Point Mining | `../pain-point-research/` | "Where do users express frustration online?" |
