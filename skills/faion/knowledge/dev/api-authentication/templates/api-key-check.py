# purpose: Stdlib API-key validator with rotation overlap window
# consumes: Header key + key store
# produces: Boolean valid/invalid + rotation flag
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~250 tokens when loaded
# Constant-time SHA-256 API key verification
# Usage: from templates.api_key_check import hash_key, verify_api_key

import hashlib
import hmac


def hash_key(plaintext: str) -> str:
    """Return SHA-256 hex digest of key for storage."""
    return hashlib.sha256(plaintext.encode()).hexdigest()


def verify_api_key(presented: str, stored_hash: str) -> bool:
    """Constant-time comparison to prevent timing attacks."""
    return hmac.compare_digest(hash_key(presented), stored_hash)
