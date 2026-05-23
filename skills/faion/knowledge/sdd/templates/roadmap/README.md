# Roadmap Template

Project timeline, features, and success metrics. Copy and customize per project.

---

```markdown
---
version: "1.0"
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
project: {project-name}
---

# Roadmap: {Project Name}

## Vision

{1-2 sentences: where is this project going in 6-12 months}

---

## Strategic Goals

| Goal | Success Metric | Target |
|------|----------------|--------|
| {Goal 1} | {metric} | {target value} |
| {Goal 2} | {metric} | {target value} |
| {Goal 3} | {metric} | {target value} |

---

## Now (Current Phase) - High Confidence

Features actively being worked on or immediately planned.

| Feature | Status | Priority | Notes |
|---------|--------|----------|-------|
| feature-{NNN}-{name} | In Progress | P0 | {notes} |
| feature-{NNN}-{name} | Todo | P0 | {notes} |
| feature-{NNN}-{name} | Todo | P1 | {notes} |

**Focus Areas:**
- {Primary focus 1}
- {Primary focus 2}

---

## Next (Upcoming Phase) - Medium Confidence

Features planned for the next cycle. Details may change.

| Feature | Description | Dependencies | Priority |
|---------|-------------|--------------|----------|
| {feature} | {one-liner} | {deps} | P1 |
| {feature} | {one-liner} | {deps} | P2 |

**Exploration Areas:**
- {Area requiring research/validation}

---

## Later (Future) - Lower Confidence

Strategic themes and directions. Specific features TBD.

| Theme | Description | Rationale |
|-------|-------------|-----------|
| {theme} | {high-level goal} | {why important} |
| {theme} | {high-level goal} | {why important} |

---

## Done (Completed)

| Feature | Completed | Highlights | Metrics Impact |
|---------|-----------|------------|----------------|
| feature-{NNN}-{name} | YYYY-MM | {key outcome} | {metric change} |
| feature-{NNN}-{name} | YYYY-MM | {key outcome} | {metric change} |

---

## Milestones

| Milestone | Target | Status | Key Deliverables |
|-----------|--------|--------|------------------|
| {name} | {phase} | Planned/Active/Done | {deliverables} |
| {name} | {phase} | Planned/Active/Done | {deliverables} |

---

## Dependencies

### External

| Dependency | Type | Status | Impact |
|------------|------|--------|--------|
| {service/API} | Integration | {status} | Blocks {features} |
| {technology} | Adoption | {status} | Enables {features} |

### Internal

| Dependency | Type | Status | Impact |
|------------|------|--------|--------|
| {feature} | Prerequisite | {status} | Required for {features} |

---

## Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| {risk} | High/Med/Low | High/Med/Low | {mitigation} | {plan B} |

---

## Resources

### Current Allocation

| Resource | Allocation | Focus |
|----------|------------|-------|
| {role/team} | {%} | {what they're working on} |

### Constraints

- {Resource constraint 1}
- {Resource constraint 2}

---

## Metrics Dashboard

| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| {metric} | {value} | {goal} | {up/down/stable} |
| {metric} | {value} | {goal} | {up/down/stable} |

---

## Release Schedule

| Version | Scope | Target | Status |
|---------|-------|--------|--------|
| v{X.Y} | {features} | {phase} | Planned |
| v{X.Y} | {features} | {phase} | Planned |

---

## Decision Log

| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| YYYY-MM-DD | {what changed} | {why} | {effect on roadmap} |

---

*Roadmap v1.0*
*Last updated: YYYY-MM-DD*
```

---

## Usage Notes

### Now/Next/Later Framework

| Horizon | Confidence | Granularity | Commitment |
|---------|------------|-------------|------------|
| Now | High (90%) | Detailed features | Committed |
| Next | Medium (70%) | Feature outlines | Planned |
| Later | Lower (50%) | Themes/directions | Exploring |

### Avoiding Date Promises

Instead of specific dates, use:
- Phases: "Phase 1", "Q2", "H1 2024"
- Relative: "After feature X", "Next cycle"
- Confidence: "High/Medium/Lower confidence"

This prevents false precision and manages expectations.

### Update Frequency

- **Weekly**: Update "Now" section status
- **Monthly**: Review "Next" section priorities
- **Quarterly**: Reassess "Later" themes

### Roadmap vs Backlog

| Roadmap | Backlog |
|---------|---------|
| Strategic view | Tactical view |
| Phases and themes | Specific tasks |
| "Why" and "When" | "What" and "How" |
| Stakeholder-facing | Team-facing |

### Anti-Patterns

- **Feature factory**: List of features without strategic context
- **Date-driven**: Unrealistic dates that become broken promises
- **Static document**: Never updated, loses relevance
- **Kitchen sink**: Everything listed, nothing prioritized
