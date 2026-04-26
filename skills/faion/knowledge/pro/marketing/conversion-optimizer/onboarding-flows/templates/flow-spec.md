# Onboarding Flow Spec: [Product Name]

## Activation Event

`[event_name]` — e.g. "created 1 project with 3+ tasks in session 1"

## Segments

| Segment | Routing Question Answer | Onboarding Pattern |
|---------|------------------------|-------------------|
| Individual | "Personal use" | Template-first |
| Team admin | "Team collaboration" | Wizard |
| Evaluator | "Just exploring" | Interactive demo |

## Critical Path (required steps)

| Step | UI Pattern | Copy | Completion Criterion | Can Skip? |
|------|------------|------|----------------------|-----------|
| 1. [Step name] | [modal/tooltip/page] | [Copy ≤80 chars] | [Event fired] | No |
| 2. [Step name] | [modal/tooltip/page] | [Copy ≤80 chars] | [Event fired] | No |
| 3. [Step name] | [modal/tooltip/page] | [Copy ≤80 chars] | [Activation event] | No |

## Optional Steps (contextual triggers)

| Step | Trigger | UI Pattern | Copy |
|------|---------|------------|------|
| Profile photo | First share action | Tooltip | [Copy] |
| Invite teammate | 5th object created | In-app prompt | [Copy] |

## Email Sequence

| Email | Day | Trigger | Subject | Stop Condition |
|-------|-----|---------|---------|----------------|
| Welcome | 0 | Signup | [Subject] | Activation event |
| Quick-win | 1 | No activation by D1 | [Subject] | Activation event |
| Feature highlight | 3 | No activation by D3 | [Subject] | Activation event |
| Success story | 7 | No activation by D7 | [Subject] | Activation event |
