<!-- purpose: reviewer's rejection checklist for AI-generated ES PRs -->
<!-- consumes: PR diff + stage outputs -->
<!-- produces: ACCEPT/REJECT verdict per rule -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~150 tokens when loaded as reference -->

# Review checklist

| Rule | Verify |
|------|--------|
| past-tense-event-names | Every event class name is a past-tense business fact, not Update/Set/Change. |
| apply-only-mutation | Command method bodies do NOT assign to `self.*` state fields. Mutation lives in `_apply_*`. |
| expected-version-enforced | Every `repo.save(...)` call passes `expected_version`. Tests cover the concurrency-conflict path. |
| no-invented-apis | All event-store/library calls resolve at import time. CI build is green. |
| projection-no-side-effects | Every projection handler body is pure UPSERT/INSERT/DELETE. No HTTP / queue / mail / log-action. |

Format the review JSON as:
```json
{"accepted": false, "rejected_rule_ids": ["apply-only-mutation"], "notes": ["Order.place() sets self.status directly at line 42"]}
```
