# Agent Integration — Product Operations (PM-angle)

This file is the PM-side complement to the standalone Product Ops methodology
(`../../product-operations/product-operations/agent-integration.md`).
That file documents how to *run* a Product Ops function with agents.
This one answers a different question: when a Product Ops function (human or
agentic) already exists, **what does the PM delegate to it, what does the PM
still own, and how do PM-side subagents talk to Product Ops automations
without duplicating work or undermining authority?**

The 2026 baseline assumed: 96% of orgs have a Product Ops function, 50% report
to the CPO. The PM is therefore a *consumer* and *partner* of Product Ops —
not its operator. Any agent flow that violates that assumption (PMs running
their own private rollups in parallel, PMs writing back to system-of-record
without going through the Product Ops pipeline) reproduces the dysfunction
the function exists to remove.

## When to use

- A PM is onboarding into an org with an existing Product Ops function and
  needs an explicit RACI between their own subagents and Product Ops
  automations (who writes to Linear, who owns the KPI dictionary, who
  publishes the status pack).
- Multiple PMs in the org request inconsistent artefacts (different roadmap
  formats, different "shipped" definitions). The fix is to route their agents
  through the Product Ops canonical store, not to let each PM build their own.
- A PM is preparing a board / exec / portfolio review and needs to consume
  Product Ops outputs (rollups, heatmaps, capacity reports) instead of
  re-deriving them — without losing the narrative layer the PM still owns.
- A PM proposes a new ceremony, template, or KPI; the methodology says
  *Product Ops* ships the converged template org-wide, so the PM's
  brainstorm subagent must hand off the converged output to Product Ops
  rather than publishing unilaterally.
- A PM receives a Product Ops insight ("feature X is at risk", "KPI Y
  regressed") and needs to convert it into a discovery, scoping, or kill
  decision — i.e. PM owns the *response*, Product Ops owns the *signal*.

## When NOT to use

- Solopreneur / single-PM team with no Product Ops function. Use the solo
  tier `solo/product/product-operations/` skills directly; there is no
  partnership boundary to model.
- Org has nominally appointed a "Product Ops" person but the charter is
  undefined (the methodology's documented top challenge: role clarity).
  Drive `faion-brainstorm` on the charter first; do not bolt agents onto an
  ambiguous boundary.
- Strategic decisions: pricing, positioning, kill/scale, hiring an engineer
  onto a squad. The PM owns these. Product Ops cannot make them, and a PM
  must not delegate them to a Product Ops automation just because the data
  is there.
- Customer-facing comms (release notes prose, customer interviews,
  positioning copy). Product Ops can schedule and distribute, the PM owns
  the content.
- During the first 30 days of a new product where the workflow is unstable.
  Codifying a PM-vs-ProductOps RACI around chaos locks in the wrong shape;
  let the workflow stabilise first, then carve the boundary.

## Where it fails / limitations

- **Shadow rollups.** PM subagents that read Linear/Jira/Productboard
  directly (instead of the Product Ops canonical store) produce numbers that
  diverge from the org-published figures. The PM ships a deck, Product Ops
  ships a different deck, trust collapses. Always read from the canonical
  store.
- **Charter drift.** When a PM's own subagent gets good at status packs, the
  PM is tempted to skip Product Ops. Six months later the org has two
  parallel rollup systems and no one owns reconciliation. Hard rule:
  PM-side agents read, Product Ops agents write.
- **Decision laundering.** "Product Ops said the feature is at risk, so we
  killed it" — this offloads accountability from the PM to a function that
  has no decision rights. Agents must label every Product Ops output as
  *signal*, never *recommendation-to-kill*.
- **Template fragmentation.** PM uses `faion-brainstorm` to design a new
  spec template, ships it inside their squad, never hands it to Product Ops.
  Three squads later there are three spec templates. Hand-off step is
  mandatory.
- **Maturity mismatch.** PM asks for AI-driven predictive capacity, Product
  Ops is at Level 1 (process docs only). The PM-side agent must detect and
  refuse the request, pointing to the maturity gap, not silently produce a
  fragile prediction.
- **OKR-from-Product-Ops trap.** Product Ops can roll up OKR progress; it
  cannot author meaningful OKRs. PMs who ask their subagent to "use Product
  Ops to write our OKRs" get cargo-culted documents.

## Agentic workflow

Model the PM and Product Ops as two distinct agent surfaces with a contract
between them. Product Ops owns the *canonical store* (Postgres / Notion DB /
dbt model) and the *write-back automations*. The PM's subagents are pure
*readers* of that store plus *authors* of narrative artefacts (specs,
discovery memos, decision logs). Hand-offs are explicit: a PM-side draft
that needs to land in a system-of-record is posted to a Product Ops queue
(GitHub PR, Slack thread, Notion draft DB) where the Product Ops agent
applies the write. The PM never bypasses that queue. Inside this repo the
boundary maps cleanly to `faion-product-manager` (PM domain agent, this
skill) consuming outputs from a `faion-product-ops` orchestrator described
in the sibling methodology, with `faion-brainstorm` and `faion-sdd` as PM
downstream tools.

### Recommended subagents

- `faion-product-manager` — Owner of this skill. Reads the Product Ops
  canonical store; produces specs, decision memos, prioritisation tables;
  never writes to Linear / Jira / Productboard directly.
- `faion-product-ops` (sibling, `pro/product/product-operations/`) — Sole
  authority for canonical-store reads and system-of-record writes. PM agents
  call it as a service, not a peer.
- `faion-brainstorm` — PM uses diverge-converge cycles for new ceremonies,
  templates, KPI definitions. Output is a *converged proposal*, handed to
  Product Ops to ship org-wide. Never publishes unilaterally.
- `faion-research-agent` — When a Product Ops insight ("KPI dropped 12%")
  needs causal investigation that is out of scope for Product Ops itself
  (competitor moves, market shifts), the PM delegates to research.
- `faion-sdd` / `faion-feature-executor` — Downstream of a PM decision: when
  the PM accepts a Product Ops "missing spec" warning, the PM (not Product
  Ops) spawns the SDD task to author it.
- `faion-improver` — Quarterly: PM runs improver over the *PM/ProductOps
  contract* to detect drift (PM-side shadow rollups, Product Ops automations
  no PM reads, dropped hand-offs).

### Prompt pattern

PM weekly review (read-only consumption of Product Ops outputs):

```
Read /ops-store/rollup-latest.md and /ops-store/portfolio-heatmap.json
(produced by faion-product-ops). Do not query Linear/Jira/Productboard
directly. For each at-risk feature in my portfolio, produce: 1) PM call
(continue/pivot/kill), 2) discovery gap, 3) decision owner. If the rollup
is older than 48h, stop and request a Product Ops refresh — do not
substitute a fresh scrape.
```

PM proposes a new artefact (hand-off into Product Ops):

```
I want a new "experiment readiness" template. Run faion-brainstorm in
diverge-converge mode (3 angles, 1 converge). Output a single draft to
proposals/experiment-readiness.md. Then post to the Product Ops intake
queue (Slack #product-ops-intake) with subject "template proposal" and
stop. Do not commit to /templates/ — that is Product Ops's write.
```

PM responding to a Product Ops signal (signal vs decision separation):

```
Product Ops flagged feature F-123 as at-risk (slip > 5d, 2 blocked
dependencies). Treat this as signal, not recommendation. Pull the spec,
the last 3 customer interviews, and the metric. Produce a one-page PM
decision memo (continue/pivot/kill) with rationale. Tag the memo
@<pm-handle>; do not change feature state in Productboard.
```

## CLI tools

The PM-side tooling deliberately overlaps minimally with Product Ops's
write-side stack. PM agents read; they should not need write CLIs at all.

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `notion-cli` / `@notionhq/client` (read-only token) | Read canonical store and Product Ops rollups | https://developers.notion.com |
| Postgres `psql` (read-only role) | Query the dbt-modelled metrics layer Product Ops publishes | https://www.postgresql.org/docs/current/app-psql.html |
| `gh` | Read roadmap PRs, comment on Product Ops template proposals | https://cli.github.com |
| `slack-cli` (read scope) | Subscribe to `#product-ops-rollups`, post hand-off requests | https://api.slack.com/automation/cli |
| `mermaid-cli` (`mmdc`) | Render decision-tree / dependency diagrams in PM memos | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Convert PM markdown memos to PDF / docx for stakeholder packs | https://pandoc.org |
| `jq` / `yq` | Parse Product Ops JSON/YAML outputs in PM scripts | https://stedolan.github.io/jq/ |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes for PM |
|---------|-----------------|-----------------|-------|
| Notion (canonical store, RO) | SaaS | Yes — REST | PM reads Product Ops DBs; never edits structure |
| Linear | SaaS | Yes — GraphQL | Read-only token for PM agents; writes via Product Ops |
| Jira Cloud | SaaS | Yes — REST v3 | Same: reads only; ticket creation through Product Ops |
| Productboard | SaaS | Yes — REST | Source-of-truth for features; PM consumes the rolled-up view |
| PostHog / Amplitude / Mixpanel | SaaS / OSS | Yes — REST | PM reads pre-modelled metrics, not raw events |
| dbt Cloud / Lightdash / Metabase | OSS / SaaS | Yes — REST | The contract surface: PM dashboards live here |
| Slack | SaaS | Yes — Bolt | Hand-off channel + digest distribution |
| Loom / Granola / Otter | SaaS | Partial | PM artefacts (interview clips, meeting recaps) — outside Product Ops scope |
| Confluence / Notion (narrative) | SaaS | Yes — REST | Specs, decision logs, discovery memos — owned by PM, not Product Ops |
| n8n | OSS | Yes | Workspace runs an n8n instance; PM uses it for personal flows that do not touch system-of-record |

## Templates & scripts

PM-side tooling is intentionally thin. Most logic belongs in Product Ops.
The one script the PM needs is a *contract checker* that flags when a PM
subagent is about to violate the boundary.

```bash
#!/usr/bin/env bash
# pm-ops-contract-check.sh - refuse PM-side write attempts to system-of-record.
# Wrap PM agent invocations: if the planned action touches a write surface
# owned by Product Ops, exit non-zero and instruct the agent to use the
# hand-off queue instead.
set -euo pipefail
ACTION="${1:?usage: pm-ops-contract-check.sh <planned-action.json>}"
WRITE_OWNED_BY_OPS='linear|jira|productboard|aha|notion-canonical|dbt-models|kpi-dictionary'
if jq -e --arg p "$WRITE_OWNED_BY_OPS" '
  .calls[] | select(.op=="write") | .target | test($p)
' "$ACTION" >/dev/null; then
  echo "BLOCKED: PM agent attempted Product-Ops-owned write."
  echo "Hand-off path: post to #product-ops-intake or open PR in ops/templates."
  exit 2
fi
echo "OK: PM agent stays within read + narrative scope."
```

PM/ProductOps RACI table to drop into onboarding docs:

| Activity | PM | Product Ops |
|---|---|---|
| Author spec / discovery memo / decision log | R, A | C |
| Define a KPI | R | A (publishes to dictionary) |
| Run weekly portfolio rollup | I | R, A |
| Set roadmap entry status in Productboard | C | R, A |
| Ship a new template org-wide | C | R, A |
| Decide continue / pivot / kill | R, A | I (provides signal) |
| Schedule a release | C | R, A |
| Stakeholder pack distribution | C (signs off content) | R, A |

## Best practices

- **Read-only credentials for PM agents.** Issue Linear/Jira/Productboard
  tokens with read scope only. The contract is enforced by the auth layer,
  not by prompt instructions.
- **Reference the canonical store by URL, not by query.** PM memos cite
  `/ops-store/rollup-2026-04-21.md`, not "I queried Linear and found...".
  Makes hand-offs auditable and kills shadow rollups at the document layer.
- **Label every Product Ops output as signal.** PM-side templates have a
  fixed header: "Source: Product Ops rollup, freshness <ts>. PM decision
  pending below."
- **Hand-off, do not write.** PM-side brainstorms produce *proposals*; the
  publish step lives in Product Ops. This is the single most important rule
  and the easiest to break.
- **Quarterly contract audit.** Run `faion-improver` against PM-side flows
  with the explicit question: "Where am I querying system-of-record
  directly? Where is Product Ops authoring narrative I should own?"
- **Maturity-gate PM asks.** Before requesting an AI-predictive capacity
  report from Product Ops, the PM agent checks the documented Product Ops
  maturity level; if Level 1, refuse the request and propose a Level 1
  alternative.
- **Distinguish narrative from numbers.** PM owns prose (specs, memos,
  positioning); Product Ops owns numbers (KPIs, rollups, capacity).
  Composition lives in PM artefacts; origination of either lives nowhere
  else.
- **Name a PM-side consumer for every Product Ops automation.** If a
  rollup has no PM reader, it is Product Ops's debt — flag it back, do not
  silently pretend to use it.

## AI-agent gotchas

- **Auto-promotion to writer.** A PM agent that has read access to Linear
  one day gets a write token "for convenience" and starts editing tickets.
  Audit token scopes per agent in CI; refuse new writers without a Product
  Ops co-sign.
- **Stale rollup as fresh data.** PM agent reads `rollup-latest.md` whose
  `last_updated` is 5 days old, presents it in an exec deck. Always read
  the freshness header and refuse to compose stakeholder content on stale
  inputs.
- **Recommendation laundering.** Agent says "Product Ops recommends
  killing F-123." Product Ops does not recommend; it reports. Strip any
  "Product Ops recommends" language at the prompt level.
- **Cargo-cult OKRs from rollups.** LLM sees "feature X regressed by 12%"
  and proposes an OKR "improve X by 20%." OKRs need strategic context the
  rollup does not contain. Require human sign-off on every PM-authored OKR.
- **Cross-system ID drift in PM artefacts.** PM memo cites "feature 123"
  ambiguously across Productboard / Jira / Linear IDs. Always resolve
  through the canonical mapping table Product Ops maintains.
- **Bypassed hand-off queue.** The PM agent posts a "draft" directly into
  Notion canonical pages because the hand-off queue felt like ceremony.
  Lock the queue at the API level; "ceremony" is the contract.
- **Privacy contamination.** PM pulls customer interview transcripts into
  the same context as Product Ops rollups; PII leaks into the metrics
  store. Keep PM narrative store and Product Ops metrics store on
  separate auth domains.
- **Charter ambiguity coded into prompts.** A prompt that says "use Product
  Ops or just query the data yourself" trains the agent to bypass the
  function. Prompts must be unambiguous: read from canonical store, hand
  off to Product Ops, full stop.
- **Maturity-skip silence.** Agent silently produces a Level 3 predictive
  output even though Product Ops is at Level 1. Make the maturity check a
  hard gate, not a soft warning.

## References

- Methodology README: `./README.md`
- Sibling Product Ops (operator-side): `../../product-operations/product-operations/agent-integration.md`
- Solo-tier counterpart: `../../../../solo/product/product-operations/`
- Product Manager skill: `../CLAUDE.md`
- Brainstorm skill: `../../../../../faion-brainstorm/`
- Improver skill: `../../../../../faion-improver/`
- Product Operations Institute: https://productoperations.com
- "State of Product Ops" (Productboard, annual): https://www.productboard.com/research/state-of-product-ops/
- Marty Cagan on PM vs Product Ops boundary: https://www.svpg.com/product-ops/
- Mind the Product (Product Ops tag): https://www.mindtheproduct.com/tag/product-ops/
- Lenny Rachitsky on the PM/Ops partnership: https://www.lennysnewsletter.com/p/product-ops
