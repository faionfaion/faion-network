# A11y Screen Status Tracker

## Summary

**One-sentence:** Per-screen accessibility status tracker (pass / partial / fail) with owner + last-tested + remediation plan for every named screen.

**One-paragraph:** Audits without per-screen state collapse into a single PDF that goes stale within a sprint. This methodology pins one row per screen with status (pass / partial / fail / not-applicable), owner, last-tested date, blocking SC list, and the linked remediation plan. The tracker becomes the audit's living counterpart and survives scope changes. Output is a screen-status spreadsheet record validated against the schema.

**Ефективно для:**

- Living audit state: each sprint shows progress per screen.
- Per-screen ownership prevents 'team' blame.
- Pass / partial / fail / not-applicable verdict supports audit-grade evidence.
- Remediation plan link makes the next fix one click away.

## Applies If (ALL must hold)

- Product has ≥5 distinct screens / flows under accessibility audit.
- An audit must remain usable across sprints (not just snapshot).
- Multiple owners across screens; need clarity who fixes what.

## Skip If (ANY kills it)

- Single-screen tools / extensions — overhead exceeds value.
- Pre-audit phase — finish the audit first.
- Tracker already exists in QA tool with same fields — extend rather than duplicate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Screen inventory | list of screen names + URLs | design system / product map |
| Audit baseline | WCAG 2.2 AA findings per screen | audit |
| Owners + last-tested dates | name + ISO date | team |

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
| `templates/screen-status-tracker.json` | JSON skeleton matching the tracker schema. |
| `templates/screen-status-tracker.csv` | CSV row template for the tracker. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-a11y-screen-status-tracker.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[a11y-basics]]
- [[a11y-testing]]
- [[wcag-22-compliance]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
