# Quality Attribute Scenario: [Short Title]

**Quality Attribute:** [Performance / Availability / Security / Maintainability / Scalability / ...]
**ISO/IEC 25010 Characteristic:** [e.g., Performance Efficiency — Time Behaviour]
**Priority:** [(H/M/L, H/M/L) = (Importance, Difficulty)]

## Scenario

| Part | Value |
|------|-------|
| **Source** | Who or what generates the stimulus (user, attacker, time trigger, external system) |
| **Stimulus** | The event or condition that occurs (10x traffic spike, AZ failure, brute-force attack) |
| **Environment** | Context: normal operation / peak load / degraded mode / under attack |
| **Artifact** | Affected part of the system (API gateway, checkout service, auth service, entire platform) |
| **Response** | How the system responds (auto-scale, rate-limit, degrade gracefully, alert ops) |
| **Response Measure** | Quantitative success criterion with unit (p99 &lt; 500ms, 0% errors, scale within 60s) |

## Fitness Function

- [ ] Tool: [k6 / chaos-mesh / zap / locust / ArchUnit / ...]
- [ ] Wired to: [CI pipeline / pre-prod / weekly scheduled run]
- [ ] Threshold: [exact number from Response Measure above]
- [ ] Owner: [engineer name]

## Source / Rationale

[Cite competitor SLA, incident postmortem, regulatory requirement, or customer contract. No invented numbers.]
