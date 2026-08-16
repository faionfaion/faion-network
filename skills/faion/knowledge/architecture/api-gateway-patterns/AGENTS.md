# API Gateway Patterns & Technology Selection

## Summary

**One-sentence:** Selects the gateway pattern (edge / BFF / per-service / no gateway) and the product (Kong / Traefik / Envoy / APIGW / Apollo Router) based on workload, team, and platform constraints.

**One-paragraph:** Defines the gateway architecture as a single entry point for client requests, owning routing, cross-cutting concerns (auth, rate limiting, observability), and protocol translation. The output is a documented selection: pattern + product + rationale + ADR record, blocking the common failure of accidentally building two gateway layers — and, once the selection is made, the operational settings that make it correct: stateless gateway, per-consumer rate limiting, X-Request-ID propagation, a descending timeout cascade, per-upstream circuit breakers and declarative config-as-code.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'API gateway selection' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- You operate ≥3 backend services exposed to a client (web, mobile, partner).
- You need at least one cross-cutting concern (auth, rate limiting, observability) consolidated.
- You have a platform team or one engineer who can own gateway operations.

## Skip If (ANY kills it)

- Single-service monolith with one client — direct routing is simpler.
- Two services with no cross-cutting concerns — a load balancer with TLS is enough.
- Strict service-mesh-only org policy — gateway concerns live in the mesh, not a separate hop.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service inventory | list of services + protocols | service catalog |
| Client matrix | table of (client, services-used) | PM/architect |
| Operational budget | headcount + dollars | engagement charter |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | The selection lands as an ADR. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 selection rules (r1-r5) + 8 operational rules (r6-r13) + skip fallback | ~2200 |
| `content/02-output-contract.xml` | essential | JSON Schema for the selection record incl. the optional `gateway_config` block | ~1300 |
| `content/03-failure-modes.xml` | essential | 9 antipatterns with symptom + root-cause + fix | ~1400 |
| `content/04-procedure.xml` | medium | 9 steps: audit clients → pick pattern → score → ADR → CI gate → configure → wire concerns → smoke tests → deploy | ~1300 |
| `content/05-examples.xml` | medium | Worked ADR (Kong + BFF) plus Kong / nginx / BFF / `gateway_config` configuration examples | ~1400 |
| `content/06-decision-tree.xml` | essential | Applicability tree + operational review tree routing each signal to a rule id | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-gateway-products` | sonnet | Per-criterion scoring across candidate products. |
| `draft-selection-adr` | sonnet | Template-driven ADR composition. |
| `audit-existing-gateways` | opus | Cross-system inventory and overlap detection. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gateway-selection-adr.md.j2` | ADR template: pattern + product + rationale + alternatives. |
| `templates/gateway-selection-adr.md` | ADR template: pattern + product + rationale + alternatives. Generated from `templates/gateway-selection-adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/gateway-config.json` | `gateway_config` skeleton — operational half of the artefact (r6-r13). |
| `templates/kong-route.yml` | Kong declarative route, deck-sync compatible, consumer-scoped rate limit. |
| `templates/nginx-gateway.conf` | nginx gateway config keyed on consumer identity, not source IP. |
| `templates/bff-aggregator.py` | BFF fan-out with per-service timeouts and partial degradation. |
| `templates/prompt-gateway-route.txt` | Prompt for adding a route without smuggling business logic into a plugin. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-gateway-patterns.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[api-gateway-security]]
- [[api-gateway-observability]]
- [[api-gateway-resilience]]
- [[api-gateway-graphql]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
