---
slug: ai-assisted-lessons-learned-synthesis
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "4554a0024e3c4f3b"
summary: AI-assisted recipe for clustering retro notes across multiple projects to produce a synthesized lessons-learned doc with attributable themes and action items.
tags: [retro, lessons-learned, ai-agent, project-management, clustering, synthesis]
---
# AI-Assisted Lessons-Learned Synthesis

## Summary

**One-sentence:** AI-assisted recipe for clustering retro notes across multiple projects to produce a synthesized lessons-learned doc with attributable themes and action items.

**One-paragraph:** Annual delivery-process maturity reviews and project closures produce sprawling retro notes; manual synthesis takes 8-15 hours and quality varies with the synthesizer. Mechanism: ingest 6-24 months of project retros (Markdown / Confluence / Notion exports), use an LLM to (1) deduplicate similar lessons, (2) cluster into themes with quote evidence, (3) score each theme by recurrence + severity, (4) propose 5-10 prioritized action items with named owners. The agent's output is ALWAYS traceable: every theme links back to verbatim quotes from source retros. Output: a 2-3 page synthesized doc + a longer themed appendix for deep dives.

## Applies If (ALL must hold)

- you have ≥ 5 project retros from the past 18 months in a searchable format
- retros are written (not verbal-only) — text required for ingestion
- a project manager or delivery lead owns the synthesis
- AI tooling available (Claude Code, Claude API, or similar)
- annual / semi-annual review cadence has a deadline

## Skip If (ANY kills it)

- &lt; 5 retros — too small a sample for meaningful clustering
- retros not written down — start with the retro-writing methodology first
- single team / single project — manual synthesis is faster than agent setup
- highly sensitive retro content (HR incidents, IP disputes) — keep manual to avoid AI processing of confidential material

## Prerequisites (must be true before starting)

- folder of retro docs accessible (Markdown / PDF / HTML export)
- retro docs structured with sections (what went well / didn't / actions)
- agreement on the audience for the synthesis (founder, leadership, all-hands)
- LLM API access + sample budget
- a baseline of past synthesis quality so the agent output can be calibrated

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/kb-codebase-rag-symbol-chunked` | RAG pattern adapted for retro docs |
| `geek/sdlc-ai/kb-versioned-agent-memory-files` | Memory of previous synthesis informs next cycle |
| `pro/pm/project-manager/agile-ceremonies-setup` | Source of retro templates the synthesis assumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: verbatim citations, no fabricated themes, severity + recurrence scoring, named owners on actions, human edit pass | ~900 |
| `content/02-output-contract.xml` | essential | Synthesis doc schema, theme + evidence schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (hallucinated themes, recency bias, anonymity collapse, PII leak, action without owner, scope explosion) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `retro_ingestion_and_dedup` | sonnet | Per-doc parsing + near-duplicate detection |
| `theme_clustering` | opus | Cross-doc synthesis, semantic grouping |
| `severity_recurrence_scoring` | sonnet | Per-theme deterministic scoring |
| `action_item_proposal_with_owner` | opus | Cross-theme reasoning + org-knowledge |
| `executive_summary_draft` | sonnet | Templated narrative compression |

## Templates

| File | Purpose |
|------|---------|
| `templates/synthesis-doc.md` | Final 2-3 page synthesis structure |
| `templates/themed-appendix.md` | Long-form appendix with theme deep-dives |
| `templates/action-item-table.md` | Action items with owners + deadlines |
| `templates/source-citation-format.md` | Verbatim quote → retro source schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/ingest-retros.py` | Load retro docs into a normalized JSON structure | Synthesis kickoff |
| `scripts/validate-synthesis.py` | Verify every theme has ≥ 2 verbatim quotes + traceable sources | Pre-publication |

## Related

- parent skill: `geek/sdlc-ai/`
- peer methodologies: `kb-ai-assisted-quarter-retro-synthesis`, `kb-versioned-agent-memory-files`
- external: [Norm Kerth - Project Retrospectives (2001)](https://www.amazon.com/Project-Retrospectives-Handbook-Team-Reviews/dp/0932633447) · [Esther Derby - Agile Retrospectives](https://pragprog.com/titles/dlret/agile-retrospectives/) · [Anthropic - Long context for document synthesis](https://www.anthropic.com/news/100k-context-windows)
