# Design Doc Checklist

Step-by-step checklist for writing effective design documents. Use this as a guide from initial planning through approval and implementation.

## Pre-Writing Phase

### 1. Determine if Design Doc is Needed

- [ ] Feature takes > 1 engineering week to build
- [ ] Change spans multiple PRs or services
- [ ] High security or privacy implications
- [ ] API changes affecting other teams
- [ ] Requirements are unclear or ambiguous
- [ ] Stakeholder alignment needed

**Skip if:** Bug fix, < 1 day work, internal refactor with same behavior, prototype/spike

### 2. Choose Format

| Situation | Recommended Format |
|-----------|-------------------|
| Internal team change | Lightweight design doc |
| Cross-team service | Full design doc (Google-style) |
| New product initiative | PR-FAQ (Amazon-style) |
| Platform/infra change | RFC (Uber-style) |
| Strategic bet | DIBB (Spotify-style) |
| Architectural decision | ADR |

### 3. Identify Stakeholders

- [ ] **Author(s)** - Who will write the doc?
- [ ] **Required reviewers** - Who must approve? (cap at 5-7)
- [ ] **Optional reviewers** - Who might have useful input?
- [ ] **Affected teams** - Who needs to be informed?
- [ ] **Decision maker** - Who has final say if disagreement?

### 4. Gather Context

- [ ] Related design docs and ADRs
- [ ] Existing system architecture diagrams
- [ ] Requirements documents or tickets
- [ ] Relevant metrics and data
- [ ] Previous attempts or related work
- [ ] Constraints (timeline, budget, tech)

---

## Writing Phase

### 5. Draft Core Sections

#### Overview / Summary
- [ ] 1-2 paragraphs explaining what and why
- [ ] Readable by someone unfamiliar with project
- [ ] Clear problem statement

#### Context and Background
- [ ] What led to this design being needed?
- [ ] Current state of the system
- [ ] Key constraints and assumptions

#### Goals
- [ ] Specific, measurable objectives
- [ ] Success criteria (how will we know it worked?)
- [ ] Alignment with business/product goals

#### Non-Goals (Critical!)
- [ ] Explicitly state what is NOT in scope
- [ ] Address common assumptions that are incorrect
- [ ] Set boundaries for future scope creep discussions

### 6. Draft Design Section

#### System Overview
- [ ] High-level architecture diagram
- [ ] Key components and their responsibilities
- [ ] Data flow between components

#### Detailed Design
- [ ] Component-by-component breakdown
- [ ] Interface definitions (APIs, contracts)
- [ ] Data model (schemas, structures)
- [ ] Key algorithms or business logic

#### External Integrations
- [ ] Dependencies on other systems
- [ ] APIs consumed
- [ ] Third-party services

### 7. Analyze Alternatives

- [ ] At least 2-3 alternatives considered
- [ ] For each alternative:
  - [ ] Brief description
  - [ ] Pros (benefits)
  - [ ] Cons (drawbacks)
  - [ ] Why not chosen (clear rationale)
- [ ] Include "do nothing" as an alternative if applicable

### 8. Address Cross-Cutting Concerns

#### Security
- [ ] Authentication and authorization
- [ ] Data encryption (at rest, in transit)
- [ ] Input validation
- [ ] Threat model (if high-risk)
- [ ] Compliance requirements (GDPR, SOC2, etc.)

#### Privacy
- [ ] PII handling
- [ ] Data retention policies
- [ ] User consent requirements
- [ ] Data access controls

#### Scalability
- [ ] Expected load (current and future)
- [ ] Scaling strategy (horizontal, vertical)
- [ ] Bottleneck identification
- [ ] Performance targets (latency, throughput)

#### Reliability
- [ ] Failure modes and mitigation
- [ ] Redundancy approach
- [ ] Disaster recovery
- [ ] SLA commitments

#### Observability
- [ ] Logging strategy
- [ ] Metrics to collect
- [ ] Alerting thresholds
- [ ] Dashboards needed

### 9. Plan Implementation

#### Milestones
- [ ] Phase breakdown
- [ ] Dependencies between phases
- [ ] Definition of done for each phase

#### Rollout Strategy
- [ ] Feature flags
- [ ] Gradual rollout percentage
- [ ] Rollback plan
- [ ] Success metrics for each stage

#### Migration (if applicable)
- [ ] Data migration plan
- [ ] Backward compatibility period
- [ ] Deprecation timeline

### 10. Document Open Questions

- [ ] List unresolved questions
- [ ] Identify who can answer each
- [ ] Flag blockers vs nice-to-resolve
- [ ] Set timeline for resolution

---

## Review Phase

### 11. Pre-Review Checklist

- [ ] Spell-check and grammar review
- [ ] All sections complete (no TODOs)
- [ ] Diagrams are clear and labeled
- [ ] Links work and are accessible to reviewers
- [ ] Document permissions set correctly
- [ ] Required approvers identified in doc

### 12. Distribute for Review

- [ ] Send to required reviewers with clear ask
- [ ] Set review deadline (typically 3-5 business days)
- [ ] Provide context in distribution message
- [ ] For async review: specify comment format expectations
- [ ] For meeting review: schedule 60-90 min, include pre-read note

### 13. Conduct Review Meeting (if applicable)

- [ ] Start with 10-20 min silent reading
- [ ] Timebox discussion per section
- [ ] Capture decisions in real-time
- [ ] Assign action items with owners
- [ ] Schedule follow-up if needed

### 14. Iterate Based on Feedback

- [ ] Address all comments (resolve or respond)
- [ ] Make requested changes or explain why not
- [ ] Re-circulate significant changes
- [ ] Resolve disagreements via decision maker

---

## Approval Phase

### 15. Obtain Sign-Off

- [ ] All required approvers have signed
- [ ] All blocking comments resolved
- [ ] Open questions either resolved or explicitly deferred
- [ ] Status updated to "Approved"
- [ ] Approval date recorded

### 16. Communicate Approval

- [ ] Notify affected teams
- [ ] Update relevant tickets/epics
- [ ] Archive in discoverable location
- [ ] Create implementation tickets if needed

---

## Implementation Phase

### 17. Reference During Development

- [ ] Link design doc in implementation PRs
- [ ] Track deviations from design
- [ ] Update doc for significant changes (not typos)
- [ ] Use design doc for onboarding new team members

### 18. Post-Implementation

- [ ] Update status to "Implemented"
- [ ] Add implementation notes section if lessons learned
- [ ] Link to final implementation (code, configs)
- [ ] Extract ADRs for key decisions
- [ ] Archive or update superseded docs

---

## Quality Checklist

### Clarity

- [ ] Readable by engineer unfamiliar with project
- [ ] No unexplained jargon or acronyms
- [ ] Short sentences and paragraphs
- [ ] Clear headers and structure

### Completeness

- [ ] All template sections addressed
- [ ] Alternatives section not skipped
- [ ] Cross-cutting concerns covered
- [ ] Open questions captured

### Accuracy

- [ ] Technical details verified
- [ ] Metrics and data sourced
- [ ] Diagrams match description
- [ ] Links and references valid

### Actionability

- [ ] Clear next steps
- [ ] Decisions are explicit
- [ ] Owners assigned
- [ ] Success criteria measurable

---

## Quick Reference: Section Order

1. **Title and metadata** (author, status, date, reviewers)
2. **Overview** (1-2 paragraphs)
3. **Context and background**
4. **Goals and non-goals**
5. **Design** (overview, detailed, data model, API)
6. **Alternatives considered**
7. **Cross-cutting concerns** (security, privacy, scalability, etc.)
8. **Timeline and milestones**
9. **Open questions**
10. **References**
11. **Appendices** (optional: detailed data, extended diagrams)

---

## Common Mistakes to Avoid

| Mistake | Prevention |
|---------|------------|
| Writing after implementation | Start doc before coding |
| Skipping alternatives section | Always include 2-3 options |
| Too many approvers | Cap at 5-7 required reviewers |
| Design doc as spec | Keep separate: design (why/how), spec (what) |
| Never-ending review | Set deadline, escalate if stuck |
| Missing non-goals | Explicitly state what's out of scope |
| Outdated diagrams | Update or remove when design changes |
| Scattered feedback | Centralize in doc comments |

---

*For templates, see [templates.md](templates.md). For real examples, see [examples.md](examples.md).*
