# LLM Prompts for Living Documentation

Effective prompts for using LLMs to create, improve, and maintain documentation.

---

## Table of Contents

1. [Documentation Creation](#documentation-creation)
2. [Documentation Improvement](#documentation-improvement)
3. [API Documentation](#api-documentation)
4. [Code Documentation](#code-documentation)
5. [Architecture Documentation](#architecture-documentation)
6. [Content Transformation](#content-transformation)
7. [Quality Assurance](#quality-assurance)
8. [Specialized Tasks](#specialized-tasks)

---

## Documentation Creation

### Generate README from Code

```
Analyze this codebase and generate a comprehensive README.md that includes:

1. Project title and one-line description
2. Key features (bullet points)
3. Prerequisites
4. Installation instructions
5. Quick start example
6. Configuration options
7. API overview (if applicable)
8. Contributing guidelines summary
9. License

Repository structure:
[paste directory tree]

Main entry point code:
[paste main file]

Package manifest:
[paste package.json/pyproject.toml/go.mod]
```

### Generate Getting Started Guide

```
Create a "Getting Started" guide for new users of [PROJECT].

Context:
- Target audience: [developers/non-technical users/DevOps]
- Prerequisites: [list prerequisites]
- Installation method: [npm/pip/docker/etc.]

The guide should include:
1. Prerequisites check
2. Step-by-step installation
3. First run / "Hello World" example
4. Verification that everything works
5. Next steps and links to more documentation

Keep language simple and include all commands with expected output.
```

### Generate API Endpoint Documentation

```
Generate documentation for this API endpoint:

Endpoint: [METHOD] [path]
Handler code:
[paste handler function]

Request/Response types:
[paste type definitions]

Include:
1. Endpoint description
2. Authentication requirements
3. Request parameters (path, query, body)
4. Request body schema with examples
5. Response schema with examples
6. Error responses
7. Rate limiting info
8. Code examples in [Python/JavaScript/cURL]
```

---

## Documentation Improvement

### Improve Existing Documentation

```
Review and improve this documentation:

[paste existing docs]

Improve for:
1. Clarity - remove jargon, simplify sentences
2. Completeness - identify missing information
3. Accuracy - flag potentially outdated content
4. Structure - improve headings and flow
5. Examples - add or improve code examples

Provide:
1. Improved version
2. List of changes made
3. Questions for human review
```

### Add Examples to Documentation

```
This documentation lacks practical examples. Add relevant code examples:

Documentation:
[paste docs]

Context:
- Language: [Python/JavaScript/Go/etc.]
- Framework: [if applicable]
- Audience skill level: [beginner/intermediate/advanced]

For each concept, add:
1. Minimal working example
2. Common use case example
3. Expected output

Ensure examples are:
- Complete and runnable
- Well-commented
- Following project conventions
```

### Simplify Technical Documentation

```
Simplify this technical documentation for a [target audience] audience:

Original:
[paste technical docs]

Guidelines:
1. Replace jargon with plain language
2. Add analogies for complex concepts
3. Break down long paragraphs
4. Add visual structure (bullets, tables)
5. Include a TL;DR summary at the top

Maintain technical accuracy while improving accessibility.
```

---

## API Documentation

### Generate OpenAPI from Code

```
Generate an OpenAPI 3.1 specification from this API code:

Router/Controller code:
[paste code]

Models/Schemas:
[paste type definitions]

Requirements:
1. Include all endpoints with paths, methods, parameters
2. Generate request/response schemas from types
3. Add descriptions for all fields
4. Include example values
5. Add security requirements
6. Define common error responses

Output format: YAML
```

### Document API Changes

```
Generate a changelog entry for this API change:

Previous version:
[paste old OpenAPI/code]

New version:
[paste new OpenAPI/code]

Create:
1. Summary of changes
2. Breaking changes (if any) with migration guide
3. New features/endpoints
4. Deprecated features
5. Version bump recommendation (major/minor/patch)
```

### Generate SDK Documentation

```
Generate SDK documentation from this OpenAPI spec:

[paste OpenAPI spec]

Target language: [Python/JavaScript/Go/etc.]

Include:
1. Installation instructions
2. Authentication setup
3. Client initialization
4. Method documentation for each endpoint
5. Type definitions/interfaces
6. Error handling
7. Complete examples for common workflows
8. Pagination handling
```

---

## Code Documentation

### Generate Docstrings

```
Add comprehensive docstrings to this code:

[paste code]

Style: [Google/NumPy/Sphinx/JSDoc]

Include:
1. Brief description
2. Extended description if complex
3. Parameter descriptions with types
4. Return value description
5. Raises/Throws documentation
6. Examples in doctest format where helpful
7. Links to related functions/classes
```

### Document Complex Function

```
Document this complex function for other developers:

[paste function code]

Create documentation that explains:
1. What the function does (high-level)
2. Why it exists (business/technical context)
3. How it works (algorithm/approach)
4. Edge cases and limitations
5. Performance characteristics
6. Usage examples
7. Related functions

Format as a combination of inline comments and docstring.
```

### Generate Type Documentation

```
Generate documentation for these types/interfaces:

[paste type definitions]

For each type, document:
1. Purpose and when to use
2. Each field with description
3. Validation rules/constraints
4. Default values
5. Example instantiation
6. Related types

Format for [TypeDoc/Sphinx/etc.]
```

---

## Architecture Documentation

### Generate ADR from Discussion

```
Convert this decision discussion into an Architecture Decision Record:

Discussion/context:
[paste discussion, PR comments, or meeting notes]

Create an ADR with:
1. Title (ADR-NNNN: Decision Title)
2. Status (Proposed/Accepted/etc.)
3. Context (the problem we're facing)
4. Decision (what we're doing)
5. Consequences (positive, negative, neutral)
6. Alternatives Considered (with reasons for rejection)
7. References

Use the standard ADR format.
```

### Document System Architecture

```
Generate architecture documentation from this codebase:

Project structure:
[paste directory tree]

Key configuration:
[paste docker-compose.yml, k8s manifests, etc.]

Main components:
[paste key module descriptions]

Create:
1. System overview
2. Component diagram (Mermaid syntax)
3. Data flow description
4. Key technologies and why they're used
5. Deployment architecture
6. Scalability considerations
```

### Generate Sequence Diagram

```
Generate a sequence diagram for this workflow:

Code:
[paste relevant code/handlers]

Context:
[describe the user action or API call that triggers this]

Create a Mermaid sequence diagram showing:
1. All participants (user, services, databases)
2. Request/response flow
3. Async operations
4. Error handling paths
5. Key data transformations

Include a text description of the flow.
```

---

## Content Transformation

### Convert Wiki to Markdown

```
Convert this wiki content to clean Markdown for docs-as-code:

Wiki content:
[paste wiki content]

Requirements:
1. Convert formatting to GitHub-flavored Markdown
2. Fix heading hierarchy
3. Convert tables to Markdown tables
4. Update relative links
5. Add YAML frontmatter if applicable
6. Identify outdated content (flag with TODO)
7. Add navigation links

Base URL for new docs: [URL]
```

### Generate Blog Post from Docs

```
Transform this technical documentation into an engaging blog post:

Documentation:
[paste docs]

Target:
- Audience: [developers/managers/general]
- Tone: [professional/casual/tutorial]
- Length: [500/1000/2000 words]

Create a blog post that:
1. Has an engaging hook/intro
2. Explains the "why" before the "how"
3. Uses real-world examples
4. Includes code snippets
5. Has a clear call-to-action
6. Is SEO-optimized for: [keywords]
```

### Generate Video Script from Docs

```
Create a video tutorial script from this documentation:

Documentation:
[paste docs]

Video specifications:
- Length: [5/10/15 minutes]
- Style: [screencast/talking head/animated]
- Audience: [beginners/intermediate/advanced]

Script should include:
1. Hook (first 10 seconds)
2. Introduction and overview
3. Step-by-step walkthrough
4. Screen instructions (what to show)
5. Talking points for each section
6. Summary and next steps
7. Timestamps for editing
```

---

## Quality Assurance

### Review Documentation Quality

```
Review this documentation for quality and completeness:

[paste documentation]

Evaluate against these criteria:

1. **Accuracy**: Is the information correct?
2. **Completeness**: Are there gaps or missing topics?
3. **Clarity**: Is the language clear and unambiguous?
4. **Structure**: Is information organized logically?
5. **Examples**: Are there enough working examples?
6. **Up-to-date**: Does it match current code/product?
7. **Accessibility**: Is it readable for the target audience?
8. **Searchability**: Are key terms and concepts findable?

Provide:
- Score (1-10) for each criterion
- Specific issues found
- Prioritized improvement recommendations
```

### Check Code Examples

```
Verify that all code examples in this documentation are correct:

Documentation with code:
[paste docs]

Language: [Python/JavaScript/etc.]
Version: [specific version]

For each code example:
1. Check syntax correctness
2. Verify imports are included
3. Ensure variables are defined
4. Check for deprecated APIs
5. Validate expected output matches
6. Flag examples that need context

List all issues found with line numbers.
```

### Generate Vale Rules

```
Analyze our documentation and suggest custom Vale rules:

Sample documentation:
[paste several doc pages]

Our style preferences:
[describe tone, terminology preferences, etc.]

Suggest Vale rules for:
1. Brand/product terminology consistency
2. Technical term preferences
3. Sentence complexity limits
4. Heading style
5. Link text requirements
6. Commonly misused words

Format as Vale YAML configuration files.
```

---

## Specialized Tasks

### Generate Changelog

```
Generate a changelog from these commits:

Commits:
[paste git log or commit messages]

Context:
- Product name: [name]
- Version: [new version]
- Previous version: [old version]

Format as:
1. Summary of release
2. Breaking changes (with migration guide)
3. New features
4. Improvements
5. Bug fixes
6. Deprecations
7. Contributors

Follow Keep a Changelog format.
```

### Generate FAQ from Support Tickets

```
Analyze these support tickets and generate an FAQ:

Tickets:
[paste support tickets or common questions]

Create an FAQ that:
1. Groups similar questions
2. Provides clear, concise answers
3. Links to detailed documentation
4. Includes troubleshooting steps
5. Suggests preventive measures

Organize by:
- Getting Started
- Configuration
- Troubleshooting
- Integration
- Billing/Account (if applicable)
```

### Generate Migration Guide

```
Generate a migration guide from version [OLD] to [NEW]:

Old API/Code:
[paste old version]

New API/Code:
[paste new version]

Create a migration guide with:
1. Overview of changes
2. Prerequisites before migrating
3. Step-by-step migration process
4. Code transformation examples (before/after)
5. Common issues and solutions
6. Rollback instructions
7. Verification steps
8. Timeline recommendations
```

### Generate Runbook

```
Create an operational runbook for this service:

Service code/config:
[paste relevant code and configuration]

Monitoring setup:
[paste monitoring/alerting config if available]

Create a runbook with:
1. Service overview
2. Architecture and dependencies
3. Common alerts and responses
4. Troubleshooting decision tree
5. Restart/recovery procedures
6. Escalation paths
7. Useful commands and queries
8. Post-incident checklist
```

---

## Prompt Engineering Tips

### Context Matters

Always provide:
- Project/product name
- Target audience
- Technical stack
- Existing conventions
- Specific constraints

### Be Specific About Format

Specify:
- Output format (Markdown, RST, etc.)
- Style guide to follow
- Length constraints
- Required sections

### Iterate

1. Start with high-level generation
2. Review and refine
3. Ask for specific improvements
4. Request alternative phrasings

### Validation

Always verify:
- Code examples run correctly
- Links are valid
- Technical accuracy
- Consistency with existing docs

---

## Integration with Tools

### Using with Claude Code

```bash
# Generate docs from codebase
claude "Generate API documentation for src/api/ following our OpenAPI template"

# Improve existing docs
claude "Review and improve docs/getting-started.md for clarity"

# Convert formats
claude "Convert wiki/old-docs.html to Markdown in docs/"
```

### Using with Cursor

```
@docs Analyze the authentication module and generate developer documentation

@codebase Generate a sequence diagram for the checkout flow

@file:src/api.ts Generate JSDoc comments for all exported functions
```

---

*Use these prompts as starting points. Customize based on your project's specific needs and conventions.*
