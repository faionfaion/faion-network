# Agent Integration — Design Docs at Big Tech Companies

## When to use
- Choosing a design doc format/process before starting a new cross-team feature or architecture change
- Adapting an existing company's RFC/ERD process to your team's size and async culture
- Using an LLM agent to generate an initial design doc structure from requirements (agent excels at outlines and alternatives, not technical accuracy)
- Onboarding new engineers: using existing design docs as primary reference material
- Deciding whether a change needs a lightweight 1-pager, a full RFC, or no doc at all

## When NOT to use
- Bug fixes and small features (< 2 days) — skip the doc, write code
- Purely internal team decisions with no cross-team impact — use a quick comment or Slack thread
- When organizational context, team politics, or proprietary system details are critical — LLMs can't supply these
- Post-implementation documentation — design docs must precede coding to serve their purpose

## Where it fails / limitations
- LLMs generate plausible but technically inaccurate design docs when system-specific context isn't provided; every technical claim requires human verification
- The Amazon 6-pager format (no bullets, narrative prose) is difficult for LLMs to maintain over long docs — they revert to bullet points
- No tool enforces "write before coding" — without process discipline, design docs become post-mortems
- ADRs (Architecture Decision Records) produced by agents lack the organizational history and stakeholder context that makes them useful for future engineers
- Tiered RFC processes (Uber model) require human judgment to assign the right tier — agents consistently over-tier to avoid responsibility

## Agentic workflow
An agent generates the initial design doc skeleton from a spec.md, populating sections with placeholders and brainstorming alternatives (agent strength). A senior engineer or second-pass agent then validates technical accuracy, system-specific details, and trade-off correctness before the doc circulates for review. For async teams, Shopify's deadline-driven GitHub RFC model works well with agents: agent drafts PR, human reviews within deadline, agent incorporates feedback.

### Recommended subagents
- Sonnet-class agent — generate outline, alternatives section, risk list from spec.md input
- Opus-class agent — architectural review of draft doc, trade-off analysis, consistency with existing system design
- Dedicated review sub-agent (fresh context) — verify doc against constitution.md standards before circulation

### Prompt pattern
```
You are a design doc author. Input: spec.md (attached), constitution.md (attached).
Generate a design doc following the Google format:
1. Context and goals (from spec)
2. Design (2-3 alternative approaches with trade-offs; recommend one)
3. Always include "do nothing" as alternative 1
4. Implementation plan (high level)
5. Open questions
Do not include system-specific details you don't have — mark those as [NEEDS HUMAN INPUT].
```

```
Review this design doc draft for: missing alternatives, undocumented trade-offs,
missing "do nothing" option, sections where technical accuracy cannot be verified.
Output: list of issues with severity (BLOCK / WARN / NOTE).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Create RFC as GitHub PR; manage review deadline | https://cli.github.com |
| `adr-tools` | Create and manage ADR files in CLI | https://github.com/npryce/adr-tools |
| `claude` (Claude Code) | Generate initial doc structure from spec | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Docs | SaaS | Partial | Best for inline comment review (Google style); no API for structured review |
| GitHub PRs | SaaS | Yes | Shopify/Atlassian model; agent creates PR, review via PR comments |
| Confluence | SaaS | Partial | Atlassian model; REST API available for read/write |
| Slab | SaaS | Partial | RFC hosting; has API but limited automation |
| designdocs.dev | SaaS | No | Reference library of 1000+ real design docs — human browsing only |
| ADR GitHub (adr.github.io) | OSS | Yes | CLI tool for ADR lifecycle in git |

## Templates & scripts
See `templates.md` for Google, Amazon, Uber, and Spotify format templates.

ADR creation script (inline):
```bash
#!/usr/bin/env bash
# create-adr.sh <title>
# Creates a new ADR in .aidocs/decisions/ following adr.github.io format
set -euo pipefail
TITLE=$1
DECISIONS_DIR=".aidocs/decisions"
mkdir -p "$DECISIONS_DIR"
NUM=$(ls "$DECISIONS_DIR"/ADR-*.md 2>/dev/null | wc -l)
NUM=$((NUM + 1))
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
FILE="$DECISIONS_DIR/ADR-$(printf '%03d' $NUM)-$SLUG.md"
cat > "$FILE" << EOF
# ADR-$(printf '%03d' $NUM): $TITLE

## Status
Proposed

## Context
[Why are we making this decision?]

## Decision
[What did we decide?]

## Consequences
[What are the trade-offs?]

## Alternatives Considered
- Do nothing: [impact]
- [Alternative 1]: [trade-offs]
EOF
echo "Created: $FILE"
```

## Best practices
- Match doc weight to change scope: 1-pager for team-only, full RFC for cross-team, detailed ERD for org-wide (Uber tiered model)
- Always include "do nothing" as Alternative 1 — reviewers always ask, and it forces the author to justify why building is worth it
- Separate the RFC (reaching consensus) from the ADR (recording the decision) — Spotify's two-stage model prevents the doc from trying to do both jobs
- Write design docs before coding — not during, not after; changes are cheap on paper, expensive in code
- Keep reviewer count under 10; more than that creates consensus gridlock (Amazon/Google observation)

## AI-agent gotchas
- Agents produce technically fluent but organizationally ignorant design docs — they cannot know your team's history, existing systems, or stakeholder preferences
- LLMs conflate design docs (why/how) with specs (what) — enforce strict section boundaries in the prompt
- Agents over-generate alternatives (5+ options) when 2-3 concrete ones are better; instruct to limit alternatives to the 2-3 most realistic
- The Amazon 6-pager prose style (no bullets) causes agents to regress to bullets after ~2 pages — requires explicit re-prompting or post-processing
- Design doc quality degrades if the agent lacks the existing architecture context — always feed `constitution.md` and relevant existing design docs as context

## References
- https://www.industrialempathy.com/posts/design-docs-at-google/ — Malte Ubl, Google design docs
- https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs — Gergely Orosz, RFCs and design docs
- https://adr.github.io/ — Architecture Decision Records
- https://works.hashicorp.com/articles/rfc-template — HashiCorp RFC template
- https://github.com/uber/h3/blob/master/dev-docs/RFCs/rfc-template.md — Uber H3 RFC template
- "Software Engineering at Google" (O'Reilly) — design doc chapter
