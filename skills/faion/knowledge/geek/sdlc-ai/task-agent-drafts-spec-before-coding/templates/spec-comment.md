<!--
  purpose: agent spec-comment with current state / desired state / proposed plan
  consumes: ticket body + linked Notion/Slack/prior tickets + code-intel search
  produces: spec (markdown posted as first comment on the assigned ticket)
  depends-on: content/01-core-rules.xml (spec-comment-first, three-section-shape, discovery-includes-linked-context)
  token-budget-impact: low — ~200 tokens when loaded as context

  Fill every section. Mention the issue creator. Do NOT open a PR until
  the approval gate (see templates/approval-gate.yaml) clears.
-->

@{{issue.creator}} — drafted plan for review:

**Current State.** {{1-2 sentences: what behaviour exists today, with file:line or trace evidence}}

**Desired State.** {{1-2 sentences: what behaviour the ticket asks for, observable as a test or trace}}

**Proposed Plan.**
1. {{INVEST step — independent, small, testable; cite the file or function it touches}}
2. {{INVEST step — keep each step under ~10 lines of diff if possible}}
3. {{Add or update a regression test that fails today and passes after the change}}

**Open Questions.** {{Any ambiguity left in the spec; tag the right CODEOWNER. If none, write "None — proceeding on approval."}}

<!--
  Approval signals (whichever applies to this tracker):
   - Linear: reaction :thumbsup: on this comment (human only).
   - Jira:   reply containing `/agent approve` from a project developer.
   - GitHub: issue labelled `agent:approved` by a user with write access.
-->
