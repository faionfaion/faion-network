---
slug: framework-decomposition-patterns
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an LLM-friendly decomposition report classifying fat files / God models per framework (Django, Rails, Laravel, React) and proposing extraction patterns (service layer, selectors, DTOs, hooks).
content_id: "96276615e91597b6"
complexity: medium
produces: report
est_tokens: 4000
tags: [framework-patterns, code-organization, refactoring, llm-friendly, service-layer]
---
# Framework Decomposition Patterns

## Summary

**One-sentence:** Cap framework files at 150-200 lines per type via extraction patterns (service layer, selectors, DTOs, query objects, actions, custom hooks) so a single LLM Read fits in &lt;20K tokens.

**One-paragraph:** Fat controllers and God models are the LLM-context killer of legacy codebases. A 500-line Django view forces a coding agent to load 50K tokens to make a 2-line edit; the agent then mis-references, drops imports, and slows. The fix is per-framework decomposition: extract the right pattern (service layer for Rails / Django, query objects + selectors for React, DTOs for Laravel, actions + hooks for SPA frontends). This methodology produces a decomposition report per fat file: current LoC, proposed extraction pattern, target LoC after, AI-context savings, and the test set that proves equivalence. The script `find-fat-files.sh` surfaces candidates; the JS variant `find-fat-components.mjs` does the same for React.

**Ефективно для:**

- Solo dev preparing a legacy codebase for Claude Code / Cursor — files over 200 lines defeat AI-pair coding.
- Refactor sprint targeting LLM-context efficiency rather than micro-perf.
- Onboarding LLM agent into a fat-model Rails / Django repo.
- DRY audit: surface candidates whose churn justifies the decomposition.

## Applies If (ALL must hold)

- Existing codebase using Django, Rails, Laravel, React (or close equivalents).
- One or more files exceed 150 lines AND change-frequency is non-trivial (≥5 commits in 90 days).
- LLM-assisted dev is part of the workflow OR planned.
- Test coverage exists OR characterization tests will be added (see `characterization-test-recipes`).

## Skip If (ANY kills it)

- Tiny scripts, one-off Lambdas, files already under 100 lines.
- Prototypes being thrown away weekly (YAGNI).
- Frameworks with opinionated structure already enforcing the boundary (Phoenix contexts, NestJS modules).
- Microservices where one service = one concern; extra layers duplicate boundaries.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target file path(s) | string | `find-fat-files.sh` output |
| Framework | string | repo config |
| Change-frequency data | git log | repo |
| Test coverage (or characterization plan) | report / plan | tests/ + roadmap |
| AI-context budget target | tokens | team handbook |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/characterization-test-recipes` | Pre-refactor safety net for behavior-preserving decomposition. |
| `solo/dev/context-window-curation-for-coding-agents` | Downstream: bounded files feed bounded context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 14 rules: per-framework patterns, LoC caps, naming, run + skip | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decomposition report + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: extract-then-re-merge, wrong-pattern-per-framework, untested-refactor, LoC-only metric | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: identify → choose-pattern → write-characterization → extract → verify | 700 |
| `content/06-decision-tree.xml` | essential | Tree: framework? file-type? recommended pattern → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `find-fat-files` | haiku | Mechanical LoC + change-freq scan. |
| `propose-pattern` | sonnet | Bounded judgment: which extraction pattern fits this fat file. |
| `verify-equivalence` | sonnet | Run characterization tests; compare pre/post. |

## Templates

| File | Purpose |
|------|---------|
| `templates/framework-decomposition-patterns.json` | JSON Schema for the decomposition report. |
| `templates/find-fat-files.sh` | Bash helper to surface fat files by LoC + change-freq. |
| `templates/find-fat-components.mjs` | JS helper to surface fat React components by LoC + jsx-depth. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-framework-decomposition-patterns.py` | Validate a decomposition report against the schema + pattern-framework consistency. | After proposal; before extraction. |

## Related

- [[characterization-test-recipes]] — safety net for the extraction.
- [[context-window-curation-for-coding-agents]] — bounded files = bounded context.
- [[code-quality/tech-debt-management]] — sibling for picking which fat files to fix first.

## Decision tree

See `content/06-decision-tree.xml`. The tree first determines the framework (django / rails / laravel / react / generic). It then routes the fat-file type (view / controller / model / component / route) to the recommended extraction pattern. Then verifies test coverage exists OR characterization-test plan attached. Leaves emit `propose-extraction`, `block-no-coverage`, or `block-pattern-not-applicable`. Each leaf references a rule in `01-core-rules.xml`.
