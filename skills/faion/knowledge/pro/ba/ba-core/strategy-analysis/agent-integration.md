# Agent Integration — Strategy Analysis (BABOK KA basics)

> Scope: BABOK Knowledge Area 6 fundamentals — the four canonical tasks
> (analyze current state, define future state, assess risks, define change
> strategy), their inputs/outputs/techniques, and how an agent maps each one.
> Operational *drive* of a strategy-analysis engagement (need framing, multi-
> phase orchestration, decision-analysis hand-off) lives in the sibling
> `pro/ba/business-analyst/strategy-analysis/agent-integration.md` — read
> that for the end-to-end flow. Sibling-in-folder `strategy-basics` covers
> SWOT/PESTLE/business-model basics; `strategy-methods` covers technique
> deep dives. This file stays at the BABOK level: what each task expects
> on input, what it must produce, where agents help.

## When to use

- Onboarding a junior BA agent to the BABOK 6 layout — this is the canonical map a `routing-agent` uses to pick a sub-task.
- Audit / gap-check of a strategy artifact: cross-checking that all four KA-6 tasks were actually performed and not silently skipped.
- Generating BABOK-aligned task scaffolding (`current-state.md`, `future-state.md`, `risk-register.md`, `change-strategy.md`) before deeper work begins.
- Mapping legacy strategy documents into BABOK terminology so traceability tools (Jama, Modern Requirements, polarion) can ingest them.
- Training data / prompt grounding: when a custom agent must reason in BABOK terms, this file is the short reference.

## When NOT to use

- You already have a non-BABOK strategy framework in force (Wardley mapping, OKR-only, JTBD-driven discovery) — don't retrofit BABOK KA-6 on top; pick the operational sibling instead.
- Single-team backlog refinement — KA-6 is heavyweight; a one-page problem statement is enough.
- Pure product-discovery experiments before any commitment — use `lean-canvas` / `jobs-to-be-done` / opportunity-solution-trees first, formalize as KA-6 only after the opportunity is validated.
- Engineering-only refactors with no business-state change — KA-6's business need / future-state framing produces noise.

## Where it fails / limitations

- BABOK basics describe *what* must be produced, not *how* to drive it. Agents that stop at "produce the four artifacts" deliver paperwork without judgment. Pair with the operational sibling for orchestration.
- Inputs to each task (e.g., "business need" feeding current-state) are themselves outputs of prior elicitation; agents that take the README's linear arrow at face value skip the iteration loop.
- Risk assessment in BABOK is generic; for regulated domains use `risk-management` / `iso-31000` techniques on top.
- BABOK does not prescribe metrics — gaps written without measurable baseline + target are common (see #4 mistake in README); the agent must enforce measurability.
- Techniques list in BABOK is large (50+); naive agents pick the famous ones (SWOT, PESTLE) and ignore better-fitting ones (capability mapping, value-chain analysis, scenario modeling).
- KA-6 produces a *change strategy*, not a *plan*. Agents that confuse the two emit Gantt charts where a strategy memo is wanted.

## Agentic workflow

Treat KA-6 as four agent sub-routines, each with a strict input/output contract. A `ka6-router-agent` (sonnet) inspects which artifacts already exist for an initiative and dispatches to whichever sub-routine is missing or stale. Each sub-routine emits JSON conforming to the schemas below; the router validates schemas before storing artifacts in `.aidocs/<initiative>/strategy/`.

The four sub-routines:

1. **`current-state-agent` (opus)** — input: business need + organisational context. Output: current-state JSON across the README's six areas (process, org, tech, people, data, external) plus a stakeholder coverage matrix. Techniques applied: SWOT, PESTLE, capability mapping, value-chain analysis, business model canvas. Each area row carries `evidence_url` + `interviewed[]`.
2. **`future-state-agent` (opus)** — input: business need + current-state JSON + corporate strategy doc. Output: future-state JSON with vision (≤25 words), goals (each with metric + baseline + target + target_date), capability map deltas, process / tech / data target descriptions. A paired `future-state-validator` (sonnet) rejects any goal lacking measurability.
3. **`risk-agent` (sonnet)** — input: current + future state. Output: risk register JSON (id, description, likelihood 1-5, impact 1-5, exposure, mitigation, owner). BABOK lists risks of the *change* and risks of *not changing*; the agent must produce both registers.
4. **`change-strategy-agent` (opus)** — input: current + future + risks + gap analysis. Output: change strategy memo with N≥3 options (build / buy / partner / modify / status-quo) each with cost-band, time-band, risk-rating, capability-fit; recommended option; transition states if multi-phase. Hands off to `decision-analysis` (sibling methodology) for the weighted matrix.

Human-in-the-loop checkpoints: (a) sponsor signs the business need before current-state starts; (b) exec sponsor locks the future state before risk + strategy work; (c) decision-maker signs the change strategy; (d) BA + `faion-improver` revisit predicted vs. actual gap closure 6-12 months post-decision.

### Recommended subagents

- `faion-brainstorm` — divergence pass before `change-strategy-agent` writes options. Without it, the option set collapses to whatever vendor decks were on the desk.
- `faion-sdd-executor-agent` — once the change strategy is signed, scaffolds `.aidocs/backlog/<initiative>/` with constitution → spec → design → implementation-plan stubs that carry `strategy_id` traces back to the gap.
- `faion-feature-executor` — executes individual change-strategy tasks; each task references the originating gap + business need.
- `faion-improver` — quarterly meta-loop: rereads strategy artifacts older than 6 months, compares predictions vs. observed metrics, updates `.aidocs/memory/patterns.md` and `mistakes.md`.
- `password-scrubber-agent` — runs over every artifact before commit; strategy memos commonly leak vendor pricing, NDA-bound roadmaps, or named individuals.
- A custom `ka6-router-agent` (sonnet) — dispatches to the four sub-routines based on which artifacts are missing / stale.
- A custom `current-state-agent`, `future-state-agent`, `risk-agent`, `change-strategy-agent` (per workflow above).
- A custom `future-state-validator` (sonnet) — schema gate that rejects unmeasurable goals.
- A custom `babok-trace-agent` (haiku) — links each requirement / story downstream to its KA-6 source goal and gap, emits a `traces[]` array for traceability tools.

### Prompt pattern

KA-6 router (entry point):

```
You are a BABOK KA-6 router. Inputs:
  - initiative_id
  - .aidocs/<initiative>/strategy/ directory listing
Decide which of {current_state, future_state, risk, change_strategy}
is missing or > 90 days old. Emit JSON:
{ next_task, reason, required_inputs[], blocking_gaps[] }
Refuse to advance to a later task if an earlier one is missing.
```

Future-state validator (gate):

```
You are a future-state schema validator. For each goal in input JSON
verify presence of {metric, baseline, baseline_date, target,
target_date, owner}. Reject (status: "rejected", missing[]) if any
field absent or if baseline == target. No prose, only JSON.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Convert KA-6 artifacts (md ⇄ docx ⇄ pdf) for steering committees | https://pandoc.org/ |
| `mermaid-cli` (`mmdc`) | Render value-chain / capability maps from text | `npm i -g @mermaid-js/mermaid-cli` |
| `dot` (Graphviz) | Render gap dependency DAGs | `apt install graphviz` |
| `yq` / `jq` | Validate/transform the JSON schemas the agents emit | `apt install yq jq` |
| `git` + `pre-commit` | Versioning + scrubber hooks on `.aidocs/` strategy artifacts | already in repo |
| `ajv-cli` | JSON-Schema validation of the four KA-6 outputs | `npm i -g ajv-cli` |
| `markdownlint-cli2` | Enforce house style on memos before commit | `npm i -g markdownlint-cli2` |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Modern Requirements4DevOps | SaaS | API + Azure DevOps webhooks | KA-6 artefacts attach to ADO work-items; supports BABOK templates |
| Jama Connect | SaaS | REST API, webhooks | Multi-tier traceability from KA-6 goals to tests; agents drive via OAuth |
| Polarion ALM | SaaS / on-prem | REST API | KA-6 artifacts as work-item types; LiveDoc generation |
| Visual Paradigm | Desktop + Cloud | Limited API (XMI export) | Strong on capability/value-chain visuals; agents write XMI then import |
| Blueworks Live (IBM) | SaaS | REST API | Process-discovery side of current state |
| Bizagi Modeler | OSS desktop | XML export | BPMN current/future state; pair with `process-mining-automation` |
| Confluence + Jira | SaaS | REST API | De-facto repository for change-strategy memos; agents post markdown |
| Notion / Coda | SaaS | API | Lightweight option for solo / small-team initiatives |
| LucidChart / draw.io | SaaS / OSS | API or file IO | Value-chain, capability map visuals; draw.io is local-friendly |
| Aha! Roadmaps | SaaS | REST API | Future-state goals → roadmap items with traceability |

## Templates & scripts

The four BABOK output JSON Schemas live in `templates.md`. Below is a 40-line bash gate that validates them and blocks commit if any KA-6 artifact is malformed.

```bash
#!/usr/bin/env bash
# .aidocs/strategy/validate-ka6.sh
# Validates KA-6 JSON artifacts against schemas before commit.
set -euo pipefail
SCHEMA_DIR=".aidocs/_schemas/ka6"
ART_DIR=".aidocs/${1:?usage: validate-ka6.sh <initiative>}/strategy"
fail=0
for art in current-state future-state risk-register change-strategy; do
  f="$ART_DIR/$art.json"
  s="$SCHEMA_DIR/$art.schema.json"
  if [[ ! -f "$f" ]]; then
    echo "MISS  $art (file absent)"
    fail=1; continue
  fi
  if ! ajv validate -s "$s" -d "$f" --strict=false >/dev/null 2>&1; then
    echo "FAIL  $art schema"
    ajv validate -s "$s" -d "$f" --strict=false || true
    fail=1; continue
  fi
  if [[ "$art" == "future-state" ]]; then
    bad=$(jq '[.goals[] | select(.metric==null or .target==null or .target_date==null)] | length' "$f")
    if [[ "$bad" -gt 0 ]]; then
      echo "FAIL  future-state has $bad unmeasurable goals"
      fail=1
    fi
  fi
  echo "OK    $art"
done
exit $fail
```

Wire it into `pre-commit` (`.pre-commit-config.yaml`) as a `local` hook keyed on changes under `.aidocs/*/strategy/`.

## Best practices

- Treat the four KA-6 outputs as *first-class artifacts* with a versioned filename + change log, not as wiki pages that drift silently.
- Every goal in the future state carries `{metric, baseline, baseline_date, target, target_date, owner}`. No exceptions, no "TBD" — flag and re-elicit instead.
- Enforce a status-quo / "do nothing" option in every change strategy; agents skip it because it feels weak, but it is the leadership baseline.
- Rerun KA-6 quarterly *before* the next budget cycle; stale strategy artifacts cause budget-vs-reality drift.
- Keep the BABOK *technique* choice (SWOT vs. PESTLE vs. capability map) explicit in the artifact metadata so reviewers can challenge the choice, not just the output.
- Separate KA-6 artifacts (`.aidocs/*/strategy/`) from KA-3 artifacts (`.aidocs/*/requirements/`); blending them collapses traceability.
- Trace each requirement / story to a KA-6 goal id (`traces_to: GOAL-XX`); without this trace the requirement is orphaned and should not enter the backlog.
- Use small, fast subagents (haiku) for trace + schema validation; reserve opus for `current-state` and `change-strategy` where judgment dominates.
- Persist the agent's chain-of-decisions (not full thinking) into `.aidocs/<initiative>/strategy/decision-log.md` so 6-month review can audit reasoning.

## AI-agent gotchas

- Solution-shaped business need: agents accept "we need a CRM" as need; the framer must reject anything not outcome-shaped.
- Goal hallucination: future-state agents invent measurable-looking goals ("reduce cost 30%") with no source. Require `source_quote` + `source_doc` per goal.
- Technique laziness: SWOT / PESTLE chosen by default; agent should justify the technique choice against the question being answered.
- Risk register monoculture: only "change risks" listed, no "do-nothing risks". BABOK requires both — encode in schema.
- Strategy memo bloat: change-strategy memo grows to 30 pages; cap recommended length and keep evidence in linked artifacts.
- Stale artifact silently used: an agent picks a 14-month-old current-state and proceeds. Router must check `last_validated_at` and refuse if > 90 days.
- Trace decay: a requirement created six months after KA-6 has no `traces_to`. Pre-commit hook rejects orphan requirements.
- Schema drift: agent emits keys not in the schema (e.g., `priority_text` instead of `priority`). Validate strictly; reject + retry, do not accept loosely.
- Sponsor-signature spoofing: the agent should never set `signed_by` itself; that field is only writable by a `human-sign-agent` driven by a human checkpoint.
- Vendor-biased options: when the change-strategy-agent has access to vendor docs, options drift toward those vendors. Force `faion-brainstorm` divergence first.

## References

- BABOK Guide v3, Knowledge Area 6 — Strategy Analysis (IIBA, 2015).
- IIBA Agile Extension to the BABOK Guide v2 — strategy horizon mapping.
- Sibling: `pro/ba/business-analyst/strategy-analysis/agent-integration.md` (operational drive).
- Sibling: `pro/ba/ba-core/strategy-basics/` (SWOT / PESTLE / business model basics).
- Sibling: `pro/ba/ba-core/strategy-methods/` (technique deep-dives).
- Sibling: `pro/ba/business-analyst/decision-analysis/agent-integration.md` (option selection).
- This methodology's `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md`.
