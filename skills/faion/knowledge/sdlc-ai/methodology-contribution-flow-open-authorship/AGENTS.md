# Methodology Contribution Flow (Open Authorship)

## Summary

**One-sentence:** Defines the open-contribution flow for new faion methodologies — PR template, three-axis review rubric, attribution + revenue-share policy.

**One-paragraph:** External contributors need a documented path to add a methodology to faion. This methodology pins the PR template (topic, tier rationale, prior-art search, draft AGENTS.md + content files, evidence, attribution preference), a three-axis × three-reviewer review rubric, the CLA-grounded attribution policy, and the revenue-share trigger (≥5 accepted contributions → 10% share of attributed CLI-paid-tier revenue). Output is a contribution-flow record validated against the schema before merge.

**Ефективно для:**

- External contributors that want to add domain methodologies under a stable attribution policy.
- Maintainers running structured three-axis review (shape / evidence / duplication).
- Faion governance — ties contribution acceptance to a documented revenue-share policy.
- Audit trail: every accepted methodology has a contribution record with reviewers, owner, decay date.

## Applies If (ALL must hold)

- External contributor wants to add a new methodology to faion-network.
- Topic falls within faion's tier coverage (free / solo / pro / geek).
- Contributor has signed (or is willing to sign) the CLA referenced by the policy.

## Skip If (ANY kills it)

- Internal faion content — different review path applies.
- Minor edits / typo fixes — use a lightweight PR template.
- Non-methodology contribution (skill structure / tooling) — outside scope.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Contributor identity | GitHub handle + signed CLA | contributor |
| Draft methodology | v2 shape (AGENTS.md + content/*.xml) | contributor |
| Prior-art search | search results vs existing methodology + playbook list | contributor |
| Topic + tier rationale | Markdown body | contributor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| project-docs-convention | Defines AGENTS.md + content/*.xml shape this PR must conform to. |
| methodology-versioning-and-changelog | Versioning and CHANGELOG conventions invoked on accept. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: pr-template-required, three-axis-review, attribution-policy, revenue-share-policy, decay-rule | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the contribution-flow record + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: under-reviewed-merge, attribution-stripped, revenue-share-skipped, duplicate-slip-through, stale-contributor-content | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: submit → triage → three-axis review → accept + record → register | 800 |
| `content/06-decision-tree.xml` | essential | Maps PR signals (template-complete? reviewers ≥ 3? attribution + revenue-share captured?) to a verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `triage-pr` | haiku | Template-conformance check; deterministic. |
| `three-axis-review` | sonnet | Cross-axis judgement (shape / evidence / duplication). |
| `policy-finalise` | opus | Attribution + revenue-share evaluation; stakes high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/contribution-record.json` | Schema-conformant contribution record skeleton. |
| `templates/PR-template.md` | Markdown PR template the contributor fills. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-methodology-contribution-flow-open-authorship.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[methodology-versioning-and-changelog]]
- [[shift-log-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
