# AI-Assisted Specification Examples

> Real-world examples of AI-assisted specification writing patterns and outputs.

## Example 1: API Endpoint Specification

### Initial Prompt to AI

```markdown
I need to create a specification for a user authentication API endpoint.

**Context:**
- Product: SaaS platform for project management
- Target users: Enterprise teams (500+ users)
- Constraints: Must support SSO (SAML, OAuth), rate limiting, audit logging
- Existing stack: Django REST Framework, PostgreSQL, Redis

**Requirements:**
Generate a complete specification including:
1. Functional requirements (FR-X format)
2. Edge cases and error scenarios
3. Acceptance criteria (Given-When-Then)
4. API contract
```

### AI-Generated Specification

```markdown
# User Authentication API Specification

## Overview
REST API endpoint for user authentication supporting email/password
and SSO (SAML 2.0, OAuth 2.0) authentication methods.

## Functional Requirements

### FR-1: Email/Password Authentication
The system shall authenticate users via email and password,
returning a JWT token pair (access + refresh) on success.

### FR-2: SSO Authentication (SAML)
The system shall support SAML 2.0 SSO authentication flow,
redirecting to configured IdP and processing SAML assertions.

### FR-3: SSO Authentication (OAuth)
The system shall support OAuth 2.0 authentication with
configurable providers (Google, Microsoft, Okta).

### FR-4: Rate Limiting
The system shall limit authentication attempts to 5 per minute
per IP address to prevent brute force attacks.

### FR-5: Audit Logging
The system shall log all authentication attempts with timestamp,
IP address, user agent, and outcome (success/failure/reason).

### FR-6: Session Management
The system shall invalidate existing sessions when password
is changed or account is locked.

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Invalid email format | 400 Bad Request with validation error |
| User not found | 401 Unauthorized (generic message) |
| Wrong password | 401 Unauthorized (generic message) |
| Account locked | 403 Forbidden with lockout duration |
| Rate limit exceeded | 429 Too Many Requests with retry-after |
| SSO provider unavailable | 503 Service Unavailable with fallback |
| Expired SAML assertion | 401 Unauthorized, redirect to IdP |
| Missing required claims | 400 Bad Request with missing claims |

## Acceptance Criteria

### AC-1.1: Successful Email Login
**Given** a registered user with valid credentials
**When** they POST to /api/v1/auth/login with email and password
**Then** the response status is 200
**And** the response contains access_token and refresh_token
**And** access_token expires in 15 minutes
**And** an audit log entry is created with outcome "success"

### AC-1.2: Invalid Credentials
**Given** a registered user
**When** they POST to /api/v1/auth/login with wrong password
**Then** the response status is 401
**And** the response body is {"error": "Invalid credentials"}
**And** an audit log entry is created with outcome "invalid_password"

### AC-4.1: Rate Limiting
**Given** an IP address that has made 5 failed login attempts in 1 minute
**When** a 6th authentication request is made from that IP
**Then** the response status is 429
**And** the response includes header Retry-After: 60
**And** no authentication is attempted

### AC-5.1: Audit Logging
**Given** any authentication attempt (success or failure)
**When** the request is processed
**Then** an audit log entry is created containing:
  - timestamp (ISO 8601)
  - ip_address
  - user_agent
  - email (if provided)
  - outcome (success/failure)
  - failure_reason (if applicable)

## API Contract

### POST /api/v1/auth/login

**Request:**
```json
{
  "email": "user@example.com",
  "password": "string",
  "remember_me": false
}
```

**Success Response (200):**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 900,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Error Response (401):**
```json
{
  "error": "Invalid credentials",
  "error_code": "AUTH_INVALID_CREDENTIALS"
}
```

## Non-Goals (Explicitly Out of Scope)

- User registration (separate endpoint)
- Password reset (separate endpoint)
- Multi-factor authentication (Phase 2)
- Biometric authentication (not planned)
```

---

## Example 2: Feature Specification with User Stories

### Initial Prompt to AI

```markdown
Create a specification for a notification preferences feature.

**Context:**
- Users want granular control over notifications
- Current system sends all notifications (no preferences)
- Need to support email, in-app, and push channels
- Users complain about notification overload

**Ask clarifying questions before generating the spec.**
```

### AI Clarifying Questions

```markdown
Before I generate the specification, I need to understand:

1. **Notification Types**: What types of notifications exist?
   - Project updates, mentions, deadlines, comments, assignments?

2. **Granularity**: Should users control by:
   - Channel only (email on/off)?
   - Type only (mentions on/off)?
   - Channel + Type combination (mentions via email on/off)?

3. **Defaults**: What should the default preferences be?
   - All on? All off? Somewhere in between?

4. **Frequency**: Should users control frequency?
   - Immediate vs. digest (daily/weekly)?

5. **Scope**: Project-level or account-level preferences?
   - Can I mute notifications for specific projects?

6. **Do Not Disturb**: Should there be quiet hours?

7. **Team Admin Control**: Can admins override user preferences
   for critical notifications?
```

### User Answers

```markdown
1. Types: mentions, assignments, comments, deadlines, project updates
2. Granularity: Channel + Type combination
3. Defaults: All email on, in-app on, push off
4. Frequency: Immediate only for now, digest in Phase 2
5. Scope: Account-level for Phase 1, project-level later
6. DND: Yes, quiet hours feature
7. Admin: Yes, admins can mark certain notifications as "mandatory"
```

### AI-Generated User Stories

```markdown
# Notification Preferences - User Stories

## US-1: View Notification Preferences
**As a** platform user
**I want to** see my current notification preferences
**So that** I understand what notifications I'll receive

### Acceptance Criteria
- AC-1.1: Given I am logged in, when I navigate to Settings > Notifications,
  then I see a matrix of notification types vs channels
- AC-1.2: Given I view preferences, when the page loads,
  then my current preferences are pre-selected
- AC-1.3: Given I have never set preferences, when I view the page,
  then I see the default preferences (email: on, in-app: on, push: off)

## US-2: Update Notification Preferences
**As a** platform user
**I want to** toggle specific notification types per channel
**So that** I only receive notifications I care about

### Acceptance Criteria
- AC-2.1: Given I am on preferences page, when I toggle a preference,
  then the change is saved immediately (optimistic update)
- AC-2.2: Given I toggle a preference, when save fails,
  then the toggle reverts and I see an error message
- AC-2.3: Given an admin has marked a notification as mandatory,
  when I try to disable it, then I see "Required by admin" and cannot toggle

## US-3: Set Quiet Hours
**As a** platform user
**I want to** set quiet hours when I won't receive push notifications
**So that** I'm not disturbed outside work hours

### Acceptance Criteria
- AC-3.1: Given I set quiet hours 10pm-8am, when a notification triggers at 11pm,
  then no push notification is sent (queued until 8am)
- AC-3.2: Given I set quiet hours, when a notification triggers,
  then email and in-app notifications still work normally
- AC-3.3: Given I am in quiet hours, when an admin-mandatory notification triggers,
  then it bypasses quiet hours and is sent immediately

## US-4: Bulk Preference Actions
**As a** platform user
**I want to** quickly enable/disable all notifications for a channel
**So that** I can manage preferences efficiently

### Acceptance Criteria
- AC-4.1: Given I click "Disable all push", when confirmed,
  then all push notification preferences are set to off
- AC-4.2: Given some notifications are admin-mandatory, when I bulk disable,
  then mandatory notifications remain enabled with visual indicator
```

---

## Example 3: Technical Design Specification

### Initial Prompt to AI

```markdown
Based on the notification preferences spec, generate a technical design.

Include:
- Data models
- API endpoints
- Architecture decisions
- Integration with existing notification system
```

### AI-Generated Design

```markdown
# Notification Preferences - Technical Design

## Data Models

### NotificationPreference

```python
class NotificationPreference(models.Model):
    """User's preference for a specific notification type and channel."""

    class NotificationType(models.TextChoices):
        MENTION = 'mention', 'Mention'
        ASSIGNMENT = 'assignment', 'Assignment'
        COMMENT = 'comment', 'Comment'
        DEADLINE = 'deadline', 'Deadline'
        PROJECT_UPDATE = 'project_update', 'Project Update'

    class Channel(models.TextChoices):
        EMAIL = 'email', 'Email'
        IN_APP = 'in_app', 'In-App'
        PUSH = 'push', 'Push'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=32, choices=NotificationType.choices)
    channel = models.CharField(max_length=16, choices=Channel.choices)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'notification_type', 'channel']
        indexes = [
            models.Index(fields=['user', 'notification_type']),
        ]
```

### QuietHours

```python
class QuietHours(models.Model):
    """User's quiet hours configuration."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)
    start_time = models.TimeField()  # e.g., 22:00
    end_time = models.TimeField()    # e.g., 08:00
    timezone = models.CharField(max_length=64, default='UTC')
    bypass_mandatory = models.BooleanField(default=True)
```

### MandatoryNotification (Admin-defined)

```python
class MandatoryNotification(models.Model):
    """Admin-defined mandatory notification types."""

    notification_type = models.CharField(max_length=32, unique=True)
    reason = models.TextField()  # Why this is mandatory
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## API Endpoints

### GET /api/v1/users/me/notification-preferences

Returns user's complete preference matrix.

**Response:**
```json
{
  "preferences": [
    {
      "notification_type": "mention",
      "channels": {
        "email": {"enabled": true, "mandatory": false},
        "in_app": {"enabled": true, "mandatory": false},
        "push": {"enabled": false, "mandatory": false}
      }
    }
  ],
  "quiet_hours": {
    "enabled": true,
    "start_time": "22:00",
    "end_time": "08:00",
    "timezone": "Europe/Kyiv"
  }
}
```

### PATCH /api/v1/users/me/notification-preferences

Updates specific preferences.

**Request:**
```json
{
  "preferences": [
    {
      "notification_type": "mention",
      "channel": "push",
      "enabled": true
    }
  ]
}
```

### PUT /api/v1/users/me/quiet-hours

Updates quiet hours configuration.

## Architecture Decision Records

### ADR-1: Preference Storage Strategy

**Decision:** Store preferences as explicit rows, not JSON blob.

**Context:** Need to query "all users who want email notifications for mentions."

**Consequences:**
- (+) Efficient queries for notification dispatch
- (+) Easy to add new types/channels
- (-) More rows in database
- (-) Need to create default rows for new users

### ADR-2: Quiet Hours Timezone Handling

**Decision:** Store user's timezone, calculate quiet hours server-side.

**Context:** Users travel; quiet hours should follow their local time.

**Consequences:**
- (+) Consistent behavior across devices
- (+) Works offline (server decides)
- (-) Need timezone database on server
- (-) User must update timezone when traveling

## Integration Points

### Notification Dispatcher

```python
# Before sending notification
async def should_send_notification(
    user_id: str,
    notification_type: str,
    channel: str
) -> bool:
    # Check preference
    pref = await get_preference(user_id, notification_type, channel)
    if not pref.enabled:
        # Check if mandatory
        if not is_mandatory(notification_type):
            return False

    # Check quiet hours (push only)
    if channel == 'push':
        if await is_quiet_hours(user_id):
            if not (is_mandatory(notification_type) and pref.bypass_mandatory):
                await queue_for_later(user_id, notification_type)
                return False

    return True
```

## Migration Strategy

1. Create tables with default preferences OFF
2. Backfill existing users with default preferences
3. Deploy preference UI
4. Integrate dispatcher with preference checks
5. Monitor for issues, adjust defaults if needed
```

---

## Example 4: Iterative Refinement Session

### Round 1: Initial Request

**User:**
```
Create a spec for file upload feature.
```

**AI:**
```markdown
I need more context to create a useful specification:

1. What types of files? (Images, documents, any type?)
2. Size limits? (1MB? 100MB? 1GB?)
3. Where are files stored? (S3? Local? CDN?)
4. Who can upload? (All users? Specific roles?)
5. What happens after upload? (Processing? Thumbnails?)
6. Versioning needed? (Can users update files?)
7. Sharing/permissions? (Public? Private? Team?)
```

### Round 2: User Provides Context

**User:**
```
- Document files only (PDF, DOCX, XLSX, TXT)
- Max 50MB per file, 500MB total per user
- Store in S3 with CloudFront CDN
- All authenticated users can upload
- Generate PDF preview for non-PDF documents
- Yes, versioning with history
- Files are private to user unless explicitly shared
```

**AI generates initial spec...**

### Round 3: AI Asks Follow-up

**AI:**
```markdown
Spec drafted. Before finalizing, please clarify:

1. **Virus scanning:** Should files be scanned before storage?
2. **Retention:** How long to keep deleted files? Old versions?
3. **Quotas:** What happens when user exceeds 500MB?
4. **Concurrent uploads:** Max simultaneous uploads?
5. **Resume support:** Support for resumable uploads (large files)?
6. **Sharing granularity:** View only? Download? Edit?
```

### Round 4: Refinement

**User:**
```
1. Yes, virus scan with ClamAV
2. Keep deleted 30 days, keep last 10 versions
3. Block new uploads, show upgrade prompt
4. Max 3 concurrent
5. Yes, use S3 multipart for files > 10MB
6. View and Download permissions
```

**AI refines spec with all details...**

### Round 5: Edge Cases Review

**AI:**
```markdown
## Edge Cases Identified

Please confirm handling for these scenarios:

| Scenario | Proposed Handling |
|----------|-------------------|
| Virus detected | Reject upload, notify user, log incident |
| File type mismatch | Reject (e.g., .exe renamed to .pdf) |
| Upload interrupted | Resume within 24h, cleanup orphaned parts |
| Quota reached mid-upload | Fail gracefully, don't consume quota |
| Preview generation fails | Show generic icon, log for investigation |
| Concurrent version conflict | Last-write-wins with conflict notification |
| Shared file deleted | Revoke access, notify recipients |

Confirm or modify these behaviors?
```

---

## Example 5: BDD Specification Format

### Feature: Shopping Cart

```gherkin
Feature: Shopping Cart Management
  As a customer
  I want to manage items in my shopping cart
  So that I can purchase multiple products at once

  Background:
    Given I am a logged-in customer
    And the product "Widget A" exists with price $29.99 and stock 100
    And the product "Widget B" exists with price $49.99 and stock 5

  Scenario: Add item to empty cart
    Given my cart is empty
    When I add 1 "Widget A" to my cart
    Then my cart should contain 1 item
    And my cart total should be $29.99
    And the "Widget A" stock should be reserved

  Scenario: Add item that is already in cart
    Given my cart contains 2 "Widget A"
    When I add 1 "Widget A" to my cart
    Then my cart should contain 3 "Widget A"
    And my cart total should be $89.97

  Scenario: Add item exceeding stock
    Given the product "Widget B" has 5 in stock
    When I try to add 10 "Widget B" to my cart
    Then I should see error "Only 5 available"
    And my cart should contain 5 "Widget B"

  Scenario: Remove item from cart
    Given my cart contains 2 "Widget A"
    When I remove 1 "Widget A" from my cart
    Then my cart should contain 1 "Widget A"
    And the stock reservation should be released for 1 unit

  Scenario: Cart expiration
    Given my cart contains items
    And 30 minutes have passed without activity
    When I view my cart
    Then I should see a warning "Cart will expire in 30 minutes"

  Scenario: Cart expires
    Given my cart contains 2 "Widget A"
    And 60 minutes have passed without activity
    When I view my cart
    Then my cart should be empty
    And the stock reservation should be fully released
    And I should see "Your cart has expired"
```

---

## Key Patterns from Examples

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Clarifying Questions First** | AI asks questions before generating | Complex/ambiguous features |
| **Iterative Refinement** | Multiple rounds of Q&A | Discovering hidden requirements |
| **Edge Cases Table** | Tabular format for scenarios | Error handling, boundary conditions |
| **BDD Format** | Given-When-Then scenarios | Features needing test automation |
| **ADR Integration** | Architecture decisions with spec | Technical design choices |

---

*Part of the [ai-assisted-specification-writing](README.md) methodology.*
