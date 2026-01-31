# REST API Design Checklist

Step-by-step checklist for designing RESTful APIs.

## Phase 1: Resource Design

### Resource Identification

- [ ] **Identify core resources**
  - [ ] List main business entities
  - [ ] Map entities to URL paths
  - [ ] Use plural nouns (`/users`, not `/user`)
  - [ ] Use lowercase with hyphens (`/user-profiles`)

- [ ] **Define resource relationships**
  - [ ] Identify parent-child relationships
  - [ ] Decide on nesting depth (max 2-3 levels)
  - [ ] Document sub-resources (`/users/{id}/orders`)

### URL Structure

- [ ] **Standard CRUD operations**
  - [ ] GET collection: `GET /resources`
  - [ ] GET single: `GET /resources/{id}`
  - [ ] Create: `POST /resources`
  - [ ] Update: `PUT/PATCH /resources/{id}`
  - [ ] Delete: `DELETE /resources/{id}`

- [ ] **Query parameters**
  - [ ] Filtering: `?status=active`
  - [ ] Sorting: `?sort=-created_at`
  - [ ] Pagination: `?page=1&limit=20`
  - [ ] Field selection: `?fields=id,name`

## Phase 2: HTTP Methods

### Method Selection

- [ ] **GET** - Read operations only
  - [ ] No side effects
  - [ ] Cacheable responses
  - [ ] Query params for filtering

- [ ] **POST** - Create new resources
  - [ ] Return 201 with Location header
  - [ ] Return created resource in body
  - [ ] Idempotency key for retries (optional)

- [ ] **PUT** - Full replacement
  - [ ] Require complete resource representation
  - [ ] Return 200 with updated resource

- [ ] **PATCH** - Partial update
  - [ ] Only changed fields required
  - [ ] Support JSON Merge Patch or JSON Patch

- [ ] **DELETE** - Resource removal
  - [ ] Return 204 No Content
  - [ ] Soft delete vs hard delete decision

## Phase 3: Response Design

### Status Codes

- [ ] **Success codes**
  - [ ] 200 OK - GET, PUT, PATCH success
  - [ ] 201 Created - POST success
  - [ ] 204 No Content - DELETE success
  - [ ] 206 Partial Content - Pagination

- [ ] **Client error codes**
  - [ ] 400 Bad Request - Malformed syntax
  - [ ] 401 Unauthorized - Auth required
  - [ ] 403 Forbidden - No permission
  - [ ] 404 Not Found - Resource missing
  - [ ] 409 Conflict - State conflict
  - [ ] 422 Unprocessable - Validation error
  - [ ] 429 Too Many Requests - Rate limited

- [ ] **Server error codes**
  - [ ] 500 Internal Server Error
  - [ ] 503 Service Unavailable

### Response Body

- [ ] **Consistent envelope** (optional)
  - [ ] `{ "data": {...}, "meta": {...} }`
  - [ ] Or direct resource representation

- [ ] **Error responses**
  - [ ] Error code
  - [ ] Human-readable message
  - [ ] Field-level errors for validation
  - [ ] Request ID for debugging

## Phase 4: Headers & Content Negotiation

### Request Headers

- [ ] `Content-Type: application/json`
- [ ] `Accept: application/json`
- [ ] `Authorization: Bearer {token}`
- [ ] `X-Request-ID` for tracing

### Response Headers

- [ ] `Content-Type: application/json`
- [ ] `Location` header for 201
- [ ] `X-Request-ID` echo
- [ ] Cache-Control for GET responses
- [ ] Rate limit headers (X-RateLimit-*)

## Phase 5: Documentation

- [ ] **OpenAPI spec**
  - [ ] All endpoints documented
  - [ ] Request/response schemas
  - [ ] Example values
  - [ ] Error responses

- [ ] **Interactive docs**
  - [ ] Swagger UI or Redoc
  - [ ] Try-it-out functionality
  - [ ] Authentication setup

## Phase 6: Testing

- [ ] **Contract tests**
  - [ ] Schema validation
  - [ ] Required fields
  - [ ] Status codes

- [ ] **Integration tests**
  - [ ] Happy path scenarios
  - [ ] Error scenarios
  - [ ] Auth flows

---

## Quick Reference

| Action | Method | Path | Response |
|--------|--------|------|----------|
| List | GET | /resources | 200 + array |
| Get one | GET | /resources/{id} | 200 + object |
| Create | POST | /resources | 201 + object |
| Replace | PUT | /resources/{id} | 200 + object |
| Update | PATCH | /resources/{id} | 200 + object |
| Delete | DELETE | /resources/{id} | 204 |

---

*REST API Design Checklist v1.0*
