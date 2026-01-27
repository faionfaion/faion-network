# AI-Assisted Specification Writing

> **Methodology:** Collaborative human-AI specification creation using LLMs to draft, refine, and validate requirements.

## Overview

Traditional specification writing is slow, inconsistent, and often neglected. AI-assisted specification writing transforms this process by leveraging LLMs as intelligent collaborators that help structure intent, identify edge cases, and maintain consistency.

**Key Insight:** AI can handle implementation, but specification skills remain critical. The quality of AI-generated code directly correlates with specification quality.

## The Problem

| Challenge | Impact |
|-----------|--------|
| Ambiguous requirements | Implementation delays, rework cycles |
| Inconsistent spec formats | Cross-team confusion, integration issues |
| Specifications become outdated | Tech debt, divergence from reality |
| Bottleneck shifted to specification | Development velocity constrained |

## The SDD-AI Workflow (2025)

```
INTENT  →  SPEC  →  PLAN  →  EXECUTION  →  REVIEW
  |          |        |          |           |
human      AI+      AI        AI agent     human
input     human   generate    execute      verify
         collab
```

## Core Principles

1. **Specification First** - Capture expected behaviors, edge cases, and constraints upfront before any implementation
2. **One Source of Truth** - Spec anchors entire project; tests, docs, and design trace back to it
3. **Built-in Testability** - Spec defines "what done looks like" with measurable acceptance criteria
4. **Iterative by Design** - Specs evolve with feedback while maintaining full traceability
5. **Human Approval Gates** - All AI-generated specs require human review before implementation

## Human-AI Collaboration Model

| Phase | Human Role | AI Role |
|-------|------------|---------|
| Intent capture | Describe problem, constraints, context | Structure thoughts, ask clarifying questions |
| Requirement extraction | Validate completeness, domain accuracy | Generate comprehensive requirements from context |
| Edge case identification | Confirm business relevance | Enumerate technical and edge possibilities |
| Acceptance criteria | Approve criteria, verify testability | Draft testable conditions in Given-When-Then |
| Format standardization | Choose appropriate format | Apply template consistently across specs |
| Validation | Final approval, sign-off | Check consistency, completeness, conflicts |

## Supported Formats

| Format | Best For | Example |
|--------|----------|---------|
| **Natural language** | Stakeholder communication, early-stage | "The system shall..." |
| **Structured Markdown** | Technical specs, internal docs | spec.md with sections |
| **YAML/JSON** | Machine-readable, automation | OpenAPI, JSON Schema |
| **BDD/Gherkin** | Testable criteria, QA alignment | Given-When-Then |
| **EARS Notation** | Precise requirements, enterprise | "When [trigger], the [system]..." |

## Tool Ecosystem (2025-2026)

| Tool | Type | Key Features | Best For |
|------|------|--------------|----------|
| **AWS Kiro** | Enterprise IDE | 3-phase: Specify → Plan → Execute | Enterprise teams, AWS integration |
| **Claude Code** | CLI Agent | 200k context, autonomous coding, Git | Complex codebases, long context |
| **GitHub Copilot Workspace** | Extension | GitHub-native spec workflow | GitHub-centric teams |
| **Cursor** | AI IDE | Inline spec editing, composer | Rapid prototyping |
| **Windsurf** | AI IDE | Multi-file spec awareness | Large projects |

## LLM Selection Guide

| Model | Strengths | Best For Specs |
|-------|-----------|----------------|
| **Claude (Opus/Sonnet 4.x)** | Deep reasoning, 200k context, clean structure | Complex system specs, long documents |
| **GPT-4.1/5.x** | Versatile, balanced, wide language support | General specs, polyglot projects |
| **Gemini 2.5/3 Pro** | Massive context (1M+), multimodal | Large-scale projects, codebase analysis |
| **o1/o3 (OpenAI)** | Advanced reasoning, logic chains | Formal specs, complex dependencies |

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Solution |
|--------------|--------------|----------|
| Accepting AI spec without review | AI lacks domain context, may hallucinate | Always verify against business knowledge |
| Over-relying on AI for domain knowledge | AI lacks your specific business context | Provide rich context, examples, constraints |
| Specs too large for context window | Truncation, loss of coherence | Break into focused, modular specs (<100k tokens) |
| Ignoring AI suggestions | AI catches edge cases humans miss | Review all suggestions, explain rejections |
| No explicit boundaries | AI cannot infer from omission | State non-goals explicitly |
| Skipping validation phase | Errors compound in implementation | Run AI review before human approval |

## Best Practices

| Practice | Description |
|----------|-------------|
| **Tight scoping** | Keep specs focused; use multiple specs for different concerns |
| **Lessons learned file** | Maintain context AI can learn from past issues |
| **Sprint integration** | Include spec requirements in sprint planning |
| **Iterative refinement** | Start rough, refine through AI dialogue |
| **Human approval gates** | All AI specs require human review before implementation |
| **Version control** | Track spec evolution alongside code |
| **Dependency-ordered phases** | Break large specs into 5-6 phases, 30-50 requirements each |

## Research Insights

Recent academic research (2025) confirms:

- LLMs significantly improve SRS quality when used as intermediate reasoning step
- Explicit context + prompt templates outperform context-only or prompt-only approaches
- Human-AI synergy produces best results: LLMs draft, humans refine and validate
- 150-200 instruction limit per spec maintains model consistency

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step specification writing checklist |
| [examples.md](examples.md) | Real AI-assisted specification examples |
| [templates.md](templates.md) | Copy-paste spec templates |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted specification |

## External Resources

### Documentation & Guides
- [AWS Kiro Documentation](https://kiro.dev/docs/specs/) - Enterprise spec-driven development
- [Addy Osmani: How to Write a Good Spec for AI Agents](https://addyosmani.com/blog/good-spec/) - Comprehensive spec writing guide
- [Addy Osmani: LLM Coding Workflow 2026](https://addyosmani.com/blog/ai-coding-workflow/) - End-to-end workflow patterns
- [Thoughtworks: Spec-Driven Development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) - Industry analysis

### Academic Research
- [LLMs in Software Requirements Specifications (ACL 2025)](https://aclanthology.org/2025.acl-srw.31.pdf) - SRS generation research
- [LLM4SE Survey (GitHub)](https://github.com/iSEngLab/AwesomeLLM4SE) - Comprehensive LLM for SE research
- [Frontiers: LLM in RE (2025)](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1519437/full) - Systematic review

### Templates & Tools
- [OpenAI PRD Template by Miqdad Jaffer](https://www.productcompass.pm/p/ai-prd-template) - AI-focused PRD structure
- [Specification by Example (Book)](https://gojko.net/books/specification-by-example/) - Collaborative specification writing

### Standards & Frameworks
- [EARS Notation](https://www.iaria.org/conferences2013/filesICCGI13/ICCGI_2013_Tutorial_Mavin.pdf) - Easy Approach to Requirements Syntax
- [Martin Fowler: Agile Fluency](https://martinfowler.com/articles/agileFluency.html) - Agile specification practices

---

*Part of the [faion-sdd](../CLAUDE.md) methodology collection.*
