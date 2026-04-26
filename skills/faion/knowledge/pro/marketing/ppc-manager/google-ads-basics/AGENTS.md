# Google Ads API — Basics

## Summary

OAuth 2.0 authentication setup, account hierarchy (MCC → Customer → Campaign → Ad Group → Ad/Keyword), and Python client patterns for listing and updating campaigns. All credentials must be stored in environment variables or a secrets manager — never in version control.

## Why

Google Ads API uses a multi-layer auth model (developer token + OAuth refresh token + optional MCC login_customer_id) that is not obvious from the docs. Getting auth wrong blocks all API calls; getting the account hierarchy wrong produces data in the wrong place.

## When To Use

- Authenticating a Python app to the Google Ads API for the first time
- Setting up google-ads.yaml or dict-based credentials
- Querying the account hierarchy or listing campaigns with metrics
- Updating campaign status (ENABLED, PAUSED, REMOVED)

## When NOT To Use

- Search, Display, Shopping, or PMax campaign creation — use the campaign-type-specific methodologies
- Conversion tracking setup — use ads-conversion-tracking methodology
- Reporting and automation — use google-ads-reporting methodology

## Content

| File | What's inside |
|------|---------------|
| `content/01-authentication.xml` | Auth components, developer token levels, OAuth flow, security rules |
| `content/02-account-structure.xml` | Resource hierarchy, GAQL query patterns for customers and campaigns |

## Templates

| File | Purpose |
|------|---------|
| `templates/google-ads.yaml` | google-ads.yaml credential file template |
| `templates/client-setup.py` | GoogleAdsClient initialization patterns (YAML and dict) |
