---
id: ba-requirements-mgmt
name: "BA Requirements Management Methodologies"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
knowledge_area: "KA-3 Lifecycle"
---

# BA Requirements Management Methodologies

Detailed methodologies for requirements maintenance, change impact, and architecture.

---

## 1. Requirements Maintenance

### Problem
How to keep requirements accurate and useful over time?

### Framework

1. **Version Control**
   - Baseline management
   - Change history tracking
   - Branch/merge strategies

2. **Attribute Management**
   - Status (draft, approved, implemented)
   - Priority
   - Owner
   - Source

3. **Quality Monitoring**
   - Periodic reviews
   - Consistency checks
   - Completeness validation

4. **Archival Strategy**
   - When to archive
   - What to retain
   - Access policies

---

## 2. Change Impact Analysis

### Problem
How to assess the impact of proposed requirement changes?

### Framework

1. **Scope Assessment**
   - What requirements are affected?
   - What designs are affected?
   - What tests are affected?

2. **Effort Assessment**
   - Development effort
   - Testing effort
   - Documentation updates

3. **Risk Assessment**
   - Technical risks
   - Schedule risks
   - Quality risks

4. **Stakeholder Impact**
   - Who is affected?
   - Training needs
   - Communication needs

5. **Decision Support**
   - Options analysis
   - Recommendation
   - Trade-offs

### Template

```markdown
## Change Impact Analysis

### Change Request: {CR-ID}
**Description:** {change description}

### Impact Assessment
| Area | Impact | Effort |
|------|--------|--------|
| Requirements | {count} reqs affected | {hours} |
| Design | {components} | {hours} |
| Code | {modules} | {hours} |
| Tests | {test cases} | {hours} |
| **Total** | | **{total hours}** |

### Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {risk} | H/M/L | H/M/L | {action} |

### Recommendation
{Accept/Reject/Defer} because {rationale}
```

---

## 3. Requirements Architecture

### Problem
How to organize requirements into a coherent structure?

### Framework

1. **Viewpoints**
   - Business perspective
   - User perspective
   - Technical perspective
   - Operational perspective

2. **Decomposition**
   - Hierarchical breakdown
   - Parent-child relationships
   - Abstraction levels

3. **Dependencies**
   - Prerequisite relationships
   - Conflict identification
   - Synergy identification

4. **Completeness Check**
   - Coverage analysis
   - Gap identification
   - Consistency validation

### Template

```markdown
## Requirements Architecture

### Viewpoints
| Viewpoint | Stakeholders | Key Concerns |
|-----------|--------------|--------------|
| Business | Sponsor, Execs | ROI, Strategy |
| User | End users | Usability, Features |
| Technical | Developers | Feasibility, Architecture |

### Requirement Hierarchy
- BR-001: Business Requirement
  - SR-001: Stakeholder Requirement
    - FR-001: Functional Requirement
    - FR-002: Functional Requirement
  - SR-002: Stakeholder Requirement
    - FR-003: Functional Requirement

### Dependencies
| Requirement | Depends On | Enables |
|-------------|------------|---------|
| FR-001 | - | FR-003, FR-004 |
| FR-002 | FR-001 | FR-005 |
```

---

*BA Requirements Management Methodologies*
*Knowledge Area: KA-3 Lifecycle*
