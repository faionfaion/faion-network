# Living Documentation Implementation Checklist

Step-by-step guide to implementing Docs-as-Code practices in your project.

---

## Phase 1: Foundation

### 1.1 Repository Structure

- [ ] Create `docs/` folder in your repository
- [ ] Add documentation to `.gitignore` build outputs (e.g., `docs/_build/`, `site/`)
- [ ] Create `README.md` with project overview
- [ ] Create `CONTRIBUTING.md` with documentation guidelines

```
project/
├── docs/
│   ├── index.md          # Documentation home
│   ├── getting-started/  # Onboarding guides
│   ├── guides/           # How-to guides
│   ├── reference/        # API reference (auto-generated)
│   ├── decisions/        # ADRs
│   └── _assets/          # Images, diagrams
├── openapi.yaml          # API specification
├── mkdocs.yml            # Documentation config
└── README.md
```

### 1.2 Choose Documentation Generator

- [ ] Evaluate options (MkDocs, Docusaurus, Sphinx, VitePress)
- [ ] Install chosen generator
- [ ] Create initial configuration file
- [ ] Add build script to `package.json` or `Makefile`

**Decision Criteria:**

| Factor | MkDocs | Docusaurus | Sphinx | VitePress |
|--------|--------|------------|--------|-----------|
| Language | Python | Node.js | Python | Node.js |
| Best for | Tech docs | Portals | API docs | Vue projects |
| Markdown | Native | MDX | reST + MD | Native |
| Build speed | Fast | Medium | Slow | Very fast |

### 1.3 Set Up Local Development

- [ ] Add documentation dev server command
- [ ] Configure hot reload
- [ ] Test build locally
- [ ] Verify all links work

---

## Phase 2: Linting and Validation

### 2.1 Prose Linting with Vale

- [ ] Install Vale
- [ ] Create `.vale.ini` configuration
- [ ] Download style packages (Microsoft, Google, or custom)
- [ ] Create custom vocabulary file
- [ ] Add Vale to editor (VS Code extension)

```ini
# .vale.ini
StylesPath = docs/.styles
MinAlertLevel = warning

[*.md]
BasedOnStyles = Microsoft, custom
```

### 2.2 Markdown Linting

- [ ] Install markdownlint
- [ ] Create `.markdownlint.json` configuration
- [ ] Configure rules for your project
- [ ] Add editor integration

### 2.3 Link Validation

- [ ] Install link checker (linkinator, markdown-link-check)
- [ ] Configure for your project
- [ ] Add to pre-commit hooks
- [ ] Add to CI pipeline

### 2.4 API Specification Linting

- [ ] Install Spectral (for OpenAPI/AsyncAPI)
- [ ] Create `.spectral.yaml` ruleset
- [ ] Add custom rules for your API standards
- [ ] Validate existing specs

---

## Phase 3: API Documentation

### 3.1 API Specification

- [ ] Create or update `openapi.yaml` / `asyncapi.yaml`
- [ ] Validate specification with Spectral
- [ ] Add specification to version control
- [ ] Set up spec-first workflow

### 3.2 API Reference Generation

- [ ] Choose API docs tool (Swagger UI, Redoc, Scalar)
- [ ] Configure integration with your generator
- [ ] Set up automatic regeneration on spec changes
- [ ] Add "Try It" functionality if needed

### 3.3 Code-Generated Documentation

- [ ] Configure JSDoc/TypeDoc (JavaScript/TypeScript)
- [ ] Configure Sphinx autodoc (Python)
- [ ] Configure Godoc (Go)
- [ ] Add doc comments to public APIs
- [ ] Generate reference documentation

---

## Phase 4: CI/CD Integration

### 4.1 CI Pipeline Setup

- [ ] Create documentation CI workflow
- [ ] Add linting step (Vale, markdownlint)
- [ ] Add link checking step
- [ ] Add API spec validation step
- [ ] Add documentation build step
- [ ] Configure caching for faster builds

### 4.2 Pull Request Checks

- [ ] Add PR checks for documentation changes
- [ ] Configure diff-based validation
- [ ] Set up preview deployments
- [ ] Add breaking change detection (for APIs)

### 4.3 Deployment

- [ ] Choose hosting (GitHub Pages, Netlify, Vercel, ReadTheDocs)
- [ ] Configure automatic deployment on merge
- [ ] Set up custom domain if needed
- [ ] Configure versioning (if needed)

### 4.4 Monitoring

- [ ] Set up documentation analytics
- [ ] Configure search indexing (Algolia, Meilisearch)
- [ ] Add feedback mechanism
- [ ] Monitor broken links regularly

---

## Phase 5: Documentation Testing

### 5.1 Code Example Testing

- [ ] Identify all code examples in documentation
- [ ] Set up doctest or equivalent
- [ ] Add code extraction and testing to CI
- [ ] Configure language-specific testing (pytest, Jest, etc.)

### 5.2 Scenario Testing

- [ ] Review all "getting started" guides
- [ ] Test each step manually
- [ ] Automate where possible
- [ ] Add to CI as smoke tests

### 5.3 Accessibility Testing

- [ ] Run accessibility audit (Lighthouse, axe)
- [ ] Fix accessibility issues
- [ ] Add accessibility check to CI
- [ ] Ensure proper heading structure

---

## Phase 6: LLM Optimization

### 6.1 LLM-Ready Content

- [ ] Create `llms.txt` in docs root
- [ ] Create `llms-full.txt` with complete content
- [ ] Add clear summaries to each page
- [ ] Include executable code examples

### 6.2 Structured for AI

- [ ] Use consistent heading structure
- [ ] Add frontmatter with metadata
- [ ] Include "Quick Start" sections
- [ ] Provide context in each section

### 6.3 Integration

- [ ] Configure for Cursor integration
- [ ] Add to MCP server if applicable
- [ ] Test with Claude/GPT prompts
- [ ] Iterate based on AI responses

---

## Phase 7: Team Adoption

### 7.1 Guidelines and Training

- [ ] Create documentation style guide
- [ ] Document the documentation process
- [ ] Train team on Vale and linting
- [ ] Create templates for common doc types

### 7.2 Workflow Integration

- [ ] Add documentation checklist to PR template
- [ ] Update definition of done to include docs
- [ ] Create documentation-focused code review guidelines
- [ ] Set up doc champions or rotating ownership

### 7.3 Continuous Improvement

- [ ] Collect feedback on documentation
- [ ] Review analytics regularly
- [ ] Update style rules based on common issues
- [ ] Refine automation based on team needs

---

## Quick Start Checklist

For teams wanting to start quickly, focus on these essentials:

### Minimum Viable Docs-as-Code

- [ ] Docs in Git (same repo as code)
- [ ] Markdown format
- [ ] Basic generator (MkDocs or Docusaurus)
- [ ] Link checker in CI
- [ ] Auto-deploy on merge

### Next Level

- [ ] Vale for prose linting
- [ ] OpenAPI spec with auto-generated docs
- [ ] PR previews
- [ ] Search integration

### Advanced

- [ ] Doc testing (code examples run)
- [ ] Multiple output formats
- [ ] Versioned documentation
- [ ] LLM optimization (llms.txt)
- [ ] Custom style rules
- [ ] Analytics and feedback

---

## Verification Checklist

After implementation, verify:

| Check | Status |
|-------|--------|
| Docs build without errors | [ ] |
| All links valid | [ ] |
| Vale passes without errors | [ ] |
| API spec validates | [ ] |
| Code examples run | [ ] |
| Search works | [ ] |
| Mobile-friendly | [ ] |
| Accessible (WCAG 2.1) | [ ] |
| LLMs can use docs effectively | [ ] |
| Team knows the workflow | [ ] |

---

## Common Blockers and Solutions

| Blocker | Solution |
|---------|----------|
| Team resistance | Start small, show value early |
| Legacy docs in wiki | Migrate incrementally, auto-convert |
| No API spec | Create from code using generators |
| Complex build | Simplify, use pre-built themes |
| Slow CI | Cache dependencies, parallelize |
| Too many false positives | Tune Vale rules, add vocab |

---

*Use this checklist progressively. Complete Phase 1-2 before moving to advanced phases.*
