# SEO Techniques

## Summary

**One-sentence:** Advanced SEO + AEO tactics: schema markup (JSON-LD), llms.txt, social meta (OG / Twitter), pillar-cluster internal linking, entity optimisation — produces a per-site techniques checklist.

**One-paragraph:** Advanced SEO + AEO tactics: schema markup (JSON-LD), llms.txt, social meta (OG / Twitter), pillar-cluster internal linking, entity optimisation — produces a per-site techniques checklist. The methodology pins a typed input → bounded transformation → contract-checked output for the recurring decision named in `Applies If`, and produces a versioned, owner-signed artefact downstream consumers can act on without re-deriving the reasoning. Hard rules block fabrication and silent template drift; the decision tree maps observable input signals to a conclusion that names which rule applies.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Technical SEO baseline (`seo-basics`) is already passing.
- Site has ≥1 content cluster ready to receive pillar-cluster internal-link wiring.
- A named owner will validate schema in Google Rich Results Test before deploying.
- Source-of-truth for brand / product / personnel naming is canonical (no divergent strings).

## Skip If (ANY kills it)

- Site has no indexed content — schema on empty pages is wasted.
- Client-side SPA without SSR — schema injected client-side is unreliable; requires SSR.
- Technical SEO baseline is broken — fix `seo-basics` first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the SEO Techniques task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `solo/sdd/sdd/AGENTS.md` | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema-validation-checklist.md` | Markdown checklist: schema JSON-LD types, llms.txt placement, OG meta, internal-link audit; all gated by Rich Results Test pass. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-seo-techniques.py` | Validate the artefact against the 02-output-contract schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[seo-manager/seo-basics]]
- [[seo-manager/topical-authority]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
