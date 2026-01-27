# Specification Checklist

Quality gates for specification review. Use before moving to design phase.

---

## Pre-Writing Checklist

Before writing a spec, ensure you have:

- [ ] Read `constitution.md` for project constraints
- [ ] Reviewed related features in `done/` for patterns
- [ ] Identified all stakeholders and personas
- [ ] Understood the business context and goals
- [ ] Gathered any existing research or user feedback

---

## Completeness Checklist

### Problem Definition

- [ ] Problem statement clearly identifies WHO has the problem
- [ ] Problem statement explains WHAT they cannot do
- [ ] Business impact is quantified or described
- [ ] Success metric is defined and measurable

### User Context

- [ ] At least one user persona defined
- [ ] Personas include goals and pain points
- [ ] User context (when/where/how they use product) documented

### Requirements

- [ ] All functional requirements have unique IDs (FR-XXX)
- [ ] All requirements meet SMART criteria
- [ ] All requirements trace to user stories
- [ ] MoSCoW priorities assigned to all requirements
- [ ] Non-functional requirements cover:
  - [ ] Performance (response times, throughput)
  - [ ] Security (auth, encryption, compliance)
  - [ ] Scalability (concurrent users, data volume)

### Acceptance Criteria

- [ ] All requirements have acceptance criteria
- [ ] Acceptance criteria use Given-When-Then format
- [ ] Specific values used (not "valid input" but "test@example.com")
- [ ] Coverage includes:
  - [ ] Happy path (main success)
  - [ ] Error handling (validation failures)
  - [ ] Boundary conditions (min/max/empty)
  - [ ] Security scenarios (if applicable)

### Scope

- [ ] In-scope items explicitly listed
- [ ] Out-of-scope items explicitly listed with reasoning
- [ ] "Won't" items have timeline (Phase 2, Never, etc.)

### Dependencies

- [ ] Internal dependencies identified (other features)
- [ ] External dependencies identified (services, APIs)
- [ ] Assumptions documented
- [ ] Constraints documented

---

## Clarity Checklist

### Unambiguous Language

- [ ] No "should be fast" (use "< 500ms p95")
- [ ] No "handle gracefully" (specify exact behavior)
- [ ] No "support many users" (specify number)
- [ ] No "good UX" (specify measurable criteria)
- [ ] No "secure" without specifics (specify mechanism)
- [ ] No "easy to use" (specify steps/clicks)

### Testable Statements

- [ ] Every requirement can be verified pass/fail
- [ ] Acceptance criteria have concrete expected values
- [ ] No subjective judgments ("looks good", "feels right")

### Technical Precision

- [ ] Technical terms defined or linked to glossary
- [ ] Code patterns shown as actual code, not prose
- [ ] File paths use exact project structure
- [ ] Commands include all necessary flags

---

## LLM-Readiness Checklist

### Context Optimization

- [ ] Spec fits within reasonable context window (~50k tokens max)
- [ ] Information density is high (tables > paragraphs)
- [ ] No redundant information across sections
- [ ] External files referenced, not inlined entirely

### Boundaries Defined

- [ ] "Always do" actions listed (safe defaults)
- [ ] "Ask first" actions listed (high-impact changes)
- [ ] "Never do" actions listed (hard stops)

### Execution Readiness

- [ ] Test commands specified with exact syntax
- [ ] Project structure documented with paths
- [ ] Code style shown through examples
- [ ] Git workflow defined (branch naming, commit format)

---

## Consistency Checklist

### Identifiers

- [ ] Requirement IDs are unique across project
- [ ] No gaps in ID sequences
- [ ] IDs follow project convention (FR-XXX, AC-XXX)

### Traceability

- [ ] User Stories trace to personas
- [ ] Requirements trace to user stories
- [ ] Acceptance criteria trace to requirements
- [ ] Complete traceability matrix (optional for simple features)

### Cross-References

- [ ] Related features identified
- [ ] Dependencies bidirectionally linked
- [ ] Constitution constraints referenced

---

## Review Checklist

Before approval, the spec should be reviewed for:

### Stakeholder Alignment

- [ ] Key stakeholders have reviewed
- [ ] No conflicting interpretations
- [ ] Questions and concerns addressed

### Technical Feasibility

- [ ] Engineering has validated feasibility
- [ ] No impossible or unrealistic requirements
- [ ] Dependencies are available or planned

### Business Value

- [ ] Feature aligns with product roadmap
- [ ] ROI or value proposition is clear
- [ ] Priority is appropriate given resources

---

## Quick Quality Score

Rate your spec 1-5 on each dimension:

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | /5 | All sections filled? |
| Clarity | /5 | Unambiguous language? |
| Testability | /5 | All criteria verifiable? |
| LLM-Ready | /5 | Agent can execute? |
| Consistency | /5 | IDs and traces correct? |
| **Total** | **/25** | |

**Scoring:**
- 20-25: Ready for design phase
- 15-19: Minor revisions needed
- 10-14: Significant gaps to address
- <10: Requires major rework

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "System should be fast" | Specify: "Response time < 500ms p95" |
| No user personas | Define at least 2 personas with context |
| User stories without "so that" | Always include the benefit |
| Requirements without IDs | Use FR-XXX, NFR-XXX format |
| No traceability | Every FR must trace to a US |
| AC not testable | Use Given-When-Then with specific values |
| Missing out-of-scope | Explicitly list what you're NOT building |
| No related features | Check done/ for patterns to follow |
| Ambiguous boundaries | Define Always/Ask First/Never actions |
| Context dump | Summarize; reference files don't inline |

---

*Specification Checklist | v1.0.0*
