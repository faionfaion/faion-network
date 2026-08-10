# Engineering Orchestration Frameworks
**Layer:** 3 — Orchestration · **Verified:** 2026-08-03

Ground truth for every verdict below: `faion-cli` is a Go single binary; per `faion-cli/.aidocs/constitution.md` line 27, *"CLI = content manager, not orchestrator. The CLI exposes primitives for finding and fetching content. Orchestration (multi-step LLM workflows, agent meshes) lives in the caller (Claude Code, scripts, other tools)."* The narrow softening carried into every mapping section below: the CLI may emit/materialise deterministic orchestration artefacts, but never spawns an LLM turn beyond the single search-ranking call it already makes. No runtime Python (or Node) dependency may ever ship inside the CLI binary. What we actually run in-house today: bash + cron + an on-disk queue + a `.halt` flag + Claude Code subagents dispatched inline — no graph framework anywhere.

---

# LangGraph
**Layer:** 3 — Orchestration · **Verdict:** 🟡 take the idea, not the tool · **Verified:** 2026-08-03

## What it is
A Python/TS library from LangChain for building agent control flow as an explicit typed state graph — nodes are functions, edges (including conditional edges) route between them, and a `Checkpointer` persists the shared state after every node execution ("super-step").

## Current state
- Latest: **v1.2.10, released 2026-07-28** (source: pypi.org/project/langgraph/, checked 2026-08-03). Prior research pass had v1.2.9 — off by one patch release, direction of drift confirms the project ships weekly-ish patches.
- Language bindings: **Python and TypeScript only. No official Go SDK exists** (checked 2026-08-03, nothing found in the LangChain org repos or third-party listings).
- License: MIT. Maintainer: LangChain Inc. GitHub stars: high-tens-of-thousands range (not independently re-counted this pass).
- Pricing: library itself is free/OSS; LangSmith (tracing/observability) is the commercial companion product with paid tiers.

## Mechanics
- `StateGraph(StateSchema)` — nodes are plain functions `(state) -> partial_state_update`; edges connect node names, conditional edges route on a function of state.
- A `Checkpointer` (Postgres / SQLite / Redis / in-memory backends) persists the full state dict after every super-step, keyed by `thread_id` + a monotonic `checkpoint_id`.
- Time-travel: re-invoking the graph with a past `checkpoint_id` **forks a new branch of history from that point** rather than mutating the existing lineage — this is the detail worth stealing (see the dedicated `checkpoint-rollback-pattern.md` dossier).
- `interrupt()` pauses a node indefinitely, serializing state to the checkpointer; execution resumes via `Command(resume=value)` on a later invocation with the same `thread_id` — no wall-clock timeout, the pause can last arbitrarily long (days, human-review gates).
- The genuine differentiator over a plain subagent loop is this trio: durable checkpoint/resume, time-travel replay, indefinite human-in-the-loop interrupt — not the graph syntax itself.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | PyPI langgraph project page | https://pypi.org/project/langgraph/ | Version/release date verification | 2026-08-03 |
| 2 | LangGraph persistence concepts (cached from prior pass) | https://langchain-ai.github.io/langgraph/concepts/persistence/ | Checkpointer backends, thread_id/checkpoint_id, get_state_history | 2026-08-03 (not re-fetched fresh this pass; treat as secondary) |

## What to borrow for faion
The checkpoint shape (identity + state snapshot + provenance + status, enumerable history) and the "pause indefinitely, resume explicitly" HITL primitive — both documented in full, framework-independent, in `checkpoint-rollback-pattern.md`.

## What NOT to borrow — and why
The graph engine itself, the typed state-object serialization layer, and any hosted Postgres/Redis checkpointer. We have no Go SDK to reach for, adding Python to the CLI is forbidden outright, and our checkpoint volume (tens to low hundreds of units per run, single machine) doesn't need a database — flock + plain files already solves it at our scale.

## Mapping to our corpus
Caller-side only, never inside the CLI. Existing (unlabeled) implementation: `skills/faion/workflows/poll-agents/`. See `checkpoint-rollback-pattern.md` for the full mapping and a proposed concrete design (`history.log`, `rollback.sh`) that closes the gap between our current phase-marker files and LangGraph's enumerable checkpoint history.

## Open questions / staleness risk
Exact `StateGraph` code sample not independently re-verified this pass (budget-constrained fork run) — treat the API shape above as accurate in spirit, not character-for-character current syntax. Re-verify before quoting code in any customer-facing doc.

---

# CrewAI
**Layer:** 3 — Orchestration · **Verdict:** 🔴 skip · **Verified:** 2026-08-03

## What it is
Python framework distinguishing two orchestration shapes: "Crews" (role-based agent teams collaborating loosely, LLM-driven delegation) and "Flows" (deterministic, event-driven control flow with typed shared state) — the two compose (a Flow step can invoke a Crew).

## Current state
- Latest confirmed: **main `crewai` package v1.14.6, 2026-05-28** (GitHub releases, checked 2026-08-03). Prior finding of "v1.14.7, June 2026" is close but not exact-matched; sub-packages (`crewai-core`, `crewai-cli`) are ahead at v1.15.7–1.15.10 (late July 2026) but those are internal/CLI tooling packages, not the main library version.
- Language bindings: **Python only**, confirmed.
- License: MIT. Maintainer: CrewAI Inc. (VC-backed).

## Mechanics
- Flows: `@start()` marks the entry method, `@listen(other_method)` chains a step to run after another completes, `@router(method)` branches on a return value — all decorator-based, wired to a Pydantic-typed shared `State` object every step can read/write.
- `output_pydantic=SomeModel` on a task forces schema-validated output with automatic retry-on-validation-failure — a structured-output-with-retry convenience, not a novel mechanism.
- Crews use role/goal/backstory-framed agents with LLM-driven task delegation, closer to a multi-agent "team" metaphor than Flows' explicit control flow.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | GitHub crewAI releases | https://github.com/crewAIInc/crewAI/releases | Version/date verification | 2026-08-03 |

## What to borrow for faion
Nothing novel: `@start/@listen/@router` is a decorator-sugar restatement of "sequential step, then-callback, conditional branch" — patterns we already express as plain bash/cron steps and Claude Code subagent dispatch order. `output_pydantic` retry-on-validation-failure is a known structured-output pattern already covered in our own `ai-agents` domain (`strict-mode-required-fields`, `structured-output-mode-picker`).

## What NOT to borrow — and why
The framework itself. Python-only, no Go path, and the two-shape (Crews vs Flows) mental model adds a vocabulary layer over control flow we already implement more simply with bash + subagent dispatch.

## Mapping to our corpus
No adoption path — Python dependency is disallowed in the CLI, and the caller side (our own workflows) already covers the same ground without a framework dependency. Exact Flow decorator code shape not independently re-verified this pass; note before citing code samples externally.

## Open questions / staleness risk
Version pinning above (`v1.14.6`) conflicts slightly with the prior pass's `v1.14.7` — both are plausible given the project's release cadence; re-check at point of any actual citation.

---

# AutoGen / AG2 / Microsoft Agent Framework
**Layer:** 3 — Orchestration · **Verdict:** 🔴 skip · **Verified:** 2026-08-03

## What it is
Three related but now-distinct things: (1) **AutoGen**, Microsoft Research's original conversational multi-agent framework, now retired into maintenance mode; (2) **Microsoft Agent Framework**, its official GA successor, unifying AutoGen's multi-agent ideas with Semantic Kernel's enterprise tooling; (3) **AG2**, a community-run Apache-2.0 fork that split off to keep developing the original AutoGen API independently of Microsoft's direction.

## Current state
- AutoGen: **maintenance mode since October 2025** (unchanged from prior finding).
- **Microsoft Agent Framework 1.0 reached GA on 2026-04-03** (prior finding said 04-02 — off by one day; confirmed via Microsoft devblog + InfoQ, checked 2026-08-03). GA languages: **.NET and Python**.
- **Microsoft Agent Framework's Go SDK is still public preview** as of 2026-08-03 — lives in a separate repo (`microsoft/agent-framework-go`), explicitly documented as "evolving outside the core upstream codebase." Confirms the prior finding; it has NOT moved to GA.
- **AG2: latest is v1.0.1 (2026-07-29)**, following v1.0.0-beta0 (2026-07-03) which promoted the community fork to its own mainline (Classic AutoGen split into its own repo under the fork). v1.0.1 is a hotfix pinning `mcp<2` after an upstream MCP 2.0 breaking change. License: Apache-2.0. **Python only.** Not reconciled with Microsoft's Agent Framework — two separate, incompatible successor lines now exist.

## Mechanics
Conversational multi-agent pattern (`GroupChat`, agent-to-agent message passing with a manager/orchestrator agent selecting next speaker) is the core AutoGen/AG2 idea; Microsoft Agent Framework layers Semantic Kernel's plugin/connector model and enterprise auth/observability on top of similar multi-agent primitives.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | Microsoft devblog / InfoQ coverage of Agent Framework GA | (Microsoft Tech Community + InfoQ, exact URLs not retained by the research fork) | GA date, language targets | 2026-08-03 |
| 2 | `microsoft/agent-framework-go` repo | github.com/microsoft/agent-framework-go | Preview status confirmation | 2026-08-03 |
| 3 | AG2 release history | (GitHub releases, AG2 org) | v1.0.0-beta0 and v1.0.1 dates, mcp<2 pin reason | 2026-08-03 |

## What to borrow for faion
Nothing structural. The one operationally useful lesson: **a successor framework fracturing into two incompatible lines (Microsoft's official vs. the community fork) is a live risk of framework dependency in this space** — worth citing as a general argument for staying framework-independent in our own orchestration, not as a technique to copy.

## What NOT to borrow — and why
All three: AutoGen is dead-ending, Microsoft Agent Framework's Go path is preview-grade and .NET/Python-first, and AG2 is a community fork with its own churn (an MCP-version hotfix within weeks of its 1.0). None offer a stable Go story; all require a runtime we won't ship.

## Mapping to our corpus
No adoption path. Flag the fracture pattern as a risk note in any future methodology that recommends framework adoption to faion customers (`ai-agents/multi-agent-basics` already lists AutoGen/CrewAI/LangGraph as interchangeable wiring targets for a spec — that entry should get a staleness footnote pointing at this dossier).

## Open questions / staleness risk
The Microsoft/AG2 split is recent (mid-2026) and both lines are moving fast — re-verify before any future customer-facing recommendation. GA date for Microsoft Agent Framework (04-02 vs 04-03) is a one-day discrepancy between the two research passes; treat 04-03 as the more recently checked value.

---

# OpenAI Agents SDK
**Layer:** 3 — Orchestration · **Verdict:** 🔴 skip · **Verified:** 2026-08-03

## What it is
OpenAI's own lightweight multi-agent orchestration library: agents, tools, a real control-transfer "handoff" primitive between agents, and guardrails (input/output validation hooks).

## Current state
- Language bindings: **Python and TypeScript only, no Go.**
- Exact current version/release date **not independently pinned this pass** (research fork ran out of budget before confirming) — treat as unverified; do not cite a specific version number without a fresh check.
- License: MIT (open-source SDK); usage is naturally coupled to OpenAI's own model APIs, though the SDK itself is provider-agnostic in principle via LiteLLM-style adapters.

## Mechanics
- **Handoff = real control transfer**, not a tool-call wrapper: when Agent A hands off to Agent B, the entire subsequent turn is driven by B with a fresh(er) instruction set — distinct from a "call another agent as a tool and get a result back" pattern.
- **Guardrails run in parallel but only fire on the first and last agent in a handoff chain** — confirmed verbatim from official docs (openai.github.io/openai-agents-python/guardrails/, checked 2026-08-03): input guardrails execute only on the first agent, output guardrails only on the agent that produces the final output. Any intermediate agent in a multi-hop handoff chain is **not covered by guardrails at all** — the docs explicitly recommend using tool-level guardrails instead for mid-chain checks. This is a real, current, and non-obvious limitation, not a stale claim from an earlier SDK version.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | OpenAI Agents SDK guardrails docs | https://openai.github.io/openai-agents-python/guardrails/ | Verbatim confirmation of first/last-agent-only guardrail scope | 2026-08-03 |

## What to borrow for faion
The guardrail-scope **gotcha** is worth recording as a design lesson independent of the SDK: any multi-hop handoff/delegation chain (including our own subagent-to-subagent dispatch patterns) must not assume a guardrail or validation step "wraps" every hop just because it's declared once at the top — validation coverage needs to be checked per-hop, not assumed inherited. Worth a cross-reference from our `ai-agents/handoff-id-payload` or `multi-agent-orchestration-decision-tree` methodologies.

## What NOT to borrow — and why
The SDK itself: Python/TS only, and its design center of gravity is OpenAI's own model/tool ecosystem, which is not our stack.

## Mapping to our corpus
No direct adoption. Recommend adding the guardrail-scope gotcha as a cited caution in `skills/faion/knowledge/ai-agents/handoff-id-payload` and `multi-agent-orchestration-decision-tree` (both already exist and cover the adjacent ground).

## Open questions / staleness risk
Version/release date unverified this pass — must be checked before any customer-facing citation names a specific SDK version.

---

# Google ADK (Agent Development Kit)
**Layer:** 3 — Orchestration · **Verdict:** 🟡 take the idea, not the tool · **Verified:** 2026-08-03

## What it is
Google's agent-orchestration framework, notable for being one of the only production-track options with an official Go SDK, plus the A2A (Agent2Agent) protocol for cross-vendor agent interop and a resumable human-in-the-loop model.

## Current state
- **Go SDK reached GA at v2.1.0, published 2026-07-23** (pkg.go.dev, checked 2026-08-03) — this is a corrected date from the prior pass's "2026-06-30" (likely an earlier announcement date rather than this exact GA patch's publish date). This remains one of only two production-grade Go options for agent orchestration that we're aware of (the other being our own in-house pattern — no comparable is claimed here).
- **A2A cross-vendor interop confirmed**, wired via `github.com/a2aproject/a2a-go`.
- **PyPI `google-adk` went stable at 2.0 on 2026-05-19** (corrected from the prior pass's "2026-07-31") — this was a hard breaking change: full shift to a graph-based `WorkflowRuntime` node model, `@tool` decorator replaced by `@WorkflowNode`, and an incompatible session/event schema versus the 1.x line.
- Resumable HITL is supported (exact mechanism not re-verified in full this pass, consistent with the prior finding).

## Mechanics
Graph-based `WorkflowRuntime` with `@WorkflowNode`-decorated steps (post-2.0); A2A protocol messages let agents built on different frameworks/vendors hand off tasks to each other over a shared wire format rather than requiring both sides to run the same SDK.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | pkg.go.dev Google ADK Go module | pkg.go.dev (google adk go) | Go SDK v2.1.0 GA date | 2026-08-03 |
| 2 | a2a-go repo | github.com/a2aproject/a2a-go | A2A protocol Go bindings | 2026-08-03 |

## What to borrow for faion
The **A2A protocol idea** — a shared wire format for cross-vendor agent handoff — is conceptually relevant if faion ever needs to interoperate with agents built on other stacks (e.g., a customer's own LangGraph or ADK-based agent calling into `faion get-content` as a tool). Worth tracking as a future integration surface, not adopting now.

## What NOT to borrow — and why
Embedding ADK (Go or otherwise) inside the CLI would violate the CLI's own architectural rule regardless of language — "CLI does not orchestrate multi-step LLM work" applies independent of whether the orchestrator is written in Python or Go. ADK is a legitimate option for an external caller building on top of `faion-cli`, but it is not ours to ship inside the binary.

## Mapping to our corpus
No adoption inside `faion-cli`. If a future feature needs cross-vendor agent interop (a customer's LangGraph/ADK agent calling faion as a tool), A2A is the protocol to evaluate first — flag as a forward-looking note in `faion-cli-agent-adapter-pattern` (`sdlc-ai` domain), which already covers wrapping `faion search`/`get-content` as a tool for Claude Agent SDK, LangChain, and OpenAI Assistants and could gain an A2A row.

## Open questions / staleness risk
Both corrected dates (Go SDK GA 07-23 vs prior 06-30; PyPI 2.0 stable 05-19 vs prior 07-31) should be treated as the more current values, but neither was cross-checked against a second independent source this pass — worth a follow-up spot-check before quoting dates externally.

---

# Claude Agent SDK + subagents
**Layer:** 3 — Orchestration · **Verdict:** 🟢 take — already our baseline · **Verified:** 2026-08-03

## What it is
Anthropic's SDK for building agents on top of Claude, and specifically the subagent-dispatch primitive (the `Agent`/Task-style tool) that Claude Code and this research task itself use: a parent agent forks a child with a fresh, isolated context window and a scoped tool/permission set.

## Current state
- **Concurrency/depth limits confirmed exactly**, timeline verified via the Claude Code changelog: **v2.1.217 (2026-07-21)** introduced a 20-concurrent-subagent cap and disabled nested subagent spawning by default; **v2.1.219 (2026-07-24)** re-enabled nesting to a default depth of 3. This matches the prior finding precisely.
- A "200 per session" limit claimed in the prior research pass **could not be verified this pass** — not found in any changelog or doc searched. Flag as possibly fabricated or sourced from an unrelated doc; do not repeat as fact without a fresh citation.
- **No official Go SDK exists.** A prior finding of "Go SDK 1.56.0" is **wrong and should be dropped** — only unofficial community forks exist (e.g., schlunsen/, Roasbeef/, panbanda/, connerohnesorge/claude-agent-sdk-go on GitHub), none of them authoritative or Anthropic-maintained. The official SDKs are **Python (latest 0.2.128) and TypeScript** only, as of 2026-08-03.
- Each subagent gets a fresh, isolated ~200k-token context window, separate from the parent's.

## Mechanics
Parent dispatches via an `Agent`-style tool call naming a subagent type (or `general-purpose`/`fork`), a prompt, and optionally an isolation mode (worktree/remote). The child runs to completion in its own context and returns a final report; the parent's context grows only by that report, not by the child's internal tool-call trace. Depth-3 nesting means a subagent can itself dispatch further subagents, up to 3 levels deep by default (as of the 2026-07-24 change).

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | Claude Code changelog (2.1.217, 2.1.219 entries) | (CHANGELOG within Claude Code release notes, exact URL not retained by fork) | Concurrency cap + depth-disable/re-enable dates confirmed | 2026-08-03 |
| 2 | GitHub issue anthropics/claude-code#29966 | https://github.com/anthropics/claude-code/issues/29966 | Prompt-caching-disabled-for-subagents bug, full thread read | 2026-08-03 |
| 3 | Community Go SDK forks (schlunsen, Roasbeef, panbanda, connerohnesorge) | GitHub search "claude-agent-sdk-go" | Confirms no official Go SDK exists; these are unofficial | 2026-08-03 |

## What to borrow for faion
This IS our baseline already — Claude Code subagents dispatched inline, no graph framework. Nothing to newly adopt; the finding that matters is the open bug below, which should shape how aggressively we lean on subagent fan-out for cost-sensitive work.

## What NOT to borrow — and why
N/A — this is the tool we already use, not a candidate to evaluate against itself.

## Mapping to our corpus
Direct: this is `skills/faion/workflows/poll-agents/` and `sdd-batch-orchestrator/`'s actual dispatch mechanism. The caching bug (below) directly affects cost modeling for any pool run — worth a note in `poll-agents/content/04-replenishment.xml`'s quota-gate section, since a session that silently pays full uncached-input price on every subagent call burns 5h/7d quota far faster than the replenishment policy assumes.

## Open questions / staleness risk — THE CACHING BUG, CURRENT STATUS
**anthropics/claude-code#29966 is STILL OPEN as of its last activity on 2026-07-29** (checked 2026-08-03). Full thread summary:
- Filed **2026-03-02**: reporter showed 54/54 subagent requests with zero `cache_control` breakpoints hitting, measuring ~378k wasted uncached tokens in one session — matches the prior finding's number exactly.
- **2026-04-05**: an Anthropic collaborator disputed the specific code-path diagnosis, claiming "the subagent path does enable caching by default" and asked for more repro detail.
- **2026-04-06**: the original reporter countered with reverse-proxy logs still showing `cache_control` markers present in the request but `cache_read_input_tokens`/`pre=0` in the response — i.e., caching is declared but not actually landing.
- **2026-07-24**: an independent third party reported the identical zero-caching symptom "on the latest SDK" at roughly 1,000-developer scale.
- As of **2026-07-29** (last thread activity found), **no fix has shipped and no maintainer has confirmed a resolution**; community workarounds (reverse-proxy cache injection) were still being posted on that date.

**Verdict on the bug: open, unresolved, high-cost, and disputed only on root-cause mechanism — not on the empirical symptom.** Treat every subagent-heavy pool run's token-cost estimate as understated until this closes; the quota-gate skill's 50%-of-5h-window threshold should be read as conservative-by-necessity given this bug, not as a knob we can safely loosen.
