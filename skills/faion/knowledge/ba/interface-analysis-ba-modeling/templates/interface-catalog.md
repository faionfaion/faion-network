<!-- purpose: solution-wide interface catalog (one-row-per-interface index) -->
<!-- consumes: enumerate step output -->
<!-- produces: top-level interfaces[] index referenced by inventory -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200 tokens -->

# Interface Catalog: [System Name]

**Version:** [X.X]
**Date:** [Date]
**Author:** [Name]

## Interface Summary

| ID | Name | Type | Direction | External System | Protocol | Status |
|----|------|------|-----------|-----------------|----------|--------|
| IF-001 | [Name] | System | Outbound | [System] | REST | Active |
| IF-002 | [Name] | System | Inbound | [System] | SFTP | Design |
| IF-003 | [Name] | User | Bidirectional | User | Web UI | Active |

## Interface Diagram

```
[External System A] → IF-001 → [Our System] → IF-003 → [User]
                                    |
                                    ↓
                                IF-002 (SFTP)
                                    |
                                    ↓
                            [External System B]
```

## Spec Links

| ID | Spec | Source of Truth |
|----|------|----------------|
| IF-001 | [link to interface-spec.md] | [OpenAPI URL] |
| IF-002 | [link to interface-spec.md] | [Data dictionary] |

## Drift Check

Run: `./interface-drift-check.sh committed-openapi.yaml https://api.example.com/openapi.yaml`
CI: nightly GitHub Action, alerts on breaking changes → opens SDD todo/ task.
