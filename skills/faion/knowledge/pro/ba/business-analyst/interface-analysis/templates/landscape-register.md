# Integration Landscape Register — [Programme / Domain]

**Last Updated:** [Date]
**Owner:** [Name]
**Next Review:** [Date]

## Register

| IF-ID | Source SYS | Target SYS | Channel | Data | Direction | Frequency | Criticality (1-4) | Sensitivity | Source Owner | Target Owner | SLA | Standard? | Notes |
|-------|------------|------------|---------|------|-----------|-----------|-------------------|-------------|--------------|-------------|-----|-----------|-------|
| IF-001 | CRM | Billing | REST | Customer master | Out | Real-time | 1 | Confidential | Team A | Team B | 99.9% | OpenAPI in repo X | replaces legacy SFTP IF-014 |
| IF-002 | HRIS | IDP | SCIM | User accounts | Out | Hourly | 1 | Restricted | Team C | Team D | 99.5% | yes | scoped to active employees |

Channels: REST / SOAP / GraphQL / gRPC / SFTP / S3 / MQ / Kafka / EDI-X12 / HL7 / SWIFT / EDIFACT / JDBC / fixed-width

Criticality: 1 = business-critical, 2 = important, 3 = supporting, 4 = informational

Sensitivity: public / internal / confidential / restricted / unknown (unknown requires human classification)

## Shadow IT Candidates

Interfaces observed in logs/Slack/email not present in register above:

| Signal | Source/Target (suspected) | Evidence | Action |
|--------|--------------------------|----------|--------|
| [Signal] | [Suspected parties] | [Log line / Slack mention] | [Investigate / Register / Retire] |

## Governance Notes

- Standard API contract: [link to standards/api-contract-standard.md]
- Non-compliant interfaces (from governance diff): [IF-IDs or "none"]
- Interfaces with valid_until expired: [IF-IDs or "none"]
