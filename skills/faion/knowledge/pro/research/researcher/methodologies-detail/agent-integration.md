# Agent Integration — Methodologies Detail (index/reference)

## What this directory is

`methodologies-detail/` is **not** a standalone methodology. It is a flat
reference page that bundles 20 already-existing methodologies extracted from
`SKILL.md v1.1` (idea-generation, paul-graham-questions, pain-point-research,
niche-evaluation, market-research-tam-sam-som, trend-analysis,
competitor-analysis, competitive-intelligence, user-interviews,
jobs-to-be-done, persona-building, problem-validation, pain-point-mining,
niche-viability-scoring, business-model-research, value-proposition-design,
project-naming, domain-availability, pricing-research,
customer-interview-framework). It exists for human/agent skim-reading; the
canonical, agent-actionable copies live in their own sibling folders under
`pro/research/researcher/` and `pro/research/market-researcher/` /
`pro/research/user-researcher/`.

Therefore, per the BRIEF "too thin for a useful deliverable" clause, no new
agent-integration content is created here. Doing so would duplicate (and
drift from) the 20 per-methodology folders that each already need their own
`agent-integration.md`.

## How agents should use this folder

- Treat `README.md` as a TOC + cheat-sheet only. Do **not** parse it as the
  source of truth for any single methodology — fields are abridged and the
  `### Agent` line is a stub (`faion-research-agent (mode: ...)`).
- For real execution, route to the per-methodology folder, e.g.
  `pro/research/market-researcher/market-research-tam-sam-som/README.md`.
- The mode→methodology map already lives in
  `pro/research/researcher/CLAUDE.md` (`## Research Modes` table). Use that,
  not this index, for orchestrator routing.

## Recommended subagents

- `faion-research-agent` — 9-mode orchestrator; consumes individual
  methodology folders, never this aggregated page.
- `faion-domain-checker-agent` — only used for `domain-availability`.

## Where to add real content

Each of the 20 listed methodologies should get its own `agent-integration.md`
inside its own folder. This index page should remain a static TOC.

## References

- Sibling: `../CLAUDE.md` (mode routing, output files)
- Sibling: `../SKILL.md` (full methodology pointers)
- BRIEF rule: `skills/faion/.research/BRIEF.md` §"too thin" clause
