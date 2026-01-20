# AI-Assisted Specification Writing

Research compilation on using AI for specification writing in Specification-Driven Development.

**Research Date:** 2026-01-19
**Sources:** Thoughtworks, Martin Fowler, AWS Kiro, Microsoft, Red Hat, JetBrains

---

## Metadata

| Field | Value |
|-------|-------|
| **ID** | ai-assisted-specification-writing |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #ai, #specifications, #llm |
| **Domain Skill** | faion-sdd |
| **Year** | 2025-2026 |

---

## Problem

Traditional specification writing is slow, inconsistent, and often neglected. Developers struggle to articulate requirements clearly, leading to:
- Ambiguous requirements causing implementation delays
- Inconsistent spec formats across teams
- Specifications that become outdated immediately
- Bottleneck shifted from implementation to specification

**Key insight from 2025:** "AI can handle much of the implementation, and suddenly the bottleneck has shifted upstream" - specification skills have atrophied.

---

## Framework

### The SDD-AI Workflow (2025)

```
INTENT -> SPEC -> PLAN -> EXECUTION -> REVIEW
   |        |       |         |          |
 human    AI+human  AI      AI agent   human
 input   collab   generate  execute    verify
```

### Core Principles

1. **Specification First** - Expected behaviors, edge cases, and constraints captured upfront
2. **One Source of Truth** - Spec anchors entire project (tests, docs, design trace back)
3. **Built-in Testability** - Spec defines "what done looks like"
4. **Iterative by Design** - Specs evolve with feedback, maintaining traceability

### AI-Assisted Spec Writing Process

| Phase | Human Role | AI Role |
|-------|------------|---------|
| Intent capture | Describe problem, constraints | Structure and clarify |
| Requirement extraction | Validate completeness | Generate from context |
| Edge case identification | Confirm relevance | Enumerate possibilities |
| Acceptance criteria | Approve criteria | Draft testable conditions |
| Format standardization | Choose format | Apply template consistently |

### Supported Formats

- **Natural language** (most common)
- **Structured formats** (YAML, JSON, Markdown)
- **Formal specifications** (OpenAPI, JSON Schema for APIs)
- **BDD format** (Given-When-Then)

---

## Templates

### AI Prompt for Spec Generation

```markdown
Generate a specification for [FEATURE_NAME]:

**Context:**
- Product: [product description]
- Target users: [user personas]
- Constraints: [technical/business constraints]

**Requirements:**
1. Generate functional requirements (FR-X format)
2. Identify edge cases
3. Write acceptance criteria
4. Note dependencies
5. Flag potential risks

**Format:** Use standard spec.md template
```

### Spec Review Checklist (AI-Assisted)

```markdown
## AI Spec Review

- [ ] All functional requirements have acceptance criteria
- [ ] Edge cases identified and documented
- [ ] Dependencies explicitly listed
- [ ] Constraints are testable/measurable
- [ ] Scope is clearly bounded (what's NOT included)
- [ ] User stories follow format: As [user], I want [action], so that [benefit]
```

---

## Best Practices

| Practice | Description |
|----------|-------------|
| **Tight scoping** | Keep specs focused; use multiple specs for different concerns (arch, docs, testing) |
| **Lessons learned file** | Maintain file AI learns from past hiccups |
| **Sprint integration** | Include spec requirements in user stories; schedule spec writing in sprint planning |
| **Iterative refinement** | Start with rough spec, refine through AI dialogue |
| **Human approval gates** | All AI-generated specs require human review before implementation |

---

## Tools (2025-2026)

| Tool | Type | Key Features |
|------|------|--------------|
| **AWS Kiro** | Enterprise IDE | 3-phase: Specify -> Plan -> Execute; AWS integration |
| **Claude Code** | CLI Agent | Long context, autonomous coding, Git integration |
| **GitHub Spec-Kit** | Extension | GitHub-native spec workflow |
| **Cursor** | AI IDE | Inline spec editing |
| **Windsurf** | AI IDE | Multi-file spec awareness |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Accepting AI spec without review | Always verify AI-generated specs against domain knowledge |
| Over-relying on AI for domain context | Provide rich context; AI lacks your business knowledge |
| Specs too large for context window | Break into focused, modular specs |
| Ignoring AI suggestions | Review all suggestions; AI catches edge cases humans miss |

---

## Sources

- [Thoughtworks: Spec-Driven Development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Martin Fowler: SDD Tools](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [Microsoft: Spec-Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
- [JetBrains: Spec-Driven Approach](https://blog.jetbrains.com/junie/2025/10/how-to-use-a-spec-driven-approach-for-coding-with-ai/)
- [Red Hat: SDD Quality](https://developers.redhat.com/articles/2025/10/22/how-spec-driven-development-improves-ai-coding-quality)
- [Scott Logic: Specification Renaissance](https://blog.scottlogic.com/2025/12/15/the-specification-renaissance-skills-and-mindset-for-spec-driven-development.html)

---

*Reference Document | AI-Assisted Specification Writing | Version 1.0*
