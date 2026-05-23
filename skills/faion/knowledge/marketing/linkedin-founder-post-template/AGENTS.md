# LinkedIn Founder Post Template

## Summary

**One-sentence:** Produces a 180-220 word founder-voice LinkedIn post spec (hook + setup + insight + CTA) calibrated to the founder's positioning lane and weekly cadence.

**One-paragraph:** Solo founders and micro-agency owners need a repeatable LinkedIn post format that surfaces opinion + lived experience without sliding into bro-marketing tropes. This methodology emits a 180-220 word post spec scoped to one of seven hook types (contrarian, postmortem, customer-quote, day-in-life, mistake, mini-framework, prediction), with a single CTA (no link in body, one CTA in comment), tested for the founder's positioning lane, and ready to ship via Buffer or LinkedIn-native scheduling.

**Ефективно для:**

- Founder з вузькою positioning lane і weekly LinkedIn ritual.
- Заміна generic motivational LinkedIn-постів на opinion-led founder voice.
- Postmortem або contrarian-take формати, де є lived experience.
- Building thought-leadership funnel: 'LinkedIn → booking → consult'.

## Applies If (ALL must hold)

- Founder publishes >= 1 LinkedIn post per week as a positioning move.
- Named positioning lane exists (e.g., 'AI agent integration for Shopify Plus').
- Founder voice / lived experience available (transcripts, ticket data, customer notes).
- CTA is non-immediate (booking, list signup, content series) — not a buy-now button.

## Skip If (ANY kills it)

- Founder cannot allocate 25-40 minutes/post — Buffer-style auto-generators are worse than no post.
- Positioning lane undefined — run niche-positioning-for-solo-dev first.
- Goal is paid acquisition / direct response — switch to paid-ads-creative-library.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-linkedin-founder-post-template` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Markdown spec skeleton |
| `templates/output.json` | JSON spec sidecar with __faion_header__ |
| `templates/_smoke-test.md` | Minimum viable filled spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-linkedin-founder-post-template.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
