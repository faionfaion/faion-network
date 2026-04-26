# Quality Attribute Scenario

| Field | Value |
|-------|-------|
| **ID** | QA-XXX |
| **Quality Attribute** | <!-- Performance / Scalability / Availability / Security / Maintainability / Testability / Observability --> |
| **Priority** | <!-- High / Medium / Low --> |

## Scenario

| Element | Description |
|---------|-------------|
| **Source** | <!-- Who or what initiates: end user, external service, attacker, cron job, traffic spike --> |
| **Stimulus** | <!-- The event: HTTP request, component failure, traffic spike, security probe --> |
| **Environment** | <!-- System state: normal load / overloaded / degraded / maintenance window --> |
| **Artifact** | <!-- Affected part: entire system / API service / database / message broker --> |
| **Response** | <!-- What the system does: processes request, queues, degrades gracefully, rejects --> |
| **Response Measure** | <!-- Testable threshold: p99 < 300ms / availability > 99.9% / recovery < 15 min --> |

## Filled Example (Performance)

| Element | Description |
|---------|-------------|
| **Source** | End user |
| **Stimulus** | Submits a product search query |
| **Environment** | Normal operation, 500 concurrent users |
| **Artifact** | Product search API endpoint |
| **Response** | Returns ranked search results |
| **Response Measure** | p95 latency < 200ms; p99 < 500ms; 0% HTTP 5xx error rate |

## Architectural Tactics

List the tactics that satisfy this scenario:

- [ ] <!-- e.g. Add Redis cache in front of search service -->
- [ ] <!-- e.g. Add read replica for product database -->
- [ ] <!-- e.g. Set 500ms hard timeout on search API -->

## Validation Method

<!-- How this scenario will be validated: load test with k6, chaos experiment, security scan -->

## Trade-offs Accepted

<!-- What attributes are degraded to satisfy this one: security (no auth on search), consistency (stale cache) -->
