# Agent Integration — Help and Documentation

## When to use
- Writing or auditing in-app help content: tooltips, empty states, onboarding tours, inline hints
- Generating knowledge base articles or how-to guides from product specs or changelogs
- Auditing existing documentation for staleness, gaps, or coverage against support ticket patterns
- Building a help search index from existing markdown/docs content
- Creating contextual help copy for complex forms, settings pages, or error states

## When NOT to use
- Replacing interface design improvements — if the UI requires a tooltip to be understood, the UI is broken first
- Producing final user-facing copy without human editorial review (accuracy and tone)
- Generating API reference documentation without code-level context (hallucination risk on technical details)
- Substituting for user research on what users actually struggle with — support ticket analysis must precede content strategy

## Where it fails / limitations
- Agents generate plausible but inaccurate step-by-step instructions when they lack ground-truth product screenshots or current UI state
- Generated documentation goes stale immediately after product changes — no self-updating mechanism without a pipeline
- Contextual help placement requires UI/UX judgment that agents cannot make from text descriptions alone
- Agents cannot verify that help content is accessible (screen reader, keyboard navigation) without running automated tools
- Help audit tables generated from requirement lists miss implicit user confusion patterns — support tickets are a better input

## Agentic workflow
An agent ingests support ticket clusters (or user interview themes) and maps each to a help content type (tooltip, FAQ, how-to, onboarding step). It then generates draft content for each gap using the Help Content Template from `templates.md`. A second agent runs a help audit pass against the existing docs index, producing a gap/staleness report. Output is a prioritized content backlog with draft content ready for human editorial review before publishing.

### Recommended subagents
- `faion-sdd-executor-agent` — runs structured help content generation tasks from an implementation-plan task file
- General Claude subagent (opus) — analyzes support tickets and maps to help content gaps; handles nuanced user confusion patterns

### Prompt pattern
```
You are a technical writer creating contextual help for [product feature].
Given this feature description: [description]
Generate help content for three levels:
1. Inline hint (≤15 words) shown below the input field
2. Tooltip (≤40 words) shown on ? icon hover
3. How-to article (step-by-step, using the Help Content Template structure)
Do not invent behavior not described. Flag any step where you need clarification.
```

```
Help audit prompt:
Given this list of support tickets grouped by topic: [list]
And this existing help content index: [index]
For each ticket topic:
1. Does existing documentation cover it? (Y/N + link or "missing")
2. Is the content findable via search with natural language queries?
3. Is the content current (no references to deprecated features)?
Output: a gap table with priority (High/Medium/Low) and recommended action.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mintlify` | Docs-as-code platform with search and versioning | `npm i -g mintlify` / https://mintlify.com/docs |
| `docusaurus` | Static docs site with full-text search | `npx create-docusaurus@latest` / https://docusaurus.io |
| `vale` | Prose linter — enforces plain language, style guide rules | `brew install vale` / https://vale.sh |
| `markdownlint-cli` | Validates markdown structure and consistency | `npm i -g markdownlint-cli` / https://github.com/igorshubovych/markdownlint-cli |
| `broken-link-checker` | Finds dead links in documentation | `npm i -g broken-link-checker` / https://github.com/stevenvachon/broken-link-checker |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Intercom Articles | SaaS | Yes (REST API) | Create/update help articles programmatically; search analytics included |
| Notion | SaaS | Yes (REST API) | Draft help content in Notion pages via API; export to publishing pipeline |
| Mintlify | SaaS/OSS | Yes (CLI + API) | Git-based docs with AI search; agents can open PRs for doc updates |
| Algolia DocSearch | SaaS | Yes (REST API) | Power help search with crawled docs; query analytics reveal missing content |
| Chameleon / Pendo | SaaS | Partial | In-app guided tours; REST APIs for flow management; no agent-authoring SDK |
| ReadMe.com | SaaS | Yes (REST API) | API docs + guides with version management; supports programmatic content sync |

## Templates & scripts
See `templates.md` for the Help Content Template and Help Audit Template.

Inline script — scan markdown docs for broken internal links and stale screenshots:
```bash
#!/usr/bin/env bash
# help-audit.sh — check docs dir for broken links and outdated markers
# Usage: bash help-audit.sh docs/
DOCS=${1:-docs}
echo "=== Broken internal links ==="
grep -rEo '\[.*?\]\(([^)]+)\)' "$DOCS" \
  | grep -v 'http' \
  | awk -F'(' '{print $2}' \
  | tr -d ')' \
  | while read -r link; do
      [ ! -f "$DOCS/$link" ] && echo "MISSING: $link"
    done

echo ""
echo "=== Potentially stale content (references to version markers) ==="
grep -rn "TODO\|FIXME\|outdated\|deprecated\|v[0-9]\+\.[0-9]\+" \
  --include="*.md" "$DOCS" \
  | head -40
```

## Best practices
- Write help content at the moment a feature ships, not retroactively — treat it as a definition of done
- Use support ticket language, not product team language — users search with their words, not yours
- Every how-to article must have a "Result" section describing what success looks like
- Empty states are help content — design them with action guidance, not just "No items found"
- Version-pin screenshots with the app version they were taken from; stale screenshots erode trust faster than missing ones
- Track "zero-results help searches" weekly — each is an explicit content gap signal

## AI-agent gotchas
- Agents cannot verify that generated step-by-step instructions match the actual current UI — always require a human QA pass against the live product
- Generated FAQ answers are often correct in aggregate but wrong in specific edge cases — human review required before publishing
- Agents producing onboarding tour copy do not know which UI elements exist or their current labels — provide a component inventory as input
- Do not publish agent-generated documentation directly; treat all output as first draft requiring editorial review
- Agents will invent plausible troubleshooting steps that do not correspond to real error states — require a list of actual error codes/states as input

## References
- https://www.nngroup.com/articles/help-and-documentation/
- https://www.writethedocs.org/guide/
- https://developers.google.com/tech-writing
- https://learn.microsoft.com/en-us/style-guide/welcome/
- Don't Make Me Think (revised ed.) — Steve Krug
