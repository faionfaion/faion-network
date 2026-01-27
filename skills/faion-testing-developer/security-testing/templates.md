# Security Testing Templates

Copy-paste templates for security tests, CI/CD configurations, and tool setups.

---

## CI/CD Pipeline Templates

### GitHub Actions - Complete Security Workflow

```yaml
# .github/workflows/security.yml
name: Security Scanning

on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6 AM

jobs:
  # =====================
  # SAST - Static Analysis
  # =====================
  sast:
    name: Static Analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Semgrep - Multi-language SAST
      - name: Semgrep
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten
            p/python
            p/javascript

      # Bandit - Python SAST
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r src/ -f json -o bandit-report.json -ll || true
          bandit -r src/ -f txt -ll

      - name: Upload Bandit Report
        uses: actions/upload-artifact@v4
        with:
          name: bandit-report
          path: bandit-report.json

  # =====================
  # Secret Detection
  # =====================
  secrets:
    name: Secret Scanning
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for secret scanning

      # TruffleHog
      - name: TruffleHog
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified

      # Gitleaks
      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # =====================
  # Dependency Scanning
  # =====================
  dependencies:
    name: Dependency Scanning
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Python dependencies
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Python Dependency Audit
        run: |
          pip install pip-audit safety
          pip-audit -r requirements.txt || true
          safety check -r requirements.txt --json > safety-report.json || true

      # Node.js dependencies
      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: npm audit
        run: |
          npm ci
          npm audit --json > npm-audit.json || true

      # Snyk (if configured)
      - name: Snyk
        uses: snyk/actions/node@master
        continue-on-error: true
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Upload Reports
        uses: actions/upload-artifact@v4
        with:
          name: dependency-reports
          path: |
            safety-report.json
            npm-audit.json

  # =====================
  # DAST - Dynamic Testing
  # =====================
  dast:
    name: Dynamic Testing
    runs-on: ubuntu-latest
    if: github.event_name != 'pull_request'  # Only on main/develop
    steps:
      - uses: actions/checkout@v4

      - name: Start Application
        run: |
          docker-compose up -d
          sleep 30  # Wait for app to start

      - name: OWASP ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.10.0
        with:
          target: 'http://localhost:8000'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'

      - name: OWASP ZAP Full Scan
        uses: zaproxy/action-full-scan@v0.8.0
        with:
          target: 'http://localhost:8000'
        continue-on-error: true

      - name: Stop Application
        run: docker-compose down

  # =====================
  # Container Scanning
  # =====================
  container:
    name: Container Scanning
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker Image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Trivy Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload Trivy Report
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

---

### Pre-commit Hooks Configuration

```yaml
# .pre-commit-config.yaml
repos:
  # Secret Detection
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package-lock.json|yarn.lock

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  # Python Security
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.7
    hooks:
      - id: bandit
        args: ['-ll', '-x', 'tests/']

  # General Linting
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: detect-private-key
      - id: check-merge-conflict
      - id: no-commit-to-branch
        args: ['--branch', 'main']

  # Semgrep
  - repo: https://github.com/semgrep/semgrep
    rev: v1.52.0
    hooks:
      - id: semgrep
        args: ['--config', 'auto', '--error']
```

---

## Tool Configuration Templates

### Bandit Configuration

```yaml
# .bandit.yaml
skips: []

exclude_dirs:
  - tests
  - venv
  - .venv
  - node_modules
  - migrations

# All security tests
tests:
  # Assertions
  - B101  # assert_used

  # Dangerous functions
  - B102  # exec_used
  - B307  # eval

  # Hardcoded credentials
  - B104  # hardcoded_bind_all_interfaces
  - B105  # hardcoded_password_string
  - B106  # hardcoded_password_funcarg
  - B107  # hardcoded_password_default
  - B108  # hardcoded_tmp_directory

  # Cryptography
  - B303  # md5
  - B304  # des
  - B305  # cipher
  - B324  # hashlib_insecure_functions

  # Injection
  - B608  # hardcoded_sql_expressions
  - B602  # subprocess_popen_with_shell_equals_true
  - B603  # subprocess_without_shell_equals_true
  - B604  # any_other_function_with_shell_equals_true

  # Pickle/serialization
  - B301  # pickle
  - B302  # marshal

  # SSL/TLS
  - B501  # request_with_no_cert_validation
  - B502  # ssl_with_bad_version
  - B503  # ssl_with_bad_defaults

  # Flask/Django
  - B201  # flask_debug_true
  - B308  # mark_safe
  - B701  # jinja2_autoescape_false
  - B703  # django_mark_safe

  # Network
  - B310  # urllib_urlopen
  - B321  # ftplib
  - B323  # unverified_context

  # Random
  - B311  # random (use secrets module instead)
```

---

### Semgrep Configuration

```yaml
# .semgrep.yaml
rules:
  - id: hardcoded-secret
    patterns:
      - pattern-either:
          - pattern: |
              $KEY = "..."
          - pattern: |
              $KEY = '...'
    pattern-where-python: |
      import re
      key_name = str(metavars.get("$KEY", "")).lower()
      secret_patterns = ["password", "secret", "api_key", "apikey", "token", "credential"]
      return any(p in key_name for p in secret_patterns)
    message: Hardcoded secret detected
    severity: ERROR
    languages:
      - python
      - javascript
      - typescript

  - id: sql-injection
    patterns:
      - pattern-either:
          - pattern: |
              $CURSOR.execute(f"... {$USER_INPUT} ...")
          - pattern: |
              $CURSOR.execute("..." + $USER_INPUT + "...")
    message: Potential SQL injection vulnerability
    severity: ERROR
    languages:
      - python

  - id: command-injection
    patterns:
      - pattern-either:
          - pattern: |
              subprocess.run(..., shell=True, ...)
          - pattern: |
              os.system($CMD)
    message: Potential command injection - avoid shell=True
    severity: WARNING
    languages:
      - python
```

---

### OWASP ZAP Configuration

```yaml
# .zap/automation.yaml
env:
  contexts:
    - name: "Default Context"
      urls:
        - "https://localhost:8000"
      includePaths:
        - "https://localhost:8000/.*"
      excludePaths:
        - "https://localhost:8000/logout"
      authentication:
        method: "form"
        parameters:
          loginUrl: "https://localhost:8000/login"
          loginRequestData: "username={%username%}&password={%password%}"
        verification:
          method: "response"
          pattern: "Logout"
      users:
        - name: "test-user"
          credentials:
            username: "testuser"
            password: "testpass123"

jobs:
  - type: spider
    parameters:
      context: "Default Context"
      maxDuration: 10
      maxDepth: 5

  - type: spiderAjax
    parameters:
      context: "Default Context"
      maxDuration: 5

  - type: passiveScan-wait
    parameters:
      maxDuration: 5

  - type: activeScan
    parameters:
      context: "Default Context"
      policy: "Default Policy"
      maxRuleDurationInMins: 5

  - type: report
    parameters:
      template: "traditional-html"
      reportFile: "zap-report.html"
      reportTitle: "Security Scan Report"
```

```tsv
# .zap/rules.tsv
# Rule ID	Action	Description
10021	IGNORE	X-Content-Type-Options Header Missing (handled by CDN)
10038	IGNORE	Content Security Policy (CSP) Header Not Set (set in production)
10098	IGNORE	Cross-Domain Misconfiguration (expected for API)
```

---

### TruffleHog Configuration

```yaml
# .trufflehog.yaml
detectors:
  - name: aws
    verify: true
  - name: stripe
    verify: true
  - name: github
    verify: true
  - name: slack
    verify: true
  - name: twilio
    verify: true

exclude:
  paths:
    - "*.test.js"
    - "*.spec.ts"
    - "test/**"
    - "tests/**"
    - "node_modules/**"
    - "vendor/**"
    - ".git/**"
  detectors:
    - generic  # High false positive rate

entropy:
  enabled: true
  threshold: 4.5
```

---

### Gitleaks Configuration

```toml
# .gitleaks.toml
title = "Gitleaks Configuration"

[allowlist]
description = "Global allow list"
paths = [
    '''node_modules''',
    '''vendor''',
    '''\.git''',
    '''test.*\.py$''',
    '''.*_test\.go$''',
    '''\.test\.ts$''',
]

[[rules]]
id = "aws-access-key"
description = "AWS Access Key ID"
regex = '''AKIA[0-9A-Z]{16}'''
tags = ["aws", "credentials"]

[[rules]]
id = "aws-secret-key"
description = "AWS Secret Access Key"
regex = '''(?i)aws_secret_access_key\s*=\s*['\"]?([A-Za-z0-9/+=]{40})['\"]?'''
tags = ["aws", "credentials"]

[[rules]]
id = "github-token"
description = "GitHub Token"
regex = '''ghp_[a-zA-Z0-9]{36}'''
tags = ["github", "token"]

[[rules]]
id = "generic-api-key"
description = "Generic API Key"
regex = '''(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]?([a-zA-Z0-9]{32,})['\"]?'''
tags = ["api", "key"]
```

---

## Python Test Templates

### pytest Security Test Fixture

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.models import User
from app.auth import create_access_token

@pytest.fixture
def client():
    """Synchronous test client."""
    return TestClient(app)

@pytest.fixture
async def async_client():
    """Async test client for concurrent tests."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def test_user(db_session):
    """Create a regular test user."""
    user = User(
        email="testuser@example.com",
        password_hash="$argon2id$v=19$m=65536,t=3,p=4$..."
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def admin_user(db_session):
    """Create an admin test user."""
    user = User(
        email="admin@example.com",
        password_hash="$argon2id$v=19$m=65536,t=3,p=4$...",
        is_admin=True
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def user_token(test_user):
    """JWT token for regular user."""
    return create_access_token({"sub": test_user.id})

@pytest.fixture
def admin_token(admin_user):
    """JWT token for admin user."""
    return create_access_token({"sub": admin_user.id})

@pytest.fixture
def auth_headers(user_token):
    """Authorization headers for regular user."""
    return {"Authorization": f"Bearer {user_token}"}
```

---

### OWASP Top 10 Test Template

```python
# tests/security/test_owasp_top10.py
import pytest
from fastapi.testclient import TestClient

class TestBrokenAccessControl:
    """A01:2025 - Broken Access Control"""

    def test_user_cannot_access_other_user_data(self, client, user_token, other_user):
        """Horizontal privilege escalation should be blocked."""
        response = client.get(
            f"/api/users/{other_user.id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 403

    def test_user_cannot_access_admin_endpoints(self, client, user_token):
        """Vertical privilege escalation should be blocked."""
        admin_endpoints = [
            "/api/admin/users",
            "/api/admin/settings",
            "/api/admin/audit-logs",
        ]
        for endpoint in admin_endpoints:
            response = client.get(
                endpoint,
                headers={"Authorization": f"Bearer {user_token}"}
            )
            assert response.status_code == 403

    def test_ssrf_blocked(self, client, auth_headers):
        """SSRF attacks should be prevented."""
        ssrf_payloads = [
            "http://169.254.169.254/latest/meta-data/",
            "http://localhost:22",
            "http://127.0.0.1:8080/admin",
            "http://[::1]/",
            "file:///etc/passwd",
        ]
        for payload in ssrf_payloads:
            response = client.post(
                "/api/fetch-url",
                json={"url": payload},
                headers=auth_headers
            )
            assert response.status_code in [400, 403]


class TestSecurityMisconfiguration:
    """A02:2025 - Security Misconfiguration"""

    def test_debug_mode_disabled(self, client):
        """Debug endpoints should not be accessible in production."""
        debug_endpoints = [
            "/_debug/",
            "/debug/",
            "/__debug__/",
            "/api/debug",
        ]
        for endpoint in debug_endpoints:
            response = client.get(endpoint)
            assert response.status_code in [404, 403]

    def test_security_headers_present(self, client):
        """Security headers should be present."""
        response = client.get("/")
        headers = response.headers

        assert headers.get("X-Content-Type-Options") == "nosniff"
        assert headers.get("X-Frame-Options") in ["DENY", "SAMEORIGIN"]
        assert "Strict-Transport-Security" in headers

    def test_error_messages_dont_leak_info(self, client):
        """Error responses should not expose internal details."""
        response = client.get("/api/nonexistent-endpoint")
        assert "traceback" not in response.text.lower()
        assert "stack" not in response.text.lower()
        assert "exception" not in response.text.lower()


class TestInjection:
    """A05:2025 - Injection"""

    @pytest.mark.parametrize("payload", [
        "'; DROP TABLE users;--",
        "' OR '1'='1",
        "admin'--",
        "1; SELECT * FROM users",
        "' UNION SELECT password FROM users--",
    ])
    def test_sql_injection_prevented(self, client, payload, auth_headers):
        """SQL injection should be prevented."""
        response = client.get(
            f"/api/users?search={payload}",
            headers=auth_headers
        )
        assert response.status_code in [200, 400]

    @pytest.mark.parametrize("payload", [
        "<script>alert('xss')</script>",
        "<img src=x onerror=alert(1)>",
        "javascript:alert('xss')",
        "<svg onload=alert(1)>",
    ])
    def test_xss_prevented(self, client, payload, auth_headers):
        """XSS should be prevented."""
        response = client.post(
            "/api/comments",
            json={"content": payload},
            headers=auth_headers
        )
        if response.status_code == 201:
            content = response.json().get("content", "")
            assert "<script>" not in content
            assert "onerror=" not in content.lower()


class TestAuthenticationFailures:
    """A07:2025 - Authentication Failures"""

    def test_brute_force_protection(self, client):
        """Account should be protected from brute force."""
        for _ in range(10):
            response = client.post("/api/auth/login", json={
                "email": "user@example.com",
                "password": "wrongpassword"
            })

        # Should be rate limited or locked
        assert response.status_code in [429, 423]

    def test_session_invalidated_on_logout(self, client, user_token):
        """Tokens should be invalidated on logout."""
        # Logout
        client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {user_token}"}
        )

        # Old token should not work
        response = client.get(
            "/api/me",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 401

    def test_weak_passwords_rejected(self, client):
        """Weak passwords should be rejected."""
        weak_passwords = [
            "123456",
            "password",
            "12345678",
            "qwerty",
            "abc123",
        ]
        for password in weak_passwords:
            response = client.post("/api/auth/register", json={
                "email": f"test{password}@example.com",
                "password": password
            })
            assert response.status_code == 400
```

---

### Input Validation Test Template

```python
# tests/security/test_input_validation.py
import pytest

class TestInputValidation:
    """Input validation security tests."""

    @pytest.mark.parametrize("email", [
        "not-an-email",
        "@nodomain.com",
        "spaces in@email.com",
        "a" * 256 + "@example.com",
        "<script>@example.com",
        "user@<script>.com",
    ])
    def test_invalid_email_rejected(self, client, email):
        """Invalid email formats should be rejected."""
        response = client.post("/api/auth/register", json={
            "email": email,
            "password": "ValidPassword123!"
        })
        assert response.status_code == 400

    @pytest.mark.parametrize("path", [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32",
        "....//....//etc/passwd",
        "%2e%2e%2f%2e%2e%2fetc/passwd",
        "..%c0%af..%c0%afetc/passwd",
    ])
    def test_path_traversal_prevented(self, client, path, auth_headers):
        """Path traversal should be prevented."""
        response = client.get(
            f"/api/files/{path}",
            headers=auth_headers
        )
        assert response.status_code in [400, 404]

    def test_file_upload_type_validation(self, client, auth_headers):
        """Only allowed file types should be accepted."""
        dangerous_files = [
            ("malware.exe", b"MZ...", "application/x-msdownload"),
            ("shell.php", b"<?php system($_GET['cmd']); ?>", "application/x-php"),
            ("script.js", b"alert('xss')", "application/javascript"),
        ]
        for filename, content, mimetype in dangerous_files:
            response = client.post(
                "/api/upload",
                files={"file": (filename, content, mimetype)},
                headers=auth_headers
            )
            assert response.status_code == 400

    def test_file_upload_size_limit(self, client, auth_headers):
        """Large files should be rejected."""
        large_content = b"x" * (10 * 1024 * 1024 + 1)  # > 10MB
        response = client.post(
            "/api/upload",
            files={"file": ("large.txt", large_content, "text/plain")},
            headers=auth_headers
        )
        assert response.status_code == 413


class TestRateLimiting:
    """Rate limiting security tests."""

    @pytest.mark.asyncio
    async def test_api_rate_limiting(self, async_client):
        """API should enforce rate limits."""
        import asyncio

        tasks = [async_client.get("/api/public") for _ in range(100)]
        responses = await asyncio.gather(*tasks)

        rate_limited = sum(1 for r in responses if r.status_code == 429)
        assert rate_limited > 0, "Rate limiting not enforced"

    @pytest.mark.asyncio
    async def test_login_strict_rate_limiting(self, async_client):
        """Login should have strict rate limits."""
        responses = []
        for _ in range(20):
            response = await async_client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "wrong"
            })
            responses.append(response.status_code)

        assert 429 in responses, "Login rate limiting too permissive"
```

---

### Secret Detection Test Template

```python
# tests/security/test_secrets.py
import re
from pathlib import Path

SECRET_PATTERNS = [
    (r'api[_-]?key\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', "API key"),
    (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
    (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
    (r'aws_access_key_id\s*=\s*["\']AKIA[A-Z0-9]{16}["\']', "AWS Access Key"),
    (r'aws_secret_access_key\s*=\s*["\'][A-Za-z0-9/+=]{40}["\']', "AWS Secret Key"),
    (r'-----BEGIN (RSA |EC )?PRIVATE KEY-----', "Private key"),
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub Personal Access Token"),
    (r'sk_live_[a-zA-Z0-9]{24}', "Stripe Live Key"),
]

EXCLUDE_PATTERNS = [
    r'.*test.*\.py$',
    r'.*_test\.go$',
    r'.*\.test\.ts$',
    r'.*/tests/.*',
    r'.*/node_modules/.*',
]


def should_scan_file(file_path: str) -> bool:
    """Check if file should be scanned."""
    for pattern in EXCLUDE_PATTERNS:
        if re.match(pattern, file_path):
            return False
    return True


def test_no_secrets_in_source_code():
    """Ensure no secrets are hardcoded in source files."""
    source_dir = Path("src")
    violations = []

    for ext in ["*.py", "*.js", "*.ts", "*.go", "*.java"]:
        for file_path in source_dir.rglob(ext):
            if not should_scan_file(str(file_path)):
                continue

            content = file_path.read_text()
            for pattern, secret_type in SECRET_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):
                    violations.append(f"{file_path}: {secret_type}")

    assert not violations, f"Secrets found in code:\n" + "\n".join(violations)


def test_no_secrets_in_config_files():
    """Config files should not contain secrets."""
    config_files = [
        "config.py",
        "settings.py",
        ".env.example",
        "config.yaml",
        "config.json",
    ]

    for config_file in config_files:
        path = Path(config_file)
        if not path.exists():
            continue

        content = path.read_text()
        for pattern, secret_type in SECRET_PATTERNS:
            match = re.search(pattern, content, re.IGNORECASE)
            assert not match, f"{config_file} contains {secret_type}"
```

---

## JavaScript/TypeScript Test Templates

### Jest Security Test Template

```typescript
// tests/security/auth.test.ts
import request from 'supertest';
import app from '../../src/app';

describe('Authentication Security', () => {
    describe('Brute Force Protection', () => {
        it('should rate limit after multiple failed attempts', async () => {
            const attempts = Array(10).fill(null);

            for (const _ of attempts) {
                await request(app)
                    .post('/api/auth/login')
                    .send({ email: 'user@example.com', password: 'wrong' });
            }

            const response = await request(app)
                .post('/api/auth/login')
                .send({ email: 'user@example.com', password: 'wrong' });

            expect([429, 423]).toContain(response.status);
        });
    });

    describe('Session Security', () => {
        it('should invalidate session on logout', async () => {
            // Login first
            const loginRes = await request(app)
                .post('/api/auth/login')
                .send({ email: 'test@example.com', password: 'password123' });

            const token = loginRes.body.token;

            // Logout
            await request(app)
                .post('/api/auth/logout')
                .set('Authorization', `Bearer ${token}`);

            // Try to use old token
            const response = await request(app)
                .get('/api/me')
                .set('Authorization', `Bearer ${token}`);

            expect(response.status).toBe(401);
        });
    });
});

describe('Access Control', () => {
    let userToken: string;
    let adminToken: string;
    let otherUserId: string;

    beforeAll(async () => {
        // Setup tokens
    });

    it('should prevent horizontal privilege escalation', async () => {
        const response = await request(app)
            .get(`/api/users/${otherUserId}`)
            .set('Authorization', `Bearer ${userToken}`);

        expect(response.status).toBe(403);
    });

    it('should prevent vertical privilege escalation', async () => {
        const response = await request(app)
            .get('/api/admin/users')
            .set('Authorization', `Bearer ${userToken}`);

        expect(response.status).toBe(403);
    });

    it('should block admin endpoints without admin role', async () => {
        const adminEndpoints = [
            '/api/admin/users',
            '/api/admin/settings',
            '/api/admin/audit-logs',
        ];

        for (const endpoint of adminEndpoints) {
            const response = await request(app)
                .get(endpoint)
                .set('Authorization', `Bearer ${userToken}`);

            expect(response.status).toBe(403);
        }
    });
});

describe('Injection Prevention', () => {
    const sqlPayloads = [
        "'; DROP TABLE users;--",
        "' OR '1'='1",
        "admin'--",
        "1; SELECT * FROM users",
    ];

    const xssPayloads = [
        "<script>alert('xss')</script>",
        "<img src=x onerror=alert(1)>",
        "javascript:alert('xss')",
    ];

    it.each(sqlPayloads)('should prevent SQL injection: %s', async (payload) => {
        const response = await request(app)
            .get('/api/users')
            .query({ search: payload });

        expect([200, 400]).toContain(response.status);
    });

    it.each(xssPayloads)('should prevent XSS: %s', async (payload) => {
        const response = await request(app)
            .post('/api/comments')
            .set('Authorization', `Bearer ${userToken}`)
            .send({ content: payload });

        if (response.status === 201) {
            expect(response.body.content).not.toContain('<script>');
            expect(response.body.content.toLowerCase()).not.toContain('onerror=');
        }
    });
});

describe('Security Headers', () => {
    it('should have required security headers', async () => {
        const response = await request(app).get('/');

        expect(response.headers['x-content-type-options']).toBe('nosniff');
        expect(['DENY', 'SAMEORIGIN']).toContain(response.headers['x-frame-options']);
        expect(response.headers['strict-transport-security']).toBeDefined();
    });
});
```

---

## Dependency Scanning Script Template

```python
#!/usr/bin/env python3
# scripts/check_dependencies.py
"""Dependency vulnerability scanner."""

import subprocess
import json
import sys
from typing import List, Dict, Any

def run_safety_check() -> List[Dict[str, Any]]:
    """Check Python dependencies with Safety."""
    result = subprocess.run(
        ["safety", "check", "--json"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return []
    return []


def run_pip_audit() -> List[Dict[str, Any]]:
    """Check Python dependencies with pip-audit."""
    result = subprocess.run(
        ["pip-audit", "--format", "json"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return []
    return []


def run_npm_audit() -> Dict[str, Any]:
    """Check Node.js dependencies with npm audit."""
    result = subprocess.run(
        ["npm", "audit", "--json"],
        capture_output=True,
        text=True
    )

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}


def format_vulnerability(vuln: Dict[str, Any]) -> str:
    """Format vulnerability for display."""
    return f"  - {vuln.get('package_name', 'unknown')}: {vuln.get('vulnerability_id', 'unknown')}"


def main():
    """Run all dependency checks."""
    print("=" * 60)
    print("Dependency Vulnerability Scan")
    print("=" * 60)

    critical_found = False

    # Python checks
    print("\n[Python - Safety]")
    safety_vulns = run_safety_check()
    if safety_vulns:
        print(f"Found {len(safety_vulns)} vulnerabilities:")
        for vuln in safety_vulns:
            print(format_vulnerability(vuln))
            if vuln.get("severity", "").lower() == "critical":
                critical_found = True
    else:
        print("No vulnerabilities found.")

    print("\n[Python - pip-audit]")
    audit_vulns = run_pip_audit()
    if audit_vulns:
        print(f"Found {len(audit_vulns)} vulnerable packages:")
        for pkg in audit_vulns:
            print(f"  - {pkg['name']} {pkg['version']}")
            for vuln in pkg.get('vulns', []):
                print(f"    {vuln['id']}: {vuln.get('description', '')[:80]}...")
    else:
        print("No vulnerabilities found.")

    # Node.js checks
    print("\n[Node.js - npm audit]")
    npm_result = run_npm_audit()
    if npm_result.get("vulnerabilities"):
        vuln_count = npm_result.get("metadata", {}).get("vulnerabilities", {})
        print(f"Found vulnerabilities: {vuln_count}")
        if vuln_count.get("critical", 0) > 0:
            critical_found = True
    else:
        print("No vulnerabilities found.")

    print("\n" + "=" * 60)
    if critical_found:
        print("CRITICAL VULNERABILITIES FOUND - Fix before deployment!")
        sys.exit(1)
    else:
        print("Scan complete.")
        sys.exit(0)


if __name__ == "__main__":
    main()
```

---

*These templates provide a starting point for security testing. Customize based on your application's specific requirements and risk profile.*
