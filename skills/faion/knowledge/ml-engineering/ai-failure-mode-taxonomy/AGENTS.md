# AI Failure Mode Taxonomy

## Summary

**One-sentence:** Produces a closed taxonomy of 12 LLM failure modes (hallucination, IPI, refusal-bypass, schema-drop, latency-spike, cost-blowup, etc.) with detector + severity + linked methodology, anchoring every eval, alert, and incident.

**One-paragraph:** Different teams in the same company name the same failure differently — "hallucination" / "fabrication" / "drift" — making evals incomparable, alerts inconsistent, and postmortems irreproducible. A closed taxonomy enumerates exactly 12 named failure modes (with id + definition + detector + severity + linked-methodology) and forbids ad-hoc additions. Every eval case, alert rule, and incident ticket references one mode id; reports across teams become commensurable.

**Ефективно для:** multi-team AI orgs, postmortem libraries, eval-set design, alert routing, on-call runbooks, vendor-cross-comparison.

## Applies If (ALL must hold)

- ≥2 teams build / operate LLM-backed features and share a postmortem / alert channel.
- A central owner can publish + version the taxonomy.
- Existing eval cases / incidents can be re-tagged to the new ids.
- Tooling (dashboards, alerts) can read the mode id as a column / label.

## Skip If (ANY kills it)

- Single team, single feature — overhead exceeds the benefit.
- No central owner — taxonomy will fork within months.
- Tooling cannot consume the ids — output is documentation rot.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Recent incidents | tickets / JSONL | incident log |
| Existing eval categories | strings | eval harness |
| Alert rule names | strings | observability config |
| Owner & cadence | doc | team charter |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[llm-drift-daily-triage]]` | Daily report references taxonomy ids. |
| `[[indirect-prompt-injection-defense]]` | IPI mode is part of the taxonomy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: closed 12-mode set, every mode has detector+severity, version + change log, no ad-hoc ids, eval+alert+ticket link mandatory, quarterly review | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for taxonomy.json: array of {id, name, detector, severity, linked_methodology} | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns of taxonomies themselves: open list, no detectors, severity-uniform, no link to mitigations, retire-and-forget | ~600 |
| `content/04-procedure.xml` | medium | 6-step: pull existing → cluster to 12 → write detectors → assign severity → link methodology → publish | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "≥2 teams + central owner present?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Cluster existing categories | opus | Semantic reasoning. |
| Author detectors | sonnet | Concrete signal definitions. |
| Assign severities | opus | Cross-business reasoning. |
| Wire ids into dashboards | haiku | Mechanical config edit. |

## Templates

| File | Purpose |
|---|---|
| `templates/taxonomy.schema.json` | JSON Schema for taxonomy.json. |
| `templates/taxonomy-skeleton.json` | 12-mode skeleton with placeholder detectors. |
| `templates/incident-template.md` | Postmortem template that references a mode id. |
| `templates/_smoke-test.json` | Minimum valid 12-mode taxonomy. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-failure-mode-taxonomy.py` | Validates taxonomy.json: exactly 12 modes, no duplicate ids, every mode has detector+severity+linked_methodology. | Pre-commit on taxonomy.json; CI before publishing. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[llm-drift-daily-triage]]`
- `[[indirect-prompt-injection-defense]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` decides whether to formalise: single team or no owner → skip; multi-team + central owner → run procedure; mid-state (multi-team no owner) → escalate to leadership before adopting.
