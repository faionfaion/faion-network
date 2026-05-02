# Feature 048: Tier Playbooks — Implementation Plan

## Phase overview

7 phases. Phases 1-3 set up convention + scaffold + tooling. Phases 4-7 author playbooks, one tier per phase.

| Phase | Subject | Deliverable | Est. tokens |
|-------|---------|-------------|-------------|
| 1 | Convention spec | `.aidocs/conventions/playbooks/playbook-spec.md` + `AGENTS.md` + `CLAUDE.md`; cross-link from `conventions/workflows/AGENTS.md` | ~15k |
| 2 | Skill amendments | `faion/SKILL.md` body update + `faion/CLAUDE.md` tree update + `skills/CLAUDE.md` row + `tier-manifest.json` extension | ~8k |
| 3 | Validator + scaffold + prompt | `scripts/validate-tier-playbook.py`; `skills/faion/playbooks/{free,solo,pro,geek}/AGENTS.md` stubs; `prompts/playbook-author-prompt.md` template | ~25k |
| 4 | Wave 1 — Free | 30 playbooks under `playbooks/free/` | ~150k |
| 5 | Wave 2 — Solo | 30 playbooks under `playbooks/solo/` | ~150k |
| 6 | Wave 3 — Pro | 30 playbooks under `playbooks/pro/` | ~150k |
| 7 | Wave 4 — Geek | 30 playbooks under `playbooks/geek/` | ~150k |

**Total estimate:** ~648k tokens (orchestrator + 4 authoring waves combined).

## Phase 1 — Convention spec

Tasks:
1. Create `.aidocs/conventions/playbooks/CLAUDE.md` (`@AGENTS.md`)
2. Create `.aidocs/conventions/playbooks/AGENTS.md` (≤80 lines: definition, boundary, when to author, validation, related)
3. Create `.aidocs/conventions/playbooks/playbook-spec.md` (full spec per design.md § "Convention spec creation")
4. Update `.aidocs/conventions/workflows/AGENTS.md` § "Boundary" — add row pointing at new spec

Gate: spec passes 8-item self-checklist; cross-link reciprocal between workflow and tier playbook specs.

## Phase 2 — Skill amendments

Tasks:
1. Append "Playbooks" body section to `skills/faion/SKILL.md`
2. Update `skills/faion/CLAUDE.md` with playbooks tree parallel to knowledge
3. Add row to `skills/CLAUDE.md` skills index for `faion/playbooks/`
4. Extend `skills/tier-manifest.json` per tier (placeholder `playbook_paths` populated in phase 3)

Gate: `jq '.tiers.free.playbook_root' skills/tier-manifest.json` returns valid string for all 4 tiers.

## Phase 3 — Validator + scaffold + author prompt

Tasks:
1. `scripts/validate-tier-playbook.py` (Python; specced in design.md)
2. `scripts/validate-tier-playbook.sh` thin wrapper
3. `skills/faion/playbooks/CLAUDE.md` (`@AGENTS.md`) + `AGENTS.md` (orientation, ≤80 lines)
4. `skills/faion/playbooks/<tier>/CLAUDE.md` + `AGENTS.md` per tier
5. `skills/faion/playbooks/<tier>/<group>/AGENTS.md` per group with TIER-1 selections
6. Populate `playbook_paths` in `tier-manifest.json` once group folders exist
7. `prompts/playbook-author-prompt.md` (template under `skills/faion/workflows/` if reusing workflow prompt convention, or under `prompts/` at repo root)

Gate: `python3 scripts/validate-tier-playbook.py --self-test` passes (synthetic minimal playbook validates clean); empty playbook fails with specific error.

## Phases 4-7 — Authoring waves

Each wave is a pool-based dispatch.

### Pool config

- Pool size: 5-8 parallel subagents
- Batch size: 1-2 playbooks per dispatch
- Subagent model: sonnet (haiku for revision passes only)
- Subagent type: `faion-sdd-executor-agent` (in worktree isolation)
- Lock: `flock /tmp/faion-network-merge.lock` for commit serialization

### Subagent contract

Each subagent receives (variables interpolated into `prompts/playbook-author-prompt.md`):

| Variable | Source |
|----------|--------|
| `tier`, `group`, `slug` | `catalog/priority-120.md` row |
| `title`, `problem`, `solution_outline`, `persona`, `impact`, `effort` | catalog row |
| `allowed_methodology_paths` | derived from tier-manifest.json (paths from playbook tier and below) |
| `repo_branch`, `repo_path` | orchestrator |

Subagent produces:
- `skills/faion/playbooks/<tier>/<group>/<slug>/playbook.md` (+ optional companion files)
- Self-validates with `python3 scripts/validate-tier-playbook.py`
- Updates relevant `AGENTS.md` indexes (group + tier)
- Single granular commit per playbook (commit message: `feat: add tier-playbook <tier>/<group>/<slug>`)
- CHANGELOG.md entry under `## [Unreleased]`
- Reports last-line marker: `done=<slug> commit=<sha>`

### Dispatch sequence per wave

```
1. Read catalog/priority-120.md, filter to current tier
2. For each playbook (30):
   a. Reserve slug (write marker to .runs/feature-048/<wave>/<slug>.reserved)
   b. Dispatch subagent with rendered prompt
   c. Wait for marker; on fail → re-dispatch with sonnet+revision prompt
3. After all 30 complete:
   - Update tier AGENTS.md index
   - Update tier-manifest.json playbook_paths
   - Run full-tier validator: `validate-tier-playbook.py skills/faion/playbooks/<tier>/**/playbook.md`
4. Wave-level CHANGELOG.md summary entry
5. Move catalog rows from priority-120.md to (delivered.md or strikethrough)
```

### Wave order

Sequential, not parallel: Free → Solo → Pro → Geek. Reasons:
- Catalog learnings carry forward (style, validator misses, prompt tweaks)
- AGENTS.md indexes built incrementally
- Validator behavior validated on simplest tier first

### Quality gates per wave

1. 100% playbooks pass validator (path resolution, tier ≤, structure, slug)
2. Random spot-check: 3 playbooks per wave reviewed by `faion-sdd-execution`-style reviewer subagent
3. AGENTS.md per group/tier ≤80 lines
4. No duplicate slugs across all waves to date (cumulative check)

## Lifecycle markers (in feature folder)

```
.aidocs/in-progress/feature-048-tier-playbooks/
├── todo/<wave>/<slug>.md       reserved but not started
├── in-progress/<wave>/<slug>.md  subagent dispatched
└── done/<wave>/<slug>.md       completed (one-line: commit sha + path)
```

These are *thin* lifecycle trackers — the real artifact is in `skills/faion/playbooks/`.

## Dispatch prompt skeleton (rendered to subagent)

```
You are authoring tier-playbook <slug> for tier=<tier>, group=<group>.

Catalog brief: <problem> → <solution_outline>. Persona=<persona>, impact=<impact>, effort=<effort>.

Spec: read .aidocs/conventions/playbooks/playbook-spec.md before authoring.
Allowed methodology citations (tier ≤): <allowed_methodology_paths>

Deliverable: skills/faion/playbooks/<tier>/<group>/<slug>/playbook.md with the 8 fixed sections + frontmatter.

Validator: python3 scripts/validate-tier-playbook.py <path>. Must exit 0.

After writing:
1. Update group AGENTS.md index (one-line description)
2. Add CHANGELOG.md entry under [Unreleased]
3. Single commit: `feat: add tier-playbook <tier>/<group>/<slug>`
4. Push via flock /tmp/faion-network-merge.lock
5. Emit last-line marker: done=<slug> commit=<sha>

Constraints: real commands only (no foo/bar), ≤5k tokens body, citation rationale playbook-specific.
```

## Rollback plan per wave

If a wave has >10% validator failures:
1. Pause dispatch
2. Triage: spec ambiguity → fix spec; subagent prompt issue → fix prompt; content issue → manual revision
3. Re-dispatch only failing slugs
4. If failures >25% on retry: escalate to user (paused-loop pattern)

## Out of scope (this feature)

- Authoring TIER-2 catalog (remaining 280 playbooks)
- Public site rendering (separate FE feature)
- Translations to UK/PL/DE
- `/faion` retrieval extension to index playbooks
