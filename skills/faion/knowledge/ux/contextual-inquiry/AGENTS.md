# Contextual Inquiry

## Summary

**One-sentence:** Produces a contextual-inquiry report from semi-structured interviews conducted in the user's environment while they perform actual work, with master-apprentice notes + interpretation session.

**One-paragraph:** Contextual inquiry observes users in their environment performing actual work, with the researcher adopting the master-apprentice stance: user is master, researcher is apprentice. Sessions are 1-3 hours; observations focus on artefacts, breakdowns, workarounds, and verbatim language. Output is a per-participant transcript + interpretation session results + affinity-diagram themes.

**Ефективно для:**

- Early-stage product discovery: розуміти actual workflow, не declared.
- B2B / regulated workflow де lab-tests втрачають context (e.g. healthcare).
- Surface workarounds + breakdowns що користувачі не згадають у survey.
- Validate / falsify персон проти польових даних.

## Applies If (ALL must hold)

- Researcher can co-locate with the user during their actual work.
- Work involves enough activity to observe (not pure desk thinking).
- Master-apprentice frame is acceptable to the participant.

## Skip If (ANY kills it)

- Remote-only workflows where observation requires screen-share — use diary studies.
- Sensitive contexts where observation would alter behaviour materially.
- Quantitative validation of known hypotheses — use surveys or analytics.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recruitment plan | criteria + count | research |
| Consent form | PDF | legal |
| Note template | structured | this methodology |
| Recording device | audio + photo (with consent) | research kit |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[personas]] | Outputs feed persona refinement |
| [[diary-studies]] | Alternative when on-site observation is infeasible |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure | 800 |
| `content/05-examples.xml` | essential | Worked example with note | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree routing to rules | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `primary-analysis` | sonnet | Domain-specific judgement. |
| `structured-output-assembly` | sonnet | Schema-conforming JSON build. |
| `validate` | haiku | Deterministic schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-guide.md` | Contextual inquiry interview guide with master-apprentice prompts |
| `templates/field-notes.md` | Per-session field note template with timestamped verbatim quotes + breakdown log |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-contextual-inquiry.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[personas]]
- [[focus-groups]]
- [[diary-studies]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
