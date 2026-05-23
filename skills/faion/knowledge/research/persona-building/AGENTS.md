# Persona Building

## Summary

**One-sentence:** Produces 3 personas (primary + secondary + negative), each backed by >=5 interview citations, JTBD statements, top-3 pains, and a kill-criteria block; refuses single-source personas.

**One-paragraph:** Persona authoring methodology that ships exactly 3 personas (primary, secondary, negative) per product, each grounded in >=5 cited interview quotes, with explicit Jobs-to-Be-Done statements, top-3 pains, and a 'kill criteria' block naming the trait that disqualifies a user from this persona. Refuses single-source / single-interview personas.

**Ефективно для:**

- Pre-MVP: треба зафіксувати ICP перед feature greenlight.
- GTM сегментація для emails / ads / landing pages.
- Onboarding flow design - persona визначає first-run experience.
- Founder говорить про 'наших users' без конкретики - треба primary + secondary.
- Negative persona: окреслити, кого ми НЕ обслуговуємо (зменшує churn).

## Applies If (ALL must hold)

- Pre-MVP ICP lock before feature greenlight.
- GTM segmentation for emails, ads, landing pages.
- Onboarding flow design (persona drives first-run experience).
- Founder talks about 'our users' generically; needs primary + secondary.
- Negative persona work to reduce churn by naming the customer we do NOT serve.

## Skip If (ANY kills it)

- Pre-PMF zero users; do customer-development first, not personas.
- Internal tool with one user type (employees).
- Hardware / regulated medical (use clinical-trial cohorts, not personas).
- B2B enterprise with one buyer per account (build a buying committee map instead).
- Stable mature product where personas have not changed in 24 months.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Interview transcripts | markdown / Otter / Looppanel | user research ops |
| Quantitative segment data | PostHog / Amplitude cohorts | analytics |
| Tag library | JTBD + pain + segment | Dovetail / manual |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[user-research-at-scale]] | supplies the transcript volume and tagging that personas summarise |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cluster-segments` | sonnet | Cluster transcripts into 2-4 candidate segments. |
| `write-persona-cards` | sonnet | Compose persona-lean and persona-full per segment. |
| `negative-persona` | sonnet | Identify the user type the product must reject. |
| `citation-check` | haiku | Mechanical check that every persona has >=5 cited quotes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/persona-lean.md` | Lean persona card (1-page) for ad/landing copy |
| `templates/persona-full.md` | Full persona doc with JTBD + pains + day-in-the-life + kill criteria |
| `templates/persona-negative.md` | Negative persona template (who we do not serve) |
| `templates/cluster-personas.py` | Cluster transcripts by JTBD tags; print top-K segments |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-persona-building.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[user-research-at-scale]]
- [[continuous-discovery]]
- [[market-research-tam-sam-som]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
