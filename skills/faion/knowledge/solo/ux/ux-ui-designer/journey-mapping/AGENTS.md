# Customer Journey Mapping

## Summary

Visualize the complete experience a user has with a product over time — stages, actions,
touchpoints, thoughts, emotions, pain points, and opportunities. Use to find cross-channel
friction and align stakeholders on the current-state experience before designing
improvements. Always ground every map cell in cited research; "no data" is a valid value.

## Why

Teams that optimize individual touchpoints miss the overall experience. Handoffs between
channels and departments cause friction that no single team owns. A journey map makes the
full arc visible in one artifact, surfacing pain points at stage transitions that cannot
be seen from analytics alone. The emotional arc — where it dips sharply — shows where to
invest redesign effort.

## When To Use

- Designing or redesigning a multi-step flow (onboarding, checkout, support, offboarding)
- After collecting user interviews or analytics data revealing cross-touchpoint pain points
- Before a product discovery sprint to align stakeholders on the current-state experience
- Evaluating a new feature's impact on the broader experience, not just its own screen

## When NOT To Use

- No research data exists — a purely imagined journey map creates false consensus
- Single, isolated interaction with no multi-step journey
- Need to understand why users behave a certain way — use user interviews or usability testing instead
- Stakeholders want quantitative evidence — journey maps are qualitative synthesis, not metrics

## Content

| File | What's inside |
|------|---------------|
| `content/01-components.xml` | Eight map components (persona, stages, actions, touchpoints, thoughts, emotions, pain points, opportunities); journey types |
| `content/02-process.xml` | Seven-step mapping process: scope → research → stages → actions → emotions → pain points → visualize |
| `content/03-examples.xml` | E-commerce purchase journey example; workshop format; metrics per stage; agentic workflow patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/journey-map.md` | Full journey map: stage × row matrix (actions, touchpoints, thoughts, emotions, pain points) |
| `templates/stage-detail.md` | Single stage deep-dive: user goal, actions, touchpoints, thoughts, emotional state, opportunities |
| `templates/funnel-to-stages.py` | Python: convert funnel analytics CSV to stage summaries for agent ingestion |
| `templates/prompt-map.txt` | LLM prompt for synthesizing a journey map from interview excerpts and support ticket data |
