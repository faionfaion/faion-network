# Agent Integration — BA Trends Summary (ba-core)

## Status: index/summary, not a methodology

`ba-core/ba-trends-summary` is the same non-procedural index that lives under
`business-analyst/ba-trends-summary` (already enriched). The README is a static
list of 6 industry trends (AI-enabled decision making, outcome-driven strategy,
responsible innovation, operational resilience, digital trust, sustainability
integration), a critical-success-factors table, and a BA skill-priority table.
Sibling files (`checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`)
are placeholders. There is no executable workflow for an agent to drive — no
inputs, outputs, artifacts, or stop conditions.

## Why a full agent-integration.md is not warranted

- No procedure to execute, automate, or wrap. Trends are observations, not steps.
- README already declares its own next-update cadence (semi-annual, 2026-06).
- README already contains an "Agent Selection" matrix (haiku/sonnet/opus) that
  is itself a routing summary — re-stating it adds noise.
- The 6 trends each map to dedicated sibling methodologies inside `ba-core/`:
  `ai-enabled-business-analysis/`, `agile-ba-frameworks/`,
  `process-mining-automation/`, `data-driven-requirements/`,
  `modern-ba-framework/`, `ba-strategic-partnership/` — those are the correct
  targets for agentic enrichment, and most already have their own
  `agent-integration.md`.

## How agents should treat this file

- Treat as a read-only routing index. When a user asks "what's trending in BA
  for 2026?", load this README and stop.
- For actionable workflows, redirect to the linked methodology folders in
  `pro/ba/ba-core/` and use their respective `agent-integration.md`.
- Do not generate prompts, checklists, or scripts from this file — the parent
  methodologies own that.

## References

- `pro/ba/business-analyst/ba-trends-summary/agent-integration.md` (sibling, identical content)
- `pro/ba/ba-core/ai-enabled-business-analysis/`, `process-mining-automation/`,
  `modern-ba-framework/` (downstream actionable methodologies)
