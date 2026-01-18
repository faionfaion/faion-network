# M-API-009: API Testing

## Metadata
- **ID:** M-API-009
- **Category:** API
- **Difficulty:** Intermediate
- **Tags:** [api, testing, contract-testing, pact, postman]
- **Agent:** faion-api-agent

---

## Problem

Without API testing:
- Bugs reach production
- Breaking changes go unnoticed
- Integration failures surprise everyone
- Regression testing is manual and slow
- Contract violations between services

---

## Framework

### Step 1: Understand Testing Layers

| Layer | Purpose | Tools |
|-------|---------|-------|
| Unit | Test individual functions | pytest, jest |
| Integration | Test API endpoints | pytest, supertest |
| Contract | Verify API contracts | Pact, Dredd |
| E2E | Full user flows | Postman, Playwright |
| Load | Performance under stress | k6, Locust |

### Step 2: Write Integration Tests

**Python (pytest + Django):**

```python
# tests/test_users_api.py
import pytest
from rest_framework.test import APIClient
from rest_framework import status

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )

class TestUsersAPI:
    def test_list_users_unauthorized(self, api_client):
        """Anonymous users cannot list users"""
        response = api_client.get('/api/v1/users/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_users_authorized(self, authenticated_client, user):
        """Authenticated users can list users"""
        response = authenticated_client.get('/api/v1/users/')
        assert response.status_code == status.HTTP_200_OK
        assert 'data' in response.json()

    def test_create_user_success(self, authenticated_client):
        """Create user with valid data"""
        data = {
            'email': 'new@example.com',
            'password': 'SecurePass123!',
            'name': 'New User'
        }
        response = authenticated_client.post('/api/v1/users/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['data']['email'] == 'new@example.com'

    def test_create_user_validation_error(self, authenticated_client):
        """Invalid email returns 422"""
        data = {
            'email': 'invalid-email',
            'password': 'pass'
        }
        response = authenticated_client.post('/api/v1/users/', data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()['error']['code'] == 'VALIDATION_ERROR'

    def test_create_user_duplicate_email(self, authenticated_client, user):
        """Duplicate email returns 409"""
        data = {
            'email': user.email,
            'password': 'SecurePass123!'
        }
        response = authenticated_client.post('/api/v1/users/', data)
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_get_user_success(self, authenticated_client, user):
        """Get existing user by ID"""
        response = authenticated_client.get(f'/api/v1/users/{user.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']['id'] == str(user.id)

    def test_get_user_not_found(self, authenticated_client):
        """Non-existent user returns 404"""
        response = authenticated_client.get('/api/v1/users/nonexistent/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_user_success(self, authenticated_client, user):
        """Update user with valid data"""
        data = {'name': 'Updated Name'}
        response = authenticated_client.patch(f'/api/v1/users/{user.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['data']['name'] == 'Updated Name'

    def test_delete_user_success(self, authenticated_client, user):
        """Delete user returns 204"""
        response = authenticated_client.delete(f'/api/v1/users/{user.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
```

**JavaScript (Jest + Supertest):**

```javascript
// tests/users.test.js
const request = require('supertest');
const app = require('../app');
const { User } = require('../models');
const { generateToken } = require('../auth');

describe('Users API', () => {
  let authToken;
  let testUser;

  beforeAll(async () => {
    testUser = await User.create({
      email: 'test@example.com',
      password: 'testpass123',
      name: 'Test User'
    });
    authToken = generateToken(testUser);
  });

  afterAll(async () => {
    await User.deleteMany({});
  });

  describe('GET /api/v1/users', () => {
    it('returns 401 without authentication', async () => {
      const response = await request(app)
        .get('/api/v1/users')
        .expect(401);

      expect(response.body.error.code).toBe('UNAUTHORIZED');
    });

    it('returns users list with authentication', async () => {
      const response = await request(app)
        .get('/api/v1/users')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.data).toBeInstanceOf(Array);
      expect(response.body.meta).toHaveProperty('total');
    });

    it('supports pagination', async () => {
      const response = await request(app)
        .get('/api/v1/users?page=1&per_page=10')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.meta.page).toBe(1);
      expect(response.body.meta.perPage).toBe(10);
    });
  });

  describe('POST /api/v1/users', () => {
    it('creates user with valid data', async () => {
      const response = await request(app)
        .post('/api/v1/users')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          email: 'new@example.com',
          password: 'SecurePass123!',
          name: 'New User'
        })
        .expect(201);

      expect(response.body.data.email).toBe('new@example.com');
      expect(response.headers.location).toContain('/users/');
    });

    it('returns 422 for invalid email', async () => {
      const response = await request(app)
        .post('/api/v1/users')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          email: 'invalid',
          password: 'SecurePass123!'
        })
        .expect(422);

      expect(response.body.error.code).toBe('VALIDATION_ERROR');
      expect(response.body.error.details).toContainEqual(
        expect.objectContaining({ field: 'email' })
      );
    });

    it('returns 409 for duplicate email', async () => {
      const response = await request(app)
        .post('/api/v1/users')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          email: testUser.email,
          password: 'SecurePass123!'
        })
        .expect(409);

      expect(response.body.error.code).toBe('CONFLICT');
    });
  });

  describe('GET /api/v1/users/:id', () => {
    it('returns user by ID', async () => {
      const response = await request(app)
        .get(`/api/v1/users/${testUser.id}`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.data.id).toBe(testUser.id.toString());
    });

    it('returns 404 for non-existent user', async () => {
      const response = await request(app)
        .get('/api/v1/users/nonexistent123')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(404);

      expect(response.body.error.code).toBe('NOT_FOUND');
    });
  });
});
```

### Step 3: Implement Contract Testing with Pact

**Consumer side (Frontend/Client):**

```javascript
// tests/pact/userService.pact.js
const { Pact } = require('@pact-foundation/pact');
const { UserService } = require('../../services/userService');

describe('User Service Pact', () => {
  const provider = new Pact({
    consumer: 'WebApp',
    provider: 'UserAPI',
    port: 1234
  });

  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());
  afterEach(() => provider.verify());

  describe('get user by ID', () => {
    it('returns user when exists', async () => {
      // Define expected interaction
      await provider.addInteraction({
        state: 'user with ID usr_123 exists',
        uponReceiving: 'a request for user usr_123',
        withRequest: {
          method: 'GET',
          path: '/api/v1/users/usr_123',
          headers: {
            Authorization: 'Bearer valid_token'
          }
        },
        willRespondWith: {
          status: 200,
          headers: {
            'Content-Type': 'application/json'
          },
          body: {
            data: {
              id: 'usr_123',
              email: Matchers.email(),
              name: Matchers.string('John Doe'),
              status: Matchers.term({
                matcher: 'active|inactive|pending',
                generate: 'active'
              })
            }
          }
        }
      });

      // Execute and verify
      const service = new UserService(provider.mockService.baseUrl);
      const user = await service.getUser('usr_123', 'valid_token');

      expect(user.id).toBe('usr_123');
    });

    it('returns 404 when user not found', async () => {
      await provider.addInteraction({
        state: 'user with ID nonexistent does not exist',
        uponReceiving: 'a request for nonexistent user',
        withRequest: {
          method: 'GET',
          path: '/api/v1/users/nonexistent',
          headers: {
            Authorization: 'Bearer valid_token'
          }
        },
        willRespondWith: {
          status: 404,
          body: {
            error: {
              code: 'NOT_FOUND',
              message: Matchers.string()
            }
          }
        }
      });

      const service = new UserService(provider.mockService.baseUrl);
      await expect(service.getUser('nonexistent', 'valid_token'))
        .rejects.toThrow('NOT_FOUND');
    });
  });
});
```

**Provider side (Backend):**

```python
# tests/pact/test_provider.py
import pytest
from pact import Verifier

@pytest.fixture
def pact_verifier():
    return Verifier(
        provider='UserAPI',
        provider_base_url='http://localhost:8000'
    )

def test_user_service_contract(pact_verifier):
    # Set up provider states
    pact_verifier.set_state(
        'user with ID usr_123 exists',
        lambda: User.objects.create(id='usr_123', email='test@example.com')
    )

    pact_verifier.set_state(
        'user with ID nonexistent does not exist',
        lambda: None
    )

    # Verify against pact file
    pact_verifier.verify_with_broker(
        broker_url='https://pact-broker.example.com',
        consumer_version_selectors=[{'latest': True}],
        publish_verification_results=True,
        provider_version='1.0.0'
    )
```

### Step 4: Use Postman for E2E Testing

**Postman Collection:**

```json
{
  "info": {
    "name": "Users API E2E",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "baseUrl",
      "value": "https://api.example.com/v1"
    },
    {
      "key": "authToken",
      "value": ""
    }
  ],
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Login",
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Status is 200', () => {",
                  "  pm.response.to.have.status(200);",
                  "});",
                  "",
                  "pm.test('Has access token', () => {",
                  "  const json = pm.response.json();",
                  "  pm.expect(json.accessToken).to.be.a('string');",
                  "  pm.collectionVariables.set('authToken', json.accessToken);",
                  "});"
                ]
              }
            }
          ],
          "request": {
            "method": "POST",
            "url": "{{baseUrl}}/auth/login",
            "body": {
              "mode": "raw",
              "raw": "{\"email\": \"test@example.com\", \"password\": \"testpass\"}",
              "options": { "raw": { "language": "json" } }
            }
          }
        }
      ]
    },
    {
      "name": "Users",
      "item": [
        {
          "name": "Create User",
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Status is 201', () => {",
                  "  pm.response.to.have.status(201);",
                  "});",
                  "",
                  "pm.test('Response has user data', () => {",
                  "  const json = pm.response.json();",
                  "  pm.expect(json.data).to.have.property('id');",
                  "  pm.expect(json.data.email).to.eql('new@example.com');",
                  "  pm.collectionVariables.set('userId', json.data.id);",
                  "});"
                ]
              }
            }
          ],
          "request": {
            "method": "POST",
            "url": "{{baseUrl}}/users",
            "header": [
              { "key": "Authorization", "value": "Bearer {{authToken}}" }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\"email\": \"new@example.com\", \"password\": \"SecurePass123!\"}",
              "options": { "raw": { "language": "json" } }
            }
          }
        },
        {
          "name": "Get User",
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Status is 200', () => {",
                  "  pm.response.to.have.status(200);",
                  "});",
                  "",
                  "pm.test('Returns correct user', () => {",
                  "  const json = pm.response.json();",
                  "  pm.expect(json.data.id).to.eql(pm.collectionVariables.get('userId'));",
                  "});"
                ]
              }
            }
          ],
          "request": {
            "method": "GET",
            "url": "{{baseUrl}}/users/{{userId}}",
            "header": [
              { "key": "Authorization", "value": "Bearer {{authToken}}" }
            ]
          }
        }
      ]
    }
  ]
}
```

**Run with Newman (CLI):**

```bash
newman run collection.json \
  --environment production.postman_environment.json \
  --reporters cli,junit \
  --reporter-junit-export results.xml
```

### Step 5: Validate OpenAPI Spec

**Dredd (against OpenAPI spec):**

```yaml
# dredd.yml
dry-run: false
hookfiles:
  - ./tests/dredd/hooks.js
language: nodejs
server: npm start
endpoint: http://localhost:3000
path:
  - ./openapi.yaml
```

```javascript
// tests/dredd/hooks.js
const hooks = require('hooks');
const jwt = require('jsonwebtoken');

let authToken;

hooks.beforeAll((transactions, done) => {
  authToken = jwt.sign({ sub: 'test-user' }, process.env.JWT_SECRET);
  done();
});

hooks.beforeEach((transaction, done) => {
  if (transaction.request.headers['Authorization']) {
    transaction.request.headers['Authorization'] = `Bearer ${authToken}`;
  }
  done();
});

// Skip or modify specific transactions
hooks.before('Users > Create User', (transaction, done) => {
  transaction.request.body = JSON.stringify({
    email: `test-${Date.now()}@example.com`,
    password: 'SecurePass123!'
  });
  done();
});
```

```bash
dredd
```

### Step 6: Load Testing with k6

```javascript
// tests/load/users.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const responseTime = new Trend('response_time');

export const options = {
  stages: [
    { duration: '30s', target: 10 },   // Ramp up
    { duration: '1m', target: 50 },    // Stay at 50 users
    { duration: '30s', target: 100 },  // Peak
    { duration: '30s', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    errors: ['rate<0.1'],              // Error rate under 10%
  },
};

const BASE_URL = __ENV.API_URL || 'https://api.example.com';
const AUTH_TOKEN = __ENV.AUTH_TOKEN;

export default function () {
  // List users
  const listResponse = http.get(`${BASE_URL}/v1/users?page=1&per_page=20`, {
    headers: { Authorization: `Bearer ${AUTH_TOKEN}` },
  });

  check(listResponse, {
    'list users status is 200': (r) => r.status === 200,
    'list users has data': (r) => JSON.parse(r.body).data !== undefined,
  });

  errorRate.add(listResponse.status !== 200);
  responseTime.add(listResponse.timings.duration);

  sleep(1);

  // Get single user
  const userId = JSON.parse(listResponse.body).data[0]?.id;
  if (userId) {
    const getResponse = http.get(`${BASE_URL}/v1/users/${userId}`, {
      headers: { Authorization: `Bearer ${AUTH_TOKEN}` },
    });

    check(getResponse, {
      'get user status is 200': (r) => r.status === 200,
    });

    errorRate.add(getResponse.status !== 200);
    responseTime.add(getResponse.timings.duration);
  }

  sleep(1);
}
```

```bash
k6 run tests/load/users.js --env API_URL=https://api.example.com --env AUTH_TOKEN=xxx
```

---

## Templates

### Test Coverage Checklist

```markdown
## API Test Coverage: {Endpoint}

### Positive Cases
- [ ] Success with minimal required data
- [ ] Success with all optional fields
- [ ] Success with edge case values

### Negative Cases
- [ ] Missing required fields (422)
- [ ] Invalid field values (422)
- [ ] Unauthorized access (401)
- [ ] Forbidden access (403)
- [ ] Resource not found (404)
- [ ] Duplicate/conflict (409)

### Edge Cases
- [ ] Empty request body
- [ ] Large payload
- [ ] Special characters in input
- [ ] Pagination boundaries
- [ ] Concurrent requests

### Integration
- [ ] Related resources updated
- [ ] Events/webhooks triggered
- [ ] Audit logs created
```

---

## Common Mistakes

1. **Only testing happy path**
   - Missing error cases
   - Test all status codes

2. **Hardcoded test data**
   - Tests fail on different environments
   - Use fixtures and factories

3. **No contract tests**
   - Frontend/backend drift apart
   - Use Pact or similar

4. **Skipping auth tests**
   - Security vulnerabilities
   - Test all auth scenarios

5. **No load testing**
   - Performance issues in production
   - Run before major releases

---

## Next Steps

1. **Start with integration tests** - Cover all endpoints
2. **Add contract tests** - Prevent breaking changes
3. **Automate in CI** - Run on every commit
4. **Add load tests** - Before releases
5. **Monitor coverage** - Aim for 80%+

---

## Related Methodologies

- [M-API-004: OpenAPI Specification](./M-API-004_openapi_specification.md)
- [M-API-007: Error Handling](./M-API-007_error_handling.md)
- [M-API-012: Contract-First Development](./M-API-012_contract_first_development.md)

---

*Methodology: API Testing*
*Version: 1.0*
*Agent: faion-api-agent*
