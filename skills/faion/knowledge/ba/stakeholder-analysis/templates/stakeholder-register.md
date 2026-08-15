<!--
purpose: Template fixture for stakeholder-analysis: stakeholder-register.md
consumes: content/01-core-rules.xml
produces: Markdown artefact
depends-on: content/02-output-contract.xml
token-budget-impact: small
variables:
  - name: initiative_name
    type: string
    required: true
    description: The initiative as the stakeholders themselves would name it - the wording on the funding request, not the internal epic key. People have to recognise their own project in the title.
  - name: ba_name
    type: string
    required: true
    description: The analyst who owns this register. Every attitude claim below needs somebody willing to defend it in front of the person it describes.
  - name: register_version
    type: string
    required: true
    default: "1.0"
    description: Version of this register. Bump it whenever a stakeholder is added or a quadrant changes - the engagement plan downstream is built against a specific version.
  - name: date
    type: string
    required: true
    description: The date this register was last checked against reality, ISO. A register older than the last reorganisation is fiction that people still act on.
  - name: next_review
    type: string
    required: true
    description: The date the next refresh is due, ISO. Pick one now - stakeholder maps decay silently and nothing else in the process will remind you.
-->
# Stakeholder Register: {{initiative_name}}

**Version:** {{register_version}}
**Date:** {{date}}
**BA:** {{ba_name}}
**Last Refreshed:** {{date}}
**Next Review:** {{next_review}}

## Stakeholder Table

| ID | Name/Role | Department | Category | Influence | Impact | Attitude | Quadrant | Engagement |
|----|-----------|------------|----------|-----------|--------|----------|----------|------------|
| S-01 | [Name] | [Dept] | Sponsor | H | H | + | Manage Closely | Weekly 1:1 |
| S-02 | [Name] | [Dept] | Domain SME | M | H | 0 | Keep Informed | Monthly digest |
| S-03 | [Name] | [Dept] | End User | L | H | unknown | Keep Informed | Monthly digest |

Categories: Customer / EndUser / Sponsor / DomainSME / ImplementationSME / Tester / Regulator / Supplier
Attitude: + (supportive) / 0 (neutral) / - (resistant) / unknown (no evidence yet)
Quadrant: HH=Manage Closely / HL=Keep Satisfied / LH=Keep Informed / LL=Monitor

## Attitude Evidence Log

All attitude assertions require an evidence entry. No evidence → attitude must be "unknown."

| Stakeholder ID | Attitude Claimed | Evidence Quote / Link | Date | Triangulation Signal |
|---------------|-----------------|----------------------|------|---------------------|
| S-01 | + | "[Quote from kickoff meeting]" | [Date] | Meeting attendance: 4/4 sessions |

## Hidden Stakeholders Review

| Group | Identified? | Stakeholder ID | Notes |
|-------|------------|----------------|-------|
| Legal | [ ] | | |
| Infosec | [ ] | | |
| Procurement | [ ] | | |
| Works council/union | [ ] | | |
| Accessibility | [ ] | | |
| Downstream API consumers | [ ] | | |

## Change Log

| Date | Change | Rationale | Approved By |
|------|--------|-----------|-------------|
| [Date] | Added S-03 | Discovered in stakeholder interview with S-01 | {{ba_name}} |
