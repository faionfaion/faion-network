# Advanced Specification Guidelines

## Overview

Guidelines for writing comprehensive specifications for complex, mission-critical features. Learn when to write full specs, what to include, and best practices for each section.

---

## When to Use Full Specifications

### Appropriate For

- Complex features with multiple user types
- Features with significant NFRs (performance, security, scalability)
- Features with dependencies on other systems
- Mission-critical features affecting business metrics
- Features requiring team alignment across roles

### Not Appropriate For

- Simple CRUD operations (use minimal spec)
- Trivial UI changes (use basic spec)
- Internal refactoring (use design doc)
- Experimental features (use lightweight spec)

---

## What to Include

### Full Specification Sections

**All sections (14 total):**

1. **Overview** - 2-3 sentence summary
2. **Problem Statement** - Who, Problem, Impact, Solution, Success Metric
3. **User Personas** (2-3) - Roles, goals, pain points, context
4. **User Stories** (4-10) - As a/I want to/So that, with priorities
5. **Functional Requirements** (detailed) - SHALL statements with traceability
6. **Non-Functional Requirements** - Performance, scalability, security, usability
7. **Acceptance Criteria** (comprehensive) - Given/When/Then scenarios
8. **Out of Scope** - What's NOT included and why
9. **Assumptions & Constraints** - What we're assuming, what limits us
10. **Dependencies** - Internal and external dependencies
11. **Related Features** - Features that depend on or are blocked by this
12. **Recommended Skills/Methodologies** - Which skills to use
13. **Open Questions** - Unresolved decisions
14. **Appendix** - Wireframes, data models, mockups

---

## Token Estimation

| Section | Approx Tokens |
|---------|---------------|
| Overview + Problem | 200-300 |
| Personas (2) | 300-400 |
| User Stories (4-10) | 600-1000 |
| Functional Req (10-20) | 800-1200 |
| NFRs (5-10) | 500-800 |
| Acceptance Criteria (6+) | 1000-1500 |
| Dependencies + Related | 300-400 |
| Appendix | 400-600 |
| **Total** | **4100-6200** |

---

## Best Practices by Section

### 1. Use Personas Effectively

**Link user stories to specific personas:**

```
✅ "As a busy parent (Sarah)"
✅ Include realistic context (mobile vs desktop)
✅ Reference personas in acceptance criteria
```

**Bad example:**
```
❌ "As a user"
❌ Generic personas without context
```

### 2. Comprehensive Acceptance Criteria Coverage

**Cover all scenarios:**

```
✅ Happy path (normal flow)
✅ Error cases (validation failures, network errors)
✅ Edge cases (boundary conditions, empty states)
✅ Performance scenarios (large data sets)
✅ Security scenarios (unauthorized access, tampering)
✅ Accessibility scenarios (keyboard nav, screen readers)
```

**Example coverage checklist:**
- [x] Happy path
- [x] Error handling
- [x] Boundary conditions
- [x] Persistence
- [ ] Security scenarios
- [ ] Performance scenarios

### 3. Detailed Non-Functional Requirements

**Make NFRs measurable:**

```
✅ Quantifiable targets (< 200ms p95, 99.9% uptime)
✅ Measurement approach (how to measure)
✅ Validation method (how to test)
✅ Priority (Must/Should/Could)
```

**Example:**

```markdown
### NFR-001: Add to Cart Performance

**Requirement:** Add to cart operation SHALL complete in < 200ms for p95.
**Measurement:** Client-side total time from click to UI update.
**Priority:** Must
**Validation:** Load test with 50k concurrent users adding items.
```

### 4. Document Assumptions

**Be explicit about what you're assuming:**

```
✅ "Prices can change between add and checkout"
✅ "Guest carts expire after 7 days"
✅ "Users have JavaScript enabled"
```

**Why:** Prevents misunderstandings and helps with testing.

### 5. Track Dependencies

**Map all dependencies:**

```
✅ Internal (other features in the project)
✅ External (third-party services, APIs)
✅ Blocking vs blocked relationships
```

**Example:**

| Feature | Relationship | Status |
|---------|-------------|--------|
| 01-product-catalog | Depends on | Done |
| 02-user-auth | Depends on | Done |
| 04-checkout | Blocks | Todo |

### 6. Define Out of Scope Early

**Prevent scope creep:**

```
✅ List features NOT included
✅ Explain WHY (not MVP, complexity, etc.)
✅ Indicate WHEN (Phase 2, v2.0, never)
```

**Example:**

| Feature | Reason | When |
|---------|--------|------|
| Save for Later | Not MVP | Phase 2 |
| Share Cart (URL) | Complexity | Phase 3 |
| Cart Price Alerts | External dependency | Not planned |

### 7. Use Traceability

**Link requirements to user stories:**

```
✅ FR-001 traces to US-001
✅ AC-001 validates FR-001
✅ NFR-001 supports FR-001
```

**Why:** Ensures every requirement serves a user need.

---

## Writing Tips

### Problem Statement Template

```markdown
**Who:** [Target user group]
**Problem:** [What problem they face]
**Impact:** [Business/user impact]
**Solution:** [High-level solution]
**Success Metric:** [How to measure success]
```

### User Story Template

```markdown
**As a** [persona]
**I want to** [action]
**So that** [benefit]

**Priority:** Must/Should/Could
**Estimate:** [story points]
**Acceptance Criteria:** [AC IDs]
```

### Acceptance Criteria Template

```markdown
**Scenario:** [Short description]

**Given:** [Initial state]
**And:** [Additional context]
**When:** [User action]
**Then:** [Expected result]
**And:** [Additional outcomes]
```

---

## Quality Checklist

Before finalizing a full specification, verify:

- [ ] All sections present (14 total)
- [ ] Personas referenced in user stories
- [ ] User stories trace to acceptance criteria
- [ ] Functional requirements trace to user stories
- [ ] NFRs have quantifiable targets
- [ ] Acceptance criteria cover happy path + errors + edge cases
- [ ] Dependencies mapped (internal + external)
- [ ] Out of scope defined with reasons
- [ ] Assumptions documented
- [ ] Open questions listed
- [ ] Appendix has wireframes/data models (if applicable)

---

## Common Mistakes

### 1. Too Generic

**Bad:**
```
❌ "As a user, I want to use the cart"
```

**Good:**
```
✅ "As a busy parent (Sarah), I want to add products to my cart with one click so that I can save items for later checkout"
```

### 2. Unmeasurable NFRs

**Bad:**
```
❌ "System should be fast"
```

**Good:**
```
✅ "Add to cart operation SHALL complete in < 200ms for p95"
```

### 3. Missing Coverage

**Bad:**
```
❌ Only happy path tested
```

**Good:**
```
✅ Happy path + errors + edge cases + security + performance
```

### 4. No Traceability

**Bad:**
```
❌ Requirements exist in isolation
```

**Good:**
```
✅ FR-001 → US-001 → AC-001 chain
```

---

## Example: Full vs Minimal Spec

### When Full Spec is Needed

**Feature:** Shopping cart with persistence, multi-device sync, pricing rules
**Why:** Complex business logic, multiple user types, mission-critical
**Sections:** All 14 sections
**Tokens:** ~5000

### When Minimal Spec is Enough

**Feature:** Add "Share" button to product page
**Why:** Simple UI addition, no business logic
**Sections:** Overview, 1-2 user stories, basic acceptance criteria
**Tokens:** ~500-800

---

## Sources

- [IEEE 29148-2018](https://standards.ieee.org/standard/29148-2018.html) - Requirements engineering standard
- [Writing Effective Use Cases](https://www.amazon.com/Writing-Effective-Cases-Alistair-Cockburn/dp/0201702258) - Alistair Cockburn's guide
- [Impact Mapping](https://www.impactmapping.org/) - Goal-oriented planning
- [User Story Mapping](https://www.jpattonassociates.com/user-story-mapping/) - Jeff Patton's methodology
- [INVEST in Good Stories](https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/) - Bill Wake's criteria
