# Placement — Layer 1: Context
**Slice:** AGENTS.md convention · MCP live sources · layered project-context · ADR / decision journals · **Author pass:** 1 of 10 · **Date:** 2026-08-04

## Verdict summary

| Approach | Dossier verdict | Placement decision | Target path |
|---|---|---|---|
| AGENTS.md ↔ CLAUDE.md bridge | 🟢 | new methodology | `knowledge/dev/agents-md-claude-md-bridge` |
| Context-file cost discipline (ETH 2602.11988) | 🟢 with discipline | new methodology **+** workflow-edit | `knowledge/sdlc-ai/context-file-cost-budget` · `idea-to-prod/content/10-bootstrap.xml` |
| Nesting / per-module files | 🟢 | refresh existing | `knowledge/sdlc-ai/agents-md-per-module-bootstrap` |
| Layered project-context (Agent OS standards→product→spec, Cursor rules) | 🟡 | folded in as the *scoping mechanism* of `context-file-cost-budget`; no own slug | — |
| MCP as live-sources layer | 🟡 | new methodology + refresh 6 | `knowledge/sdlc-ai/mcp-vs-cli-decision-rule` |
| MCP 2026-07-28 breakage | 🟡 | new methodology | `knowledge/ai-agents/mcp-2026-07-28-migration` |
| MCP as *our* product surface | 🔴 | no placement | — |
| ADR practice / MADR 4.0.0 template | 🟢, covered | refresh only | `knowledge/architecture/architecture-decision-records` |
| ADRs **as agent context** (loading, cost, enforcement) | 🟢, gap | new methodology + playbook + workflow-edit | `knowledge/sdlc-ai/adr-as-agent-context` |
| "ADRs prevent relitigation" causal claim | 🔴 | anti-claim line inside the new slug | — |

**The tension, resolved.** Layer 1 is *mostly* methodology — it teaches artefacts the user writes, on demand, at zero standing cost. But two of our workflows **emit Layer 1 artefacts themselves**, unsupervised: `idea-to-prod` mandates an `AGENTS.md` + `CLAUDE.md` pair in every directory it creates, and maintains an append-only `decisions.md`. That is exactly the measured-harmful cell — machine-generated context files, accepted uncut, loaded wholesale. A methodology cannot fix it, because the workflow, not the user, is the author. Rule: **workflows own the constraints on artefacts they emit; methodologies teach the artefacts the user emits.** MCP emits nothing in our workflows → methodology-only, zero workflow edits.

## Workflow changes

**W1 — `idea-to-prod/content/10-bootstrap.xml`, section "Per-directory docs".** Keep the pair requirement (routing rationale stands). Extend the existing `<rule>` `<statement>` with three bounds: (a) `CLAUDE.md` is exactly the one line `@AGENTS.md`, never duplicated prose; (b) each generated `AGENTS.md` ≤200 lines and carries **commands, conventions, boundaries only** — no directory listings, dependency lists or architecture overviews; (c) a machine-generated `AGENTS.md` is a *draft*: the phase that created it must cut it before advancing, and `20-phases.xml`'s advance condition treats an uncut file as a missing output. Replace the current one-line `<rationale>` with the dated evidence: Gloaguen et al. arXiv 2602.11988 v2 (2026-06-23) — context files >20% inference cost, repository overviews measured *unhelpful*, LLM-generated files −0.5% SWE-bench Lite / −2% AGENTbench; Anthropic's own 200-line target (code.claude.com/docs/en/memory, 2026-08-03). Add an `<antipattern>`: bootstrapping eight nested `AGENTS.md` files each with a repo-overview section — the tax is paid on every tick of every future session, for content the agent derives anyway.

**W2 — same file, section "decisions.md (append-only)".** Keep append-only + chosen/rejected. Add to the mandated entry shape two fields: `confirmation:` (the test, lint rule or PreToolUse hook that makes it binding — an entry without one is a wish) and `superseded-by:` (by date; never edit in place). Add a second `<rule>`: `state.md` carries a **one-line index per decision** (date + one sentence + anchor); orchestrator and subagents read full `decisions.md` only when a task brief names the anchor. Rationale: an append-only log grows monotonically, so wholesale loading re-pays the +19–23% tax each tick for decisions irrelevant to the phase. Add `<reference>` to `adr-as-agent-context`.

**W3 — `idea-to-prod/decisions.xml`.** Append two entries dated 2026-08-04: `topic="generated-context-files-are-drafts"` (chose bounded/human-cut; rejected auto-accepted per-directory docs; rationale = the measured numbers) and `topic="decision-log-loaded-by-index"` (chose index-line loading; rejected wholesale read each tick).

**W4 — `improver/content/04-memory-files.xml`, section "decisions.md".** Add one `<rule>`: every DEC entry names its enforcement mechanism or is tagged `unenforced`; `.aidocs/memory/` is read by index, never loaded whole. Aligns improver's decision memory with W2's shape.

## New content proposed

Registration for every item below: create dir + `AGENTS.md` (no frontmatter) + `CLAUDE.md` + `meta.json` + `content/NN-*.xml` → run `scripts/regen-tier-manifest.py` → **hand-add** the `<methodology>`/`<playbook>` entry and bump `count=` in the domain index. Never run `build-domain-index-v2.py`.

1. **`agents-md-claude-md-bridge`** — `dev`, **free**. Produces a working two-file bridge: `@AGENTS.md` import, symlink alternative + Windows caveat, 4-hop import depth, precedence order, and the explicit fact that imports dedupe but **do not** save context. Free because it is a short high-frequency fact and the natural hook into the paid cost material. Not covered by `claude-md-creation` / `claude-md-creation-quality` (geek, author a CLAUDE.md body; no cross-tool interop), `agents-md-per-module-bootstrap` (nesting), `agents-md-for-receiving-team` (handoff), `ai-convention-anchoring` (conventions + lint). Index: `knowledge/dev/INDEX.xml`.
2. **`context-file-cost-budget`** — `sdlc-ai`, **solo**. Produces a Context Budget Record: 200-line ceiling, instructions-in/overviews-out classification of every existing line, a path-scoped relocation plan (`.claude/rules/` `paths:`, `claudeMdExcludes`, `.cursor/rules` equivalent — this is where the Agent OS standards→product→spec layering lands, as scoping not as a new folder tree), and the **≥5-run median protocol** required before claiming any improvement. Ships `scripts/validate-context-file-cost-budget.py`. Solo because it is the first paid step after the free bridge. Not covered by `context-window-curation-for-coding-agents` (per-task ≤6K bundle, task-scoped), `claude-md-creation-quality` (no dated cost evidence), `ai-convention-anchoring`.
3. **`adr-as-agent-context`** — `sdlc-ai`, **solo**. Produces a Decision Loading Plan over an existing `docs/decisions/`: index line → path-scoped `.claude/rules/` record → PreToolUse hook for the one-way-door subset; promotes MADR's optional `Confirmation` to mandatory; carries the explicit anti-claim that no controlled study supports "prevents". Not covered by `architecture-decision-records`, `adr-reversibility-tagging`, `adr-staleness-audit`, `adr-supersession-detection`, `adr-consequence-evidence-binding`, `adr-ai-drafted-with-review`, `adr-workflow` — all authoring/triage/drift, none loading or enforcement.
4. **`mcp-vs-cli-decision-rule`** — `sdlc-ai`, **solo**. Per-source routing (CLI / MCP / neither) with the token-floor arithmetic, `ENABLE_TOOL_SEARCH` fallback traps, and the first-party-OAuth-only security rule. All 12 existing MCP slugs are geek and teach *building*; none says when not to.
5. **`mcp-2026-07-28-migration`** — `ai-agents`, **geek**. Breaking-change-by-breaking-change checklist with SEP numbers and the 12-month deprecation clock.
6. **Playbook `wire-decision-journal-into-agent-context`** — `playbooks/solo/role-software-architect/`, goal `govern-decide`, **solo**. Done = journal index-lined in AGENTS.md, one-way-door subset path-scoped, one PreToolUse hook live. Checked `adr-draft-for-a-single-decision` and `adr-write-up-client-architecture`: both produce records, neither wires them. Index: `playbooks/by-goal/govern-decide/INDEX.xml`.
7. **Refresh, not new** (bump `last_reviewed`, re-pin, update INDEX summary if changed): `ml-engineering/{mcp-architecture,mcp-server-implementation,mcp-client-integration,mcp-security}`, `ai-agents/{mcp-transport-stdio-vs-http,mcp-resource-vs-tool-vs-prompt}` — all pinned to 2025-11-25; `validate-mcp-architecture.py` encodes the dead revision and will now pass non-conformant servers. Also `sdlc-ai/agents-md-per-module-bootstrap` (closest-file-wins + cost evidence) and `architecture/architecture-decision-records` (MADR 4.0.0 pin; resolve the architecture/sdd duplicate slug).

## Rejected

MCP for our own product surface — trades a zero-token local binary for a per-request tool-definition tax. Any "comprehensive AGENTS.md template" or a `faion init-agents-md` generator — that is selling the measured-harmful variant. New slugs for "what is AGENTS.md" / "what is MCP" — covered. Base ADR practice, template, supersession, staleness, reversibility — six existing slugs. YADR / YAML ADRs — single unverified secondary source. MCP registry as a discovery recommendation — preview since 2025-09-08. The 60k-repos / 170-member figures as current numbers.

## Risks / conflicts with other slices

- `idea-to-prod/content/10-bootstrap.xml` and `idea-to-prod/decisions.xml` — the Layer 2 passes (constitution-md-pattern, spec-delta) and Layer 3 (checkpoint-rollback) will target the same layout contract. **Highest collision risk.**
- `improver/content/04-memory-files.xml` — Layer 3 checkpoint/rollback also touches durable state.
- `knowledge/sdlc-ai/INDEX.xml` — three of my additions land here; merge entries and `count=`, never overwrite.
- `knowledge/ai-agents/INDEX.xml` — Layer 3/4 passes add here too.
- `skills/tier-manifest.json` — regenerated, never hand-edited; exactly one pass should run `regen-tier-manifest.py`, last.
