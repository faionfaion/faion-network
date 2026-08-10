# Placement — Domain Tools (Layer 5)
**Slice:** research repositories, desk research, concept/prototype tools · **Author pass:** 9 of 10 · **Date:** 2026-08-04

## Verdict summary

| Tool cluster | Substitute or complement | Placement decision | Target path |
|---|---|---|---|
| Research repositories (Dovetail/Marvin/Condens/Looppanel/Notably) | Complement, conditional on scale | Keep existing methodologies at pro; no new methodology; fix the one stale playbook | `research/research-repository-setup`, `research/research-repository-ops`, `playbooks/pro/ux-research/user-interviews-at-scale/playbook.md` |
| Desk research w/ citations (Perplexity, Elicit, Consensus, Scite, OpenAI/Gemini Deep Research) | Partial substitute (decompose-search step is commoditized) | Insert tool-use rule into two workflows' research phases; re-tier two methodologies | `workflows/idea-to-prod/content/20-phases.xml`, `workflows/brainstorm/content/02-phases.xml`, `research/ai-research-tools`, `research/perplexity-ai-research` |
| Concept/prototype generation (Figma Make, UX Pilot, Magic Patterns, v0, Uizard) | Complement (no accessibility/token-QA in any tool) | Keep methodologies at geek — reject the prior down-tier | `ux/generative-ui-design(-ui-design)`, `ux/ai-generated-layout-review-checklist`, `ux/figma-ai-ecosystem(-ui-design)` |

## Workflow changes

1. **`workflows/idea-to-prod/content/20-phases.xml`, Phase 1 section.** Add a second `<rule>` after the existing tool-chain rule: task briefs for desk-research dimensions (competitor pricing, market sizing, any claim needing a citation) MUST point the subagent at a UI-based desk-research tool — Perplexity Pro or Gemini Deep Research, never the `PPLX_API_KEY` path — and require per-claim `verified_by` + H/M/L confidence before the output lands in `research/NN-<slug>.md`, mirroring `research/perplexity-ai-research`'s `content/02-output-contract.xml`. Additive only — the existing gemini→codex→claude fallback chain is a *code-search* chain and is untouched.
2. **`workflows/brainstorm/content/02-phases.xml`, Phase 1 DIVERGE.** Append one clause to the existing "distinct persona" rule: a persona whose brief needs external market/citation grounding (not pure corpus reasoning) follows the same UI-tool + verification discipline as idea-to-prod Phase 1; a recommendation built on unverified tool output cannot enter the 30-item list without a confidence tag. Scoped narrowly — fires only when a brief explicitly requires external grounding, so it doesn't turn every brainstorm into a research run.
3. No change to `media-ops`, `improver`, `poll-agents`, `sdd-batch-orchestrator` — out of scope for this slice.

## Stale-price defect — the fix

**File:** `skills/faion/playbooks/pro/ux-research/user-interviews-at-scale/playbook.md`

- Frontmatter `description` (line 3): drop "tag in Dovetail" → "tag in a research repository (Marvin or Condens)".
- Prerequisites (line 22): `A Dovetail account (Starter plan, $29/mo, ...)` → `A research-repository account for tagging + synthesis — Marvin (free, 2 seats, 5 uploads/mo) or Condens Lite (EUR15/mo, unlimited transcription/projects). Current per-vendor comparison: research/research-repository-setup/templates/platform-scorecard.md — do not hardcode a price here.`
- Phase 5 heading + steps (lines 66-73, "Tag in Dovetail"): swap Dovetail → Marvin; the mechanic is a 1:1 match (Project → import → tag group → highlight+tag → Insights→Charts).
- Phase 6 (lines 75-81): same swap; "Dovetail link button → Add evidence" → "Marvin's Insight report evidence link".
- Next (line 108): `Upgrade to Dovetail's Team plan ($99/mo)...` → `Upgrade to Marvin's paid tier (contact sales — no published self-serve price as of 2026-08) or Condens Business (EUR500/mo, 5 contributors) once multiple researchers tag simultaneously.`
- Add frontmatter field `last_price_check: 2026-08-04`, distinct from `last_verified` (which covers procedural correctness, not dollar figures). Makes every price-bearing file greppable (`grep -rl last_price_check`) for a scoped re-audit instead of re-reading full bodies.

## Re-tiering decisions

- **`research/ai-research-tools`: geek → solo.** Pure tool-selection map, no API key, applies to any solopreneur doing market/competitive research — not the agent-building population geek is scoped to (`ai/` + `sdlc-ai/` per `skills/CLAUDE.md`). Agree with the dossier's committed call.
- **`research/perplexity-ai-research`: geek → pro.** Still requires `PPLX_API_KEY` + Python batch caller + JSON-schema validation — one notch more technical than plain selection, still not agent-building. Agree. Flag as a follow-up CR (not executed here): rewrite prerequisites to lead with the UI workflow first, demote the API script to an optional appendix — required by the "works without a terminal" constraint.
- **`research/research-repository-setup`, `research/research-repository-ops`: keep pro.** Overrule the prior down-tier. The methodology's own Skip-If clause already excludes `<50 studies/year` solo use; what it produces (access matrix, ingestion wiring, audit trail) is a multi-researcher concern independent of tool price. Price-ratio against geek's $99 bundle is not a valid signal on its own.
- **`ux/generative-ui-design(-ui-design)`, `ux/ai-generated-layout-review-checklist`, `ux/figma-ai-ecosystem(-ui-design)`: keep geek.** Only 1 of 5 tools (Uizard, $12) sits in the claimed $12-22 band; Figma Make at realistic usage and Magic Patterns Business meet/exceed geek's $99. None of the five ships accessibility or design-token validation — the buyer who needs that judgment layer is geek's serious-shipper persona, not solo/pro.

Registration for every tier change above: edit `meta.json` `tier` field → run `scripts/regen-tier-manifest.py` → hand-edit the `tier` attribute on the matching `<methodology>` row in `knowledge/research/INDEX.xml`. Do not touch `figma-ai-ecosystem`'s twin slug (`content_id: 6885a4c5c2cc788e`) without also updating `figma-ai-ecosystem-ui-design` — same body, two slugs.

## Tool-aware vs tool-agnostic — the mechanism

Keep both shapes, decouple price from prose. Tool-agnostic methodology bodies (`content/*.xml`) stay evergreen — no dollar figures inline, ever. Tool-aware artifacts (playbooks with literal UI steps, like `user-interviews-at-scale`) keep naming vendors because the literal-steps pattern *is* the value — but every dollar figure lives in exactly one file per domain, which methodologies/playbooks link to, never copy. `research-repository-setup/templates/platform-scorecard.md` already has this shape (a blank fill-in scorecard); extend it to also ship dossier-verified prices with `[re-verify: YYYY-MM]` markers, so it doubles as both a customer worksheet and the corpus's one source of truth for repository pricing. Pair with the `last_price_check` frontmatter field above so a scripted audit finds every price-bearing file without reading bodies. This is the direct fix for the failure that produced three conflicting Dovetail numbers in this corpus already.

## New content proposed

None. Coverage is complete: `ai-research-tools`/`perplexity-ai-research` cover desk research; the three ux methodologies cover concept generation; `research-repository-setup`/`-ops` cover repositories. Only a template extension: pre-fill `platform-scorecard.md` with this dossier's verified Marvin/Condens/Dovetail/Looppanel numbers (dated, with re-verify markers). Registration: no `meta.json` (it's a template, not a methodology) — add one row to `research-repository-setup/AGENTS.md`'s Content table noting the scorecard is now pre-filled, not blank.

## Rejected

- New standalone methodologies per vendor (Marvin, Condens, Perplexity, Uizard, ...) — redundant with the existing selection-map methodologies and recreates the exact staleness trap this defect proves.
- Re-tiering the three ux methodologies down — dossier's arithmetic overrules the prior pass.
- Running or editing `scripts/build-domain-index-v2.py` — broken (`--write` wipes the index); never invoke.

## Risks / conflicts with other slices

- `research/research-repository-setup`'s `templates/access-matrix.md` and `taxonomy-seed.yaml` may be touched by an adjacent Layer-4 (SDD/PM tooling) slice — coordinate before editing.
- Re-tiering `research/ai-research-tools` and `research/perplexity-ai-research` changes `tier-manifest.json` rows the desk-research dossier itself analyzed — if another pass independently re-tiers overlapping `research/` slugs, resolve by dossier date, not last-edit-wins.
- `skills/faion/playbooks/pro/ux-research/user-interviews-at-scale/playbook.md` is a single file — no other placement pass should edit it independently of this fix.
