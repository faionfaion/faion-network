# Agent Integration — BA Strategic Partnership (ba-core)

Focus of this variant: the foundational mindset shift from order-taker to strategic
partner — the per-engagement behaviors, framing checks, and intake patterns that
establish the posture. The `business-analyst` variant covers the quarterly impact /
opportunity-mining loop; this one stays at the level of how a BA shows up to any
single request.

## When to use
- Intake of a new requirement or "can you just add X" request — agent re-frames as outcome / problem before scoping is locked.
- Re-reading an existing requirements doc, user story, or PRD to detect order-taker language and rewrite it as outcome statements with measurable KPIs.
- Onboarding a junior BA: agent runs a stance-rubric on their last 5 artifacts and produces concrete coaching deltas.
- Pre-meeting framing for stakeholder calls: agent drafts the 3 strategic questions to ask before accepting the stated requirement.
- Spec review gate before a ticket goes to engineering — block the ticket if it has no problem statement, no outcome metric, no kill criterion.

## When NOT to use
- Quarterly portfolio-level opportunity mining and value reporting — use the `business-analyst` variant of this methodology, which has the diverge/converge opportunity loop.
- Modeling work (BPMN, use-case decomposition, traceability matrices) — use `business-process-analysis`, `use-case-modeling`, `requirements-traceability`.
- Live stakeholder dialogue, executive influence, workshop facilitation — agent prepares, never speaks for the BA.
- Trivial maintenance tickets (copy edits, dependency bumps) where strategic framing is overhead.

## Where it fails / limitations
- The methodology is a posture, not a procedure. Without per-org context (OKRs, business model, P&L, customer evidence) the agent emits generic "be more strategic" platitudes.
- "Order-taker vs strategic partner" is a rubric that judges artifacts; it cannot judge trust, executive presence, or political capital — those are human-only.
- The BABOK framing assumes formal BA roles; in solo / startup contexts the BA hat is shared, and the rubric over-formalizes simple decisions.
- AI-rewritten requirement docs read like AI: balanced, hedged, and bland. A BA's strategic voice is partly stylistic — let the human keep the final pen.
- Outcome metrics demanded by the rubric require baseline data the org may not have; agent must distinguish "no metric" (red) from "metric not yet instrumented" (yellow).

## Agentic workflow
The core loop is single-pass per artifact: a `ba-stance-reviewer` subagent (Sonnet
class) ingests one requirements artifact plus a small org-context bundle (mission,
top 3 OKRs, target persona, last quarter's outcomes), scores six stance axes,
quotes order-taker language verbatim, and proposes a strategic-partner rewrite for
each finding. Output is strict JSON so a downstream `faion-sdd-execution` gate can
auto-block tickets that fail thresholds. For coaching mode, batch 5–10 artifacts
through the same subagent and aggregate the per-axis trend; pair with
`faion-improver` for monthly cadence. Human BA always reviews the rewrites before
they hit a stakeholder — strategic credibility is non-delegable.

### Recommended subagents
- `faion-sdd-executor-agent` — enforce the stance-gate as a quality check inside the SDD spec → design → tasks pipeline; reject specs missing problem / outcome / kill criterion.
- `faion-brainstorm` — use the converge phase to pick the single best strategic-partner rewrite when the reviewer emits 3 alternatives.
- `faion-improver` — monthly aggregation: trend the six stance scores per BA, surface regressions, log to `.aidocs/memory/patterns.md`.
- Custom `ba-stance-reviewer` (Sonnet) — single-artifact per-axis scoring against the rubric below; canonical schema in templates section.
- Custom `ba-intake-framer` (Haiku) — at request intake, expand a one-line ask into the 3 framing questions and a strawman outcome statement.
- `password-scrubber-agent` — scrub PII from stakeholder transcripts before they enter any of the above.

### Prompt pattern
```
ROLE: BA stance reviewer.
INPUT: <one requirement artifact> + <org_context.json: mission, okrs[3], persona, last_quarter_outcomes>.
TASK: Score 0-5 on six axes (problem_clarity, outcome_orientation, evidence_grounding,
enterprise_scope, partner_voice, kill_criterion). For each finding: quote the
order-taker phrase verbatim, classify the failure mode, propose a strategic-partner
rewrite that ties to one of the supplied OKRs.
ANTI-PATTERNS: generic "be more strategic" advice, rewrites that invent metrics not
in org_context, hedging adjectives ("better", "more aligned"), bullet soup.
OUTPUT: strict JSON per schema in templates.md.
```

```
ROLE: BA intake framer.
INPUT: <one-line stakeholder ask>.
TASK: Produce (1) the underlying problem hypothesis, (2) three framing questions to
ask the stakeholder before accepting the ask, (3) a strawman outcome statement
(KPI + delta + horizon). Refuse to produce a solution.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `llm` (Simon Willison) | One-shot stance reviews from CLI: `cat spec.md \| llm -m claude-opus-4-7 -t ba-stance` | `pip install llm llm-anthropic` |
| `aichat` | Interactive stance dialogue with role files for the reviewer / framer subagents | `cargo install aichat` |
| `gh` / `linear-cli` / `jira-cli` | Pull a ticket body for the stance reviewer; comment back the rewrite as suggestion | `gh` via package manager; `npm i -g @linear/cli`; `pip install jira-cli` |
| `pandoc` | Normalize Word/Confluence/Notion exports to markdown the agent can ingest | `apt install pandoc` |
| `markdownlint-cli2` | Enforce structure on the rewritten artifact (headings, sections present) | `npm i -g markdownlint-cli2` |
| `csvkit` / `duckdb` | Sanity-check that an outcome metric in a rewrite has a real baseline in org data | `pip install csvkit duckdb` |
| `ripgrep` | Bulk-scan a docs folder for order-taker phrases (`as requested`, `please add`, `the user wants`) before deeper review | `apt install ripgrep` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Linear | SaaS | Yes (REST + GraphQL) | Outcomes / projects schema fits the rubric; comment the rewrite back via API |
| Jira + Atlassian Intelligence | SaaS | Yes (REST + Forge) | Forge app can run the reviewer at ticket-create time as a quality gate |
| GitHub Issues + Projects | SaaS | Yes (REST + GraphQL) | Cheapest place to host stance-gate as a PR check via `gh` and Actions |
| Productboard | SaaS | Partial | Good for capturing the rewritten outcome; limited write API for nested fields |
| Notion / Confluence | SaaS | Yes (API) | Where most order-taker BRDs actually live; bulk-scan via API for stance audits |
| Dovetail | SaaS | Yes (API) | Pull verbatim user quotes for the evidence_grounding axis |
| OpenProject | OSS | Yes (REST API) | Self-host gate for regulated orgs |
| n8n | OSS | Yes | Schedule the stance audit on a folder cadence (faion-net hosts n8n on port 5678) |

## Templates & scripts

`templates.md` is empty in this methodology. Inline a stance-review JSON schema and
a one-shot intake-framer below; both are kept under 50 lines combined.

### Stance review schema (canonical)
```json
{
  "artifact_id": "string",
  "stance_overall": "order_taker | mixed | strategic_partner",
  "axes": {
    "problem_clarity":      {"score": 0, "evidence_quote": "string", "rewrite": "string"},
    "outcome_orientation":  {"score": 0, "evidence_quote": "string", "rewrite": "string"},
    "evidence_grounding":   {"score": 0, "evidence_quote": "string", "rewrite": "string"},
    "enterprise_scope":     {"score": 0, "evidence_quote": "string", "rewrite": "string"},
    "partner_voice":        {"score": 0, "evidence_quote": "string", "rewrite": "string"},
    "kill_criterion":       {"score": 0, "evidence_quote": "string", "rewrite": "string"}
  },
  "linked_okr_id": "string|null",
  "auto_block": "boolean",
  "block_reason": "string|null"
}
```
Threshold rule: `auto_block=true` if any axis < 2 OR if `kill_criterion.score < 1`.

### Intake-framer one-liner
```bash
#!/usr/bin/env bash
# ba-frame — turn a one-line ask into 3 framing questions + strawman outcome.
# Usage: ba-frame "add a CSV export to the dashboard"
set -euo pipefail
: "${MODEL:=claude-opus-4-7}"
ASK="${*:?usage: ba-frame <one-line ask>}"
llm -m "$MODEL" --no-stream <<EOF
You are a strategic BA. The stakeholder said: "$ASK".
Refuse to design a solution. Output JSON:
{"problem_hypothesis": "...",
 "framing_questions": ["q1","q2","q3"],
 "strawman_outcome": {"kpi":"...","delta":"...","horizon_months":0}}
EOF
```

## Best practices
- Treat order-taker language as a lint rule, not a moral failing — scan for verbatim phrases (`as per request`, `the user asked for`, `please implement`) and surface them mechanically.
- Always require a `linked_okr_id` on the rewritten artifact; an outcome with no parent OKR is still order-taking, just dressed up.
- Keep the stance reviewer separate from the rewriter prompt — judging-while-generating dilutes both. Two passes, one model, cheap.
- Anchor every rewrite in a verbatim user / data quote already present in the artifact; if no anchor exists, score `evidence_grounding` zero and refuse to rewrite.
- Make the kill-criterion field non-negotiable. A "strategic partner" who can't say when to stop is just a louder order-taker.
- For solo / startup contexts, collapse the six axes to three (problem, outcome, kill) — the full rubric over-formalizes a one-person team.
- Run the audit on artifact diffs (PRs to the docs repo) not on full files — focuses agent attention and avoids re-judging unchanged content.
- Log every stance score to `.aidocs/memory/patterns.md` so trends per BA / per stakeholder become visible over months, not just per ticket.

## AI-agent gotchas
- The agent will rationalize order-taker language if the original author's name is in context — it's been trained to be agreeable. Mitigation: strip authorship metadata before the prompt and instruct the reviewer to assume the artifact is anonymous.
- "Strategic-partner" rewrites drift toward consultant-speak: vision, alignment, synergy, leverage. Mitigation: ban a stoplist in the system prompt; reject and regenerate any rewrite containing them.
- Outcome metrics get fabricated to satisfy the schema (`"reduce churn 12%"` with no source). Mitigation: require `linked_okr_id` to point at an actual OKR in the supplied org_context, else null + lower the score.
- Order-taker vs partner is culturally loaded; in some org cultures direct rewrites read as insubordinate. Mitigation: ship rewrites as suggestions, never overwrite the source artifact.
- Confirmation bias: if you feed the agent a doc you wrote, it tends to find it strategic. Mitigation: red-team pass by a second instance with system prompt "assume this is order-taker until proved otherwise".
- Token bloat at scale: scanning a 200-doc Confluence space sequentially is expensive. Mitigation: pre-filter via ripgrep on order-taker phrases, only invoke the LLM on hits.
- Human-in-the-loop checkpoints: (1) before any rewrite is applied to a stakeholder-visible artifact, (2) before any auto-block fires on a regulated / contractually-bound spec, (3) before a stance score becomes part of an individual's performance review — all three must stay human.
- Cross-tier portability: this lives in `pro/`; readers may use it on `solo/` tier without enterprise tooling. Keep CLI / flat-file inputs as the primary path so the rubric still works with just `llm` + a markdown file.

## References
- IIBA, BABOK Guide v3 — chapters on Business Analysis Planning & Monitoring, and Strategy Analysis (sections on stakeholder engagement and BA approach selection).
- IIBA, "Business Analyst as Strategic Partner" position paper, 2024 update.
- Adrian Reed, "Business Analyst" (BCS, 2018) — chapters on stance and stakeholder dynamics.
- Marty Cagan, "Inspired" and "Transformed" — outcome-over-output discipline applicable to BA artifacts.
- Teresa Torres, "Continuous Discovery Habits" — opportunity-solution-tree framing usable inside requirement intake.
- Anthropic Claude Code subagents docs — `https://docs.anthropic.com/en/docs/claude-code/sub-agents`.
- Sibling variant for portfolio / quarterly loop: `../../business-analyst/ba-strategic-partnership/agent-integration.md`.
