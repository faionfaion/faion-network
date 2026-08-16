# SonarQube AI-Code Gate

## Summary

**One-sentence:** SonarQube quality-gate config that holds AI-generated code to a higher bar than human-authored: coverage, duplication, security hotspots, AI-author tag, gated merge.

**One-paragraph:** AI-generated code is statistically more likely to contain duplication, security hotspots, and untested branches. This methodology defines a SonarQube quality-gate profile with stricter thresholds for AI-authored changes (coverage ≥85% on new code, duplication ≤2%, zero security hotspots, zero major code smells) and a per-PR `ai-author` tag that routes the gate. Output is the SonarQube `quality-gate.json` + `sonar-project.properties` + CI wiring.

**Ефективно для:**

- Team uses SonarQube (Community 10+, Enterprise, or Sonar Cloud) and runs scans per PR.
- AI agents author or modify code in the repo, identifiable via commit author / co-author / branch naming.
- There is leadership support for a higher quality bar on AI-authored code.

## Applies If (ALL must hold)

- Team uses SonarQube (Community 10+, Enterprise, or Sonar Cloud) and runs scans per PR.
- AI agents author or modify code in the repo, identifiable via commit author / co-author / branch naming.
- There is leadership support for a higher quality bar on AI-authored code.

## Skip If (ANY kills it)

- Team uses no static analysis platform that supports per-PR quality gates.
- AI-author identification is impossible (no commit metadata convention; mixed author commits).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| SonarQube server URL | url | Team infra catalog |
| Authentication token | string | Vault / GitHub secret |
| AI-author convention | yaml | Repo at `governance/ai-authoring.yaml` |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-gov-sonarqube-ai-code-gate` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-quality-gate.json` | SonarQube quality gate JSON spec |
| `templates/sonar-project.properties` | sonar-project.properties wiring |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gov-sonarqube-ai-code-gate.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ai-quality-gate.json`

```json
{
  "name": "ai-strict-v1",
  "conditions": [
    {
      "metric": "new_coverage",
      "op": "LT",
      "error": "85"
    },
    {
      "metric": "new_duplicated_lines_density",
      "op": "GT",
      "error": "2"
    },
    {
      "metric": "new_security_hotspots",
      "op": "GT",
      "error": "0"
    },
    {
      "metric": "new_code_smells",
      "op": "GT",
      "error": "0",
      "scope": "MAJOR+"
    },
    {
      "metric": "new_blocker_violations",
      "op": "GT",
      "error": "0"
    }
  ]
}
```

### `templates/sonar-project.properties`

```ini
sonar.projectKey=payments-service
sonar.host.url=https://sonar.faion.net
sonar.newCode.referenceBranch=main
sonar.qualitygate.wait=true
# CI sets sonar.qualitygate.name=ai-strict-v1 when AI author detected
```
