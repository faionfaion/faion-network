<!-- purpose: an EMPTY constitution.md — every slot is a placeholder, every example is a comment -->
<!-- consumes: the elicitation question "what have you had to explain twice?" -->
<!-- produces: .product/constitution.md (or .aidocs/constitution.md) once the TODOs are resolved -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: small — the finished file is loaded by every phase, so keep it small -->

# TODO(PROJECT_NAME) Constitution

<!--
Sync Impact Report
version: 0.0.0 -> TODO(VERSION)
added: TODO(RULE_IDS)
modified: -
removed: -
out of sync: TODO(DOWNSTREAM_FILES)
-->

## Scope

Domain facts, business rules, the data model, invariants and deploy topology live in
`TODO(PROJECT_SPEC_PATH)/project-spec/`, not here. This file holds only standing
decisions about how the work is done.

<!--
Delegation is mandatory even while that folder is nearly empty. A constitution that
absorbs domain facts inherits their churn and stops being cheap enough to load.
-->

## Rules

<!--
Admission test — all four must hold, per r1-four-part-admission-test:
  durable      it outlives the current feature
  cross-cutting it constrains more than one feature or layer
  contestable  a competent engineer could have chosen otherwise
  checkable    you can name the observation that would show a violation

Write the **Why:** FIRST, from the answer to "what have you had to explain twice?",
then write the rule from the why. At most 20 rules; at most 60 words per rule body.

Shape of one rule — delete this comment, do not copy the example into your file:

  ### R-01 One migration per pull request

  **Why:** two migrations in one pull request cannot be rolled back independently

  Each pull request contains at most one schema migration. A change needing two
  migrations is split into two pull requests, merged in order.

This template ships with NO pre-filled rules on purpose. A pre-filled constitution
is somebody else's opinions arriving with the authority of a standard.
-->

### R-01 TODO(RULE_TITLE)

**Why:** TODO(RULE_WHY)

TODO(RULE_BODY)

## Compliance

TODO(WHO_CHECKS) checks these rules by TODO(HOW). On a violation, TODO(CONSEQUENCE).

Mechanically checked today: TODO(MACHINE_CHECKED_RULE_IDS).
Checked only by reading: TODO(HUMAN_CHECKED_RULE_IDS).

<!--
A rule with no named checker becomes folklore within a quarter, and nobody announces
the moment it stopped being enforced. If a rule is mechanically checkable, move the
check into a linter or CI job and cite that job here.
-->

## Amendment

TODO(AMENDMENT_PROCESS)

Versioning: MAJOR when a rule is removed or its meaning is reversed, MINOR when a
rule is added, PATCH for wording that does not change what is permitted. Every change
updates the Sync Impact Report above and the footer below.

<!--
A rule that no longer holds is amended or retired — never left in place and quietly
ignored, and never superseded by appending a contradicting rule below it. History
belongs in decisions.md / ADRs, which are append-only; this file is the standing set.
-->

---

**Version:** TODO(VERSION) · **Ratified:** TODO(RATIFICATION_DATE) · **Last amended:** TODO(AMENDMENT_DATE)
