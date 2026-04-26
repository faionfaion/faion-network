# Agent Integration — Software-Developer Methodology Index

## What this file is
This `methodologies/` directory is **not** a single methodology — it is the legacy umbrella index for the software-developer skill, listing 68 patterns across Python, JS/TS, backend languages, DevOps, and documentation. Most of those patterns now live as their own siblings under `free/dev/software-developer/<slug>/` and are individually enriched. This page is the **agent's lookup table**: pick the right sibling, do not implement directly from this index.

## When to use
- An agent has a coarse task ("implement a Django service", "scaffold a Go API", "set up Storybook") and needs to dispatch into the right concrete methodology folder.
- Building a routing/RAG layer that maps natural-language asks to the granular methodology slugs in this skill.
- Documenting which legacy "section" each methodology came from when answering "where did this rule originate?"
- Composing a multi-step plan: this index gives the canonical ordering (Python → JS → backend → DevOps → docs) for cross-cutting tasks.

## When NOT to use
- Implementing from this file directly — every snippet here is a stub. The full content lives in the sibling folder for each methodology (e.g., `django-coding-standards/README.md`).
- Treating this as a "best practices 2026" document — it's a 2024-vintage index. Pull current guidance from `best-practices-2026/README.md` instead.
- Citing it as the canonical source for any single pattern — cite the sibling.

## Where it fails / limitations
- **Stale fragments.** Many entries are 5-line skeletons; the real depth is in sibling folders. An agent that only reads this index produces shallow output.
- **Broken cross-refs.** The "Agents" table references names like `faion-code-agent`, `faion-test-agent`, `faion-devops-agent`, `faion-frontend-brainstormer-agent`, `faion-storybook-agent`, `faion-frontend-component-agent`. Most of those agents do **not** exist in this repo's `agents/` directory — only `faion-sdd-executor-agent`, `nero-sdd-executor-agent`, and `password-scrubber-agent` are present. Treat the original list as aspirational.
- **Mixed scope.** It conflates language patterns (Python type hints) with infra (Kubernetes ConfigMap), making it a poor single navigation layer for any one domain.
- **No SDD integration.** The original index predates the `.aidocs/` lifecycle; an agent following it verbatim skips spec → design → test → impl gates.
- **Section count drift.** Headline says "68 methodologies" but the sibling folder count is different (and growing); use folder listings as ground truth.

## Agentic workflow
Use this index purely as a **dispatcher**. The recommended Claude flow: (1) parse the user's task; (2) match keywords against the section index in this README; (3) read the sibling folder's `README.md`, `checklist.md`, and `agent-integration.md` (where it exists) — those are the real source of truth; (4) execute under the SDD lifecycle (`backlog/ → todo/ → in-progress/ → done/`) using `faion-sdd-executor-agent`. Never quote stub snippets from this index in production code; always hop to the sibling.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — drives the actual implementation cycle once the right methodology has been resolved.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrubs any DevOps-section snippets (Terraform state, AWS IAM, secret-management) before sharing externally.
- A purpose-built **methodology-router agent** (worth creating): takes a free-text task, returns the sibling folder slug(s) plus a confidence score; refuses to dispatch into stub-only entries.
- `nero-sdd-executor-agent` — when the dispatched task lands on a NERO repo, this agent applies the `.product/` lifecycle instead of the generic `.aidocs/`.

### Prompt pattern
Dispatch pass:
```
Given the user task: "<task>", consult the section index in
free/dev/software-developer/methodologies/README.md and return:
1. Top 3 candidate sibling slugs (full path under
   free/dev/software-developer/).
2. For each, confidence (H/M/L) and one-line rationale.
3. Recommended order if more than one applies.
4. Flag any candidate whose sibling folder has only stub content
   (≤30 lines of README) — escalate to a human or pick another.
Do NOT implement; only route.
```

Read-the-real-doc pass:
```
For the resolved sibling <slug>, load:
- README.md (full)
- checklist.md (full)
- agent-integration.md (if present)
Then proceed under the SDD lifecycle. Reject any plan that quotes
the methodologies/README.md stubs instead of the sibling content.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rg` (ripgrep) | Search slugs and section headers across the index and sibling folders | `apt install ripgrep` ; https://github.com/BurntSushi/ripgrep |
| `fd` | Locate sibling folders by slug | `apt install fd-find` ; https://github.com/sharkdp/fd |
| `glow` / `mdcat` | Render markdown in terminal for fast review | https://github.com/charmbracelet/glow |
| `tree -L 2` | Visualize sibling structure under `free/dev/software-developer/` | bundled |
| `markdownlint-cli2` | Lint stub-quality of sibling READMEs | https://github.com/DavidAnson/markdownlint-cli2 |
| `git log --diff-filter=A -- <slug>/README.md` | Determine when a methodology was added; flag old stubs | bundled with git |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS / OSS | yes | Periodic job to detect stub methodologies (<30 lines) and open issues. |
| meilisearch / typesense | OSS search | yes (HTTP API) | Index all sibling READMEs; let the dispatcher agent query semantically instead of regex. |
| Linear / GitHub Issues | SaaS issue tracker | yes | Track each stub-quality methodology as a backlog item to enrich. |
| ChromaDB / Qdrant | OSS vector DB | yes | Embed the index + siblings for RAG-style routing. |

## Templates & scripts

The directory exists, but agents need a **stub detector** to avoid acting on shallow content. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# stub-detect.sh — list sibling methodologies whose README is too thin.
# Usage: stub-detect.sh skills/faion/knowledge/free/dev/software-developer
set -euo pipefail
root="${1:?usage: stub-detect.sh PATH}"
threshold=80   # lines
echo "Methodology stubs (README <${threshold} lines):"
for d in "$root"/*/ ; do
  name=$(basename "$d")
  [ "$name" = "methodologies" ] && continue
  readme="$d/README.md"
  [ -f "$readme" ] || { echo "  $name (no README)"; continue; }
  lines=$(wc -l < "$readme")
  if [ "$lines" -lt "$threshold" ]; then
    has_ai="-"
    [ -f "$d/agent-integration.md" ] && has_ai="ai+"
    printf "  %-40s %4d lines  %s\n" "$name" "$lines" "$has_ai"
  fi
done
```

Run during a research batch to prioritize which methodologies need enrichment.

## Best practices
- **Always hop to the sibling.** This index is a map, not a manual. The depth is one folder away.
- **Verify the agent table before delegating.** The historical "Agents" rows reference names that may not exist; check `agents/` and `skills/*/agents/` first. If an agent is missing, fall back to `faion-sdd-executor-agent`.
- **Use it for ordering, not content.** The Python → JS → backend → DevOps → docs sequence is a sensible default for full-stack scaffolding tasks.
- **Pair with `best-practices-2026/`.** When this index says "Python Type Hints," cross-read the 2026 file for current syntax (`|` unions, `TypeIs`, `ReadOnly`).
- **Keep it as the routing layer.** Resist the urge to expand it back into a textbook — fragmenting into siblings was the right call.
- **Audit quarterly.** Run the stub-detector; sibling READMEs <80 lines are likely candidates for the next research batch.
- **Mark deprecations explicitly.** When a methodology is superseded (e.g., generic "React Component Pattern" → React 19 RSC patterns), edit this index to point to the replacement.

## AI-agent gotchas
- **Stub seduction.** Agents read this file's 5-line code samples and treat them as complete, producing shallow output. Always force a sibling read before generating.
- **Hallucinated agent names.** The index lists agents that don't exist (`faion-code-agent`, `faion-test-agent`, ...); LLMs cheerfully `Task(subagent_type="faion-code-agent", ...)` and the call fails at runtime. Validate against the actual `agents/` listing.
- **Outdated framework references.** "Next.js App Router" snippet here is generic; current repo guidance is in `best-practices-2026/`. Agents that quote this index ship 2-year-old patterns.
- **Section overlap.** Some siblings exist in two sections (e.g., Django patterns under "Python Ecosystem" and again under "ORM Best Practices"). Agents pick one path; reconcile via the SDD spec.
- **Wildcard "Apply best practices" instructions.** This index uses generic phrasing; reject prompts that copy "Use best practices for {language}" — force concrete sibling references.
- **DevOps section drift.** Kubernetes / Terraform snippets here predate the `pro/infra/*` skill expansion. For infra work, route to `pro/infra/` siblings instead of staying inside `software-developer`.
- **No SDD lifecycle awareness.** Agents pulled in by this index skip spec/design/test docs and dive into code. Mandate the lifecycle in the dispatcher prompt.
- **Frontend-only / backend-only blind spot.** Tasks that span both (e.g., Storybook + Next.js + Django API) require multiple sibling reads; the agent must pick a *set*, not a single slug.
- **Trusting the count.** "68 methodologies" is the historical figure; current tally differs. Use `ls` not the README's number.

## References
- Sibling skill folder: `skills/faion/knowledge/free/dev/software-developer/` (one dir per methodology — that's where the real content lives).
- Cross-reference: `skills/faion/knowledge/free/dev/software-developer/best-practices-2026/README.md` for current (2025/2026) practice.
- Skill manifest: `skills/faion/SKILL.md` and `skills/tier-manifest.json`.
- SDD lifecycle: `.aidocs/INDEX.md` at workspace root; `skills/faion-sdd-execution/`.
- Agents directory: `agents/` (only `faion-sdd-executor-agent`, `nero-sdd-executor-agent`, `password-scrubber-agent` exist as of this enrichment).
