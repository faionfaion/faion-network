<!-- __faion_header_v1__ -->
<!-- purpose: Markdown audit report skeleton: per-item PASS/WARN/FAIL with remediation -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: rubric -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: ~260 tokens when loaded as context -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Markdown audit report skeleton: per-item PASS/WARN/FAIL with remediation","consumes":"see content/02-output-contract.xml","produces":"rubric","depends_on":"content/02-output-contract.xml","token_budget_impact":"~260 tokens when loaded as context"}} -->
# 2026 Best-Practices Audit — <repo-name>

Generated <date>; baseline rubric version 2026.1.

| Item | Status | Weight | Evidence | Remediation |
|------|--------|--------|----------|-------------|
| ts-strict | PASS | 3 | tsconfig.json line 12 | — |
| react-19-suspense | WARN | 2 | 3 of 7 server components | wrap remaining fetches in `<Suspense>` |
| py-3-13-strict | FAIL | 3 | mypy --strict emits 18 errors | fix or add per-module ignores |

## Top remediation order
1. ...
