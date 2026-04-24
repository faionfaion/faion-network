# API Authentication Examples

Real-world examples of API authentication implementations.

## Example 1: Stripe-Style API Keys

**Scenario:** SaaS payment API with hierarchical API keys.

```python
# models.py
from enum import Enum

class KeyType(str, Enum):
    LIVE = "live"
    TEST = "test"

class APIKeyPrefix:
    LIVE_SECRET = "sk_live_"
    TEST_SECRET = "sk_test_"
    LIVE_PUBLISHABLE = "pk_live_"
    TEST_PUBLISHABLE = "pk_test_"

# service.py
class APIKeyService:
    async def create_key_pair(self, account_id: str, env: KeyType):
        """Create secret + publishable key pair"""
        if env == KeyType.LIVE:
            secret_prefix = APIKeyPrefix.LIVE_SECRET
            public_prefix = APIKeyPrefix.LIVE_PUBLISHABLE
        else:
            secret_prefix = APIKeyPrefix.TEST_SECRET
            public_prefix = APIKeyPrefix.TEST_PUBLISHABLE

        # Secret key (server-side only)
        secret_key, secret_hash = APIKeyManager.generate_key(secret_prefix)

        # Publishable key (client-side safe)
        public_key, public_hash = APIKeyManager.generate_key(public_prefix)

        # Store both
        await self.db.execute("""
            INSERT INTO api_keys (account_id, key_hash, prefix, type, env)
            VALUES ($1, $2, $3, $4, $5), ($1, $6, $7, $8, $9)
        """, account_id, secret_hash, secret_prefix, "secret", env,
             account_id, public_hash, public_prefix, "publishable", env)

        return {
            "secret_key": secret_key,  # Show once, never again
            "publishable_key": public_key
        }

# Usage
keys = await api_key_service.create_key_pair("acct_123", KeyType.LIVE)
print(keys["secret_key"])  # sk_live_abc123...
print(keys["publishable_key"])  # pk_live_xyz789...
```

## Example 2: GitHub-Style Personal Access Tokens

**Scenario:** Developer platform with scoped tokens.

```python
# scopes.py
SCOPES = {
    "repo": "Full control of private repositories",
    "repo:status": "Access commit status",
    "public_repo": "Access public repositories",
    "user": "Update user data",
    "user:email": "Access user email addresses (read-only)",
    "admin:org": "Full control of orgs and teams",
    "write:org": "Read and write org data"
}

# token_service.py
class PersonalAccessTokenService:
    async def create_token(
        self,
        user_id: str,
        name: str,
        scopes: list[str],
        expires_in_days: int = 90
    ):
        """Create scoped personal access token"""
        # Validate scopes
        invalid_scopes = [s for s in scopes if s not in SCOPES]
        if invalid_scopes:
            raise ValueError(f"Invalid scopes: {invalid_scopes}")

        # Generate token
        token = f"ghp_{secrets.token_urlsafe(32)}"
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        # Store with expiration
        await self.db.execute("""
            INSERT INTO personal_access_tokens
            (user_id, token_hash, name, scopes, expires_at)
            VALUES ($1, $2, $3, $4, NOW() + INTERVAL '{days} days')
        """, user_id, token_hash, name, scopes, days=expires_in_days)

        return {
            "token": token,  # Show once
            "name": name,
            "scopes": scopes,
            "expires_at": datetime.utcnow() + timedelta(days=expires_in_days)
        }

# Validation
async def verify_pat(token: str, required_scope: str) -> User:
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    pat = await db.fetchrow("""
        SELECT user_id, scopes, expires_at
        FROM personal_access_tokens
        WHERE token_hash = $1 AND revoked = false
    """, token_hash)

    if not pat or pat["expires_at"] < datetime.utcnow():
        raise HTTPException(401, "Invalid or expired token")

    # Check scope hierarchy
    if not has_scope(pat["scopes"], required_scope):
        raise HTTPException(403, f"Scope '{required_scope}' required")

    return await get_user(pat["user_id"])
```

## Example 3: Multi-Tenant SaaS with JWT

**Scenario:** Multi-tenant B2B SaaS with organization context.

```python
# models.py
class User(BaseModel):
    id: str
    email: str
    default_org_id: str

class Organization(BaseModel):
    id: str
    name: str
    tier: str  # free, pro, enterprise

class TokenClaims(BaseModel):
    sub: str  # user_id
    org_id: str
    org_tier: str
    roles: list[str]
    permissions: list[str]

# token_service.py
class MultiTenantTokenService:
    async def create_token(
        self,
        user: User,
        org_id: str
    ) -> str:
        """Create JWT with organization context"""
        # Verify user belongs to org
        membership = await self.db.fetchrow("""
            SELECT role, permissions
            FROM org_memberships
            WHERE user_id = $1 AND org_id = $2
        """, user.id, org_id)

        if not membership:
            raise ValueError("User not member of organization")

        # Get organization details
        org = await self.get_organization(org_id)

        # Build claims
        claims = {
            "sub": user.id,
            "email": user.email,
            "org_id": org.id,
            "org_tier": org.tier,
            "role": membership["role"],
            "permissions": membership["permissions"],
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow()
        }

        return jwt.encode(claims, SECRET_KEY, algorithm="HS256")

# Middleware
@app.middleware("http")
async def organization_context(request: Request, call_next):
    """Inject organization context from token"""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")

    if token:
        try:
            claims = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.state.user_id = claims["sub"]
            request.state.org_id = claims["org_id"]
            request.state.org_tier = claims["org_tier"]
            request.state.permissions = claims["permissions"]
        except JWTError:
            pass

    return await call_next(request)

# Permission check
def require_permission(permission: str):
    async def checker(request: Request):
        if not hasattr(request.state, "permissions"):
            raise HTTPException(401, "Authentication required")

        if permission not in request.state.permissions:
            raise HTTPException(403, f"Permission '{permission}' required")

        return request.state
    return Depends(checker)

# Usage
@app.post("/orgs/{org_id}/projects")
async def create_project(
    org_id: str,
    state = Depends(require_permission("projects:create"))
):
    # Verify org_id matches token
    if org_id != state.org_id:
        raise HTTPException(403, "Access denied")

    # Create project for organization
    pass
```

## Example 4: OAuth 2.0 with PKCE (Mobile App)

**Scenario:** Mobile app using OAuth 2.0 with PKCE extension.

```typescript
// mobile-oauth-client.ts
import * as Crypto from 'expo-crypto';

class MobileOAuthClient {
  private clientId = 'mobile_app_client_id';
  private redirectUri = 'myapp://oauth/callback';
  private authUrl = 'https://auth.example.com/authorize';
  private tokenUrl = 'https://auth.example.com/token';

  async login(): Promise<void> {
    // Generate PKCE parameters
    const codeVerifier = this.generateCodeVerifier();
    const codeChallenge = await this.generateCodeChallenge(codeVerifier);

    // Store code_verifier for later
    await AsyncStorage.setItem('code_verifier', codeVerifier);

    // Build authorization URL
    const state = this.generateState();
    const params = new URLSearchParams({
      client_id: this.clientId,
      redirect_uri: this.redirectUri,
      response_type: 'code',
      scope: 'read:profile write:profile',
      state: state,
      code_challenge: codeChallenge,
      code_challenge_method: 'S256'
    });

    const authorizationUrl = `${this.authUrl}?${params}`;

    // Open browser for user authentication
    const result = await WebBrowser.openAuthSessionAsync(
      authorizationUrl,
      this.redirectUri
    );

    if (result.type === 'success') {
      const { code, state: returnedState } = this.parseCallback(result.url);

      // Verify state
      if (state !== returnedState) {
        throw new Error('Invalid state parameter');
      }

      // Exchange code for tokens
      await this.exchangeCodeForTokens(code, codeVerifier);
    }
  }

  private generateCodeVerifier(): string {
    const array = new Uint8Array(32);
    Crypto.getRandomValues(array);
    return this.base64URLEncode(array);
  }

  private async generateCodeChallenge(verifier: string): Promise<string> {
    const hashed = await Crypto.digestStringAsync(
      Crypto.CryptoDigestAlgorithm.SHA256,
      verifier
    );
    return this.base64URLEncode(hashed);
  }

  private async exchangeCodeForTokens(
    code: string,
    codeVerifier: string
  ): Promise<void> {
    const response = await fetch(this.tokenUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        grant_type: 'authorization_code',
        code: code,
        redirect_uri: this.redirectUri,
        client_id: this.clientId,
        code_verifier: codeVerifier
      })
    });

    if (!response.ok) {
      throw new Error('Token exchange failed');
    }

    const tokens = await response.json();

    // Store tokens securely
    await SecureStore.setItemAsync('access_token', tokens.access_token);
    await SecureStore.setItemAsync('refresh_token', tokens.refresh_token);

    // Clear code_verifier
    await AsyncStorage.removeItem('code_verifier');
  }

  private base64URLEncode(input: any): string {
    return btoa(String.fromCharCode(...new Uint8Array(input)))
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '');
  }
}
```

## Example 5: Rate-Limited API Keys

**Scenario:** Public API with tiered rate limits per key.

```python
# rate_limiter.py
from datetime import datetime, timedelta
import redis.asyncio as redis

class RateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def check_limit(
        self,
        key_id: str,
        limit: int,
        window_seconds: int = 3600
    ) -> tuple[bool, dict]:
        """Check if request is within rate limit"""
        now = datetime.utcnow().timestamp()
        window_start = now - window_seconds
        key = f"rate_limit:{key_id}"

        # Remove old entries
        await self.redis.zremrangebyscore(key, 0, window_start)

        # Count requests in current window
        count = await self.redis.zcard(key)

        if count >= limit:
            # Get reset time
            oldest = await self.redis.zrange(key, 0, 0, withscores=True)
            reset_at = oldest[0][1] + window_seconds if oldest else now

            return False, {
                "limit": limit,
                "remaining": 0,
                "reset": int(reset_at)
            }

        # Add current request
        await self.redis.zadd(key, {str(now): now})
        await self.redis.expire(key, window_seconds)

        return True, {
            "limit": limit,
            "remaining": limit - count - 1,
            "reset": int(now + window_seconds)
        }

# Middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    api_key = request.state.api_key  # From auth middleware

    # Get tier-specific limit
    limits = {
        "free": 100,
        "pro": 1000,
        "enterprise": 10000
    }
    limit = limits.get(api_key.tier, 100)

    allowed, info = await rate_limiter.check_limit(
        api_key.id,
        limit,
        window_seconds=3600
    )

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded"},
            headers={
                "X-RateLimit-Limit": str(info["limit"]),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(info["reset"]),
                "Retry-After": str(info["reset"] - int(time.time()))
            }
        )

    response = await call_next(request)

    # Add rate limit headers
    response.headers["X-RateLimit-Limit"] = str(info["limit"])
    response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
    response.headers["X-RateLimit-Reset"] = str(info["reset"])

    return response
```

---

*API Authentication Examples v1.0*
