# API Authentication Templates

Ready-to-use code templates for implementing API authentication.

## API Key Authentication

### FastAPI Implementation

```python
# api_key_auth.py
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional
import hashlib
import secrets
from datetime import datetime, timedelta
from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True)
    key_hash = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    prefix = Column(String, nullable=False)  # e.g., "sk_live_"
    user_id = Column(String, nullable=False)
    scopes = Column(String)  # JSON array of scopes
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime)
    revoked = Column(Boolean, default=False)
    rate_limit = Column(Integer, default=1000)  # requests per hour

class APIKeyManager:
    @staticmethod
    def generate_key(prefix: str = "sk_live_") -> tuple[str, str]:
        """Generate API key and return (full_key, hash)"""
        random_part = secrets.token_urlsafe(32)
        full_key = f"{prefix}{random_part}"
        key_hash = hashlib.sha256(full_key.encode()).hexdigest()
        return full_key, key_hash

    @staticmethod
    def hash_key(key: str) -> str:
        """Hash an API key for storage"""
        return hashlib.sha256(key.encode()).hexdigest()

    async def create_key(
        self,
        db,
        user_id: str,
        name: str,
        scopes: list[str],
        prefix: str = "sk_live_"
    ) -> tuple[str, APIKey]:
        """Create new API key"""
        full_key, key_hash = self.generate_key(prefix)

        api_key = APIKey(
            id=secrets.token_urlsafe(16),
            key_hash=key_hash,
            name=name,
            prefix=prefix,
            user_id=user_id,
            scopes=",".join(scopes),
            created_at=datetime.utcnow()
        )

        db.add(api_key)
        await db.commit()

        # Return full key only once
        return full_key, api_key

    async def verify_key(self, db, key: str) -> Optional[APIKey]:
        """Verify API key and return key object"""
        key_hash = self.hash_key(key)

        api_key = await db.query(APIKey).filter(
            APIKey.key_hash == key_hash,
            APIKey.revoked == False
        ).first()

        if api_key:
            # Update last used timestamp
            api_key.last_used_at = datetime.utcnow()
            await db.commit()

        return api_key

# Dependency
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(
    api_key: str = Security(api_key_header),
    db = Depends(get_db)
) -> APIKey:
    """FastAPI dependency for API key authentication"""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required"
        )

    key_manager = APIKeyManager()
    key_obj = await key_manager.verify_key(db, api_key)

    if not key_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    return key_obj

# Usage in routes
@app.get("/protected")
async def protected_route(api_key: APIKey = Depends(verify_api_key)):
    return {"user_id": api_key.user_id, "scopes": api_key.scopes}
```

## JWT Authentication

### FastAPI JWT Implementation

```python
# jwt_auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: str
    scopes: list[str] = []
    token_type: str = "access"

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

def create_access_token(
    user_id: str,
    scopes: list[str] = [],
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": user_id,
        "scope": " ".join(scopes),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: str) -> str:
    """Create JWT refresh token"""
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_token_pair(user_id: str, scopes: list[str] = []) -> TokenPair:
    """Create access and refresh token pair"""
    access_token = create_access_token(user_id, scopes)
    refresh_token = create_refresh_token(user_id)

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """Verify JWT token and return token data"""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        scopes = payload.get("scope", "").split()
        token_type = payload.get("type", "access")

        return TokenData(
            user_id=user_id,
            scopes=scopes,
            token_type=token_type
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def require_scope(required_scope: str):
    """Dependency to check for required scope"""
    async def scope_checker(token_data: TokenData = Depends(verify_token)):
        if required_scope not in token_data.scopes and "admin" not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Scope '{required_scope}' required"
            )
        return token_data
    return scope_checker

# Usage
@app.post("/login")
async def login(email: str, password: str):
    # Verify credentials (not shown)
    user = authenticate_user(email, password)

    tokens = create_token_pair(
        user_id=user.id,
        scopes=["read:profile", "write:profile"]
    )

    return tokens

@app.post("/refresh")
async def refresh(token_data: TokenData = Depends(verify_token)):
    if token_data.token_type != "refresh":
        raise HTTPException(400, "Invalid token type")

    # Issue new tokens
    return create_token_pair(token_data.user_id)

@app.get("/protected")
async def protected(token_data: TokenData = Depends(verify_token)):
    return {"user_id": token_data.user_id}

@app.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: str,
    _: TokenData = Depends(require_scope("admin"))
):
    # Delete user logic
    pass
```

## OAuth 2.0 Server

### Authorization Code Flow

```python
# oauth_server.py
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import secrets
from urllib.parse import urlencode
from datetime import datetime, timedelta

class OAuthClient(BaseModel):
    client_id: str
    client_secret: str
    redirect_uris: list[str]
    allowed_grant_types: list[str]
    allowed_scopes: list[str]

class AuthorizationCode(BaseModel):
    code: str
    client_id: str
    redirect_uri: str
    user_id: str
    scopes: list[str]
    code_challenge: Optional[str] = None
    expires_at: datetime

class OAuthServer:
    def __init__(self):
        self.clients: dict[str, OAuthClient] = {}
        self.auth_codes: dict[str, AuthorizationCode] = {}

    def register_client(
        self,
        redirect_uris: list[str],
        allowed_grant_types: list[str],
        allowed_scopes: list[str]
    ) -> tuple[str, str]:
        """Register OAuth client"""
        client_id = f"client_{secrets.token_urlsafe(16)}"
        client_secret = secrets.token_urlsafe(32)

        self.clients[client_id] = OAuthClient(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uris=redirect_uris,
            allowed_grant_types=allowed_grant_types,
            allowed_scopes=allowed_scopes
        )

        return client_id, client_secret

    async def authorize(
        self,
        client_id: str,
        redirect_uri: str,
        response_type: str,
        scope: str,
        state: str,
        code_challenge: Optional[str] = None
    ) -> str:
        """Handle authorization request"""
        # Validate client
        client = self.clients.get(client_id)
        if not client:
            raise HTTPException(400, "Invalid client_id")

        # Validate redirect_uri
        if redirect_uri not in client.redirect_uris:
            raise HTTPException(400, "Invalid redirect_uri")

        # Validate scopes
        requested_scopes = scope.split()
        if not all(s in client.allowed_scopes for s in requested_scopes):
            raise HTTPException(400, "Invalid scope")

        # User authentication happens here (not shown)
        # Assume user is authenticated and authorized
        user_id = "user_123"

        # Generate authorization code
        code = secrets.token_urlsafe(32)
        self.auth_codes[code] = AuthorizationCode(
            code=code,
            client_id=client_id,
            redirect_uri=redirect_uri,
            user_id=user_id,
            scopes=requested_scopes,
            code_challenge=code_challenge,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )

        # Redirect with code
        params = {"code": code, "state": state}
        return f"{redirect_uri}?{urlencode(params)}"

    async def token(
        self,
        grant_type: str,
        code: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        code_verifier: Optional[str] = None
    ) -> dict:
        """Handle token request"""
        if grant_type == "authorization_code":
            # Validate authorization code
            auth_code = self.auth_codes.get(code)
            if not auth_code:
                raise HTTPException(400, "Invalid code")

            if auth_code.expires_at < datetime.utcnow():
                raise HTTPException(400, "Code expired")

            # Validate client
            client = self.clients.get(client_id)
            if not client or client.client_secret != client_secret:
                raise HTTPException(401, "Invalid client credentials")

            # Validate PKCE if present
            if auth_code.code_challenge:
                if not code_verifier:
                    raise HTTPException(400, "code_verifier required")
                # Verify code_challenge matches code_verifier (not shown)

            # Delete used code
            del self.auth_codes[code]

            # Issue tokens
            access_token = create_access_token(
                auth_code.user_id,
                auth_code.scopes
            )
            refresh_token = create_refresh_token(auth_code.user_id)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": 3600,
                "scope": " ".join(auth_code.scopes)
            }

        elif grant_type == "client_credentials":
            # Validate client
            client = self.clients.get(client_id)
            if not client or client.client_secret != client_secret:
                raise HTTPException(401, "Invalid client credentials")

            # Issue token (no user context)
            access_token = create_access_token(
                client_id,
                client.allowed_scopes
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": 3600
            }

        raise HTTPException(400, "Unsupported grant_type")

# FastAPI routes
oauth_server = OAuthServer()

@app.get("/oauth/authorize")
async def authorize_endpoint(
    client_id: str,
    redirect_uri: str,
    response_type: str,
    scope: str,
    state: str,
    code_challenge: Optional[str] = None
):
    redirect_url = await oauth_server.authorize(
        client_id, redirect_uri, response_type,
        scope, state, code_challenge
    )
    return RedirectResponse(redirect_url)

@app.post("/oauth/token")
async def token_endpoint(
    grant_type: str,
    code: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    code_verifier: Optional[str] = None
):
    return await oauth_server.token(
        grant_type, code, redirect_uri,
        client_id, client_secret, code_verifier
    )
```

## Client-Side Templates

### JavaScript/TypeScript Client

```typescript
// auth-client.ts
interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  token_type: string;
  expires_in: number;
}

class AuthClient {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
    this.loadTokens();
  }

  private loadTokens(): void {
    this.accessToken = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
  }

  private saveTokens(tokens: TokenResponse): void {
    this.accessToken = tokens.access_token;
    if (tokens.refresh_token) {
      this.refreshToken = tokens.refresh_token;
    }

    localStorage.setItem('access_token', tokens.access_token);
    if (tokens.refresh_token) {
      localStorage.setItem('refresh_token', tokens.refresh_token);
    }
  }

  async login(email: string, password: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const tokens: TokenResponse = await response.json();
    this.saveTokens(tokens);
  }

  async refresh(): Promise<void> {
    if (!this.refreshToken) {
      throw new Error('No refresh token');
    }

    const response = await fetch(`${this.baseUrl}/refresh`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.refreshToken}`
      }
    });

    if (!response.ok) {
      this.logout();
      throw new Error('Refresh failed');
    }

    const tokens: TokenResponse = await response.json();
    this.saveTokens(tokens);
  }

  async fetch(url: string, options: RequestInit = {}): Promise<Response> {
    if (!this.accessToken) {
      throw new Error('Not authenticated');
    }

    const headers = new Headers(options.headers);
    headers.set('Authorization', `Bearer ${this.accessToken}`);

    let response = await fetch(url, { ...options, headers });

    // Auto-refresh on 401
    if (response.status === 401 && this.refreshToken) {
      await this.refresh();
      headers.set('Authorization', `Bearer ${this.accessToken}`);
      response = await fetch(url, { ...options, headers });
    }

    return response;
  }

  logout(): void {
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  isAuthenticated(): boolean {
    return this.accessToken !== null;
  }
}

// Usage
const auth = new AuthClient('https://api.example.com');

await auth.login('user@example.com', 'password');
const response = await auth.fetch('/api/users/me');
const user = await response.json();
```

---

*API Authentication Templates v1.0*
