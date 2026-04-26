# Agent Integration — MLP Planning

## When to use

- MVP shipped with measurable activation but Day-30 retention plateaus below 25-30%.
- Quantitative signal (NPS < 30, churn surveys) shows users finish the core job yet describe the product as "fine" or "okay".
- Retention curve is flat after week 2 — function works, emotion missing.
- About to enter a paid acquisition phase: every dollar spent on a non-lovable product compounds CAC waste.
- Pre-launch on a category where competitors already cleared the "viable" bar (e.g., a 5th note-taking app, 10th invoicing tool).
- Refactor/redesign sprint where the team has explicit budget for polish, copy, micro-interactions.

## When NOT to use

- Pre-MVP — there is nothing to make lovable yet. Use mvp-scoping or `minimum-product-frameworks/` first.
- Product-market fit not validated — adding delight before signal hides the demand problem.
- Infrastructure/B2B plumbing where users only interact via API or backend — delight surface is too small to justify the framework.
- Capacity-constrained team mid-incident — Layer 1 (Functional) and Layer 2 (Reliable) regressions trump delight work.
- Hard-deadline compliance/regulatory features — polish budget should be zero until shipped.

## Where it fails / limitations

- Subjective scoring on the 4-layer audit (Functional/Reliable/Usable/Delightful) drifts between reviewers — without rubric anchors, "4" means different things per scorer.
- "Delight" is culturally specific — confetti charms US consumers, irritates Japanese enterprise. Generic delight templates do not transfer.
- LLMs over-rotate to copy-as-delight when given vague prompts — produces clever microcopy and skips actual interaction-design wins (latency, defaults, progressive disclosure).
- The framework assumes a single primary persona; multi-sided products (marketplaces, prosumer + admin) need separate audits per side.
- Polish prioritization formula (Pain × Frequency × Visibility) is multiplicative — a single 0 zeros out a real opportunity. Use additive scoring when any factor is hard to estimate.
- Retention lift attribution is noisy — a "40% retention bump" from delight work co-occurs with onboarding, pricing, and seasonality changes. Always pair with a holdout cohort.

## Agentic workflow

Drive MLP planning as a 3-phase agent loop: (1) **Audit phase** — feed the agent product analytics export + recent NPS/churn comments and ask it to fill the 4-layer scorecard per feature; (2) **Discovery phase** — agent surfaces delight opportunities by clustering negative-but-not-blocking feedback ("works but underwhelming") and matching them to the 5 delight categories (Speed/Simplicity/Personality/Anticipation/Celebration); (3) **Planning phase** — agent generates a polish backlog ranked by Pain × Frequency × Visibility, and writes the MLP plan using `templates.md`. Human-in-the-loop required at the discovery → planning handoff (delight choices are brand decisions, not data decisions).

### Recommended subagents

- `faion-mlp-gap-finder-agent` — domain-specific agent (declared in `README.md` frontmatter); audits MVP, scores 4 layers, surfaces gaps. Invoke for the audit phase.
- `faion-sdd-executor-agent` — once polish tasks are defined as SDD tasks, drives sequential execution with quality gates. Use after MLP plan is approved.
- `faion-brainstorm` skill — multi-agent diverge/converge for the delight-opportunity step (single-agent ideation tends to converge on copywriting; brainstorm forces broader categories).
- `user-researcher` knowledge (`pro/ux/user-researcher/`) — pull qualitative interview methods for validating delight hypotheses before building.

### Prompt pattern

```
You are MLP-gap-finder. Inputs: <feature list>, <analytics CSV>, <NPS verbatims>.
For each feature, score 1-5 on Functional/Reliable/Usable/Delightful using the rubric below.
Output: JSON array [{feature, scores: {f,r,u,d}, evidence: [verbatim_id...]}].
Do NOT invent scores; cite at least one evidence_id per non-default score.
```

```
You are delight-prioritizer. Input: gap report from previous step.
Cluster gaps by delight category (Speed/Simplicity/Personality/Anticipation/Celebration).
Reject any "delight" idea that requires lifting Layer 1-3 scores below 4.
Output: ranked backlog with Pain×Frequency×Visibility, max 12 items.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `posthog` CLI | Pull retention cohorts, funnel data for the audit | `npm i -g posthog-cli` · posthog.com/docs/cli |
| `amplitude-api` | Export event data for delight-moment analysis | pip `amplitude-analytics` · developers.amplitude.com |
| `gh` (GitHub CLI) | Create polish-backlog issues from agent JSON output | cli.github.com |
| `linear` CLI (`@linear/sdk`) | Push MLP backlog into Linear with Pain/Freq/Vis labels | developers.linear.app |
| `productboard-cli` (community) | Sync delight opportunities to Productboard | community fork on GitHub |
| `dovetail` API | Pull tagged interview snippets as evidence | dovetail.com/developers |
| `delighted` API / `wootric` | NPS verbatim export, segment by score | delighted.com/docs/api |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostHog | SaaS + OSS | Yes — REST + SQL API | Retention curves, feature-flag-gated delight rollouts |
| Amplitude | SaaS | Yes — Export API | Best for funnel/cohort math; Pathfinder identifies friction points |
| Mixpanel | SaaS | Yes — Query API | Solid for activation funnel; impact reports for delight A/B |
| Productboard | SaaS | Partial — REST API, weak write surface | Good for tagging delight opportunities against features |
| Linear | SaaS | Yes — GraphQL | Stable target for polish backlog; cycle planning fits delight sprints |
| Maze | SaaS | Partial — API limited | Run usability tests on delight prototypes pre-build |
| Dovetail | SaaS | Yes — REST | Tag-driven theme extraction from user interviews |
| Pendo / Appcues | SaaS | Partial — REST | Onboarding/empty-state delight delivery without code deploys |
| Hotjar / FullStory | SaaS | Partial — API limited | Session replay to find dull moments humans miss |
| LottieFiles | OSS + SaaS | Yes — REST | Source library for celebration animations agents can wire in |

## Templates & scripts

See `templates.md` for the MLP Planning Document and Delight Sprint templates. Inline helper for converting an audit JSON into a Linear-ready backlog:

```bash
#!/usr/bin/env bash
# audit-to-backlog.sh — turn mlp-gap-finder JSON into Linear issues
# Usage: ./audit-to-backlog.sh audit.json TEAM_ID
set -euo pipefail

AUDIT="$1"
TEAM="$2"
: "${LINEAR_API_KEY:?missing LINEAR_API_KEY}"

jq -c '.[] | select(.scores.d < 4 or .scores.u < 4)' "$AUDIT" | while read -r row; do
  feature=$(echo "$row" | jq -r '.feature')
  layer=$(echo "$row" | jq -r 'if .scores.d < 4 then "delight" else "usable" end')
  pain=$(echo "$row" | jq -r '.pain // 3')
  freq=$(echo "$row" | jq -r '.frequency // 3')
  vis=$(echo "$row" | jq -r '.visibility // 3')
  prio=$((pain * freq * vis))

  curl -sS -X POST https://api.linear.app/graphql \
    -H "Authorization: $LINEAR_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -nc --arg t "$TEAM" --arg title "MLP polish: $feature ($layer)" \
              --arg desc "Pain×Freq×Vis = $prio" \
              '{query:"mutation($i:IssueCreateInput!){issueCreate(input:$i){success}}",
                variables:{i:{teamId:$t,title:$title,description:$desc,priority:2}}}')" \
    | jq -e '.data.issueCreate.success' >/dev/null
  echo "queued: $feature ($prio)"
done
```

## Best practices

- Anchor each layer score with a concrete rubric example before scoring (e.g., "Delight=5 means at least one user voluntarily shared a screenshot in the last 30 days"). Stops score drift across reviewers and sessions.
- Score features against current user verbatims, not against the team's aspirations. Pull at least 5 evidence quotes per non-trivial score.
- Treat performance budgets (TTI, p95 latency on the core action) as Layer 4 work, not infra work — speed is the cheapest, most underrated form of delight.
- Run a delight sprint as a fixed time-box (max 2 weeks) on a single workflow. Cross-cutting "polish everywhere" loses focus and produces nothing shippable.
- Ship delight behind a feature flag with a 50/50 split for the first week. Confetti on payment is funny once and annoying on day 30 — flag it so you can dial back without a deploy.
- Pair every delight feature with a kill-switch metric (rage-click rate, time-to-dismiss). Delight that increases task completion time without retention lift is a regression.
- Write the MLP completion criteria in `templates.md` BEFORE starting work. Without numeric exit criteria, "MLP" expands until the team burns out.

## AI-agent gotchas

- Agents inflate Functional/Reliable scores when the team trains them on internal docs — internal docs always describe the happy path. Force grounding on session replays or support tickets, not docs.
- LLMs collapse "Usable" and "Delightful" because the language overlaps. In the prompt, explicitly forbid scoring Delight ≥ 4 unless the agent can quote a user verbatim using emotional language ("love", "amazing", "I showed my friend").
- "Add personality" prompts produce on-brand-but-generic copy at scale. Constrain agents with brand voice samples and a banned-phrases list (no "delight", "magic", "seamless", "effortless").
- Without a holdout cohort instruction, agents recommend stacked changes that make causal attribution impossible. Always require: "ship one delight intervention per cohort per week."
- Agents will recommend animations that fail accessibility (no `prefers-reduced-motion` check) — add an explicit a11y constraint to the prompt and link `pro/ux/accessibility-specialist/`.
- Delight-opportunity clustering by an LLM tends to favor visual/auditory categories (Celebration, Personality) over harder ones (Speed, Anticipation). Force minimum coverage: at least 1 idea per category.
- Human-in-the-loop checkpoints: (a) after audit scores — review for evidence grounding; (b) after delight-category clustering — brand approval; (c) before flag rollout — legal/compliance for any data-driven personalization.

## References

- Aarron Walter, *Designing for Emotion* (A Book Apart, 2011) — foundational source for emotional design hierarchy.
- Lance Wilson, "Why MVP is dead and MLP is the way" — bringing the MLP term into product vocabulary.
- Jared Spool, *The $300 Million Button* — case study on usability-as-delight.
- Kano Model (Noriaki Kano) — adjacent framework that maps to Layer 4 "delighters".
- PostHog product analytics docs: posthog.com/docs/product-analytics/retention
- Amplitude Pathfinder: amplitude.com/blog/pathfinder
- WCAG 2.2 Reduced Motion: w3.org/WAI/WCAG22/Understanding/animation-from-interactions
- Related methodologies in this skill: `mvp-scoping/`, `minimum-product-frameworks/`, `release-planning/`, `product-analytics/`.
