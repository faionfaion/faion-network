---
slug: indirect-prompt-injection-defense
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "73960df637e179b5"
summary: "Indirect Prompt Injection Defense — testable methodology for LLM-agent design, evals, safety, cost. faion has `cheap-guardrail-tripwire` + `refusal-field-strict-schema` (output side). Missing: input-side IPI defense — trust-boundary model across tools, span-tainting, sandboxed reasoning over untrusted content, exfil canaries. The single most-asked-about a..."
tags: [ai, geek, methodology]
---
# Indirect Prompt Injection Defense

## Summary

**One-sentence:** Indirect Prompt Injection Defense — testable methodology for LLM-agent design, evals, safety, cost. faion has `cheap-guardrail-tripwire` + `refusal-field-strict-schema` (output side). Missing: input-side IPI defense — trust-boundary model across tools, span-tainting, sandboxed reasoning over untrusted content, exfil canaries. The single most-asked-about a...

**One-paragraph:** Indirect Prompt Injection Defense closes a known gap in ai practice: faion has `cheap-guardrail-tripwire` + `refusal-field-strict-schema` (output side). Missing: input-side IPI defense — trust-boundary model across tools, span-tainting, sandboxed reasoning over untrusted content, exfil canaries. The single most-asked-about agent-security topic in 2026 and faion has no canonical methodology. The methodology is anchored to the recurring activity 'Harden an agent against prompt injection and jailbreak across tool boundaries (role: p7-llm-agent-developer)' and produces an auditable artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Harden an agent against prompt injection and jailbreak across tool boundaries (role: p7-llm-agent-developer)' shows up in the user's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — the artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems, dashboards, or transcripts that feed the methodology's inputs.
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
| `content/01-core-rules.xml` | essential | 3-5 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 4-8 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `indirect_prompt_injection_defense_template_fill` | haiku | Template fill, no judgement |
| `indirect_prompt_injection_defense_evidence_check` | sonnet | Bounded comparison + judgement |
| `indirect_prompt_injection_defense_synthesis` | opus | Cross-input synthesis + final write-up |

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
- triggering activity: `Harden an agent against prompt injection and jailbreak across tool boundaries (role: p7-llm-agent-developer)`
- external: industry references cited inline in `content/01-core-rules.xml`
