# M-API-012: Contract-First Development

## Metadata
- **ID:** M-API-012
- **Category:** API
- **Difficulty:** Intermediate
- **Tags:** [api, contract-first, openapi, design-first]
- **Agent:** faion-api-agent

---

## Problem

Traditional "code-first" API development leads to:
- API design influenced by implementation details
- Frontend blocked waiting for backend
- Documentation always out of date
- Breaking changes discovered late
- No clear contract between teams

Contract-first flips this: **design the API contract first, then implement**.

---

## Framework

### Step 1: Understand the Approach

**Code-First vs Contract-First:**

| Aspect | Code-First | Contract-First |
|--------|------------|----------------|
| Start with | Implementation | OpenAPI spec |
| Documentation | Generated after | Source of truth |
| Frontend start | After backend done | Immediately (mocks) |
| Changes | Frequent, breaking | Planned, versioned |
| Team alignment | Often misaligned | Single source of truth |

### Step 2: Write OpenAPI Spec First

**Start with the contract:**

```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: Users API
  version: 1.0.0
  description: User management API

servers:
  - url: http://localhost:3000/api/v1
    description: Development
  - url: https://api.example.com/v1
    description: Production

paths:
  /users:
    get:
      operationId: listUsers
      summary: List all users
      tags: [Users]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: per_page
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'

    post:
      operationId: createUser
      summary: Create a new user
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserInput'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '422':
          $ref: '#/components/responses/ValidationError'

  /users/{userId}:
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: string
          format: uuid

    get:
      operationId: getUser
      summary: Get user by ID
      tags: [Users]
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      required: [id, email, createdAt]
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        status:
          type: string
          enum: [active, inactive, pending]
        createdAt:
          type: string
          format: date-time

    CreateUserInput:
      type: object
      required: [email, password]
      properties:
        email:
          type: string
          format: email
        password:
          type: string
          minLength: 8
        name:
          type: string

    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        meta:
          $ref: '#/components/schemas/PaginationMeta'

    PaginationMeta:
      type: object
      properties:
        total:
          type: integer
        page:
          type: integer
        perPage:
          type: integer

    Error:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            details:
              type: array
              items:
                type: object

  responses:
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: NOT_FOUND
              message: User not found

    ValidationError:
      description: Validation error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

### Step 3: Review and Approve Contract

**Review checklist:**

```markdown
## API Contract Review

### Naming
- [ ] Resource names are nouns (plural)
- [ ] Consistent naming convention
- [ ] Clear, descriptive operation IDs

### Endpoints
- [ ] RESTful URL structure
- [ ] Appropriate HTTP methods
- [ ] Pagination for collections
- [ ] Filtering parameters defined

### Schemas
- [ ] All fields documented
- [ ] Required fields marked
- [ ] Formats specified (email, uuid, date-time)
- [ ] Constraints defined (min, max, pattern)

### Responses
- [ ] All status codes documented
- [ ] Error format consistent
- [ ] Examples provided

### Security
- [ ] Authentication defined
- [ ] Authorization documented
- [ ] Sensitive fields identified

### Compatibility
- [ ] No breaking changes from previous version
- [ ] Deprecation notices included
```

### Step 4: Set Up Mock Server

**Prism (OpenAPI mock server):**

```bash
# Install Prism
npm install -g @stoplight/prism-cli

# Start mock server
prism mock openapi.yaml

# Server runs on http://localhost:4010
```

**Custom mock with Express:**

```javascript
// mock-server.js
const express = require('express');
const { faker } = require('@faker-js/faker');

const app = express();
app.use(express.json());

// Mock users
const generateUser = (overrides = {}) => ({
  id: faker.string.uuid(),
  email: faker.internet.email(),
  name: faker.person.fullName(),
  status: faker.helpers.arrayElement(['active', 'inactive', 'pending']),
  createdAt: faker.date.past().toISOString(),
  ...overrides
});

let users = Array.from({ length: 50 }, () => generateUser());

// List users
app.get('/api/v1/users', (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const perPage = Math.min(parseInt(req.query.per_page) || 20, 100);

  const start = (page - 1) * perPage;
  const paginatedUsers = users.slice(start, start + perPage);

  res.json({
    data: paginatedUsers,
    meta: {
      total: users.length,
      page,
      perPage
    }
  });
});

// Get user
app.get('/api/v1/users/:userId', (req, res) => {
  const user = users.find(u => u.id === req.params.userId);

  if (!user) {
    return res.status(404).json({
      error: {
        code: 'NOT_FOUND',
        message: 'User not found'
      }
    });
  }

  res.json({ data: user });
});

// Create user
app.post('/api/v1/users', (req, res) => {
  const { email, password, name } = req.body;

  // Validation
  const errors = [];
  if (!email) errors.push({ field: 'email', message: 'Required' });
  if (!password) errors.push({ field: 'password', message: 'Required' });
  if (password && password.length < 8) {
    errors.push({ field: 'password', message: 'Must be at least 8 characters' });
  }

  if (errors.length > 0) {
    return res.status(422).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Validation failed',
        details: errors
      }
    });
  }

  const newUser = generateUser({ email, name });
  users.push(newUser);

  res.status(201).json({ data: newUser });
});

app.listen(4010, () => {
  console.log('Mock server running on http://localhost:4010');
});
```

### Step 5: Generate Server Code

**OpenAPI Generator:**

```bash
# Install
npm install @openapitools/openapi-generator-cli -g

# Generate Python/FastAPI server
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python-fastapi \
  -o ./server

# Generate Node.js/Express server
openapi-generator-cli generate \
  -i openapi.yaml \
  -g nodejs-express-server \
  -o ./server

# Generate TypeScript types
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o ./client
```

**Generated FastAPI structure:**

```python
# server/openapi_server/apis/users_api.py
from openapi_server.models import User, CreateUserInput, UserList

class UsersApi:
    async def list_users(
        self,
        page: int = 1,
        per_page: int = 20
    ) -> UserList:
        # TODO: Implement
        pass

    async def create_user(
        self,
        create_user_input: CreateUserInput
    ) -> User:
        # TODO: Implement
        pass

    async def get_user(
        self,
        user_id: str
    ) -> User:
        # TODO: Implement
        pass
```

### Step 6: Generate Client SDKs

**TypeScript client:**

```bash
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-fetch \
  -o ./sdk/typescript \
  --additional-properties=npmName=@myorg/api-client
```

**Usage:**

```typescript
// Generated client usage
import { UsersApi, Configuration } from '@myorg/api-client';

const config = new Configuration({
  basePath: 'https://api.example.com/v1',
  accessToken: 'your-token'
});

const usersApi = new UsersApi(config);

// List users
const { data, meta } = await usersApi.listUsers({ page: 1, perPage: 20 });

// Create user
const newUser = await usersApi.createUser({
  createUserInput: {
    email: 'new@example.com',
    password: 'SecurePass123!'
  }
});

// Get user
const user = await usersApi.getUser({ userId: 'uuid-here' });
```

### Step 7: Validate Implementation Against Contract

**Dredd (contract testing):**

```yaml
# dredd.yml
dry-run: false
hookfiles: ./tests/dredd-hooks.js
language: nodejs
server: npm start
endpoint: http://localhost:3000
path:
  - ./openapi.yaml
```

```javascript
// tests/dredd-hooks.js
const hooks = require('hooks');
const jwt = require('jsonwebtoken');

let stash = {};

hooks.beforeAll((transactions, done) => {
  stash.token = jwt.sign({ sub: 'test-user' }, process.env.JWT_SECRET);
  done();
});

hooks.beforeEach((transaction, done) => {
  transaction.request.headers['Authorization'] = `Bearer ${stash.token}`;
  done();
});

// Prepare test data
hooks.before('Users > Create User', (transaction, done) => {
  transaction.request.body = JSON.stringify({
    email: `test-${Date.now()}@example.com`,
    password: 'SecurePass123!'
  });
  done();
});

hooks.after('Users > Create User', (transaction, done) => {
  const response = JSON.parse(transaction.real.body);
  stash.userId = response.data.id;
  done();
});

hooks.before('Users > Get User', (transaction, done) => {
  transaction.fullPath = `/api/v1/users/${stash.userId}`;
  done();
});
```

```bash
# Run validation
dredd
```

**Spectral (OpenAPI linting):**

```yaml
# .spectral.yaml
extends: spectral:oas
rules:
  operation-operationId: error
  operation-tags: error
  oas3-api-servers: error

  # Custom rules
  must-have-examples:
    description: Responses must have examples
    given: $.paths.*.*.responses.*.content.application/json
    then:
      field: example
      function: truthy
```

```bash
spectral lint openapi.yaml
```

### Step 8: Set Up CI Pipeline

```yaml
# .github/workflows/api-contract.yml
name: API Contract

on:
  push:
    paths:
      - 'openapi.yaml'
      - 'server/**'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint OpenAPI spec
        uses: stoplightio/spectral-action@v0.8.10
        with:
          file_glob: 'openapi.yaml'

  validate:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - name: Start server
        run: |
          npm install
          npm start &
          sleep 10

      - name: Run contract tests
        run: npx dredd

  generate:
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v4

      - name: Generate TypeScript client
        run: |
          npx @openapitools/openapi-generator-cli generate \
            -i openapi.yaml \
            -g typescript-fetch \
            -o ./sdk/typescript

      - name: Publish SDK
        run: |
          cd ./sdk/typescript
          npm publish
        env:
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

## Templates

### Contract-First Workflow

```markdown
## API Development Workflow

### 1. Design Phase
- [ ] Write OpenAPI spec
- [ ] Review with stakeholders
- [ ] Get approval

### 2. Mock Phase
- [ ] Start mock server
- [ ] Frontend development begins
- [ ] Test integrations with mocks

### 3. Implementation Phase
- [ ] Generate server stubs
- [ ] Implement business logic
- [ ] Write unit tests

### 4. Validation Phase
- [ ] Run contract tests (Dredd)
- [ ] Verify against spec
- [ ] Fix discrepancies

### 5. Release Phase
- [ ] Generate client SDKs
- [ ] Update documentation
- [ ] Deploy
```

### Spec Review Template

```markdown
## API Spec Review: {API Name} v{version}

**Reviewer:** {name}
**Date:** {date}

### Endpoints
| Endpoint | Status | Notes |
|----------|--------|-------|
| GET /users | Approved | |
| POST /users | Needs change | Add rate limiting note |

### Schemas
| Schema | Status | Notes |
|--------|--------|-------|
| User | Approved | |
| CreateUserInput | Approved | |

### Security
- [ ] Authentication documented
- [ ] Rate limiting specified
- [ ] Sensitive data identified

### Compatibility
- [ ] No breaking changes
- [ ] Migration path documented

### Decision
- [ ] Approved
- [ ] Approved with changes
- [ ] Rejected

**Comments:**
{comments}
```

---

## Examples

### Full Contract-First Project Structure

```
my-api/
├── openapi.yaml              # Source of truth
├── .spectral.yaml            # Linting rules
├── dredd.yml                 # Contract test config
│
├── server/                   # Backend implementation
│   ├── src/
│   │   ├── routes/
│   │   ├── services/
│   │   └── models/
│   └── tests/
│       └── dredd-hooks.js
│
├── sdk/                      # Generated clients
│   ├── typescript/
│   ├── python/
│   └── go/
│
├── mock/                     # Mock server
│   └── server.js
│
└── docs/                     # Generated docs
    └── index.html
```

---

## Common Mistakes

1. **Modifying spec to match code**
   - Spec should drive code, not vice versa
   - Fix code to match spec

2. **Skipping mock phase**
   - Frontend still blocked
   - Always provide mocks first

3. **No contract validation**
   - Spec and code drift apart
   - Run Dredd in CI

4. **Overly detailed initial spec**
   - Analysis paralysis
   - Start minimal, iterate

5. **Not versioning the spec**
   - Breaking changes untracked
   - Use Git, semantic versioning

---

## Next Steps

1. **Write your OpenAPI spec** - Before any code
2. **Set up mock server** - Enable parallel development
3. **Generate server stubs** - Fast implementation start
4. **Add contract tests** - Validate continuously
5. **Generate SDKs** - Distribute to clients

---

## Related Methodologies

- [M-API-004: OpenAPI Specification](./M-API-004_openapi_specification.md)
- [M-API-008: API Documentation](./M-API-008_api_documentation.md)
- [M-API-009: API Testing](./M-API-009_api_testing.md)

---

*Methodology: Contract-First Development*
*Version: 1.0*
*Agent: faion-api-agent*
