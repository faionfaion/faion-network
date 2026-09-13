<!-- purpose: minimum-viable filled-in offboard artefact for smoke testing -->
<!-- consumes: nothing — this is a hand-filled fixture -->
<!-- produces: artefact instance that MUST validate via scripts/validate-graceful-offboard-script.py -->
<!-- depends-on: templates/graceful-offboard-script.md, content/02-output-contract.xml -->
<!-- token-budget-impact: ~700 tokens -->

# Graceful Offboard Script — Smoke Test Fixture

The valid example from `content/02-output-contract.xml`; `scripts/validate-graceful-offboard-script.py --self-test` runs it.

```json
{
  "client": {
    "name": "Northwind Retail",
    "account_owner": "maria@agency.example",
    "sponsor_contact": "tom@northwind.example"
  },
  "qbr_source": "qbr/2026-q2/northwind.xlsx",
  "bad_fit_signals": [
    {
      "kind": "gross_margin_below_target",
      "value": 11,
      "target": 30,
      "period": "2025-Q4 to 2026-Q2",
      "consecutive_quarters": 3
    },
    {
      "kind": "out_of_scope_requests_above_cap",
      "value": 14,
      "target": 4,
      "period": "2026-Q2"
    }
  ],
  "contract": {
    "termination_clause_id": "MSA 14.2",
    "notice_days": 30,
    "decision_date": "2026-06-05",
    "last_service_date": "2026-07-10",
    "days_notice_given": 35,
    "prepaid_period": {
      "exists": true,
      "disposition": "delivered_in_full",
      "amount": 3200
    }
  },
  "script": {
    "framing": "fit_and_alignment",
    "fit_statement": "Your roadmap has moved toward in-store systems integration; we are built for e-commerce growth work, and you will get more from a partner whose core is integration.",
    "states_last_service_date": true,
    "banned_phrases_found": [],
    "client_criticism_found": false
  },
  "handover": {
    "assets": [
      {
        "name": "Google Ads account 123-456-7890",
        "kind": "ad_account",
        "owned_by": "client",
        "transfer_method": "admin access transferred to tom@northwind.example, agency access removed",
        "transfer_date": "2026-07-03",
        "conditioned_on_payment": false
      },
      {
        "name": "northwind.example DNS at Cloudflare",
        "kind": "domain_dns",
        "owned_by": "client",
        "transfer_method": "zone ownership moved to client's Cloudflare account",
        "transfer_date": "2026-07-06",
        "conditioned_on_payment": false
      },
      {
        "name": "GA4 property 987654321",
        "kind": "analytics_account",
        "owned_by": "client",
        "transfer_method": "client made Administrator, agency demoted then removed",
        "transfer_date": "2026-07-03",
        "conditioned_on_payment": false
      },
      {
        "name": "github.com/agency/northwind-storefront",
        "kind": "source_repository",
        "owned_by": "client",
        "transfer_method": "repository transferred to client GitHub org",
        "transfer_date": "2026-07-08",
        "conditioned_on_payment": false
      },
      {
        "name": "Figma: Northwind design system",
        "kind": "design_files",
        "owned_by": "client",
        "transfer_method": "file ownership transferred to client Figma team",
        "transfer_date": "2026-07-08",
        "conditioned_on_payment": false
      },
      {
        "name": "Runbooks and campaign documentation",
        "kind": "documentation",
        "owned_by": "client",
        "transfer_method": "exported to client Google Drive folder",
        "transfer_date": "2026-07-09",
        "conditioned_on_payment": false
      }
    ],
    "transition_support": {
      "days": 30,
      "cost": "included"
    }
  },
  "alternatives": [
    {
      "provider": "Bridgeport Systems",
      "matched_need": "ERP and POS integration for mid-size retail, the direction Northwind's roadmap is taking",
      "confirmed_on": "2026-06-02",
      "confirmed_via": "call",
      "warm_introduction_offered": true
    }
  ],
  "delivery": {
    "live_conversation": {
      "date": "2026-06-05",
      "channel": "video_call",
      "delivered_by": "maria@agency.example"
    },
    "written_follow_up": {
      "date": "2026-06-05",
      "business_days_after_conversation": 0,
      "contains_only_what_was_said": true,
      "includes_handover_plan": true
    },
    "email_only": false
  },
  "feedback_request": {
    "scheduled_date": "2026-08-09",
    "days_after_last_service": 30,
    "promoter_action": "ask_for_testimonial_and_referral",
    "non_promoter_action": "thank_and_ask_one_question_no_argument"
  },
  "internal_record": {
    "root_cause_category": "scope_and_expectations",
    "intake_change": "Qualification call now asks for a scope-change budget and a named change-approver; retainers without both are not signed",
    "flagged_for_review": false
  }
}
```
