---
slug: inc-runbook-as-markdown-tagged-steps
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Runbooks stored as markdown with tagged steps (`[read]`, `[write]`, `[approval-required]`, `[verify]`) the agent can parse and execute; humans + agents read the same file.
content_id: "cff78cb2d52f8f01"
complexity: medium
produces: playbook-step
est_tokens: 4200
tags: [runbook, incident, markdown, ai-agents, sdlc-ai]
---
# Runbook as Markdown with Tagged Steps

## Summary

**One-sentence:** Runbooks stored as markdown with tagged steps (`[read]`, `[write]`, `[approval-required]`, `[verify]`) the agent can parse and execute; humans + agents read the same file.

**One-paragraph:** Runbooks live in two parallel worlds — markdown humans skim and YAML/JSON the agent runs. Drift between them is the leading cause of 3am surprises. This methodology unifies both: runbooks are markdown files with machine-parsable step tags (`[read]`, `[write]`, `[approval-required]`, `[verify]`) the agent reads and executes step-by-step, while the same file remains human-skimmable. Output is the runbook markdown plus a JSON parsed-step list per execution.

**Ефективно для:**

- Team operates production systems with runbooks consulted at 3am.
- AI agents participate in incident response and need machine-parseable structure.
- Existing runbooks are markdown but drift from execution reality.

## Applies If (ALL must hold)

- Team operates production systems with runbooks consulted at 3am.
- AI agents participate in incident response and need machine-parseable structure.
- Existing runbooks are markdown but drift from execution reality.

## Skip If (ANY kills it)

- Team has no runbooks (install the basics first).
- Runbooks already use a fully machine-driven tool (Rundeck / Stackstorm) — different methodology applies.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Runbook markdown directory | md | Repo at `docs/runbooks/` |
| Step tag spec | md | Repo at `docs/runbooks/TAG-SPEC.md` |
| Approval token verifier | config | From `gov-approval-token-signed-jwt` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-inc-runbook-as-markdown-tagged-steps` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/runbook-template.md` | Runbook markdown skeleton with tagged steps |
| `templates/parser.py` | Reference runbook parser |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-inc-runbook-as-markdown-tagged-steps.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
