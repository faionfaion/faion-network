---
slug: accessibility-evaluation
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Five-stage WCAG 2.1/2.2 AA audit report: automated scan, triage, keyboard, screen reader, structured findings with W3C-technique citations.
content_id: "91d3d5badacc2e25"
complexity: deep
produces: report
est_tokens: 5000
tags: [wcag, accessibility, a11y, audit, testing]
---
# Accessibility Evaluation

## Summary

**One-sentence:** Five-stage WCAG 2.1/2.2 AA audit report: automated scan, triage, keyboard, screen reader, structured findings with W3C-technique citations.

**One-paragraph:** Five stages: (1) automated scan (axe-core + Pa11y + Lighthouse) — catches 30-40% of issues; (2) triage with WCAG SC mapping + priority classification; (3) scripted Playwright keyboard traces; (4) human screen-reader verification on the established AT pairings (NVDA+FF, JAWS+Chrome, VoiceOver+Safari, TalkBack+Chrome); (5) POUR-grouped report with W3C technique citations. Pin axe-core version per repo; stable WCAG-SC IDs so re-runs diff. Screen-reader stage is human-only; agent-fabricated AT transcripts are undetectable and produce false compliance records.

**Ефективно для:**

- Pre-release WCAG 2.1/2.2 AA аудит перед launch — структуровані evidence для VPAT.
- Regression check after design-system upgrade — diff проти previous report.
- RFP / procurement: VPAT/ACR documentation з W3C-technique citations.
- CI gating на PR що чіпає shared library components.

## Applies If (ALL must hold)

- Web product targeting WCAG 2.1 AA or 2.2 AA conformance.
- Audit results must be defensible (VPAT/ACR or legal context).
- Both automated and AT-based verification are feasible.

## Skip If (ANY kills it)

- Early lo-fi wireframe stage — use accessibility-first-design heuristics.
- Native iOS/Android — use Accessibility Inspector + Accessibility Scanner.
- PDF/document accessibility — use PAC 2024 or Acrobat Pro.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Site/app URL or build | URL or local server | build pipeline |
| axe-core version pin | semver | repo lockfile |
| AT pairings inventory | list | this methodology |
| WCAG version target | 2.1 or 2.2 | product brief |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[wcag-22-compliance]] | Source of WCAG SC reference text and severity rubric |
| [[accessibility-first-design]] | Heuristics used to filter false positives in triage |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: tools-30-40-pct, pin-axe-version, keyboard-coverage, spa-post-route, at-pairings, no-fabricated-AT-transcripts | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for findings report + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: placeholder-alt, dark-mode-regression, redundant-aria-label, axe-clean-equals-compliant | 800 |
| `content/04-procedure.xml` | essential | 5 steps: scan → triage → keyboard → screen-reader → report | 900 |
| `content/05-examples.xml` | essential | Worked example: triage of 3 axe findings into POUR report rows | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree: finding source → priority + stage | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scanner` | haiku | Mechanical execution of axe + Pa11y CLI. |
| `triage` | sonnet | Dedup + WCAG SC mapping needs judgement. |
| `keyboard-trace` | sonnet | Playwright trace interpretation. |
| `writer` | sonnet | POUR-grouped markdown report. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-report.md` | POUR-grouped findings report skeleton with W3C-technique citations |
| `templates/scan.mjs` | axe-core + Pa11y + Lighthouse runner emitting normalised JSON |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-accessibility-evaluation.py` | Validate audit-report JSON against the schema | Pre-commit / pre-VPAT |

## Related

- [[accessibility-first-design]]
- [[wcag-22-compliance]]
- [[a11y-annotation-pattern-library]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
