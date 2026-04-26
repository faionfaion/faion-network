# Competitive Intelligence (Market-Researcher Lens)

## Summary

Competitive intelligence at the market-researcher level produces three deliverables the general CI loop does not cover: win/loss analysis (coding closed-deal records into structured loss reasons), pricing intelligence (triangulating list price against realized ACV from G2 disclosures and Vendr/Tropic benchmarks), and market-positioning signals (clustering competitor hero copy and buyer language by job-to-be-done). The core rule: every loss-reason row requires at least one verbatim buyer-side quote with speaker attribution — rep notes alone never justify a loss code.

## Why

Win/loss self-report bias causes sales reps to over-attribute losses to "price" when buyers actually leave for product fit, integration risk, or relationship gaps. Posted list price diverges from realized close price by 15-35% in B2B SaaS. Positioning language extracted from exec decks reflects aspiration, not buyer perception. Systematic triangulation across win/loss records, pricing page snapshots, and review-site text produces CI that drives decisions instead of confirming existing beliefs.

## When To Use

- Deal review backlog has more than 20 closed-lost/closed-won opportunities in 60 days with unstructured CRM notes
- Pricing committee meets quarterly and needs a defensible benchmark per segment
- Inbound positioning brief is stalling because category language is contested
- Repositioning, rebrand, or new-segment launch where messaging needs evidence from buyer language
- Pre-Series-B/C: investors ask for a defensible win-rate trend with reasons-coded loss data

## When NOT To Use

- Fewer than 10 closed deals per quarter — sample too small; use customer interviews instead
- Self-serve / PLG product with no sales conversations — switch to churn analytics and cancel-survey
- Pricing locked by multi-year MSAs for the next 12 months — pricing intel has no decision to inform
- Single-product, single-segment startup — positioning emerges from PMF interviews
- Where buyer interviews are blocked by NDA — synthesize from public review sites, do not fabricate

## Content

| File | What's inside |
|------|---------------|
| `content/01-win-loss-analysis.xml` | Win/loss coding rules, loss-reason taxonomy, buyer-interview requirements, and confidence scoring |
| `content/02-pricing-intelligence.xml` | Pricing triangulation (list vs. realized vs. buyer-disclosed), packaging diffs, AB-test detection rules |
| `content/03-positioning-signals.xml` | Positioning extraction from hero copy, review headlines, and analyst mentions; JTBD clustering approach |
| `content/04-antipatterns.xml` | AI-agent gotchas: hallucinated reasons, currency ambiguity, hidden-tier collapse, reason-taxonomy drift |

## Templates

| File | Purpose |
|------|---------|
| `templates/wl-join.py` | Python script joining win/loss, pricing, and positioning event streams into a dated competitive-analysis.md |
