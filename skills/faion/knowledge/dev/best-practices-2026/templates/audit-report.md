<!--
purpose: Markdown audit report skeleton — per-rule PASS/WARN/FAIL with evidence and remediation
consumes: scored rubric from templates/rubric.json
produces: report
depends-on: content/04-procedure.xml
token-budget-impact: ~260 tokens when loaded as context
variables:
  - name: repo_name
    type: string
    required: true
    description: The repository audited, as owner/name. One repo per report - a monorepo audited as a single unit averages away the one package that is actually failing.
  - name: date
    type: string
    required: true
    description: The date the scan ran, ISO. Drift is measured from this date and the rubric is versioned by year, so an undated report cannot be compared to the next one.
  - name: snapshot_version
    type: string
    required: true
    description: What the scan actually read - the tag, commit SHA or lockfile hash. Without it a PASS cannot be tied to the code that passed, and the next failure looks like a regression.
  - name: extracted_rules
    type: text
    required: true
    description: Which rule ids were promoted into constitution.md this pass. If none were, write none - an audit that extracts nothing every time is a report nobody is acting on.
  - name: next_scan_due
    type: string
    required: true
    description: Date the next drift scan is due, ISO - 90 days out unless you have a reason. Unscheduled audits become annual, and annual audits are archaeology.
-->
# 2026 Best-Practices Audit — {{repo_name}}

Generated {{date}}; baseline rubric version 2026.1; snapshot version {{snapshot_version}}.

| Rule | Status | Weight | Evidence | Remediation |
|------|--------|--------|----------|-------------|
| r4-ts-strict-flags | PASS | 3 | tsconfig.json:12 | — |
| r5-react-19-patterns | WARN | 2 | 3 of 7 server components | wrap remaining fetches in Suspense |
| r9-ruff-mypy-strict | FAIL | 3 | mypy --strict emits 18 errors | fix, or add per-module ignores with an owner |

## Remediation order

Ordered by weight x blast radius; strictness flips first.

1. ...

## Constitution extraction

Rules extracted into `constitution.md` this pass: {{extracted_rules}}. Next drift scan due: {{next_scan_due}}.
