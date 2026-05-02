---
name: api-key-auth
description: Generate cryptographically strong API keys, store them hashed, and protect endpoints with Bearer middleware — no third-party auth service required.
tier: solo
group: api-design
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working API key authentication system: a generation endpoint that issues keys once (shown to the user, never stored), a hashed store in your database, and middleware that validates `Authorization: Bearer <key>` on every protected route — in Python (FastAPI/Flask) or Node.js (Express).

## Prerequisites

- Python 3.10+ **or** Node.js 18+ project with an existing HTTP framework (FastAPI, Flask, or Express).
- A running database (SQLite, PostgreSQL, or MySQL) — any ORM or raw driver works.
- `pip` or `npm` available; no external auth service account required.
- Basic familiarity with HTTP middleware / dependency injection patterns.

## Steps

1. **Add the key-generation utility to your project.**

   Python — add `utils/api_keys.py`:

   ```python
   import secrets
   import hashlib

   def generate_api_key() -> tuple[str, str]:
       """Return (raw_key, sha256_hex). Store only the hash."""
       raw = secrets.token_urlsafe(32)          # 256-bit entropy, URL-safe base64
       hashed = hashlib.sha256(raw.encode()).hexdigest()
       return raw, hashed
   ```

   Node.js — add `utils/apiKeys.js`:

   ```js
   const { randomBytes, createHash } = require('crypto')

   function generateApiKey() {
     const raw = randomBytes(32).toString('hex')        // 64-char hex string
     const hashed = createHash('sha256').update(raw).digest('hex')
     return { raw, hashed }
   }

   module.exports = { generateApiKey }
   ```

2. **Create the `api_keys` table in your database.**

   SQL (works for SQLite, PostgreSQL, MySQL):

   ```sql
   CREATE TABLE api_keys (
     id          INTEGER PRIMARY KEY AUTOINCREMENT,
     owner_id    INTEGER NOT NULL,
     key_hash    CHAR(64) NOT NULL UNIQUE,  -- sha256 hex
     name        VARCHAR(120),              -- human label ("prod", "ci")
     created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     last_used   TIMESTAMP,
     revoked     BOOLEAN DEFAULT FALSE
   );
   CREATE INDEX idx_api_keys_hash ON api_keys (key_hash);
   ```

3. **Build the key-issuance endpoint — show the raw key once, store only the hash.**

   Python / FastAPI:

   ```python
   from fastapi import APIRouter, Depends
   from utils.api_keys import generate_api_key
   from db import get_db   # your DB session dependency

   router = APIRouter(prefix="/api/keys", tags=["api-keys"])

   @router.post("/")
   def create_key(name: str, owner_id: int, db=Depends(get_db)):
       raw, hashed = generate_api_key()
       db.execute(
           "INSERT INTO api_keys (owner_id, key_hash, name) VALUES (?, ?, ?)",
           (owner_id, hashed, name),
       )
       db.commit()
       # Return raw key ONCE — it cannot be recovered later
       return {"key": raw, "warning": "Save this key now; it will not be shown again."}
   ```

   Node.js / Express:

   ```js
   const { generateApiKey } = require('../utils/apiKeys')

   router.post('/api/keys', async (req, res) => {
     const { name, ownerId } = req.body
     const { raw, hashed } = generateApiKey()
     await db.run(
       'INSERT INTO api_keys (owner_id, key_hash, name) VALUES (?, ?, ?)',
       [ownerId, hashed, name]
     )
     res.json({ key: raw, warning: 'Save this key now; it will not be shown again.' })
   })
   ```

4. **Write the authentication middleware that checks `Authorization: Bearer <key>`.**

   Python / FastAPI (dependency):

   ```python
   import hashlib
   from fastapi import Header, HTTPException, Depends
   from db import get_db

   async def require_api_key(
       authorization: str = Header(...),
       db=Depends(get_db),
   ):
       if not authorization.startswith("Bearer "):
           raise HTTPException(status_code=401, detail="Missing Bearer token")
       raw_key = authorization.removeprefix("Bearer ").strip()
       key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
       row = db.execute(
           "SELECT id FROM api_keys WHERE key_hash = ? AND revoked = 0",
           (key_hash,),
       ).fetchone()
       if not row:
           raise HTTPException(status_code=401, detail="Invalid or revoked API key")
       db.execute(
           "UPDATE api_keys SET last_used = CURRENT_TIMESTAMP WHERE key_hash = ?",
           (key_hash,),
       )
       db.commit()
       return row["id"]
   ```

   Node.js / Express (middleware function):

   ```js
   const { createHash } = require('crypto')

   async function requireApiKey(req, res, next) {
     const auth = req.headers['authorization'] ?? ''
     if (!auth.startsWith('Bearer ')) {
       return res.status(401).json({ error: 'Missing Bearer token' })
     }
     const raw = auth.slice(7).trim()
     const hash = createHash('sha256').update(raw).digest('hex')
     const row = await db.get(
       'SELECT id FROM api_keys WHERE key_hash = ? AND revoked = 0',
       [hash]
     )
     if (!row) return res.status(401).json({ error: 'Invalid or revoked API key' })
     await db.run(
       'UPDATE api_keys SET last_used = CURRENT_TIMESTAMP WHERE key_hash = ?',
       [hash]
     )
     req.apiKeyId = row.id
     next()
   }

   module.exports = { requireApiKey }
   ```

5. **Apply the middleware to the routes you want to protect.**

   FastAPI — add `Depends(require_api_key)` to each protected route or router:

   ```python
   @router.get("/data", dependencies=[Depends(require_api_key)])
   def get_data():
       return {"status": "ok"}
   ```

   Express — mount before the route handler:

   ```js
   const { requireApiKey } = require('./middleware/apiKey')
   router.get('/data', requireApiKey, (req, res) => res.json({ status: 'ok' }))
   ```

6. **Add a revocation endpoint so keys can be invalidated without deleting history.**

   ```sql
   -- SQL you can wire to a DELETE /api/keys/:id endpoint
   UPDATE api_keys SET revoked = TRUE WHERE id = ? AND owner_id = ?;
   ```

   Keep revoked rows in the table for audit purposes; the `AND revoked = 0` clause in step 4 already blocks them.

## Verify

Issue a key from the creation endpoint, then call a protected route:

```bash
# 1. Issue a key (replace port and path to match your app)
KEY=$(curl -s -X POST http://localhost:8000/api/keys \
  -H "Content-Type: application/json" \
  -d '{"name":"smoke-test","owner_id":1}' | python3 -c "import sys,json; print(json.load(sys.stdin)['key'])")

# 2. Call a protected route with the key
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $KEY" \
  http://localhost:8000/data
```

Expected: the second command prints `200`. Call the same route without the header and confirm it returns `401`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Middleware always returns 401 even with a valid key | Key stored as plaintext by mistake | Check the `key_hash` column in the DB — it should be a 64-char hex string. If it contains the raw key, drop the table, fix the issuance endpoint to call `generate_api_key()` and re-issue. |
| `Authorization` header is `None` in FastAPI | Header name mismatch | FastAPI lowercases all header names. Declare `authorization: str = Header(...)` (lowercase). |
| Node `req.headers['authorization']` is `undefined` | Client sent `Authorization` (capital A) but Express lowercases keys | Express auto-lowercases all headers — check the client is actually sending the header. Use `curl -v` to inspect raw headers. |
| `last_used` never updates | DB session not committed after UPDATE | Call `db.commit()` (Python) or `await db.run()` (Node) immediately after the UPDATE statement in the middleware. |
| Timing attack concern on hash comparison | SHA-256 comparison is not constant-time in naive string equality | Use `hmac.compare_digest(stored_hash, computed_hash)` in Python; `crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b))` in Node instead of `==`. |

## Next

- Add rate limiting per `api_key_id` (see `rate-limiting` playbook) to prevent brute-force key enumeration.
- Scope your keys: add a `scopes` column (comma-separated or JSON array) and check required scopes in the middleware.
- Move to a dedicated secrets table with envelope encryption if you need GDPR-compliant key storage.

## References

- [knowledge/solo/dev/api-developer/api-authentication](../../../knowledge/solo/dev/api-developer/api-authentication) — the hashed-credential storage pattern and Bearer token contract that steps 1–4 implement directly; also covers the "show once" issuance constraint this playbook enforces.
- [knowledge/solo/dev/api-developer/api-rest-design](../../../knowledge/solo/dev/api-developer/api-rest-design) — guides the POST /api/keys resource shape and the 401/200 response contract that the Verify section validates.
