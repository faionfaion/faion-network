# Prompt Engineering — Security and Injection Defense

## Summary

**One-sentence:** Hardens prompts against prompt-injection, jailbreaks, data exfiltration, and instruction-hierarchy bypass via structured input separation, output filters, and red-team tests.

**One-paragraph:** Hardens prompts against prompt-injection, jailbreaks, data exfiltration, and instruction-hierarchy bypass via structured input separation, output filters, and red-team tests. The methodology assumes the inputs in Prerequisites and produces a `spec` artefact validated by `scripts/validate-prompt-engineering-security.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** ML and security engineers shipping LLM features that ingest untrusted user or tool-result content.

## Applies If (ALL must hold)

- Any LLM system that processes user-supplied text (chatbots, document processors, agents).
- Systems where model outputs could trigger real-world actions (email sending, API calls, code execution).
- Applications handling sensitive data (PII, credentials, financial data).
- Multi-agent systems where one agent's output becomes another agent's prompt.
- Agentic pipelines that read untrusted external content (web pages, uploaded files).

## Skip If (ANY kills it)

- Internal tooling with no user-supplied text — security overhead is not justified.
- Closed test environments with controlled inputs only.
- Replacing proper authentication and authorization — prompt hardening is defense-in-depth, not a substitute for access control.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[prompt-engineering-production]]` | Adjacent context the agent normally already has when this methodology fires. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules with rationale and source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples for the output artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix. | ~800 |
| `content/04-procedure.xml` | medium | Five-step procedure with decision-gates. | ~700 |
| `content/05-examples.xml` | medium | One end-to-end worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether the methodology applies, ending in rule refs. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-requirements` | sonnet | Structured interview-style extraction. |
| `synthesize-spec` | opus | Cross-section trade-off synthesis. |
| `lint-output` | haiku | Schema validation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/spec.md.tmpl` | Markdown spec skeleton with the required sections + placeholders. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-engineering-security.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[prompt-engineering-production]]
- [[guardrails-concepts]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `prompt-engineering-security` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
