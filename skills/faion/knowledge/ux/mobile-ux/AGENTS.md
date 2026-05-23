# Mobile UX Design Basics

## Summary

**One-sentence:** Produce a mobile UX audit report covering touch targets, thumb-zone placement, navigation pattern, input types, Core Web Vitals, and platform conformance against hard thresholds (44pt/48dp, LCP<2.5s, CLS<0.1).

**One-paragraph:** Apply mobile-first design (smallest screen first, then enhance). Inputs: live URL or build + screen-by-screen UI inventory. Output: a mobile audit report with one finding per violation (category | element | observed-value | threshold | platform | fix-direction). Thresholds are hard: touch targets ≥44x44pt (iOS) / 48x48dp (Android); one primary action per screen; bottom tabs (3-5) for primary navigation; LCP<2.5s, FID<100ms, CLS<0.1.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- The product is intended to run on mobile (web responsive, iOS, or Android).
- A reviewable mobile build / URL / screen inventory exists.
- Touch interaction is the primary input modality.

## Skip If (ANY kills it)

- Internal tools used exclusively on desktop (admin panels via VPN).
- Mobile is explicitly out of scope for the current phase.
- Accessibility-only audit — overlaps but is not a replacement for dedicated a11y review.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Mobile build URL or app build | URL / artefact | engineering |
| Screen inventory (route → screen name) | list | PM |
| Target platforms (iOS / Android / web) | doc | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/wireframing` | Wireframes are the upstream source of layout decisions. |
| `solo/ux/ux-ui-designer/visibility-of-system-status` | Loading states must hit the same thresholds on mobile. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules + skip-this-methodology fallback | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the mobile-audit report + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure: inventory → measure → categorise → cite-evidence → fix-direction → re-test | ~600 |
| `content/05-examples.xml` | medium | Worked audit example for a checkout flow | ~500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `lighthouse-pull` | haiku | Mechanical pull of LCP/FID/CLS metrics. |
| `touch-target-audit` | sonnet | Screen-by-screen measurement of tap-target sizes. |
| `platform-conformance` | opus | iOS HIG vs Material guideline interpretation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mobile-audit-report.md` | Mobile audit report skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mobile-ux.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |
| `scripts/mobile-audit.sh` | Run Lighthouse mobile audit + summarise Core Web Vitals. | At step 2 (measure) when a URL is reachable. |

## Related

- [[wireframing]]
- [[visibility-of-system-status]]
- [[recognition-over-recall]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, mobile build reachable, target platforms named) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
