<!-- purpose: filled-in canonical signing document for calibration (Northwind Field) -->
<!-- consumes: nothing — this is a hand-filled fixture -->
<!-- produces: document instance that MUST validate via scripts/validate-ios-signing-and-provisioning.py -->
<!-- depends-on: templates/output.md, content/02-output-contract.xml -->
<!-- token-budget-impact: ~900 tokens -->

# Ios Signing And Provisioning — Smoke Test Fixture

The valid example from `content/02-output-contract.xml`; `scripts/validate-ios-signing-and-provisioning.py --self-test` runs it.

```json
{
  "app": {
    "name": "Northwind Field",
    "bundle_id": "com.northwind.field",
    "built_for_client": true,
    "owning_account": "client",
    "owning_team_id": "A1B2C3D4E5",
    "agency_role_on_client_account": "App Manager"
  },
  "secret_store": {
    "kind": "fastlane_match",
    "location": "git@github.com:northwind/ios-certificates.git (match, encrypted)",
    "readers": [
      "ci:github-actions/northwind-field",
      "maria@agency.example",
      "release-lead@northwind.example"
    ]
  },
  "private_keys_outside_secret_store": false,
  "certificates": [
    {
      "type": "distribution",
      "identifier": "Apple Distribution: Northwind Ltd (A1B2C3D4E5), serial 6F3A9C2E",
      "expiry": "2027-02-14",
      "storage_location": "match: certs/distribution/6F3A9C2E.p12",
      "shared_by_team": true
    },
    {
      "type": "development",
      "identifier": "Apple Development: CI (A1B2C3D4E5), serial 1D8B44A0",
      "expiry": "2027-02-14",
      "storage_location": "match: certs/development/1D8B44A0.p12",
      "shared_by_team": true
    }
  ],
  "profiles": [
    {
      "name": "match AppStore com.northwind.field",
      "bundle_id": "com.northwind.field",
      "type": "app_store",
      "uuid": "c4d1a2e6-7f3b-4a9c-9d2e-0b1f5a6c7d8e",
      "expiry": "2027-02-14",
      "storage_location": "match: profiles/appstore/"
    },
    {
      "name": "match Development com.northwind.field",
      "bundle_id": "com.northwind.field",
      "type": "development",
      "uuid": "9a8b7c6d-5e4f-4a3b-8c2d-1e0f9a8b7c6d",
      "expiry": "2027-02-14",
      "storage_location": "match: profiles/development/"
    }
  ],
  "asc_api_keys": [
    {
      "key_id": "K7M2P9Q4RS",
      "issuer_id": "69a6de8e-1234-47e3-e053-5b8c7c11a4d1",
      "role": "App Manager",
      "used_by": "github-actions/northwind-field upload-testflight",
      "p8_storage_location": "GitHub Actions secret ASC_KEY_P8 (org: northwind)",
      "p8_stored_at_issue": true
    }
  ],
  "push": {
    "auth": "token_key",
    "key_id": "T3N8V5W2XY",
    "team_id": "A1B2C3D4E5",
    "p8_storage_location": "backend vault: secret/apns/northwind-field.p8"
  },
  "build_configs": [
    {
      "name": "debug",
      "aps_environment": "development",
      "apns_host": "api.sandbox.push.apple.com"
    },
    {
      "name": "testflight",
      "aps_environment": "production",
      "apns_host": "api.push.apple.com"
    },
    {
      "name": "app_store",
      "aps_environment": "production",
      "apns_host": "api.push.apple.com"
    }
  ],
  "rotation_calendar": [
    {
      "asset": "Apple Distribution serial 6F3A9C2E",
      "expiry": "2027-02-14",
      "rotate_by": "2027-01-10",
      "lead_days": 35,
      "owner": "maria@agency.example"
    },
    {
      "asset": "Apple Development serial 1D8B44A0",
      "expiry": "2027-02-14",
      "rotate_by": "2027-01-10",
      "lead_days": 35,
      "owner": "maria@agency.example"
    },
    {
      "asset": "profile c4d1a2e6 (App Store)",
      "expiry": "2027-02-14",
      "rotate_by": "2027-01-10",
      "lead_days": 35,
      "owner": "maria@agency.example"
    },
    {
      "asset": "profile 9a8b7c6d (Development)",
      "expiry": "2027-02-14",
      "rotate_by": "2027-01-10",
      "lead_days": 35,
      "owner": "maria@agency.example"
    }
  ],
  "revocation_runbook": {
    "who_may_revoke": [
      "release-lead@northwind.example",
      "maria@agency.example"
    ],
    "impact": [
      {
        "certificate_type": "distribution_app_store",
        "installed_builds": "keep_launching",
        "pipelines_broken": [
          "github-actions/northwind-field release"
        ]
      },
      {
        "certificate_type": "development",
        "installed_builds": "stop_launching",
        "pipelines_broken": [
          "github-actions/northwind-field pr-build"
        ]
      },
      {
        "certificate_type": "apns",
        "installed_builds": "not_applicable",
        "pipelines_broken": [
          "backend push sender"
        ]
      }
    ],
    "regeneration_order": [
      "revoke in the portal",
      "fastlane match nuke <type> then match <type>",
      "regenerate profiles for the bundle id",
      "rotate CI secrets",
      "run a TestFlight build and a push smoke test"
    ],
    "verified_against": "https://developer.apple.com/help/account/certificates/revoke-a-certificate/"
  },
  "review": {
    "status": "ready_for_review",
    "reviewer": "release-lead@northwind.example",
    "binding_action_performed_by_agent": false
  }
}
```
