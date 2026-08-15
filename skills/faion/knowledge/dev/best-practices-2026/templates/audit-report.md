<!-- __faion_header_v1__ -->
<!-- purpose: Markdown audit report skeleton — per-rule PASS/WARN/FAIL with evidence and remediation -->
<!-- consumes: scored rubric from templates/rubric.json -->
<!-- produces: report -->
<!-- depends-on: content/04-procedure.xml -->
<!-- token-budget-impact: ~260 tokens when loaded as context -->
# 2026 Best-Practices Audit — <repo-name>

Generated <date>; baseline rubric version 2026.1; snapshot version <snapshot_version>.

| Rule | Status | Weight | Evidence | Remediation |
|------|--------|--------|----------|-------------|
| r4-ts-strict-flags | PASS | 3 | tsconfig.json:12 | — |
| r5-react-19-patterns | WARN | 2 | 3 of 7 server components | wrap remaining fetches in `<Suspense>` |
| r9-ruff-mypy-strict | FAIL | 3 | mypy --strict emits 18 errors | fix, or add per-module ignores with an owner |

## Remediation order

Ordered by weight x blast radius; strictness flips first.

1. ...

## Constitution extraction

Rules extracted into `constitution.md` this pass: <rule-ids>. Next drift scan due: <date + 90d>.
