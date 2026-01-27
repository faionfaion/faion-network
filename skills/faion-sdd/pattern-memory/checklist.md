# Pattern Capture Checklist

## When to Capture

Use this checklist to decide whether a solution should become a pattern.

### Pre-Capture Validation

- [ ] Solution worked successfully in the current task
- [ ] Solution addresses a recurring problem (seen 2+ times)
- [ ] Solution includes non-obvious insight or approach
- [ ] Solution is generalizable beyond current context
- [ ] Solution is not a well-known best practice

### Do NOT Capture If

- [ ] It's a one-off fix specific to this codebase
- [ ] It's already documented in framework docs
- [ ] It's a trivial implementation
- [ ] It's a project-specific configuration
- [ ] It only works in very narrow conditions

## Capture Process

### Step 1: Identify Pattern Components

- [ ] **Problem**: What issue does this solve?
- [ ] **Context**: When/where does this problem occur?
- [ ] **Solution**: What is the approach?
- [ ] **Trade-offs**: What are the downsides?
- [ ] **Evidence**: Which task demonstrated this?

### Step 2: Check for Duplicates

- [ ] Search existing patterns for similar solutions
- [ ] If similar exists: merge or link, don't duplicate
- [ ] If variant: note the difference in metadata

### Step 3: Categorize

- [ ] Select primary category: `code` | `architecture` | `workflow`
- [ ] Select subcategory (see categories below)
- [ ] Add 3-5 relevant tags
- [ ] Note language/framework if applicable

### Step 4: Document

- [ ] Write clear problem statement
- [ ] Document solution approach (steps)
- [ ] Include minimal working code example
- [ ] List when to use (contexts)
- [ ] List when NOT to use (anti-contexts)
- [ ] Note related patterns if any

### Step 5: Initial Scoring

- [ ] Set confidence to 0.5 (initial)
- [ ] Set usage_count to 1
- [ ] Set success_rate to 1.0
- [ ] Record provenance (task ID)

## Category Reference

### Code Patterns

| Subcategory | Examples |
|-------------|----------|
| error-handling | Try-catch patterns, fallbacks, retries |
| data-management | State patterns, caching, transforms |
| api-design | Endpoints, responses, versioning |
| testing | Unit tests, mocks, test data |
| validation | Input validation, schema validation |
| async | Promises, async/await, concurrency |

### Architecture Patterns

| Subcategory | Examples |
|-------------|----------|
| structural | Component org, modules, layers |
| behavioral | Events, pub-sub, commands |
| integration | API integration, service comms |
| data-flow | State management, data pipelines |
| security | Auth patterns, access control |

### Workflow Patterns

| Subcategory | Examples |
|-------------|----------|
| planning | Decomposition, estimation, risk |
| execution | Implementation order, debugging |
| review | Code review, quality gates |
| collaboration | PR workflow, documentation |

## Post-Capture Validation

### After First Reuse

- [ ] Pattern worked in new context
- [ ] Update confidence: +0.10
- [ ] Update usage_count: +1
- [ ] Add new task to verified_in list

### After Three Reuses

- [ ] Review pattern documentation for clarity
- [ ] Update trade-offs based on experience
- [ ] Consider syncing to CLAUDE.md (if confidence >= 0.7)

### After Five Reuses

- [ ] Mark as "established" (confidence 0.8+)
- [ ] Ensure pattern is in CLAUDE.md
- [ ] Add comprehensive code examples
- [ ] Document edge cases encountered

## Maintenance Checklist

### Monthly Review

- [ ] Archive patterns unused for 90+ days
- [ ] Merge duplicate/overlapping patterns
- [ ] Update confidence scores based on recent usage
- [ ] Review failed applications (mistakes.md)
- [ ] Sync high-confidence patterns to CLAUDE.md

### Quarterly Review

- [ ] Gap analysis: what patterns are missing?
- [ ] Review pattern categories for completeness
- [ ] Update related pattern links
- [ ] Retire obsolete patterns (tech changes)

## Quick Capture Format

When in a hurry, capture minimal info:

```markdown
## NEW PATTERN: [Name]

**Category:** [code|architecture|workflow]/[subcategory]
**Problem:** [One sentence]
**Solution:** [One sentence]
**Task:** TASK_XXX
**Confidence:** 0.5
```

Expand later during maintenance review.
