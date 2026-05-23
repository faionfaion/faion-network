---
slug: swipe-file-tweet-hooks
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a tagged swipe-file config (hook taxonomy, source URL, performance baseline, attribution) for build-in-public audience growth (0 → 5K)."
content_id: "4bd2d230d125e326"
complexity: light
produces: config
est_tokens: 3000
tags: [swipe-file, hooks, tweets, build-in-public, solo]
---

# Swipe File Tweet Hooks

## Summary

**One-sentence:** Produces a tagged swipe-file config (hook taxonomy, source URL, performance baseline, attribution) for build-in-public audience growth (0 → 5K).

**Ефективно для:** Indie hackers building in public who keep re-deriving hooks from scratch and have no record of what hook shapes converted in their own history.

**One-paragraph:** Swipe files exist as random docs of tweets; they don't usually carry a hook taxonomy, source URL, or performance baseline. This methodology produces a config file with each entry tagged by hook-shape (contrarian / curious-gap / list-of-N / personal-failure / data-reveal), the verbatim hook, the source URL + author handle (for attribution), and the baseline impressions the original hit. Output is consumed by the operator's drafting tool to seed new tweets without plagiarism.

## Applies If (ALL must hold)

- Operator runs build-in-public on X for audience growth (0 → 5K range).
- Operator can curate ≥20 hooks before first use.
- Attribution discipline is acceptable (no plagiarism).
- Storage path for the swipe file is decided.

## Skip If (ANY kills it)

- Operator copies hooks verbatim into own tweets — that's plagiarism, not swipe-filing.
- B2B audience where hook shapes are different (LinkedIn-style).
- Curation < 20 entries — file too thin to be useful.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| ≥20 high-performing source tweets identified | list of URLs | manual curation |
| hook taxonomy (5+ shapes) | list | internal decision |
| storage path (JSON or YAML) | file path | founder decision |
| attribution policy (cite author when adapting) | string | founder decision |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/marketing/smm-manager/growth-twitter-x-growth` | Downstream growth playbook. |
| `solo/marketing/smm-manager/tweet-thread-launch-template` | Downstream launch template. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations + JSON schema | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `tag_hook_shape` | haiku | Bounded classification. |
| `draft_adapted_hook` | sonnet | New-hook generation from swipe shape. |
| `audit_attribution` | opus | Cross-source plagiarism + credit check. |

## Templates

| File | Purpose |
|---|---|
| `templates/swipe-file-tweet-hooks.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/swipe-file-tweet-hooks.md` | Markdown skeleton with the required fields. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-swipe-file-tweet-hooks.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[growth-twitter-x-growth]] — consumer.
- [[tweet-thread-launch-template]] — consumer.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
