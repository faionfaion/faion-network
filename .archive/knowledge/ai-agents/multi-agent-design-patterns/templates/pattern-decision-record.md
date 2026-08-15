<!--
purpose: ADR-style decision record skeleton for selecting one of the 8 canonical multi-agent patterns.
consumes: task statement, alternatives discussion, latency/cost/audit constraints.
produces: PatternDecisionRecord (PDR) validated by scripts/validate-multi-agent-design-patterns.py.
depends-on: content/06-decision-tree.xml; content/01-core-rules.xml.
token-budget-impact: ~500 tokens to author; near-zero at runtime (design artefact).
-->

# PDR-NNN: <pattern> for <task>

- **Status:** proposed | accepted | superseded
- **Date:** YYYY-MM-DD
- **Authors:** <names>

## Task

<one paragraph stating the multi-agent task and acceptance criteria>

## Decision

**Pattern:** `<one of: sequential | parallel_fanout | hierarchical | generator_critic | loop | human_in_loop | router | blackboard>`

**Downstream impl methodology:** `geek/ai/ai-agents/<slug>`

## Rationale

<>=32 chars; reference the dominant trade-off axis (latency / cost / audit / parallelism)>

## Alternatives considered

| Pattern | Why rejected |
|---|---|
| `<name>` | <>=16 chars> |
| `<name>` | <>=16 chars> |

## Trade-offs

| Axis | Impact |
|---|---|
| Latency | <e.g. "+50% vs sequential due to extra critic round"> |
| Cost | <e.g. "+30% — critic uses opus"> |
| Audit | <e.g. "Best — every claim has generator + critic trail"> |
| Parallelism | <e.g. "None — pattern is inherently sequential loop"> |

## HITL gates

- <action name> — <approval requirement>

<!-- if pattern == blackboard, add: -->
## Concurrency plan

<single-writer queue | CRDT | DB transactions; describe the locking model>

<!-- if pattern == router, add: -->
## Classifier accuracy

<reported test-set accuracy ≥ 0.85; describe held-out evaluation>
