# Agent Integration — BA Trends Summary

## Status: index/summary, not a methodology

`ba-trends-summary` is a non-procedural index file. The README is a static
list of 6 industry trends (AI-enabled decision making, outcome-driven strategy,
responsible innovation, operational resilience, digital trust, sustainability
integration), critical success factors, and a BA skill-priority table. The
sibling files (`checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md`)
are empty placeholders. There is no executable workflow here for an agent to
drive — no inputs, outputs, artifacts, or stop conditions.

## Why a full agent-integration.md is not warranted

- No procedure to execute, automate, or wrap. Trends are observations, not steps.
- Already declares its own next-update cadence (semi-annual, 2026-06).
- Already contains an "Agent Selection" matrix (sonnet/opus/haiku per task)
  that is itself a routing summary — duplicating it adds noise.
- The 6 trends each map to dedicated sibling methodologies
  (`ai-enabled-business-analysis`, `agile-ba-frameworks`,
  `process-mining-automation`, `data-driven-requirements`, `modern-ba-framework`,
  `ba-strategic-partnership`) — those are the correct targets for agentic
  enrichment, not this summary.

## How agents should treat this file

- Treat as a read-only routing index. When a user asks "what's trending in BA
  for 2026?", load this README and stop.
- For actionable agent workflows, redirect to the linked methodology folders
  (one level up: `business-analyst/<topic>/`) and use their respective
  `agent-integration.md` once produced.
- Do not generate prompts, checklists, or scripts from this file — the parent
  methodologies own that.

## References

- `business-analyst/README.md` (parent skill index)
- `ai-enabled-business-analysis/`, `process-mining-automation/`,
  `modern-ba-framework/` (downstream actionable methodologies)
