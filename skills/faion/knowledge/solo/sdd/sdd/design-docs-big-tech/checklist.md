# Design Doc Checklist

Step-by-step checklist for writing effective design documents, based on practices from Google, Amazon, Uber, Spotify, and other leading tech companies.

---

## Pre-Writing Phase

### 1. Determine Document Scope

- [ ] Identify the change type:
  - [ ] Bug fix (no doc needed)
  - [ ] Small feature (mini-doc, optional)
  - [ ] Medium feature (standard design doc)
  - [ ] Large feature (detailed RFC)
  - [ ] Architecture change (RFC + ADR)
  - [ ] New service/system (full design doc + architecture review)

- [ ] Select appropriate template:
  - [ ] Lightweight (team-scope changes)
  - [ ] Standard (cross-team impact)
  - [ ] Heavyweight (org/company-wide impact)

### 2. Gather Context

- [ ] Review existing documentation for the system
- [ ] Understand current architecture and constraints
- [ ] Identify affected systems and dependencies
- [ ] Research similar solutions in codebase or industry
- [ ] List key stakeholders who need to review

### 3. Identify Reviewers and Approvers

- [ ] Technical reviewers (engineers from affected teams)
- [ ] Architecture/Principal engineer (for significant changes)
- [ ] Product manager (for user-facing changes)
- [ ] Security reviewer (for sensitive data/auth changes)
- [ ] Limit total reviewers to under 10 people

---

## Writing Phase

### 4. Write the Overview

- [ ] One-paragraph summary of what this doc covers
- [ ] Why this document exists (motivation)
- [ ] What problem you're solving
- [ ] Target audience for the document

**Quality Check:**
- [ ] Can someone unfamiliar with the project understand the overview?
- [ ] Is the scope clearly defined?

### 5. Document Context and Background

- [ ] What led to this design being needed?
- [ ] Current state of the system
- [ ] Pain points or limitations being addressed
- [ ] Any relevant history or previous attempts
- [ ] Links to related documents, ADRs, or specs

**Quality Check:**
- [ ] Can a newcomer follow any links to get full context?
- [ ] Is the background 1-2 paragraphs (or up to a page for complex projects)?

### 6. Define Goals and Non-Goals

**Goals:**
- [ ] List 3-5 specific, measurable goals
- [ ] Prioritize goals (must-have vs nice-to-have)
- [ ] Align goals with business/product objectives

**Non-Goals:**
- [ ] Explicitly state what this design does NOT address
- [ ] Explain why certain things are out of scope
- [ ] Prevent scope creep during review

**Quality Check:**
- [ ] Are goals specific enough to evaluate success?
- [ ] Do non-goals prevent misunderstanding of scope?

### 7. Propose the Design

**High-Level Overview:**
- [ ] System architecture diagram (if applicable)
- [ ] Component relationships
- [ ] Data flow description

**Detailed Design:**
- [ ] Each major component described
- [ ] API contracts (endpoints, request/response formats)
- [ ] Data model (schema, structures)
- [ ] Key algorithms or logic
- [ ] Integration points with existing systems

**Quality Check:**
- [ ] Is every verb clear about who/what is performing the action?
- [ ] Are technical terms defined or linked?
- [ ] Would another engineer be able to implement from this?

### 8. Document Alternatives Considered

**For each alternative (minimum 2-3):**
- [ ] Description of the approach
- [ ] Pros (benefits)
- [ ] Cons (drawbacks)
- [ ] Why it was not chosen

**Required Alternative:**
- [ ] "Do nothing" baseline - what happens if we don't build this?

**Quality Check:**
- [ ] Are alternatives genuine options, not strawmen?
- [ ] Is the reasoning for rejection clear and fair?
- [ ] Would the chosen approach still win if reviewed by others?

### 9. Address Cross-Cutting Concerns

**Security:**
- [ ] Authentication/authorization implications
- [ ] Data encryption (at rest, in transit)
- [ ] Input validation and sanitization
- [ ] Threat model (if applicable)

**Privacy:**
- [ ] PII handling
- [ ] Data retention policies
- [ ] GDPR/CCPA compliance (if applicable)
- [ ] User consent requirements

**Scalability:**
- [ ] Expected load and growth
- [ ] Bottleneck analysis
- [ ] Horizontal/vertical scaling strategy
- [ ] Database scaling considerations

**Reliability:**
- [ ] Failure modes and recovery
- [ ] Retry and timeout strategies
- [ ] Circuit breaker patterns
- [ ] Graceful degradation

**Monitoring and Observability:**
- [ ] Key metrics to track
- [ ] Alerting thresholds
- [ ] Logging strategy
- [ ] Dashboards needed

**Quality Check:**
- [ ] Are security concerns addressed proportionally to risk?
- [ ] Is scalability realistic for expected growth?

### 10. Define SLAs (for services)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Availability | 99.9% | Uptime monitoring |
| P99 Latency | <100ms | APM metrics |
| Throughput | 1000 RPS | Load testing |
| Error Rate | <0.1% | Error tracking |

- [ ] Define SLAs appropriate for service tier
- [ ] Align with dependent services
- [ ] Plan for SLA monitoring

### 11. Plan Rollout and Migration

**Rollout Strategy:**
- [ ] Phased rollout plan
- [ ] Feature flag strategy
- [ ] Canary/blue-green deployment
- [ ] Rollback plan

**Migration (if applicable):**
- [ ] Data migration steps
- [ ] Backward compatibility period
- [ ] Deprecation timeline
- [ ] Communication plan

**Quality Check:**
- [ ] Is rollback possible at each phase?
- [ ] Are dependencies sequenced correctly?

### 12. List Open Questions

- [ ] Document unresolved questions
- [ ] Assign owners to each question
- [ ] Set deadlines for resolution
- [ ] Mark questions that block implementation

**Quality Check:**
- [ ] Are questions specific enough to answer?
- [ ] Is it clear which questions block progress?

### 13. Add References

- [ ] Link to related design docs
- [ ] Link to ADRs
- [ ] Link to specs and PRDs
- [ ] External resources (papers, blog posts)
- [ ] API documentation

---

## Review Phase

### 14. Pre-Review Self-Check

**Content Quality:**
- [ ] Document is complete (all sections filled)
- [ ] Technical accuracy verified
- [ ] Diagrams are clear and labeled
- [ ] No placeholder text remaining
- [ ] Spell-check and grammar review

**Readability:**
- [ ] Can be understood without prior context
- [ ] Jargon is explained or linked
- [ ] Length is appropriate for scope
- [ ] Sections are logically ordered

**Trade-offs:**
- [ ] Disadvantages of chosen approach are documented
- [ ] Trade-offs are explicitly stated
- [ ] Decision rationale is clear

### 15. Circulate for Review

**Distribution:**
- [ ] Share with identified reviewers
- [ ] Use appropriate channels (mailing list, doc sharing, RFC tool)
- [ ] Set clear review deadline
- [ ] Specify type of feedback needed

**Review Period:**
- [ ] Lightweight changes: 2-3 days
- [ ] Standard changes: 1 week
- [ ] Major changes: 2-3 weeks

### 16. Collect and Address Feedback

**During Review:**
- [ ] Monitor for comments
- [ ] Respond to questions promptly
- [ ] Clarify misunderstandings
- [ ] Note recurring concerns

**After Review:**
- [ ] Address all comments (respond or incorporate)
- [ ] Update document based on feedback
- [ ] Resolve conflicts through discussion
- [ ] Mark addressed comments as resolved

### 17. Obtain Approvals

- [ ] All required approvers have signed off
- [ ] No unresolved blocking concerns
- [ ] Approval documented in system
- [ ] Date and approver names recorded

---

## Post-Approval Phase

### 18. Finalize Document

- [ ] Update status to "Approved" or "Implementing"
- [ ] Record final approval date
- [ ] Archive review comments
- [ ] Lock document from major edits (minor updates OK)

### 19. Create ADR (if needed)

For significant architectural decisions:
- [ ] Create Architecture Decision Record
- [ ] Capture: context, decision, consequences
- [ ] Link to original design doc
- [ ] Store in team's ADR repository

### 20. Communicate Decision

- [ ] Announce to affected teams
- [ ] Update project documentation
- [ ] Create implementation tasks/tickets
- [ ] Schedule kickoff if needed

---

## During Implementation

### 21. Keep Document Updated

- [ ] Note significant deviations from design
- [ ] Update if scope changes
- [ ] Mark obsolete sections
- [ ] Link to implementation PRs

### 22. Document Lessons Learned

After implementation:
- [ ] What went well?
- [ ] What would you change?
- [ ] Were estimates accurate?
- [ ] Add retrospective notes to document

---

## Quick Reference: Section Length Guide

| Section | Typical Length |
|---------|---------------|
| Overview | 1-2 paragraphs |
| Background | 1-2 paragraphs (up to 1 page) |
| Goals/Non-Goals | 3-5 bullets each |
| Design | 1-3 pages |
| Alternatives | 1/2 - 1 page |
| Cross-cutting | 1/2 - 1 page |
| Rollout | 1/2 page |
| Open Questions | 3-7 questions |

**Total Document Length:**
- Mini-doc: 1-2 pages
- Standard: 2-5 pages
- Detailed RFC: 5-10 pages
- Heavyweight: 10+ pages (with justification)

---

## Amazon 6-Pager Specific Checklist

If writing in Amazon's narrative format:

- [ ] No bullet points in main document
- [ ] Full narrative prose throughout
- [ ] Data and graphs in appendix only
- [ ] Can be understood without appendix
- [ ] Written for unfamiliar reader
- [ ] Every word adds value (no fluff)
- [ ] Logical flow from intro to conclusion
- [ ] Maximum 6 pages (excluding appendix)

---

## Review Meeting Checklist (if applicable)

**Before Meeting:**
- [ ] Distribute document 24+ hours in advance
- [ ] Reserve meeting room/video call
- [ ] Invite all reviewers
- [ ] Prepare for common questions

**During Meeting:**
- [ ] Silent reading period (10-15 minutes)
- [ ] Discussion of key concerns
- [ ] Capture action items
- [ ] Note decisions made

**After Meeting:**
- [ ] Distribute meeting notes
- [ ] Update document with decisions
- [ ] Follow up on action items
- [ ] Schedule follow-up if needed

---

*Checklist | Design Docs at Big Tech | v2.0*
