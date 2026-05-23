<!-- purpose: Markdown skeleton naming both axes. | consumes: see content/02-output-contract.xml inputs | produces: artefact conforming to content/02-output-contract.xml (cap-pacelc-walkthrough) | depends-on: content/01-core-rules.xml | token-budget-impact: small (template is loaded only when an artefact is being authored) -->
# CAP / PACELC Walkthrough — <artefact_id>

**Owner:** <@handle>
**Version:** 1.0.0
**Last reviewed:** 2026-05-23

## Decision

- CAP under partition: AP | CP
- PACELC otherwise (Else): EL | EC

## Rationale

Cites RPO/RTO + read/write split + partition exposure.

## Inputs used

| Path | Type |
|------|------|
| policy/rpo-rto.md | policy |
| observability/orders-read-write-split.json | metric |
