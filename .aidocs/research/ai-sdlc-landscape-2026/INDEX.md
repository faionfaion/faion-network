# AI-SDLC Landscape 2026 — research dossiers

**Compiled:** 2026-08-03 · **Freshness horizon:** ~3 months. Re-verify versions and prices after November 2026 before relying on anything here.

25 dossiers, one per approach, each with: current state (dated), mechanics detailed enough to reimplement from, collected primary sources, what to borrow, what not to, and a mapping onto our corpus.

**Verdict legend:** 🟢 take · 🟡 take the idea, not the tool · 🔴 skip. Verdicts are from the standpoint of a **solopreneur, including a non-technical one**.

## Layer 1 — Context

| Dossier | Verdict | One line |
|---|---|---|
| [agents-md-standard](layer1-context/agents-md-standard.md) | 🟢 | Convention, not a versioned spec; interop is free, accuracy gains are not (+19% cost, LLM-generated files measurably hurt) |
| [mcp-live-sources](layer1-context/mcp-live-sources.md) | 🟡 | Live sources matter; MCP costs 17.6k–55k tokens before work starts and broke compatibility 2026-07-28 |
| [decision-journal-adr](layer1-context/decision-journal-adr.md) | 🟢 | MADR 4.0.0 stable; the gap is loading discipline, not the template |

## Layer 2 — Decomposition

| Dossier | Verdict | One line |
|---|---|---|
| [ears-notation](layer2-decomposition/ears-notation.md) | 🟢 | The only idea in the landscape that is a grammar, not a prompt convention — RE2-checkable, full linter design included |
| [constitution-md-pattern](layer2-decomposition/constitution-md-pattern.md) | 🟢 | We already have the file and none of what gives it authority |
| [spec-delta-pattern](layer2-decomposition/spec-delta-pattern.md) | 🟢 | Merge order + scenario-loss check = the deterministic reviewer a solo cannot hire |
| [spec-kit](layer2-decomposition/spec-kit.md) | 🟡 | v0.15.2; enforces file existence only, no content parser anywhere |
| [kiro](layer2-decomposition/kiro.md) | 🟡 | The shape is worth copying; the product is a second metered IDE |
| [openspec](layer2-decomposition/openspec.md) | 🟡 | Take the format; its `specs/` tree would fork our source of truth in two |
| [agent-os](layer2-decomposition/agent-os.md) | 🟡 | `discover-standards` is excellent; v3 kept the folders and deleted the pipeline |
| [bmad-method](layer2-decomposition/bmad-method.md) | 🟡 | Built to write code; everything below story generation is Scrum-for-agents |
| [bmad-prfaq](layer2-decomposition/bmad-prfaq.md) | 🟢 | Zero software dependency, portable across concept types; our corpus has zero coverage |
| [flat-rate-planning](layer2-decomposition/flat-rate-planning.md) | 🟡 | Moves your *cheapest* long session off the meter; for us it is a new cost, not a saving |
| [tessl](layer2-decomposition/tessl.md) | 🔴 | Post-mortem, not an evaluation — the spec-as-source product no longer exists |

## Layer 3 — Orchestration

| Dossier | Verdict | One line |
|---|---|---|
| [checkpoint-rollback-pattern](layer3-orchestration/checkpoint-rollback-pattern.md) | 🟢 | LangGraph's real contribution, implementable on bash + an on-disk queue |
| [engineering-frameworks](layer3-orchestration/engineering-frameworks.md) | 🔴 | Python-only across the board; durable checkpoint/replay is the sole genuine differentiator |
| [visual-automation-tools](layer3-orchestration/visual-automation-tools.md) | 🟡 | n8n self-hosted is the only one that can shell out to a local binary |

## Layer 4 — Reliability

| Dossier | Verdict | One line |
|---|---|---|
| [three-tier-verification-ladder](layer4-reliability/three-tier-verification-ladder.md) | 🟢 | The cost discipline the whole layer reduces to: lint → trigger evals → behavioural evals |
| [structured-output](layer4-reliability/structured-output.md) | 🟢 | Guarantees shape only; every semantic constraint in a schema is silently dropped |
| [eval-harnesses](layer4-reliability/eval-harnesses.md) | 🟢 | Promptfoo dev-time via `exec:`; the SaaS platforms cannot test a Go binary |
| [groundedness-and-citations](layer4-reliability/groundedness-and-citations.md) | 🟡 | Citations API is unusable in our hot path; a candidate-set ID check is a free, stronger equivalent |
| [llm-as-judge](layer4-reliability/llm-as-judge.md) | 🟡 | Best debiased judge tops out at κ=0.549 — pairwise triage only, never an absolute gate |

## Layer 5 — Domain

| Dossier | Verdict | One line |
|---|---|---|
| [desk-research-with-citations](layer5-domain/desk-research-with-citations.md) | 🟢 | Perplexity usable *with* forced verification; the Tow Center 37% is best-in-class, which is the argument |
| [research-repositories](layer5-domain/research-repositories.md) | 🟡 | Structural value only past small-scale use; below that markdown is adequate |
| [concept-and-prototype-tools](layer5-domain/concept-and-prototype-tools.md) | 🟡 | None does design-system or accessibility QA — the judgment layer stays with the human |

## Corrections to the source landscape document

The document this research was commissioned against contained these errors. Recorded so they are not re-propagated.

| Claim | Correction |
|---|---|
| Tessl Framework "~9 months in closed beta"; live Spec Registry | Pivoted **2026-01-29** to agent-skills governance. No `tessl build`, no `.spec.md`, no Framework page. The registry is a **Skills** Registry. CLI never left 0.x |
| Spec Kit v0.11 (June 2026) | **v0.15.2, 2026-08-03**; `converge` landed in v0.11.2, 2026-06-18 |
| Spec Kit is greenfield-only | Refuted — README has an explicit brownfield phase plus `docs/guides/evolving-specs.md` |
| BMAD ~49k stars, branch at v6.8, Marketplace in v6.3.0 | **51,439 stars**; line reached **v6.10.0 (2026-07-03)**; Marketplace shipped 2026-04-09 and was **retired 2026-05-17**. The Analyst→PM→Architect→SM→Dev→QA cast is v4/v5 — v6.3.0 merged personas into Amelia |
| Web Bundles move the expensive phase off the meter | Inverted. A 40-turn planning chat is ~$3 cached; one agentic implementation task is ~$26. It moves the *cheap* session |
| AGENTS.md "de-facto standard", 170+ orgs, 60,000+ repos | No versioned spec exists — it is a convention. **190 orgs** as of 2026-05-18. The repo figure is dated 2025-12-09 and never refreshed |
| Claude Code is "the main holdout" | Overstated — Anthropic documents the `@AGENTS.md` bridge itself |
| MCP is what separates a real context layer from imitation | False dichotomy. A CLI the agent already shells out to is a live source at zero token cost |
| Dovetail ~$99/seat/mo | Dovetail **killed self-serve pricing**. Current page: Free ($0, 1 project) and sales-gated Enterprise only |
| No tool machine-validates EARS | False market-wide — **QVscribe has since 2019** on DOORS Next/Jama/Polarion. True only inside the AI-agent SDLC segment |
| Kiro: four hook triggers; requirements/design must complete before implementation | **Ten** triggers; blockable are `PreToolUse`, `UserPromptSubmit`, `PreTaskExec`. Quick Spec generates all three artefacts with no gates |

## Corrections to our own prior analysis

| Earlier claim | Correction |
|---|---|
| Delta-only specs cut loaded context 30–40% | Our specs are **already 64% delta**. Real saving ≈150–250 tokens/feature. The 13× win is already owned via `project-spec/` routing |
| Claude Agent SDK has a Go SDK v1.56.0 | No official Go SDK exists. `faion-cli` has **no Anthropic dependency at all** — `internal/anthropic/` is hand-rolled over `go-retryablehttp` |
| Position bias dominates LLM-judge error | Backwards — style bias 0.10–0.76 dominates; position bias ≤0.04 |
| Confident AI $19.99/user/mo | **$200/mo** |
| MiniCheck usable as a cheap groundedness scorer | **CC BY-NC** — not usable commercially |
| OpenSpec dropped `diff` for `git diff` | Dropped in v0.2.0 pointing at `openspec show` |
| Agent OS dropped `decisions.md` for Recaps | Wrong on both halves — `decisions.md` never existed in any tag; Recaps shipped v1.4.1 (2025-08-19) and were removed by v3 |

## Corpus defects surfaced during this research

Verified directly against the repo, not taken from agent reports.

1. **Seven SDD methodologies exist on disk, are cited by name in root `AGENTS.md`, and are absent from `tier-manifest.json`; six are also absent from `sdd/INDEX.xml`** (98 dirs on disk, 90 declared). Unreachable by either retrieval path.
2. **883 broken `methodology_refs`/`playbook_refs` across 5,744 published MDX files** (18,107 refs checked, 75 distinct phantom slugs). Over 350 of them point at the seven methodologies above — i.e. **~40% of our "writer hallucination" problem is our own unwired manifest.**
3. **MCP content contradicts itself.** `ai-agents/model-context-protocol/` cites spec 2026-07-28; `ml-engineering/mcp-architecture/` (and its `validate-mcp-architecture.py`) and `ai-agents/mcp-transport-stdio-vs-http/` are pinned to 2025-11-25 — 14 references, including `ml-engineering/INDEX.xml`. All sold at geek tier.
4. **No `constitution` methodology exists** in any of the 3,070 manifest entries.
5. **Zero coverage** for EARS, BMAD/PRFAQ, OpenSpec/spec-delta, Kiro, and n8n/visual automation.
6. **Tier skew inverted against our advantage:** reliability content is 42/57 geek, MCP+structured-output+orchestration is 26/29 geek with zero at solo or free — while the `sdd` domain, where the market is crowded, is 67/91 solo.
7. **Stale sold content:** `playbooks/pro/ux-research/user-interviews-at-scale` quotes Dovetail Starter $29 / Team $99 — plans that no longer exist.
8. **`skills/bmad-*/`** — 46 untracked directories, 2.5 MB, all carrying `SKILL.md` (so they load into every Claude Code session via the `~/workspace/.claude` symlink), 76 files referencing a `_bmad/` root that does not exist, and zero presence in `tier-manifest.json`.
