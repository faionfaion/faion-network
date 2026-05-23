---
slug: quality-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Three-process framework (Plan / Manage / Control) with machine-readable DoD per repo, automated PR gate, and weekly metric collection separating must/should items to preserve velocity.
content_id: "3d23e184e7b5346c"
complexity: medium
produces: config
est_tokens: 4000
tags: [quality-management, definition-of-done, defect-management, quality-metrics, testing]
---
# Quality Management

## Summary

**One-sentence:** Three-process framework (Plan / Manage / Control) with machine-readable DoD per repo, automated PR gate, and weekly metric collection separating must/should items to preserve velocity.

**One-paragraph:** Three-process framework — Plan Quality, Manage Quality, Control Quality — implemented as code-driven gates. Definition of Done is machine-readable (quality/dod.yaml per repo) and versioned. Quality gates run twice: pre-commit (fast — lint, format) and pre-merge (full — tests, coverage, security scan). Defect escape rate is tracked with SPC charting as a leading indicator. Must items block merge; should items open follow-up issues. Prevention beats detection (Deming).

**Ефективно для:**

- Defining DoD across a multi-team / multi-repo product
- Defect-escape rate climbing or production incidents recurring on same surfaces
- Pre-release hardening: quality audit before major launch
- Compliance kickoff (SOC2, ISO 9001) where evidence trail must be reproducible

## Applies If (ALL must hold)

- Setting Definition of Done across a multi-team or multi-repo product
- Defect-escape rate climbing or production incidents recurring on the same surfaces
- Codebase has no quality dashboard and PM/PO cannot answer trend direction
- Pre-release hardening: agent-driven quality audit before a major launch
- Compliance kickoff (SOC2, ISO 9001) where evidence trail must be reproducible

## Skip If (ANY kills it)

- One-person prototype before product-market fit — quality gates slow validation
- Spike or research code marked throwaway — formal QC inflates effort 2-3x
- When the team rejects DoD as ceremony — fix the trust issue first
- Aesthetic UX polish — use design review, not quality management process

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-repo standards | YAML | team consensus + tech lead |
| Coverage / lint config | config files | engineering |
| Defect history | JSON / CSV | issue tracker export |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[project-integration]] | DoD outcomes feed integrated status |
| [[risk-management]] | Quality failures become risks if not addressed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: dod-as-code, must-vs-should-split, twice-not-duplicated, escape-rate-leading-indicator, higher-bar-for-agent-code | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output per step | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `validate-dod` | haiku | Mechanical line-item check against dod.yaml |
| `triage-defect` | sonnet | Severity/priority with rationale; awaits human confirmation |
| `trend-analysis` | sonnet | SPC charting on escape rate + MTTR |

## Templates

| File | Purpose |
|------|---------|
| `templates/dod.yaml` | Machine-readable Definition of Done with must/should items and scope tags |
| `templates/defect-report.md` | Defect report template with severity, steps, environment, root cause |
| `templates/quality-checklist.md` | Pre-ship quality checklist (code, testing, performance, security, accessibility) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-quality-management.py` | Validate dod.yaml shape + pass/fail summary from CI inputs | Pre-commit; PR gate |

## Related

- parent skill: `pro/pm/project-manager/`
- [[project-integration]]
- [[risk-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
