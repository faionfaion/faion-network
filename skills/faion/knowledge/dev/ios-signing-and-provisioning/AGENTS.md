# Ios Signing And Provisioning

## Summary

**One-sentence:** Documents iOS signing: provisioning profiles, App Store Connect API keys, push certs, rotation cadence.

**One-paragraph:** Documents iOS signing: provisioning profiles, App Store Connect API keys, push certs, rotation cadence. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness without re-deriving the rationale.

**Ефективно для:**

- Pro-tier dev workflow, де потрібен auditable artefact замість ad-hoc decision.
- Команди, де ≥2 stakeholders читають один артефакт і повинні дійти однакового висновку.
- Cases where input must be cited (no fabrication) і decision-trail зберігається для review.
- Recurring trigger, що з'являється ≥1 раз на cycle і виправдовує methodology overhead.

## Applies If (ALL must hold)

- The app ships through Apple signing: App Store, TestFlight, ad-hoc or enterprise builds.
- The operator has read access to Certificates, Identifiers and Profiles in the Apple Developer portal and to Users and Access in App Store Connect, so every expiry and Key ID can be read rather than assumed.
- A secret store exists or can be created (CI secrets, fastlane match, or the team password manager) to hold `.p12` and `.p8` material.
- The backend's APNs sender configuration and the Xcode entitlements per build configuration are readable.
- A named human can approve revocation, rotation, transfer and submission.

## Skip If (ANY kills it)

- No Apple signing chain: web app, simulator-only builds, or Android-only.
- The portal and App Store Connect are unreachable, so expiries and roles cannot be read; a document built from memory is the failure the inventory exists to prevent.
- Signing is fully owned by a third-party release service under its own contract and the team holds no key material; document the vendor boundary instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Certificate list with type, serial or SHA and expiry | portal export or screenshot | Apple Developer portal, Certificates |
| Provisioning profiles with bundle ID, type, UUID and expiry | portal export or `security cms -D -i profile.mobileprovision` | Apple Developer portal, Profiles |
| App Store Connect API keys with Key ID, Issuer ID, role and consumer | Users and Access, Keys tab | App Store Connect |
| APNs credential: auth key (Key ID, Team ID) or certificate with expiry | portal Keys tab or Certificates | Apple Developer portal |
| App record Team ID and, for a client app, the client's Team ID and the agency's role | App Store Connect app page, Users and Access | App Store Connect |
| Secret store name, location and reader list | CI settings, match repo, or password-manager vault | platform / release engineering |
| `aps-environment` per build configuration and the APNs host the backend targets per environment | entitlements files, backend config | app repository, backend repository |
| Apple's current documentation on certificate revocation impact | URL under developer.apple.com | Apple Developer Help |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/dev/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: asset inventory, APNs token key over cert, keys in secret store, ASC API key least privilege, rotation calendar with lead time, aps-environment per build config, client account owns app, revocation impact | 1900 |
| `content/02-output-contract.xml` | essential | Draft-07 schema: app ownership with Team ID and transfer plan, secret store and readers, certificates / profiles / ASC keys / APNs credential with identifier, expiry and storage, least-privilege key roles, token-key push, aps-environment to host map per build config, rotation calendar with 30-day lead and owner, revocation runbook verified against Apple, review with no agent binding action; valid + invalid examples, forbidden patterns | ~4850 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 1200 |
| `content/04-procedure.xml` | essential | 8 steps: confirm the owning account, inventory from the portal, consolidate keys into one secret store, least-privilege ASC keys per pipeline, token-key push, build-config to APNs map, rotation calendar and revocation runbook, hand off before any binding action | ~1850 |
| `content/05-examples.xml` | recommended | Complete signing document for a client app on fastlane match with token-key push and a 35-day rotation lead, a note per non-obvious value, and a bad document with the validator output | ~2600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/output.md.j2` | Playbook-step skeleton matching the schema in 02-output-contract.xml |
| `templates/output.md` | Playbook-step skeleton matching the schema in 02-output-contract.xml Generated from `templates/output.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in canonical example for calibration |
| `templates/_smoke-test.md` | Filled-in canonical example for calibration Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ios-signing-and-provisioning.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[app-store-and-play-store-release]]
- [[android-keystore-and-signing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
