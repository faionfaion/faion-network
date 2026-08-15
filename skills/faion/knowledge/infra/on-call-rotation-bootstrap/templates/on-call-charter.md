<!--
purpose: On-call charter skeleton
consumes: team headcount, SLA, comp policy URL
produces: filled on-call-charter.md
depends-on: content/01-core-rules.xml r1
token-budget-impact: ~500 tokens when filled
variables:
  - name: team_name
    type: string
    required: true
    description: The team that carries this pager, as the org chart names it. One team per charter - a shared rotation with two charters is how a page ends up acknowledged by nobody.
  - name: effective_date
    type: string
    required: true
    description: The date this charter takes effect, ISO. On-call terms change what people are paid and when they sleep; an undated charter cannot be shown to have been agreed before the shift.
  - name: shift_length
    type: enum
    required: true
    options: [168h, 24h, 12h, 8h]
    description: Length of one shift. 168h (a week) is the default for teams of 6 or more; anything shorter multiplies hand-offs, and a hand-off is where an unresolved incident gets forgotten.
  - name: rotation_owner
    type: string
    required: true
    description: The engineer who owns the schedule itself - swaps, gaps, escalation config. Not the manager. This role rotates yearly and the name here is who to chase when the calendar is empty.
  - name: participants
    type: text
    required: true
    description: Everyone in the rotation, comma-separated. Count them: below five people, a weekly rotation means one week in four and this charter is a plan for attrition, not for coverage.
  - name: url
    type: string
    required: true
    description: Link to the written compensation policy. If it does not exist yet, write it before this charter ships - unpaid off-hours pages are the term people accept quietly and leave over.
  - name: schedule_repo_path
    type: path
    required: true
    description: Where the schedule config lives in version control. A rotation that exists only in a vendor UI has no review, no history and no answer to "who changed the escalation path".
-->

# On-Call Charter — {{team_name}} (effective {{effective_date}})

Shift length: {{shift_length}}
Tiers: primary + secondary (default) | primary only (only if team 5-7 with external retainer)
Acknowledgement SLA: sev-1 5 min, sev-2 15 min, sev-3 next business hour
Escalation: primary -> secondary (8 min) -> manager (15 min)
Compensation: 1 h time-off-in-lieu per off-hours page; max 8 h/shift; cash above ceiling
Swap policy: any engineer can swap with 48 h notice via tool override
Rotation owner: {{rotation_owner}} (rotates yearly)
Participants: {{participants}}

Comp policy doc: {{url}}
Schedule config: {{schedule_repo_path}}
