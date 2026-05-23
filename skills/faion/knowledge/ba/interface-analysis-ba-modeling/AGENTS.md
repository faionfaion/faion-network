# Interface Analysis

## Summary

**One-sentence:** Inventory + contract analysis of every connection point (API, file, message bus, UI, hardware) with named owner, data shape, SLA, and error contract per interface.

**One-paragraph:** Pre-integration discovery: enumerate every interface between solution and external surface (system-to-system, system-to-user, system-to-hardware), classify by protocol, attach OpenAPI / AsyncAPI / file-schema contracts, declare SLA + error semantics, name owner per interface, and link to test fixtures. Output is a `spec` artefact developers consume to build integration code that does not break on edge cases.

**Ефективно для:**

- Integration spec coли solution touches ≥2 external systems.
- Pre-OpenAPI doc — surface every endpoint + payload + error code.
- Compliance review (ENISA, ISO 27001) requiring documented interface map.
- Migration / replatform — diff current vs target interface inventory.

## Applies If (ALL must hold)

- Solution communicates with ≥1 external system, user surface, file format, or hardware.
- Contract drift between teams already caused at least one production incident.
- SLA + error semantics need formal capture before development.
- Each interface has an owner reachable for validation.

## Skip If (ANY kills it)

- Self-contained CLI / batch script with no external surface.
- Trivial CRUD service with one well-known REST consumer.
- Interface already documented in current, accurate OpenAPI/AsyncAPI artefact — extend it.
- Spike / prototype where interface is intentionally throwaway.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Architecture map | C4 / diagram-as-code | architect |
| Sample payloads | JSON / XML / CSV | integration team |
| SLA targets | Markdown / SLO doc | SRE / ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[data-analysis]] | Sibling — defines data entities that flow across interfaces |
| [[business-process-analysis]] | Upstream — process map identifies where interfaces hand off |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: every interface typed + contract-bound, named owner, SLA + error codes, versioned, test-fixture linked | 950 |
| `content/02-output-contract.xml` | essential | JSON Schema + examples | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: untyped payload, anonymous owner, missing error contract, no version | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 750 |
| `content/05-examples.xml` | essential | Worked example: payment-webhook interface end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing on contract completeness + owner | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `enumerate_interfaces` | sonnet | Pattern-match candidates from architecture map. |
| `contract_extraction` | haiku | Mechanical pull of payload shapes from sample data. |
| `sla_negotiation` | opus | Cross-team SLA reasoning + error-budget tradeoffs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interface-spec.md` | Markdown skeleton (per interface: protocol, payload, errors, SLA, owner) |
| `templates/_smoke-test.json` | Minimum viable interface-inventory fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-interface-analysis.py` | Validate inventory JSON against output-contract | Pre-commit; before handoff to integration team |

## Related

- [[data-analysis]]
- [[business-process-analysis]]
- [[acceptance-criteria]]
- [[bpmn-via-ai-then-human-review]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on contract completeness + named owner per interface to the rule firing.
