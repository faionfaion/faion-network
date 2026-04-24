# Agent Integration — Blurred Roles and Team Evolution

## When to use

- Designing or auditing the role split for an AI-augmented product team where one human owns multiple disciplines (PM + design + data) backed by Claude subagents.
- Migrating a relay-race "spec → design → engineering → QA" workflow into a Venn-diagram model where each human or agent owns overlapping responsibilities.
- Framing solopreneur staffing decisions: which roles to absorb personally, which to delegate to agents, which to keep as a paid human.
- Calibrating PM:Engineer ratios when agent throughput shifts the bottleneck from coding to discovery, evals, and prioritization (Andrew Ng's "2 PMs : 1 Engineer" inversion).
- Writing role descriptions, hiring scorecards, or skill-growth plans that explicitly assume cross-disciplinary fluency rather than handoffs.

## When NOT to use

- Heavily regulated environments (medical devices, aerospace, finance audit) where role separation is a compliance requirement (e.g., SOX, IEC 62304, FAA DO-178C). Blurring violates the audit trail.
- Large-scale orgs (>50 engineers) with established RACI — the methodology is descriptive of a future state, not a refactor playbook.
- Performance-management decisions: this is an operating-model lens, not a competency framework. Don't use it to justify firing or leveling.
- Day-to-day task assignment within a single sprint — too abstract; use a normal queue/board.

## Where it fails / limitations

- Methodology is a single conceptual page (Andrew Ng quote + Venn metaphor + skill table). Zero implementation detail, no checklist content, no examples — overstating it as a "process" leads to cargo-culting.
- The 2:1 PM:Engineer ratio is one observation, not a benchmark; treat as a hypothesis per team, not a target.
- Blurred ownership creates accountability gaps. Without a "decision DRI" convention, decisions stall in the overlap zone.
- Cross-functional fluency expectations can become unspoken hiring filters that discriminate against specialists; keep an explicit "depth role" alongside the T-shape.
- Agents amplify the failure mode: if four subagents all "join discovery", you get four contradictory PRDs and no owner.

## Agentic workflow

Treat each Venn-overlap zone (PM/design, eng/discovery, data/product) as an agent role with a single human DRI. The human owns the decision; agents run the parallel disciplinary lenses and converge on a shared artifact (PRD, eval set, GTM brief). Use `faion-brainstorm` to spin a diverge phase across role-flavored personas (PM-agent, designer-agent, data-agent, eng-agent) on the same problem, then converge. For role-evolution audits, run a one-shot `researcher`-style agent that maps current responsibilities → target Venn zones → gap list, then file SDD tasks for each gap.

### Recommended subagents

- `faion-brainstorm` — diverge/converge across role personas on a single problem (PM, designer, eng, data) to surface overlap and conflict before a human DRI decides.
- `faion-improver` — session-based audit of current role split vs. blurred-role target; emits gap list and SDD tasks.
- `faion-sdd-executor-agent` — execute the resulting role-restructuring tasks (job-spec rewrites, RACI updates, skill-plan docs) under quality gates.
- `researcher` (knowledge skill) — pull external benchmarks (PM:Eng ratios, AI-era job descriptions) when calibrating targets.

### Prompt pattern

```
You are <role>-agent for product P. Other agents are running in parallel
for the other roles. Read the shared brief at <path>. Produce only your
discipline's lens (risks, opportunities, constraints) — do not synthesize
across roles. The human DRI converges. Output: <schema>.
```

```
Audit current team T against the blurred-roles model. For each member,
list (a) primary discipline, (b) secondary fluencies, (c) overlap zones
they participate in, (d) gaps. Output a CSV plus 3 prioritized SDD tasks
to close the largest gap. Do not propose firing or restructuring.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Pull team membership, code-review patterns, who-touches-what to infer current role overlap | `gh auth login`; https://cli.github.com |
| `git shortlog -sne --since=90.days` | Surface contribution distribution per person → input to overlap analysis | built-in |
| `linear-cli` / `linear` MCP | Read assignee history per ticket type to map current role split | https://github.com/evangelion-ui/linear-cli |
| `notion-cli` / Notion MCP | Sync role docs, RACI, skill matrices into the team wiki | https://github.com/makenotion/notion-mcp-server |
| `op` (1Password CLI) | Pull access matrices (who has prod, who has analytics) — a real proxy for current role boundaries | `op-unlock`; https://developer.1password.com/docs/cli |
| `claude` (Claude Code CLI) | Drive the role-persona subagents non-interactively (`claude -p "..."`) for batch audits | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes (REST + MCP) | Best signal for who-owns-what; query assignees+labels to derive current role split |
| Notion | SaaS | Yes (MCP, REST) | Host the role-Venn doc, RACI, skill-growth plan |
| GitHub Projects | SaaS | Yes (`gh` + GraphQL) | Cheaper Linear substitute; CODEOWNERS file is the most concrete role boundary |
| Lattice / 15Five | SaaS | Partial (REST, gated) | Skill-growth tracking; agents can read goals but writes usually need human approval |
| Pavilion / Reforge | SaaS | No | Curriculum source for the new PM skillset; manual reading only |
| Maven cohorts ("AI for PMs") | SaaS | No | External upskilling; agent role is to summarize and map to internal gaps |
| HoneyDew / Productboard | SaaS | Partial (REST) | Useful when PM owns data — single source for product+metric overlap |

## Templates & scripts

Inline a small audit script that surfaces current role overlap from git + GitHub CODEOWNERS, which is the cheapest input to a blurred-roles assessment.

```bash
#!/usr/bin/env bash
# role-overlap.sh — emit per-author file-area distribution from git history.
# Usage: ./role-overlap.sh <since> <repo-root>
# Example: ./role-overlap.sh 90.days .
set -euo pipefail
since="${1:-90.days}"
root="${2:-.}"
cd "$root"
git log --since="$since" --name-only --pretty=format:'AUTHOR=%aN' \
  | awk '
    /^AUTHOR=/ { author=substr($0,8); next }
    NF {
      n=split($0,p,"/"); area=(n>1?p[1]:"root")
      key=author"\t"area; count[key]++
    }
    END { for (k in count) print count[k]"\t"k }
  ' \
  | sort -nr \
  | awk -F'\t' 'BEGIN{print "commits\tauthor\tarea"} {print $1"\t"$3"\t"$4}'
# Read result: an author touching >=3 distinct top-level areas is in
# Venn-overlap territory; an author at 1 area is a specialist. Feed
# to the brainstorm subagent as input for the role-audit prompt.
```

## Best practices

- Make every Venn-overlap zone have exactly one human DRI; agents fill the zone but never own the decision. Document this in the role doc, not in tribal knowledge.
- When inverting the PM:Eng ratio, hire/grow PMs who can run evals and write SQL — otherwise the ratio just creates more meetings.
- Write the new role description as "primary lens + 3 fluencies + 1 overlap zone owned" rather than a flat skill list. Forces explicit T-shape.
- Use commit/PR-author distribution as the truth signal for current role boundaries; self-reported role splits in surveys are systematically wrong by ~30%.
- Pair every "PM speaks design" expectation with a designer-side expectation ("understands constraints, tracks metrics"). One-sided blurring breeds resentment.
- Re-audit role overlap quarterly. Blurred roles drift back to silos under pressure; the audit is the forcing function.
- Keep one "depth specialist" per critical discipline (security, ML eval, accessibility). Full-blurring is an anti-pattern in deep domains.

## AI-agent gotchas

- Parallel role-persona agents on the same problem produce contradictions; without a human DRI to converge, the team ships the loudest agent's recommendation. Always attach a converge step.
- Agents inherit the prompt's role boundary, so a PM-agent given an engineering codebase will silently write code. Constrain via tool allow-lists per persona, not via prose instructions.
- Agent-driven skill assessments (e.g., "rate this PM on data fluency from their PRDs") are noisy and biased toward verbose writers. Use as a discussion seed, never as a performance input.
- The "2 PMs : 1 Engineer" inversion only holds when the engineer is heavily AI-augmented; if you measure on baseline engineering throughput, you'll over-hire PMs and under-build. Track agent-assisted velocity separately.
- Cross-role knowledge transfer between agents leaks proprietary context (e.g., the data-agent surfaces customer PII in a design-agent prompt). Run a `password-scrubber-agent` style filter on inter-agent handoffs.
- Human-in-the-loop checkpoints: (a) DRI assignment per overlap zone, (b) approval of any role-restructure SDD task, (c) final sign-off on hiring scorecards generated by agents.

## References

- Andrew Ng, "AI is changing the role of the PM" (Sequoia AI Ascent 2024 talk).
- Marty Cagan, "Transformed: Moving to the Product Operating Model" (2024) — chapter on cross-functional teams.
- Lenny Rachitsky newsletter, "The new PM skillset for the AI era" (2024–2025 issues).
- Reforge, "Product Strategy in the Age of AI" course outline.
- "The Product Operating Model" — Silicon Valley Product Group, https://www.svpg.com/
- Anthropic, Claude Code subagents docs — https://docs.anthropic.com/en/docs/claude-code/sub-agents
