# Creative Brief Template

## Summary

**One-sentence:** Standardized creative brief artefact for paid-ads campaign launches — audience, angle, hook, proof, CTA, format constraints — every field typed + sourced + owner-named.

**One-paragraph:** Paid-ads playbooks reference creative variants but faion lacks a standardized creative-brief artefact. This methodology pins a 7-field typed schema (audience, angle, hook, proof, CTA, format, owner) where every field cites an input source and refuses generic placeholders. Core rules: one brief per campaign instance, every input typed and sourced, named individual owner (not "team"), versioned + dated, every creative decision traces to an input. Output: a versioned brief that designers + media buyers can act on without re-deriving rationale.

**Ефективно для:**

- Paid-ads campaign launch — спільний brief для creative + media buying.
- Перезапуск кампанії з новим angle — versioned brief carries delta vs prior.
- Multi-variant ad testing — кожен variant traces до hook/angle in brief.
- Agency / freelance handoff — typed contract, без "use your judgment".

## Applies If (ALL must hold)

- Paid-ads campaign launch (Meta, Google, LinkedIn, TikTok) within ≤30 days.
- Named designer + named media buyer will consume the brief downstream.
- ≥2 creative variants planned (otherwise the brief is overkill).
- A previous campaign or baseline exists for the audience or close enough to anchor numbers.

## Skip If (ANY kills it)

- One-off post on owned channels — overhead exceeds value.
- Brand-awareness campaign with no direct-response metric — different brief shape.
- Regulated industry where ad copy must go through legal — defer to legal SOP.
- No named owner — brief will be orphaned regardless of quality.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target audience definition | spec / persona doc | growth team / ICP doc |
| Past campaign results (if any) | report / CSV | ads platform export |
| Product proof points (case studies, numbers) | list | marketing wiki |
| Brand voice guidelines | doc | brand team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[paid-ads-creative-library]] | Source of past creative variants for inspiration / dedup |
| [[icp-message-mining-from-ai-conversations]] | Audience phrasing + objection list |
| [[experiment-hypothesis-scoring]] | Brief feeds an experiment hypothesis downstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: one-brief-per-campaign, typed-and-sourced-input, named-owner, versioned-and-dated, traceable-decision | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the brief + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure: assemble inputs → fill template → validate → owner sign-off → publish | 700 |
| `content/05-examples.xml` | essential | Worked example: Meta lead-gen campaign brief for a B2B SaaS | 500 |
| `content/06-decision-tree.xml` | essential | Tree: which fields are required vs optional per campaign type | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-brief` | sonnet | Per-campaign judgment with bounded inputs. |
| `lint-fields` | haiku | Mechanical schema check + banned-token filter. |
| `review-compliance` | opus | Cross-input synthesis for regulated copy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/creative-brief.md` | Markdown skeleton with every required field labelled |
| `templates/creative-brief.json` | JSON example matching the output contract |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-creative-brief-template.py` | Validate brief JSON against the output-contract schema | After draft; before designer handoff |

## Related

- [[paid-ads-creative-library]]
- [[icp-message-mining-from-ai-conversations]]
- [[experiment-hypothesis-scoring]]
- [[experiment-verdict-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree decides which brief fields are mandatory by campaign type (lead-gen vs conversion vs retargeting vs brand) and routes the agent to the relevant rule from `01-core-rules.xml`. Use it before filling the template — mandatory-vs-optional differs by campaign shape.
