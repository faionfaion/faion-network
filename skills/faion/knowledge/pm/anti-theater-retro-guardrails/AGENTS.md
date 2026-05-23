# Anti-Theatre Retro Guardrails

## Summary

**One-sentence:** Rubric for bi-weekly retros that blocks status-theatre patterns: forces one specific named-mistake-with-fix, enforces psychological-safety language rules, and emits a tracked decision the team checks at the next retro.

**One-paragraph:** Scrum-ceremonies covers the happy path; the failure mode (status-theatre retros) has no opinionated guardrail. This rubric forces every retro to surface exactly one named mistake with a concrete fix, applies a psychological-safety language rule (separate behaviour from identity), and emits a tracked decision the team must review at the next retro. Output: a retro record the team and sponsor can audit for theatre.

**Ефективно для:** scrum masters running bi-weekly retros; PMs salvaging political teams; engineering managers building mistake-memory.

## Applies If (ALL must hold)

- Team runs a regular retro cadence (bi-weekly or sprint-end)
- Past retros have produced action items that nobody owned or completed
- Team is willing to surface one specific mistake per session
- A facilitator role exists

## Skip If (ANY kills it)

- Brand-new team with no history yet — wait 2-3 sprints
- Hostile environment where surfacing mistakes is unsafe — fix psychological safety first
- Single-person team — there is no team retro
- Pure status meeting masquerading as retro — different methodology applies

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Last 3 retros' decisions / action items | Markdown / sheet | team wiki |
| Facilitator with authority to enforce rubric | Named person | team |
| Psychological-safety language guide | Markdown | team culture doc |
| Retro-decision tracker | Sheet / Linear list | PM tool |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager` | parent role skill |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `review_last_retro_decisions` | haiku | Mechanical lookup |
| `facilitate_retro` | sonnet | Bounded facilitation prompts |
| `synthesise_one_mistake` | opus | High-stakes synthesis of specific mistake |

## Templates

| File | Purpose |
|------|---------|
| `templates/anti-theater-retro-guardrails.json` | JSON schema for the retro record |
| `templates/anti-theater-retro-guardrails.md` | Markdown retro skeleton with required sections |
| `templates/_smoke-test.md` | Minimum-viable filled retro |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-anti-theater-retro-guardrails.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/`
- [[ai-status-digest-pipeline]]
- [[client-trust-rebuild-comms-templates]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether anti-theater-retro-guardrails applies: root question — "Does the team run a regular retro AND past retros have produced unowned action items?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-one-named-mistake, r2-concrete-fix, r3-language-rule, r4-prior-decision-review, r5-named-owner, r6-versioned-record.
