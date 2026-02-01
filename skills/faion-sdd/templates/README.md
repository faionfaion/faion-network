# SDD Document Templates

Copy-paste ready templates for Specification-Driven Development. Optimized for LLM-assisted workflows (Claude Code, Cursor, Codex).

---

## Template Overview

| Template | Purpose | When to Use |
|----------|---------|-------------|
| [constitution.md](constitution.md) | Project standards, tech stack, constraints | Project setup, once per project |
| [spec.md](spec.md) | Feature specification (WHAT) | Before design, for each feature |
| [design.md](design.md) | Technical design (HOW) | After spec approval |
| [implementation-plan.md](implementation-plan.md) | Task breakdown, dependencies | After design approval |
| [task.md](task.md) | Single executable task | During implementation |
| [roadmap.md](roadmap.md) | Feature timeline, metrics | Project planning |
| [memory.md](memory.md) | Patterns, mistakes, decisions | Continuous learning |

---

## Document Lifecycle

```
constitution.md (once)
        |
        v
    spec.md  -->  design.md  -->  implementation-plan.md  -->  task.md (N)
        |             |                    |                       |
    "What to      "How to           "What tasks,             "Execute
     build"        build"            what order"              this now"
```

---

## Template Selection Guide

### Starting a New Project

1. **Create `constitution.md`** - Define tech stack, standards, principles
2. **Create `roadmap.md`** - Outline phases and success metrics

### Adding a Feature

1. **Create `spec.md`** - Define requirements, user stories, acceptance criteria
2. **Create `design.md`** - Architecture decisions, data models, APIs
3. **Create `implementation-plan.md`** - Break into tasks, identify dependencies
4. **Create `task.md` files** - One per task, ready for execution

### Learning from Execution

1. **Update `memory.md`** - Record patterns and mistakes after each task

---

## LLM Optimization Tips

### Context Efficiency

- **YAML frontmatter**: Machine-readable metadata at the top
- **Structured tables**: Easy to parse, low token overhead
- **Cross-references**: Link to related docs, avoid duplication
- **Clear sections**: Use `---` separators for easy navigation

### Token Budget

| Document | Typical Size | Read by Agent |
|----------|--------------|---------------|
| constitution.md | 2-5k tokens | Always (context) |
| spec.md | 3-8k tokens | During design |
| design.md | 5-15k tokens | During task creation |
| implementation-plan.md | 3-10k tokens | During execution |
| task.md | 2-5k tokens | Per task execution |

**100k Token Rule**: Each task should complete within 100k context:
- Research: ~20k (reading existing code)
- Task file: ~5k
- Implementation: ~50k
- Buffer: ~25k

### Traceability

Every document links to its predecessors:
```
Task -> Implementation Plan -> Design -> Spec -> Constitution
```

This enables:
- **Validation**: Check if implementation matches spec
- **Debugging**: Trace bugs back to requirements
- **Refactoring**: Understand original intent

---

## Template Customization

### Removing Sections

If a section doesn't apply to your project, remove it entirely rather than leaving placeholders. LLMs work better with concise documents.

### Adding Sections

Add project-specific sections as needed:
- **Regulatory**: For compliance-heavy projects (HIPAA, GDPR, SOC2)
- **Multi-tenant**: For SaaS architecture considerations
- **Legacy**: For migration/integration with existing systems

### Frontmatter Fields

All templates use YAML frontmatter. Common fields:
```yaml
---
version: "1.0"
status: draft | review | approved
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: Name
---
```

---

## Best Practices

### For Humans

1. **Review before approving** - Specs and designs need human validation
2. **Keep it updated** - Outdated docs are worse than no docs
3. **Focus on "why"** - Code shows "what", docs explain "why"

### For LLMs

1. **Be explicit** - State assumptions, don't leave things implied
2. **Use examples** - Concrete examples > abstract descriptions
3. **Define vocabulary** - Clarify domain-specific terms
4. **Specify constraints** - What NOT to do is as important as what to do

### For Teams

1. **Version control** - All docs in git, alongside code
2. **Single source** - One roadmap, one backlog, no duplicates
3. **Atomic features** - Each feature folder is self-contained

---

## File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature folder | `feature-{NNN}-{slug}/` | `feature-024-starter-kits/` |
| Standalone task | `TASK-{NNNN}-{slug}.md` | `TASK-0042-add-auth.md` |
| Feature task | `TASK-{PREFIX}-{NNN}.md` | `TASK-SK-001.md` |

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Writing specification templates | haiku | Form completion, mechanical setup |
| Reviewing specifications for clarity | sonnet | Language analysis, logical consistency |
| Architecting complex system specs | opus | Holistic design, novel combinations |
## Related

- [SDD Workflow Overview](../faion-sdd-planning/methodologies/sdd-workflow-overview.md)
- [Writing Specifications](../faion-sdd-planning/methodologies/writing-specifications.md)
- [Writing Design Documents](../faion-sdd-planning/methodologies/writing-design-documents.md)
- [Writing Implementation Plans](../faion-sdd-planning/methodologies/writing-implementation-plans.md)
- [Task Creation & Parallelization](../faion-sdd-planning/methodologies/task-creation-parallelization.md)

---

*SDD Templates v3.0*
*Optimized for LLM-assisted development*
