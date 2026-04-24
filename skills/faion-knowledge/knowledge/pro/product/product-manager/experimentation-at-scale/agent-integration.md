# Agent Integration — Experimentation at Scale (PM angle)

> Companion to `../../product-operations/experimentation-at-scale/agent-integration.md`. Product Operations owns the platform, governance, statistics, and SRM; the PM angle covers **what to test, why, and how to act on the result.** Prefer the ops doc for tooling/stats; use this one for hypothesis framing and decision-making.

## When to use

- A roadmap bet is reversible, has a clear behavioral prediction, and you can measure it within ≤4 weeks at current traffic — A/B is the right tiebreaker between PM-favored options.
- Quarterly planning when the roadmap candidate list outgrows conviction — turn opinions into a ranked experiment slate by ICE/RICE × testability.
- After a discovery round (`continuous-discovery`, `opportunity-solution-trees`) where 2–4 candidate solutions exist for one opportunity — experiment to pick, not to launch.
- A guardrail-only "do-no-harm" rollout: PM wants to ship a refactor or migration and needs proof it didn't regress conversion/retention.
- A pricing or packaging change where finance wants quantified lift before commit (with legal sign-off on bait-pricing rules).
- Stakeholder dispute resolution: design vs. eng vs. growth holding strong opinions — pre-register the metric, run, accept the verdict.
- Onboarding a new PM into an experiment-mature org — agentized hypothesis review tightens the loop fast.

## When NOT to use

- Strategic, irreversible bets (rebrand, repositioning, contract terms) — A/B will under-power on the metrics that matter and over-emphasize short-term proxies. Use evidence triangulation instead.
- Pre-PMF (<1k WAU): the PM should be doing problem interviews, not optimizing CTAs. A null result here means "no signal," not "no effect."
- Innovation-tier features where the audience needs >30 days to learn the new behavior — novelty/primacy will dominate the readout.
- Internal tooling, B2B with <50 accounts, or one-off launches (regulatory, marketing event). Use cohort/case-study analysis.
- When the PM cannot articulate a falsifiable behavioral prediction with a numeric MDE — that is a discovery gap, not an experiment gap. Run a fake-door, prototype test, or interview round first.
- Surfaces under compliance review (HIPAA, PCI, KYC) where any variant requires legal sign-off — gating loop is slower than the agentic experiment author; default to risk-controlled rollout, not A/B.
- When success can only be measured >1 quarter out (LTV, retention beyond available holdout) — switch to switchback or holdout-cohort analysis with explicit stakeholder agreement.

## Where it fails / limitations

- HiPPO override: even with a clean readout, leadership ships the loser anyway. Without a written decision rule pre-committed by the exec sponsor, experimentation becomes theatre.
- "Experiment to launch, not to learn": PM ships the variant once it crosses 95% CI without checking guardrails — guardrails fail, ops gets paged, trust in the platform erodes.
- Solution-shaped hypotheses: "we should add a banner" — the hypothesis carries the answer. PM agents must rewrite to behavioral if-then-because before any sample-size math runs.
- Metric tunnel-vision: PM optimizes the KPI in their OKR; the experiment moves the KPI but cannibalizes a sibling team's metric. Cross-team guardrails are the fix, not heroic monitoring.
- Local maxima: 18 months of CTA color tests yield 6% lift and zero strategic learning. Without an opportunity-tree-rooted slate, experimentation drifts to micro-optimizations.
- Prioritization blind spot: agents will rank by ICE without checking dependency on long-running platform work, then surface a "ship-now" candidate that needs a 6-week migration first.
- Reading outcomes wrong: "p=0.08, directionally positive" → ship. PM agents will defer to whichever framing matches the PM's prior unless forced to copy verbatim framework output.
- Communication failure: a clean win in one segment, flat overall — PM ships globally citing "the win." Segmented readout is mandatory; segment cuts must be pre-registered to avoid p-hacking.

## Agentic workflow

```
Backlog        → idea-triager (sonnet)         → testable? + feeds opportunity tree
Hypothesis     → hypothesis-author (sonnet)    → if-then-because, MDE, primary, segment cuts
Prioritize     → ice-rice-ranker (haiku)       → ranked slate, dep-aware
Pre-flight     → assumption-mapper (sonnet)    → list of stop-conditions + decision rule
Pre-flight     → ops-platform agents           → sample size, guardrails, flags (delegated)
Decision       → readout-interpreter (opus)    → ship / iterate / kill / extend
Comms          → stakeholder-narrator (sonnet) → exec memo, slack/loom blurb, OKR delta
Post-launch    → learning-curator (opus)       → links experiment → opportunity-tree node
```

PM-side agents focus on framing, prioritization, decision, and narrative. Statistics, flags, SRM, and metric registry are delegated to product-operations agents (see sibling doc). Human-in-the-loop checkpoints: hypothesis approval (PM + design), decision rule sign-off (PM + sponsor), ship/kill call (PM only).

### Recommended subagents

| Subagent | Model | Cadence | Inputs | Outputs |
|----------|-------|---------|--------|---------|
| `idea-triager` | sonnet | On idea intake | Idea text, opportunity tree, traffic estimate | Testability score + tier (A/B, prototype, qual, irreversible) |
| `hypothesis-author` | sonnet | Per candidate idea | Idea, opportunity tree node, prior experiments | `experiment-doc.md` with if-then-because, primary metric, MDE |
| `ice-rice-ranker` | haiku | Weekly slate | Hypothesis pool, eng dep graph, current OKRs | Ranked slate with confidence, effort, reach, dep flags |
| `assumption-mapper` | sonnet | Pre-launch | Hypothesis, surface | Falsifiable assumptions + stop conditions + decision rule |
| `readout-interpreter` | opus | At decision point | Ops readout JSON, hypothesis doc, segment cuts | Verdict (ship/iterate/kill/extend) + caveats |
| `stakeholder-narrator` | sonnet | At decision point | Verdict, OKR map, audience | Exec memo, slack blurb, ticket update |
| `learning-curator` | opus | Monthly | All closed experiments | Opportunity-tree edits, "patterns we found", "patterns we killed" |
| `roadmap-impact-modeler` | sonnet | Quarterly | Closed experiments, OKR tree | Adjusted forecast for next quarter's roadmap |

Models calibrated to risk: opus only for verdicts and learning synthesis (where misreading is expensive), sonnet for structured authoring, haiku for ranking math.

### Prompt pattern

Hypothesis author:

```
<role>You are hypothesis-author for a senior PM. You refuse solution-shaped hypotheses.</role>

<schema>
  hypothesis: "If <behavior change>, then <metric M> will <move> by <Δ>, because <mechanism>."
  primary_metric: <one metric, from registry>
  mde_relative: <0.005..0.20>
  segment_cuts: <pre-registered, max 5>
  stop_conditions: <guardrail breaches that must trigger kill>
  decision_rule: <"ship if primary +X% with no guardrail breach and..">
</schema>

<rules>
- Reject if hypothesis names a feature instead of a behavior change.
- Reject if MDE is missing or > likely effect by 3x (overpowered, waste).
- Reject if primary metric is not in `metric-catalog.yaml`.
- Reject if decision rule allows ad-hoc judgment ("we'll see").
- Output JSON to schema; markdown digest <= 60 lines.
</rules>
```

Readout interpreter:

```
<role>You are readout-interpreter. You copy framework numbers verbatim. You never paraphrase confidence.</role>

<inputs>
  ops_readout: { lift, ci_low, ci_high, p_value, srm_pass, power_achieved, segment_breakdown }
  hypothesis_doc: <pre-registered>
</inputs>

<rules>
- If srm_pass=false: VERDICT=invalid, recommend rerun, do not interpret lift.
- If power_achieved < 0.7: VERDICT=inconclusive, recommend extend or kill, never ship.
- Apply pre-registered decision rule; if rule silent, VERDICT=defer to PM.
- Surface guardrail breaches BEFORE primary metric in the narrative.
- Surface novelty risk if runtime < 14 days OR engagement metric.
- Output: { verdict: ship|iterate|kill|extend|invalid, primary_evidence, caveats[], next_step }
</rules>
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Treat hypothesis-doc as PR; reviewers = sponsor + design + data | cli.github.com |
| `growthbook` / `statsig` / `eppo` | Read readouts, do NOT compute (delegated to ops) | per vendor |
| `linear` / `jira` CLI | Link experiment ↔ ticket ↔ OKR | linear.app/docs/cli, atlassian.com |
| `notion` / `coda` API | Pre-registration log, decision-rule archive | notion.so/api |
| `productboard` / `airfocus` API | Idea intake, testability triage | productboard.com/api |
| `tg-send` (NERO) | Send weekly slate + decision memo to stakeholders | `~/bin/tg-send` |
| `mermaid-cli` | Render opportunity-tree edits from learning-curator | mermaid.js.org |
| `claude` (Agent SDK) | Drive the PM-side agents above | docs.anthropic.com |

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Productboard | SaaS | Yes (REST) | Idea intake → opportunity tree, links to experiments |
| Airfocus | SaaS | Yes (REST) | Prioritization scoring (RICE/ICE), good for ranker agent |
| Maze | SaaS | Yes (REST) | Prototype tests for non-A/B ideas (use before promoting to live experiment) |
| Dovetail | SaaS | Yes (REST) | Qual evidence repository — pair with experiment registry for triangulation |
| Pendo / FullStory | SaaS | Partial | Behavior cohort context for hypothesis authoring |
| Notion / Coda | SaaS | Yes (REST) | Pre-registration log; decision-rule archive |
| Mixpanel / Amplitude | SaaS | Yes (REST) | Read-only context for hypothesis authoring (do not run stats here) |
| GrowthBook / Statsig / Eppo | OSS / SaaS | Yes | Source of truth for readout JSON consumed by readout-interpreter |
| Linear / Jira | SaaS | Yes (REST) | Two-way link experiment ↔ ticket ↔ OKR for narrator |

## Templates & scripts

Hypothesis intake schema (`hypothesis-doc.yaml`):

```yaml
id: exp_2026-04-onboarding-checklist
opportunity_tree_node: opp.activation.first-value
hypothesis: |
  If we replace the static onboarding video with a 3-step interactive checklist,
  then day-7 activation rate will increase by >= 4% (relative)
  because users self-direct to first-value tasks faster (evidence: 12 interviews, 3 prototype tests).
primary_metric: d7_activation_rate
guardrail_metrics:
  - signup_to_login_latency_p95
  - support_tickets_per_signup
mde_relative: 0.04
power: 0.8
alpha: 0.05
runtime_min_days: 14
segment_cuts: [device, plan, signup_source]
decision_rule: |
  SHIP if primary_lift >= 4% AND ci_low > 0 AND no guardrail breach AND no SRM.
  ITERATE if 0 < primary_lift < 4% AND no guardrail breach.
  KILL if primary_lift <= 0 OR guardrail breach.
  EXTEND if power_achieved < 0.7 AND no guardrail breach.
stop_conditions:
  - support_tickets_per_signup spike > 25% week-over-week
  - p95 signup latency > 1.5x baseline for >24h
sponsor: vp-product@team
prior_evidence:
  - dovetail/study-2026-03-onboarding-pain
  - maze/proto-2026-04-checklist-v3
  - exp_2025-Q4-onboarding-video (null result)
```

Idea-triage helper (`scripts/triage_idea.py`, ~30 lines):

```python
import json, sys
SCORES = {"reversible": 1, "irreversible": 0, "behavior_change": 1, "feature_only": 0}
TIER = {3: "A/B", 2: "prototype-or-A/B", 1: "qual-first", 0: "irreversible-strategic"}

def triage(idea: dict) -> dict:
    score = 0
    score += SCORES["reversible" if idea.get("reversible") else "irreversible"]
    score += 1 if idea.get("min_traffic_ok") else 0
    score += SCORES["behavior_change" if idea.get("behavioral_prediction") else "feature_only"]
    return {"score": score, "tier": TIER[score], "rationale": idea.get("notes", "")}

if __name__ == "__main__":
    idea = json.load(sys.stdin)
    json.dump(triage(idea), sys.stdout)
```

## Best practices

- Pre-register the decision rule, not just the metric — written, signed by sponsor, archived in Notion. Without this, "we won" becomes negotiable.
- Tie every experiment to one opportunity-tree node; if it doesn't link, it's a CTA test, not product work — schedule, but cap to ≤25% of slate.
- Keep one primary metric per experiment. PM agents will be tempted to add "secondary primary"; reject in review.
- Force a behavioral if-then-because hypothesis. "Try a banner" is rejected; "If we surface plan upgrades in-context, then trial-to-paid will move +3% because friction at the upgrade moment is the bottleneck" is accepted.
- Pre-register segment cuts (max 5). Post-hoc segments are exploratory only and labelled as such — never drive ship decisions.
- Treat null results as findings, not failures. Add to learning-curator inputs; over time, a pattern of nulls in a region of the opportunity tree means rethink the opportunity.
- Run a quarterly "decisions we got wrong" memo with sponsor — single highest-leverage org-learning loop.
- Cap PM time on experiment ops to <20%. If it's higher, the platform isn't mature enough; push work back to product-ops or invest in tooling.
- Always pair an experiment with a kill criterion before launch. PMs are biased to ship; the kill rule is the only thing that keeps the slate honest.
- Maintain a living opportunity-tree map; learning-curator edits it after every closed experiment so future PMs see why a path was abandoned.

## AI-agent gotchas

- Agents will turn ambiguous PM intent ("can we improve activation?") into a hypothesis without flagging missing evidence — require a `prior_evidence:` field with at least 2 sources, else hypothesis-author refuses.
- Readout-interpreter under temperature >0.2 will narrate "directionally positive" on null results — pin temperature ≤0.1 and force JSON output with explicit verdict enum.
- Decision rules drift between hypothesis-doc and readout — narrator agent should compute a hash of the hypothesis-doc at launch and refuse to render a ship memo if the hash changed.
- ICE/RICE rankers will rank a 6-week dependency-locked experiment above a ready-to-go one because they ignore deps — feed the eng dep graph into the ranker prompt.
- Stakeholder-narrator will round confidence intervals into clean numbers ("4% lift, 95% confidence") — force verbatim copy of CI low/high; never paraphrase.
- Learning-curator will hallucinate a pattern from N=2 closed experiments; require N≥5 with shared opportunity-tree branch before emitting a "pattern" claim.
- HiPPO leak: if the agent has access to leadership chat, it will weight comments as "evidence" — keep prior_evidence sources to artifact links only (Dovetail study IDs, prior experiments, prototype tests).
- Readout-interpreter must check SRM and power before reading lift; reorder prompt to fail fast on invalid experiments — otherwise opus will write a nicely worded ship memo on a broken assignment.
- Roadmap-impact-modeler will compound point estimates into 4-quarter forecasts and report them as fact — require it to emit ranges and to label assumptions, never single-number forecasts.
- PM-only ship/kill: agents must not auto-execute the ship action; gate at the flag-deployer step. If autonomy is dialed up, require dual-key approval from PM and sponsor.
- Translation drift (Ukrainian PM input ↔ English experiment doc): hypothesis-author should round-trip-translate the if-then-because and surface differences before approval, otherwise nuance about "first-value" or "activation" gets lost.
- Token cost: readout-interpreter on a 12-segment readout balloons; cap at 50k tokens, otherwise summarize segments first, then interpret.

## References

- Ron Kohavi, Diane Tang, Ya Xu — *Trustworthy Online Controlled Experiments* (2020) — chapters 5 (institutional memory) and 8 (decision-making) are the PM-relevant core.
- Teresa Torres — *Continuous Discovery Habits* (2021) — opportunity-solution-tree wiring of experiments to assumptions.
- Marty Cagan — *Inspired*, *Empowered* — product decision frameworks, not platform mechanics.
- Itamar Gilad — *Evidence-Guided* (2024) — ICE confidence framing tied to experiment evidence.
- Microsoft ExP "lessons learned" papers (Kohavi, 2014–2024) — covers HiPPO override, primary metric drift.
- Booking.com PM blog posts on decision rules and pre-registration.
- Sibling doc: `../../product-operations/experimentation-at-scale/agent-integration.md` — platform, stats, SRM, vendor APIs.
- Sibling skill: `../../../research/researcher/continuous-discovery/README.md` — feeds testable hypotheses upstream.
- Sibling methodology: `../opportunity-solution-trees/` (if present) — anchors experiments to opportunities.
- Anthropic Claude Agent SDK — structured outputs, scheduled triggers (`schedule` skill).
