---
slug: buyer-interview-script-for-freelancers
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "b58036e004175ed5"
summary: Mom-Test-style buyer interview script tuned for freelancers selling a service offer — hiring triggers, budget authority, vendor preference, switching pain.
tags: [freelancer, buyer-interview, mom-test, service-offer, p3-freelancer]
---
# Buyer Interview Script for Freelancers

## Summary

**One-sentence:** A buyer-side interview script for freelancers selling a service (not a product), focused on hiring triggers, budget authority, and vendor preference — gathering evidence before pitching a new offer or pivoting niche.

**One-paragraph:** Rob Fitzpatrick's Mom Test gives the universal interview floor: ask about past behavior, not future intent. For freelancers building a service offer (P3 archetype), that floor is necessary but not sufficient — they also need buyer-specific questions: what triggered the last hire, who controls the budget, what the buyer wishes a vendor had asked, and what would make them switch from their current provider. This methodology pins the 12 questions every freelance buyer interview must cover, the disqualifiers that end the interview early (saving time on bad-fit leads), and the synthesis pattern that turns 5+ interviews into a positioning shift or an offer adjustment. Output: a buyer-evidence pack signed off by the freelancer, used as input to a service rewrite or pivot decision.

## Applies If (ALL must hold)

- Freelancer is building or pivoting a productized service offer (not a one-off custom job).
- Target buyer is reachable (LinkedIn, past clients, communities) — 5+ candidates available.
- The freelancer is the one running the interviews (not a researcher proxy).
- Decision at end: keep the offer, refine it, or pivot — not "interview for the sake of insight."

## Skip If (ANY kills it)

- Selling a digital product (SaaS, info-product) — use `jobs-to-be-done` or `pricing-research` instead.
- Already validated with paying clients at the target price for 6+ months — talking to buyers is now business development, not research.
- Freelancer wants to interview "the market" — there is no market, only buyers. Define them first.
- &lt; 5 candidates reachable — interview output will be anecdote.

## Prerequisites

- A written one-line ICP describing the buyer (role, company size, situation).
- A current service one-pager or proposal — the artifact under test.
- A note-taking template (a Google Doc per interview is fine).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/researcher/user-interviews` | Interview-craft (recording consent, follow-up prompts, silence management) assumed. |
| `pro/research/researcher/problem-validation` | Buyer interviews feed problem-validation evidence; pair if running both. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: past-behavior bias, budget authority, switching pain, vendor wishlist, disqualifiers | ~900 |
| `content/02-output-contract.xml` | essential | Evidence pack shape, quote-citation requirement, decision matrix | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes including hypothetical-question drift, friend-as-buyer trap | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `interview-summary-from-notes` | sonnet | Bounded judgment, per-transcript extraction |
| `evidence-pack-synthesis` | opus | Cross-interview pattern recognition |
| `disqualifier-flagging` | haiku | Mechanical rule application |

## Templates

| File | Purpose |
|------|---------|
| `templates/buyer-interview-script.md` | The 12 questions with probes and disqualifiers |
| `templates/evidence-pack.md` | Per-interview block + synthesis section |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/quote-coverage-check.py` | Verifies that every claim in evidence-pack has &gt;= 2 verbatim citations | Pre-decision review |

## Related

- parent skill: `pro/research/researcher/`
- peer methodology: `user-interviews`, `problem-validation`, `pricing-research`
- external: [The Mom Test by Rob Fitzpatrick](https://www.momtestbook.com/) · [Building a StoryBrand (Donald Miller) for offer language](https://buildingastorybrand.com/)
