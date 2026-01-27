# SDD Trends Adoption Checklist

Step-by-step checklist for adopting modern Specification-Driven Development practices.

**Version:** 1.0

---

## Pre-Adoption Assessment

### Team Readiness

- [ ] Team has basic LLM experience (prompting, context management)
- [ ] At least one champion for SDD adoption identified
- [ ] Management buy-in for process changes
- [ ] Dedicated time allocated for learning curve (first 2-4 weeks)
- [ ] Existing documentation practices assessed

### Infrastructure Readiness

- [ ] Git-based workflow established
- [ ] CI/CD pipeline functional
- [ ] Access to LLM tools (Claude Code, Cursor, Copilot, or similar)
- [ ] Markdown rendering in IDE configured
- [ ] Code review process defined

---

## Phase 1: Foundation (Week 1-2)

### 1.1 Directory Structure

- [ ] Create `.aidocs/` directory in project root
- [ ] Set up standard folder structure:
  ```
  .aidocs/
  ├── constitution.md
  ├── backlog/
  ├── todo/
  ├── in-progress/
  └── done/
  ```
- [ ] Create initial `constitution.md` with tech stack decisions
- [ ] Add `.aidocs/` to repository (not gitignored)

### 1.2 ADR Setup

- [ ] Create `docs/adr/` directory
- [ ] Add ADR template (see templates.md)
- [ ] Write first ADR: "ADR-0001: Adopt Architecture Decision Records"
- [ ] Document 3-5 existing architectural decisions as ADRs
- [ ] Establish ADR review process (who approves, how long)

### 1.3 Documentation Standards

- [ ] Define Markdown style guide (headings, code blocks, tables)
- [ ] Set up documentation linting (markdownlint or similar)
- [ ] Configure IDE for Markdown preview
- [ ] Establish folder naming conventions
- [ ] Create CLAUDE.md / COPILOT.md / CURSOR.md for LLM context

---

## Phase 2: SDD Workflow (Week 3-4)

### 2.1 Specification Process

- [ ] Create spec template (see templates.md)
- [ ] Write first feature specification
- [ ] Establish spec review checklist:
  - [ ] Clear problem statement
  - [ ] User stories with acceptance criteria
  - [ ] Non-functional requirements defined
  - [ ] Out of scope explicitly stated
  - [ ] Success metrics identified

### 2.2 Design Document Process

- [ ] Create design doc template
- [ ] Link design docs to specs (traceability)
- [ ] Establish design review process
- [ ] Include ADR references in design docs
- [ ] Define when design doc is required vs. optional

### 2.3 Implementation Planning

- [ ] Create implementation plan template
- [ ] Define task granularity (100k token rule)
- [ ] Establish dependency tracking
- [ ] Create task file format (TASK-XXX-name.md)
- [ ] Set up task lifecycle: backlog → todo → in-progress → done

---

## Phase 3: LLM Integration (Week 5-6)

### 3.1 Context Engineering

- [ ] Create project-specific CLAUDE.md (or equivalent)
- [ ] Document coding standards for LLM consumption
- [ ] List key patterns and anti-patterns
- [ ] Include example code snippets
- [ ] Add decision history references

### 3.2 Workflow Integration

- [ ] Configure LLM tool with project context
- [ ] Establish prompt templates for common tasks:
  - [ ] Spec writing assistance
  - [ ] Design review prompts
  - [ ] Code generation from specs
  - [ ] Test generation prompts
- [ ] Set up human review gates

### 3.3 Quality Gates

- [ ] Define L1-L6 quality gates:
  - [ ] L1: Spec complete
  - [ ] L2: Design approved
  - [ ] L3: Plan reviewed
  - [ ] L4: Code implemented
  - [ ] L5: Tests passing
  - [ ] L6: Documentation updated
- [ ] Create gate checklists
- [ ] Establish confidence thresholds (90%+ to proceed)

---

## Phase 4: Platform Engineering (Week 7-8)

### 4.1 Developer Portal Setup

- [ ] Evaluate portal options (Backstage, Port, internal)
- [ ] Set up service catalog
- [ ] Configure documentation aggregation
- [ ] Enable API documentation auto-generation
- [ ] Create onboarding golden path

### 4.2 Observability Integration

- [ ] Add OpenTelemetry to services
- [ ] Configure structured logging
- [ ] Set up distributed tracing
- [ ] Create dashboards for key metrics
- [ ] Document runbooks in portal

### 4.3 Self-Service Capabilities

- [ ] Template for new services
- [ ] Automated CI/CD setup
- [ ] Environment provisioning
- [ ] Secret management integration
- [ ] Cost visibility per service

---

## Phase 5: Continuous Improvement (Ongoing)

### 5.1 Metrics Tracking

- [ ] Track specification quality metrics:
  - [ ] Spec-to-implementation time
  - [ ] Rework percentage
  - [ ] Spec completeness score
- [ ] Monitor LLM effectiveness:
  - [ ] Generation acceptance rate
  - [ ] Review iteration count
  - [ ] Test coverage of generated code
- [ ] Platform metrics:
  - [ ] Time to first commit (new joiners)
  - [ ] Deployment frequency
  - [ ] Lead time for changes

### 5.2 Pattern Library

- [ ] Document successful patterns
- [ ] Create reusable spec templates
- [ ] Build prompt library
- [ ] Share ADR patterns across teams
- [ ] Establish code generation patterns

### 5.3 Retrospectives

- [ ] Monthly SDD process review
- [ ] Quarterly tooling assessment
- [ ] Annual strategy alignment
- [ ] Collect and act on developer feedback
- [ ] Update CLAUDE.md based on learnings

---

## Quick Start Checklist

Minimal viable SDD setup (can be done in 1 day):

- [ ] Create `.aidocs/constitution.md` with tech stack
- [ ] Create `docs/adr/` with template
- [ ] Write one ADR for current architecture choice
- [ ] Create `CLAUDE.md` with project context
- [ ] Write one spec for next feature
- [ ] Establish human review gate before LLM execution

---

## Validation Checklist

Use this to verify SDD adoption is working:

### Signs of Success

- [ ] Specs are written before code
- [ ] ADRs are created for significant decisions
- [ ] LLM-generated code passes review first time >70%
- [ ] Documentation stays up-to-date
- [ ] New team members productive faster
- [ ] Fewer "why did we do this?" questions

### Warning Signs

- [ ] Specs written after code (documentation, not specification)
- [ ] ADRs created but never referenced
- [ ] LLM outputs require heavy rewriting
- [ ] Documentation diverges from code
- [ ] Tribal knowledge still dominates
- [ ] Repeated architectural debates

---

## Maturity Levels

### Level 1: Basic

- Specs exist for major features
- ADRs started
- Some LLM assistance used
- Basic documentation in place

### Level 2: Consistent

- All features have specs
- ADRs are standard practice
- LLM integrated into workflow
- Documentation auto-generated where possible
- Quality gates enforced

### Level 3: Optimized

- Specs drive development
- ADRs referenced in code and reviews
- LLM-first for repetitive tasks
- Living documentation fully implemented
- Platform engineering mature

### Level 4: Leading

- AI-assisted spec writing
- Predictive quality analysis
- Self-healing documentation
- Full platform self-service
- Continuous improvement automated

---

## Resources

- [README.md](README.md) - Overview and context
- [examples.md](examples.md) - Real-world examples
- [templates.md](templates.md) - Copy-paste templates
- [llm-prompts.md](llm-prompts.md) - Effective prompts

---

*Checklist Document | SDD Trends Adoption | Version 1.0*
