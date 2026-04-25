# Agent Integration — Design Docs Patterns

## When to use
- Before implementing any feature that takes more than one engineering day — writing forces clarity before code
- When a feature is cross-cutting (affects multiple modules, services, or teams) and alignment is needed
- When requirements are unclear or conflicting — the act of writing exposes gaps that discussion alone misses
- When generating an SDD `design.md` artifact in the SDD lifecycle (`spec → design → test-plan → impl-plan`)
- When an agent must communicate a technical decision to a human reviewer before proceeding with implementation
- When spawning Architecture Decision Records (ADRs) from a larger design doc

## When NOT to use
- Bug fixes with obvious root cause and one-line solution — PR description is sufficient
- Prototypes and spikes where the output is discarded regardless of design quality
- Work that takes less than a few hours — overhead exceeds benefit
- Solo work on purely internal refactors with identical external behavior — code review only

## Where it fails / limitations
- Design docs without a review deadline accumulate feedback indefinitely and never reach "Approved" state
- LLM-generated design docs can sound authoritative while missing domain-specific constraints the model has no access to (performance SLAs, compliance requirements, organizational politics)
- Heavyweight formats (Amazon 6-Pager, Uber ERD) are inappropriate for solo developers or small teams — they create process overhead without the multi-team alignment benefit
- ADRs become outdated when the codebase diverges from the decision — without tooling to link ADRs to code, they become historical artifacts that mislead future readers
- Design docs in wikis (Notion, Confluence) become invisible after 6 months — use a docs-as-code approach (markdown in repo) to keep them findable

## Agentic workflow
A design-doc agent takes a feature spec (from `spec.md`) and generates a structured `design.md` following the lightweight Google-style format: context/problem, goals/non-goals, proposed solution, alternatives considered, open questions. The agent explicitly identifies decisions that require human judgment (trade-offs, irreversible choices, compliance implications) and marks them as `[DECISION NEEDED]` sections. After human review and approval, a second agent extracts key architectural decisions into individual ADR files using the `adr-tools` format.

### Recommended subagents
- `design-doc-agent` (Sonnet/Opus) — generates design doc draft from spec; identifies gaps and trade-offs; produces `design.md`
- `adr-agent` (Haiku) — extracts key decisions from approved design doc into ADR files using standard template
- `review-agent` (Sonnet) — reads design doc and spec together, flags inconsistencies and missing non-goals

### Prompt pattern
```
You are writing a lightweight design doc (Google-style) for the following feature spec:

<spec.md contents>

Generate design.md with these sections:
1. Context and problem statement
2. Goals (what this design achieves)
3. Non-goals (explicit out-of-scope items)
4. Proposed solution (architecture, data flow, key decisions)
5. Alternatives considered (at least 2, with trade-offs)
6. Open questions (mark as [DECISION NEEDED] if human input is required)

Keep it to 2-4 pages. No implementation details — focus on "what and why", not "how".
```

```
Read this design doc and identify:
1. Decisions that are irreversible or expensive to change later (flag as HIGH RISK)
2. Assumptions that are not validated by data
3. Missing non-goals that could cause scope creep
4. Sections where the proposed solution contradicts the goals

Return a structured review with line references.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `adr-tools` | CLI for creating, listing, and linking ADRs as markdown files | `brew install adr-tools` / [github.com/npryce/adr-tools](https://github.com/npryce/adr-tools) |
| `markdownlint` | Lint design doc markdown for style consistency | `npm install -g markdownlint-cli` / [github.com/DavidAnson/markdownlint](https://github.com/DavidAnson/markdownlint) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion | SaaS | Partial — API | Good for team wikis; API allows reading/writing pages programmatically |
| Google Docs | SaaS | Partial — Drive API | Most common for lightweight design docs; API access is complex |
| GitHub / GitLab (markdown) | SaaS/OSS | Yes — Git | Docs-as-code in repo; agents can read, write, and PR design docs |
| designdocs.dev | SaaS | No | 1000+ real-world design doc examples for reference |
| Backstage | OSS | Yes — API | ADR plugin integrates with Backstage catalog |

## Templates & scripts
See `templates.md` for the full Google-style, Amazon 6-Pager, and ADR templates.

ADR creation script using adr-tools (inline):
```bash
#!/bin/bash
# create-adr.sh TITLE
# Usage: ./create-adr.sh "Use PostgreSQL as primary database"
set -euo pipefail
TITLE="${*:?Usage: $0 TITLE}"
adr new "$TITLE"
echo "ADR created. Link it to the design doc with:"
echo "adr link <N> 'informed by' <design-doc-path>"
```

## Best practices
- Write the design doc BEFORE starting implementation — a post-hoc doc rationalizes decisions already made and misses the goal of catching issues early
- Start with non-goals — explicitly listing what a design does NOT address prevents scope creep during review
- Keep the "Alternatives considered" section honest: at least two alternatives with genuine trade-offs, not strawmen set up to fail
- Use docs-as-code (markdown in repo, same PR as spec): design docs in wikis become invisible; in-repo docs stay discoverable and versioned
- Set a review deadline when circulating the doc — without a deadline, "still in review" is a permanent state
- Mark `[DECISION NEEDED]` on every open question before sharing — gives reviewers a clear action item rather than a question to ponder
- Extract ADRs for every significant architectural choice: database selection, API versioning strategy, auth mechanism — one decision per ADR, immutable once accepted

## AI-agent gotchas
- **LLM design docs sound authoritative but lack domain context.** Agents generating design docs from specs alone will miss performance SLAs, cost constraints, existing system integration points, and organizational constraints. Always require a human review pass before treating an LLM-generated design doc as approved
- **"Alternatives considered" sections are often low quality from LLMs** — models tend to generate weak alternatives that do not represent real options. Prompt explicitly: "For each alternative, provide a real-world project that chose it and the specific trade-off that made it unsuitable here"
- **Design docs must not be implementation plans.** Agents often conflate design (what/why) with implementation plans (how/tasks). If a design doc starts listing file names and function signatures, it has crossed into implementation territory — move that content to `implementation-plan.md`
- **ADRs are immutable once accepted.** Agents must not modify existing ADR files when the decision changes — instead, create a new ADR that supersedes the old one. Agents that edit past ADRs corrupt the decision history
- **Review deadline enforcement is outside the agent's scope.** Agents can generate docs and mark open questions, but cannot chase human reviewers. Build a human checkpoint: do not proceed to `implementation-plan.md` generation until the design doc is explicitly marked "Approved"

## References
- [Design Docs at Google (Malte Ubl)](https://www.industrialempathy.com/posts/design-docs-at-google/)
- [Engineering Planning with RFCs (Pragmatic Engineer)](https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs)
- [Amazon 6-Pager anatomy](https://writingcooperative.com/the-anatomy-of-an-amazon-6-pager-fc79f31a41c9)
- [Oxide RFD process](https://oxide.computer/blog/rfd-1-requests-for-discussion)
- [designdocs.dev — 1000+ examples](https://www.designdocs.dev/)
- [ADR GitHub resources](https://adr.github.io/)
- [adr-tools CLI](https://github.com/npryce/adr-tools)
