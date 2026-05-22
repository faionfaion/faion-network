<!--
purpose: Filled-in minimum viable example of a FinTech KYC BA Pack artefact.
consumes: nothing — fixture.
produces: a worked Markdown example for tests / docs.
depends-on: content/02-output-contract.xml + templates/fintech-kyc-ba-pack.md.
token-budget-impact: ~150 tokens.
-->

# FinTech KYC BA Pack — fkyc-smoke-001

- **artefact_id**: fkyc-smoke-001
- **owner**: alice@acme.com
- **status**: active
- **version**: 1.0.0
- **last_reviewed**: 2026-05-22

## Decision

Apply the fintech-kyc-ba-pack procedure to the pilot engagement; emit artefact bound to the scope doc.

## Rationale

Decision cites the scope doc (input A) and the risk register row #3 (input B). The pilot is the canonical instance for this gap; the rationale exceeds the 60-character floor and names every input it relies on.

## Inputs used

- scope_doc — repo:engagements/acme-pilot/scope.md
- risk_register_row3 — repo:engagements/acme-pilot/risk-register.csv#L3

## Notes

Ready for owner review; supersedes none.
