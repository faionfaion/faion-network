---
slug: screen-reader-test-script-templates
tier: pro
group: accessibility-specialist
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "78eddb28c83f9c21"
summary: Reusable VoiceOver / NVDA / TalkBack test scripts per UI component archetype — form, modal, table, navigation, autocomplete, video player, toast — that turn the abstract testing-with-assistive-technology methodology into copy-pasteable steps for every audit.
tags: [accessibility, screen-reader, voiceover, nvda, talkback, a11y-audit, testing]
---

# Screen-Reader Test Script Templates

## Summary

**One-sentence:** Library of reusable screen-reader test scripts (VoiceOver macOS, VoiceOver iOS, NVDA Windows, TalkBack Android) per UI component archetype — form, modal, table, navigation, autocomplete, video player, toast — so every audit reuses tested steps instead of inventing them.

**One-paragraph:** Generic accessibility methodologies tell auditors what to test (focus order, labels, live regions) but not how — leaving each auditor to invent the keystrokes, gestures, and expected utterances per component every time. This methodology pins component-archetype scripts that have been validated against WCAG 2.2 AA and against actual screen-reader behaviour on the latest stable releases. Each script lists: pre-conditions, the exact keystroke/gesture sequence per screen reader, the expected utterance pattern, the failure-mode catalogue, and the WCAG SC mapped. Scripts cover the seven highest-traffic component archetypes. Mechanism: pick the archetype that matches the component under audit, run the script verbatim per screen reader, log pass/fail per step. Primary output: a `sr-audit-results.yaml` per audit + per-component findings with WCAG SC traceback.

## Applies If (ALL must hold)

- audit target uses standard HTML semantics or ARIA pattern set
- screen readers available: VoiceOver (macOS + iOS), NVDA (Windows), TalkBack (Android) — at least 2 of the 4
- WCAG 2.2 AA or 2.1 AA is the target conformance level
- auditor has basic screen-reader proficiency (can navigate by headings + landmarks)

## Skip If (ANY kills it)

- target is a non-standard or game-style UI (custom canvas, WebGL, immersive VR) — needs bespoke script
- only one screen reader available — audit is single-platform; document the gap
- WCAG 2.0 AA only — some scripts (e.g. autocomplete) reference 2.1+ criteria; remove those

## Prerequisites

- machines with the four screen readers installed (or a sub-set)
- target build available on real OS (not just browser tools)
- known accounts / data for forms (the script needs real input)
- WCAG SC reference for traceback

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ux/accessibility-specialist/a11y-testing` | Provides the broader audit workflow this slots into |
| `pro/ux/accessibility-specialist/accessibility-first-design` | Component-archetype taxonomy shared |
| `pro/ux/accessibility-specialist/aria-patterns-cheatsheet` | ARIA expectations referenced inside scripts |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: per-platform parity, expected utterance not exact, WCAG mapping per step, fail-stop on showstoppers, build-version pinning | ~1000 |
| `content/02-output-contract.xml` | essential | sr-audit-results.yaml schema, per-script result shape, component archetype list | ~800 |
| `content/03-failure-modes.xml` | essential | 7 failure modes: false-pass on silent failures, version drift, gesture variants, language differences, etc. | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `script_selection_for_component` | haiku | Match component to archetype |
| `audit_results_summarisation` | sonnet | Compact per-script results into findings |
| `wcag_traceback_drafting` | sonnet | Map findings to specific success criteria |
| `developer_friendly_finding_draft` | sonnet | Translate audit output for engineering team |

## Templates

| File | Purpose |
|------|---------|
| `templates/script-form.md` | Form archetype: label, required, error, submission |
| `templates/script-modal.md` | Modal: focus trap, escape, return-focus |
| `templates/script-table.md` | Data table: header association, sortable |
| `templates/script-navigation.md` | Primary nav: landmarks, current, expanded state |
| `templates/script-autocomplete.md` | Combobox per ARIA Authoring Practices |
| `templates/script-video-player.md` | Player: captions, controls, transcript |
| `templates/script-toast.md` | Live region announcement |
| `templates/sr-audit-results.schema.yaml` | Result schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/audit-runner.py` | Walks the component list, opens the matching script in the auditor's terminal, captures pass/fail | During audit session |
| `scripts/wcag-rollup.py` | Aggregates per-script results into a per-SC compliance summary | After audit complete |

## Related

- parent skill: `pro/ux/accessibility-specialist/`
- peer methodologies: `a11y-testing`, `aria-patterns-cheatsheet`, `accessibility-first-design`, `ada-title-ii-compliance-2026`
- external: [WAI-ARIA Authoring Practices 1.2](https://www.w3.org/WAI/ARIA/apg/) · [WebAIM screen-reader survey](https://webaim.org/projects/screenreadersurvey/) · [Deque axe DevTools](https://www.deque.com/axe/) · [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
