<!-- purpose: Markdown skeleton with both options + trade-offs. | consumes: see content/02-output-contract.xml inputs | produces: artefact conforming to content/02-output-contract.xml (choreography-vs-orchestration-decision) | depends-on: content/01-core-rules.xml | token-budget-impact: small (template is loaded only when an artefact is being authored) -->
# Choreography vs Orchestration — <workflow>

**Owner:** <@handle>
**Pattern:** <choreography | orchestration>

## Workflow

<step list with compensations>

## Trade-offs

| Axis | Choreography | Orchestration |
|------|--------------|----------------|
| Operational ownership | Distributed across emitters | Centralized on coordinator |
| Debug story | Trace across N topics | Single coordinator log |
| Coupling | Loose (events) | Tight (coordinator knows steps) |
| Latency overhead | Lower | One extra hop per step |

## Decision

<decision sentence + rationale citing inputs>
