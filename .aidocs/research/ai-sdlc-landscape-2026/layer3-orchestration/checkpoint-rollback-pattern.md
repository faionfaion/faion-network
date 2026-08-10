# Checkpoint / Rollback Pattern
**Layer:** 3 — Orchestration · **Verdict:** 🟢 take the idea, not the tool · **Verified:** 2026-08-03

## What it is

The single genuinely reusable idea inside LangGraph (and, less visibly, inside Temporal, Restate, and every durable-execution framework) is not the graph — it's the discipline of writing a **checkpoint** after every discrete unit of orchestration progress, such that (a) a crashed or interrupted run resumes from the last checkpoint instead of from zero, and (b) an operator can point the run backward at any prior checkpoint and re-execute from there with a *different* input, decision, or code path — a **rollback**, not a retry.

Stripped of the graph abstraction, a checkpoint is just: **a serialized snapshot of orchestration state, written to durable storage, addressable by an ID, taken at a boundary the orchestrator controls.** Nothing about that requires a DAG engine, a Python process, or a hosted service. It requires discipline about *when* you snapshot and *what* the snapshot must contain to be resumable.

We already do a primitive version of this in `faion-network/skills/faion/workflows/poll-agents/` (`QUEUE.txt` / `DONE.txt` / `ACTIVE.txt`) and in the faion-net-fe ultimate-guide-v8 pool (`mark.sh` phase markers). This dossier documents the general pattern and proposes tightening our own implementation to close the one gap our real incident (the ghost-state-dir bug, 2026, ship 43) exposed.

## Mechanics

### What a checkpoint must capture (the four fields, independent of framework)

| Field | Purpose | LangGraph's version | Our on-disk version |
|---|---|---|---|
| **Identity** | Which run, which step, which attempt | `thread_id` + `checkpoint_id` (monotonic per thread) | backlog slug + phase letter (`states/<slug>/phase-<X>.*`) |
| **State snapshot** | Enough to resume or replay without re-deriving prior work | full graph `State` object (typed dict/Pydantic), serialized to the checkpointer backend | `meta.txt` (url_slug, created_at) + the actual work product already on disk (the `.mdx` files) — state is *mostly the filesystem itself*, not a separate blob |
| **Provenance** | What produced this checkpoint, for audit and for detecting a stale/duplicate write | node name + parent checkpoint_id (forms a DAG of checkpoints, not just a chain) | `DONE.txt` line: `done=<slug> commit=<sha> <iso-date>` — the git commit IS the provenance pointer |
| **Status** | done / failed / in-flight / superseded | not explicit in LangGraph — inferred from whether a later checkpoint exists on the thread | explicit marker files: `phase-<X>.done`, `phase-<X>.failed`, `phase-<X>.in-flight` |

The important design choice LangGraph makes that we should copy explicitly: **checkpoints are addressable and enumerable**, not just "the current state." `get_state_history(thread_id)` returns every checkpoint on a thread in order. Our `DONE.txt` append-log already gives us this for free (it's an append-only ledger) — the phase-marker files do NOT (a `.done` file has no history, only current status). That asymmetry is worth fixing (see below).

### When to write one

Write a checkpoint at every boundary where **redoing the work between here and the last checkpoint would cost more than the write itself** — concretely:

1. After any step that calls an LLM (the expensive, non-deterministic part). Never make an agent re-derive an LLM output it already produced.
2. After any step that has an external side effect that is not idempotent on blind retry (a commit, a publish, a payment call, a message send).
3. Before any step that is likely to fail (network calls, a subagent dispatch, anything with a timeout) — write an "in-flight" marker *before* dispatch, not only "done" after, so a crash mid-flight is visible as a stuck marker rather than silence.
4. At natural human-review gates — the SDD `todo/ → in-progress/ → done/` directory move IS a checkpoint write; moving a task file between lifecycle directories is exactly "write a checkpoint whose ID is the file's path."

### How rollback differs from retry

**Retry** re-runs the *same* step with the *same* inputs, hoping for a transient-failure recovery (network blip, rate limit, flaky test). It requires no rollback machinery — just re-invoke, same checkpoint boundary.

**Rollback** discards one or more checkpoints and resumes from an *earlier* one, usually because:
- a human decided a decision made at step N was wrong (LangGraph's `interrupt()` + edit-state-then-resume flow), or
- step N's output was internally consistent but wrong in a way no automated check caught (needs a human or a different model to redo it differently), or
- the world changed between checkpoint N and now (stale data, a spec that moved) and steps after N need to re-run against new inputs.

The operational difference: retry replays forward with identical state; rollback **truncates the checkpoint history** back to N and then either replays forward from there (deterministic re-execution, e.g. LangGraph time-travel) or waits for new human input before continuing (LangGraph `interrupt`, or our own `todo/ → in-progress/` move-back). A rollback that doesn't truncate history — that just "keeps going but pretends step N didn't happen" — is how the ghost-state-dir bug happened (see below): a marker got written in the wrong place, so the *real* history looked incomplete and the dispatcher tried to redo already-finished work.

### The failure mode we already hit (and the fix, already applied)

`faion-net-fe/.aidocs/_pool/ultimate-guide-v8/scripts/mark.sh` marks a phase `done` by touching `states/<slug>/phase-<X>.done`. Originally the script did an unconditional `mkdir -p "$STATE_DIR"` at the top of every invocation. A phase worker that mistyped a long backlog slug (dropped one word out of a 7-word hyphenated slug) silently created a **ghost checkpoint directory** under the wrong key — the write succeeded, looked identical to a real checkpoint, and the dispatcher, unable to find `phase-A.done` in the ghost dir, offered to redispatch the `A` phase on an article that was actually 4/7 done, which would have produced a duplicate article.

The fix generalizes past this one script: **a checkpoint write must fail loudly if its identity key doesn't already exist in the checkpoint store, except at the one legitimate creation entry point.** `mark.sh`'s `done` and `failed` cases now guard with `[ -d "$STATE_DIR" ] || { echo "ERROR ..."; exit 3; }`. This is the bash equivalent of LangGraph raising on an unknown `thread_id` when you pass `checkpoint_id` explicitly instead of implicitly creating a new thread — a checkpoint store must distinguish "resume an existing lineage" from "start a new one," and only one code path may do the latter.

### A concrete design for a bash + on-disk-queue orchestrator (what we should actually build)

This is the pattern generalized past the ultimate-guide-v8 special case, meant to be reusable across any pool/queue orchestrator we run (poll-agents, media-ops pipelines, SDD batch execution):

```
<pool-dir>/
├── QUEUE.txt              # pending unit-of-work IDs, one per line (unchanged)
├── DONE.txt               # append-only ledger: id  phase  status  commit_sha  iso_ts (unchanged, this IS checkpoint history)
├── ACTIVE.txt             # in-flight ids (unchanged)
├── .statelock             # flock target so writes are serialized (unchanged)
└── states/<id>/
    ├── meta.txt           # identity: created_at, source inputs, url_slug/equivalent
    ├── phase-<X>.in-flight   # written BEFORE dispatch, not just after
    ├── phase-<X>.done        # written after; content = commit sha + timestamp
    ├── phase-<X>.failed      # written after; content = reason + timestamp
    └── history.log         # NEW: append-only per-id checkpoint ledger (mirrors DONE.txt but scoped to this id, survives DONE.txt being pruned/rotated)
```

Three concrete additions over what we already run:

1. **`history.log` per state dir** — an append-only file, one line per checkpoint transition (`<iso_ts> <phase> <in-flight|done|failed> <reason-or-commit>`), so a single ID's full checkpoint lineage is inspectable without grepping the global `DONE.txt`. This is what turns "current status only" into "enumerable history," closing the LangGraph parity gap noted above.
2. **Rollback = truncate + requeue, never silent skip.** A rollback script `rollback.sh <id> <phase>` does exactly three things: (a) verify the state dir exists (same guard as `mark.sh` done/failed), (b) `rm` every `phase-<Y>.done`/`.failed`/`.in-flight` for `phase-<Y> >= phase-<X>` in lineage order, append a `rolled-back` line to `history.log`, and (c) re-add the id to `QUEUE.txt` at the target phase. No script may silently treat a missing marker as "not started" without this explicit rollback record — that ambiguity is exactly what produced the ghost-dispatch near-miss.
3. **In-flight markers are written before dispatch, checked on every tick.** The cron-tick keepalive already reads `QUEUE.txt`/`DONE.txt` fresh each time (see `poll-agents/content/03-state-shape.xml`); extending it to also flag any `phase-*.in-flight` older than N minutes with no matching subagent alive is the cheap version of a "dead letter" queue — it turns a silently-stuck checkpoint into a visible alert instead of a queue that never drains.

None of this requires a graph library, a Python process, or a hosted checkpointer. It requires: one lockfile, one append-only ledger per unit of work, and a hard rule that "does this checkpoint identity already exist" is checked before every write except the one designated creation path.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | `poll-agents/content/03-state-shape.xml` | local: `faion-network/skills/faion/workflows/poll-agents/content/03-state-shape.xml` | Our own atomic-pop (`head`/`tail`/`mv`), on-disk state rationale, recovery flow after `/compact` | 2026-08-03 |
| 2 | `poll-agents/content/04-replenishment.xml` | local: same dir | Two-signal replenishment, strict in-flight cap, quota gate, failed-batch retry-with-sonnet policy | 2026-08-03 |
| 3 | `mark.sh` | local: `faion-net-fe/.aidocs/_pool/ultimate-guide-v8/scripts/mark.sh` | Exact phase-marker mechanics: flock, `phase-<X>.{done,failed,in-flight}`, ghost-dir guard, `DONE.txt` append with git sha | 2026-08-03 |
| 4 | `feedback_pool_ghost_state_dir.md` (NERO memory) | local: `~/.claude/projects/-home-nero-workspace/memory/feedback_pool_ghost_state_dir.md` | Real incident: mistyped slug silently created a ghost checkpoint dir → near-duplicate dispatch; the fix (guard + loud failure) | 2026-08-03 |
| 5 | LangGraph persistence / checkpointing docs | https://langchain-ai.github.io/langgraph/concepts/persistence/ | `thread_id`/`checkpoint_id`, checkpointer backends (memory/SQLite/Postgres/Redis), `get_state_history`, `interrupt()` human-in-the-loop resume | see engineering-frameworks.md for dated verification of the current API surface |

## What to borrow for faion

- The four-field checkpoint shape (identity, state snapshot, provenance, status) as a naming convention for any future queue/pool orchestrator, not just the ultimate-guide-v8 pool.
- "Checkpoint identity must be checked-before-write, one designated creation path only" as a hard rule in `faion-network` methodology form (candidate: a new methodology under `sdlc-ai` or `ai-agents`, e.g. `checkpoint-identity-guard` — codifying the mark.sh fix as a reusable pattern rather than a one-off bugfix).
- Per-id `history.log` as a cheap addition that gets us LangGraph's `get_state_history` for free, in bash.
- Explicit `in-flight`-before-dispatch marker as the cheap version of durable-execution's "the orchestrator survives even if it crashes mid-step."

## What NOT to borrow — and why

- **A graph engine or DAG-typed state object.** Our orchestration units are files and shell commands, not typed Python/TS state passed between nodes. Introducing a `StateGraph`-shaped abstraction into a bash+cron system adds a serialization layer (and a Python/TS runtime dependency) to solve a problem plain files already solve.
- **A hosted checkpointer (Postgres/Redis-backed).** Our checkpoint volume (tens to low hundreds of units per run) and single-machine execution model don't need a database; flock + plain files is the correct-scaled solution. Adding a DB would be solving for a scale (thousands of concurrent runs, multi-machine) we don't have and the CLI (Go, no server-side orchestration) will never have.
- **Automatic replay-on-crash.** LangGraph will silently re-invoke a graph from its last checkpoint on restart. We deliberately do NOT want silent automatic resume for anything that dispatches an LLM subagent — the quota-gate and failed-batch-retry-with-sonnet policies exist precisely because blind automatic retry on an agent failure is the wrong default (per `04-replenishment.xml`); a human or the cron tick's explicit logic should decide to resume, not an implicit crash handler.

## Mapping to our corpus

- Existing (unlabeled) implementations of this pattern: `skills/faion/workflows/poll-agents/content/03-state-shape.xml` + `04-replenishment.xml` (the general pool pattern), `faion-net-fe/.aidocs/_pool/ultimate-guide-v8/scripts/mark.sh` (concrete phase-marker implementation), the SDD `todo/ → in-progress/ → done/` directory-move convention itself (`faion-network/AGENTS.md`).
- **CLI boundary, restated:** `faion-cli/.aidocs/constitution.md` line 27: *"CLI = content manager, not orchestrator. The CLI exposes primitives for finding and fetching content. Orchestration (multi-step LLM workflows, agent meshes) lives in the caller."* This pattern belongs entirely to the caller side (workflows, pool scripts, SDD executors) — the CLI itself never writes a checkpoint or performs a rollback. The one narrow softening from the prior research pass stands: *the CLI may emit and materialise deterministic orchestration artefacts (e.g., scaffold a `states/<id>/` layout, validate a checkpoint file's shape), but it must never itself spawn an LLM turn beyond the single search-ranking call it already makes, and it must never decide when to roll back.*
- No existing methodology directly names "checkpoint/rollback" as a reusable pattern independent of `poll-agents`. Candidate gap: promote the mark.sh guard fix into a standalone `sdlc-ai` or `ai-agents` methodology (working title `checkpoint-identity-guard` or `on-disk-checkpoint-ledger`) so it's discoverable outside the one workflow that happened to need it.

## Open questions / staleness risk

- LangGraph's exact checkpointer API (`get_state_history`, `interrupt()` signature, checkpointer backend list) should be cross-checked against `engineering-frameworks.md`'s dated verification in this same research pass — this file describes the pattern generically and should not be treated as the authoritative LangGraph API reference.
- We have not yet built `history.log` or `rollback.sh` as described above — this section is a proposed design, not a shipped one. Flag for a follow-up SDD task if adopted.
- The ghost-state-dir incident is dated to "ship 43" during the ultimate-guide v8 run (2026, exact date not in the memory file) — treat the incident date as approximate; the fix (guard clause in `mark.sh`) is confirmed present in the current file as of 2026-08-03.
