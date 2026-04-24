# Quality Attributes Analysis Checklist

Step-by-step checklist for conducting quality attributes analysis using ATAM methodology.

---

## Quick Analysis (30-60 minutes)

For smaller projects or initial assessment:

### 1. Identify Key Stakeholders
- [ ] List all stakeholder groups (users, ops, security, business, dev)
- [ ] Identify decision makers and their authority
- [ ] Note each stakeholder's primary quality concerns
- [ ] Determine who has final say on trade-offs

### 2. Define Top Quality Attributes
- [ ] Select 3-5 most critical quality attributes
- [ ] Rank them by business priority (MoSCoW: Must/Should/Could/Won't)
- [ ] Identify any hard constraints (regulatory, SLA, technical)
- [ ] Note known conflicts between attributes

### 3. Create Key Scenarios
- [ ] Write 1-2 scenarios per critical quality attribute
- [ ] Include: Source, Stimulus, Environment, Response, Measure
- [ ] Ensure measures are quantifiable
- [ ] Validate scenarios with stakeholders

### 4. Document Trade-offs
- [ ] Identify obvious trade-offs (performance vs security, etc.)
- [ ] Note which attribute wins in each conflict
- [ ] Document rationale for decisions
- [ ] Get stakeholder sign-off

---

## Standard Analysis (Half-day to Full-day)

For medium projects requiring systematic approach:

### Phase 1: Preparation (1-2 hours)

#### 1.1 Stakeholder Identification
- [ ] Create stakeholder registry with roles and concerns
- [ ] Schedule stakeholder interviews or workshops
- [ ] Prepare quality attribute questionnaire
- [ ] Review existing documentation (requirements, SLAs, contracts)

#### 1.2 Business Context
- [ ] Document business drivers (growth, cost, compliance, etc.)
- [ ] Identify mission-critical scenarios
- [ ] Note regulatory and compliance requirements
- [ ] Understand competitive pressures and market constraints

#### 1.3 Technical Context
- [ ] Review current architecture (if exists)
- [ ] Identify technology constraints
- [ ] Note integration requirements
- [ ] Document existing quality metrics and SLOs

### Phase 2: Quality Attribute Elicitation (2-3 hours)

#### 2.1 Attribute Identification
- [ ] Use ISO 25010 as checklist of quality characteristics
- [ ] Have stakeholders rate importance of each attribute (1-5)
- [ ] Identify unstated assumptions about quality
- [ ] Probe for "of course it should..." requirements

#### 2.2 Scenario Generation
For each high-priority attribute:
- [ ] Generate 3-5 specific scenarios
- [ ] Include normal operation scenarios
- [ ] Include stress/overload scenarios
- [ ] Include failure/attack scenarios
- [ ] Ensure scenarios are testable

#### 2.3 Scenario Refinement
- [ ] Quantify response measures (latency in ms, uptime %, etc.)
- [ ] Specify environment conditions precisely
- [ ] Identify the artifact/component involved
- [ ] Validate scenarios are realistic and achievable

### Phase 3: Prioritization (1-2 hours)

#### 3.1 Build Utility Tree
- [ ] Create root node "Utility" (overall system value)
- [ ] Add quality attributes as first-level children
- [ ] Refine each attribute into specific concerns
- [ ] Add scenarios as leaf nodes

#### 3.2 Prioritize Scenarios
For each scenario, rate:
- [ ] Business importance: (H)igh, (M)edium, (L)ow
- [ ] Technical difficulty: (H)ard, (M)edium, (E)asy
- [ ] Combined priority: (H,H), (H,M), (M,H), etc.
- [ ] Focus on (H,H) and (H,M) scenarios

#### 3.3 Identify Architectural Drivers
- [ ] List scenarios with (H,H) priority
- [ ] These are the architectural drivers
- [ ] Ensure all drivers have clear acceptance criteria
- [ ] Get stakeholder agreement on driver list

### Phase 4: Trade-off Analysis (1-2 hours)

#### 4.1 Identify Conflicts
- [ ] Map conflicting quality attributes
- [ ] Document specific conflict scenarios
- [ ] Note which attributes must win in each case
- [ ] Identify any "must have both" situations

#### 4.2 Evaluate Tactics
For each architectural driver:
- [ ] List applicable tactics
- [ ] Evaluate impact on other quality attributes
- [ ] Estimate implementation complexity
- [ ] Consider operational implications

#### 4.3 Document Decisions
- [ ] Create decision record for each major trade-off
- [ ] Include context, decision, consequences
- [ ] Note alternatives considered
- [ ] Get stakeholder approval

### Phase 5: Documentation (1 hour)

#### 5.1 Quality Attribute Specification
- [ ] Create formal QA specification document
- [ ] Include all prioritized scenarios
- [ ] Document accepted trade-offs
- [ ] Add verification criteria

#### 5.2 NFR Traceability
- [ ] Link scenarios to architecture components
- [ ] Map tactics to implementation tasks
- [ ] Create verification test cases
- [ ] Set up monitoring dashboards

---

## Full ATAM Analysis (3-4 days)

For large, mission-critical systems:

### Day 0: Preparation

#### Pre-work Distribution
- [ ] Send architecture documentation to evaluation team
- [ ] Distribute ATAM overview to participants
- [ ] Collect stakeholder availability
- [ ] Prepare presentation templates

#### Team Formation
- [ ] Assemble evaluation team (3-5 external members)
- [ ] Assign roles: lead, scribe, timekeeper
- [ ] Brief team on project context
- [ ] Review similar ATAM evaluations for patterns

### Day 1: Architecture Presentation (Phase 1)

#### Step 1: Present ATAM (1 hour)
- [ ] Explain ATAM purpose and process
- [ ] Set expectations for outputs
- [ ] Clarify roles and responsibilities
- [ ] Address questions about methodology

#### Step 2: Present Business Drivers (1 hour)
- [ ] Project manager presents business context
- [ ] Document primary business goals
- [ ] Identify key stakeholders and their concerns
- [ ] Note constraints and assumptions

#### Step 3: Present Architecture (2 hours)
- [ ] Architect presents high-level architecture
- [ ] Show key architectural patterns used
- [ ] Explain major design decisions
- [ ] Highlight known trade-offs

#### Step 4: Identify Architectural Approaches (1 hour)
- [ ] Catalog architectural styles in use
- [ ] Note patterns for each quality attribute
- [ ] Document approaches for handling failures
- [ ] List integration strategies

### Day 2: Analysis (Phase 1 continued)

#### Step 5: Generate Utility Tree (2 hours)
- [ ] Create utility tree structure
- [ ] Populate with quality attributes
- [ ] Add refinements and scenarios
- [ ] Prioritize using (Importance, Difficulty)

#### Step 6: Analyze Approaches (4 hours)
For each high-priority scenario:
- [ ] Map to architectural approach
- [ ] Identify sensitivity points
- [ ] Identify trade-off points
- [ ] Document risks and non-risks

### Day 3: Stakeholder Scenarios (Phase 2)

#### Step 7: Brainstorm Scenarios (2 hours)
- [ ] Facilitate scenario brainstorming session
- [ ] Each stakeholder proposes scenarios
- [ ] Consolidate similar scenarios
- [ ] Prioritize by voting

#### Step 8: Analyze Stakeholder Scenarios (4 hours)
- [ ] Merge with utility tree scenarios
- [ ] Analyze additional high-priority scenarios
- [ ] Uncover new risks and trade-offs
- [ ] Validate previous findings

### Day 4: Results (Phase 2 continued)

#### Step 9: Present Results (2 hours)
- [ ] Compile all findings
- [ ] Organize risks into themes
- [ ] Create risk summary for each business driver
- [ ] Prepare final presentation

#### Final Deliverables
- [ ] Risk catalog with severity ratings
- [ ] Non-risk documentation (validated decisions)
- [ ] Sensitivity point analysis
- [ ] Trade-off point documentation
- [ ] Risk themes and mitigation recommendations
- [ ] Prioritized action items

---

## Post-Analysis Activities

### Immediate Follow-up (Week 1)

- [ ] Distribute ATAM report to all participants
- [ ] Schedule follow-up meetings for clarification
- [ ] Assign owners to high-severity risks
- [ ] Create tickets for mitigation actions

### Short-term (Month 1)

- [ ] Address critical risks
- [ ] Implement monitoring for sensitivity points
- [ ] Update architecture documentation
- [ ] Revise SLOs based on findings

### Ongoing

- [ ] Review quality metrics quarterly
- [ ] Conduct lightweight reassessment after major changes
- [ ] Update utility tree as priorities shift
- [ ] Maintain risk register

---

## Quality Attribute Quick Reference

### Performance Checklist
- [ ] Response time targets defined (p50, p95, p99)
- [ ] Throughput requirements quantified
- [ ] Resource utilization limits set
- [ ] Peak load scenarios documented
- [ ] Performance testing strategy defined

### Availability Checklist
- [ ] Uptime SLA defined (99.9%, 99.99%, etc.)
- [ ] MTTR targets set
- [ ] Failure modes identified
- [ ] Redundancy strategy documented
- [ ] Disaster recovery plan exists

### Security Checklist
- [ ] Threat model completed
- [ ] Authentication requirements defined
- [ ] Authorization model documented
- [ ] Encryption requirements specified
- [ ] Compliance requirements noted

### Scalability Checklist
- [ ] Growth projections documented
- [ ] Scaling strategy defined (horizontal/vertical)
- [ ] Bottlenecks identified
- [ ] Capacity planning completed
- [ ] Auto-scaling triggers defined

### Maintainability Checklist
- [ ] Deployment frequency targets set
- [ ] Code quality metrics defined
- [ ] Documentation requirements specified
- [ ] Testing coverage targets set
- [ ] Technical debt management process exists

### Reliability Checklist
- [ ] Error rate targets defined
- [ ] Retry and timeout policies documented
- [ ] Circuit breaker thresholds set
- [ ] Graceful degradation scenarios defined
- [ ] Chaos engineering plans exist

---

## Verification Checklist

### Scenario Quality
- [ ] Every scenario has all six parts (source, stimulus, environment, artifact, response, measure)
- [ ] Response measures are quantifiable
- [ ] Scenarios are testable
- [ ] Scenarios cover normal, stress, and failure conditions

### Prioritization Quality
- [ ] All high-priority scenarios have architectural drivers
- [ ] Priorities reflect actual business value
- [ ] Stakeholders agree on prioritization
- [ ] (H,H) scenarios receive most attention

### Trade-off Quality
- [ ] All conflicts are explicitly documented
- [ ] Trade-off decisions have clear rationale
- [ ] Stakeholders accept trade-off choices
- [ ] No hidden conflicts remain

### Documentation Quality
- [ ] QA specification is complete
- [ ] ADRs created for major decisions
- [ ] Traceability to architecture exists
- [ ] Verification tests defined
