# Agent Integration — Continuous Discovery Habits (product-planning lens)

This methodology lives in two places in the knowledge base. The `pro/research/*` copies cover the research-collection side (how to interview, transcribe, synthesize). This file is the **product-planning** lens: how Continuous Discovery feeds the Opportunity Solution Tree (OST), backlog, roadmap, and delivery decisions inside a Product Trio that is partially staffed by agents.

## When to use

- Active product with paying users where weekly discovery output must convert into roadmap moves, not slide decks. Trio rhythm: PM + Design Lead + Tech Lead, optionally simulated by a `pm-agent`, `ux-agent`, `arch-agent` triad for a solo operator.
- Quarterly OKR cycle where each Outcome at the OST root must be traced to opportunities, opportunities to assumption tests, and tests to delivered increments.
- Backlog grooming sessions where you need to reject "feature requests" framed as solutions and re-cast them as opportunities under an existing Outcome.
- Roadmap negotiation with stakeholders asking "why not feature X?" — OST gives a defensible structure: parent Outcome → competing Opportunities → ranked Assumption Tests.
- Solo/small-team setup where the human can only run 1–2 interviews/week; agents fill the gap by mining tickets, analytics, sales calls, and competitor changelogs into the same OST.
- Post-launch teams where shipped features are not moving the Outcome — Continuous Discovery loop diagnoses the broken assumption, not the build quality.

## When NOT to use

- Pre-PMF or zero-user products — no signal volume to support a weekly cadence. Use `customer-development`, `jobs-to-be-done`, `problem-validation` first.
- Crisis triage (active outage, churn cliff, security incident) — pause discovery, run focused root-cause work, resume the cadence after stabilization.
- Hardware / regulated medical / enterprise sales with 6–18 month contract cycles — interview cadence cannot be weekly; collapse to monthly or quarterly windows and rename the practice.
- Stakeholder culture demanding "validation" from a single interview — Torres explicitly rejects validation theater. Either re-educate or pick a different framework (e.g., Lean Startup-style Build-Measure-Learn) and avoid the OST vocabulary.
- Pure platform/infra teams whose users are other engineers inside the company — adapt the framework with developer-survey + DX telemetry, but the canonical Torres habits will not map cleanly.

## Where it fails / limitations

- OST rot: opportunities accumulate because agents add fast and humans prune slow. Without a monthly archival pass the tree becomes unsearchable in ~8 weeks.
- Discovery-delivery decoupling: discovery output never traces to a PR or spec. Symptom: `spec.md` files have no `opp_id` references. Fix: require opportunity ID in PR title and SDD spec front-matter.
- "Solution mining" by stakeholders: requests arrive as "add filter X". If the intake agent does not classify and reject, the OST fills with solutions disguised as opportunities.
- Trio dilution: when only the PM attends interviews, Design and Tech leads lose intuition. Agents can simulate trio coverage, but the human PM must rotate which Lead reviews synthesis, otherwise OST scoring anchors on PM bias.
- Capacity over-allocation: 15–20% discovery is the canonical number; teams under PMF pressure drop to 5% and the OST silently dies.
- Recruiting infrastructure debt: weekly interviews require a recurring source (in-app prompt, customer panel, Userinterviews API). Without it cadence collapses by week 4.
- LLM synthesis hallucination: small-N pattern claims (`N<5`) drift into "validated" language; require schema-level rejection of the word "validated" and an explicit `n_signals` ≥ threshold.
- Roadmap fatigue: 30+ opportunities make stakeholders skip the OST. Cap visible opportunities per Outcome at 7 ± 2; archive the rest under "parked".

## Agentic workflow

The product-planning loop sits **downstream** of research collection (see `pro/research/researcher/continuous-discovery/agent-integration.md` for the upstream side) and **upstream** of delivery. Agents bridge the three:

```
research-collection (upstream)  →  product-planning (this lens)  →  delivery (SDD)

   raw signals → tagged notes      ost-curator → opportunity-scorer → trio-deliberation
                                    ↓                                        ↓
                                   opportunity-solution-tree.md         spec.md (opp_id)
```

In practice on this repo: `agents/faion-sdd-executor-agent.md` consumes specs that cite opportunity IDs; the planning loop is what produces those IDs. Research subagents (researcher domain) feed the OST curator; planning subagents convert OST leaves into SDD backlog items. Use `loop` skill for cadence triggers and `schedule` skill for managed cron triggers.

### Recommended subagents

| Subagent | Model | Cadence | Inputs | Outputs |
|----------|-------|---------|--------|---------|
| `intake-classifier` | haiku | Real-time on each new request | Slack/Linear/email feature requests | Classified `opportunity` vs `solution` vs `bug` with reason |
| `ost-curator` | sonnet | Weekly | All research outputs + intake queue | Updated `opportunity-solution-tree.md`, dedupe report |
| `opportunity-scorer` | sonnet | Weekly | OST leaves, signal counts, segment data | `(reach × frequency × severity × addressability)` score table |
| `assumption-designer` | sonnet | Per opportunity selected for build | Selected opportunity, OST context | Falsifiable test plan: smoke test / fake door / prototype / Wizard of Oz / concierge |
| `trio-deliberation-agent` | opus | Bi-weekly | Top-N scored opportunities + tests | Trio decision memo: build / test / park / kill, with rationale |
| `roadmap-synth` | opus | Monthly | OST snapshot + delivered increments + outcome metrics | Roadmap delta + kill list + doubled-down list |
| `outcome-tracker` | haiku | Daily | Outcome metric source (analytics, revenue) | Outcome trend + flag if Outcome unchanged > 4 weeks despite delivery |
| `spec-linker` | haiku | On PR open | PR title, branch name, SDD spec | Verify `opp_id` reference; block PR if missing in SDD context |

Keep cheap models on collection and tagging; reserve `opus` for bi-weekly+ deliberation where reasoning across the full OST matters.

Repo subagents to wire into this flow:

- `agents/faion-sdd-executor-agent.md` — consumes specs that reference `opp_id`; this loop produces those IDs.
- `skills/faion-brainstorm/` — invoke for diverge/converge when the trio cannot agree on which opportunity to test next.
- `skills/faion-improver/` — invoke when outcome-tracker flags a stagnant Outcome (treat as a system-improvement session).
- `skills/faion/knowledge/pro/research/researcher/continuous-discovery/` — upstream sibling for the research collection angle.

### Prompt pattern

```
<role>You are the {agent}. Continuous Discovery (Torres) — product-planning lens.</role>

<inputs>
  <ost>{path to opportunity-solution-tree.md}</ost>
  <intake>{path to intake-queue.md}</intake>
  <outcomes>{path to outcomes-register.md}</outcomes>
  <delivered>{path to recent merged PRs with opp_id refs}</delivered>
  <segment_filter>{optional: limit to a user segment}</segment_filter>
</inputs>

<rules>
  - Classify every node as: outcome | opportunity | solution | assumption_test.
  - Reject inputs phrased as features ("add X"); re-prompt for the underlying need.
  - Never declare "validated"; use "tested" with explicit pass/fail criteria.
  - Score opportunities with (reach * frequency * severity * addressability), 1-5 each.
  - Cap visible opportunities per Outcome at 7; archive overflow to `parked/`.
  - Output JSON matching {schema_path}; emit a markdown digest <= 60 lines.
</rules>

<task>{cadence-specific instruction}</task>
```

Wire through Claude Agent SDK with structured outputs (Pydantic/Zod schemas enforced) — XML prompts + JSON output, per `feedback_agent_output` in NERO memory.

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` (Claude Code) | Orchestrate subagents; one slash command per cadence (`/discovery-intake`, `/discovery-score`, `/discovery-trio`) | https://docs.anthropic.com/en/docs/claude-code |
| `gh` | Pull issues/PRs as intake signal; verify `opp_id` in PR titles | `gh` CLI |
| `linear` CLI | Query feature requests + bug clusters; tag against OST nodes | https://developers.linear.app |
| `productboard` CLI / API | Sync opportunities + insights bidirectionally | https://developer.productboard.com |
| `notion` CLI | Mirror OST into team Notion; pull comments back as intake | https://developers.notion.com |
| `posthog` / `amplitude-cli` | Outcome metric trend; feeds outcome-tracker | https://posthog.com/docs/api |
| `dovetail` API | Pull tagged research notes as OST evidence | https://developers.dovetail.com |
| `cron` / `systemd-timer` | Run cadence triggers; on NERO use `loop`/`schedule` skill | systemd timers, cron |
| `gh actions` | Spec-linker: PR check that blocks merge if SDD spec lacks `opp_id` | https://docs.github.com/actions |

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Productboard | SaaS | Yes (REST + webhooks) | Native OST-shaped objects: Objectives → Drivers → Features. Insight linking is the killer feature for this lens. |
| Dovetail | SaaS | Yes (REST) | Source of evidence; OST nodes link to Dovetail tags. Magic AI summaries (2025+) reduce synth load. |
| Notion | SaaS | Yes (REST) | Cheapest OST home for solo PMs; database views handle the tree shape adequately. |
| Airtable | SaaS | Yes (REST + scripting) | Lightweight insight DB if not on Dovetail; good for opportunity scoring tables. |
| ProdPad | SaaS | Yes (REST) | OST-friendly idea management; lighter than Productboard. |
| Aha! | SaaS | Partial (REST, slow) | Roadmap-heavy; OST is bolted on, not native. Avoid if discovery-first. |
| Cycle.app | SaaS | Yes (REST + GraphQL) | 2024+ entrant; opinionated continuous-discovery UX, AI synthesis built-in. |
| Mixpanel / Amplitude / PostHog | SaaS / OSS | Yes (REST + SQL) | Outcome metric source for outcome-tracker. PostHog is self-hostable. |
| Linear | SaaS | Yes (GraphQL) | Delivery-side; require `opp_id` in issue templates. |
| Jira | SaaS | Yes (REST, verbose) | Same as Linear but heavier; agents need a custom field for `opp_id`. |
| Trello / GitHub Projects | Free / SaaS | Yes (REST) | Solo-PM fallback if Productboard is overkill. |
| ChartHop / Lattice | SaaS | Limited | OKR alignment to Outcomes — useful for outcome-tracker context. |
| Userinterviews.com | SaaS | Yes (REST) | Recruiting infra (upstream); without it the cadence dies. |
| Slack | SaaS | Yes (Webhooks + Bolt) | Trio deliberation channel; post weekly digest, capture decisions. |

## Templates & scripts

OST node schema (drop into `.aidocs/product_docs/discovery/ost-schema.json`, shared with the research-side methodology):

```json
{
  "id": "opp_xxx",
  "type": "outcome|opportunity|solution|assumption_test",
  "parent_id": "opp_yyy|null",
  "title": "string",
  "evidence": [{"source": "interview|ticket|analytics|sales|competitor", "ref": "url", "date": "ISO"}],
  "n_signals": 0,
  "score": {"reach": 1, "frequency": 1, "severity": 1, "addressability": 1, "total": 1},
  "status": "open|in_test|tested_pass|tested_fail|parked|killed|delivered",
  "linked_specs": ["feature-040-auth-refactor"],
  "last_touched": "ISO",
  "owner": "trio|pm|design|eng"
}
```

Spec-linker GitHub Actions check (`.github/workflows/spec-opp-link.yml`, ~30 lines):

```yaml
name: spec-opp-link
on: { pull_request: { types: [opened, edited, synchronize] } }
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Verify opp_id in SDD spec
        run: |
          set -euo pipefail
          spec=$(git diff --name-only origin/${{ github.base_ref }}...HEAD \
                 | grep -E '\.aidocs/.*spec\.md$' | head -1 || true)
          if [[ -z "$spec" ]]; then
            echo "No spec changed; skipping opp_id check"
            exit 0
          fi
          if ! grep -qE '^opp_id:\s*opp_[a-z0-9_]+' "$spec"; then
            echo "FAIL: $spec must declare opp_id (front-matter)."
            echo "Example:  opp_id: opp_2026q2_search_friction"
            exit 1
          fi
          echo "OK: $spec references $(grep -E '^opp_id:' "$spec")"
```

Cadence triggers (`crontab -e` or NERO `schedule` skill):

```
*/30 * * * *  claude run /discovery-intake          # classify new requests
0 9   * * 1   claude run /discovery-score           # weekly OST score
0 10  * * 2,4 claude run /discovery-trio            # bi-weekly trio deliberation
0 11  1 * *   claude run /discovery-roadmap-synth   # monthly roadmap delta
0 7   * * *   claude run /discovery-outcome-track   # daily outcome metric
```

## Best practices

- Pin one Outcome at the OST root before any opportunity work; without a measurable Outcome, agents drift into solution mining.
- Force "opportunity vs solution" classification at intake; reject anything phrased as a feature and re-prompt for the underlying need (`intake-classifier` does this automatically).
- Cap visible opportunities per Outcome at 7 ± 2; agents archive overflow to a `parked/` branch monthly. Larger trees become invisible.
- Score opportunities on `(reach × frequency × severity × addressability)`, not gut feel; agents emit numeric scores and surface week-over-week deltas.
- Every opportunity selected for build must spawn at least one falsifiable assumption test from the menu: smoke test, fake door, prototype, Wizard of Oz, concierge. "Ship and measure" is not a test.
- Tie discovery to delivery in tooling: `opp_id` in PR titles, in SDD spec front-matter, in commit trailers. Spec-linker enforces this.
- Rotate the human reviewer of synthesis output weekly; agents anchor on prior patterns, humans catch curse-of-knowledge.
- Capacity rule: discovery 15–20%, tech debt 10–15%, delivery 65–75%. Track in `outcomes-register.md`; alert if discovery drops below 10% for two consecutive weeks.
- Monthly research-reviewer pass must produce a "kill list" alongside the doubled-down list; without pruning, OSTs collapse under their own weight.
- Token budget: weekly score + trio deliberation ≤ 30k tokens, monthly roadmap synth ≤ 80k. Pre-summarize per-day with haiku, feed summaries to opus.
- Privacy: never feed raw PII transcripts to a non-zero-retention model. Use ZDR-eligible Anthropic endpoints or strip PII pre-prompt.
- Single source of truth: pick Productboard OR Dovetail OR Notion as canonical OST home; mirror to the others. Dual-write breaks evidence linking.

## AI-agent gotchas

- "Validation" is a banned word in prompts and outputs; agents trained on generic UX content drift into validation theater. Require the schema to use `tested_pass | tested_fail` only.
- Intake-classifier will pass "add filter X" through if the prompt does not include explicit examples of the rejection class — provide ≥10 few-shot rejections.
- OST-curator can dedupe aggressively and merge unrelated opportunities; require human review on any merge that crosses Outcomes.
- Opportunity-scorer hallucinates `reach` numbers when analytics fetch fails — require fetched-at timestamp + source URL in every score row, reject otherwise.
- Trio-deliberation agent will rubber-stamp the highest-scoring opportunity; force it to nominate a "devil's advocate" alternative every run.
- Roadmap-synth tends to produce optimistic delta projections; constrain to past-only attribution ("delivered X moved Outcome Y by Z%"), never future-tense promises.
- Spec-linker false negatives: PRs that touch existing specs without changing the front-matter still need `opp_id`. Lint on the file content, not the diff.
- Outcome-tracker will declare improvement on noisy daily metrics; require a 2-week rolling window minimum before status changes.
- Cron drift: long-running cadence agents accumulate state inconsistencies (orphan opportunities, stale `last_touched`). Schema-validation pass monthly is mandatory.
- Idempotency: any agent writing to Productboard / Notion / Linear via API must use idempotency keys (hash of source URL + date), or retries create duplicates.
- Curse-of-knowledge in agent prompts: agents trained on internal docs use jargon. Add a lint pass that flags any term not present in the last 20 interview transcripts.
- Subagent invocation cost: opus on every intake item burns budget; route via `intake-classifier` (haiku) and only escalate to opus for trio deliberation.
- Recruitment automation can violate panel ToS (Userinterviews weekly batch limits); rate-limit at agent level.

## References

- Teresa Torres, *Continuous Discovery Habits* (2021) — canonical text. https://www.producttalk.org/continuous-discovery-habits/
- producttalk.org/podcast — 2025–2026 episodes on AI-augmented discovery and Claude Code integration.
- Marty Cagan, *Inspired* / *Empowered* — adjacent product-trio practices and outcome-driven roadmaps.
- Itamar Gilad, *Evidence-Guided* — opportunity scoring (RICE / ICE) variants compatible with OST scoring.
- Sibling methodology (this skill): `../competitive-positioning/README.md`, `../portfolio-strategy/README.md`.
- Upstream sibling (research lens): `../../../research/researcher/continuous-discovery/agent-integration.md`.
- Upstream sibling (research lens): `../../../research/market-researcher/continuous-discovery/agent-integration.md`.
- Related methodology: `../../../research/researcher/opportunity-solution-trees/agent-integration.md`.
- Anthropic Claude Agent SDK — agents, structured outputs, scheduled triggers. https://docs.anthropic.com/en/api/agent-sdk
- Productboard "Insights → Drivers → Features" model — https://www.productboard.com
- Dovetail Magic AI synthesis (2025) — https://dovetail.com
