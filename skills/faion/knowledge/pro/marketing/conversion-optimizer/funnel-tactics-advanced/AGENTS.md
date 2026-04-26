# Funnel Optimization Tactics — Advanced

## Summary

Industry-specific drop-off benchmarks, personalization by segment, exit-intent recovery, retargeting sequences, ICE-scored test prioritization, and analytics event tracking patterns. The rule: segment before personalizing — a single message to all users underperforms targeted messages by 15-40%.

## Why

Generic optimization misses high-value segments. A SaaS funnel and an e-commerce funnel have different critical drop points; a returning user and a first-time visitor need different messaging. Advanced tactics recover abandoning users and direct test effort to highest-ICE hypotheses first.

## When To Use

- Baseline funnel is instrumented and you have step-level conversion data
- You want to recover abandoning users via exit intent or retargeting
- You need to prioritize a backlog of A/B test hypotheses using ICE scoring
- You are optimizing for a specific industry (SaaS, e-commerce, mobile app)

## When NOT To Use

- No tracking in place — implement analytics events first
- Fewer than 1,000 monthly visitors — personalization overhead is not justified
- Still finding product-market fit — advanced tactics amplify a working funnel, not a broken one

## Content

| File | What's inside |
|------|---------------|
| `content/01-industry-tactics.xml` | Industry-specific biggest drops and top tactics for SaaS, e-commerce, mobile |
| `content/02-personalization.xml` | Segment types, expected lift ranges, exit-intent and retargeting patterns |
| `content/03-measurement.xml` | Key conversion metrics with benchmarks, ICE scoring rules, event tracking |

## Templates

| File | Purpose |
|------|---------|
| `templates/exit-intent-config.js` | Exit intent manager configuration with tracking hooks |
| `templates/retargeting-email-sequence.md` | 3-email retargeting sequence with timing, goals, and metric targets |
| `templates/ice-scoring-worksheet.md` | Hypothesis prioritization table with ICE scoring guide |
| `templates/analytics-events.js` | Funnel event tracking implementation for all 6 standard steps |
| `templates/ab-test-spec.md` | A/B test specification: hypothesis, control/variant, metrics, decision criteria |
