---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-02
version: 2.0.0
applies_to: any
content_id: 084b0d7bdc299820
success_criteria:
  - Phase 0 consent gate runs first when the user did not explicitly request brainstorming.
  - Phase 1 produces ≥10 distinct-persona generations of 30 recs each, with no cross-talk.
  - Phase 2 dedup + consensus count + tier ranking yields a single merged list.
  - Phase 3 attaches an adversarial review verdict (KEEP / DEMOTE / DROP) to every item.
---

# Brainstorm Workflow

## Summary

Multi-agent diverge-converge-review for ideation, technical audits, and improvement plans. Five phases: Phase 0 CONSENT GATE → Phase 1 DIVERGE (10 research agents, distinct personas, 30 recs each) → Phase 2 CONVERGE (synthesis: dedup + consensus count + tier ranking) → Phase 3 REVIEW (8 adversarial reviewers, one attack vector each) → Phase 4 FINALIZE (re-tier per reviewer consensus + self-evaluation).

## Why

Generic single-pass ideation anchors on the first plausible answer the model produces. Distinct personas in independent generation prevent anchoring; consensus counting separates signal from noise; adversarial review prevents rubber-stamping. Without the consent gate, auto-routing burns user quota on output they did not request.

## When To Use

- Technical audit / improvement plan ("what should we fix in X?", "audit the codebase").
- Architecture / vendor / build-vs-buy decision exploration with explicit trade-offs.
- Feature ideation when prioritization matters more than raw idea count.
- Cost optimization with ranked, reviewer-validated recommendations.
- Any task where diverse perspectives at scale beat one careful answer.

## When NOT To Use

- User asks a direct, scoped question — answer it inline.
- Simple bug fix with a known root cause.
- Refactor where the shape is already decided.
- Anything that fits in one short answer (Phase 0 routes here on "Short answer").

## Content

| File | What's inside |
|------|---------------|
| `content/01-overview.xml` | Core principle (diverge-converge-review beats single-pass), role split, language convention. |
| `content/02-phases.xml` | Five phases with rules and rationales: Phase 0 consent gate, Phase 1 diverge, Phase 2 converge, Phase 3 review, Phase 4 finalize. Configuration defaults. |
| `content/03-personas.xml` | Three persona strategies (by domain, Six Thinking Hats, by lens) and selection guide. |
| `content/04-reviewer-roles.xml` | 8 required attack vectors + optional roles + reviewer output contract (KEEP/DEMOTE/DROP). |
| `content/05-anti-patterns.xml` | Diverge / review / consent-gate / output smells with rules and rationales. |

## Related

- `decisions.xml` — architectural choices (10/8 agent counts, parallel limit 3, consent gate, distinct personas, adversarial reviewers).
- `../sdd-batch-orchestrator/` — multi-feature SDD batch (frequently consumes brainstorm output for plan-phase ideation).
- `../improver/` — session-based audit (often follows brainstorm with applied fixes).
- `../../knowledge/solo/product/product-planning/` — feature prioritization frameworks.
- `../../../../.aidocs/conventions/workflows/workflow-spec.md` — authoritative workflow spec.
