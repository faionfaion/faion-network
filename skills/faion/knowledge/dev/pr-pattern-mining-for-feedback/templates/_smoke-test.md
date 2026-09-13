<!-- purpose: filled-in canonical feedback report for calibration (billing team, Q2 2026) -->
<!-- consumes: nothing — this is a hand-filled fixture -->
<!-- produces: report instance that MUST validate via scripts/validate-pr-pattern-mining-for-feedback.py -->
<!-- depends-on: templates/output.md, content/02-output-contract.xml -->
<!-- token-budget-impact: ~1100 tokens -->

# PR Pattern Mining For Feedback — Smoke Test Fixture

The valid example from `content/02-output-contract.xml`; `scripts/validate-pr-pattern-mining-for-feedback.py --self-test` runs it.

```json
{
  "scope": {
    "kind": "team",
    "per_author_counts_listed": false
  },
  "corpus": {
    "repositories": [
      "acme/billing-api",
      "acme/billing-worker"
    ],
    "window_start": "2026-04-01",
    "window_end": "2026-06-30",
    "merged_prs": 64,
    "review_comments": 412,
    "query": "gh api graphql -f query='{ repository(owner:\"acme\", name:\"billing-api\") { pullRequests(states:MERGED, first:100, orderBy:{field:UPDATED_AT, direction:DESC}) { nodes { number mergedAt reviewThreads(first:100) { nodes { comments(first:50) { nodes { author { login } body url } } } } } } } }' (both repos, filtered to mergedAt in window)",
    "sufficient_sample": true
  },
  "ranking_basis": "review_round_trips",
  "top_patterns": [
    {
      "id": "p1",
      "behaviour": "HTTP client call without a timeout: `requests.get(url)` blocks the worker indefinitely when the upstream hangs",
      "before_example": "resp = requests.get(url)",
      "after_example": "resp = requests.get(url, timeout=(3, 10))",
      "distinct_prs": 11,
      "distinct_reviewers": 4,
      "comment_urls": [
        "https://github.com/acme/billing-api/pull/402#discussion_r1890011",
        "https://github.com/acme/billing-api/pull/417#discussion_r1890877",
        "https://github.com/acme/billing-worker/pull/88#discussion_r1891204"
      ],
      "count": 14,
      "cost": 2.1,
      "score": 29.4,
      "baseline_count": 14,
      "remeasure_date": "2026-09-30",
      "formatter_coverable": false
    },
    {
      "id": "p2",
      "behaviour": "Test asserts only the HTTP status code; the response body and the side effect (row written, event published) are not asserted",
      "before_example": "assert resp.status_code == 200",
      "after_example": "assert resp.status_code == 200\nassert resp.json()[\"invoice_id\"] == invoice.id\nassert Invoice.objects.filter(id=invoice.id, status=\"sent\").exists()",
      "distinct_prs": 7,
      "distinct_reviewers": 3,
      "comment_urls": [
        "https://github.com/acme/billing-api/pull/399#discussion_r1889120",
        "https://github.com/acme/billing-api/pull/408#discussion_r1890340",
        "https://github.com/acme/billing-api/pull/421#discussion_r1891560"
      ],
      "count": 9,
      "cost": 1.8,
      "score": 16.2,
      "baseline_count": 9,
      "remeasure_date": "2026-09-30",
      "formatter_coverable": false
    },
    {
      "id": "p3",
      "behaviour": "N+1 query in list endpoints: related rows loaded per item inside the serializer loop",
      "before_example": "for inv in Invoice.objects.all(): inv.customer.name",
      "after_example": "for inv in Invoice.objects.select_related(\"customer\"): inv.customer.name",
      "distinct_prs": 5,
      "distinct_reviewers": 2,
      "comment_urls": [
        "https://github.com/acme/billing-api/pull/404#discussion_r1890205",
        "https://github.com/acme/billing-api/pull/411#discussion_r1890733",
        "https://github.com/acme/billing-api/pull/425#discussion_r1891902"
      ],
      "count": 6,
      "cost": 2.5,
      "score": 15.0,
      "baseline_count": 6,
      "remeasure_date": "2026-09-30",
      "formatter_coverable": false
    }
  ],
  "appendix_patterns": [],
  "single_occurrence": [
    {
      "behaviour": "Retry loop without jitter on the payment-provider client",
      "comment_urls": [
        "https://github.com/acme/billing-worker/pull/91#discussion_r1891330"
      ]
    }
  ],
  "automation_gap": {
    "comments_excluded": 38,
    "tool": "ruff",
    "config_change": "enable I001 (isort) and Q000 (quotes) in pyproject.toml [tool.ruff.lint] select; run ruff format in pre-commit"
  },
  "suggested_rules": [
    {
      "pattern_id": "p1",
      "rule": "Every requests call passes an explicit timeout",
      "channel": "linter_or_formatter_rule",
      "channel_id": "flake8-bandit S113 (request-without-timeout) via ruff S113",
      "status": "new",
      "cycles_without_drop": 0
    },
    {
      "pattern_id": "p2",
      "rule": "Endpoint tests assert body and side effect, not only status",
      "channel": "pr_template_checkbox",
      "why_not_earlier_channels": "No linter can judge assertion sufficiency; a CI check on assertion count would be gamed; the checkbox puts the question in front of the author at the moment it matters",
      "status": "new",
      "cycles_without_drop": 0
    },
    {
      "pattern_id": "p3",
      "rule": "List endpoints use select_related or prefetch_related for every relation the serializer touches",
      "channel": "ci_check_or_test",
      "channel_id": "django-test-plus assertNumQueries on every list endpoint test",
      "why_not_earlier_channels": "No static rule can see the serializer's relation access; a query-count assertion in CI catches the regression on the exact endpoint",
      "status": "new",
      "cycles_without_drop": 0
    }
  ],
  "notes": [
    {
      "observation": "Reviewers ask for ADR links on schema changes in 4 PRs; no channel yet, revisit when the ADR template lands",
      "pattern_id": "p4"
    }
  ],
  "review": {
    "status": "ready_for_owner_check",
    "owner": "eng-manager@acme.example",
    "shared_by_agent": false
  }
}
```
