<!--
purpose: Closing owner/action/due line. Byte-identical in 37 templates. The three fields are the whole content — an action without an owner and a date is the failure this shape exists to prevent.
consumes: one action row
produces: an H2 Next actions section with one action line
depends-on: nothing
token-budget-impact: ~30 tokens
variables:
  - name: action_owner
    type: string
    required: true
    default: "<name>"
    description: One named human accountable for the action.
  - name: action
    type: string
    required: true
    default: "<action>"
    description: The action, stated so completion is observable.
  - name: action_due
    type: string
    required: true
    default: "<date>"
    description: ISO-8601 date the action is due.
-->
## Next actions

- owner: `{{action_owner}}` — action: `{{action}}` — due: `{{action_due}}`
