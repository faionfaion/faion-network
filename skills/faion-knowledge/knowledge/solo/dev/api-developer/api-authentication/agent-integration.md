# Agent Integration — API Authentication

## When to use
- Any API exposing user data, billing, or write operations across an authentication boundary.
- Server-to-server integrations: API keys (with rotation) or OAuth client credentials.
- Third-party access on behalf of users: OAuth 2.0 authorization code + PKCE.
- First-party SPA + mobile sessions: short-lived access JWT + rotating refresh token, ideally cookie-bound.
- Machine-to-machine in zero-trust networks: mTLS or signed JWTs with audience claims.
- Scoped delegation: OAuth scopes / fine-grained API key permissions instead of admin-or-nothing.

## When NOT to use
- Internal services on a private network where mTLS or service mesh identity already authenticates the caller — adding JWT layers is theatre.
- Public read-only endpoints (status, public data) — auth adds friction without security gain.
- One-off scripts that read a single resource — a per-script API key beats hand-rolled JWT.
- Embedding HS256 secrets into mobile / SPA bundles — they will leak. Use OAuth + PKCE or server proxy.

## Where it fails / limitations
- JWT revocation is hard; "stateless tokens" become stateful when you need a deny-list.
- Refresh token theft → silent persistent access. Rotation + reuse-detection is mandatory, not optional.
- API keys without prefix + hash storage are unrecoverable on breach. Treat them like passwords.
- OAuth implicit flow is deprecated; using it is a finding in any modern audit.
- Custom auth middleware is the highest-risk code in the repo: subtle bugs (e.g. accepting `alg:none`) bypass everything.
- Scope-creep: too many scopes → users approve all; too few → admin-or-nothing.
- Clock skew breaks JWT exp / iat. Allow 30–60s leeway, sync with NTP.
- mTLS clients are painful to rotate at scale; certificate management is a separate problem.

## Agentic workflow
Auth is the bug class with the highest blast radius — keep agents far from key material and treat every change to auth code as security-review-required. Agents may scaffold endpoints, draft permission decorators, write tests, audit dependencies. Agents must NOT change algorithms, generate secrets in repo, or modify token issuance without a human gate. Use a dedicated quality gate that fails CI on any diff touching `auth/` without an attached test for revocation, expiry, and the negative case.

### Recommended subagents
- `security-review` (built-in) — run on every PR touching `auth/`, `oauth/`, or middleware.
- `faion-sdd-execution` — gate that requires negative tests (expired token, missing scope, wrong audience) on every auth change.
- An `oauth-flow-implementer` agent (Sonnet) — wires authorization code + PKCE end-to-end with library defaults, no custom crypto.
- A `secrets-scanner` task — runs gitleaks/trufflehog on the diff before commit.

### Prompt pattern
```
Implement Authorization Code + PKCE for the dashboard SPA against
auth.example.com. Use authlib in the backend; do NOT roll your own state
or code_verifier. Cookie-bind the access token (HttpOnly, Secure,
SameSite=Lax). Add tests:
  - happy path
  - state mismatch → reject
  - expired authorization code → reject
  - PKCE verifier mismatch → reject
Output: unified diff + checklist of OWASP ASVS items covered.
```

```
Audit auth/middleware.py for these flaws:
  - alg:none accepted
  - missing aud / iss check
  - no exp / nbf validation
  - secrets read from .env at import time (vs per-request)
  - revocation list check missing
Report only — do not patch.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jwt` (mike-engel) | Decode/encode/sign JWTs in shell | `brew install mike-engel/jwt-cli/jwt-cli` |
| `step` | PKI + JWT + OAuth + mTLS swiss-army | `brew install step` · smallstep.com |
| `oauth2c` | OAuth 2.0 flows from CLI (auth code, PKCE, etc.) | `brew install oauth2c` |
| `mkcert` | Local TLS certs for mTLS dev | `brew install mkcert` |
| `gitleaks` / `trufflehog` | Secret scanning in repo + git history | OSS |
| `httpie` + `--auth-type=bearer` | Hand-test API auth | `pip install httpie` |
| `oathtool` | TOTP for MFA testing | apt/brew |
| `nuclei -t http/misconfiguration/jwt-*` | OAuth/JWT misconfig scans | nuclei templates |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Auth0 | SaaS | Yes — Management API + terraform-provider-auth0 | Mature, expensive at scale |
| Clerk | SaaS | Yes — REST API + Backend SDK | Best DX for SPA + mobile |
| WorkOS | SaaS | Yes — REST API | Enterprise SSO/SCIM as a service |
| Stytch | SaaS | Yes — REST API | Passwordless, B2B SSO |
| Keycloak | OSS | Yes — admin REST API + kcadm.sh | Self-host, OIDC + SAML, heavy to operate |
| Authentik | OSS | Yes — REST API | Lighter Keycloak alternative |
| Ory (Kratos + Hydra + Keto) | OSS | Yes — config-as-code | Composable identity stack |
| Supabase Auth | OSS + SaaS | Yes — REST + JS SDK | Postgres-native |
| AWS Cognito | SaaS | Yes — IaC | Cheap, sharp edges around password policy |
| HashiCorp Vault | OSS + SaaS | Yes — `vault` CLI + REST | Secrets + dynamic credentials, not user auth |
| 1Password Secrets / OP CLI | SaaS | Yes — `op` CLI | Already in NERO toolchain for service creds |

## Templates & scripts
See `templates.md` and `examples.md` for FastAPI + JWT, OAuth code-flow, scope guards.

JWT misconfig smoke test:

```bash
#!/usr/bin/env bash
# Fail if API accepts alg:none or wrong-aud tokens.
set -euo pipefail
HOST=${1:?usage: $0 https://api.example.com}
NONE=$(jwt encode --alg none '{"sub":"x","exp":9999999999}' '')
WRONG_AUD=$(jwt encode --alg HS256 --secret "$JWT_SECRET" \
  '{"sub":"x","aud":"other","exp":9999999999}')
for tok in "$NONE" "$WRONG_AUD"; do
  code=$(curl -s -o /dev/null -w '%{http_code}' \
    "$HOST/api/users/me" -H "Authorization: Bearer $tok")
  [ "$code" = "401" ] || { echo "FAIL: token accepted ($code)"; exit 1; }
done
echo "OK: bad tokens rejected"
```

## Best practices
- Never roll your own crypto, JWT validation, or OAuth state machine. Use `authlib`, `jose`, `passport`, `nextauth`, `authjs`, vendor SDK.
- Access tokens 5–15 min. Refresh tokens rotated on every use, with reuse-detection (re-used refresh = invalidate family + force re-auth).
- Cookie-bind tokens for browsers: `HttpOnly; Secure; SameSite=Lax|Strict`. Bearer tokens in localStorage are XSS-fatal.
- API keys: store hashed (argon2/scrypt/HMAC-SHA-256), prefix to identify (`sk_live_`), display only at creation.
- Rotate secrets/keys on a schedule, not after a breach. Two-active-key window for zero-downtime rotation.
- Validate `iss`, `aud`, `exp`, `nbf`, `kid`. Reject `alg:none` and unknown `alg`. Pin allowed algorithms.
- Use asymmetric (RS256/EdDSA) when verifiers are distributed; HS256 only when issuer == verifier.
- Scopes: name by capability + resource (`read:users`, `write:billing`); never `admin` as a scope you grant casually.
- Log every authentication event with request_id, IP, user-agent. Alert on credential-stuffing patterns.
- Rate-limit `/login` and `/oauth/token` per IP + per account. Lockout with backoff, not permanent.

## AI-agent gotchas
- Agents will happily generate "demo" JWT secrets and commit them. Run secret scanning on every diff and reject.
- LLMs frequently write JWT validators that omit `aud`/`iss` checks ("the test passed!"). SDD gate must require those assertions in tests.
- Refresh-token rotation looks fine in unit tests and breaks under concurrent requests (last-write-wins). Force a per-family lock + reuse-detection test.
- An agent shown two flows will pick the simpler — implicit grant or password grant. Both are deprecated. Constrain prompts to "code flow + PKCE only".
- Generated middleware often catches `JWTError` and returns 200 with a default user (silent bypass). Lint for "auth error returns non-401".
- API key hashing is often skipped in MVPs. The migration to hashed storage later is painful — make it the SDD acceptance criterion from day 1.
- Agents debugging "401 in prod" will reach for `alg:none` or wider `aud` matches. Lock auth config behind a separate review path.
- Mobile/SPA agents may store refresh tokens in `localStorage`. The right answer is HttpOnly cookie + same-site + CSRF token. Document this in the project AGENTS.md so the agent picks the right pattern by default.
- When using a vendor (Auth0/Clerk), do not let agents hand-roll parallel auth for "just this one endpoint" — that is the bug class. Force every endpoint through the vendor middleware.

## References
- https://datatracker.ietf.org/doc/html/rfc6749 (OAuth 2.0)
- https://datatracker.ietf.org/doc/html/rfc7636 (PKCE)
- https://datatracker.ietf.org/doc/html/rfc9700 (OAuth 2.0 Security BCP)
- https://datatracker.ietf.org/doc/html/rfc7519 (JWT)
- https://owasp.org/www-project-api-security/ (API Security Top 10)
- https://owasp.org/www-project-application-security-verification-standard/
- https://datatracker.ietf.org/doc/html/rfc8725 (JWT BCP)
- https://oauth.net/2/pkce/
