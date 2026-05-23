# Focus Groups

## Summary

**One-sentence:** Produces a focus-group findings report from >=3 groups of 6-10 participants × 60-90 minutes per segment, with written-first exercises + late concept reveal + theme stability check.

**One-paragraph:** Moderated qualitative method: 6-10 participants per group, 60-90 min, minimum 3 groups per segment before themes are treated as stable. Structure: warm-up (10 min), three core topics with probe ladders (40-60 min), late concept reveal (last 25%), wrap-up. Written-first exercises before open discussion capture unanchored individual opinions. Recruit one extra participant per group to absorb ~20% no-show rate.

**Ефективно для:**

- Early-stage concept exploration перед quantitative дослідженням.
- Reaction data на copy / naming / value propositions / visual concepts.
- Map user vocabulary — як customers describe проблему власними словами.
- Stakeholder buy-in: PM спостерігає live discussion.

## Applies If (ALL must hold)

- Early-stage concept exploration or vocabulary mapping.
- >=3 groups per segment can be recruited.
- Topic is not sensitive (health, finance, harassment).

## Skip If (ANY kills it)

- Usability testing — group dynamics drown individual task behaviour.
- Sensitive or personal topics — social pressure distorts answers.
- Final decision-making — small N + groupthink ≠ representative data.
- Anything shipped without 1:1 follow-up — group consensus alone is unreliable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recruitment criteria | segment definition | research |
| Discussion guide | warm-up + probe ladders + reveal | this methodology template |
| Moderator | trained | research vendor or in-house |
| Recording + consent | PDF + audio | legal |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[personas]] | Segments map to personas |
| [[contextual-inquiry]] | Complement: contextual inquiry surfaces individual workflow |

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
| `templates/discussion-guide.md` | Focus group discussion guide skeleton with probe ladders + reveal timing |
| `templates/note-taking.md` | Per-group note-taking template with quote capture + dominance tracking |
| `templates/transcript-themer.py` | Python clustering helper grouping verbatim quotes into candidate themes across groups |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-focus-groups.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[personas]]
- [[contextual-inquiry]]
- [[diary-studies]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
