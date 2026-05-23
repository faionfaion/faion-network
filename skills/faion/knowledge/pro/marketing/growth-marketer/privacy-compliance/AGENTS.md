---
slug: privacy-compliance
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Privacy-by-default analytics setup: CMP with deny-default consent, GA4 Consent Mode v2 wiring, CCPA GPC signal handling, IP anonymization, and a tag-firing audit log.
content_id: "b44f392c25727ca4"
complexity: deep
produces: config
est_tokens: 4200
tags: [privacy, gdpr, ccpa, analytics, consent, tracking]
---
# Privacy-Compliant Analytics

## Summary

**One-sentence:** Privacy-by-default analytics setup: CMP with deny-default consent, GA4 Consent Mode v2 wiring, CCPA GPC signal handling, IP anonymization, and a tag-firing audit log.

**One-paragraph:** Privacy-by-default analytics setup: CMP with deny-default consent, GA4 Consent Mode v2 wiring, CCPA GPC signal handling, IP anonymization, and a tag-firing audit log. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Команди що запускають GA4 / Mixpanel / Segment у EU або CA traffic.
- Перед публічним launch — щоб не отримати CMP-shaming на Twitter day-1.
- При додаванні нового pixel / tag — як gate перевірки.
- Audit existing analytics на default-deny + GPC signal.

## Applies If (ALL must hold)

- Production-traffic site з > 10% користувачів з EU/EEA/UK/CA.
- Доступ до tag manager (GTM / Tealium) + CMP (OneTrust / Cookiebot / Sourcepoint / Klaro).
- Технічна команда здатна на dataLayer + Consent Mode v2 wiring.

## Skip If (ANY kills it)

- Internal-only / authenticated app з 0 anonymous tracking — менш стрімкі вимоги.
- 100% non-EU/CA traffic + no PII collected — мінімальна compliance baseline достатня.
- Static-marketing site з 0 tracking — нічого не gate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-tradeoffs` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-skeleton.md` | Privacy-Compliant Analytics skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Privacy-Compliant Analytics. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-privacy-compliance.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[conversion-tracking]]
- [[google-analytics]]
- [[ops-metrics-basics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
