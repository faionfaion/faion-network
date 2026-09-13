<!--
purpose: Canonical skeleton for the `pr-mentoring-session-protocol` record — one PR, one learning goal, the gap anchored to a diff line, labelled comment counts, the junior's restatement and fix, the follow-up PR, and the junior's confirmation.
consumes: The junior's open PR, the prior session record, the review comment thread, and the follow-up PR once it exists.
produces: A committed record at .product/pr-mentoring-session-protocol/<junior>-<date>.md readable by the junior, mirrored as JSON for scripts/validate-pr-mentoring-session-protocol.py.
depends-on: templates/header.yaml, content/02-output-contract.xml, scripts/validate-pr-mentoring-session-protocol.py.
token-budget-impact: ~600 tokens to fill end-to-end.
-->
---
version: 0.1.0
pr: <pr_url>
junior: <junior>
senior: <senior>
date: <session_date>
---

# Session

- pr_url: <pr_url>
- junior: <junior>
- senior: <senior>
- date: <session_date>
- record_readable_by_junior: true
- evaluation_use: <evaluation_use>

# Learning goal

<learning_goal>

# Observed gap

- did: <gap_did>
- should: <gap_should>
- line: <gap_line_url>

# Restated gap (the junior's words)

<restated_gap>

# Comment counts

- issue: <issue_count>
- suggestion: <n>
- question: <n>
- nitpick: <nitpick_count>
- praise: <praise_count>
- thought: <n>
- session_outcome: <learning_goal_addressed | learning_goal_not_addressed; not_addressed when nitpicks outnumber every other label combined>

# Fix commit

- url: <commit URL, authored by the junior; null until pushed>
- author: <junior>

# Deferred findings

Unrelated problems, posted as ordinary review comments after the session.

- <line URL>: <one line>

# Progression

- prior_record_url: <prior_record_url>
- prior_action_status: <demonstrated | partial | not-demonstrated; required when a prior record exists>
- not_demonstrated_streak: <not_demonstrated_streak>

# Decision

- follow_up_action: <follow_up_action>
- demonstrate_in: window <follow_up_window>, url <follow-up PR or ticket URL; null until it exists>
- escalation: <intervention pairing-session | structured-exercise | course, escalated_to role:handle; required at a streak of 3>

# Junior confirmation

- method: <comment | reaction | co-authorship>
- url: <URL of the confirmation>
- confirmed_at: <YYYY-MM-DD>

# Evidence

- <gap_line_url>
- <prior_record_url>
- <follow-up PR URL when it exists>

# Status

<open until the follow-up PR URL is recorded, then closed>
