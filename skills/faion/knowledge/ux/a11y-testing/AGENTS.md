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

| Methodology | Why |
|-------------|-----|
| a11y-basics | Provides WCAG POUR / conformance vocabulary used across the accessibility-specialist domain. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with sourced rationale + skip-this-methodology + run-the-checklist | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure (input / action / output / decision-gate) | 800 |
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
| `templates/audit-report.md` | Markdown skeleton for the audit narrative. |
| `templates/a11y-scan.sh` | axe + pa11y + lighthouse CI wrapper. |
| `templates/audit-findings.json` | JSON findings skeleton matching the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-a11y-testing.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[a11y-basics]]
- [[wcag-22-compliance]]
- [[testing-with-assistive-technology]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
