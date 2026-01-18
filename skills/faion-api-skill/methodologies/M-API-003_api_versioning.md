# M-API-003: API Versioning

## Metadata
- **ID:** M-API-003
- **Category:** API
- **Difficulty:** Intermediate
- **Tags:** [api, versioning, backwards-compatibility]
- **Agent:** faion-api-agent

---

## Problem

APIs evolve over time. Without versioning:
- Breaking changes break client applications
- No way to deprecate old functionality
- Clients forced to update immediately
- Impossible to support multiple client versions

---

## Framework

### Step 1: Choose Versioning Strategy

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| URL Path | `/v1/users` | Clear, cacheable | URL changes |
| Query Param | `/users?version=1` | Flexible | Easy to miss |
| Header | `Accept: application/vnd.api+json;version=1` | Clean URLs | Hidden |
| Content Negotiation | `Accept: application/vnd.company.v1+json` | RESTful | Complex |

**Recommendation:** URL Path versioning is most common and clear.

### Step 2: Define What's a Breaking Change

**Breaking changes (require new version):**

```yaml
# Field removal
- name: string  # Removing this breaks clients

# Type change
- age: string   # Was: age: number

# Required field added
- newRequiredField: string!  # Existing requests fail

# Endpoint removal
DELETE /v1/legacy-endpoint

# Status code change
200 -> 201  # Clients may not handle

# Authentication change
API Key -> OAuth  # Old keys stop working
```

**Non-breaking changes (safe):**

```yaml
# New optional field
+ nickname: string?  # Clients ignore unknown fields

# New endpoint
+ GET /v1/new-resource

# New optional parameter
+ ?include=details

# New enum value (if clients handle unknown)
+ status: "NEW_STATUS"

# Performance improvements
# Documentation updates
```

### Step 3: Implement URL Versioning

**Express.js:**

```javascript
// routes/v1/users.js
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  // V1 response format
  res.json({
    users: [
      { id: 1, name: 'John', email: 'john@example.com' }
    ]
  });
});

module.exports = router;

// routes/v2/users.js
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  // V2 response format (different structure)
  res.json({
    data: [
      {
        id: '1',
        type: 'user',
        attributes: { name: 'John', email: 'john@example.com' }
      }
    ],
    meta: { total: 1 }
  });
});

module.exports = router;

// app.js
const app = express();

app.use('/v1/users', require('./routes/v1/users'));
app.use('/v2/users', require('./routes/v2/users'));
```

**Django:**

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    path('v1/', include('api.v1.urls')),
    path('v2/', include('api.v2.urls')),
]

# api/v1/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListV1.as_view()),
    path('users/<int:pk>/', views.UserDetailV1.as_view()),
]

# api/v2/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListV2.as_view()),
    path('users/<int:pk>/', views.UserDetailV2.as_view()),
]
```

### Step 4: Implement Header Versioning

**Express.js:**

```javascript
// middleware/version.js
const versionMiddleware = (req, res, next) => {
  // Check Accept header
  const accept = req.headers['accept'] || '';
  const versionMatch = accept.match(/version=(\d+)/);

  // Or check custom header
  const customVersion = req.headers['api-version'];

  req.apiVersion = versionMatch?.[1] || customVersion || '1';
  next();
};

// routes/users.js
router.get('/', (req, res) => {
  if (req.apiVersion === '2') {
    return res.json({ data: users, meta: {} });
  }
  // Default to v1
  res.json({ users });
});
```

**Django REST Framework:**

```python
# versioning.py
from rest_framework.versioning import AcceptHeaderVersioning

class CustomVersioning(AcceptHeaderVersioning):
    default_version = '1.0'
    allowed_versions = ['1.0', '2.0']
    version_param = 'version'

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'api.versioning.CustomVersioning',
}

# views.py
class UserViewSet(viewsets.ModelViewSet):
    def list(self, request):
        if request.version == '2.0':
            serializer = UserV2Serializer(self.get_queryset(), many=True)
        else:
            serializer = UserV1Serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
```

### Step 5: Plan Deprecation

**Deprecation timeline:**

```yaml
Timeline:
  1. Announce deprecation (6+ months before)
  2. Add deprecation headers
  3. Update documentation
  4. Reduce support (3 months before)
  5. Remove version (on date)
```

**Deprecation headers:**

```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 01 Jan 2025 00:00:00 GMT
Link: <https://api.example.com/v2/users>; rel="successor-version"
Warning: 299 - "This API version is deprecated. Please migrate to v2."
```

**Implementation:**

```javascript
// middleware/deprecation.js
const deprecatedVersions = {
  'v1': {
    sunset: new Date('2025-01-01'),
    successor: '/v2'
  }
};

const deprecationMiddleware = (req, res, next) => {
  const version = req.path.match(/^\/(v\d+)/)?.[1];
  const deprecation = deprecatedVersions[version];

  if (deprecation) {
    res.set('Deprecation', 'true');
    res.set('Sunset', deprecation.sunset.toUTCString());
    res.set('Link', `<${deprecation.successor}>; rel="successor-version"`);
    res.set('Warning', `299 - "API ${version} is deprecated"`);
  }

  next();
};
```

### Step 6: Maintain Multiple Versions

**Shared logic pattern:**

```javascript
// services/userService.js
class UserService {
  async getUsers(options = {}) {
    const users = await User.find(options.filter);
    return users;
  }

  async createUser(data) {
    // Shared business logic
    return User.create(data);
  }
}

// routes/v1/users.js
router.get('/', async (req, res) => {
  const users = await userService.getUsers();
  // V1 formatting
  res.json({ users: users.map(formatUserV1) });
});

// routes/v2/users.js
router.get('/', async (req, res) => {
  const users = await userService.getUsers();
  // V2 formatting
  res.json({
    data: users.map(formatUserV2),
    meta: { total: users.length }
  });
});
```

**Version-specific serializers (Django):**

```python
# serializers/v1.py
class UserSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

# serializers/v2.py
class UserSerializerV2(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'created_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
```

---

## Templates

### Version Planning Checklist

```markdown
## API Version: v{X}

### Breaking Changes
- [ ] Field removed: {field}
- [ ] Field type changed: {field}
- [ ] Endpoint removed: {endpoint}
- [ ] Auth method changed

### Migration Guide
- [ ] Document all changes
- [ ] Provide code examples
- [ ] List deprecated endpoints
- [ ] Specify sunset date

### Timeline
- [ ] Announcement date: {date}
- [ ] v{X} release date: {date}
- [ ] v{X-1} deprecation: {date}
- [ ] v{X-1} sunset: {date}
```

### Changelog Template

```markdown
# API Changelog

## v2.0.0 (2025-01-15)

### Breaking Changes
- Removed \`GET /users/{id}/settings\` - Use \`GET /users/{id}?include=settings\`
- Changed \`User.name\` from string to object \`{ first, last }\`
- Authentication now requires OAuth 2.0 (API keys deprecated)

### New Features
- Added \`POST /users/{id}/preferences\`
- Added cursor-based pagination
- Added rate limit headers

### Deprecations
- \`GET /legacy/users\` - Sunset: 2025-07-01

### Migration Guide
See [v1 to v2 Migration](./docs/migration-v1-v2.md)

## v1.5.0 (2024-10-01)
### Added
- New \`status\` field on Order resource
- Webhook support for order events
```

---

## Examples

### Complete Versioning Setup (Express.js)

```javascript
// app.js
const express = require('express');
const app = express();

// Version config
const VERSIONS = {
  current: 'v2',
  supported: ['v1', 'v2'],
  deprecated: ['v1'],
  sunset: { 'v1': new Date('2025-06-01') }
};

// Deprecation middleware
app.use((req, res, next) => {
  const version = req.path.match(/^\/(v\d+)/)?.[1];

  if (version && VERSIONS.deprecated.includes(version)) {
    res.set({
      'Deprecation': 'true',
      'Sunset': VERSIONS.sunset[version].toUTCString(),
      'Warning': `299 - "${version} is deprecated, use ${VERSIONS.current}"`
    });
  }

  next();
});

// Version routes
app.use('/v1', require('./routes/v1'));
app.use('/v2', require('./routes/v2'));

// Redirect unversioned to current
app.use('/users', (req, res) => {
  res.redirect(307, `/v2/users${req.url === '/' ? '' : req.url}`);
});

// Version info endpoint
app.get('/versions', (req, res) => {
  res.json({
    current: VERSIONS.current,
    supported: VERSIONS.supported,
    deprecated: VERSIONS.deprecated.map(v => ({
      version: v,
      sunset: VERSIONS.sunset[v]
    }))
  });
});

app.listen(3000);
```

### Version Negotiation (Django REST)

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': '2',
    'ALLOWED_VERSIONS': ['1', '2'],
    'VERSION_PARAM': 'version',
}

# views.py
from rest_framework import viewsets
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.version == '1':
            return UserSerializerV1
        return UserSerializerV2

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Add deprecation warning for v1
        response = Response(serializer.data)
        if request.version == '1':
            response['Deprecation'] = 'true'
            response['Warning'] = '299 - "v1 deprecated, use v2"'

        return response

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

router_v2 = DefaultRouter()
router_v2.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v2/', include(router_v2.urls)),
]
```

---

## Common Mistakes

1. **No versioning from start**
   - Hard to add later
   - Start with v1 from day one

2. **Breaking changes in minor versions**
   - v1.1 should not break v1.0 clients
   - Use semantic versioning

3. **Too many active versions**
   - Support max 2-3 versions
   - Clear sunset dates

4. **Inconsistent versioning**
   - Mix of URL and header
   - Pick one strategy

5. **No migration path**
   - Clients don't know how to upgrade
   - Always provide migration guide

---

## Next Steps

1. **Choose strategy** - URL path recommended for most cases
2. **Start with v1** - Even if it's your first version
3. **Document changes** - Keep detailed changelog
4. **Plan deprecation** - 6-12 months notice
5. **Monitor usage** - Track which versions are used

---

## Related Methodologies

- [M-API-001: REST API Design](./M-API-001_rest_api_design.md)
- [M-API-004: OpenAPI Specification](./M-API-004_openapi_specification.md)
- [M-API-012: Contract-First Development](./M-API-012_contract_first_development.md)

---

*Methodology: API Versioning*
*Version: 1.0*
*Agent: faion-api-agent*
