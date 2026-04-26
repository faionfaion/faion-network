# BA Framework Knowledge Areas (Detailed)

Detailed overview of 6 Business Analysis Knowledge Areas with tasks, outputs, and methodologies.

---

## KA-1: Business Analysis Planning and Monitoring

**Purpose:** Define approach, identify stakeholders, plan governance.

### Tasks

| Task | Description | Key Output |
|------|-------------|------------|
| Plan BA Approach | Define how BA will be performed | BA approach document |
| Plan Stakeholder Engagement | Identify and plan work with stakeholders | Stakeholder engagement approach |
| Plan Governance | Define decision-making for requirements | Governance approach |
| Plan Information Management | Define how BA info stored/accessed | Information management approach |
| Identify Improvements | Assess BA performance, recommend improvements | BA performance improvements |

### Methodologies

- ba-planning
- stakeholder-analysis

### Key Outputs

- BA approach document
- Stakeholder register and map
- Governance framework
- Communication plan

---

## KA-2: Elicitation and Collaboration

**Purpose:** Obtain information from stakeholders and confirm results.

### Tasks

| Task | Description | Key Output |
|------|-------------|------------|
| Prepare for Elicitation | Understand scope, select techniques | Elicitation activity plan |
| Conduct Elicitation | Draw out relevant information | Elicitation results (unconfirmed) |
| Confirm Results | Verify understanding with stakeholders | Elicitation results (confirmed) |
| Communicate BA Info | Ensure shared understanding | BA communication |
| Manage Collaboration | Encourage stakeholders to work together | Updated stakeholder engagement |

### Methodologies

- elicitation-techniques

### Key Techniques

- Interviews
- Workshops
- Document Analysis
- Observation
- Surveys
- Prototyping
- Brainstorming
- Focus Groups

---

## KA-3: Requirements Lifecycle Management

**Purpose:** Manage and maintain requirements throughout solution lifecycle.

### Tasks

| Task | Description | Key Output |
|------|-------------|------------|
| Trace Requirements | Ensure alignment at different levels | Requirements (traced) |
| Maintain Requirements | Keep accurate and consistent | Requirements (maintained) |
| Prioritize Requirements | Rank by importance | Requirements (prioritized) |
| Assess Changes | Evaluate proposed changes | Change assessment |
| Approve Requirements | Obtain agreement and approval | Requirements (approved) |

### Methodologies

- requirements-traceability
- requirements-lifecycle
- requirements-prioritization

### Key Outputs

- Traceability matrix
- Requirements baseline
- Prioritized backlog
- Change impact analysis

---

## KA-4: Strategy Analysis

**Purpose:** Define future state needed to address business needs.

### Tasks

| Task | Description | Key Output |
|------|-------------|------------|
| Analyze Current State | Understand existing environment | Current state description |
| Define Future State | Define goals and objectives | Future state description |
| Assess Risks | Identify uncertainties and impacts | Risk assessment results |
| Define Change Strategy | Develop approach to achieve future state | Change strategy |

### Methodologies

- strategy-analysis

### Key Techniques

- Gap Analysis
- SWOT Analysis
- Business Model Canvas
- Capability Assessment
- Risk Analysis

---

## KA-5: Requirements Analysis and Design Definition

**Purpose:** Structure, specify, model, verify, and validate requirements.

### Tasks

| Task | Description | Key Output |
|------|-------------|------------|
| Specify/Model Requirements | Analyze and refine into requirements | Requirements (specified/modeled) |
| Verify Requirements | Ensure quality standards met | Requirements (verified) |
| Validate Requirements | Ensure alignment with business goals | Requirements (validated) |
| Define Architecture | Ensure requirements support each other | Requirements architecture |
| Define Design Options | Define solution approaches | Design options |
| Analyze Value/Recommend | Assess options, recommend solution | Solution recommendation |

### Methodologies

- use-case-modeling
- user-story-mapping
- data-analysis
- business-process-analysis
- decision-analysis
- interface-analysis
- requirements-validation
- acceptance-criteria
- requirements-documentation

### Key Techniques

- Use Cases
- User Stories
- Process Modeling (BPMN)
- Data Modeling (ERD)
- Decision Tables
- Interface Specifications
- Prototyping

---

## KA-6: Solution Evaluation

**Purpose:** Assess solution performance and value delivered.

### Tasks

| Task | Description | Key Output |
|------|-------------|------------|
| Measure Performance | Define how performance measured | Solution performance measures |
| Analyze Measures | Examine data against expected value | Performance analysis |
| Assess Solution Limitations | Investigate problems and causes | Solution limitations |
| Assess Enterprise Limitations | Investigate enterprise factor impacts | Enterprise limitations |
| Recommend Actions | Identify actions to increase value | Value improvement recommendations |

### Methodologies

- solution-assessment

### Key Outputs

- Performance metrics
- Value realization report
- Improvement recommendations
- Lessons learned

---

## Knowledge Area Relationships

```
KA-1 (Planning)
    ↓ defines approach
KA-2 (Elicitation) → KA-5 (Analysis) → KA-6 (Evaluation)
    ↓ produces              ↓ produces      ↓ assesses
    requirements            solutions       value
    ↓
KA-3 (Lifecycle) manages throughout
    ↑
KA-4 (Strategy) provides context
```

---

## Typical BA Workflow

1. **KA-1:** Plan BA approach, identify stakeholders
2. **KA-4:** Analyze current state, define future state
3. **KA-2:** Elicit requirements from stakeholders
4. **KA-5:** Analyze, model, validate requirements
5. **KA-3:** Trace, prioritize, approve requirements
6. **KA-5:** Define design options, recommend solution
7. **Development:** Solution implemented
8. **KA-6:** Evaluate solution, recommend improvements
9. **KA-3:** Update requirements based on learnings

---

## Underlying Competencies (All Knowledge Areas)

| Category | Competencies |
|----------|--------------|
| **Analytical** | Creative thinking, decision making, systems thinking, problem solving |
| **Behavioral** | Ethics, accountability, trustworthiness, adaptability |
| **Business** | Business acumen, industry knowledge, organization knowledge |
| **Communication** | Verbal, written, listening, non-verbal |
| **Interaction** | Facilitation, leadership, teamwork, negotiation |

---

*BA Knowledge Areas v1.0*
*Based on Business Analysis Framework (BABOK)*

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Gather and analyze requirements | sonnet | Complex reasoning about stakeholder needs |
| Write acceptance criteria for features | sonnet | Requires testing perspective and detail |
| Create process flow diagrams (BPMN) | opus | Architecture and complex modeling decisions |
| Format requirements in templates | haiku | Mechanical formatting and pattern application |
| Validate requirements with stakeholders | sonnet | Needs reasoning and communication planning |
| Perform gap analysis between states | opus | Strategic analysis and trade-off evaluation |

