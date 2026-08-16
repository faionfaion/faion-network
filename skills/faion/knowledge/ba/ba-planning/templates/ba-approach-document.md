<!--
purpose: BA approach document — analysis approach, stakeholder list, elicitation plan, deliverables, governance, replan triggers.
consumes: recent task context and a named downstream owner (see Prerequisites)
produces: BA approach document artefact
depends-on: content/02-output-contract.xml
token-budget-impact: ~420 tokens when filled
-->

---
engagement_id: ENG-001
approach: Plan-Driven  # Plan-Driven | Change-Driven | Hybrid
version: "0.1"
approver: name@domain
last_reviewed: 2026-01-01
---

# Business Analysis Approach: <initiative_name>

**Version:** [X.X]
**Date:** <date>
**Business Analyst:** [Name]

## 1. Initiative Overview

[Brief description of the change initiative — what it is, why it exists, and what problem it solves]

## 2. Analysis Approach

**Selected Approach:** <selected_approach>
**Rationale:** [Decision rule applied: clarity level, change frequency, regulatory requirements]

**Per-Artifact Classification (Hybrid only):**

| Artifact | Type | Version Policy |
|----------|------|---------------|
| BRD | Baselined | v1.0 locked before design |
| Stakeholder Register | Living | Updated continuously |
| Process Models | Baselined per phase | Locked at phase sign-off |

## 3. Stakeholders

| ID | Name/Role | Category | Influence | Engagement | Availability |
|----|-----------|----------|-----------|------------|--------------|
| S-01 | [Name] | Sponsor | H | Manage Closely | [When] |
| S-02 | [Name] | Domain SME | M | Keep Informed | [When] |

Hidden stakeholders reviewed: [ ] legal [ ] infosec [ ] procurement [ ] works council [ ] accessibility [ ] downstream API consumers

## 4. Elicitation Plan

| Activity | Technique | Participants | Timing | Deliverable |
|----------|-----------|--------------|--------|-------------|
| <activity> | Interview/Workshop/Survey/Observation/Doc Analysis | <who> | [When] | <output> |

## 5. Deliverables

| ID | Deliverable | Description | Type | Status |
|----|-------------|-------------|------|--------|
| DEL-01 | Stakeholder Register | All parties identified and mapped | Living | draft |
| DEL-02 | Business Requirements Document | Functional requirements, AC, traceability | Baselined | not started |

## 6. Governance

**Requirements Approval:** [Named role — must be a specific person, not "leadership"]
**Change Process:** [How changes to baselined artifacts are handled]
**Review Cadence:** [Frequency — e.g., bi-weekly]
**Escalation Path:** [Defined chain when approval is blocked]

## 7. Risks and Constraints

| Risk/Constraint | Impact | Mitigation |
|-----------------|--------|------------|
| <item> | H/M/L | <action> |

## 8. Replan Triggers

This plan will be replanned when:
- A stakeholder is added or removed from the register.
- A scope change is merged that affects deliverables or governance.
- Two consecutive elicitation sessions are missed.
- last_reviewed is older than 14 days.
