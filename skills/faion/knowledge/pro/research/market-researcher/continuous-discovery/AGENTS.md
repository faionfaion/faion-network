# Continuous Discovery

## Summary

Continuous discovery is the practice of running weekly market-scanning and competitor-monitoring loops instead of one-shot research sprints. Rather than treating market intelligence as a project-start deliverable, it maintains a living picture of competitors, pricing, new entrants, and category signals on a daily/weekly/bi-weekly cadence using cheap models for data collection and Opus only for synthesis.

## Why

Markets in fast-moving categories (AI tooling, dev tools, PLG SaaS) shift faster than quarterly research cycles. Competitors ship weekly, pricing A/B-tests daily, and new entrants arrive via YC batches and ProductHunt. A rolling scan catches these moves before they show up in churn, while a severity rubric (0-5) filters cosmetic noise from genuine strategic events.

## When To Use

- Live category where competitors ship weekly and a 6-month-old market map is already wrong.
- Pricing-sensitive segments where competitor packaging changes erode conversion within days.
- GTM teams needing a weekly "what changed" digest without burning a senior analyst.
- Funded categories where new entrants (YC batches, ProductHunt launches) appear faster than a quarterly TAM refresh catches.
- Geo expansion plays where local competitors and regulatory shifts move the SOM monthly.
- Post-launch defense: detecting when a fast-follower clones your wedge before churn shows up.

## When NOT To Use

- Pre-PMF zero-to-one with no defined competitive set — run competitor-analysis once first.
- Slow-moving regulated categories (medtech, defense, classical banking) where half-life is years.
- Compliance-bound enterprise sales with 12-18 month cycles — quarterly snapshots beat noisy weekly diffs.
- Single-customer custom-software work — no "market" to scan.
- When the team will not act on signals — unread scans become a research graveyard that burns tokens.
- Crisis mode (active outage, churn cliff) — pause scan, focus on incident, resume after stabilization.

## Content

| File | What's inside |
|------|---------------|
| `content/01-cadence-and-workflow.xml` | Agent cadence table (daily/weekly/bi-weekly/monthly/quarterly), recommended subagents, model selection rationale |
| `content/02-rules-and-gotchas.xml` | Severity rubric (0-5), source-decay rules, anti-hallucination constraints, best practices |

## Templates

| File | Purpose |
|------|---------|
| `templates/competitor-registry.json` | Competitor registry schema with id, tier, changelog/pricing URLs, geos, review sources |
| `templates/changelog-watcher.py` | Claude Agent SDK watcher: fetch + diff + hash + append signals.jsonl |
| `templates/cron-schedule.txt` | Crontab entries for all cadence agents |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/validate-signal.sh` | Reject any signal row missing source_url + fetched_at + raw_hash triple |
