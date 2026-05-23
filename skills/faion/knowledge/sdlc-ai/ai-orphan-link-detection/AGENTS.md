# AI Orphan-Link Detection

## Summary

**One-sentence:** Detector that finds broken / orphaned markdown links in AI-generated documentation (relative paths, anchor refs, methodology cross-links) and emits a per-file remediation report.

**One-paragraph:** AI agents write docs that look polished but link to files that don't exist (`see docs/setup.md`), anchors that drifted (`#configuration` after the section was renamed), or methodology slugs that the agent imagined. This methodology runs a deterministic crawler over `*.md` files, resolves every link, classifies orphans by category (missing-file, missing-anchor, external-404, methodology-slug-unknown), and emits a remediation report keyed by file + line.

**Ефективно для:**

- AI-authored markdown / MDX is in the PR.
- Documentation site or repo enforces link integrity (docs are user-facing or onboarding-critical).
- There is a known graph of valid methodology slugs / page paths to validate against.

## Applies If (ALL must hold)

- AI-authored markdown / MDX is in the PR.
- Documentation site or repo enforces link integrity (docs are user-facing or onboarding-critical).
- There is a known graph of valid methodology slugs / page paths to validate against.

## Skip If (ANY kills it)

- The doc is a personal scratchpad with no consumers.
- Links are all external (treat as content-marketing post; use a different link-check tool).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Markdown files | md/mdx | PR diff |
| Methodology slug index | json | knowledge/<domain>/INDEX.xml union |
| Site URL map | json | Gatsby/Next/Hugo build output |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace + final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-orphan-link-detection` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/orphan-report.json` | Report skeleton |
| `templates/worked-example.md` | Worked example narrative |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-orphan-link-detection.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
