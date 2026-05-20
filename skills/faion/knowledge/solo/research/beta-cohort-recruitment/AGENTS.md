---
slug: beta-cohort-recruitment
tier: solo
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "4f5cdbd9d0e4dcd1"
summary: Recruits a private-beta or design-partner cohort with NDA, expectations contract, feedback cadence, and exit ramp — distinct from open user-interview recruiting.
tags: [private-beta, design-partner, recruitment, nda, gtm]
---
# Private-Beta / Design-Partner Cohort Recruitment

## Summary

**One-sentence:** Sources, screens, and signs up a small invited cohort (typically 5-15) for a private beta or paid design partnership, with the contracts, cadence, and exit criteria written before the first invite goes out.

**One-paragraph:** Open user-interview recruiting (`user-interviews`) talks to anyone willing to share 30 minutes — useful for exploration. A private beta is different: a small set of named accounts who commit to multi-week usage, share confidential feedback, accept NDA terms, and in exchange get unusually deep access and influence on the roadmap. The cost of recruiting them wrong is high: a bad cohort either drowns the founder in feature requests they cannot serve, or churns silently leaving no signal. This methodology pins five things — ICP-first sourcing, a screener that filters for fit and time, an NDA + expectations one-pager, a defined feedback cadence, and an explicit graduation/exit ramp. Output: a signed cohort with a tracked engagement log.

## Applies If (ALL must hold)

- Product is past prototype but pre-GA — there is real software to use, not just mockups.
- Founder needs depth feedback (workflow integration, retention signal) not breadth feedback.
- Target ICP is reachable in some channel (network, niche community, outbound, list).
- Founder has at least 4 hours/week to dedicate to cohort touchpoints.

## Skip If (ANY kills it)

- Product is still mockup-only — run `user-interviews` instead.
- Founder cannot personally support each beta (>= 30 partners) — switch to public/open beta playbook.
- No ICP defined yet — back up to `niche-evaluation` first.
- Sales cycle is &lt; 30 days from now — paid pilots beat beta cohorts when revenue is the goal.

## Prerequisites

- A written ICP statement (1-2 sentences, named segment with sizing signal).
- A landing-page or one-pager describing the beta proposition.
- A working onboarding path (signup, first-value-step) — beta partners do not debug your auth flow for free.
- Legal: a one-page mutual NDA template ready (see templates/).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/user-interviews` | Cadence touchpoints reuse interview-craft basics. |
| `solo/research/researcher/jobs-to-be-done` | Optional: pair JTBD with beta feedback for switching evidence. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: ICP-first, screener filter, signed expectations, cadence, exit ramp | ~900 |
| `content/02-output-contract.xml` | essential | Cohort log shape; required signed docs; engagement KPI thresholds | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: friend-of-founder cohort, NDA-as-contract-only, etc. | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `screener-question-draft` | haiku | Template fill from ICP + capacity |
| `candidate-fit-score` | sonnet | Apply screener rubric to a candidate's responses |
| `engagement-trend-summary` | opus | Synthesis across multiple touchpoints to detect retention vs decay |

## Templates

| File | Purpose |
|------|---------|
| `templates/beta-screener.md` | 8 screener questions with scoring rubric |
| `templates/expectations-one-pager.md` | What the partner gets, what the founder gets, NDA terms, exit conditions |
| `templates/cohort-log.csv` | Per-partner row: name, signup, last touchpoint, engagement score, status |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/cohort-health.py` | Compute weekly engagement metrics from cohort-log.csv | Weekly |

## Related

- parent skill: `solo/research/researcher/`
- peer methodology: `user-interviews`, `problem-validation`, `pricing-research`
- external: [First Round Review on design partners](https://review.firstround.com/) · [Y Combinator on early customers](https://www.ycombinator.com/library)
