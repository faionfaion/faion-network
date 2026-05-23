# AI-Generated Dockerfile Red-Flag List

## Summary

**One-sentence:** Red-flag checklist that scans AI-authored Dockerfiles for the 12 highest-blast-radius patterns (latest tag, root user, curl|sh, missing healthcheck, ARG secrets) and emits a JSON report.

**One-paragraph:** AI coding agents produce Dockerfiles that look plausible but reproduce well-known antipatterns: floating tags, root-as-default, curl|sh installers, ARG-leaked secrets, no healthcheck, no multi-stage build. This methodology codifies a 12-item red-flag list executed against every AI-authored Dockerfile before merge. Output is a JSON report listing matched red-flags with severity + remediation, suitable for CI gating.

**Ефективно для:**

- An AI coding agent (Claude Code, Cursor, Copilot) authored or edited a `Dockerfile` / `Containerfile`.
- The image is built and pushed automatically on merge — no human eyeballs guarantee a base review.
- The runtime is internet-exposed (web server, API, worker pulling from a queue) so blast radius matters.

## Applies If (ALL must hold)

- An AI coding agent (Claude Code, Cursor, Copilot) authored or edited a `Dockerfile` / `Containerfile`.
- The image is built and pushed automatically on merge — no human eyeballs guarantee a base review.
- The runtime is internet-exposed (web server, API, worker pulling from a queue) so blast radius matters.

## Skip If (ANY kills it)

- Dockerfile is hand-authored by a senior engineer with image-signing in place.
- The image is build-once-throwaway (single-CI-step scratch container, never pushed).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Dockerfile path | text | git diff / PR payload |
| Image base policy | yaml | team `security/base-images.yaml` |
| Allowed registry list | yaml | team `security/registries.yaml` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-dockerfile-redflag-list` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/redflag-report.json` | JSON skeleton for the validator output |
| `templates/Dockerfile.template` | Reference Dockerfile satisfying every red-flag rule |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-dockerfile-redflag-list.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
