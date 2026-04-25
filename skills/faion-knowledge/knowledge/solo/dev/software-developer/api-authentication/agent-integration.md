# Agent Integration — API Authentication

## When to use
- Adding auth to a new service: pick API keys (S2S), JWT (user sessions), OAuth (3rd-party), or mTLS (high-trust) by traffic shape.
- Migrating from session cookies to JWT/OIDC because clients now include mobile + SPA + partner.
- Implementing key rotation, scope tightening, or a per-tenant key model.
- Hardening: short access TTL + refresh tokens + token-binding + revocation list.
- Federating identity through an IdP (Auth0, Keycloak, Cognito, Clerk, WorkOS).

## When NOT to use
- Reinventing OAuth/OIDC by hand — use a library or IdP. Custom auth is the #1 source of CVEs.
- Long-lived JWTs (>1h access tokens) "to avoid refresh complexity" — revocation becomes impossible.
- API keys for end-user auth — you'll end up shipping them to the browser; that's not auth, that's a public secret.
- mTLS for public consumer apps — cert distribution and rotation kill UX; reserve for B2B / agent-to-agent.

## Where it fails / limitations
- JWT revocation is hard: stateless tokens can't be invalidated mid-life. Need a denylist (Redis with TTL = remaining JWT lifetime) or short TTL + refresh.
- Symmetric secrets (HS256) shared across services let any service mint admin tokens; use asymmetric (RS256/EdDSA) with public-key distribution.
- Storing JWTs in `localStorage` exposes them to XSS; in cookies, exposes to CSRF unless `SameSite=Strict|Lax` + double-submit token.
- API keys checked with `==` are vulnerable to timing attacks; use `hmac.compare_digest`.
- "Bearer" tokens replayed from logs/proxies are accepted blindly; lacking audience/issuer/binding, anyone with the token is the user.
- OAuth implicit flow + password grant are deprecated; agents pull old StackOverflow examples that still use them.

## Agentic workflow
Decision tree first: agent reads the use-case (S2S, user, 3rd-party, IoT) and picks the method per the table in `README.md`. Schema-first JWT: claims defined in a typed dataclass / pydantic model with `iss/aud/exp/iat/jti/sub` mandatory. Reviewer agent runs `bandit`, checks for `algorithm: HS256` shared secrets, hardcoded keys, missing `verify=True`, missing `audience` parameter. For OAuth/OIDC, force the agent to use a real library (`authlib`, `oauthlib`, `node-openid-client`) and never hand-roll the redirect dance.

### Recommended subagents
- `password-scrubber-agent` — scan diff for committed secrets / private keys before push.
- `security-review` (slash skill) — first-pass security audit of the auth diff.
- `faion-sdd-executor-agent` — drives spec → flow → middleware → tests for each auth method.

### Prompt pattern
```
Implement <auth method> for endpoint group <group>.
Constraints:
- JWT: RS256 or EdDSA, exp <= 15min, refresh token rotation with reuse detection.
- API key: SHA-256 hash at rest, prefix sk_live_, hmac.compare_digest comparison.
- OAuth: use authlib/oauthlib, PKCE for public clients, never implicit/password grants.
- All secrets via env or 1Password (never literals). Provide a denylist hook.
- Tests: 401 on missing/invalid/expired/wrong-audience/wrong-issuer/revoked.
Output: middleware + verifier + 6 unit tests + a 5-line README on rotation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| jwt-cli | Inspect / sign / verify JWTs | `cargo install jwt-cli` |
| oidc-client / openid-client | OIDC flows | npm |
| authlib (Python) | OAuth 2.0 + OIDC client/server | `pip install authlib` |
| python-jose / pyjwt | JWT encode/decode | pip |
| openssl | Generate keys (`genpkey`, `req`, `x509` for mTLS) | system |
| step-cli (Smallstep) | PKI for mTLS, ACME, JWK | `brew install step` |
| 1Password CLI (`op`) | Fetch secrets at runtime/CI | 1password.com/downloads/command-line |
| sops + age | Encrypted secrets in git | mozilla/sops |
| jose (panva) | JOSE primitives in Node | `npm i jose` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Auth0 / Okta CIC | SaaS | Yes — Management API | Mature OIDC, expensive at scale. |
| Clerk | SaaS | Yes — REST + Backend SDKs | Best DX for SaaS auth (orgs, MFA, sessions). |
| WorkOS | SaaS | Yes — REST | SSO/SCIM for B2B. |
| Cognito | SaaS | Yes — IaC | AWS-native; quirks but cheap at scale. |
| Supabase Auth | OSS + SaaS | Yes — REST | Postgres + JWT; good for Supabase stacks. |
| Keycloak / Authentik / Zitadel | OSS | Yes — REST + admin CLI | Self-host IdP; Zitadel has the cleanest API. |
| Logto | OSS + SaaS | Yes — Management API | Modern Auth0 alt. |
| Vault (HashiCorp) | OSS / SaaS | Yes — CLI + API | For dynamic credentials, mTLS PKI, key rotation. |
| Cloudflare Access / Tailscale | SaaS | Yes | Zero-trust / mTLS-style entry without app changes. |

## Templates & scripts
See `templates.md` and `examples.md` for FastAPI verifier, JWT issuer, OAuth callback. Constant-time API-key check:

```python
# scripts/api_key_check.py
import hmac, hashlib
from typing import Optional

def hash_key(plaintext: str) -> str:
    return hashlib.sha256(plaintext.encode()).hexdigest()

def verify_api_key(presented: str, stored_hash: str) -> bool:
    presented_hash = hash_key(presented)
    return hmac.compare_digest(presented_hash, stored_hash)
```

## Best practices
- Use asymmetric JWTs (RS256/EdDSA); publish public keys via JWKS endpoint; rotate signing keys with `kid` header.
- Access token TTL ≤15 min; refresh token rotation with reuse detection (single-use refresh, deny on replay).
- Always verify `iss`, `aud`, `exp`, `nbf` (clock-skew tolerance ≤60s); reject tokens missing any.
- Hash API keys at rest; show full key only once at creation; store only prefix (`sk_live_xxxx`) for UI display.
- Scopes / roles in JWT, but enforce per-route via a policy layer (Casbin, Cerbos, Oso) — not scattered `if user.role`.
- Rate-limit auth endpoints aggressively (`5 req/min/IP` on login, `20 req/min/user` on refresh) to limit brute-force.
- Log every auth decision with `decision`, `reason`, `user_id`, `ip`, `user_agent`; fail closed on logging failure for high-risk endpoints.
- For SPAs: tokens in HTTP-only `SameSite=Lax` cookies + CSRF token; never `localStorage`.

## AI-agent gotchas
- Agents reach for `algorithm: HS256` with a hardcoded `SECRET_KEY = "your-secret-key"` from the README. Force the prompt to require RS256 + key from env/Vault.
- `jwt.decode(token)` without `algorithms=[...]` accepts `alg: none` — historical CVE class. Force explicit algorithms list.
- Agents forget `audience=` argument; tokens issued by another service in the same trust boundary become valid here.
- Refresh-token implementations frequently lack rotation + reuse detection; an attacker who steals one refresh token gets indefinite access.
- OAuth callbacks generated by LLMs often skip `state` / PKCE verification — vulnerable to CSRF and code-interception.
- Agents store API keys in plaintext "for now"; "for now" ships to prod. Force hashing on insert with a DB-level `BEFORE INSERT` trigger or app-level wrapper.
- LLMs `==` compare keys/tokens (timing attack). Replace with `hmac.compare_digest` and lint for `==` on auth values.
- Human-in-loop checkpoint: any change to issuer, audience, signing key, or token TTL must require human approval. Tokens already in flight at the time of change must be considered.

## References
- OWASP JWT Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
- OAuth 2.0 Security Best Current Practice (RFC 9700) — https://datatracker.ietf.org/doc/html/rfc9700
- OAuth 2.1 draft — https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1
- OIDC Core 1.0 — https://openid.net/specs/openid-connect-core-1_0.html
- PKCE (RFC 7636) — https://datatracker.ietf.org/doc/html/rfc7636
- Hashicorp Vault PKI — https://developer.hashicorp.com/vault/docs/secrets/pki
- jose (RFC 7515-7519) — https://datatracker.ietf.org/wg/jose/about/
