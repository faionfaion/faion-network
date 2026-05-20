---
slug: jobs-to-be-done
tier: solo
group: research
domain: researcher
version: 1.0.0
status: stable
last_reviewed: 2026-05-17
maintainers: [faion-net]
summary: Framework that maps customer progress by interviewing recent switchers and tagging Push/Pull/Habit/Fear forces.
content_id: "8ec6f0d653b43606"
tags: [research, jobs-to-be-done, jtbd, customer-progress, switching-behavior]
---

# Jobs To Be Done (improved form)

## Summary

**One-sentence:** Framework that maps customer progress by interviewing recent switchers and tagging Push/Pull/Habit/Fear forces.

**One-paragraph:** Defines what progress customers are trying to make so products target stable motivations, not shifting feature requests. Mechanism: interview switchers within 60-90 days, tag each statement Push/Pull/Habit/Fear, synthesize 1-3 candidate "When... I want... So I can..." statements backed by ≥3 verbatim quotes each, and always capture functional + emotional + social dimensions. Primary output: validated job statement(s) with competitive set.

## Applies If (ALL must hold)

- task_type ∈ {pre-build_validation, feature_reframing, switcher_diagnosis}
- target_audience_defined == true
- ≥5 recent switchers (60-90 days) reachable for interviews
- product is NOT pure impulse-purchase B2C

## Skip If (ANY kills it)

- product already validated AND task is optimization — use A/B testing instead
- B2C impulse (snacks, fashion) — job is "feel good now," JTBD over-engineers
- pure API/infra tooling — persona/feature thinking is faster
- < 5 recent switchers reachable — JTBD without switching data is hypothesis-spinning

## Prerequisites

- target audience defined precisely (e.g., "solo founders, post-launch, <$10k MRR")
- recruitment channel ready (User Interviews, Respondent, warm intros)
- interview transcripts will be stored in a folder consumable by the force-tagger

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/user-interviews` | This methodology consumes interview transcripts; does not teach interviewing technique |
| `solo/research/researcher/problem-validation` | Pairs with JTBD for evidence weight when used together |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: job-vs-solution, three dimensions, 4 forces, switcher recency, ≥5-interview minimum | ~900 |
| `content/02-output-contract.xml` | essential | Job-statement schema, evidence requirements, forbidden patterns | ~600 |
| `content/03-failure-modes.xml` | essential | 8 LLM-specific failure modes with detector + repair | ~1100 |
| `content/04-switcher-interview-method.xml` | advanced | 5-stage timeline (First Thought → Consumption), questions per stage | ~800 |
| `content/05-job-map-8-stages.xml` | advanced | Apply only if job has ≥3 distinct steps; pain mapping per stage | ~700 |
| `content/06-cross-cultural-framing.xml` | edge | When emotional/social dimensions diverge from Christensen examples | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `screener_outreach_draft` | haiku | Template fill with audience parameters, low cost |
| `forces_tagging_per_transcript` | sonnet | Per-statement judgment; bounded; high volume |
| `job_statement_synthesis` | opus | Cross-transcript synthesis; needs deep coherence |
| `job_map_expansion` (optional) | sonnet | Mechanical expansion of statement into 8 stages |

## Templates

| File | Purpose |
|------|---------|
| `templates/job-statement.json` | JSON schema for validated job statement output |
| `templates/jtbd-interview-guide.md` | Interview guide with timeline questions |
| `templates/job-map.md` | 8-stage map skeleton (Define → Locate → Prepare → Confirm → Execute → Monitor → Modify → Conclude) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/force-aggregator.py` | Reads tagged transcripts, returns Push/Pull/Habit/Fear severity table | After all transcripts tagged, before synthesis |
| `scripts/validate-job-statement.py` | Validates output vs output-contract schema | After synthesis, before main agent accepts |

## Related

- parent skill: `solo/research/researcher/`
- peer methodologies: `problem-validation`, `pricing-research`, `value-proposition-design`
- external: [HBR JTBD](https://hbr.org/2016/09/know-your-customers-jobs-to-be-done) · [jtbd.info](https://jtbd.info/) · [Strategyn](https://strategyn.com/jobs-to-be-done/)
