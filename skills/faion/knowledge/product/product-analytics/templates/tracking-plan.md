## Tracking Plan: {Product} — {Feature/Release}

### Key Questions This Plan Answers
1. {Question 1 — what decision will this data inform?}
2. {Question 2}
3. {Question 3}

### User Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| user_id | string | Unique user identifier | "usr_abc123" |
| plan | string | Subscription tier | "pro" |
| signup_date | date (UTC) | Account creation date | "2024-01-15" |
| {custom} | {type} | {description} | {example} |

### Events (max 12 per feature)

#### Onboarding Events

| Event (Object Action) | Trigger | Properties | Owner |
|-----------------------|---------|------------|-------|
| Signup Started | Click signup CTA | source | Growth |
| Signup Completed | Form submitted | method (email/google) | Growth |
| Onboarding Step Completed | Each step done | step_name, duration_s | Product |
| Onboarding Completed | All steps done | total_duration_s | Product |

#### Core Feature Events

| Event (Object Action) | Trigger | Properties | Owner |
|-----------------------|---------|------------|-------|
| {Feature} Viewed | Page/modal opened | entry_point | {Owner} |
| {Feature} Created | Item created | type, count | {Owner} |

#### Conversion Events

| Event (Object Action) | Trigger | Properties | Owner |
|-----------------------|---------|------------|-------|
| Upgrade Initiated | Click upgrade CTA | from_plan, to_plan | Growth |
| Purchase Completed | Payment success | amount_usd, plan | Growth |
| Purchase Failed | Payment failed | error_type | Engineering |

### Naming Conventions
- Events: Object Action (e.g., "Account Created", "Feature Used")
- Properties: snake_case (e.g., step_name, user_id)
- Timestamps: _utc suffix (e.g., created_at_utc)
- Server-side required for: all conversion/revenue events
