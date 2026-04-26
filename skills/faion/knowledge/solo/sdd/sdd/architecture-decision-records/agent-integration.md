# Agent Integration — Architecture Decision Records

## When to use
- Technology selection decisions (framework, database, message broker) affecting the whole project
- Breaking API changes requiring consumer migration
- Adopting architectural patterns (microservices, event-driven, CQRS, hexagonal)
- Quality attribute tradeoffs where multiple reasonable options exist (eventual consistency vs. strong consistency)
- Cross-team or cross-service decisions that need a persistent rationale
- Undocumented existing decisions that implicitly govern the codebase ("let's capture why we use Redis here")

## When NOT to use
- Single-line bug fixes or trivial feature additions
- Implementation details that are fully reversible with no downstream impact
- Decisions already covered by the project constitution or a prior ADR
- Micro-decisions inside a task scope (e.g., which loop style to use)
- Experimental / spike work — wait until the experiment concludes and a real decision is made

## Where it fails / limitations
- ADRs document the moment of decision; if context drifts silently over months, the record becomes misleading without status updates
- Immutability is a discipline problem: teams frequently amend accepted ADRs in place instead of superseding them, destroying traceability
- Without tooling (adr-tools, Log4brains), ADR numbering gaps and orphaned "Superseded" links accumulate
- LLM-generated alternatives sections can be shallow; agents lack domain context to evaluate tradeoffs accurately without explicit input
- In solo/solopreneur contexts (faion-net profile), ADRs only pay back if the project outlives a few months — overhead is real for throwaway spikes

## Agentic workflow
An agent can draft an ADR in one pass after receiving the decision context: problem statement, two or three alternatives the developer is weighing, and the chosen option. The draft goes to human review before status changes from `Proposed` to `Accepted`. Supersession of an existing ADR should always be human-confirmed — the agent identifies candidate ADRs to supersede (via grep of the docs/ directory) and flags them, but does not flip status unilaterally.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the full SDD lifecycle; can generate ADR drafts as part of the design phase, linking them to AD-X entries in design.md

### Prompt pattern
```
You are drafting an Architecture Decision Record.
Context: <project constitution summary>
Decision needed: <one sentence>
Alternatives considered: <list>
Chosen option: <option>
Constraints: <hard constraints>

Produce an ADR in MADR format. Status: Proposed.
Do not mark it Accepted — that requires human sign-off.
```

```
Review ADR docs/adr/. Identify any ADR whose status should be updated
to Deprecated or Superseded given the following recent change: <change>.
List candidates with reasons. Do not edit files.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| adr-tools | Bash scripts: `adr new`, `adr list`, `adr generate toc` | `brew install adr-tools` / https://github.com/npryce/adr-tools |
| adr-tools-python | Python port of adr-tools, cross-platform | `pip install adr-tools-python` |
| Log4brains | ADR management + renders static HTML site with full decision history | `npm install -g log4brains` / https://github.com/thomvaill/log4brains |
| adr-viewer | Python: renders ADRs as browsable HTML | `pip install adr-viewer` / https://github.com/mrwilson/adr-viewer |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Log4brains | OSS | Yes — CLI-driven | Generates static site from markdown ADRs; scriptable in CI |
| GitHub (PR-based review) | SaaS | Yes | ADR review via PR; agents can open PRs with ADR drafts |
| Backstage (TechDocs) | OSS | Partial | ADRs surfaced inside Backstage portal; requires plugin config |
| Confluence | SaaS | Partial | REST API allows page creation; loses version-control benefits |

## Templates & scripts
See `templates.md` for Nygard, MADR, Y-statement, and Extended templates.

Minimal helper to create a sequenced ADR file:
```bash
#!/usr/bin/env bash
# usage: ./new-adr.sh "use-postgresql-for-primary-store"
set -euo pipefail
DIR="docs/adr"
mkdir -p "$DIR"
LAST=$(ls "$DIR"/*.md 2>/dev/null | grep -oP '\d{4}' | sort | tail -1 || echo "0000")
NEXT=$(printf "%04d" $((10#$LAST + 1)))
FILE="$DIR/${NEXT}-${1}.md"
cat > "$FILE" <<EOF
# ${NEXT}. $(echo "$1" | tr '-' ' ' | sed 's/\b./\u&/g')

Date: $(date +%Y-%m-%d)
Status: Proposed

## Context
[Why this decision is needed]

## Decision
[What was decided]

## Consequences
[Outcomes, positive and negative]
EOF
echo "Created $FILE"
```

## Best practices
- Write the ADR the day the decision is made, not retroactively — context fades within days
- Keep each ADR to one page; if rationale exceeds two pages, split into a separate architecture note and link from the ADR
- Store ADRs in the same repository as the code they govern so git history ties commits to decisions
- Always document rejected alternatives — this is the highest-value section for future readers
- When superseding, update only the `Status` line of the old ADR and add a "Superseded by" link; never rewrite its content
- In multi-agent workflows, treat ADRs as human-gated artifacts: agents draft, humans approve

## AI-agent gotchas
- Agents have no memory of prior ADRs across sessions; always pass the `docs/adr/` directory listing as context before asking for a new ADR
- LLMs hallucinate plausible-sounding alternatives that were never actually considered; prompt the human to confirm which alternatives were truly evaluated
- Status field is a human-in-loop checkpoint: agent sets `Proposed`, human sets `Accepted` after review — never automate the `Accepted` transition
- Agents may generate an ADR that duplicates an existing one; always include a step to grep for existing ADRs on the same topic before creating a new file
- Token cost: feeding all existing ADRs for context can be expensive in large projects; use adr-tools `adr list` output (titles only) to select relevant ones, then load full text selectively

## References
- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions (original Nygard post)
- https://adr.github.io/ (ADR GitHub organization — templates, tools, examples)
- https://adr.github.io/madr/ (MADR — Markdown Any Decision Records)
- https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record (Spotify guidance)
- https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/
- "Documenting Software Architectures" — Clements et al.
