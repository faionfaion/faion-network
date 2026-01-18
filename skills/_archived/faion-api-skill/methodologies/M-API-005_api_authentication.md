# M-API-005: API Authentication

## Metadata
- **ID:** M-API-005
- **Category:** API
- **Difficulty:** Intermediate
- **Tags:** [api, authentication, security, oauth, jwt]
- **Agent:** faion-api-agent

---

## Problem

APIs need to verify who is making requests. Without proper authentication:
- Anyone can access sensitive data
- No way to track usage per user
- Cannot enforce rate limits per user
- Audit trails are impossible

---

## Framework

### Step 1: Choose Authentication Method

| Method | Use Case | Complexity | Security |
|--------|----------|------------|----------|
| API Keys | Server-to-server, simple apps | Low | Medium |
| JWT (Bearer Token) | User authentication, SPAs | Medium | High |
| OAuth 2.0 | Third-party access, enterprise | High | High |
| Session Cookies | Traditional web apps | Low | Medium |

### Step 2: Implement API Key Authentication

**When to use:** Server-to-server communication, simple integrations.

**Implementation:**

```python
# Django middleware
import hashlib
from django.http import JsonResponse

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_key = request.headers.get('X-API-Key')

        if not api_key:
            return JsonResponse(
                {'error': 'API key required'},
                status=401
            )

        # Hash the key for comparison (store hashed keys in DB)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        try:
            api_key_obj = APIKey.objects.get(key_hash=key_hash, is_active=True)
            request.api_client = api_key_obj.client
        except APIKey.DoesNotExist:
            return JsonResponse(
                {'error': 'Invalid API key'},
                status=401
            )

        return self.get_response(request)
```

```javascript
// Express.js middleware
const crypto = require('crypto');

const apiKeyAuth = async (req, res, next) => {
  const apiKey = req.headers['x-api-key'];

  if (!apiKey) {
    return res.status(401).json({ error: 'API key required' });
  }

  const keyHash = crypto
    .createHash('sha256')
    .update(apiKey)
    .digest('hex');

  const client = await APIKey.findOne({
    keyHash,
    isActive: true
  });

  if (!client) {
    return res.status(401).json({ error: 'Invalid API key' });
  }

  req.client = client;
  next();
};
```

**Best practices:**
- Hash keys before storing (never store plain text)
- Support key rotation (multiple active keys per client)
- Include key metadata (created, last used, scopes)
- Rate limit per key

### Step 3: Implement JWT Authentication

**When to use:** User authentication, mobile apps, SPAs.

**JWT Structure:**
```
header.payload.signature

Header: {"alg": "HS256", "typ": "JWT"}
Payload: {"sub": "user123", "exp": 1735689600}
Signature: HMAC-SHA256(header + payload, secret)
```

**Implementation:**

```python
# Django with djangorestframework-simplejwt
# settings.py
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

# urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
]

# views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'user': request.user.email})
```

```javascript
// Express.js with jsonwebtoken
const jwt = require('jsonwebtoken');

// Login endpoint
app.post('/auth/login', async (req, res) => {
  const { email, password } = req.body;

  const user = await User.findOne({ email });
  if (!user || !await user.checkPassword(password)) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const accessToken = jwt.sign(
    { sub: user.id, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: '15m' }
  );

  const refreshToken = jwt.sign(
    { sub: user.id, type: 'refresh' },
    process.env.JWT_REFRESH_SECRET,
    { expiresIn: '7d' }
  );

  res.json({ accessToken, refreshToken });
});

// Auth middleware
const jwtAuth = (req, res, next) => {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Token required' });
  }

  const token = authHeader.split(' ')[1];

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET);
    req.user = payload;
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    }
    return res.status(401).json({ error: 'Invalid token' });
  }
};

// Refresh endpoint
app.post('/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;

  try {
    const payload = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET);

    if (payload.type !== 'refresh') {
      throw new Error('Invalid token type');
    }

    const user = await User.findById(payload.sub);
    const newAccessToken = jwt.sign(
      { sub: user.id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: '15m' }
    );

    res.json({ accessToken: newAccessToken });
  } catch (err) {
    res.status(401).json({ error: 'Invalid refresh token' });
  }
});
```

### Step 4: Implement OAuth 2.0

**When to use:** Third-party integrations, "Login with Google/GitHub".

**Flows:**

| Flow | Use Case |
|------|----------|
| Authorization Code | Web apps with backend |
| Authorization Code + PKCE | Mobile apps, SPAs |
| Client Credentials | Server-to-server |
| Refresh Token | Renewing access |

**Authorization Code Flow:**

```
1. User clicks "Login with GitHub"
2. Redirect to GitHub:
   https://github.com/login/oauth/authorize?
     client_id=YOUR_CLIENT_ID&
     redirect_uri=https://yourapp.com/callback&
     scope=user:email&
     state=random_string

3. User authorizes
4. GitHub redirects to callback:
   https://yourapp.com/callback?code=AUTH_CODE&state=random_string

5. Exchange code for token (server-side):
   POST https://github.com/login/oauth/access_token
   {
     client_id, client_secret, code, redirect_uri
   }

6. Receive access_token
7. Use token to get user info:
   GET https://api.github.com/user
   Authorization: Bearer ACCESS_TOKEN
```

**Implementation:**

```python
# Django with social-auth-app-django
# settings.py
AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GITHUB_KEY = 'your-client-id'
SOCIAL_AUTH_GITHUB_SECRET = 'your-client-secret'
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

# urls.py
urlpatterns = [
    path('auth/', include('social_django.urls', namespace='social')),
]
```

```javascript
// Express.js with Passport.js
const passport = require('passport');
const GitHubStrategy = require('passport-github2').Strategy;

passport.use(new GitHubStrategy({
    clientID: process.env.GITHUB_CLIENT_ID,
    clientSecret: process.env.GITHUB_CLIENT_SECRET,
    callbackURL: "http://localhost:3000/auth/github/callback"
  },
  async (accessToken, refreshToken, profile, done) => {
    let user = await User.findOne({ githubId: profile.id });

    if (!user) {
      user = await User.create({
        githubId: profile.id,
        email: profile.emails[0].value,
        name: profile.displayName
      });
    }

    return done(null, user);
  }
));

app.get('/auth/github', passport.authenticate('github', { scope: ['user:email'] }));

app.get('/auth/github/callback',
  passport.authenticate('github', { failureRedirect: '/login' }),
  (req, res) => {
    // Generate JWT for the authenticated user
    const token = jwt.sign({ sub: req.user.id }, process.env.JWT_SECRET);
    res.redirect(`/app?token=${token}`);
  }
);
```

### Step 5: Implement Token Refresh

**Why refresh tokens:**
- Access tokens are short-lived (15 min) for security
- Refresh tokens are long-lived (7 days) for UX
- If access token is stolen, limited damage window

**Flow:**

```
1. Client sends request with expired access token
2. Server returns 401 with error: "Token expired"
3. Client sends refresh token to /auth/refresh
4. Server validates refresh token
5. Server issues new access token (and optionally new refresh token)
6. Client retries original request
```

**Client-side implementation:**

```javascript
// axios interceptor for automatic refresh
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const { data } = await axios.post('/auth/refresh', {
          refreshToken: localStorage.getItem('refreshToken')
        });

        localStorage.setItem('accessToken', data.accessToken);
        originalRequest.headers.Authorization = `Bearer ${data.accessToken}`;

        return axios(originalRequest);
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);
```

### Step 6: Implement Scopes and Permissions

```python
# Django REST Framework
from rest_framework.permissions import BasePermission

class HasScope(BasePermission):
    def __init__(self, required_scope):
        self.required_scope = required_scope

    def has_permission(self, request, view):
        token_scopes = request.auth.get('scopes', [])
        return self.required_scope in token_scopes

class ProductViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), HasScope('products:write')]
        return [IsAuthenticated(), HasScope('products:read')]
```

```javascript
// Express.js scope middleware
const requireScope = (scope) => (req, res, next) => {
  const userScopes = req.user?.scopes || [];

  if (!userScopes.includes(scope)) {
    return res.status(403).json({
      error: 'Insufficient permissions',
      required: scope
    });
  }

  next();
};

// Usage
app.post('/products',
  jwtAuth,
  requireScope('products:write'),
  createProduct
);
```

---

## Templates

### Auth Endpoints Checklist

```markdown
## Authentication Endpoints

### Registration
- [ ] POST /auth/register
  - Input: email, password, name
  - Output: user + tokens
  - Validations: email format, password strength

### Login
- [ ] POST /auth/login
  - Input: email, password
  - Output: accessToken, refreshToken
  - Rate limiting: 5 attempts per minute

### Token Refresh
- [ ] POST /auth/refresh
  - Input: refreshToken
  - Output: new accessToken
  - Rotate refresh token

### Logout
- [ ] POST /auth/logout
  - Blacklist refresh token
  - Clear client tokens

### Password Reset
- [ ] POST /auth/forgot-password
- [ ] POST /auth/reset-password

### OAuth
- [ ] GET /auth/github
- [ ] GET /auth/github/callback
- [ ] GET /auth/google
- [ ] GET /auth/google/callback
```

### Security Headers

```javascript
// Security headers middleware
app.use((req, res, next) => {
  // Prevent clickjacking
  res.setHeader('X-Frame-Options', 'DENY');

  // Prevent MIME sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // XSS protection
  res.setHeader('X-XSS-Protection', '1; mode=block');

  // HSTS
  res.setHeader(
    'Strict-Transport-Security',
    'max-age=31536000; includeSubDomains'
  );

  next();
});
```

---

## Examples

### Complete Auth Flow (Django)

```python
# models.py
from django.contrib.auth.models import AbstractUser
import secrets

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class RefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)

    @classmethod
    def create_for_user(cls, user):
        return cls.objects.create(
            user=user,
            token=secrets.token_urlsafe(32),
            expires_at=timezone.now() + timedelta(days=7)
        )

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=401
            )

        # Create tokens
        access_token = str(AccessToken.for_user(user))
        refresh_token = RefreshToken.create_for_user(user)

        return Response({
            'accessToken': access_token,
            'refreshToken': refresh_token.token,
            'user': UserSerializer(user).data
        })

class RefreshView(APIView):
    permission_classes = []

    def post(self, request):
        token = request.data.get('refreshToken')

        try:
            refresh = RefreshToken.objects.get(
                token=token,
                revoked=False,
                expires_at__gt=timezone.now()
            )
        except RefreshToken.DoesNotExist:
            return Response(
                {'error': 'Invalid refresh token'},
                status=401
            )

        # Rotate token
        refresh.revoked = True
        refresh.save()

        new_refresh = RefreshToken.create_for_user(refresh.user)
        access_token = str(AccessToken.for_user(refresh.user))

        return Response({
            'accessToken': access_token,
            'refreshToken': new_refresh.token
        })

class LogoutView(APIView):
    def post(self, request):
        token = request.data.get('refreshToken')

        RefreshToken.objects.filter(
            token=token,
            user=request.user
        ).update(revoked=True)

        return Response({'message': 'Logged out'})
```

---

## Common Mistakes

1. **Storing tokens in localStorage**
   - Vulnerable to XSS
   - Use httpOnly cookies for refresh tokens

2. **Long-lived access tokens**
   - If stolen, long exposure
   - Keep access tokens short (15-30 min)

3. **Not validating token expiry**
   - Always check exp claim
   - Handle expired tokens gracefully

4. **Secrets in code**
   - Never commit secrets
   - Use environment variables

5. **No token revocation**
   - Can't invalidate compromised tokens
   - Implement token blacklist

---

## Next Steps

1. **Start with JWT** - Good balance of simplicity and security
2. **Add refresh tokens** - Better UX without compromising security
3. **Implement OAuth** - For social login
4. **Add scopes** - Fine-grained permissions
5. **Audit logging** - Track authentication events

---

## Related Methodologies

- [M-API-001: REST API Design](./M-API-001_rest_api_design.md)
- [M-API-006: Rate Limiting](./M-API-006_rate_limiting.md)
- [M-API-007: Error Handling](./M-API-007_error_handling.md)

---

*Methodology: API Authentication*
*Version: 1.0*
*Agent: faion-api-agent*
