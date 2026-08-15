<!--
purpose: Markdown skeleton enforcing the six-section structure
consumes: API surface inventory
produces: Docs site page tree
depends-on: content/01-core-rules.xml
token-budget-impact: ~250 tokens when loaded
variables:
  - name: api_name
    type: string
    required: true
    description: The API's public name as it appears in the docs nav and in support tickets. Match the SDK package name - a docs site that calls it something else costs every reader one search.
  - name: base_url
    type: string
    required: true
    description: Production base URL including the version segment. Copy-pasteable, because the Quick Start below is the first thing a new integrator runs and the first place they give up.
  - name: auth_scheme
    type: enum
    required: true
    options: [bearer-token, api-key-header, oauth2, basic]
    description: How a caller authenticates on day one. If you support several, document the day-one path here and the rest further down - a blurred first example doubles your support load.
  - name: token_howto
    type: text
    required: true
    description: Where a developer actually obtains a credential - the console page, the CLI command, the person to email. This is the step that silently blocks most first integrations.
  - name: free_rate_limit
    type: string
    required: true
    description: Requests per hour on the free tier, as a number. Limits described as "reasonable" get discovered by being hit in production, at someone else's peak hour.
  - name: support_contact
    type: string
    required: true
    description: Where a caller goes with a 500 and a traceId - the support address or issue tracker URL. A docs page that ends without one turns every server error into a public complaint.
-->
# {{api_name}}

## Overview

Brief description: what the API does and who it is for.

## Authentication

Scheme: `{{auth_scheme}}`

```
Authorization: Bearer <token>
```

How to obtain a token: {{token_howto}}

Rate limits: Free tier — {{free_rate_limit}} req/hour. Pro tier — [N] req/hour.
Headers returned: `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

## Quick Start

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  {{base_url}}/users
```

## Endpoints

### Users

| Method | Path | Description |
|--------|------|-------------|
| GET | /users | List users |
| POST | /users | Create user |
| GET | /users/{id} | Get user by ID |
| PATCH | /users/{id} | Update user fields |
| DELETE | /users/{id} | Delete user |

## Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| 400 | Bad Request | Check request body against schema |
| 401 | Unauthorized | Verify your API key |
| 403 | Forbidden | Check required permissions |
| 404 | Not Found | Verify resource ID |
| 409 | Conflict | Resource already exists |
| 429 | Rate Limited | Back off and retry after X-RateLimit-Reset |
| 500 | Server Error | Contact {{support_contact}} with the traceId |

## SDKs

- Python: `pip install example-api`
- JavaScript: `npm install @example/api-client`

## Changelog

### v1.1.0 (YYYY-MM-DD)

- Added user search endpoint
- Fixed pagination cursor bug

### v1.0.0 (YYYY-MM-DD)

- Initial release
