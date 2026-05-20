---
slug: faion-cli-as-agent-skill
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "678b6d1139e5dbcf"
summary: Faion Cli As Agent Skill delivers a concrete, testable methodology that turns the recurring task of 'Methodology corpus integration: faion-into-our-agent (2 weeks)' into an auditable artefact, addressing the gap: Most relevant gap to faion's own GTM: a methodology showing geek-ti
tags: [ai, geek, method, methodology]
---
# Faion Cli As Agent Skill

## Summary

**One-sentence:** Faion Cli As Agent Skill delivers a concrete, testable methodology that turns the recurring task of 'Methodology corpus integration: faion-into-our-agent (2 weeks)' into an auditable artefact, addressing the gap: Most relevant gap to faion's own GTM: a methodology showing geek-tier devs how to wire `faion search` + `faion get-content` into their own agent as a reasoning tool. Today the integration is implicit in CLI docs only.

**One-paragraph:** Most relevant gap to faion's own GTM: a methodology showing geek-tier devs how to wire `faion search` + `faion get-content` into their own agent as a reasoning tool. Today the integration is implicit in CLI docs only. Faion Cli As Agent Skill closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Methodology corpus integration: faion-into-our-agent (2 weeks)' (p7-llm-agent-developer, geek tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Methodology corpus integration: faion-into-our-agent (2 weeks)' (role: p7-llm-agent-developer) is in your current workload at least once per cycle.
- You have authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the artefact — human reviewer OR downstream agent.
- An auditable source-of-truth is available for the inputs the methodology needs.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems / dashboards / docs that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `geek/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `faion_cli_as_agent_skill_template_fill` | haiku | Template fill, no judgment |
| `faion_cli_as_agent_skill_evidence_check` | sonnet | Bounded comparison + judgment |
| `faion_cli_as_agent_skill_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `geek/ai/` (see neighbouring methodologies)
- triggering activity: `p7-llm-agent-developer/Methodology corpus integration: faion-into-our-agent (2 weeks)`
- external: industry references cited inline in `content/01-core-rules.xml`
