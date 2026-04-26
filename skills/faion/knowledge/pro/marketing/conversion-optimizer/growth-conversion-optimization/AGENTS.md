# Conversion Rate Optimization (CRO)

## Summary

A research-driven cycle for systematically improving conversion rates across web funnels: measure where users drop off, research why, form testable hypotheses, run A/B tests to statistical significance (95%+, 100+ conversions/variant, 2+ weeks), implement winners, and document learnings in a reusable library. A 1% → 2% lift doubles effective marketing spend.

## Why

Traffic without conversion is wasted acquisition budget. CRO applies scientific method to UX decisions: hypothesis + controlled test + significance gate + learning library. Without the gate, early-stop false positives corrupt the program. Without the library, the same mistakes repeat. The PIE framework (Potential × Importance × Ease) ensures effort goes to high-traffic, high-impact pages first.

## When To Use

- Established traffic (≥5k unique visitors/page/month) with under-converting funnels.
- Starting or running a structured A/B testing program.
- Redesigning forms, pricing pages, checkout, or onboarding where research-driven hypotheses outperform opinion.
- Quarterly CRO program reviews: wins, losses, learnings, next-cycle backlog.
- Multi-page funnel diagnosis using heatmaps + session recordings + exit surveys together.

## When NOT To Use

- Low-traffic pages (under ~5k uniques/month) — statistical significance is unreachable; use qualitative research instead.
- Pre-PMF startups — optimizing the wrong funnel; nail message-market fit first.
- Stable, mature funnels with sub-1% lift potential — resources better spent on acquisition or new product.
- Major redesigns — run user research and prototype testing, not A/B tests.
- Compliance-heavy flows (KYC, medical) where CRO levers conflict with required disclosures.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | CRO cycle: Analyze → Research → Hypothesize → Test → Learn; funnel metrics benchmarks; PIE prioritization; A/B test requirements. |
| `content/02-examples.xml` | Worked examples: signup form 45% lift, pricing page FAQ +15%, mobile redesign +20%. Antipatterns: early stops, single-test fundamentalism, heatmap-only research. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cro-audit.md` | CRO audit template: funnel analysis table, research findings, PIE backlog, recommended tests. |
| `templates/ab-test-brief.md` | A/B test brief: hypothesis, variants, metrics, sample size, implementation checklist. |
| `templates/sample-size.py` | Binary metric sample-size calculator: two-sided, 95% confidence, 80% power. |
