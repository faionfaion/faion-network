# Living Documentation Examples

Real-world projects implementing Docs-as-Code practices.

---

## Enterprise Examples

### Stripe

**Approach:** Industry-leading API documentation

| Aspect | Implementation |
|--------|----------------|
| **Format** | Three-panel layout (nav, content, code) |
| **API Docs** | Generated from OpenAPI with custom tooling |
| **Code Examples** | Multi-language, runnable snippets |
| **Versioning** | Multiple API versions documented |
| **Search** | Full-text search with Algolia |

**Key Practices:**
- Every API change requires doc update in same PR
- Interactive "Try It" console
- Changelogs auto-generated from API versions
- Language-specific SDKs documented alongside API

**URL:** [stripe.com/docs](https://stripe.com/docs)

---

### Cloudflare

**Approach:** MkDocs Material with extensive customization

| Aspect | Implementation |
|--------|----------------|
| **Generator** | MkDocs with Material theme |
| **Source** | GitHub (cloudflare/cloudflare-docs) |
| **CI/CD** | GitHub Actions, Cloudflare Pages |
| **Linting** | Vale, markdownlint |
| **API Docs** | OpenAPI with Redoc |

**Key Practices:**
- Docs as code in public GitHub repo
- Community contributions welcome
- Automatic versioning per product
- Search with Algolia

**GitHub:** [github.com/cloudflare/cloudflare-docs](https://github.com/cloudflare/cloudflare-docs)

---

### Grafana

**Approach:** Comprehensive docs-as-code with Vale

| Aspect | Implementation |
|--------|----------------|
| **Generator** | Hugo |
| **Linting** | Vale with custom Grafana style |
| **CI/CD** | Drone CI, automated checks |
| **API Docs** | Auto-generated from code |
| **Multi-repo** | Docs from multiple repositories |

**Key Practices:**
- Writers' Toolkit with Vale integration
- PR previews for every documentation change
- Style guide enforcement via CI
- Grafana-specific Vale rules

**Guide:** [grafana.com/docs/writers-toolkit](https://grafana.com/docs/writers-toolkit/)

---

### Datadog

**Approach:** Vale for quality, extensive automation

| Aspect | Implementation |
|--------|----------------|
| **Generator** | Custom static site generator |
| **Linting** | Vale with custom rules |
| **Translations** | Multi-language documentation |
| **API Docs** | Auto-generated from OpenAPI |
| **CI/CD** | GitHub Actions |

**Key Practices:**
- Vale enforces terminology consistency
- Custom vocabulary for Datadog terms
- Automatic translation workflows
- Extensive code example testing

**Blog:** [datadoghq.com/blog/engineering/how-we-use-vale](https://www.datadoghq.com/blog/engineering/how-we-use-vale-to-improve-our-documentation-editing-process/)

---

### Spotify (Backstage)

**Approach:** TechDocs in developer portal

| Aspect | Implementation |
|--------|----------------|
| **Platform** | Backstage (internal developer portal) |
| **Format** | TechDocs (MkDocs-based) |
| **Source** | Docs live with service repos |
| **Catalog** | Service catalog with docs links |
| **Search** | Unified search across all services |

**Key Practices:**
- Each service owns its documentation
- Docs auto-published to portal
- Consistent templates across teams
- Documentation part of service scorecard

**URL:** [backstage.io/docs/features/techdocs](https://backstage.io/docs/features/techdocs/)

---

## Open Source Examples

### Kubernetes

**Approach:** Large-scale multi-contributor documentation

| Aspect | Implementation |
|--------|----------------|
| **Generator** | Hugo |
| **Source** | kubernetes/website on GitHub |
| **Contributors** | 100s of contributors |
| **Localization** | 15+ languages |
| **CI/CD** | Netlify, Prow checks |

**Key Practices:**
- SIG Docs working group
- Versioned documentation per release
- Automatic reference doc generation
- Community-driven translations

**GitHub:** [github.com/kubernetes/website](https://github.com/kubernetes/website)

---

### React

**Approach:** Docusaurus-powered interactive docs

| Aspect | Implementation |
|--------|----------------|
| **Generator** | Docusaurus |
| **Interactive** | Sandboxes with CodeSandbox/StackBlitz |
| **Versioning** | Version per major release |
| **Search** | Algolia DocSearch |
| **CI/CD** | Vercel deployment |

**Key Practices:**
- Interactive code examples
- Visual diagrams for concepts
- Community contributions
- Automatic deployment

**URL:** [react.dev](https://react.dev)

---

### Django

**Approach:** Sphinx with comprehensive API docs

| Aspect | Implementation |
|--------|----------------|
| **Generator** | Sphinx |
| **Format** | reStructuredText |
| **API Docs** | Auto-generated from docstrings |
| **Versioning** | Per Django version |
| **Hosting** | ReadTheDocs |

**Key Practices:**
- Every feature requires documentation
- Doc tests for code examples
- Strict review process
- Version dropdown for all releases

**URL:** [docs.djangoproject.com](https://docs.djangoproject.com)

---

### Rust

**Approach:** mdBook for guides, rustdoc for API

| Aspect | Implementation |
|--------|----------------|
| **Guides** | mdBook |
| **API** | rustdoc (generated from code) |
| **Source** | rust-lang/rust on GitHub |
| **Testing** | Code examples are tested |
| **CI/CD** | GitHub Actions |

**Key Practices:**
- The Rust Book is a first-class citizen
- All public APIs must have docs
- Code examples are compile-tested
- Community contributions encouraged

**URL:** [doc.rust-lang.org](https://doc.rust-lang.org)

---

### Astro

**Approach:** Starlight (their own docs framework)

| Aspect | Implementation |
|--------|----------------|
| **Generator** | Starlight (Astro-based) |
| **Source** | withastro/docs on GitHub |
| **i18n** | Community translations |
| **Search** | Algolia |
| **CI/CD** | Vercel |

**Key Practices:**
- Built their own docs framework (Starlight)
- Heavy use of MDX components
- Interactive examples
- Excellent developer experience

**URL:** [docs.astro.build](https://docs.astro.build)

---

## API Documentation Examples

### Anthropic (Claude API)

**Approach:** Mintlify-powered, LLM-optimized

| Aspect | Implementation |
|--------|----------------|
| **Platform** | Mintlify |
| **LLM Integration** | llms-full.txt standard |
| **API Docs** | OpenAPI-generated |
| **Examples** | Multi-language code snippets |
| **Search** | AI-powered search |

**Key Practices:**
- Co-developed llms-full.txt with Mintlify
- Documentation optimized for LLM consumption
- Interactive API playground
- Extensive prompt examples

**URL:** [docs.anthropic.com](https://docs.anthropic.com)

---

### OpenAI

**Approach:** Custom docs platform with playground

| Aspect | Implementation |
|--------|----------------|
| **Platform** | Custom |
| **API Docs** | OpenAPI with custom UI |
| **Examples** | Runnable in playground |
| **Search** | Full-text search |
| **Changelog** | Detailed API changelog |

**Key Practices:**
- Integrated API playground
- Cookbook with example use cases
- Clear migration guides
- Community examples

**URL:** [platform.openai.com/docs](https://platform.openai.com/docs)

---

### Twilio

**Approach:** Interactive tutorials and code samples

| Aspect | Implementation |
|--------|----------------|
| **Platform** | Custom |
| **API Docs** | OpenAPI-generated |
| **Tutorials** | Step-by-step with code |
| **Languages** | 6+ programming languages |
| **Testing** | Examples are tested in CI |

**Key Practices:**
- Quickstart for each product
- Code samples in all major languages
- Interactive console
- Helper libraries documented

**URL:** [twilio.com/docs](https://www.twilio.com/docs)

---

## Documentation Platforms in Production

### Projects Using Mintlify

| Project | URL |
|---------|-----|
| Anthropic | docs.anthropic.com |
| Perplexity | docs.perplexity.ai |
| Zapier | platform.zapier.com/docs |
| Resend | resend.com/docs |
| Dub | dub.co/docs |

### Projects Using GitBook

| Project | URL |
|---------|-----|
| Optimism | docs.optimism.io |
| Supabase | supabase.com/docs |
| Plane | docs.plane.so |

### Projects Using Docusaurus

| Project | URL |
|---------|-----|
| React Native | reactnative.dev |
| Redux | redux.js.org |
| Prettier | prettier.io/docs |
| Algolia | algolia.com/doc |

### Projects Using MkDocs Material

| Project | URL |
|---------|-----|
| FastAPI | fastapi.tiangolo.com |
| Pydantic | docs.pydantic.dev |
| SQLModel | sqlmodel.tiangolo.com |
| Material for MkDocs | squidfunk.github.io/mkdocs-material |

### Projects Using ReadTheDocs

| Project | URL |
|---------|-----|
| Django | docs.djangoproject.com |
| Flask | flask.palletsprojects.com |
| pytest | docs.pytest.org |
| Celery | docs.celeryq.dev |

---

## Patterns from Examples

### What Great Documentation Has in Common

1. **Docs live with code** - Same repo, same PR, same review
2. **Automated building** - CI/CD builds and deploys docs
3. **Style enforcement** - Vale or equivalent linting
4. **Search** - Algolia or similar for discoverability
5. **Versioning** - Multiple versions for different releases
6. **Community** - Open to contributions
7. **Testing** - Code examples are validated
8. **Interactive** - Runnable examples where possible

### Anti-Patterns to Avoid

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| Wiki separate from code | Docs in same repo |
| Manual deploys | Automatic CI/CD |
| No review process | Same review as code |
| Stale examples | Tested examples |
| Single maintainer | Team ownership |
| No search | Integrated search |
| No analytics | Track what's used |

---

*Study these examples when implementing your own living documentation.*
