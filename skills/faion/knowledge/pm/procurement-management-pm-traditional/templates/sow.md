<!--
purpose: Statement of Work template with scope, deliverables, acceptance, payment schedule
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~200-1000 tokens when loaded as context
variables:
  - name: project_name
    type: string
    required: true
    description: The engagement's name as both parties will use it on invoices and in email subject lines. Pick it once - two names for one SOW is how a disputed invoice starts.
  - name: date
    type: string
    required: true
    description: Date of this version, ISO. Every change order that follows is dated against it, and a SOW without a version date cannot be shown to predate the work it authorised.
  - name: buyer_entity
    type: string
    required: true
    description: The contracting legal entity on your side, exact registered name. A SOW naming a brand instead of an entity is a document your lawyer will make you redo after the dispute starts.
  - name: vendor_entity
    type: string
    required: true
    description: The vendor's legal entity, exact registered name - check it against their invoice details, not their website footer. The trading name and the entity are often different companies.
  - name: contract_type
    type: enum
    required: true
    options: [FFP, T-and-M, T-and-M-cap, CPFF]
    description: Pricing structure. Fixed price moves risk to the vendor and you pay for that; uncapped time-and-materials moves all of it to you. If you cannot say which risk you are buying, sign neither.
  - name: notice_period
    type: string
    required: true
    description: Termination notice in days, both directions. This is the field people skip, then discover it means three months of paying for work they had already stopped wanting.
  - name: acceptance_owner
    type: string
    required: true
    description: Who signs that a deliverable is accepted. Payment is tied to acceptance, so an unnamed acceptor means the vendor escalates to whoever will approve fastest rather than most carefully.
-->

# Statement of Work: {{project_name}}

**Version:** 1.0
**Date:** {{date}}
**Buyer:** {{buyer_entity}}
**Vendor:** {{vendor_entity}}
**Contract Type:** {{contract_type}}
**Acceptance authority:** {{acceptance_owner}}

## 1. Background
[Context and business need driving this procurement]

## 2. Scope of Work

### In Scope
- [Item 1]
- [Item 2]

### Out of Scope
- [Exclusion 1]

## 3. Deliverables

| ID | Deliverable | Acceptance Criteria | Due Date |
|----|-------------|---------------------|----------|
| D1 | [Name] | [Testable criteria — metric, threshold] | [Date] |
| D2 | [Name] | [Testable criteria] | [Date] |

## 4. Milestones and Payment

| Milestone | Deliverables | Payment % | Date |
|-----------|-------------|-----------|------|
| Kickoff | — | 25% | [Date] |
| [Mid-point] | D1 | 50% | [Date] |
| Final acceptance | D2 | 25% | [Date] |

Payment is tied to acceptance by {{acceptance_owner}}, not to calendar dates.

## 5. Assumptions
- [Buyer will provide X by Y date]
- [Access to Z environment granted by kickoff]

## 6. Dependencies
- [Buyer-owned dependency]
- [Third-party dependency]

## 7. Change Process
Changes to scope, timeline, or price require a written Change Order signed by both parties before work begins.

## 8. Exit Terms
- Notice period: {{notice_period}}
- Data handback: within [Y] days of termination
- Transition assistance: [Z] hours included
- IP transfer: upon final payment receipt

## 9. Required Legal Clauses (legal review required)
- [ ] Limitation of liability cap
- [ ] Indemnification scope
- [ ] IP ownership and work-for-hire language
- [ ] Data residency and sub-processor terms
- [ ] Jurisdiction and governing law
- [ ] Termination for convenience
