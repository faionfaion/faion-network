# Google Ads Campaign Setup

## Summary

Structured process for creating Google Ads Search campaigns via the API: conversion tracking first, then campaign with PAUSED status, ad groups by theme, Responsive Search Ads (RSA), and extensions. Default network settings must explicitly disable Display and Search Partners — the API does not match the UI defaults. Never flip status to ENABLED without verified conversion tracking firing in the last 24 hours and at least one RSA per ad group.

## Why

Wrong campaign settings waste budget from day one. The API's network-settings default silently opts campaigns into Display Network and Search Partners, unlike the UI recommendation. Smart Bidding without seeded conversions spends ~14 days in learning burning budget. A spec-driven, PAUSED-first approach with a pre-launch gate prevents these failure modes and makes multi-account provisioning repeatable.

## When To Use

- Templating new Google Ads accounts: agent provisions a Search campaign with conversion tracking, RSAs, extensions, and naming convention enforced
- Onboarding agency or multi-tenant clients where the same campaign skeleton repeats across many accounts
- Pre-launch QA: agent walks the launch checklist and refuses to enable until every item passes
- Migrating manual campaigns to Smart Bidding by templating fresh campaigns with historical conversions

## When NOT To Use

- One-off campaigns launched in the UI in under 20 minutes — API setup overhead does not pay back
- Campaigns using UI-only features (some recommendations, brand-suitability tweaks, certain PMax settings)
- Heavily creative-led campaigns where asset variation is the primary work
- Already-running accounts with established Smart Bidding — re-templating restarts learning

## Content

| File | What's inside |
|------|---------------|
| `content/01-setup-steps.xml` | Campaign type selection, settings, naming convention, ad group structure, RSA guidelines |
| `content/02-checklist.xml` | Pre-launch, campaign setup, ad creation, and launch checklist steps |
| `content/03-agent-rules.xml` | API gotchas: network defaults, budget micros, location targeting, PAUSED-first rule |

## Templates

| File | Purpose |
|------|---------|
| `templates/launch-gate.py` | Pre-flight checks before flipping campaign to ENABLED |
| `templates/campaign-checklist.md` | Human-readable launch checklist for Search campaigns |
| `templates/ad-copy.md` | RSA headline and description template (15 headlines, 4 descriptions) |
