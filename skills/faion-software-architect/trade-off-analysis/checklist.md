# Trade-off Analysis Checklist

Step-by-step checklist for conducting thorough trade-off analysis at various levels of depth.

## Quick Decision Checklist (30 minutes)

For Type 2 (reversible) decisions and time-sensitive choices.

### Pre-Analysis

- [ ] Define the decision to be made in one sentence
- [ ] Identify decision owner and stakeholders
- [ ] Set decision deadline
- [ ] Classify decision type (Type 1 irreversible / Type 2 reversible)

### Option Generation

- [ ] List at least 3 viable options (including "do nothing")
- [ ] Eliminate clearly infeasible options
- [ ] Ensure options are mutually exclusive

### Quick Evaluation

- [ ] Identify top 3 criteria for this decision
- [ ] Score each option (High/Medium/Low) against criteria
- [ ] Identify biggest risk for each option
- [ ] Check: What do we lose with each option?

### Decision

- [ ] Select option with best fit to criteria
- [ ] Document decision and rationale (brief ADR)
- [ ] Communicate to affected parties
- [ ] Set review checkpoint (if needed)

---

## Standard Trade-off Analysis Checklist (2-4 hours)

For significant technical decisions with moderate impact.

### Phase 1: Context Establishment (20 min)

- [ ] **Document the problem statement**
  - What problem are we solving?
  - What triggered this decision?
  - What happens if we don't decide?

- [ ] **Identify stakeholders**
  - Who is affected by this decision?
  - Who has input authority?
  - Who has decision authority?

- [ ] **Gather constraints**
  - Budget constraints
  - Timeline constraints
  - Technical constraints
  - Regulatory/compliance constraints
  - Team capability constraints

- [ ] **Define success criteria**
  - How will we know this was a good decision?
  - What metrics matter?

### Phase 2: Option Discovery (30 min)

- [ ] **Brainstorm options**
  - Include obvious solutions
  - Include "do nothing" option
  - Include contrarian options
  - Consider hybrid approaches

- [ ] **Research each option**
  - Industry adoption
  - Vendor stability (if applicable)
  - Community/ecosystem health
  - Integration with existing systems

- [ ] **Initial feasibility check**
  - Technical feasibility
  - Resource feasibility
  - Timeline feasibility

- [ ] **Shortlist options** (aim for 3-5)

### Phase 3: Criteria Definition (20 min)

- [ ] **List quality attributes relevant to decision**
  - Performance (latency, throughput)
  - Scalability (horizontal, vertical)
  - Availability (uptime, recovery)
  - Security (confidentiality, integrity)
  - Maintainability (modifiability, testability)
  - Cost (initial, operational, total)

- [ ] **Add business criteria**
  - Time to market
  - Team expertise/learning curve
  - Vendor relationship
  - Strategic alignment

- [ ] **Assign weights to criteria**
  - Use 1-5 or 1-10 scale
  - Validate weights with stakeholders
  - Document rationale for weights

### Phase 4: Option Evaluation (45 min)

- [ ] **Score each option against each criterion**
  - Use consistent scale (1-5 recommended)
  - Document scoring rationale
  - Flag uncertain scores for discussion

- [ ] **Calculate weighted scores**
  - Weighted score = Raw score x Weight
  - Sum weighted scores for each option

- [ ] **Identify sensitivity points**
  - Which criteria most influence the outcome?
  - What if weights changed?

- [ ] **Create decision matrix**
  - Options as columns
  - Criteria as rows
  - Include weights and scores

### Phase 5: Trade-off Identification (30 min)

- [ ] **For each option, document:**
  - What we gain (benefits)
  - What we lose (sacrifices)
  - What risks we accept
  - What risks we avoid

- [ ] **Identify trade-off points**
  - Where does improving one criterion hurt another?
  - Which trade-offs are acceptable?
  - Which are deal-breakers?

- [ ] **Consider second-order effects**
  - Impact on adjacent systems
  - Impact on team dynamics
  - Impact on future decisions

### Phase 6: Risk Analysis (20 min)

- [ ] **For recommended option, identify risks:**
  - Technical risks
  - Operational risks
  - Business risks
  - Integration risks

- [ ] **Assess each risk:**
  - Probability (High/Medium/Low)
  - Impact (High/Medium/Low)
  - Risk score = Probability x Impact

- [ ] **Define mitigations:**
  - Mitigation strategy for high risks
  - Contingency plans
  - Risk monitoring approach

### Phase 7: Decision and Documentation (15 min)

- [ ] **Make recommendation**
  - State recommended option
  - Summarize key trade-offs accepted
  - List conditions/assumptions

- [ ] **Document in ADR**
  - Context and problem
  - Options considered
  - Decision and rationale
  - Trade-offs accepted
  - Consequences

- [ ] **Plan communication**
  - Who needs to know?
  - What format (meeting, doc, email)?
  - When to communicate?

---

## ATAM-style Deep Analysis Checklist (1-3 days)

For Type 1 (irreversible) decisions with significant business impact.

### Phase 0: Preparation (Before ATAM Session)

- [ ] **Identify evaluation team**
  - Lead evaluator
  - Technical recorder
  - Business analyst
  - External perspective (optional)

- [ ] **Gather documentation**
  - Business requirements
  - Current architecture (if exists)
  - Quality attribute requirements
  - Constraints documentation

- [ ] **Schedule participants**
  - Architects
  - Key developers
  - Product owner
  - Operations representative
  - Business stakeholders

- [ ] **Prepare materials**
  - Architecture presentation
  - Business drivers summary
  - Scenario templates

### Phase 1: Partnership and Preparation (Day 1 Morning)

- [ ] **Present ATAM method** to stakeholders
  - Purpose and outputs
  - Expected participation
  - Timeline

- [ ] **Present business drivers**
  - Business context
  - Key business goals
  - Major constraints
  - Quality attribute priorities

### Phase 2: Architecture Presentation (Day 1 Afternoon)

- [ ] **Present architecture** at appropriate level
  - High-level overview
  - Key architectural decisions
  - Technology choices
  - Integration points

- [ ] **Identify architectural approaches**
  - List approaches used
  - Map approaches to quality attributes
  - Note where approaches conflict

### Phase 3: Utility Tree Development (Day 2 Morning)

- [ ] **Build utility tree**
  ```
  Utility
  ├── Performance
  │   ├── Latency < 200ms for 95th percentile (H,H)
  │   └── Handle 10K concurrent users (M,H)
  ├── Availability
  │   ├── 99.9% uptime (H,H)
  │   └── Recovery < 15 minutes (M,M)
  └── Security
      └── Zero data breaches (H,H)
  ```

- [ ] **Prioritize scenarios**
  - Rate importance (H/M/L)
  - Rate difficulty (H/M/L)
  - Focus on (H,H) scenarios

- [ ] **Refine scenarios**
  - Make scenarios testable
  - Add stimulus and response measures
  - Validate with stakeholders

### Phase 4: Architectural Analysis (Day 2 Afternoon - Day 3)

- [ ] **Analyze each high-priority scenario**
  - How does architecture support this?
  - What architectural decisions affect this?
  - What are the risks?

- [ ] **Identify sensitivity points**
  - Components/decisions affecting single quality attribute
  - Document why they're sensitive

- [ ] **Identify trade-off points**
  - Components/decisions affecting multiple quality attributes
  - Document the trade-off relationship
  - Example: "Caching improves performance but complicates consistency"

- [ ] **Catalog risks**
  - Decisions that could prove problematic
  - Missing information
  - Unresolved conflicts

- [ ] **Catalog non-risks**
  - Decisions that appear sound
  - Well-supported architectural approaches

### Phase 5: Brainstorming and Scenario Prioritization (Day 3)

- [ ] **Brainstorm additional scenarios** with stakeholders
  - Growth scenarios
  - Failure scenarios
  - Change scenarios
  - Exploratory scenarios

- [ ] **Prioritize through voting**
  - Each stakeholder gets votes
  - Consolidate similar scenarios
  - Identify top scenarios for analysis

- [ ] **Analyze additional high-priority scenarios**
  - Same analysis as Phase 4
  - Focus on scenarios that reveal new insights

### Phase 6: Results Presentation

- [ ] **Compile findings**
  - Sensitivity points list
  - Trade-off points list
  - Risks and risk themes
  - Non-risks

- [ ] **Present to stakeholders**
  - Architecture strengths
  - Identified risks and trade-offs
  - Recommendations

- [ ] **Document outcomes**
  - Full ATAM report
  - Executive summary
  - Action items

---

## Build vs Buy Analysis Checklist

Specialized checklist for build vs buy decisions.

### Strategic Assessment

- [ ] **Core vs Context**
  - Is this core to competitive advantage?
  - Is this a differentiating capability?
  - Would custom solution create IP value?

- [ ] **Market analysis**
  - Are there mature solutions available?
  - How many viable vendors?
  - What's the vendor landscape trend?

### Build Evaluation

- [ ] **Capability assessment**
  - Do we have required expertise?
  - Can we hire/develop expertise?
  - What's the learning curve?

- [ ] **Cost estimation**
  - Development cost (be realistic)
  - Maintenance cost (typically 15-20% annually)
  - Infrastructure cost
  - Opportunity cost

- [ ] **Timeline**
  - Time to MVP
  - Time to feature parity with buy option
  - Can we meet business deadlines?

- [ ] **Risk assessment**
  - Technical risk (can we build it?)
  - Schedule risk (will it take longer?)
  - Quality risk (will it work well?)

### Buy Evaluation

- [ ] **Vendor assessment**
  - Financial stability
  - Market position
  - Product roadmap alignment
  - Support quality

- [ ] **Fit analysis**
  - Feature fit (% of requirements met)
  - Gap analysis (missing features)
  - Customization options
  - Integration complexity

- [ ] **Cost analysis**
  - License/subscription cost (3-year TCO)
  - Implementation cost
  - Integration cost
  - Training cost
  - Customization cost

- [ ] **Risk assessment**
  - Vendor lock-in risk
  - Contract/pricing risk
  - Dependency risk
  - Data portability

### Hybrid Consideration

- [ ] **Identify hybrid options**
  - Buy core, build extensions
  - Build core, integrate bought components
  - Open source + custom development

- [ ] **Evaluate integration complexity**

### Decision Framework

- [ ] **Score comparison**

| Factor | Weight | Build | Buy |
|--------|--------|-------|-----|
| Strategic fit | | | |
| Time to value | | | |
| Total cost (3-yr) | | | |
| Risk level | | | |
| Flexibility | | | |

- [ ] **Make recommendation with exit strategy**

---

## Technical Debt Trade-off Checklist

For decisions involving speed vs quality trade-offs.

### Debt Classification

- [ ] **Classify the debt type**
  - Deliberate prudent ("ship now, fix later")
  - Deliberate reckless ("no time for design")
  - Inadvertent prudent ("now we know better")
  - Inadvertent reckless ("what's layering?")

- [ ] **Assess debt location**
  - Code debt
  - Architectural debt
  - Test debt
  - Documentation debt
  - Infrastructure debt

### Impact Assessment

- [ ] **Quantify current impact**
  - Developer time spent on workarounds
  - Bug frequency in affected area
  - Deployment friction

- [ ] **Project future impact**
  - Will this area change frequently?
  - Is this blocking other work?
  - Does this affect customer experience?

### Decision Criteria

- [ ] **Time pressure evaluation**
  - Is the deadline real?
  - What's the cost of missing deadline?
  - Can scope be reduced instead?

- [ ] **Debt budget check**
  - Are we within 15-20% debt allocation?
  - Is existing debt manageable?

### If Taking Debt

- [ ] **Document the debt**
  - What shortcut was taken
  - Why it was necessary
  - Planned remediation approach
  - Trigger for paying off debt

- [ ] **Set repayment timeline**
  - Specific sprint/quarter
  - Trigger conditions

- [ ] **Add to debt registry**

### If Paying Off Debt

- [ ] **Prioritize by impact**
  - Business impact
  - Developer productivity impact
  - Risk if left unpaid

- [ ] **Estimate effort accurately**
- [ ] **Plan incremental payoff** (Boy Scout Rule)

---

## Post-Decision Review Checklist

For reviewing trade-off decisions after implementation.

- [ ] **Collect outcome data**
  - Did we achieve expected benefits?
  - Did predicted risks materialize?
  - Were there unexpected consequences?

- [ ] **Validate trade-offs**
  - Were trade-offs as expected?
  - Any trade-offs we didn't anticipate?

- [ ] **Document lessons learned**
  - What would we do differently?
  - What worked well?

- [ ] **Update decision records**
  - Mark decision status
  - Add outcome notes
  - Link to follow-up decisions

- [ ] **Share learnings**
  - Team retrospective
  - Knowledge base update
