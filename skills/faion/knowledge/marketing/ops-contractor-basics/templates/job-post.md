<!--
purpose: Contractor job post skeleton — role, outcome, requirements, rate band, application filter
consumes: scope of work + budget band + timezone constraints
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~250-600 tokens when loaded as context
variables:
  - name: role_title
    type: string
    required: true
    description: The role as a contractor would search for it - "Figma UI designer", not "Design Ninja". This is the line that decides whether the right people ever see the post.
  - name: company_name
    type: string
    required: true
    description: Who is hiring, as it appears on your site. Anonymous posts get anonymous applicants; a name is the first thing a good contractor checks before spending an hour on your test.
  - name: outcome
    type: text
    required: true
    description: The problem you need solved or the outcome you need reached - not a list of tasks. "Our onboarding flow loses 60% of signups at step 3" attracts a different applicant than "design some screens".
  - name: weekly_hours
    type: string
    required: true
    description: Hours per week you actually expect, as a range. Understating it to seem light is how a contractor discovers they took a half-time job and leaves in month two.
  - name: timezone_overlap
    type: string
    required: true
    description: Required overlap with your working hours, stated as an offset and a window - "at least 2h overlap with UTC+2, 09:00-18:00". Timezone is the most common silent mismatch in contractor hiring.
  - name: rate_band
    type: string
    required: true
    description: The rate range you will actually pay, with currency and unit. Posting without it triples your screening load and filters for people who negotiate rather than people who deliver.
  - name: engagement_length
    type: enum
    required: true
    options: [one-time, three-month, six-month, ongoing]
    description: How long this runs. Say it honestly - "ongoing" written to attract applicants for a two-week job is the fastest way to lose the contractor you wanted to keep.
-->
# {{role_title}} Needed at {{company_name}}

## About Us
[2-3 sentences: what you build, who you serve, why it matters]

## The Role
{{outcome}}

## Responsibilities
- [Task 1 — concrete deliverable]
- [Task 2 — concrete deliverable]
- [Task 3 — concrete deliverable]

## Requirements
- [Specific skill with experience level: e.g. "3+ years Figma, SaaS UI experience"]
- Availability: {{weekly_hours}}
- Timezone: {{timezone_overlap}}
- Communication: [e.g. "Async-first, responds within 24h"]

## Nice to Have
- [Bonus skill or experience]
- [Industry familiarity]

## Compensation
- Rate: {{rate_band}}
- Estimated hours: {{weekly_hours}}
- Duration: {{engagement_length}}

## How to Apply
Please include:
1. Brief intro (2-3 sentences: who you are, relevant experience)
2. 2-3 portfolio links most relevant to this role
3. One specific thing you noticed about our product or company

Applications without portfolio links will not be reviewed.
