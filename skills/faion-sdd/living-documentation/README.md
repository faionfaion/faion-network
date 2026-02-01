# Living Documentation (Docs-as-Code)

> "Documentation that evolves at the same pace as software design and development." - Cyrille Martraire

## Overview

Living Documentation is a philosophy and practice that treats documentation as a living artifact that changes alongside your codebase. Rather than creating static documents that become outdated, you generate documentation from code, specifications, and tests - ensuring it remains accurate and valuable.

**Core Principle:** Documentation should be **reliable**, require **low effort**, be **collaborative**, and provide **insight**.

---

## The Problem with Traditional Documentation

| Issue | Impact |
|-------|--------|
| Outdated immediately | Teams lose trust in docs |
| Manual updates | High maintenance burden |
| Separate from code | Drift between reality and docs |
| No validation | Broken links, invalid examples |
| Not searchable | Knowledge is siloed |

**Result:** "Documentation debt" accumulates, static wikis become graveyards of outdated information.

---

## Docs-as-Code Philosophy

### Core Principles

1. **Treat docs like code** - Same systems, processes, workflows
2. **Version control** - Store in Git alongside source code
3. **CI/CD integration** - Auto-build, lint, validate on every commit
4. **Single source of truth** - Generate from code where possible
5. **Test your docs** - Validate code examples actually run

### Documentation Types

| Generated from Code | Maintained Manually |
|---------------------|---------------------|
| API reference (OpenAPI/AsyncAPI) | Architecture decisions (ADRs) |
| Code comments (JSDoc, docstrings) | Design rationale |
| Test specs (BDD scenarios) | User guides |
| Type definitions | Tutorials |
| Changelogs (from commits) | Onboarding docs |

---

## Key Concepts from Cyrille Martraire's Book

### Living Documentation Principles

1. **Reliable** - Documentation is always accurate because it's generated from working code
2. **Low Effort** - Automation minimizes manual documentation work
3. **Collaborative** - Everyone contributes using the same tools as code
4. **Insightful** - Documentation provides understanding, not just description

### Documentation Approaches

| Approach | Description |
|----------|-------------|
| **Specification by Example** | Examples of behavior become automated tests and documentation |
| **Annotations and Conventions** | Code annotations generate documentation automatically |
| **Glossary Extraction** | Domain terms extracted from source code |
| **BDD/DDD Integration** | Living docs built on Behavior-Driven and Domain-Driven Design |

### Why Documentation?

> "Engineers across large companies consistently report that deep system behaviour is poorly documented. Process docs and style guides exist, but the underlying 'why this works this way' is rarely captured in a durable, searchable form."

---

## The "Why" Over "What"

The most valuable documentation explains **why** decisions were made, not just what the code does.

**Context Notes carry engineering history:**
- Prevent repeated architectural debates
- Avoid regressions during refactors
- Prevent production incidents from unseen edge cases

**Architecture Decision Records (ADRs):**
- Document the context, decision, and consequences
- Explain why alternatives were rejected
- Store in repository alongside code

---

## Documentation Generators (2025-2026)

### Static Site Generators

| Tool | Language | Best For |
|------|----------|----------|
| **MkDocs** | Python | Technical docs, Material theme |
| **Docusaurus** | JavaScript | Developer portals, React ecosystem |
| **Sphinx** | Python | API docs, reStructuredText, scientific |
| **VitePress** | JavaScript | Vue ecosystem, fast builds |
| **Starlight** | JavaScript | Astro-based, modern DX |

### Documentation Platforms

| Platform | Approach | Key Features |
|----------|----------|--------------|
| **Mintlify** | Docs-as-Code | Git-based, AI search, used by Anthropic |
| **GitBook** | Docs-as-Content | WYSIWYG, collaboration, Notion-like |
| **ReadTheDocs** | Open Source | Auto-build from Git, versioning |
| **Backstage** | Developer Portal | Service catalog, TechDocs |
| **Readme** | API Docs | Interactive, metrics, onboarding |

### API Documentation

| Tool | Specification | Features |
|------|---------------|----------|
| **Swagger UI** | OpenAPI 3.x | Interactive console, try-it-out |
| **Redoc** | OpenAPI 3.x | Three-panel layout, Stripe-like |
| **Scalar** | OpenAPI 3.x | Modern UI, API client built-in |
| **Bump.sh** | OpenAPI + AsyncAPI | Auto changelog, breaking changes |
| **Stoplight** | OpenAPI | Design-first, mocking |

---

## Linting and Validation

### Prose Linting

| Tool | Purpose |
|------|---------|
| **Vale** | Style guide enforcement (customizable rules) |
| **markdownlint** | Markdown syntax and style |
| **textlint** | Pluggable text linter |

### API Linting

| Tool | Purpose |
|------|---------|
| **Spectral** | OpenAPI/AsyncAPI linting |
| **Redocly CLI** | OpenAPI validation, bundling |
| **AsyncAPI CLI** | AsyncAPI validation, generation |

### Link Validation

| Tool | Purpose |
|------|---------|
| **linkinator** | Broken link detection |
| **markdown-link-check** | Check links in Markdown |
| **check-links** | Link validation in CI |

---

## LLM Optimization

Modern documentation should be optimized for both humans and LLMs.

### Best Practices

1. **Provide markdown versions** - LLMs work better with plain text
2. **Use `llms.txt` and `llms-full.txt`** - Standard format for LLM consumption
3. **Structure for context** - Clear headings, summaries, and examples
4. **Include code examples** - Executable snippets LLMs can reference

### LLM-Ready Structure

```markdown
# [Component Name]

## Summary
[1-2 sentence description for LLM context]

## Quick Start
[Code example that works immediately]

## API Reference
[Auto-generated from OpenAPI/code]

## Architecture
[Human-maintained design decisions]

## Changelog
[Auto-generated from commits]

---
*Last updated: [AUTO-DATE]*
*Generated from: [SOURCE_FILE]*
```

### Tools Supporting LLM Integration

- **Mintlify** - Created `llms-full.txt` format with Anthropic
- **GitBook** - Supports llms.txt standards
- **Custom scripts** - Generate context files for Cursor, Copilot, Claude

---

## Version Control for Docs

### Co-locate with Code

Store documentation in the same repository as code:

```
project/
├── src/           # Source code
├── docs/          # Documentation
│   ├── guides/
│   ├── api/
│   └── decisions/
├── openapi.yaml   # API specification
└── README.md
```

### Benefits

- **Same PR** - Update docs with code changes
- **Same review** - Technical review includes docs
- **Same history** - Git log shows docs evolution
- **Same CI** - Validate docs with every commit

---

## Documentation Testing

### Types of Doc Tests

| Type | Description | Tools |
|------|-------------|-------|
| **Link validation** | Check for broken links | linkinator, markdown-link-check |
| **Code example testing** | Run code snippets | doctest, pytest, mdx-js |
| **Schema validation** | Validate OpenAPI/AsyncAPI | Spectral, Redocly |
| **Prose linting** | Style guide enforcement | Vale, textlint |
| **Build testing** | Ensure docs build | MkDocs, Docusaurus build |

### Documentation Failures Block Deploys

> "Documentation failures should block deployments just like test failures or security vulnerabilities."

---

## Single-Source Documentation

### Principles

1. **Write once** - Define information in one place
2. **Reference everywhere** - Use includes, transclusions
3. **Generate variants** - Create multiple formats from single source
4. **Maintain consistency** - Updates propagate automatically

### Techniques

| Technique | Tool/Method |
|-----------|-------------|
| API from spec | OpenAPI/AsyncAPI generators |
| Docs from comments | JSDoc, Sphinx autodoc, pydoc |
| Diagrams from code | Mermaid, PlantUML, D2 |
| Changelogs from commits | conventional-changelog, release-please |
| Config docs from schemas | JSON Schema to docs |

---

## Documentation CI/CD

### Pipeline Steps

```
Code Change
    |
+---------------------------------------+
| CI/CD Pipeline                        |
|   - Lint docs (Spectral, Vale)        |
|   - Validate links                    |
|   - Generate API docs                 |
|   - Run doc tests                     |
|   - Build documentation site          |
|   - Deploy to hosting                 |
+---------------------------------------+
    |
Updated Documentation
```

### Key Metrics

| Metric | Target |
|--------|--------|
| Build success rate | > 95% |
| Time to feedback | < 10 minutes |
| Link check coverage | 100% |
| API spec validation | All specs pass |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Docs separate from code | Co-locate documentation with source code |
| Manual API doc updates | Generate from OpenAPI spec automatically |
| No link validation | Add link checker to CI pipeline |
| Docs not searchable | Index in developer portal with full-text search |
| No style enforcement | Use Vale with custom style rules |
| Code examples untested | Run doc tests in CI |
| No versioning | Use ReadTheDocs or similar for versions |

---

## External Resources

### Books

- [Living Documentation: Continuous Knowledge Sharing by Design](https://www.oreilly.com/library/view/living-documentation-continuous/9780134689418/) - Cyrille Martraire
- [Write Better with Vale](https://pragprog.com/titles/bhvale/write-better-with-vale/) - Brian P. Hogan
- [Docs for Developers](https://docsfordevelopers.com/) - Jared Bhatti et al.

### Guides and References

- [Write the Docs - Docs as Code](https://www.writethedocs.org/guide/docs-as-code/)
- [Google Documentation Best Practices](https://google.github.io/styleguide/docguide/best_practices.html)
- [Kong - What is Docs as Code](https://konghq.com/blog/learning-center/what-is-docs-as-code)

### Tools Documentation

- [Vale Documentation](https://vale.sh)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [AsyncAPI Documentation](https://www.asyncapi.com/docs)
- [Spectral Linting](https://stoplight.io/open-source/spectral)
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- [Docusaurus](https://docusaurus.io/)

### Platforms

- [Mintlify](https://mintlify.com/) - Docs-as-Code platform
- [GitBook](https://www.gitbook.com/) - Docs-as-Content platform
- [ReadTheDocs](https://readthedocs.org/) - Open source doc hosting
- [Backstage](https://backstage.io/) - Developer portal framework

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Writing specification templates | haiku | Form completion, mechanical setup |
| Reviewing specifications for clarity | sonnet | Language analysis, logical consistency |
| Architecting complex system specs | opus | Holistic design, novel combinations |

## Related Methodologies

| Methodology | Relationship |
|-------------|--------------|
| [Architecture Decision Records](../architecture-decision-records/) | ADRs are living documents |
| [API-First Design](../../faion-api-developer/api-first-design/) | OpenAPI specs as documentation |
| [Specification by Example](../specification-by-example/) | BDD scenarios as living docs |
| [Test-Driven Development](../../faion-testing-developer/tdd/) | Tests document expected behavior |

---

## Files in This Folder

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step implementation checklist |
| [examples.md](examples.md) | Real projects using docs-as-code |
| [templates.md](templates.md) | Copy-paste templates and configurations |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted documentation |

---

*Last updated: 2026-01-25*
