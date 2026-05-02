---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-02
version: 2.0.0
applies_to: any
---

# Brainstorm Workflow

## Summary

Multi-agent diverge-converge-review for ideation, technical audits, and improvement plans. Produces prioritized, reviewer-validated recommendations through 4 phases: DIVERGE (10 research agents) → CONVERGE (synthesis) → REVIEW (8 adversarial reviewers) → FINALIZE.

## Why

Generic "give me ideas" prompts yield groupthink. Distinct personas in independent generation prevent anchoring; adversarial reviewers prevent rubber-stamping; consensus counting separates signal from noise.

## When To Use

- Technical audit / improvement plan ("what should we fix in X?")
- Architecture decision exploration with explicit trade-offs
- Feature ideation with prioritization needed
- Cost optimization with ranked recommendations
- Any task where diverse perspectives at scale beat one careful answer

## When NOT To Use

- User asks a direct, scoped question — answer it
- Simple bug fix with a known root cause
- Refactor where the shape is already decided
- Anything that fits in one short answer

## Phase 0: CONSENT GATE (mandatory)

**If the orchestrator triggered brainstorm but the user did not explicitly ask for it** ("brainstorm", "10 ideas", "audit", "diverge-converge", "what could we improve", "give me options"):

1. STOP. Do not launch any agents.
2. Use `AskUserQuestion`:
   - **question**: "This is a 10+ agent brainstorm (~30min, hundreds of recommendations). Should I run it, or give a short direct answer?"
   - **options**:
     - `{label: "Run brainstorm", description: "10 research + 8 review agents, full diverge-converge-review"}`
     - `{label: "Short answer", description: "2-3 sentence recommendation, no agents"}`
3. On "Short answer" → exit workflow, answer inline.
4. On "Run brainstorm" → proceed to Phase 1.

**Skip Phase 0 only if** the user's message contains an explicit brainstorm trigger word OR they previously approved a brainstorm in this session.

## Phase 1: DIVERGE (research agents)

Launch N=10 research agents (max 3 parallel) with **distinct personas** — each gets a unique focus area. Personas: by domain (frontend/backend/infra/security/UX/cost), by framework (Six Thinking Hats), or by lens (user/dev/business/ops). Each agent produces exactly 30 recommendations in `state → problem → solution → impact` shape. Independent generation; no cross-pollination.

Anti-patterns: identical prompts → groupthink. Too many agents (>12) → diminishing returns. No persona differentiation → bandwagon bias.

## Phase 2: CONVERGE (synthesis)

Single synthesis pass: deduplicate (cluster similar recs), count consensus (how many agents independently surfaced each), rank by impact (cost / effort / risk / user-impact), structure into priority tiers (This Week / Month / Quarter / Backlog).

## Phase 3: REVIEW (adversarial reviewers)

Launch M=8 review agents (max 3 parallel) with assigned attack vectors:

1. Feasibility & Effort — realistic estimates? hidden deps?
2. Security — gaps introduced? minimum viable hardening?
3. Architecture — coherence? contradictions? ordering?
4. Solo Dev / DX — maintenance burden? toil?
5. Cost-Benefit — actual $$ impact? ROI rank?
6. Missing Perspectives — user features? data? operations?
7. Domain Expert — deep dive on top recommendation
8. Prioritization Synthesis — final ordering with feedback

Anti-patterns: "review this document" → rubber-stamping. Same perspective across reviewers → echo chamber.

## Phase 4: FINALIZE

Re-tier per reviewer consensus. Adjust effort estimates. Add devil's-advocate items. Cost projection if relevant. Mark backlog with explicit "why defer".

## Configuration

| Parameter | Default | Notes |
|-----------|---------|-------|
| research_agents | 10 | 10-12 optimal |
| review_agents | 8 | 6-10 viable |
| parallel_limit | 3 | concurrency cap |
| recs_per_agent | 30 | hard requirement |

## Self-Evaluation

After each brainstorm: Coverage (all perspectives covered?), Novelty (surprising recs?), Actionability (executable now?), Bias (groupthink? infrastructure bias?), User focus (≥20% user-facing?).

## Evidence Base

MultiColleagues (ECIS 2025), A-MEM (arXiv 2502.12110), IBIS-based brainstorming (ACM 2024), Six Thinking Hats, Brainwriting.

## Related

- `../sdd-batch-orchestrator/` — multi-feature SDD batch (uses brainstorm output for plan-phase ideation)
- `../improver/` — session-based audit (often follows brainstorm with applied fixes)
- `../../knowledge/solo/product/product-planning/` — feature prioritization frameworks
