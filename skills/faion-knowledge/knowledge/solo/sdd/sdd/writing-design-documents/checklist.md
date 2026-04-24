# Design Document Checklist

Quality gate for design documents before proceeding to implementation planning.

---

## Pre-Writing Checklist

Before starting the design document:

- [ ] Specification (spec.md) is complete and approved
- [ ] All FR-X and NFR-X requirements are defined
- [ ] Constitution is read and tech stack is understood
- [ ] Related designs in `done/` folder are reviewed
- [ ] Existing codebase patterns are researched

---

## Completeness Checklist

### Requirements Coverage

- [ ] All FR-X from spec have corresponding AD-X
- [ ] All NFR-X are addressed (performance, security, scalability)
- [ ] Spec Coverage matrix is complete
- [ ] Every FR maps to at least one AD

### Architecture Decisions

- [ ] Each AD-X has context, decision, rationale
- [ ] Alternatives considered for each decision
- [ ] Consequences documented (positive and negative)
- [ ] Trade-offs explicitly stated
- [ ] Decisions have status (Proposed/Accepted)

### Technical Specification

- [ ] All files listed with CREATE/MODIFY actions
- [ ] All API endpoints documented with request/response
- [ ] All data models defined (TypeScript + SQL if applicable)
- [ ] Dependencies listed with versions
- [ ] Error handling documented

### Cross-Cutting Concerns

- [ ] Security considerations documented
- [ ] Performance targets defined
- [ ] Caching strategy specified (if applicable)
- [ ] Logging and monitoring approach defined
- [ ] Migration/rollback plan (if applicable)

---

## Clarity Checklist

### Structure

- [ ] Document follows standard template
- [ ] Sections are in logical order
- [ ] Table of contents is accurate
- [ ] Links to reference documents work

### Content

- [ ] Technical jargon is explained or linked
- [ ] Diagrams are clear and labeled
- [ ] Code examples are syntactically correct
- [ ] API examples include realistic data

### Traceability

- [ ] File changes traced to FR-X and AD-X
- [ ] Test strategy covers acceptance criteria
- [ ] Related designs are linked

---

## LLM-Readiness Checklist

Design doc optimized for LLM code generation:

- [ ] Type definitions are complete and explicit
- [ ] API contracts have example JSON
- [ ] Error responses are documented
- [ ] Validation rules are specified
- [ ] Pattern references point to existing code
- [ ] File structure uses absolute paths
- [ ] Dependencies have exact versions

---

## Review Checklist

Before marking design as approved:

### Self-Review

- [ ] Read the document from start to finish
- [ ] All TODOs and placeholders resolved
- [ ] No outdated information
- [ ] No conflicting decisions

### Peer Review

- [ ] At least one other engineer reviewed
- [ ] Security review completed (if security-sensitive)
- [ ] Performance review completed (if performance-critical)
- [ ] Feedback addressed or documented

### LLM Review (Optional)

Use this prompt to have an LLM review the design:

```
Review this design document for:
1. Completeness - are all requirements covered?
2. Clarity - is anything ambiguous?
3. Correctness - are there technical issues?
4. Consistency - does it align with the spec?
5. Implementability - can this be built as described?

Provide specific, actionable feedback.
```

---

## Common Mistakes to Avoid

| Mistake | How to Fix |
|---------|------------|
| No rationale for decisions | Always explain WHY, not just WHAT |
| Missing file list | Every file touched must be listed |
| Vague API contracts | Specify exact request/response JSON |
| No traceability | Every AD must trace to FR-X |
| Forgetting security | Add security section for ALL features |
| No testing strategy | Define what tests you'll write |
| Missing alternatives | Document at least 2 alternatives per major AD |
| No related designs | Check `done/` folder for patterns |
| Overspecification | Keep it high-level, don't write pseudo-code |
| Underspecification | Include enough detail for implementation |

---

## Quality Metrics

| Metric | Target |
|--------|--------|
| FR Coverage | 100% of FR-X have AD-X |
| NFR Coverage | 100% of NFR-X addressed |
| Alternatives | At least 2 per major decision |
| API Documentation | 100% endpoints with examples |
| File Traceability | 100% files linked to AD-X |

---

## Sign-off Template

```markdown
## Design Approval

**Design:** [Feature Name]
**Version:** X.X
**Date:** YYYY-MM-DD

### Checklist Status

- [x] Completeness: All sections filled
- [x] Clarity: Reviewed and clear
- [x] Traceability: All mappings verified
- [x] LLM-Ready: Optimized for code generation

### Reviewers

| Reviewer | Role | Status | Date |
|----------|------|--------|------|
| [Name] | Author | Approved | YYYY-MM-DD |
| [Name] | Peer | Approved | YYYY-MM-DD |

### Notes

[Any caveats or deferred decisions]

---

**Status:** APPROVED - Ready for Implementation Plan
```

---

*Checklist | SDD Quality Gate | Version 3.0.0*
