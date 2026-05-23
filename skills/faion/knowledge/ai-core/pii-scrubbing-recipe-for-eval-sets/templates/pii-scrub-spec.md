<!-- purpose: pii-scrub-spec narrative markdown skeleton -->
<!-- consumes: pii-scrub-spec.json artefact -->
<!-- produces: human-readable review draft -->
<!-- depends-on: content/02-output-contract.xml schema -->
<!-- token-budget-impact: ~200 tokens when loaded as context -->

# PII Scrub Spec — `<artefact_id>`

- **Owner:** `<handle-or-role>`
- **Version:** `1.0.0`
- **Last reviewed:** `2026-05-22`

## Inputs used

| Name | Source |
|------|--------|
| traffic_sample | `warehouse://<table>` |
| consent_dict | `git://<repo>/consent.yaml` |
| retention_policy | `git://<repo>/legal/retention.yaml` |

## Scrub strategy

- **Mode:** `regex_plus_ml`
- **Rules:** email, phone, credit_card, ml-ner-person

## Consent

- **Field:** `user.consent.eval_v1`
- **Rows dropped (missing flag):** `<count>`

## Retention

- **Days:** `365`
- **Class:** `<row_class>`

## Audit

Spec validated by `scripts/validate-pii-scrubbing-recipe-for-eval-sets.py` on `<date>`. Reviewed by `<reviewer>`.
