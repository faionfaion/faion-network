# purpose: Template helper for API Authentication (jwt_auth.py).
# consumes: see content/02-output-contract.xml inputs for api-authentication
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-1000 tokens when loaded as context
"""
FastAPI JWT authentication with full claims validation.
Uses python-jose. Replace SECRET_KEY/PUBLIC_KEY with env var or Vault ref.
Never hardcode secrets in source code.
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

# Configuration — load from environment, not hardcoded
ALGORITHM = "HS256"           # Use RS256/EdDSA for distributed verifiers
ALLOWED_ALGORITHMS = ["HS256"]
SECRET_KEY = "REPLACE_WITH_ENV_VAR"   # os.environ["JWT_SECRET_KEY"]
AUDIENCE = "https://api.example.com"
ISSUER = "https://auth.example.com"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

bearer_scheme = HTTPBearer()


def create_access_token(subject: str, scope: str = "", extra: Optional[dict] = None) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": subject,
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "scope": scope,
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    """FastAPI dependency: validates Bearer token and returns payload."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=ALLOWED_ALGORITHMS,  # explicit allowlist — never accept alg:none
            audience=AUDIENCE,
            issuer=ISSUER,
        )
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


def require_scope(required_scope: str):
    """Dependency factory: fails 403 if token lacks the required scope."""
    def checker(payload: dict = Depends(verify_token)) -> dict:
        scopes = payload.get("scope", "").split()
        if required_scope not in scopes and "admin" not in scopes:
            raise HTTPException(status_code=403, detail=f"Scope '{required_scope}' required")
        return payload
    return checker


# Usage:
# @app.get("/users")
# async def list_users(payload: dict = Depends(require_scope("read:users"))):
#     ...
