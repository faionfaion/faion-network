# Agent Integration — Architecture Workflows

## When to use
- Standardizing repeated architecture activities across a team or project: design, review, ADR, evaluation, assessment, migration, design doc review.
- Onboarding a new architect/agent — gives them a checklist instead of tribal knowledge.
- Multi-stakeholder decisions where the workflow itself (readouts, async review) is the deliverable, not just the outcome.
- Audit-grade documentation (regulated industries) where you must show "we followed an evaluation method."

## When NOT to use
- One-person, one-decision contexts where the workflow ceremony costs more than the decision.
- Pure code-level refactors — use design-pattern methodologies, not these high-level workflows.
- Tight time-boxed prototypes; the workflows assume there is room for review cycles.

## Where it fails / limitations
- ATAM/CBAM are heavyweight; teams under ~20 people rarely sustain them without burnout.
- Agent-driven "review workflows" tend to produce LGTM-grade rubber-stamps unless you wire in adversarial reviewers and explicit failure criteria.
- Workflows codify steps but not judgement — the trickiest decisions still require senior humans to break ties.
- Migration planning workflows underestimate data backfills; LLM plans typically skip the dual-write/cutover scaffolding details.

## Agentic workflow
Treat each workflow type as a small pipeline of role-specialized subagents: a clarifier, a designer, a reviewer/critic, and a documenter. Drive them via `faion-brainstorm` for diverge/converge phases, `faion-sdd-execution` for structured outputs, and a separate critic-style prompt for review. Always materialize state to disk between steps (spec.md, options.md, adr-NNN.md) so agents reload from files, not transcript memory.

### Recommended subagents
- `faion-brainstorm` — diverge step in system-design and tech-evaluation workflows.
- `faion-sdd-execution` — produces spec/design/test-plan triples and tracks lifecycle states.
- `faion-feature-executor` — drives migration plan execution task-by-task.
- `faion-improver` — runs the "after-action review" 30 days post-decision against ADR consequences.

### Prompt pattern
```
ROLE: design-critic
INPUT: docs/architecture/specs/spec.md and diagrams/*.mmd
TASK: Risk-storm the design. Produce a table:
| risk | likelihood | impact | mitigation | owner |
Reject mitigations that are "add monitoring" without a concrete metric+threshold.
```

```
ROLE: tech-evaluator
GOAL: Choose between <A>, <B>, <C> for <use case> with NFRs <...>.
Output: weighted-score matrix with criteria, weights, scores, citations,
and a recommendation that survives steel-manning the runner-up.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| adr-tools | ADR creation, status transitions | https://github.com/npryce/adr-tools |
| log4brains | ADR static site + lifecycle | `npm i -g log4brains` |
| structurizr-cli | C4 DSL render in CI | https://github.com/structurizr/cli |
| mermaid-cli | Mermaid lint/render | `npm i -g @mermaid-js/mermaid-cli` |
| pmd / ArchUnit / Packwerk | Architecture rule enforcement (tied to design review) | per-language |
| openatam (community) | ATAM utility-tree templating | search GitHub for "atam template" |
| WebSearch (Claude) | Tech-evaluation evidence gathering | built into Claude Code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Pull Requests | SaaS | Yes | Native review workflow for ADRs-as-code |
| Backstage TechDocs | OSS | Yes | Markdown-first ADR/C4 publishing |
| Linear / Jira | SaaS | Partial | Track migration tasks; APIs are agent-drivable |
| Confluence | SaaS | Avoid | Editor is hostile to agents; export+import is lossy |
| IcePanel | SaaS | Partial | Good design review UI, JSON export feeds agents |
| Sourcegraph Cody / Glean | SaaS | Yes | Code-context for design reviews; cite real files |

## Templates & scripts
See `templates.md` for system-design, ADR, ATAM utility tree, and migration templates. Inline helper to drive a per-PR architecture review check:

```bash
#!/usr/bin/env bash
# arch-review-check.sh — fail PR if architecture-impacting paths change without an ADR update.
set -euo pipefail
BASE="${1:-origin/main}"
WATCHED='^(infra|deploy|services/[^/]+/(api|domain)|docs/architecture)/'
CHANGED=$(git diff --name-only "$BASE"...HEAD)
if echo "$CHANGED" | grep -E "$WATCHED" > /dev/null; then
  if ! echo "$CHANGED" | grep -E '^docs/architecture/decisions/[0-9]+-' > /dev/null; then
    echo "ARCH-REVIEW: architecture-impacting paths changed without an ADR." >&2
    echo "Add an ADR under docs/architecture/decisions/ (or update an existing one)." >&2
    exit 1
  fi
fi
echo "ARCH-REVIEW: ok"
```

## Best practices
- Pick exactly one workflow per artifact type; stop the team from inventing a new review form per project.
- For tech evaluation, force the agent to cite at least one source per claim (release notes, benchmarks). Anything uncited is a hallucination candidate.
- Time-box ADR readouts (10–15 min reading + 30 min discussion) — the workflow only works with discipline.
- Always run an after-action review on the top-3 ADRs at 30 and 90 days; feed findings back into the next round of evaluations.
- For migration workflows, require the agent to draft the *rollback plan* before the cutover plan.
- Convert each workflow into a CI check or PR template so it self-enforces without process police.

## AI-agent gotchas
- Review workflows degrade to rubber-stamping unless you give the critic a separate persona and adversarial prompt.
- Agents tend to emit one giant "do everything" plan; force decomposition into the canonical phases (CLARIFY → ESTIMATE → DESIGN → DEEP DIVE → TRADE-OFFS → DOCUMENT) and check each step.
- ATAM utility trees from LLMs are usually too uniform — every leaf marked "high importance, high difficulty." Require explicit ranking distribution.
- Migration plans skip backfill, dual-write, and feature-flag cutover. Inject those as required headings in the template.
- Human-in-loop gates: ADR acceptance, evaluation outcome sign-off, migration go/no-go. Wire these as approvals, not comments.

## References
- https://adr.github.io/
- https://www.sei.cmu.edu/our-work/projects/display.cfm?customel_datapageid_4050=21407
- https://c4model.com/
- https://martinfowler.com/articles/lightweight-architecture.html
- https://github.com/joelparkerhenderson/architecture-decision-record
- https://arc42.org/
