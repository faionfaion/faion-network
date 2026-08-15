<!--
purpose: Markdown skeleton issue body the reporter fills in before submission.
consumes: nothing — this IS the input form.
produces: a bug report ready for the scorer to ingest.
depends-on: ticket tracker that supports Markdown issue templates.
token-budget-impact: ~150 tokens when copied into a new issue body.
variables:
  - name: surface
    type: string
    required: true
    description: The screen, endpoint or component where it shows - "Login form", "POST /v1/orders". It is the first word of the title and the thing triage routes on, so use the team's name for it.
  - name: observable_symptom
    type: text
    required: true
    description: What you saw, phrased so a stranger could recognise it without your context - "submit no-ops on an email with a leading space". Not "it is broken", not a theory about why.
  - name: start_url
    type: string
    required: true
    description: The exact URL the reproduction starts from, query string included. A reproduction that opens with "log in and navigate to" is a reproduction nobody will actually run.
  - name: actor_role
    type: string
    required: true
    description: The role the reproducing user must hold. A large share of "cannot reproduce" is the reporter being an admin and the triager not being one.
  - name: build_sha
    type: string
    required: true
    description: The build number or git SHA you saw this on. "Latest" ages within the hour and turns the report into something nobody can falsify or close.
  - name: severity
    type: enum
    required: true
    options: [critical, high, medium, low]
    description: Technical impact if nothing is done. Data loss or corruption is critical however few users hit it. This is not urgency - urgency is the next field.
  - name: priority
    type: enum
    required: true
    options: [P0, P1, P2, P3]
    description: Business urgency - how soon someone must act. A low-severity bug on the signup page can be P0; a critical one in an unreleased feature can be P3.
-->

## Title
{{surface}}: {{observable_symptom}}

## Environment
- OS + version:
- Browser + version (if web):
- Build / git SHA: {{build_sha}}
- Feature flags ON:
- User role / permissions: {{actor_role}}

## Steps to reproduce
<!-- Numbered, atomic, from a named initial state. -->
1. Open {{start_url}} while logged-in as {{actor_role}}.
2. ...
3. ...

## Expected result

## Actual result
{{observable_symptom}}

## Severity (technical impact)
{{severity}}

## Priority (business urgency)
{{priority}}

## Evidence
<!-- Drag a screenshot or screen-recording, or paste console / log excerpt below. -->

## AI feature?
- [ ] This bug involves an LLM / AI feature

### If yes — AI context (REQUIRED when checked)
- Prompt id (or full prompt body):
- Model + version:
- Temperature / seed:
- Full conversation export (attach JSON):
- Verbatim AI output that triggered the bug:
