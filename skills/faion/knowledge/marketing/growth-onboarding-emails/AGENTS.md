# Behavior-Triggered Onboarding Emails

## Summary

**One-sentence:** Produces a behavior-triggered onboarding sequence artefact firing on user action/inaction, with one CTA per email and an escalation ladder.

**One-paragraph:** Solo products ship time-only drips and lose stuck users silently. This methodology pins a behavior-triggered onboarding sequence: every email fires on a tracked behavior, one CTA per email matching the next activation step, an escalation ladder for users stuck ≥3 times, and immediate suppression on activation. Output: an onboarding-sequence spec wired to a named activation event.

**Ефективно для:**

- готова основа для повторюваної задачі «growth-onboarding-emails» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Product has a named activation event tracked in analytics.
- ESP supports behavior triggers (not just time drips).
- Operator can wire activation-event suppression on the sequence.

## Skip If (ANY kills it)

- Pre-activation event definition — sequence cannot be measured.
- ESP that only supports time drips — switch ESP first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Activation event definition | tracked event name | analytics config |
| User behavior log for last 30 days | CSV / dashboard | Mixpanel / PostHog |
| Onboarding step map | diagram / doc | product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer/` | Parent role / operating context. |
| `solo/marketing/content-marketer/growth-email-marketing` | Email-program substrate this sequence rides on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the onboarding-sequence artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-onboarding-emails.md` | Markdown skeleton: artefact body + per-section table. |
| `templates/growth-onboarding-emails.json` | onboarding-sequence JSON skeleton validating against scripts/. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-onboarding-emails.py` | Validate the onboarding-sequence artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[growth-email-marketing]]
- [[indie-mini-crm-notion]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
