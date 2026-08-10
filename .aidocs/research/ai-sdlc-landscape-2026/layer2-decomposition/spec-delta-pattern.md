# Spec-Delta Pattern (tool-independent)
**Layer:** 2 — Decomposition · **Verdict:** 🟢 take — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is

The spec-delta pattern is the document shape underneath OpenSpec, extracted from the tool. The claim: **a change document should describe only what changes**, against a baseline that lives elsewhere and is never restated. Three moving parts:

1. A **baseline** that is a real file on disk and the single source of truth (for us: `.aidocs/project-spec/`).
2. A **delta** carried by the change, expressed as explicit operations — added / changed / removed / renamed — each naming the baseline element it touches.
3. An **archive step** that merges the delta into the baseline and moves the change aside, so the baseline is always current and the change history is always replayable.

Adopting it costs no installation, no Node, no new CLI. It is a writing convention plus a merge discipline. That is why it gets 🟢 while OpenSpec itself gets 🟡.

## Current state

The pattern has no version and no owner. Its dated reference points:

| Item | Value | As of |
|------|-------|-------|
| Canonical implementation | OpenSpec v1.7.0 (2026-07-29), 63,637 stars, MIT | 2026-08-03 |
| Longest-running instance | OpenSpec's own repo: 36 capability specs, **83 archived changes**, oldest `2025-08-05-initialize-typescript-project` | 2026-08-03 |
| Taxonomy | Böckeler's spec-first / **spec-anchored** / spec-as-source ladder — the delta pattern is the operational form of spec-anchored | published 2025-10-15 |
| Published token benchmark | Jamie Telin, IT Chronicles (Medium), **published 2026-03-18** | 2026-08-03 |
| Our baseline instance | `faion-cli/.aidocs/project-spec/`: 58 md files, 25,042 words | 2026-08-03 |
| Our feature specs | `faion-cli/.aidocs/features/done/*/spec.md`: **22 files, 22,819 words** (22,343 body words excl. headers), avg 1,037 words ≈ ~1,400 tokens | 2026-08-03 |
| Our methodology coverage | `skills/faion/knowledge/sdd/` — `project-spec-structure` v1.0.0, tier `solo`, last reviewed **2026-05-25**. **No** `spec-delta-format` methodology. **No** EARS methodology anywhere in the corpus | 2026-08-03 |

## Mechanics

### The proposed template, assessed section by section against OpenSpec

The shape under review:

```
# CHANGE-<id>: <title>
## Baseline (what the system does now)   ← never edited inside the change doc; quoted only
## Delta (what changes)
### Added / ### Changed / ### Removed
## Unchanged (explicit)                   ← mandatory section
## Requirements (EARS)
## Status: Proposed | Applied | Archived
```

| Section | OpenSpec's real equivalent | Assessment |
|---------|---------------------------|------------|
| `# CHANGE-<id>: <title>` | directory name `changes/<change-id>/`; no ID inside the doc | **Change.** The ID belongs to the directory, not a heading. A heading ID drifts from its folder the first time you rename the folder. Our lifecycle already encodes this: `feature-021-auth-tier-gated-content/`. |
| `## Baseline … quoted only` | **Nothing.** OpenSpec never quotes the baseline into the change. The delta names requirements by header; the baseline is the file on disk | **Change — this is the pattern's own anti-pattern.** Quoting the baseline reintroduces exactly the restatement the delta exists to eliminate, and the quote goes stale the moment another change lands. Replace with a *reference*: capability path + requirement IDs + the git ref the delta was authored against. A pointer cannot drift; a quotation must. |
| `## Delta` / `### Added / Changed / Removed` | `## ADDED Requirements` / `## MODIFIED Requirements` / `## REMOVED Requirements` / **`## RENAMED Requirements`** | **Change — one section missing.** RENAMED is not decoration. Without it every rename is a REMOVE + ADD pair that loses the requirement's identity, its scenario history, and every cross-reference pointing at it. OpenSpec applies RENAMED *first*, before REMOVED, precisely so a rename and a removal in the same change cannot be confused. Add it. |
| `## Unchanged (explicit)` — **mandatory** | **Nothing.** No such concept anywhere in OpenSpec's format, parser, validator, or merge engine | **Ceremony as written.** Full argument below — I commit to dropping it. |
| `## Requirements (EARS)` | `### Requirement: <name>` + a body containing `SHALL`/`MUST`, then `#### Scenario:` blocks with `**WHEN**` / `**THEN**` / `**AND**` | **Keep, with a correction.** EARS is a template for the *requirement sentence*; it does not replace scenarios. Structurally these compose perfectly — EARS produces the one-line SHALL statement, Given/When/Then produces the acceptance scenarios beneath it. But EARS must not be a separate section: requirements belong *inside* the delta operations, because a requirement's operation (added vs changed) is the whole point. A separate `## Requirements` section detaches them from their verbs. |
| `## Status: Proposed \| Applied \| Archived` | **Nothing.** Status is *location*: `changes/<id>/` = in flight, `changes/archive/YYYY-MM-DD-<id>/` = archived | **Drop.** A status field inside a document that also lives in a state directory is a second source of truth for the same fact, and it will drift — every time. Our lifecycle already is the status: `backlog/ → todo/ → in-progress/ → done/`. One place, no sync. |

### The verdict on `## Unchanged (explicit)` — committed

**It is ceremony. Drop it as a mandatory section.** Five reasons, in descending weight:

1. **It is unbounded by construction.** "What changes" is finite and enumerable; "what does not change" is the entire rest of the system. Any author faced with an infinite set writes an arbitrary, unfalsifiable sample of it. A mandatory section whose correct content is undefinable produces filler.

2. **It is unverifiable.** Every other section of a delta is machine-checkable — does this requirement exist in the baseline, does it carry SHALL, does it have a scenario, does the merge apply cleanly. "Unchanged" can only be checked by proving a negative across the whole baseline. A section no validator can gate is a section that rots silently.

3. **It goes stale faster than anything else in the document.** A delta's Added/Changed/Removed blocks are consumed by the archive step and then frozen as history. An "Unchanged" list makes a claim about the *rest of the baseline* — which other changes are mutating in parallel. By archive time it may be false, and nothing will have noticed.

4. **We already have the bounded version, and it is in 19 of our 22 specs.** `## Out of Scope` appears in 19/22 `spec.md` files in `faion-cli/.aidocs/` (1,031 words total; a further 3 use `## Scope` with an out-of-scope subsection). Out-of-Scope is the *useful* half of "Unchanged": it is bounded to the things a reader of *this change* would plausibly expect it to cover. That is the anti-scope-creep guard the proposal is reaching for, and we've been shipping it since feature-001.

5. **The real failure mode it targets has a better, automatic fix.** The genuine risk is not that the author forgets to promise nothing else changed — it is that an LLM rewriting a requirement block **silently drops a scenario or a clause it did not think was important.** A prose promise does not catch that. OpenSpec's **scenario-loss check** does, mechanically: on `MODIFIED`, it compares the delta block's `#### Scenario:` set against the baseline block's, and **aborts the archive** if the delta omits one the baseline still carries (`findMissingCurrentScenarios`, hard error, issue #1477). That is "Unchanged (explicit)" implemented as a diff rather than a promise — bounded, verifiable, and impossible to write filler into.

**What to keep of the intent.** One narrow, bounded, *optional* form earns its place: when a change MODIFIES a requirement, a `**Preserved:**` line inside that requirement's block naming the scenarios/clauses deliberately carried over unchanged. Bounded to the requirement being touched, one line, and directly checkable against the scenario-loss rule. Everything wider than that is prose about the universe.

### The archive procedure

Adapted from `specs-apply.ts` v1.7.0, stripped of what only exists because OpenSpec keys requirements on their title string. Our IDs are stable (`FR-NNN` / `REQ-NNN` per `sdd/spec-requirements`), which removes the rename-chain walking and the near-miss typo detection entirely — the two most complex parts of their implementation.

```
1. GATE      Delta validates clean; every ID in Changed/Removed/Renamed exists in the
             baseline; no ID appears in two operation sections; every Added/Changed
             requirement carries SHALL/MUST and ≥1 scenario. Any failure → stop, nothing moves.

2. RESOLVE   Load the baseline files the delta names. If a target file does not exist:
             Added only. Changed/Renamed against a missing baseline → hard error.
             Removed against a missing baseline → warn, skip.

3. APPLY     In this order, non-negotiable:  RENAMED → REMOVED → CHANGED → ADDED
             - RENAMED  old missing ∧ new present → already applied, no-op.
                        old missing ∧ new missing → error.  new already present → error.
             - REMOVED  missing → warn "already removed", continue. present → delete.
             - CHANGED  missing → error.
                        baseline scenarios ⊄ delta scenarios → ERROR (scenario loss).
                        identical content → no-op (don't count, don't rewrite).
             - ADDED    present ∧ identical → no-op. present ∧ different → error.

4. RECOMPOSE Preserve original baseline ordering for surviving requirements;
             append new ones at the end. Collapse 3+ blank lines to 2.

5. VERIFY    Re-read every touched baseline file. Confirm: Added present, Changed applied,
             Removed gone, Renamed under the new name and not the old.
             Mismatch → stop. NOTHING has moved yet, so it is safe to fix and retry.

6. MOVE      in-progress/<feature>/ → done/<feature>/, delta preserved verbatim as history.

7. COMMIT    One commit: baseline edits + feature move + CHANGELOG entry. Same PR as the code.
```

Steps 5-before-6 is the ordering that matters and the one OpenSpec got wrong until v1.7.0 (2026-07-29): their archive handed the spec sync to a background task and moved the change folder immediately, so a change could end up archived, the baseline never updated, and the summary still printing `Specs: ✓ Synced`. Verify, then move. Never the reverse.

Step 7 is not OpenSpec's — it is ours, from `project-spec-structure/content/03-delta-update.xml`: the spec delta lands in the same PR as the code, with a `readiness.md` checkbox blocking merge and a written one-line reason required for "no spec impact." Keep it. It is the strictest rule in either system.

### The final recommended template

```markdown
# <feature-id> — <title>

**Baseline:** `.aidocs/project-spec/` @ <git-sha-or-tag>
**Touches:** auth.md · business-rules.md · api/endpoints/search.md
<!-- Reference, never a quotation. The baseline is a file, not a paragraph. -->

## Why
<2-6 sentences. The problem, in the user's terms. Non-empty is the only rule.>

## Out of Scope
- <bounded list of things a reader of THIS change would expect it to cover, and it doesn't>

## Delta

### ADDED

#### FR-014 — <short name>
The system SHALL <one EARS-shaped normative sentence>.

##### Scenario: <name>
- **GIVEN** <precondition>        (optional)
- **WHEN** <trigger>
- **THEN** <observable outcome>
- **AND** <further outcome>       (optional)

### CHANGED

#### FR-007 — <short name>
<the COMPLETE new requirement body — this replaces the baseline block>
**Preserved:** Scenario "expired token", Scenario "tier downgrade"
<!-- optional, bounded; the scenario-loss check verifies it mechanically -->

##### Scenario: <name>
- **WHEN** …
- **THEN** …

### REMOVED
- FR-003 — <name>  · reason: <one line>

### RENAMED
- FROM: FR-011 — <old name>
- TO:   FR-011 — <new name>
<!-- ID stays. Only the title moves. This is why we don't need rename-chain walking. -->

## Project-spec delta (lands in same PR)
- `business-rules.md` — BR-019 added: <one line>
- `auth.md` — email verification section updated
- <or: "no spec impact — <reason>">
```

Notes on the choices:

- **No `## Status`.** The directory is the status.
- **No `## Baseline` body.** A path and a git ref. Two lines.
- **No `## Unchanged`.** `## Out of Scope` (which we already write) plus the mechanical scenario-loss check.
- **EARS shapes the SHALL sentence**, it is not a section. The five useful templates: *ubiquitous* ("The system SHALL …"), *event-driven* ("WHEN <trigger>, the system SHALL …"), *state-driven* ("WHILE <state>, the system SHALL …"), *optional-feature* ("WHERE <feature is included>, the system SHALL …"), *unwanted-behaviour* ("IF <condition>, THEN the system SHALL …"). They cost nothing structurally and they kill the vague-requirement failure mode that `sdd/spec-requirements` already forbids by other means.
- **Requirement IDs live inside the operation blocks**, not in a detached `## Requirements` section, so the verb and the requirement never separate.
- **`## Project-spec delta` is ours and stays.** It already appears verbatim as a section in one of our shipped specs (`## Project-spec delta (lands in same PR)`), which means the discipline is real and not aspirational.

## The token argument, quantified

### Their number — verified, with the date corrected

**Source:** Jamie Telin, *"Is Your Safe Choice Burning Your Budget?"*, IT Chronicles on Medium, **published 2026-03-18** (not 2026-06-03 — the prior pass's date is wrong; 2026-06-03 is the release date of OpenSpec v1.4.1, likely a conflation).

Verified figures:

| Metric | OpenSpec | Spec-Kit | Delta |
|--------|----------|----------|-------|
| **Test 2 total** | **91,729** | **181,040** | +97% |
| Test 2 — planning phase | 38,117 | 96,298 | +152% |
| Test 2 — implementation phase | 53,612 | 84,742 | +58% |
| **Test 1 total** | 57,740 | 120,947 | +109% |
| Assistant turns (both runs) | baseline | — | OpenSpec ~**20% fewer** |
| Tool calls (both runs) | baseline | — | OpenSpec ~**25% fewer** |

The 91,729 / 181,040 pair and the ~20%-fewer-turns claim in the prior pass are **correct**. Task: implementing streaming + session support (list / open / delete / new) in an MVP-state AI chat app. Agents: GPT-5.2 and GPT-5.2-Codex. Repo: `knowit-flx/workshop-1-2026`. Qualitative finding: Spec-Kit needed autonomous bug-fixing rounds to get streaming status right; OpenSpec was correct first pass.

**Methodology caveats — this is n=2, not a benchmark:**

1. **Two runs, one task, one codebase, one domain.** No repetitions, no variance reported, no confidence interval. The two runs disagree by a factor of 1.6× on OpenSpec's own total (57,740 vs 91,729), which is itself evidence that run-to-run variance is large relative to the effect being measured.
2. **Neither tool version is stated.** Between the plausible authoring window and publication, OpenSpec moved through 1.1.x–1.2.x. Spec-Kit's version is likewise unnamed.
3. **The comparison is confounded by workflow, not just format.** Spec-Kit's flow produces constitution + spec + plan + tasks + implement as separate artifacts by design; OpenSpec produces proposal + delta + tasks. A large part of the 97% is "Spec-Kit writes more documents," not "full specs cost more tokens than deltas." The benchmark cannot separate the two.
4. **Author proximity.** The source repo was built for a spec-driven-development workshop the author ran. Familiarity with one tool's prompting is a real and unquantified variable.
5. **Wrong model family for us.** GPT-5.2 / GPT-5.2-Codex. Our stack is Claude. Context handling, tool-call economy, and re-read behaviour differ enough that the ratio does not transfer cleanly.
6. **No cost-of-error accounting.** "Spec-Kit needed bug-fixing rounds" is arguably the finding that matters most, and it is reported qualitatively with no attempt to price it.

**Honest read:** directionally credible, magnitude unreliable. Treat "delta-based flows are meaningfully cheaper than full-artifact flows, plausibly 1.5–2×" as the takeaway; do not quote 97% as a property of the format.

### Our number — measured today

Measured on `~/workspace/projects/faion-net/faion-cli/.aidocs/` on **2026-08-03**, excluding one archived/superseded spec:

```
22 spec.md files in features/done/     22,819 words total (22,343 body words)
                                       avg 1,037 words/feature ≈ ~1,400 tokens
                                       corpus total ≈ ~30,800 tokens
```

Word split by section, across all 22:

| Section | Words | Share |
|---------|-------|-------|
| Functional Requirements | 8,402 | 37.6% |
| Acceptance Criteria | 5,904 | 26.4% |
| **→ change-specific subtotal** | **14,306** | **64.0%** |
| Problem | 1,580 | 7.1% |
| Goal | 1,348 | 6.0% |
| Out of Scope | 1,031 | 4.6% |
| Scope | 852 | 3.8% |
| Boundaries | 821 | 3.7% |
| Non-Functional Requirements + Non-functional | 572 | 2.6% |
| Why | 391 | 1.8% |
| Traces To | 289 | 1.3% |
| preamble / other | 1,153 | 5.2% |
| **→ context & restatement subtotal** | **8,037** | **36.0%** |

**What delta-only would actually save us on the write side: about 500 tokens per feature — and that is the ceiling, not the estimate.**

The arithmetic: 8,037 restatement words ÷ 22 features = 365 words/feature ≈ **~490 tokens**. But `Problem`, `Goal` and `Why` are genuinely change-specific and would survive any delta format; only `Boundaries`, `Traces To`, parts of `Scope`, and the NFR restatement are true baseline duplication. The realistic saving is **~150–250 tokens per feature**, roughly **10–18%** of a spec, and about **4,000 tokens across the entire 22-feature history**.

That is a rounding error. **Our specs are already 64% delta.** The delta-only rule in `project-spec-structure` is largely working; the remaining duplication is small enough that adopting OpenSpec's format for token reasons alone would not pay for the migration.

**Where the real money is — and we already have it.** Reframe the question from "what does it cost to write a spec" to "what does it cost an agent to answer *what does this system do right now?*":

| Route | Cost |
|-------|------|
| Reconstruct current state from 22 feature specs | 22,819 words ≈ **~30,800 tokens** — and it is wrong, because later features supersede earlier ones with no marker |
| Load the whole `project-spec/` tree | 25,042 words ≈ ~33,800 tokens — correct, but no cheaper |
| **Routed read of `project-spec/`** — 58 files, avg 432 words, each subdir carrying its own `AGENTS.md` + `CLAUDE.md`, agent opens the 3–4 files it needs | ~1,700 words ≈ **~2,300 tokens** |

**~13× cheaper, and correct instead of merely cheap.** That is the token win the OpenSpec benchmark is actually measuring — the agent stops re-deriving the world from change history — and **we captured it in `project-spec-structure`, not in a delta format.** The delta format is what keeps the baseline honest; the routed baseline is what makes it cheap. We have the second and two-thirds of the first.

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|-------|-----|--------------|---------|
| 1 | Jamie Telin, *Is Your Safe Choice Burning Your Budget?* | https://medium.com/it-chronicles/is-your-safe-choice-burning-your-budget-1cfddf8782e4 | The only public OpenSpec-vs-Spec-Kit token benchmark. Published **2026-03-18**. Both test runs, phase split, turn/tool-call deltas, task and model details | 2026-08-03 |
| 2 | OpenSpec `src/core/specs-apply.ts` @ `45cca5d` | shallow clone of `main` | The merge algorithm the archive procedure above is adapted from; RENAMED→REMOVED→MODIFIED→ADDED; scenario-loss check | 2026-08-03 |
| 3 | OpenSpec `src/core/validation/validator.ts` + `constants.ts` @ `45cca5d` | shallow clone | Full ERROR/WARNING/INFO rule set; `--strict` = zero errors AND zero warnings | 2026-08-03 |
| 4 | OpenSpec `CHANGELOG.md` (#1437, #1475) | shallow clone | Why verify-then-move is the correct archive ordering; the background-sync bug fixed in 1.7.0 | 2026-08-03 |
| 5 | OpenSpec self-hosted `openspec/` tree @ `45cca5d` | shallow clone | 83 archived changes since 2025-08-05 — the pattern's longest continuous field test | 2026-08-03 |
| 6 | Böckeler, *Understanding Spec-Driven-Development* | https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html | The spec-first / spec-anchored / spec-as-source ladder. Published 2025-10-15 | 2026-08-03 |
| 7 | `skills/faion/knowledge/sdd/project-spec-structure/` (AGENTS.md, `content/01-04`, meta.json) | local | Folder shape, rebuild test, same-PR delta rule, location decision. v1.0.0, tier `solo`, reviewed 2026-05-25 | 2026-08-03 |
| 8 | `skills/faion/knowledge/sdd/INDEX.xml` + `spec-requirements/AGENTS.md` | local | 274-line index; FR-NNN/NFR-NNN numbering; confirms zero EARS coverage | 2026-08-03 |
| 9 | `faion-cli/.aidocs/` corpus measurement | local | 22 spec.md / 22,819 words / section split; project-spec 58 files / 25,042 words | 2026-08-03 |
| 10 | `faion-network/.aidocs/in-progress/feature-049-spec-deltas-bdd-cli/` | local | Uncommitted, never executed, written 2026-05-02. spec.md, design.md, spec-delta.md, test-plan.md, implementation-plan.md (749 lines) | 2026-08-03 |

## What to borrow for faion

1. **The four verbs, RENAMED included.** ADDED / CHANGED / REMOVED / RENAMED, with the merge order `RENAMED → REMOVED → CHANGED → ADDED`. This is the pattern's irreducible core.
2. **Baseline by reference, never by quotation.** Path + git ref. This single rule is what makes the delta small and keeps it from going stale.
3. **The scenario-loss check.** The one mechanical safeguard worth building in Go. It is the automatic form of "nothing else changed," and it catches the LLM failure mode that prose promises cannot.
4. **Verify-then-move archive ordering,** with nothing having moved when verification fails.
5. **EARS as the requirement-sentence template**, layered under our existing Given/When/Then scenarios. Zero structural cost, kills vague requirements.
6. **Three severity levels** — error / warning / info — with a `--strict` mode that promotes warnings. Lets a checker nag without blocking.
7. **New methodology for the corpus: `sdd/spec-delta-format`.** The delta shape is currently documented only inside an uncommitted feature folder. It belongs in `knowledge/sdd/` next to `project-spec-structure`, which references it.
8. **New methodology: `sdd/ears-requirement-templates`.** Verified gap — zero EARS coverage across all 23 domains. A corpus selling 2,622 methodologies with no EARS entry has a hole a buyer will notice.

## What NOT to borrow — and why

1. **`## Unchanged (explicit)` as a mandatory section.** Committed above: ceremony. Unbounded, unverifiable, stale-prone, duplicates our `## Out of Scope` (already in 19/22 specs), and the failure it targets is better caught by the scenario-loss check.
2. **`## Baseline` as quoted text.** Reintroduces the restatement the pattern exists to remove, and drifts.
3. **`## Status:` inside the document.** Duplicates the lifecycle directory. Two sources of truth for one fact.
4. **A separate `## Requirements` section.** Detaches requirements from their operation verb, which is the only thing that makes a delta a delta.
5. **A parallel `.aidocs/specs/<capability>/` tree.** F049 proposes it; it forks the baseline in two. See below.
6. **Requirement-name-as-key.** OpenSpec needs case-folding, near-miss typo detection, and rename-chain walking with a cycle guard, all because the primary key is a title string. Our stable `FR-NNN` IDs delete that entire class of code. Do not regress to titles for OpenSpec compatibility.
7. **Character-count gates on prose** (`## Why` between 50 and 1000 chars, requirement text under 500). Arbitrary, and under `--strict` they turn valid work into failures.
8. **Quoting "97% fewer tokens" as a property of the format.** n=2, one task, GPT-5.2, confounded by workflow verbosity. Directional only.

## Mapping to our corpus

**Does OpenSpec beat `project-spec-structure`? No — we beat it on three of four axes, and lose on one.**

| Axis | OpenSpec | `project-spec-structure` (v1.0.0, 2026-05-25) | Winner |
|------|----------|------------------------------------------------|--------|
| Baseline richness | requirements + scenarios only, per capability | 15+ artefact types + `domain/`, `api/`, `integrations/`, `decisions/` subtrees; 58 files in the faion-cli instance | **Us** |
| Retrieval economy | agent reads whole capability spec | per-subdir `AGENTS.md`+`CLAUDE.md` routing; ~2,300 tokens for a routed read vs ~33,800 for the tree | **Us** |
| Acceptance bar | validator exit code | **rebuild test** — a mid-level dev rebuilds the project in two weeks from `project-spec/` + `ui-ux-design.md` + `constitution.md`; runs at end-of-feature and pre-deploy after every CR/BUG | **Us** |
| Delta enforcement | 20+ hard parser errors, machine-checked, blocks archive | same-PR rule + reviewer diff check + `readiness.md` checkbox + written reason for "no spec impact" — all **human-enforced** | **OpenSpec** |

The one loss is the one that matters most for a solopreneur: on a solo project the author and the reviewer are the same person, and `03-delta-update.xml` names that blind spot explicitly ("the author has a blind spot — they wrote the code and the spec from the same mental model"). Our answer to it is a second pair of eyes we do not have. **A deterministic Go checker is the substitute for the reviewer we structurally cannot hire.** That is the strongest single argument for building this.

Concrete corpus actions:

- **`sdd/project-spec-structure`** — add a `content/05-delta-format.xml` (or a sibling methodology) pinning the four verbs, the merge order, and the scenario-loss rule. `03-delta-update.xml` currently mandates the same-PR delta without ever defining what a delta *looks like*.
- **`sdd/spec-structure`, `spec-requirements`, `spec-advanced-guidelines`, `writing-specifications`** — all describe a *full* spec. At minimum, cross-link to the delta variant so an agent reading them for a brownfield feature doesn't produce a full rewrite.
- **New: `sdd/ears-requirement-templates`** — verified zero coverage.
- **New: `sdd/spec-driven-development-rungs`** — the spec-first / spec-anchored / spec-as-source ladder, with Tessl as the worked failure of the top rung (see `tessl.md`).
- **`readiness-checklist`** — add the delta-validation gate alongside the existing spec-impact checkbox once a checker exists.

### On F049 — I agree with the prior pass, with two additions

Read in full: `spec.md` (181 lines), `design.md` (193), `spec-delta.md` (162), `test-plan.md` (112), `implementation-plan.md` (101). Written **2026-05-02**, sitting in `.aidocs/in-progress/`, uncommitted, never executed.

Agreed with the prior recommendation to **REVISE**, on every point:

- **Kill `.aidocs/specs/<capability>/`.** F049 explicitly lists it as Goal 1 and creates three capability specs (`sdd-lifecycle`, `sdd-cli`, `sdd-bdd`). This is a second living-spec tree beside `project-spec/` — the exact drift F049's own "Why" section says it exists to prevent. `project-spec/` is strictly richer and already has the rebuild test as its acceptance bar. Deltas target `project-spec/` files.
- **Kill the Python module.** `design.md` specifies `faion_cli/sdd/{cli,parser,delta,validator,linter,archiver,differ,lister,grammar}.py` and `spec.md`'s Risks table says "faion-cli Python codebase grows". `faion-cli` is a Go single binary and ships no runtime interpreter. This section is a straight artifact of pre-pivot drafting.
- **Kill `faion sdd diff`.** OpenSpec shipped `diff`, deprecated it in v0.2.0, and pointed users at `show`. Simulating a post-merge view duplicates the merge engine for no gain; `git diff` after the merge answers the same question for free.
- **Drop `test-plan.md` from the validated set.** F049's success criteria require "All BDD scenarios in this spec have matching test cases in test-plan.md" — a hand-maintained mapping between two documents that will drift by the second feature. The scenarios *are* the test contract.
- **Add RENAMED.** F049 has only ADDED/MODIFIED/REMOVED throughout `spec.md`, `spec-delta.md`, and `design.md`.

Two things the prior pass did not flag, both of which I would add to the revision:

- **Add the scenario-loss check.** F049's MODIFIED is defined in `design.md` as "*full new body — replaces existing entry*" — byte-for-byte OpenSpec's design, and therefore byte-for-byte its silent-scenario-drop hazard. F049 has no detector. Given that our specs will be regenerated by LLMs, this is the highest-value single rule in the whole feature and it is missing.
- **Drop the `.next-id` lock file.** `design.md` has `archive` reserving capability-scoped IDs in `.aidocs/specs/<cap>/.next-id`. A lock file mutated by an archive command is a merge-conflict generator in a git-tracked tree, and it exists only to serve the capability-scoped ID scheme that goes away with `.aidocs/specs/`. Feature-scoped or file-scoped `FR-NNN` needs no allocator.

One thing F049 got **right** and the revision must preserve: its BDD grammar section (`REQ-sdd-bdd-002`) demands a *strict* keyword set `{GIVEN, AND, WHEN, THEN}` formatted as `- **<KEYWORD>** <text>`, and rejects `WHENEVER`. OpenSpec does not validate scenario keywords at all — `countScenarios` matches any `####` header. F049's strictness is genuinely better than the tool that inspired it, and it is cheap to enforce.

**Net:** F049 is a good instinct with a stale implementation. Rewrite `design.md` around Go + `project-spec/` as the single baseline, add RENAMED and the scenario-loss check, delete `differ.py`, `.next-id`, and the `.aidocs/specs/` tree. The `spec.md` "Why" section survives intact — it diagnosed the problem correctly on 2026-05-02.

## Open questions / staleness risk

- **The benchmark is the weakest evidence in this dossier.** One author, one task, n=2, GPT-5.2. If token economics ever become load-bearing for a Faion product decision, run our own: same feature, full-spec vs delta, Claude, three repetitions. Until then cite it as directional.
- **The ~500-tokens-per-feature ceiling is measured on `faion-cli` only** — 22 features, one Go CLI, one author. Other repos with chattier specs would show more duplication. The 36% context share is not a universal constant.
- **The routed-read figure (~2,300 tokens) is an estimate**, from 58 files × 432 avg words assuming an agent opens 3–4. Not instrumented. Worth measuring against real session transcripts before it appears in customer-facing material.
- **`project-spec-structure` v1.0.0 was last reviewed 2026-05-25** — before this research. Any delta-format addition should bump the version and `last_reviewed`.
- **Unresolved design question:** should a delta be a separate `spec-delta.md`, or should `spec.md` simply *be* the delta? F049 chose separate files; `project-spec-structure` implies `spec.md` is already delta-only when `project-spec/` exists. Two files means two things to keep consistent; one file means the delta verbs live inside a document that also carries Why / Out of Scope. **My lean: one file** — the recommended template above is a single `spec.md`, because 22 features of evidence say our `spec.md` is already 64% delta and does not need a sibling. Not settled; it is the first decision the F049 revision has to make.
- **Staleness horizon: ~3 months** for the OpenSpec-derived mechanics (they ship monthly minors); indefinite for the pattern itself, which is a document shape and does not have a release cadence.
