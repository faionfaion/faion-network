---
slug: adr-staleness-audit
tier: pro
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "e4b2c01d81f4fff9"
summary: Quarterly audit cadence and rubric for marking ADRs accepted / superseded / deprecated / re-open based on staleness signals.
tags: [adr, architecture, audit, staleness, governance, quarterly]
---
# ADR Staleness Audit

## Summary

**One-sentence:** Quarterly audit cadence and rubric for marking ADRs accepted / superseded / deprecated / re-open based on staleness signals.

**One-paragraph:** ADRs decay silently — an "accepted" status from 2 years ago may describe something the team stopped doing 14 months ago. Mechanism: a quarterly audit walks every ADR with status="accepted" or "proposed" and applies a 4-signal rubric — (1) code reality match (does the codebase still implement the decision?), (2) stakeholder still present (did the original signer still own this?), (3) reversal triggers fired (any pre-mortem trigger hit?), (4) external context changed (new constraints, regulations, vendor changes). ADR moves to: accepted (no change), superseded (linked to new ADR), deprecated (decision abandoned, no successor), or re-open (active reconsideration). Output: an audit doc + a roadmap of which ADRs need superseding work.

## Applies If (ALL must hold)

- repo has ≥ 10 accepted ADRs older than 6 months
- there is a named architecture owner (architect, tech lead, founder) who runs the audit
- ADRs are in a versioned location (git, wiki with history) so changes are auditable
- the team accepts that ADRs need re-review (not "set and forget")

## Skip If (ANY kills it)

- &lt; 10 ADRs — manual ad-hoc review is sufficient
- ADRs in narrative form without testable decision sections — can't audit reality match
- decision velocity &gt; quarterly cadence (very fast-moving team) — use a monthly audit instead
- using `adr-decay-detector-agent` already — agent handles the code-reality-match signal continuously; staleness audit becomes lighter

## Prerequisites (must be true before starting)

- list of accepted ADRs with their decision date + signers
- current org chart (who's still here)
- ADR-decay-detector output if running, OR manual code-reality check capacity
- pre-mortem reversal-triggers per one-way-door ADR (if `adr-reversibility-tagging` is in use)
- a quarterly review window scheduled (1-2 days for ~30 ADRs)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | Base ADR format the audit reads |
| `solo/dev/software-architect/adr-reversibility-tagging` | Reversibility tier drives audit priority |
| `geek/sdlc-ai/kb-adr-decay-detector-agent` | Continuous decay signal feeds the audit |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 4-signal rubric, immutable supersession, prioritize by reversibility, audit cadence quarterly, evidence-backed | ~900 |
| `content/02-output-contract.xml` | essential | Audit-report schema, ADR-state-transition schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (delete-not-supersede, audit drift, ghost-signer ignored, weak evidence, bulk-status-flip, no follow-up) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `signal_score_per_adr` | sonnet | 4-signal scoring with deterministic mapping |
| `code_reality_match_check` | sonnet | Per-ADR evidence pull from code |
| `audit_rollup_synthesis` | opus | Cross-ADR pattern detection (e.g., all 2023 ADRs from departed lead are stale) |
| `supersession_action_draft` | sonnet | Draft a new ADR that supersedes a stale one |

## Templates

| File | Purpose |
|------|---------|
| `templates/staleness-audit-report.md` | Audit roll-up doc structure |
| `templates/adr-state-transition.md` | Per-ADR decision record (accepted/superseded/deprecated/re-open) |
| `templates/supersession-adr.md` | Skeleton for the new ADR that supersedes a stale one |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/score-staleness.py` | Score every ADR on the 4 signals | Quarterly audit kickoff |
| `scripts/generate-supersession-skeleton.py` | Bootstrap a new ADR from a stale one's text | After audit decides supersede |

## Related

- parent skill: `pro/dev/software-architect/`
- peer methodologies: `architecture-decision-records`, `adr-reversibility-tagging`, `adr-decay-detector-agent`
- external: [Nygard - ADR follow-up](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) · [MADR superseded status](https://adr.github.io/madr/) · [ThoughtWorks - living-architecture](https://www.thoughtworks.com/radar)
