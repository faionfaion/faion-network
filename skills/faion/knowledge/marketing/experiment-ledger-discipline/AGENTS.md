# Experiment Ledger Discipline

## Summary

**One-sentence:** Append-only experiment ledger — every hypothesis, variant, result, learning recorded with producer + consumer + decision-fed; immutable rows + versioned deltas; queryable by future-self.

**One-paragraph:** Most CRO programs forget their own history in 6 months and re-run lost experiments. This methodology pins the ledger as an append-only, immutable knowledge layer with explicit consumer + decision-fed per entry. Core rules: append-only (edits create new versioned rows with delta_reason); every entry has producer + consumer + decision-fed; query latency bounded (≤ 5s for the canonical search); learning_summary required at close; superseded-by chain when prior results are invalidated. Output: a versioned ledger config + entry shape that an LLM agent can query and a human can audit.

**Ефективно для:**

- CRO program lasting &gt;6 months — institutional memory at risk.
- Multi-rater scoring team — same hypothesis tested differently across cycles.
- Agency / freelance handoff — incoming consultant queries past learnings.
- Quarterly retro — pull every shipped + killed test from the ledger by tag.

## Applies If (ALL must hold)

- ≥1 experiment shipped per month for ≥3 months (history worth preserving).
- A storage layer that supports append + version (git, Notion, dedicated DB).
- ≥1 named consumer who actually queries the ledger.
- Authority to enforce that no test ships without a ledger entry.

## Skip If (ANY kills it)

- Cadence too low (&lt;1 test/quarter) — overhead exceeds value.
- No queryable storage (only PDFs / Slack history) — fix storage first.
- No named consumer — ledger becomes orphaned write-only log.
- Single-person solo work for &lt;3 months — memory still fresh.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Ledger storage | git repo / Notion DB / SQL table | growth team |
| Shipped experiment list (≥1 month) | report / CSV | ledger or prior tool |
| Verdict template integration | spec | experiment-verdict-template |
| Tag taxonomy | list | growth lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[experiment-hypothesis-scoring]] | Upstream producer of queued hypotheses. |
| [[experiment-verdict-template]] | Downstream producer of verdicts that close ledger entries. |
| [[ab-testing-basics]] | Background on the entries the ledger holds. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: append-only, producer-consumer-decision, query-latency-bound, learning-summary-required, superseded-by-chain | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for one ledger entry + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: open entry → ship test → record result → close with learning → archive | 600 |
| `content/06-decision-tree.xml` | essential | Tree: entry state → next action | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `write-entry` | haiku | Template fill. |
| `close-with-learning` | sonnet | Synthesis of result + cohort context. |
| `audit-ledger-health` | sonnet | Cross-entry diff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ledger-entry.json` | JSON example of one ledger entry |
| `templates/ledger-config.yaml` | Storage + tag taxonomy + retention config |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-experiment-ledger-discipline.py` | Validate one ledger entry JSON against the schema | On entry create + close |

## Related

- [[experiment-hypothesis-scoring]]
- [[experiment-verdict-template]]
- [[ab-testing-basics]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes on entry state (proposed / shipped / closed / superseded) to the next action and pins the rule from `01-core-rules.xml`. Use it before mutating an entry — direct edits violate append-only.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ledger-entry.json`

```json
{
  "entry_id": "ent-2026q2-pricing-social-proof",
  "status": "closed",
  "producer": "@alex",
  "consumer": "@beth",
  "decision_fed": "Reposition pricing social proof for Q3 cycle",
  "hypothesis": "Moving social proof above the fold on /pricing increases pricing-to-signup conversion.",
  "variants": [
    "control",
    "above-fold"
  ],
  "result": "+5.2% conversion lift, p=0.03, n=12400 sessions",
  "learning_summary": "Above-fold social proof lifts /pricing conversion 5.2% (n=12.4k, p=0.03). Effect concentrated in returning visitors (+8.1%); new visitors flat. Ship to all; revisit new-visitor variant in Q3.",
  "tags": [
    "pricing",
    "social-proof",
    "above-fold"
  ],
  "cycle_id": "2026-Q2",
  "created_at": "2026-04-15T09:00:00Z",
  "closed_at": "2026-05-20T17:00:00Z",
  "prev_entry_id": null,
  "superseded_by": null
}
```

### `templates/ledger-config.yaml`

```yaml
version: "1.0.0"
storage:
  layer: "notion-db"        # one of: notion-db | git-yaml | sqlite | postgres
  url_or_path: "https://notion.so/<workspace>/<db>"
  index_fields: ["tags", "status", "cycle_id"]
query_latency_budget_seconds: 5
tag_taxonomy:
  surface: [landing, pricing, signup, onboarding, in-product, billing, lifecycle-email]
  lever: [copy, layout, social-proof, ctas, pricing, feature-gate, onboarding-flow]
  result: [winner, loser, inconclusive, killed-early]
retention:
  closed_entries: forever
  proposed_entries_max_age_days: 90       # auto-archive proposed entries that don't ship
  superseded_chain_kept: forever
```
