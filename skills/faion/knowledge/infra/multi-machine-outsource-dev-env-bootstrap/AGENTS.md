# Multi-Machine Outsource Dev Env Bootstrap

## Summary

**One-sentence:** Spec for bootstrapping a senior outsource specialist's multi-machine dev env (laptop + desktop + VDI) per engagement, with isolation per client.

**One-paragraph:** Spec for bootstrapping a senior outsource specialist's multi-machine dev env (laptop + desktop + VDI) per engagement, with isolation per client. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Senior бере 2+ engagements паралельно — без ізоляції credentials легко зливаються.
- Новий desktop або client laptop треба підняти до working state менш ніж за 2 години.
- Dotfiles живуть single-machine — на другій машині все треба робити з нуля.
- VDI-сесії додають третю площину, де треба ті ж самі tools, але без особистих secrets.

## Applies If (ALL must hold)

- Engineer takes on a new client engagement
- Engineer uses >=2 personal machines (laptop + desktop) + occasionally a VDI
- Engagements must remain isolated (no leakage of client A creds onto client B host)
- Dotfiles + tool versions + secrets must be reproducible on a fresh machine in <2 hours

## Skip If (ANY kills it)

- Single-machine engineer with one client — overkill
- Engagement allows shared global config (rare) — no isolation needed
- All work happens in client-issued VDI only — different bootstrap model

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trigger context | Markdown / ticket / transcript | upstream task |
| Named owner | string (handle, email, role) | team roster |
| Storage location | URL / repo path | artefact store |
| Prior cycle artefact (if any) | this methodology's output | last run |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/AGENTS.md` | parent group context (vocabulary, neighbouring methodologies) |
| `solo/sdd/sdd` | SDD discipline for artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + run-the-checklist + skip-this-methodology conclusions | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid + invalid + forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom / root-cause / fix | ~700 |
| `content/04-procedure.xml` | essential | step-by-step procedure (input/action/output/decision-gate) | ~700 |
| `content/05-examples.xml` | essential | one worked end-to-end example with inputs and final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | root-question + branches + conclusion refs to 01-core-rules | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment over bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high or evidence chain is required |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | working skeleton matching the `produces=spec` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-machine-outsource-dev-env-bootstrap.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Does the engineer use >=2 machines + needs per-client isolation + <2h bootstrap?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
