# Agent Integration — Blurred Roles and Team Evolution (PM lens)

## When to use

- Redefining the PM job description in a 2026 AI-augmented team where Claude subagents already handle research, eval design, copy, and prototype code that PMs used to broker.
- Deciding which PM activities to keep in a human DRI, which to delegate to a `faion-mlp-agent` / `faion-mvp-scope-analyzer-agent`, and which to share with designers or staff engineers.
- Inverting the PM:Engineer ratio (Andrew Ng's "2 PMs : 1 Engineer") in teams whose engineers ship via Claude Code — the new bottleneck is discovery, evals, and prioritization, all PM work.
- Drafting hiring scorecards or growth plans for "AI-era PMs": SQL fluency, eval authoring, model-cost awareness, distribution intuition, design literacy.
- Resolving the PM-vs-X identity collisions (PM vs designer on UX flows, PM vs growth on activation, PM vs engineer on technical scoping) that surface when each role gains agent leverage.

## When NOT to use

- A solopreneur founder team — there is no PM/X overlap to manage; you are the Venn. Use `product-operations/blurred-roles-team-evolution` instead, which is framed for that scope.
- Regulated product surfaces (HIPAA, SOX, PCI, medical-device 510k) where PM-vs-QA / PM-vs-compliance separation is auditable. Document the regulated surface as a non-blurred zone explicitly.
- Performance reviews or leveling discussions. The Venn model is an operating-model lens, not a competency rubric — using it to justify promotion / PIP is misuse.
- Teams under heavy delivery pressure mid-sprint. Role-restructuring is a quiet-quarter activity; mixing it into delivery cadence corrodes both.

## Where it fails / limitations

- Methodology source content is one page (skill table + Andrew Ng quote + Venn metaphor). It describes a target state, not a transition path — agents will hallucinate process if you ask "implement the methodology".
- "PM speaks design / understands data / knows AI basics" is a one-sided expectation list. Without the matching designer/data/eng-side blurring, the PM becomes a permanent integrator and burns out.
- The 2:1 PM:Engineer ratio is one observation from one operator; treat as a hypothesis per team, not a benchmark. Agents will cite it as if it's industry data — it isn't.
- Blurring without a "decision DRI per overlap zone" creates accountability vacuum: the PM-vs-designer overlap becomes a place where decisions stall instead of accelerate.
- Skill-blurring expectations become covert hiring filters that shut out specialists (deep researcher, deep platform PM, deep growth PM); agents trained on these JDs will reject candidates the team actually needs.

## Agentic workflow

For each PM-vs-X overlap zone (PM/design, PM/growth, PM/engineer, PM/data, PM/eval), name a single human DRI and a Claude subagent that runs the parallel disciplinary lens. The PM owns the converged decision artifact (PRD, eval set, growth brief). Use `faion-brainstorm` to fan out persona-flavored agents (PM-agent, designer-agent, growth-agent, eng-agent) on the same problem, then converge in a PM-DRI session. For role-evolution audits, run `faion-improver` to compare current responsibilities against a target Venn and emit SDD tasks. Never let an agent persona own a decision in an overlap zone — agents propose, the human PM decides.

### Recommended subagents

- `faion-mlp-agent` — PM-owned MVP/MLP shaping; absorbs the "PM speaks design + tracks metrics + understands data" expectation by running its 5 modes (analyze, find-gaps, propose, update, plan) and emitting structured artifacts the PM converges on.
- `faion-mvp-scope-analyzer-agent` — PM-owned competitor + scope analysis; replaces the "PM goes asks the analyst" handoff that the methodology says is dead.
- `faion-brainstorm` — diverge across role personas (PM, designer, growth, eng, data) on a shared problem; the PM is the converger, not a participant in diverge.
- `faion-improver` — quarterly audit of "what is the PM currently doing vs. the Venn target"; emits gap list and SDD tasks.
- `faion-sdd-executor-agent` — execute the PM-restructure tasks (rewriting JDs, RACI updates, skill plans, agent-allowlist edits) under quality gates.
- `researcher` (knowledge skill) — pull external benchmarks (PM:Eng ratios, PM JDs at AI-native companies) when the PM is calibrating their own role.

### Prompt pattern

```
You are <role>-agent (designer | growth | eng | data) reviewing PRD draft
at <path>. The PM is the DRI. Produce only your discipline's lens:
risks, missing inputs, conflicts with your role's metrics. Do NOT
synthesize across roles; do NOT propose final scope. Output JSON with
keys: risks[], missing_inputs[], conflicts[], suggested_questions[].
```

```
You are PM-DRI for product P. Read the parallel disciplinary lenses
in <dir>/lens-*.json (designer, growth, eng, data). Converge into a
single PRD: explicit decisions per overlap zone, explicit "deferred to
specialist" markers where you choose not to absorb the discipline.
Emit PRD.md plus decisions.csv (zone, decision, rationale, owner).
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` + CODEOWNERS | Where the PM-vs-eng line currently sits in code; PRs touching files PM owns are the overlap signal | `gh auth login`; https://cli.github.com |
| `linear` MCP / `linear-cli` | Pull PM ticket distribution: ratio of discovery vs. delivery vs. handoff tickets per PM | https://github.com/evangelion-ui/linear-cli |
| `dbt` / `duckdb` | The "PM understands data deeply" expectation operationalized: PM writes SQL or dbt models against product analytics | https://docs.getdbt.com ; https://duckdb.org |
| `figma` MCP | "PM speaks design fluently" — read Figma comments and frames programmatically; agent generates PM annotations | https://github.com/GLips/Figma-Context-MCP |
| `posthog` / `amplitude` CLI / API | PM-owned funnel/retention queries the PM used to ask the analyst for | https://posthog.com/docs/api ; https://developers.amplitude.com |
| `claude` (Claude Code) | Drive the persona-lens agents non-interactively (`claude -p "..."`) for batch role audits and JD rewrites | https://docs.anthropic.com/en/docs/claude-code |
| `notion` MCP | Sync PM JD, RACI per overlap zone, growth plan into the team wiki | https://github.com/makenotion/notion-mcp-server |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes (REST + MCP) | Best signal for PM ticket-type distribution; query labels/assignees to derive current PM scope |
| Productboard | SaaS | Partial (REST) | PM-owned product+metric overlap; useful when PM absorbs analyst role |
| PostHog / Amplitude / Mixpanel | SaaS / OSS (PostHog) | Yes (REST) | Direct PM access kills the "PM asks analyst" handoff; agents draft funnels for PM review |
| Figma | SaaS | Yes (REST + MCP) | PM-vs-designer overlap; agents read Figma comments and surface PM action items |
| Maze / UserTesting | SaaS | Partial (REST) | PM-owned discovery; agents schedule, transcript, and synthesize tests |
| Reforge / Lenny's "PM AI" | SaaS | No | Curriculum for the new PM skillset; agent role is summarize + map to internal gaps |
| Eval platforms (Braintrust, Langfuse, Humanloop) | SaaS | Yes (REST/SDK) | "PM authors evals" expectation made operational; agents draft eval sets, PM approves |
| Lattice / 15Five | SaaS | Partial (REST, gated) | Skill-growth tracking for the PM's T-shape; writes usually need human approval |
| GitHub Projects | SaaS | Yes (`gh` + GraphQL) | Free Linear substitute; CODEOWNERS file is the most concrete PM-vs-eng boundary |

## Templates & scripts

Inline a small audit script that quantifies PM scope drift: ratio of discovery tickets to delivery tickets per PM, fed into the role-Venn audit prompt.

```bash
#!/usr/bin/env bash
# pm-scope-audit.sh — emit PM ticket-type distribution from Linear.
# Usage: GRAPHQL_TOKEN=... ./pm-scope-audit.sh <team-key> <since-iso>
# Output: TSV of pm_email, discovery_tickets, delivery_tickets, handoff_tickets
set -euo pipefail
team="${1:?team-key}"
since="${2:?since-iso e.g. 2026-01-01}"
: "${GRAPHQL_TOKEN:?Linear API key}"
q='{"query":"query($t:String!,$s:DateTimeOrDuration!){issues(filter:{team:{key:{eq:$t}},updatedAt:{gt:$s}}){nodes{assignee{email} labels{nodes{name}}}}}","variables":{"t":"'"$team"'","s":"'"$since"'"}}'
curl -sS -X POST https://api.linear.app/graphql \
  -H "Authorization: $GRAPHQL_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$q" \
  | jq -r '
    .data.issues.nodes[]
    | select(.assignee.email)
    | {email: .assignee.email,
       kind: ([.labels.nodes[].name] | map(ascii_downcase)
              | if any(. == "discovery") then "discovery"
                elif any(. == "handoff" or . == "spec") then "handoff"
                else "delivery" end)}
    | [.email, .kind] | @tsv
  ' \
  | sort | uniq -c \
  | awk '{print $2"\t"$3"\t"$1}' \
  | sort
# Read result: a PM at <20% discovery is a delivery-broker (pre-blurring);
# >50% discovery + nonzero handoff is the AI-era target shape; pure handoff
# is the role the methodology says is dying. Feed into faion-improver.
```

## Best practices

- Make every PM-vs-X overlap zone have exactly one PM DRI; agents fill the zone, but only the human PM closes decisions. Document this in the PM JD, not in tribal knowledge.
- Pair every "PM speaks design" expectation with a designer-side blurring ("designer tracks activation metrics, owns one funnel"). One-sided blurring breeds resentment and burns out the PM.
- When inverting the PM:Engineer ratio, only hire/grow PMs who can write SQL, author evals, and read a model card — otherwise the ratio just creates more meetings and slower decisions.
- Write the PM JD as "primary lens (product strategy) + 3 fluencies (data, design, AI) + 1 specialist depth (e.g., growth or platform)" rather than a flat skill list. Forces explicit T-shape and prevents shallow generalism.
- Use commit-author + Linear-assignee distribution as the truth signal for current PM scope. Self-reported PM scope in surveys is systematically wrong by ~30%; agents that audit from prose JDs replicate that error.
- Keep one "depth specialist" PM per critical surface (security, accessibility, ML eval, monetization). Full-blurring is an anti-pattern in deep domains; the specialist is the audit backstop.
- Re-audit PM scope quarterly with `faion-improver`. Blurred PM roles drift back to delivery-brokering under deadline pressure; the audit is the forcing function.
- Distinguish "PM absorbs the discipline" (PM does it themselves with agents) from "PM gains fluency" (PM can review what an agent or specialist produced). Conflating them kills PMs.

## AI-agent gotchas

- Parallel role-persona agents on the same PRD produce contradictions; without a human PM-DRI to converge, the PRD ships the loudest agent's recommendation. Always attach a converge step owned by the PM.
- An agent given the PM JD plus repo access will silently rewrite code (PM-vs-engineer overlap collapses). Constrain via tool allow-lists per persona — `faion-mvp-scope-analyzer-agent` should not have `Edit` on source files.
- Agent-driven PM evaluations ("rate this PM's data fluency from their PRDs") are noisy and biased toward verbose writers. Use as a discussion seed, never as a performance input.
- The "2 PMs : 1 Engineer" inversion holds only when the engineer is heavily AI-augmented. If you measure on baseline engineering throughput, you'll over-hire PMs and under-build. Track agent-assisted velocity separately before changing the ratio.
- Cross-role agent handoffs leak proprietary context (the data-agent surfaces customer PII into a designer-agent prompt). Run a `password-scrubber-agent` style filter on inter-agent handoffs that involve PM-owned customer data.
- Agents asked to "redefine the PM role" without constraints will produce maximalist JDs that no human can actually fill. Constrain prompts: "primary lens + max 3 fluencies + 1 specialist depth + explicit non-goals".
- Human-in-the-loop checkpoints: (a) PM-DRI assignment per overlap zone, (b) approval of any PM JD rewrite generated by an agent, (c) explicit sign-off on the PM:Engineer ratio change before any hiring action, (d) PM review of every eval set drafted by an agent.

## References

- Andrew Ng, "AI is changing the role of the PM" (Sequoia AI Ascent 2024 talk).
- Marty Cagan, "Transformed: Moving to the Product Operating Model" (2024) — chapter on cross-functional teams and the PM role.
- Lenny Rachitsky newsletter, "The new PM skillset for the AI era" (2024–2025 issues).
- Reforge, "AI for PMs" / "Product Strategy in the Age of AI" course outlines.
- Silicon Valley Product Group, "The Product Operating Model" — https://www.svpg.com/
- Anthropic, Claude Code subagents docs — https://docs.anthropic.com/en/docs/claude-code/sub-agents
- Sister methodology (operations lens): `pro/product/product-operations/blurred-roles-team-evolution/agent-integration.md`
