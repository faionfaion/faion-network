---
slug: dependency-graph-reasoning
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "4d49f7e0f19d1be7"
summary: Builds, maintains, and queries a cross-task / cross-team dependency graph for multi-team product PMs — "what is at risk if X slips by 1 week" answered deterministically.
tags: [program-management, dependency-graph, multi-team, risk-analysis, p6-product, geek-pm]
---
# Dependency Graph Reasoning (Geek Tier)

## Summary

**One-sentence:** Builds and maintains a queryable dependency graph across tasks and teams so a program PM can answer "what is at risk if X slips by 1 week" deterministically rather than by tribal knowledge.

**One-paragraph:** Value-stream-management methodologies model flow at the high level; PMBOK Critical Path covers single-program scheduling; neither answers the multi-team query: "Team B's API contract is two weeks late — which Team A tasks are now blocked, which Team C deliverables miss the cross-functional milestone, and what is the minimum re-plan?". This methodology pins five things: (1) extract dependencies into a typed graph (FS / SS / FF / SF + cross-team handoff edges), (2) store the graph as code (Mermaid, DOT, JSON, or a tool-backed file), (3) refresh from source-of-truth trackers weekly, (4) define standard queries (blocked-by, at-risk-if, longest-path), (5) update via PR-style change requests so the graph stays calibrated. Output: a queryable graph file + weekly risk report.

## Applies If (ALL must hold)

- Program involves &gt;= 3 teams contributing to a shared outcome.
- A single program PM (or two) is accountable for cross-team coordination.
- Slips and blockers happen often enough that tribal-knowledge tracking is failing.
- A source-of-truth tracker (Jira, Linear, GitHub Projects) exists per team — even if not unified.

## Skip If (ANY kills it)

- Single-team project — value-stream and sprint-planning methodologies are enough.
- Teams that explicitly run async / no-dependencies — graph would be sparse and noisy.
- Pre-program phase before teams are even assigned — define them first.
- Org has a dedicated PMO tool (Smartsheet, Aha!, Asana Portfolios) maintaining a portfolio graph — extend it, don't fork.

## Prerequisites

- List of teams, leads, and current quarterly objectives.
- Per-team tracker access (or weekly export).
- A graph-storage choice (Mermaid + Markdown, DOT + Graphviz, or a tool — pick one and stay).
- The cross-team milestones / deliverables list.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager/multi-team-coordination` | Coordination ritual / sync cadence assumed. |
| `geek/pm/project-manager/program-risk-management` | Risk register format consumed by the graph queries. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: typed edges, graph-as-code, weekly refresh, standard queries, PR-style updates | ~1000 |
| `content/02-output-contract.xml` | essential | Graph file shape, query output formats, weekly report | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: stale graph, missing edges, fake critical path | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-dependencies-from-trackers` | sonnet | Per-team ticket parsing; bounded judgment |
| `compute-blocked-by` | haiku | Pure graph traversal |
| `at-risk-if-slip-analysis` | opus | Multi-edge what-if scenario reasoning |

## Templates

| File | Purpose |
|------|---------|
| `templates/program-graph.mmd` | Mermaid graph skeleton with team-prefixed node naming |
| `templates/query-format.md` | Standard query shapes: blocked-by, at-risk-if-slip-N-weeks, longest-path-to-milestone |
| `templates/weekly-risk-report.md` | Templated weekly output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/graph-validate.py` | Confirm nodes have team prefix, all edges have type, no cycles | After every update |
| `scripts/query-graph.py` | Run standard queries against the JSON form | Weekly + on demand |

## Related

- parent skill: `geek/pm/project-manager/`
- peer methodology: `multi-team-coordination`, `program-risk-management`, `value-stream-management`
- external: [Critical Path Method (PMBOK)](https://www.pmi.org/) · [Theory of Constraints (Goldratt)](https://www.toc-goldratt.com/) · [Graphviz](https://graphviz.org/) · [Mermaid](https://mermaid.js.org/)
