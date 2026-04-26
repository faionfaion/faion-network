# FastAPI JWT verifier using RS256 public key
# Usage: from templates.fastapi_jwt_verifier import verify_jwt_token
# Requires: python-jose[cryptography], fastapi

import os
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

ALGORITHM = "RS256"
PUBLIC_KEY = os.environ["JWT_PUBLIC_KEY"]   # PEM-encoded RSA public key
AUDIENCE = os.environ["JWT_AUDIENCE"]        # e.g. "https://api.example.com"
ISSUER = os.environ["JWT_ISSUER"]            # e.g. "https://auth.example.com"

_bearer = HTTPBearer()


def verify_jwt_token(
    credentials: HTTPAuthorizationCredentials = Security(_bearer),
) -> dict:
    """Verify RS256 JWT; return decoded payload or raise 401."""
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
        )
    except JWTError as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc
    return payload
