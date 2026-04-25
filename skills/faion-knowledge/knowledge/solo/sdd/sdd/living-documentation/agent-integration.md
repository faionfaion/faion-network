# Agent Integration — Living Documentation (Docs-as-Code)

## When to use
- When setting up a new project's documentation pipeline: choose a generator, configure CI, co-locate docs with code
- When documentation has drifted from code: auto-generate API reference from OpenAPI specs, JSDoc, or docstrings
- When onboarding a new agent to a codebase: living docs (especially llms.txt and structured README) reduce hallucination compared to prose wikis
- When deploying a developer portal (Backstage, Port) that surfaces service ownership, architecture, and runbooks
- When documentation failures (broken links, invalid API specs) should block deploys the same as test failures

## When NOT to use
- Internal ADRs and design rationale — these must remain manually authored; auto-generated "why" is always wrong
- User-facing marketing copy — living docs tools optimize for accuracy, not persuasion
- Projects that will be archived or deprecated within 3 months — infrastructure investment exceeds value
- Teams that have not established code review discipline — docs-as-code workflows require the same PR review rigor as code PRs

## Where it fails / limitations
- Auto-generated API docs (from OpenAPI) are accurate but unreadable without human-curated guides and examples around them
- Docs-as-code CI pipelines (lint, link check, build) add maintenance overhead; broken pipelines block doc updates and frustrate contributors
- `llms.txt` is not yet universally supported by LLM tools; agents that cannot read it fall back to full-site scraping
- Vale prose linting requires custom style rules; default rules produce too many false positives on technical writing
- Backstage (89% market share) requires significant ops overhead: Kubernetes, plugin maintenance, catalog ingestion pipelines; not suitable for solo projects

## Agentic workflow
An agent maintaining living documentation operates in two modes: generation (writing docs from code artifacts) and validation (checking docs against current code). For generation, the agent reads OpenAPI specs, JSDoc comments, or Pydantic models, then writes or updates the corresponding documentation sections. For validation, the agent runs the docs CI pipeline (Vale, linkinator, Spectral) and fixes failures. The agent must never overwrite manually-authored architectural rationale sections — only update auto-generated sections tagged with `<!-- AUTO-GENERATED -->`.

### Recommended subagents
- `faion-sdd-executor-agent` — executes doc generation tasks defined in implementation-plan.md
- Haiku-tier subagent — mechanical doc generation from structured inputs (OpenAPI → Markdown, JSDoc → reference pages)
- Sonnet-tier subagent — review pass for consistency, readability, and completeness of generated docs

### Prompt pattern
```
Read the OpenAPI spec at openapi.yaml.
For each endpoint, generate a Markdown section following this template:
## POST /api/[path]
**Description:** [summary]
**Request:** [request schema as code block]
**Response (2xx):** [response schema as code block]
**Errors:** [error codes and descriptions as table]
Write output to docs/api/[tag].md. Only update sections tagged <!-- AUTO-GENERATED -->.
Do not modify any other content.
```

```
Run documentation validation and fix all failures:
1. markdownlint-cli2 docs/ — fix formatting issues
2. linkinator docs/ --recurse — fix broken links (update or remove, do not leave placeholders)
3. spectral lint openapi.yaml — fix all errors (warnings optional)
Report: N issues found, N fixed, N require human review.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `vale` | Prose style linting (customizable rules) | `brew install vale` / [docs](https://vale.sh) |
| `markdownlint-cli2` | Markdown formatting linter | `npm i -g markdownlint-cli2` / [docs](https://github.com/DavidAnson/markdownlint-cli2) |
| `linkinator` | Broken link detection (recursive) | `npm i -g linkinator` / [docs](https://github.com/JustinBeckwith/linkinator) |
| `spectral` | OpenAPI/AsyncAPI linting | `npm i -g @stoplight/spectral-cli` / [docs](https://stoplight.io/open-source/spectral) |
| `redocly` | OpenAPI validation + bundling + docs generation | `npm i -g @redocly/cli` / [docs](https://redocly.com/docs/cli/) |
| `mkdocs` | Python-based docs site builder (Material theme) | `pip install mkdocs-material` / [docs](https://squidfunk.github.io/mkdocs-material/) |
| `conventional-changelog-cli` | Auto-generate CHANGELOG.md from commit history | `npm i -g conventional-changelog-cli` / [docs](https://github.com/conventional-changelog/conventional-changelog) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Mintlify | SaaS | Yes — Git-based | llms.txt + llms-full.txt standard; Anthropic uses it; agents write Markdown, Mintlify deploys |
| ReadTheDocs | OSS/SaaS | Yes — webhook | Auto-build from Git push; version management built in |
| GitBook | SaaS | Partial — API | Good for content-heavy docs; Markdown sync available |
| Backstage TechDocs | OSS | Yes — plugin | Reads MkDocs from repo; agents write docs, portal renders them |
| Scalar | OSS | Yes — file-based | Modern API doc renderer from OpenAPI; embeddable |
| Bump.sh | SaaS | Yes — API | Tracks OpenAPI changes, auto-generates changelog for breaking changes |
| GitHub Actions | SaaS CI | Yes | Pipeline: lint → validate → build → deploy on every push |

## Templates & scripts
See `templates.md` for MkDocs config, Vale config, GitHub Actions pipeline, and llms.txt structure.

Docs CI pipeline (GitHub Actions):
```yaml
name: docs-ci
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install tools
        run: |
          npm i -g markdownlint-cli2 linkinator @stoplight/spectral-cli
          pip install vale mkdocs-material
      - name: Lint Markdown
        run: markdownlint-cli2 "docs/**/*.md"
      - name: Check links
        run: linkinator docs/ --recurse --skip "localhost"
      - name: Lint OpenAPI
        run: spectral lint openapi.yaml
      - name: Build docs
        run: mkdocs build --strict
```

## Best practices
- Tag every auto-generated section with `<!-- AUTO-GENERATED: source=openapi.yaml -->` so agents and humans know not to manually edit it
- Write `llms.txt` at the repo root listing the top-level doc structure with one-line descriptions — agents and LLM tools use it as a navigation index
- Run docs CI on every PR, not just main merges — catching broken links on feature branches costs far less than fixing them post-merge
- Keep architectural rationale (ADRs, design decisions) in manually-authored files that are explicitly excluded from auto-generation targets
- Use `bump.sh` or similar for API changelog tracking — breaking change detection in OpenAPI is more reliable than manual CHANGELOG entries
- Structure docs for both humans and LLMs: short summary paragraph → code example → full reference; LLMs read the summary + code and skip prose

## AI-agent gotchas
- Agents writing documentation auto-generate entire pages from code comments and then lose the manually-authored introductory sections on subsequent runs — use `<!-- AUTO-GENERATED -->` boundaries and instruct agents to never touch content outside those tags
- Vale rules produce many false positives on technical writing (e.g., passive voice rules flag valid API descriptions); configure `.vale.ini` to disable overly aggressive rules before running agents against the full docs
- Agents updating OpenAPI specs sometimes introduce breaking changes without flagging them (renamed fields, removed endpoints) — run `bump.sh diff` or `redocly diff` before committing spec changes
- `linkinator` follows redirects and can take minutes on large doc sites; agent timeout settings must be configured accordingly
- Agents generating `llms.txt` tend to make it too detailed (copying full section content) — the standard specifies brief descriptions, not content; link to full pages instead

## References
- [Write the Docs: Docs as Code](https://www.writethedocs.org/guide/docs-as-code/)
- [Living Documentation — Cyrille Martraire (O'Reilly)](https://www.oreilly.com/library/view/living-documentation-continuous/9780134689418/)
- [GitBook: LLM-Ready Docs](https://gitbook.com/docs/publishing-documentation/llm-ready-docs)
- [Mintlify — Docs-as-Code Platform](https://mintlify.com/)
- [Vale Documentation](https://vale.sh)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Spectral — OpenAPI Linting](https://stoplight.io/open-source/spectral)
- [Squarespace: Docs-as-Code Journey](https://engineering.squarespace.com/blog/2025/making-documentation-simpler-and-practical-our-docs-as-code-journey)
