# Agent Integration — Architecture Decision Records (ADR)

## When to use
- Before committing to a tech stack choice that will be hard to reverse (database, framework, auth strategy)
- After a production incident that exposes a design weakness — capture the fix decision
- When a new team member keeps asking "why did we choose X?" — ADR is the answer
- Anytime two or more viable alternatives were seriously considered
- At the start of a new feature with meaningful architectural surface (new service, new API contract, new data model)

## When NOT to use
- Trivial implementation details (which library function to call, naming conventions)
- Decisions that will certainly be revisited within 1-2 weeks (too early, no context yet)
- Configuration values that belong in docs, not in decision records
- When there was only one realistic option — no choice means no ADR needed

## Where it fails / limitations
- ADRs not co-located with code (e.g., stored only in wiki) get stale and orphaned — agents can't find them during code review
- Agents cannot automatically detect when a decision is superseded; humans must update status fields
- "Proposed" ADRs require human review and sign-off; agents must not self-approve
- ADR quality degrades when alternatives section is skipped — agents writing ADRs will omit alternatives if not prompted explicitly

## Agentic workflow
An agent reads the codebase's `docs/adr/` directory, identifies the highest existing ADR number, and writes a new `NNN-title.md` file using the Nygard format. The agent populates Context from the spec/design docs, Decision from the architectural direction already established, and Consequences from tradeoff analysis. All new ADRs are written with status `Proposed`; a human must change it to `Accepted` before the ADR is considered active. The `faion-sdd-executor-agent` references existing ADRs (via AD-X citations) during implementation task execution.

### Recommended subagents
- `faion-sdd-executor-agent` — reads ADRs as AD-X citations in design.md; enforces decisions during code generation
- General research subagent (claude-opus-4-7) — drafts alternatives section and consequences; requires broad context

### Prompt pattern
```
Read docs/adr/ to find the next ADR number. Read {feature}/design.md to extract decision AD-{N}.
Write docs/adr/{NNN}-{slug}.md using the Nygard format.
Status must be "Proposed". List at least 2 alternatives considered and why each was rejected.
Do not invent consequences — base them only on information in spec.md and design.md.
```

```
Review existing ADRs in docs/adr/. For each ADR with status "Accepted", check if the codebase
still follows the decision. Output a table: ADR number | Status | Still followed? | Notes.
Flag any ADR that appears to be violated as "review-needed".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `adr-tools` | CLI to create, list, and link ADRs in standard format | `brew install adr-tools` / https://github.com/npryce/adr-tools |
| `log4brains` | Markdown-based ADR knowledge base with web UI | `npx log4brains init` / https://github.com/thomvaill/log4brains |
| `pyadr` | Python CLI for ADR lifecycle management | `pip install pyadr` / https://github.com/opinionated-digital-center/pyadr |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub (docs/adr/ in repo) | SaaS | Yes | Best: ADRs versioned with code, agents can read via file system |
| Confluence | SaaS | Partial — REST API | ADRs stored in wiki; agents can write via API but content drifts from code |
| Notion | SaaS | Yes — REST API | Flexible; works if team uses Notion for docs; link to code PRs manually |
| Backstage | OSS | Yes — REST/gRPC | ADR plugin available; good for large orgs with service catalogs |
| log4brains | OSS | Yes — file-based | Static site generation from `docs/adr/`; zero API needed |

## Templates & scripts
See `templates.md` for the full Nygard ADR template.

Inline script — list all ADRs with status:
```bash
#!/usr/bin/env bash
# adr-status.sh — list ADRs with their status line
ADR_DIR="${1:-docs/adr}"
echo "ADR | Title | Status"
echo "----|-------|-------"
for f in "$ADR_DIR"/*.md; do
  num=$(basename "$f" .md | cut -d- -f1)
  title=$(head -1 "$f" | sed 's/# //')
  status=$(grep -m1 "^\*\*Status:\*\*" "$f" | sed 's/\*\*Status:\*\* //')
  echo "$num | $title | $status"
done
```

## Best practices
- Number sequentially from 001; never reuse a number even if an ADR is deleted
- Write in active voice: "We will use PostgreSQL" not "PostgreSQL was chosen"
- Keep each ADR under 400 words; if it's longer, the decision scope is too broad — split it
- Link related ADRs bidirectionally in the "Related Decisions" section
- Store in `docs/adr/` in the same repository as the code; agents need file-system access
- When superseding, update the old ADR's status to "Superseded by ADR-NNN" — do not delete
- Review ADRs at major version bumps; mark obsolete ones as "Deprecated"

## AI-agent gotchas
- Agents will fabricate alternatives if not grounded in real context — always provide spec.md and design.md as input
- "Proposed" status is a human-in-loop gate; agents must not skip it even when certain
- Agents writing ADRs tend to copy-paste consequences from the Decision section — require distinct, actionable consequence bullets in the prompt
- Long ADR histories (>50 files) increase context cost; pass only the index list to agents, not all ADR content
- ADR content is immutable by convention; agents must create a new ADR to amend decisions, never edit an Accepted one

## References
- https://adr.github.io — ADR GitHub org, tools and format overview
- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions — Nygard's original post
- https://aws.amazon.com/architecture/well-architected/ — AWS Well-Architected includes decision logging
- https://github.com/npryce/adr-tools — adr-tools CLI
- https://github.com/thomvaill/log4brains — log4brains static ADR site
