# Interface Specification: [Interface Name]

**Version:** [X.X]
**Date:** [Date]
**Author:** [Name]

## Overview

| Attribute | Value |
|-----------|-------|
| **Interface ID** | IF-[NNN] |
| **Interface Name** | [Name] |
| **Type** | User / System / Hardware / Communication |
| **Direction** | Inbound / Outbound / Bidirectional |
| **Description** | [What this interface does] |

## Connected Systems

| System | Role | Team Owner | Contact |
|--------|------|------------|---------|
| [This solution] | Provider / Consumer | [Team] | [Name] |
| [External system] | Provider / Consumer | [Team] | [Name] |

## Data Specification

### [Message/Payload Name]

**Direction:** [Inbound/Outbound]
**Format:** [JSON/XML/CSV/Binary/Fixed-width]
**Encoding:** [UTF-8/ASCII]

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| [field_name] | [type] | Y/N | [rules] | [description] |

## Technical Specification

| Attribute | Value |
|-----------|-------|
| **Protocol** | [REST/SOAP/SFTP/MQ/EDI/HL7/SWIFT] |
| **Endpoint/Path** | [URL or file path pattern] |
| **Method** | [GET/POST/PUT/PATCH/DELETE — if REST] |
| **Authentication** | [OAuth2/API Key/mTLS/SFTP key] |
| **Rate Limit** | [X requests per Y — if applicable] |
| **Timeout** | [X seconds] |
| **Versioning Strategy** | [URI versioning/Header versioning/None] |

## Operational Specification

| Attribute | Value |
|-----------|-------|
| **Frequency** | [Real-time/Batch/On-demand] |
| **Schedule** | [If batch — cron expression or description] |
| **Volume (avg)** | [Expected messages/records per period] |
| **Volume (peak)** | [Peak expected] |
| **SLA** | [Availability %, response time P95] |
| **Criticality Tier** | [1-4 — requires human approval for tier-1] |

## Error Handling

| Error Condition | HTTP/Error Code | Response | Retry? | Retry Strategy | Notification |
|-----------------|----------------|----------|--------|---------------|--------------|
| [Condition 1] | [Code] | [Action] | Y/N | [Exponential backoff / N attempts] | [Who/How] |

## Security Requirements

- Authentication: [Mechanism]
- Authorization: [Roles/scopes required]
- Encryption in transit: [TLS version]
- Encryption at rest: [If applicable]
- Data sensitivity: [public/internal/confidential/restricted]
- PII fields: [List fields containing PII]

## Dependencies

- [Dependency 1 — what must exist/be operational for this interface to function]
