---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
applies_to: skills/faion/workflows/<workflow>/playbooks/<surface>.md
---

> **For:** playbook authors (LLM agent or human). **Prereqs:** read `workflow-spec.md` §1–3 and §6 first. **You will:** create or audit a `playbooks/<surface>.md` file that adapts an existing workflow to a concrete delivery surface.

**TL;DR**

- A playbook is a Markdown how-to that adapts a workflow to one delivery surface (e.g. `faion-net-fe`, `storybook`, `knowledge`).
- Lives at `skills/faion/workflows/<workflow>/playbooks/<surface>.md`. One file per surface, kebab-case.
- Every active playbook MUST cite ≥1 methodology from `skills/faion/knowledge/<tier>/<group>/<skill>/<methodology-slug>/` in a required `## Methodologies` table.
- Playbooks **may** override: verify command, test runner, deploy script, file-grouping heuristics, deploy gates, surface-specific pitfalls, methodology selection.
- Playbooks **may not** override: phase order, phase ids, output contract grammar, tool allowlist budget, idempotency class, failure-routing classes.

---

## 1. Definition + boundary

A **playbook** is a per-surface adaptation of a workflow. It records the concrete commands, paths, and choices a human or agent uses to run the workflow against one specific delivery target.

**Boundary statement (load-bearing):**

> Playbooks adapt surface choices, never redefine phase order.

A playbook fills surface-specific slots already declared by the workflow. If you find yourself adding new phase ids, reordering phases, or rewriting output contracts, stop — the work belongs in the workflow, not the playbook.

## 2. Diátaxis position: how-to

Playbooks are *how-tos* in the Diátaxis sense: goal-oriented, assume competence, deliver a recipe. Section titles use action-leading verbs (`## Verify the build`, not `## Verification`). Reference and explanation belong in the workflow, not here.

A playbook MUST NOT contain:
- philosophy, rationale, or "why this design";
- multi-paragraph narrative introductions;
- duplicated copies of workflow phase definitions.

## 3. Where playbooks live

```
skills/faion/workflows/<workflow>/playbooks/<surface>.md
```

### Naming

- Slug regex: `^[a-z][a-z0-9-]{2,40}$`. Kebab-case.
- One surface = one file. Do not group surfaces (e.g. `frontend-and-storybook.md` is wrong; create two files).
- Surface names match infrastructure reality: `faion-net-fe`, `faion-net-be`, `faion-network-knowledge`, `storybook`, `nero-prod`.

### When to add a new playbook vs. a note in an existing one

Add a new playbook when **all** apply:
- The surface has a distinct verify / deploy mechanism.
- The surface has a distinct repo or branch shape.
- The surface introduces ≥3 surface-specific pitfalls.

Otherwise, a one-paragraph note inside an existing playbook is enough.

## 4. Front-matter required keys

Every playbook starts with this YAML block. Pre-commit rejects missing keys.

```yaml
---
status: draft | active | deprecated
audience: both
owner: <handle>
last_verified: YYYY-MM-DD
version: <semver>                              # playbook.version, see workflow-spec §10
applies_to: <workflow-slug>                    # e.g. sdd-batch-orchestrator
verifies_against: <workflow-version-range>     # e.g. ^1.4
surface: <surface-slug>                        # matches filename
---
```

Mismatch between `surface` and the filename, or `verifies_against` not overlapping the parent workflow's current `version`, fails CI.

## 5. Required H2 sections (in order)

```
1.  ## Goal
2.  ## Surface choices
3.  ## Methodologies
4.  ## Repo and branch
5.  ## End-to-end binding
6.  ## Parallelism heuristics
7.  ## Pitfalls
8.  ## Verify
9.  ## Rollback
10. ## Worked example
11. ## Next
12. ## Related
```

A playbook with sections out of order or missing one fails the spec checklist.

### Section content rules

- `## Goal` — one sentence: "to ship X on surface Y, run workflow Z." No context, no theory.
- `## Surface choices` — the table from §6.
- `## Methodologies` — the table from §6.5. Required ≥1 row.
- `## Repo and branch` — bullet list: repo path, default branch (`main` or `master` — pin one), worktree root prefix, merge lock path.
- `## End-to-end binding` — for each workflow phase, one line: surface-specific note OR `inherits default`. Phase ids match the workflow exactly. MAY include per-phase methodology citation as a sub-bullet (`→ apply: <methodology-path>`) when a phase pulls a specific knowledge piece.
- `## Parallelism heuristics` — table mapping variant/area → typical files touched. Drives the wave planner.
- `## Pitfalls` — numbered list: each entry has Symptom → Cause → Mitigation. MAY cite a methodology as authority for the mitigation (`see: <methodology-path>`).
- `## Verify` — exact verify command(s) for this surface, runnable as-is.
- `## Rollback` — exact recovery commands per mutating phase. `inherits default` allowed only if workflow declares a default rollback.
- `## Worked example` — see §9.
- `## Next` — 1–3 verb-led bullets: what the reader does after this doc.
- `## Related` — three buckets: `Workflow:` (one link up), `Siblings:` (peer playbooks), `Used by:` (back-references).

## 6. Surface choices table

Required. Three columns, fixed rows:

| Choice | Value | Rationale |
|--------|-------|-----------|
| Verify command | `<exact command>` | <one line> |
| Test runner | `<exact command or "n/a">` | <one line> |
| Deploy mechanism | `<deploy-*.sh script or "n/a">` | <one line> |
| File-grouping heuristic | `<rule for wave planner>` | <one line> |
| Deploy gate | `confirm \| auto \| n/a` | <one line> |

A row may be `n/a` only if the workflow's phase set genuinely omits that capability. Adding new rows is allowed; removing or renaming required rows fails CI.

## 6.5. Methodologies table

Required. The playbook is not just a list of commands — it pulls in domain knowledge from `skills/faion/knowledge/<tier>/<group>/<skill>/<methodology-slug>/`. Every active playbook MUST cite at least one methodology that gives the agent (and the human reader) the substantive HOW behind the WHAT.

Schema:

| Phase | Methodology | Why for this surface |
|-------|-------------|----------------------|
| `<phase-id or "all">` | `<tier>/<group>/<skill>/<methodology-slug>` | <one line: what the methodology contributes to this phase on this surface> |

### Rules

- Path is relative to `skills/faion/knowledge/`. Validator resolves the methodology folder; broken paths fail CI.
- The `Phase` column matches a phase id from the parent workflow OR the literal `all` for cross-cutting methodologies (e.g. semantic-xml-content for prompt files).
- Required minimum: ≥1 methodology row for `status: active` playbooks. Surfaces with rich domain (frontend, backend, marketing) typically cite 3–8.
- Tier of the methodology must be ≤ the runtime tier of the surface (free playbook may not cite pro-only methodology). Validator checks against `skills/tier-manifest.json`.
- The `Why for this surface` rationale is mandatory and surface-specific. Generic descriptions ("explains REST design") fail review; the rationale must explain why **this** methodology applies to **this** playbook.
- A methodology may be cited from multiple playbooks; the rationale differs per surface.

### Where else methodologies appear

Beyond the required §6.5 table, methodologies MAY be cited inline:

- In `## End-to-end binding` per-phase notes as `→ apply: <methodology-path>` sub-bullets.
- In `## Pitfalls` mitigation lines as `see: <methodology-path>`.
- In the `## Worked example` when a step explicitly invokes a methodology checklist.

These inline citations do not replace the §6.5 table — the table is the canonical, machine-parseable index.

## 7. What playbooks MAY override

| Override | Where it goes |
|----------|---------------|
| Verify command | Surface choices row + `## Verify` section. |
| Test runner | Surface choices row. |
| Deploy script | Surface choices row + reference to live `deploy-*.sh`. |
| File-grouping heuristics for wave planner | `## Parallelism heuristics` table. |
| Deploy gate (confirm vs auto) | Surface choices row. |
| Surface-specific pitfalls | `## Pitfalls` numbered list. |
| Tighter tool allowlist | `## End-to-end binding` per-phase note (narrowing only). |
| Per-phase reference values (env vars, fixture paths) | `## End-to-end binding` per-phase note. |
| Methodology selection per surface | `## Methodologies` table + inline citations. |

## 8. What playbooks MAY NOT override (C10)

Hard list. Validator rejects on sight:

- **Phase order or phase ids** — phase set is workflow-owned.
- **Output contract grammar** — last-line marker regex is workflow-owned.
- **Tool allowlist budget** — playbooks may narrow, never expand.
- **Idempotency class** of any phase — class is a workflow contract.
- **Failure-routing classes** (`hook-fail`, `merge-conflict`, `quota`, `schema-violation`) — set is workflow-owned. Playbook MAY add surface-specific commentary, never new routing semantics.
- **Marker emission contract** — who emits, what regex.

If any of these need to change, open an issue against the workflow and bump its version.

## 9. Worked-example requirement

Every playbook closes with `## Worked example`: one real end-to-end run, real surface, real repo, real commands. Never `foo/bar`. Redact only secrets.

Required content of the worked example:

- The dispatch invocation (concrete `Agent` call shape with parameters).
- The phase-by-phase artifacts produced (file paths, commit shas as ellipses `abc1234...`).
- The verify command output (last 5 lines including the `verdict=` marker).
- The deliver step output (e.g. `tg-send` confirmation, screenshot path, PR URL).

Synthetic toy examples fail review.

## 10. Drift sentinels for playbooks

Mandatory checks (block commit if any fail):

- Every shell command in code fences resolves to an existing binary in `~/bin/`, repo root, or `node_modules/.bin/`.
- Every `<reference path="">` and Markdown link points to an existing file.
- `verifies_against` range contains the parent workflow's current `version`.
- `surface` front-matter matches the filename.
- Every required row in `## Surface choices` is present.
- `## Methodologies` table has ≥1 row for `status: active` playbooks.
- Every methodology path in `## Methodologies` resolves to an existing folder under `skills/faion/knowledge/`.
- Every methodology tier is ≤ the surface tier (no `pro/...` cited from a free-tier playbook).
- `last_verified` is within 90 days for `status: active`.

Run locally: `bash scripts/validate-playbook.sh <workflow-slug> <surface-slug>`.

## 11. Compat with workflow major bumps

When the parent workflow majors (e.g. `1.x` → `2.0`):

1. The workflow ships a `MIGRATION.md` listing breaking changes.
2. Every playbook re-evaluates against the migration:
   - If still applicable as-is → bump `verifies_against` to `^2.0`, update `last_verified`, commit.
   - If a surface choice changed → patch the affected section, bump `playbook.version` minor, update `verifies_against`, commit.
   - If the playbook's pattern no longer fits → mark `status: deprecated`, link the replacement.
3. CI rejects any active playbook whose `verifies_against` does not overlap the parent workflow's current `version`.

## 12. Minimal inline template

Drop into `skills/faion/workflows/<workflow>/playbooks/<surface>.md` and edit:

```markdown
---
status: draft
audience: both
owner: ruslan
last_verified: 2026-05-02
version: 0.1.0
applies_to: <workflow-slug>
verifies_against: ^1.0
surface: <surface-slug>
---

# Playbook: <Surface Title>

## Goal
To ship <feature kind> on <surface> via the <workflow-slug> workflow.

## Surface choices
| Choice | Value | Rationale |
|--------|-------|-----------|
| Verify command | `npm run typecheck && npm run lint && npm run build` | Gatsby build catches SSR issues. |
| Test runner | `n/a` | E2E lives in faion-net-e2e. |
| Deploy mechanism | `bash deploy-fe-dev.sh` | Push → SSH → rsync. |
| File-grouping heuristic | One feature per `src/pages/*` subtree. | Wave planner. |
| Deploy gate | confirm | Public surface. |

## Methodologies
| Phase | Methodology | Why for this surface |
|-------|-------------|----------------------|
| all | `solo/dev/frontend-developer/gatsby-ssr-pitfalls` | Gatsby SSR errors are the #1 build failure on this surface. |
| review | `pro/ux/accessibility-specialist/wcag-audit-checklist` | Public marketing pages must meet WCAG 2.1 AA. |
| verify | `solo/dev/code-quality/static-analysis` | Establishes the lint baseline for this repo. |
| deliver | `solo/marketing/seo-manager/topical-authority` | Marketing pages need topical-authority discipline before going live. |

## Repo and branch
- Repo path: `~/workspace/projects/faion-net/faion-net-fe/`
- Default branch: `main`
- Worktree root prefix: `/tmp/wt-<feature-id>-fe`
- Merge lock: `/tmp/faion-net-fe-merge.lock`

## End-to-end binding
- `study` — read `.aidocs/<project>/todo/<feature>/spec.md`.
- `clarify` — inherits default.
- `plan` — wave-group by `src/pages/*` subtree.
- `wave-execute` — inherits default.
- `verify` — `npm run typecheck && npm run lint && npm run build`.
  - → apply: `solo/dev/code-quality/static-analysis`
- `review` — focus on Gatsby SSR pitfalls and a11y.
  - → apply: `solo/dev/frontend-developer/gatsby-ssr-pitfalls`
  - → apply: `pro/ux/accessibility-specialist/wcag-audit-checklist`
- `fix` — inherits default.
- `deliver` — focused screenshot of changed page; `tg-send` to <chat>.
  - → apply: `solo/marketing/seo-manager/topical-authority`
- `close` — `bash deploy-fe-dev.sh` only after `AskUserQuestion` confirm.

## Parallelism heuristics
| Variant / area | Files typically touched |
|----------------|-------------------------|
| Marketing pages | `src/pages/marketing/**` |
| Docs pages | `src/pages/docs/**` |

## Pitfalls
1. **Symptom:** SSR build fails on hooks at module top level.
   **Cause:** `useEffect` outside a component during SSR.
   **Mitigation:** Move into component body or guard with `typeof window !== 'undefined'`.

## Verify
```bash
cd ~/workspace/projects/faion-net/faion-net-fe
npm run typecheck && npm run lint && npm run build
```
Expect: exit 0, no warnings, `verdict=PASS` from review subagent.

## Rollback
- `wave-execute`: `git -C <worktree> reset --hard origin/main`.
- `deliver`: `bash deploy-fe-dev.sh` with previous SHA.

## Worked example
<one real run, redacted only for secrets>

## Next
- Run `bash scripts/validate-playbook.sh <workflow-slug> <surface-slug>` before commit.
- Bump `last_verified` after a successful end-to-end run.

## Related
- Workflow: `../AGENTS.md`
- Siblings: `faion-net-be.md`, `storybook.md`
- Used by: `.aidocs/<project>/todo/<feature>/`
```

## 13. Anti-patterns

Named, rejection-on-sight:

1. **Playbook reorders phases or invents new phase ids** — fork-by-copy disguised as adaptation.
2. **Worked example uses `foo/bar`** — synthetic placeholders fail review.
3. **Verify command in fence not present in repo** — drift sentinel #1 catches this.
4. **Inlined copy of `deploy-*.sh`** — link to live source, never inline.
5. **Theory or rationale paragraphs** — wrong Diátaxis quadrant; move to workflow.
6. **Free-form `Surface choices` columns** — schema is fixed.
7. **`verifies_against: "*"`** — wildcards mask incompatibility; declare a real range.
8. **Renaming a required H2 section** — section names are mechanical anchors.
9. **Multiple surfaces in one file** — split into one file per surface.
10. **Time estimates** — repo-wide ban.
11. **`## Methodologies` table empty or missing** — playbook becomes a command list without domain knowledge.
12. **Generic methodology rationale** ("explains testing") — must be surface-specific (why **this** methodology for **this** playbook).
13. **Methodology tier exceeds surface tier** — pro-only methodology cited from a free-tier playbook.

## 14. Related

- `workflow-spec.md` — parent spec. Read §6 (phase quad-block), §7 (tool allowlist), §8 (idempotency), §10 (versioning) before authoring.
- `skills/faion/workflows/sdd-batch-orchestrator/templates/playbook-skeleton.md` — live skeleton kept in sync with this spec.
- `skills/faion/workflows/sdd-batch-orchestrator/playbooks/` — concrete playbooks per surface (when populated).
- `rules/skill-authoring.md` — mandatory pre-edit reading.
