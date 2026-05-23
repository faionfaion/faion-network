---
slug: screen-reader-test-script-templates
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Per-flow screen-reader test script (NVDA / VoiceOver / TalkBack) with expected announcements, gestures, and pass/fail criteria.
content_id: "d9610ac5824eb17a"
complexity: medium
produces: report
est_tokens: 4100
tags: [screen-reader, nvda, voiceover, talkback, testing, a11y]
---
# Screen Reader Test Script Templates

## Summary

**One-sentence:** Per-flow screen-reader test script (NVDA / VoiceOver / TalkBack) with expected announcements, gestures, and pass/fail criteria.

**One-paragraph:** AT testing without scripted steps produces unreproducible results. This methodology pins per-flow test scripts: device + SR + version, gesture or shortcut sequence, expected announcement strings, and pass/fail criteria. Output is a versioned SR test script that any tester (human or agent) can replay deterministically.

**Ефективно для:**

- Reproducible AT tests across testers, releases, devices.
- Pass/fail criteria removes 'I thought I heard X' ambiguity.
- Expected announcements pinned to actual SR strings.
- Per-SR script captures platform-specific behaviour (e.g. VO rotor vs NVDA browse-mode).

## Applies If (ALL must hold)

- Repeatable AT testing required across releases or environments.
- Multiple testers (or agents) will run the same script.
- Audit baseline references screen-reader findings.

## Skip If (ANY kills it)

- One-off exploratory SR pass — capture as notes, not as a script.
- Flows with no SR-relevant interaction (pure video player) — defer to media-player a11y.
- Pre-AT phase — run `a11y-basics` first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Flow under test | URL or app screen sequence | product |
| Target SR + version | NVDA 2024.x / VoiceOver iOS 17.x / TalkBack 14.x | device fleet |
| WCAG SC mapping | SC list expected to be exercised | audit baseline |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| a11y-basics | Provides WCAG POUR / conformance vocabulary used across the accessibility-specialist domain. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with sourced rationale + skip-this-methodology + run-the-checklist | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure (input / action / output / decision-gate) | 800 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs (preconditions, severity, modality) to a rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `triage-inputs` | haiku | Mechanical scrape from inputs. |
| `apply-rules` | sonnet | Per-rule judgement on inputs. |
| `synthesise-artefact` | sonnet | Aggregates rule outcomes into the final artefact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sr-test-script.md` | Markdown skeleton for SR test script. |
| `templates/sr-test-script.json` | JSON schema-conformant script. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-screen-reader-test-script-templates.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[testing-with-assistive-technology]]
- [[a11y-testing]]
- [[wcag-22-compliance]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
