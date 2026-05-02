---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
applies_to: skills/faion/workflows/<slug>/
---

> **For:** workflow authors (LLM agent or human). **Prereqs:** `rules/skill-authoring.md`, `docs/skill-authoring.md`. **You will:** create or audit a `skills/faion/workflows/<slug>/` folder that delivers a multi-phase orchestration pattern.

**TL;DR**

- A workflow is a versioned, phase-graph orchestration pattern under `skills/faion/workflows/<slug>/`. The orchestrator is always Claude in the active session; subagents are spawned via `Agent` with versioned prompt files.
- Folder is `AGENTS.md` (≤80 lines) + numbered `content/*.xml` (semantic XML) + optional `templates/`, `playbooks/`, `prompts/`, `scripts/`.
- Phase = quad-block: Inputs · Pre-conditions · Steps · Outputs · Post-conditions · Constraints · Failure-routing · Done. Failure routing lives **only** inside `<phase>`.
- Workflow owns phase order. Playbooks adapt surface choices.
- Workflows MAY cite methodologies for cross-cutting concerns; playbooks MUST cite methodologies for surface-specific knowledge.

---

## 1. Definition + position

A **workflow** is a versioned orchestration pattern that drives a multi-phase delivery from intake to close inside one Claude Code session. It encodes:

- the phase graph (ordered phases, allowed transitions, terminal states);
- the output contract (what each phase emits so the orchestrator can decide next phase);
- the tool budget (which tools each phase may use);
- the failure routing (what happens on hook fail, conflict, quota, schema violation).

Workflows live under `skills/faion/workflows/<slug>/`.

**Diátaxis position:** *reference + explanation*. The doc tells the agent what is true and why. It does not teach by example (that is what `playbooks/<surface>.md` and `prompts/*.md` are for).

**Boundary with playbook:**
- Workflow = phase order, output contract, tool allowlist budget, idempotency class, failure-routing classes (canonical).
- Playbook = per-surface adaptation (verify command, test runner, deploy script, file-grouping heuristics, deploy gates).
- A playbook **never** changes phase order or introduces new phase ids.

## 2. When to author one vs. reuse

Add a new workflow when **all** apply:
- The orchestration pattern is genuinely new (not "same flow, different surface").
- It will host ≥2 distinct surface playbooks within 6 months.
- An existing workflow would need ≥3 phase-shape overrides to fit — not just per-surface choices.

Otherwise:
- Same orchestration, new surface → add a playbook under the existing workflow.
- Same orchestration, one phase tweak → note in the existing playbook, do not fork.
- One-off feature delivery → use `/faion` (sdd-batch-orchestrator workflow), not a workflow.

## 3. Folder shape ("I am here" map)

```
skills/faion/workflows/<slug>/
├── CLAUDE.md            @AGENTS.md
├── AGENTS.md            ≤80 lines · routing + file table + invariants
├── content/             required · numbered semantic XML
│   ├── 01-overview.xml
│   ├── 02-phases.xml
│   ├── 03-prompt-files.xml
│   ├── 04-parallelism.xml
│   ├── 05-defaults-constraints.xml
│   ├── 06-...
│   └── NN-anti-patterns.xml
├── decisions.xml        required · why this shape, what was rejected (§13)
├── templates/           optional · reusable artifacts referenced by content
├── prompts/             optional · per-phase prompt files (§3.1)
├── playbooks/           optional · per-surface adaptations
└── scripts/             optional · validators, smoke replays
```

**Required:** `CLAUDE.md`, `AGENTS.md`, `content/`, `decisions.xml`.
**Optional:** `templates/`, `prompts/`, `playbooks/`, `scripts/`.

### When to add each optional folder

| Folder | Add when |
|--------|----------|
| `templates/` | A reusable XML/JSON/script artifact is referenced from more than one phase or playbook. |
| `prompts/` | A phase dispatches a subagent and the prompt is ≥30 lines or shared across phases. Inline `<steps>` for shorter prompts. |
| `playbooks/` | A second concrete delivery surface comes online (the first surface's choices may live in `content/` until then). |
| `scripts/` | The workflow needs a smoke replay, a fixture-loader, or a domain validator beyond `validate-methodology-xml.py`. |

## 4. AGENTS.md contract

Hard cap: **80 lines** including front-matter and code fences. Spillover goes to `.agents/<topic>.md`.

### Required front-matter (YAML)

```yaml
---
status: draft | active | deprecated
audience: agent | human | both        # almost always "both"
owner: <handle>
last_verified: YYYY-MM-DD
version: <semver>                      # workflow.version, see §10
applies_to: <surface tag or "any">
supersedes: <previous slug or null>
---
```

### Required H2 sections (in order)

1. `## Summary` — one paragraph: what this workflow orchestrates.
2. `## Why` — one paragraph: what improvises without it (the failure mode it prevents).
3. `## When To Use` — bullet list of triggers.
4. `## When NOT To Use` — bullet list of anti-triggers.
5. `## Content` — table mapping `content/*.xml` files to one-line descriptions.
6. `## Templates` — table of `templates/` files (skip if folder absent).
7. `## Related` — links to siblings, parents, references.

`## Phases (canonical)` is **not** in AGENTS.md — it lives in `content/02-phases.xml`. AGENTS.md is the routing card; phase definitions are reference material.

## 5. content/*.xml shape

Files are numbered `01-`, `02-`, … in canonical reading order. Each is parseable as semantic XML against the closed tag glossary at `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml`.

### Why semantic XML, not Markdown

- Closed tag vocabulary → deterministic retrieval (`grep '<phase id="3"'` always works).
- Validator catches schema drift before commit.
- Diff reviews stay mechanical when tags are renamed.
- Markdown is for human-facing prose; XML is for machine-checked contract.

### Validator

```bash
python3 scripts/validate-methodology-xml.py skills/faion/workflows/<slug>/content/<file>.xml
```

A missing required attribute, an unknown tag, or a phase without `id` fails the run.

## 6. Phase quad-block schema (C3) — the contract

Every phase in `content/02-phases.xml` (or the equivalent phase-listing file) MUST conform to this skeleton:

```xml
<phase id="<kebab-id>" version="<semver>" idempotency="pure|converging|side_effect">
  <inputs>
    <var name="<name>" type="string|enum(...)|bool|path|list" required="true|false" default="..."/>
  </inputs>

  <pre-conditions>
    <assert>git status --porcelain is empty</assert>
    <assert>cwd matches <repo-path></assert>
    <assert>op-unlock executed if secrets needed</assert>
  </pre-conditions>

  <steps>
    <!-- Imperative steps OR <prompt-ref path="prompts/<name>.md" version="^X.Y"/> -->
  </steps>

  <outputs>
    <out name="<name>" type="..."/>
    <done-marker regex="^(done|verdict)=\S+( \w+=\S+)*$"/>
  </outputs>

  <post-conditions>
    <assert>verify command exits 0</assert>
    <assert>commit exists with title matching <type>: <short></assert>
  </post-conditions>

  <constraints>
    <tool-allowlist>Read, Grep, Glob, Edit, Bash</tool-allowlist>
    <forbid>git push to origin/main without confirm</forbid>
  </constraints>

  <failure-routing>
    <on condition="hook-fail" action="fix-root-cause" next="same-phase"/>
    <on condition="merge-conflict" action="emit-verdict-fail" next="abort"/>
    <on condition="quota" action="park-loop" next="schedule-wakeup"/>
    <on condition="schema-violation" action="emit-verdict-fail" next="abort"/>
  </failure-routing>

  <done-condition>
    <!-- One sentence the orchestrator can check to declare success. -->
  </done-condition>
</phase>
```

**Failure-routing rule (load-bearing):** `<failure-routing>` lives **only** inside `<phase>`. A workflow MUST NOT carry a top-level routing table. Cross-phase routing is the orchestrator's responsibility, expressed via `next=` per failure class.

### Worked example

See `skills/faion/workflows/sdd-batch-orchestrator/content/02-phases.xml` for a fully-populated phase set. The `verify` phase is the canonical reference for `verdict=PASS|FAIL` emission.

## 7. Tool allowlist per phase (C7)

Each `<phase>` MUST carry `<tool-allowlist>` listing the exact tools its subagent (or the orchestrator, if `<actor>orchestrator</actor>`) may invoke. Defaults are denied.

- Read-only phases (study, clarify, review): `Read, Grep, Glob, WebFetch, WebSearch, AskUserQuestion`.
- Mutating phases (wave-execute, fix, deliver): add `Edit, Write, Bash`.
- Never grant `Agent` recursively unless the phase is explicitly an orchestrator dispatch.
- Never grant `Bash` without a `<failure-routing>` row for `hook-fail`.

A playbook MAY tighten the allowlist for its surface, never expand it (the workflow allowlist is the **budget**).

## 8. Idempotency classes (C5)

Mandatory `idempotency` attribute on every `<phase>`:

| Class | Meaning | Re-entry guard required? |
|-------|---------|--------------------------|
| `pure` | Re-run produces identical output, no side effects. | No. |
| `converging` | Re-run reaches same final state from any intermediate state. | Optional, recommended. |
| `side_effect` | Re-run is unsafe without explicit guard (commit, push, deploy, DB write). | **Yes — declare in `<pre-conditions>`.** |

### Re-entry guards (canonical patterns)

- Marker file: `.aidocs/<feature>/lifecycle/<phase>.done` exists ⇒ skip phase.
- Lock file: `flock -n /tmp/<repo-slug>-merge.lock` (e.g. `/tmp/faion-network-merge.lock`).
- Git-state probe: `git log --grep="<commit-marker>" -1` non-empty ⇒ already applied.

Pinned lock-file path convention: `/tmp/<repo-slug>-merge.lock` for merge serialization, `/tmp/<repo-slug>-<phase>.lock` for phase-level guards. TTL 6 hours.

## 9. Output contract grammar (C4)

Every phase emits a **last-line marker** that the orchestrator parses with one regex:

```
^(done|verdict)=\S+( \w+=\S+)*$
```

| Phase kind | Required marker | Examples |
|------------|-----------------|----------|
| Mutating (commit, deploy, write) | `done=<phase-id> commit=<sha> ...` | `done=wave-execute commit=abc1234 files=7` |
| Verification (lint, build, test, review) | `verdict=PASS\|FAIL\|FAIL-WITH-NITS ...` | `verdict=PASS coverage=0.92` |
| Read-only (study, clarify) | `done=<phase-id> ...` | `done=study features=4` |

### Emission contract

- The **subagent prompt file** is responsible for emitting the marker as the literal last line of stdout.
- The **orchestrator** reads the subagent's final message, regex-matches the last non-empty line, and routes by the parsed `verdict=` or `done=` value.
- Body above the marker may stream prose; structured payloads use fenced ```json blocks.
- A subagent that does not emit a valid last-line marker is treated as `verdict=FAIL reason=marker-missing`.

## 10. Versioning + compatibility (C2)

Three independent SemVer axes:

| Axis | Carrier | Bumps when |
|------|---------|------------|
| `workflow.version` | `AGENTS.md` front-matter | Phase added/removed/reordered (major); new optional input (minor); doc-only fix (patch). |
| `prompt.version` | `prompts/<name>.md` front-matter | Output contract or required input changes (major); behavior tweak (minor); typo (patch). |
| `playbook.version` | `playbooks/<surface>.md` front-matter | Required-section change (major); new surface choice (minor); cmd update (patch). |

### Compat ranges

- Each playbook declares `verifies_against: <range>` (e.g. `^1.4`) against the workflow it adapts.
- Each `<prompt-ref>` in `content/` declares `version="^X.Y"` against its prompt file.
- A workflow major bump requires a `MIGRATION.md` next to `AGENTS.md` with: removed inputs, renamed outputs, replacement workflow.

### Worked bump example

Workflow `sdd-batch-orchestrator` is at `1.4.2`. We add a new phase `12-archive` at the end. Phase set changed → bump to `1.5.0` (additive, not breaking). Playbook `faion-network-knowledge.md` declared `verifies_against: ^1.4` → still satisfied (1.5.0 ∈ ^1.4 = [1.4.0, 2.0.0)). No migration needed. CHANGELOG entry: `feat: add archive phase to sdd-batch-orchestrator (1.5.0)`.

If instead we removed phase `08-recapture`, that is breaking → bump to `2.0.0`, write `MIGRATION.md`, every playbook re-declares `verifies_against: ^2.0`.

## 11. Plan-then-apply / dry-run (C9)

Every `idempotency="side_effect"` phase MUST support a `dry_run: true` input that:

- runs all read-only steps,
- emits a `<plan>` artifact at `.aidocs/<feature>/plans/<phase>.xml` (paths to be touched, commands to be run, branches to be moved),
- emits a `verdict=PLAN files=N commands=M` marker,
- performs **no** mutation.

The corresponding apply run validates the plan artifact is fresh (≤24h, hash-matched) before mutating.

Workflows MAY declare a global `dry-run-mode` element in `content/01-overview.xml` mapping mutating phases to no-op surrogates (`git diff` instead of commit, `echo` instead of deploy).

## 12. Drift sentinels (C8 — Tier-1 subset)

Mandatory checks (run via `bash scripts/validate-workflow.sh <slug>`, fail commit if any fail):

- Every `<reference path="">` and Markdown link in `AGENTS.md` + `content/*.xml` resolves to an existing file.
- `AGENTS.md` ≤ 80 lines.
- Every `content/*.xml` validates against the tag glossary.
- `last_verified` in front-matter is within 90 days for `status: active` workflows.
- Every `<prompt-ref>` resolves to an existing prompt file with matching version range.
- Every `<methodology-ref path="...">` resolves to an existing folder under `skills/faion/knowledge/`.

Deferred to v2: per-phase telemetry envelope, full smoke-replay harness, automated `verifies_against` matrix.

## 12.5. Methodology references (cross-cutting)

A workflow MAY cite methodologies from `skills/faion/knowledge/<tier>/<group>/<skill>/<methodology-slug>/` for cross-cutting principles that apply to the workflow as a whole or to a specific phase regardless of surface (e.g. semantic-xml-content for prompt files, code-review-checklist for the review phase). Surface-specific methodologies belong in playbooks (see `playbook-spec.md` §6.5).

### Where workflow methodology references appear

- **AGENTS.md `## Related` section** — cross-cutting methodologies that inform the whole workflow. One link per row.
- **Phase XML** — inline `<methodology-ref path="<tier>/<group>/<skill>/<methodology-slug>" reason="<one line>"/>` element inside `<constraints>` or `<steps>`. The element is part of the closed tag glossary; validator resolves the path.

### Rules

- Path is relative to `skills/faion/knowledge/`. Broken paths fail CI.
- Tier of the cited methodology must be ≤ the workflow's intended runtime tier (workflow declared as solo MAY NOT cite pro-only methodologies; a workflow without a declared tier defaults to the lowest tier of its consumers).
- Optional, not required — a workflow with zero methodology references is allowed if all knowledge belongs in surface-specific playbooks.
- Reason text is mandatory when present and must be specific (why **this** methodology for **this** workflow/phase).

### Boundary with playbooks

| Citation lives in | When |
|-------------------|------|
| Workflow (`AGENTS.md` or phase XML) | Methodology applies regardless of delivery surface (semantic-xml-content for prompts, sdd-conventions for lifecycle, code-review-principles for the review phase). |
| Playbook (`## Methodologies` table) | Methodology is surface-specific (gatsby-ssr-pitfalls only for FE; django-n-plus-1 only for BE). |

When in doubt, push the citation down to the playbook — surface-specific is cheaper to maintain than mis-scoped cross-cutting.

## 13. Decisions log (C12)

Every workflow ships `decisions.xml` listing non-obvious choices:

```xml
<decisions>
  <decision date="2026-04-15" topic="phase-count">
    <chose>12 phases including separate clarify and review</chose>
    <rejected>9-phase variant collapsing clarify into plan</rejected>
    <rationale>Clarify needs an `AskUserQuestion` boundary; folding it into plan blocks parallel waves.</rationale>
  </decision>
</decisions>
```

Required: at least one entry per non-obvious phase or per architectural choice that future-you would otherwise re-litigate.

Out of scope here: full failure-mode catalog (Symptom→Cause→Mitigation). Defer to v2.

## 14. Anti-patterns

Named, rejection-on-sight:

1. **Playbook redefines phase order** — playbooks adapt, never restructure.
2. **Top-level `<failure-routing>` table** — routing lives only inside `<phase>`.
3. **Phase missing `done=` or `verdict=` marker** — orchestrator cannot route.
4. **Tool allowlist deferred to playbook** — workflow owns the budget.
5. **Per-phase `idempotency` omitted** — re-run safety becomes a guess.
6. **Inline copy of `deploy-*.sh` in a playbook** — link to live source, never inline.
7. **AGENTS.md > 80 lines** — split to `.agents/` instead of bloating.
8. **Free-form prose tags inside `content/*.xml`** — closed glossary only.
9. **Time estimates anywhere** — use complexity levels and token estimates.
10. **`Co-Authored-By: Claude` trailer or emojis in commits** — repo-wide ban.
11. **`<methodology-ref>` with broken path or generic reason** — every citation must resolve and explain why this methodology applies here.
12. **Surface-specific methodology cited from a workflow** — push to the relevant playbook's `## Methodologies` table instead.

## 15. Minimal inline template

Drop the following into `skills/faion/workflows/<your-slug>/` and edit:

```
your-slug/
├── CLAUDE.md            # @AGENTS.md
├── AGENTS.md            # paste skeleton below, ≤80 lines
├── content/
│   ├── 01-overview.xml
│   └── 02-phases.xml    # phase quad-block per §6
└── decisions.xml
```

`AGENTS.md` skeleton:

```markdown
---
status: draft
audience: both
owner: ruslan
last_verified: 2026-05-02
version: 0.1.0
applies_to: any
---

# <Workflow Title>

## Summary
<one paragraph>

## Why
<one paragraph>

## When To Use
- <trigger 1>
- <trigger 2>

## When NOT To Use
- <anti-trigger 1>

## Content
| File | What's inside |
|------|---------------|
| `content/01-overview.xml` | Core principle, role split, language. |
| `content/02-phases.xml` | Phases + quad-blocks. |

## Related
- `.aidocs/conventions/workflows/workflow-spec.md` — this spec.
- `skills/faion/workflows/sdd-batch-orchestrator/` — reference impl.
```

`content/02-phases.xml` minimal:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<text id="02-phases" title="Phases">
  <phase id="study" version="0.1.0" idempotency="pure">
    <inputs>
      <var name="feature_id" type="string" required="true"/>
    </inputs>
    <pre-conditions>
      <assert>cwd is repo root</assert>
    </pre-conditions>
    <steps>
      <step>Read .aidocs/&lt;feature_id&gt;/spec.md.</step>
    </steps>
    <outputs>
      <done-marker regex="^done=study"/>
    </outputs>
    <post-conditions>
      <assert>study report saved</assert>
    </post-conditions>
    <constraints>
      <tool-allowlist>Read, Grep, Glob</tool-allowlist>
    </constraints>
    <failure-routing>
      <on condition="schema-violation" action="emit-verdict-fail" next="abort"/>
    </failure-routing>
    <done-condition>Study report exists and last line matches done=study.</done-condition>
  </phase>
</text>
```

## 16. Validation procedure + checklist

```bash
bash scripts/validate-workflow.sh <slug>
```

Pre-merge checklist (block PR if any unchecked):

- [ ] `AGENTS.md` ≤ 80 lines, all 7 required sections present.
- [ ] Front-matter has all 7 required keys.
- [ ] Every `content/*.xml` validates against tag glossary.
- [ ] Every `<phase>` has `id`, `version`, `idempotency`, all 8 quad-block slots.
- [ ] Every mutating phase declares re-entry guard in `<pre-conditions>`.
- [ ] Every `<phase>` has `<tool-allowlist>` and `<failure-routing>`.
- [ ] No top-level `<failure-routing>` element exists anywhere.
- [ ] `decisions.xml` has ≥1 entry.
- [ ] `last_verified` is current; CHANGELOG entry under `## [Unreleased]`.

## 17. Related

- `playbook-spec.md` — sibling spec for per-surface adaptations. Read §6/§7/§8/§10 when authoring a workflow that ships with playbooks.
- `skills/faion/workflows/sdd-batch-orchestrator/templates/prompt-skeleton.md` — live phase-prompt skeleton.
- `skills/faion/workflows/sdd-batch-orchestrator/templates/playbook-skeleton.md` — live playbook skeleton.
- `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml` — closed tag vocabulary.
- `docs/skill-authoring.md` — folder shape, token budgets across all skill kinds.
- `rules/skill-authoring.md` — mandatory pre-edit reading.
