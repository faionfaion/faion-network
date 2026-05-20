---
slug: ai-feature-incident-runbook
tier: pro
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "d0923263ae73d34e"
summary: AI-specific incident runbook — hallucination spike, jailbreak in the wild, refusal-rate anomaly, output-quality regression — with classification → mitigation → root-cause → harden steps the on-call ML engineer follows from page to post-mortem.
tags: [llm-incident, ai-feature, on-call, ml-engineer, runbook, postmortem]
---
# AI-Feature Incident Runbook

## Summary

**One-sentence:** An AI-specific incident runbook covering hallucination spikes, jailbreak-in-the-wild, refusal-rate anomalies, and output-quality regressions — with classification → mitigation → root-cause → harden steps that the on-call ML engineer follows from page to post-mortem.

**One-paragraph:** Generic SRE runbooks (latency spikes, 5xx, queue depth) do not handle the failure surface of an LLM-backed feature: hallucination spike pushing wrong facts into production, a jailbreak observed in the wild that extracts the system prompt, a refusal-rate anomaly that breaks UX without breaking SLI, and quality regressions where the API is healthy but the outputs are worse after a model swap. This methodology defines the four AI-incident classes, the mitigation playbook for each (temperature pin, model rollback, prompt revert, refusal-class allowlist), the root-cause investigation tree (model version, prompt drift, retrieval drift, eval-set staleness, upstream provider change), and the harden steps that close the loop. Output: an incident-record artifact suitable for stakeholders and a postmortem draft that the team reviews.

## Applies If (ALL must hold)

- Service in production exposes an LLM call (Claude, OpenAI, Gemini, local) to end-users or downstream systems.
- An observability stack captures at minimum: per-request latency, cost, refusal flag, and a periodic quality signal (eval set or human review).
- An on-call rotation exists with paging configured against at least one AI-specific SLI (refusal rate, quality score, hallucination flag count).
- A post-mortem culture and template exist; pages are followed by written incident records.

## Skip If (ANY kills it)

- LLM feature is internal-only with no real user impact — incident response is informal.
- Feature is a one-off batch job, not a live service — page-to-postmortem flow does not apply.
- No quality signal in observability — generic SRE runbook still applies; this runbook needs quality data to be useful.
- LLM call is upstream of a deterministic re-check layer that already gates output — incident classes shift to classical SRE.

## Prerequisites

- Observability stack with the AI four pillars wired (see sibling methodology `ai-feature-observability-four-pillars`).
- Mitigation playbook artifacts checked in: model-rollback script, prompt-revert flag, temperature-pin config.
- A versioned `prompts/` folder and a versioned model+prompt registry.
- Incident severity matrix that includes AI-specific SEV1 / SEV2 / SEV3 thresholds.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ai/ml-engineer/ai-feature-observability-four-pillars` | Sibling — supplies the SLI signal the runbook reads. |
| `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps` | Runbook authoring convention; this runbook is one such file. |
| `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish` | Postmortem drafting convention; this runbook closes into it. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: classify before mitigate, mitigation reversible by default, eval-set freshness, prompt registry as ground truth, postmortem within 5 business days | ~1100 |
| `content/02-output-contract.xml` | essential | Incident-record schema, mitigation log, postmortem draft sections | ~800 |
| `content/03-failure-modes.xml` | essential | 6 LLM-specific incident failure modes with detector + mitigation + harden | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-incident-from-signals` | sonnet | Bounded judgment across the four SLIs |
| `mitigation-playbook-select` | haiku | Lookup from incident class to known-good mitigation |
| `root-cause-investigation-summary` | opus | Cross-signal synthesis across model, prompt, retrieval, eval, provider |
| `postmortem-draft` | opus | Long-form synthesis; required to be human-reviewed before publish |

## Templates

| File | Purpose |
|------|---------|
| `templates/incident-record.json` | Schema for the live incident record |
| `templates/mitigation-playbook.md` | Class → mitigation lookup table |
| `templates/postmortem.md` | Postmortem template with the four AI-specific sections |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/classify.py` | Read last 30 min of SLI signals; emit incident class | On page |
| `scripts/mitigate.sh` | Apply selected mitigation (model rollback, prompt revert, temperature pin) | After class confirmed by on-call |
| `scripts/harden-checklist.py` | Emit the four-step harden checklist tied to the incident class | After mitigation stable |

## Related

- parent skill: `pro/ai/ml-engineer/`
- peer methodologies: `ai-feature-observability-four-pillars`, `llm-observability`, `llm-observability-stack`
- external: [Anthropic Trust &amp; Safety responses](https://www.anthropic.com/) · [OpenAI Incident History](https://status.openai.com/) · [SRE Book chapter 14](https://sre.google/sre-book/managing-incidents/)
