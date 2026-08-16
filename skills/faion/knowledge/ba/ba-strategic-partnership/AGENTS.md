# BA Strategic Partnership

## Summary

**One-sentence:** Evolution checklist that lifts a BA from documentation-only execution to strategic-partner stance — quarterly OKR co-ownership, business-case authorship, named sponsor mapping.

**One-paragraph:** Evolution checklist that lifts a BA from documentation-only execution to strategic-partner stance — quarterly OKR co-ownership, business-case authorship, named sponsor mapping. Captured as a versioned artefact downstream agents and reviewers consume without re-deriving rationale. Mechanism: typed input → bounded transformation → contract-checked output.

**Ефективно для:**

- Senior BA / lead BA repositioning to strategic partner role.
- Quarterly OKR alignment sessions з sponsor + delivery.
- Career-growth artefact для performance review.
- Outsource P4 engagement positioning против commodity BA work.

## Applies If (ALL must hold)

- BA has ≥6 months tenure with current sponsor.
- Sponsor named and reachable for quarterly sync.
- Existing BA work consistent (no firefighting baseline).
- Org has OKR / strategic-plan structure to align against.

## Skip If (ANY kills it)

- First-month BA on new engagement — execute basics first.
- Sponsor not engaged or transition imminent.
- Tactical engagement (≤8 weeks) where strategic stance is overreach.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent task context (30 days) | Markdown / tracker | BA |
| Write access to artefact store | repo / wiki | engagement manager |
| Named downstream owner | stakeholder list | BA |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[ba-planning]] | Companion / upstream methodology |
| [[decision-analysis]] | Sibling artefact in the same lifecycle |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + examples | 800 |
| `content/03-failure-modes.xml` | essential | Antipatterns | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Mechanical template fill. |
| `synthesize_decision` | sonnet | Per-instance bounded judgment. |
| `review_for_compliance` | opus | Cross-input synthesis on high-stakes outputs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ba-strategic-partnership.json` | Skeleton artefact with required fields |
| `templates/_smoke-test.json` | Minimum viable filled artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ba-strategic-partnership.py` | Validate artefact against output-contract | After subagent returns; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ba-planning]]
- [[decision-analysis]]
- [[benefit-sustainment-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on artefact-state signal to the active rule.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ba-strategic-partnership.json`

```json
{
  "ba_name": "REPLACE",
  "period": "REPLACE",
  "sponsor_name": "REPLACE",
  "version_tag": "REPLACE",
  "okrs_coowned": [],
  "business_cases_authored": [],
  "sponsor_syncs": []
}
```

### `templates/_smoke-test.json`

```json
{
  "ba_name": "Maria Lopes",
  "period": "2026Q2",
  "sponsor_name": "Pedro Silva",
  "version_tag": "v1.0.0",
  "okrs_coowned": [
    {
      "id": "okr-rev-1",
      "objective": "Reduce AP cycle time 40%",
      "ba_role": "co-owner: process redesign + AC"
    }
  ],
  "business_cases_authored": [
    {
      "id": "bc-01",
      "title": "Invoice automation",
      "primary_author": "Maria Lopes"
    }
  ],
  "sponsor_syncs": [
    {
      "date": "2026-04-15",
      "minutes_path": "syncs/2026-04-15.md"
    }
  ]
}
```
