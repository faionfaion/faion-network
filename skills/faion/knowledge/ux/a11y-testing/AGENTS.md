# Accessibility Testing Process

## Summary

**One-sentence:** End-to-end accessibility testing process combining automated scan, manual keyboard pass, AT testing, and disabled-user feedback into a single audit report.

**One-paragraph:** Accessibility testing without process produces inconsistent audits where different reviewers reach different verdicts. This methodology pins a four-layer process — automated scan (axe + pa11y + lighthouse), manual keyboard pass, AT testing on at least two screen readers, and structured disabled-user feedback — and aggregates findings into one prioritised report. Output is an audit report validated against the schema before delivery.

**Ефективно для:**

- Four-layer process closes the ~70% gap that scanners miss.
- Audit-grade reports usable for VPAT and procurement.
- Per-issue severity (blocker / major / minor) prioritises remediation.
- Disabled-user feedback weighted heavier than synthetic findings.

## Applies If (ALL must hold)

- Product is mid- to large-sized and requires an audit-grade report.
- Audit budget supports four testing layers within the same window.
- WCAG 2.2 AA (or higher) is the conformance target.

## Skip If (ANY kills it)

- ≤1 screen / quick sweep — use `a11y-basics`.
- Compliance paperwork only — use `regulatory-compliance-2026`.
- Pure scanner pass with no AT — produces non-audit-grade output.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target product / flows | URL list | product |
| WCAG target | string (default 2.2 AA) | team policy |
| AT environment | NVDA / VoiceOver / TalkBack installed | tester rig |
| Disabled-user panel | ≥3 participants OR explicit waiver | research |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| a11y-basics | Provides WCAG POUR / conformance vocabulary used across the accessibility-specialist domain. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 11 testable rules with sourced rationale (four layers, AT pair, severity enum, user-panel weighting, evidence, axe+Pa11y union, keyboard walkthrough, NVDA+Firefox / VoiceOver+Safari, bug links criterion + screenshot, priority rubric, CI per-PR + release diff) + skip-this-methodology + run-the-checklist; Background: agentic pipeline roles | 2050 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom + root-cause + fix, including axe "0 violations" as conformance and unbounded auto-fix loops | 900 |
| `content/04-procedure.xml` | essential | Seven-step procedure (input / action / output / decision-gate): scope, automated, keyboard, AT with SR checklist, cognitive, user panel + aggregate, CI integration | 850 |
| `content/05-examples.xml` | essential | Reference tables: automated find/miss, keyboard test matrix, priority rubric; audit-report and a11y-scan templates | 800 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs (preconditions, severity, modality) to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `triage-inputs` | haiku | Mechanical scrape from inputs. |
| `apply-rules` | sonnet | Per-rule judgement on inputs. |
| `synthesise-artefact` | sonnet | Aggregates rule outcomes into the final artefact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-report.md.j2` | Markdown skeleton for the audit narrative. |
| `templates/audit-report.md` | Markdown skeleton for the audit narrative. Generated from `templates/audit-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/audit-findings.json` | JSON findings skeleton matching the schema. |
| `templates/a11y-scan.sh` | Automated-layer CI wrapper: axe + pa11y + lighthouse per URL, findings normalised to the severity enum with evidence_url, summary.md marks the other three layers Not Tested. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-a11y-testing.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[a11y-basics]]
- [[wcag-22-compliance]]
- [[testing-with-assistive-technology]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
