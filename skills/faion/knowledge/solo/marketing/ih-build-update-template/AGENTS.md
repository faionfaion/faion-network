---
slug: ih-build-update-template
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Per-post Indie Hackers build-update template optimised for the IH algorithm — TL;DR + 3 numbers + 1 ask, 600-1200 chars body, weekly cadence.
content_id: "34627a4a80ffb26f"
complexity: medium
produces: spec
est_tokens: 4300
tags: [indie-hackers, build-update, posting-cadence, social, distribution]
---
# Indie Hackers Build-Update Template

## Summary

**One-sentence:** Per-post Indie Hackers build-update template optimised for the IH algorithm — TL;DR + 3 numbers + 1 ask, body 600-1200 chars, weekly cadence on Tuesday morning ET.

**One-paragraph:** `growth-indiehackers-strategy` covers the broad IH platform play; this template is the per-post fill-in. The IH algorithm rewards posts that lead with a TL;DR, surface 3 concrete numbers (MRR, signup count, conversion, churn, retention) and end with one specific ask answerable in &lt;1 min. Body sweet spot is 600-1200 chars (above 1500 buries the ask; below 400 reads as low-effort). Posts on Tuesday 8-10am ET reliably out-perform other slots. Output is a markdown post draft + scheduled cadence.

**Ефективно для:**

- Solo founders building in public on IndieHackers ≥1×/week.
- Converting build-progress into qualified replies (founder-mode operators read IH for signal).
- Stacking with a hook-bank methodology — the IH post is one row in the bank.
- Recruiting affiliates / co-marketers from the IH audience.

## Applies If (ALL must hold)

- Operator has an Indie Hackers account and is shipping a product or service.
- Operator has at least 3 numeric signals this week (MRR delta, signup count, conv rate, etc.).
- A specific ask exists (e.g. "Which of these three landing-page variants reads cleaner?").
- Operator can post within the Tuesday 8-10am ET window OR has scheduling enabled.

## Skip If (ANY kills it)

- Nothing shipped or measured this week — IH has zero tolerance for "thoughts" posts.
- The product is enterprise B2B with no public surface — IH audience cannot reciprocate.
- Operator already pushed an IH post within the last 72h — over-posting hurts reach.
- No genuine ask available — fake asks burn trust.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 3 numeric signals from the last 7 days | scalars | analytics / billing |
| TL;DR draft ≤180 chars | string | founder |
| Specific ask | string | founder |
| Product link or screenshot | URL / image | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[hook-bank-template]] | IH post hooks feed the bank; bank patterns feed the hook draft. |
| [[icp-fit-scorecard-solo]] | Replies from IH are an input signal for the scorecard. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: TL;DR ≤180, 3 numbers required, 1 ask, 600-1200 char body, Tue 8-10am ET, weekly cadence | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for IH post bundle + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix): no numbers, vague ask, wall of text, off-slot post | 700 |
| `content/04-procedure.xml` | essential | 6-step procedure: collect numbers → draft TL;DR → write body → set ask → schedule slot → log reply outcomes | 800 |
| `content/05-examples.xml` | essential | Worked example: full post with 3 numbers + ask + observed reply pattern | 600 |
| `content/06-decision-tree.xml` | essential | Tree routing observable signals → rule id | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `numbers_extraction` | haiku | Mechanical CSV read. |
| `tldr_drafting` | sonnet | 180-char hook with tone control. |
| `body_writing` | sonnet | 600-1200 char narrative tying numbers to the ask. |
| `reply_outcome_tagging` | sonnet | Classify qualified vs noise replies after 24h. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ih-post.md` | IH post skeleton with required sections |
| `templates/reply-triage.csv` | Reply outcome log for the bank |
| `templates/_smoke-test.json` | Minimum viable IH post bundle for validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ih-build-update-template.py` | Validate IH post bundle (TL;DR length, body char range, 3 numbers, ask present) against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[hook-bank-template]]
- [[icp-fit-scorecard-solo]]
- [[gumroad-ops-playbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps numeric-signal availability, ask quality, body length, and slot timing to a rule from `01-core-rules.xml`, telling the agent whether to publish, block on a missing element, or skip the week. Walk it on every fresh post; do not cache outcomes across posts.
