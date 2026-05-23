<!--
purpose: 12-row trace skeleton the reviewer fills before submitting.
consumes: nothing — this IS the reviewer's working sheet.
produces: trace → JSON via scorer.
depends-on: PR open + lockfile + repo conventions.
token-budget-impact: ~180 tokens when copied.
-->

# AI Code Review trace — &lt;pr_ref&gt;

- ai_pct_lines:
- reviewer_email:

| # | check | verdict | notes |
|---|-------|---------|-------|
| 01 | hallucinated-imports        | | |
| 02 | silent-skip-tests           | | |
| 03 | convention-drift            | | |
| 04 | supply-chain                | | |
| 05 | secret-exposure             | | |
| 06 | deferred-debt               | | |
| 07 | error-handling-coverage     | | |
| 08 | overscoped-changes          | | |
| 09 | test-quality                | | |
| 10 | perf-regression             | | |
| 11 | deferred-impl               | | |
| 12 | ai-disclosure               | | |

verdict (aggregate): approve | request-changes | block
block_reason (if block):
