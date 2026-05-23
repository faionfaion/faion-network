<!-- purpose: PII handling decision matrix for ES events -->
<!-- consumes: event field list + privacy classification -->
<!-- produces: choice between crypto-shredding vs externalization -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200 tokens when loaded as reference -->

# GDPR PII policy for events

| Field kind | Allowed in payload? | Policy |
|------------|---------------------|--------|
| User identifier (UUID) | yes | none |
| Pseudonymous token (card_token_id, customer_handle) | yes | none |
| Direct PII (email, phone, full name, address) | no | crypto-shredding OR externalized side table |
| Sensitive PII (SSN, card number, biometrics) | no | externalized side table only |

## Crypto-shredding workflow

1. Per-subject AES-256 key stored in mutable keystore (`pii_keys`).
2. PII fields encrypted with that key inside events.
3. Erasure request → delete key from keystore → ciphertext becomes undecryptable.
4. Document the policy in the event-catalog entry under `pii_handling: crypto_shredding`.

## Externalized side table workflow

1. Event payload carries opaque ID only.
2. PII lives in mutable `pii_index` table indexed by the opaque ID.
3. Erasure request → DELETE the row.
4. Document the policy in the event-catalog entry under `pii_handling: externalized_side_table`.
