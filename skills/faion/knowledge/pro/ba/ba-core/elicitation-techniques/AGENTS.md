# Elicitation Techniques

## Summary

A deterministic technique-selector for the 10 BABOK v3 elicitation techniques (interview, workshop, focus group, observation, survey, document analysis, prototyping, brainstorming, interface analysis, collaborative game). Select a ranked mix of 1-3 techniques based on concrete situation inputs — never a single technique in isolation. Always triangulate: pair at least two techniques where the second challenges the first.

## Why

Stakeholders cannot reliably articulate what they need; the BA must draw it out using the right combination of techniques. The wrong technique wastes sessions or misses whole classes of requirements (e.g., interface analysis is systematically skipped by teams using only the 8-item shortlist). A scored selector with explicit data prerequisites forces transparency about what the team actually knows.

## When To Use

- Early-discovery phase: choosing a technique mix from BABOK's 10 and justifying each pick
- Training or onboarding a junior BA or LLM agent needing a deterministic decision tree
- Mixed-method project where triangulation (interview + observation + document analysis) is needed on the same workflow
- Mid-project scope renegotiation: re-elicit only the changed area with the cheapest adequate technique
- Budget/time pressure: structured selector beats ad-hoc choice when sessions must be minimized

## When NOT To Use

- The technique is already locked by org policy (e.g., regulated industry mandates signed workshops) — skip selection, execute per the sibling `business-analyst/elicitation-techniques/`
- Continuous-discovery shop on a stable product (Teresa Torres cadence) — that is its own pattern
- One-stakeholder, one-sitting situation — just run the interview; selector adds overhead
- Pure UX research with users (not stakeholders) — use `ux-researcher/` techniques instead
- Hackathon or spike — prototype and time-box; no BABOK ceremony needed

## Content

| File | What's inside |
|------|---------------|
| `content/01-techniques.xml` | Full BABOK v3 10-technique catalog with when-to-use per technique, known limitations, and selection decision tree |
| `content/02-agentic.xml` | Agent workflow, subagent roles, prompt patterns for technique-selector and interview-guide agents, AI gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-guide.md` | Interview guide: objectives, background, main, and closing question sections |
| `templates/workshop-agenda.md` | Workshop agenda with time blocks, activity types, materials, and expected outputs |
| `templates/technique-selector.py` | Deterministic BABOK v3 technique scorer from a situation JSON |
