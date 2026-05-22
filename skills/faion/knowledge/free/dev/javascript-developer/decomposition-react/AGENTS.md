---
slug: decomposition-react
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Breaks large React components into custom hooks + feature folders + service layers, capping each file at 80 lines for LLM readability.
content_id: "04ada1bff3825ae8"
complexity: medium
produces: playbook-step
est_tokens: 3500
tags: [react, decomposition, hooks, feature-folders]
---
# React Decomposition

## Summary

**One-sentence:** Splits React components past 80 lines into custom hooks, feature folders, and service modules so each file fits an agent's working context.

**One-paragraph:** React components past ~80 lines collapse LLM editing accuracy. This methodology pulls non-render logic into custom hooks (`useX`), groups by feature (not by type), and pushes I/O into a thin services layer. Output is a per-component decomposition plan: identify render vs logic vs I/O, propose the new file tree, list the hooks to extract. The 80-line rule is a budget — past that, agents start guessing.

**Ефективно для:**

- React-репо з компонентами 300+ рядків: знизити cognitive load для людини + агента.
- Migration legacy class-based → functional + hooks.
- Storybook + test coverage: малі компоненти легше mock-ати.
- RSC (React Server Components): чітке розмежування server / client логіки.

## Applies If (ALL must hold)

- React project (functional components + hooks).
- At least one component &gt; 80 lines OR &gt; 200 LOC.
- Tests exist for current behaviour (so refactor stays safe).

## Skip If (ANY kills it)

- Class-based React legacy — different decomposition methodology (still useful but signature differs).
- Generated UI (auto-codegen from Figma) — splitting fights the generator.
- Tests broken — fix tests first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Component file path | absolute | project tree |
| LOC + token count | integer | wc -l + tokenizer |
| Render vs logic vs I/O map | static analysis | manual or LSP |
| Test command | shell | package.json scripts |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 80-line-budget, hooks-for-logic, feature-folders, services-for-io, test-between-moves | 1000 |
| `content/02-output-contract.xml` | essential | Schema for decomposition plan | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: prop-drilling-replaced-by-context, hooks-misused, by-type-folders | 700 |
| `content/04-procedure.xml` | essential | 5-step decomposition | 700 |
| `content/06-decision-tree.xml` | essential | Component shape tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_concerns` | sonnet | Per-component judgement. |
| `draft_plan` | sonnet | Maps concerns to hooks + services. |
| `execute` | haiku | Mechanical moves once plan is set. |

## Templates

| File | Purpose |
|------|---------|
| `templates/useFeature.hook.ts` | Custom hook skeleton |
| `templates/feature-folder.tree.txt` | Feature-folder layout reference |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decomposition-react.py` | Validate decomposition plan + 80-line budget | Before applying moves |

## Related

- - [[code-decomposition-patterns]] — language-agnostic patterns this specialises.
- - [[javascript-modern]] — TS-strict + named-exports apply here too.

## Decision tree

See `content/06-decision-tree.xml`. Branches on what dominates the component: logic-heavy → extract hook. I/O-heavy → extract service. State-heavy → extract reducer + context. Multi-feature → split into feature folders.
