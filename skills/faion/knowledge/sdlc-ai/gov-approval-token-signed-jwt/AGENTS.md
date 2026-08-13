# Approval Token as Signed JWT

## Summary

**One-sentence:** Approval tokens for AI-agent-initiated privileged actions are encoded as signed JWTs with audience, scope, expiry, and one-time nonce; verifier rejects unsigned, stale, or replayed tokens.

**One-paragraph:** AI agents that initiate privileged actions (deploy, secret rotation, schema migration) need cryptographic approval, not chat confirmations. This methodology encodes the approval token as a signed JWT: claims include subject (agent id), audience (target resource), scope (action verb + resource), expiry (≤15 min), and a one-time nonce stored server-side. Verifier rejects unsigned, expired, or replayed tokens. Output is the verifier configuration + issuer keypair + revocation list.

**Ефективно для:**

- AI agents can initiate actions with production blast radius (deploy, rotate-secret, migrate-db).
- Human approver is in-the-loop but synchronous chat-based approval has been abused or audited as insufficient.
- The platform has a signing key infrastructure (KMS / HSM / cloud KMS) — JWT signing must be in hardware-rooted trust.

## Applies If (ALL must hold)

- AI agents can initiate actions with production blast radius (deploy, rotate-secret, migrate-db).
- Human approver is in-the-loop but synchronous chat-based approval has been abused or audited as insufficient.
- The platform has a signing key infrastructure (KMS / HSM / cloud KMS) — JWT signing must be in hardware-rooted trust.

## Skip If (ANY kills it)

- Agents never touch privileged actions — read-only research only.
- Existing approval flow is already cryptographic (e.g. WebAuthn ceremony per action).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Signing keypair | kms | Cloud KMS / HSM |
| Audience / scope catalog | yaml | Repo at `approvals/scopes.yaml` |
| Revocation store | redis | Team-managed nonce store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-gov-approval-token-signed-jwt` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/approval-config.yaml` | Approval verifier config |
| `templates/verifier.py` | Reference JWT verifier implementation |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gov-approval-token-signed-jwt.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/approval-config.yaml`

```yaml
issuer_key_id: kms://arn:aws:kms:eu-west-1:123:key/abc
audience: prod-cluster-us-east-1
scope_pattern: "^[a-z]+:[a-z0-9-]+$"
exp_seconds_max: 900
nonce_store: redis://nonce.svc:6379/0
hsm_rooted: true
crl_url: https://approvals.internal/crl
```

### `templates/verifier.py`

```python
"""Minimal reference verifier; production uses pyjwt or jose."""
from __future__ import annotations
import json


def verify(token: str, public_jwk: dict, expected_aud: str, nonce_seen: set) -> tuple[bool, str]:
    """Return (allowed, reason). Production: replace with pyjwt."""
    header_b64, payload_b64, sig_b64 = token.split(".")
    payload = json.loads(_b64url_decode(payload_b64).decode())
    if payload.get("aud") != expected_aud:
        return False, "aud mismatch"
    if payload.get("scope", "").endswith(":*") or payload["scope"] == "*":
        return False, "wildcard scope"
    if payload.get("exp", 0) - payload.get("iat", 0) > 900:
        return False, "expiry too long"
    jti = payload.get("jti")
    if not jti or jti in nonce_seen:
        return False, "replay or missing jti"
    nonce_seen.add(jti)
    return True, "ok"


def _b64url_decode(s: str) -> bytes:
    import base64
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)
```
