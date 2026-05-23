<!-- purpose: per-interface spec skeleton (protocol + contract + owners + errors + SLA + fixtures) -->
<!-- consumes: architecture map + sample payloads + SRE SLO doc -->
<!-- produces: one entry in interfaces[] of the inventory -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~350 tokens loaded as template context -->

# Interface Specification: [Interface Name]

**Version:** [X.X]
**Date:** [Date]
**Author:** [Name]

## Overview

| Attribute | Value |
|-----------|-------|
| **Interface ID** | IF-XXX |
| **Interface Name** | [Name] |
| **Type** | User / System / Hardware / Communication |
| **Direction** | Inbound / Outbound / Bidirectional |
| **Description** | [What this interface does — one sentence] |

## Connected Systems

| System | Role | Contact |
|--------|------|---------|
| Our system | Provider / Consumer | [Name] |
| [External system] | Provider / Consumer | [Name] |

## Data Specification

### [Message/Payload Name]

**Direction:** Inbound / Outbound
**Format:** JSON / XML / CSV / Binary / Event
**Encoding:** UTF-8

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| [field_name] | string/int/bool | Y/N | [rules] | [description] |

**Example Payload (literal values, no placeholders):**
```json
{
  "field1": "actual-example-value",
  "field2": 123
}
```

## Technical Specification

| Attribute | Value |
|-----------|-------|
| **Protocol** | REST / gRPC / SFTP / Queue / AsyncAPI |
| **Spec source** | [OpenAPI URL or Protobuf path — source of truth] |
| **Authentication** | [OAuth 2.0 / API Key / mTLS — cite vendor docs] |
| **Rate limit** | [X requests per Y or "tbd"] |
| **Timeout** | [X seconds — both caller and callee] |
| **Idempotency** | [Key field name + dedup window, or N/A] |
| **Retry safe?** | Yes / No / [conditions] |

## Operational Specification

| Attribute | Value |
|-----------|-------|
| **Frequency** | Real-time / Batch / On-demand |
| **Volume** | [Expected messages/day — mark "tbd" until load test] |
| **SLA** | [Availability, response time — mark "tbd" until measured] |

## Error Handling

| Error Code | Condition | Consumer must | Retry? | Alert? |
|------------|-----------|---------------|--------|--------|
| [Code] | [When it occurs] | [Specific action] | Y/N | Y/N |

_Error codes verified against: [live traffic capture / vendor docs URL]_

## Security Requirements
- Auth type: [cite vendor docs URL]
- [Specific requirement]

## Traceability
- Requirements: [REQ-XXX]
- Design: design.md section [X]
- Test plan: test-plan.md IF-XXX contract tests
