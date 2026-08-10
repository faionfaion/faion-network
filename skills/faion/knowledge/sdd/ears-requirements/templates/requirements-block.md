<!-- purpose: the Requirements section of a spec.md, with the ears_pattern column wired in -->
<!-- consumes: user-flows.md (happy path -> When, negative path -> If ... then, preconditions -> While) -->
<!-- produces: the FR/NFR table that sdd/spec-requirements owns and EARS constrains one field of -->
<!-- depends-on: content/02-output-contract.xml, templates/ears-rules.json -->
<!-- token-budget-impact: small -->

## Requirements

Every `FR-NNN` statement parses as one of the five EARS patterns. `NFR-NNN` parses
where it is a system response to a condition; otherwise it carries `n-a` plus a reason.
Run `faion lint requirements <this file>` before review.

| Id | Statement | ears_pattern | Priority | Verification method | Source flow |
|----|-----------|--------------|----------|---------------------|-------------|
| FR-001 | When a customer submits the checkout form, the payment service shall create a charge intent. | event-driven | must | integration test | `user-flows.md#checkout-happy-path` |
| FR-002 | If the payment provider returns a declined status, then the checkout page shall display the message "Card declined". | unwanted-behaviour | must | negative test | `user-flows.md#checkout-declined` |
| FR-003 | While the account is in trial state, the billing service shall reject all charge attempts. | state-driven | must | state-machine test | `user-flows.md#trial` |
| FR-004 | Where the multi-currency feature is enabled, the dashboard shall display amounts in the account currency. | optional-feature | should | flag matrix test | — |
| FR-005 | The billing service shall retain invoices for 7 years. | ubiquitous | must | property test + monitor | — |
| NFR-001 | The payment integration is isolated behind a single adapter module with no provider types in domain code. | n-a | should | architecture test (import boundary) | — |

`ears_pattern: n-a` MUST be accompanied by a reason. Record it here:

| Id | Reason for n-a |
|----|----------------|
| NFR-001 | architectural constraint, not a system response to a condition |

### Refused, and where it went

Anything that is not a system response to a condition does not belong in this table.

| Candidate | Routed to |
|-----------|-----------|
| "non-technical users can self-onboard" | `roadmap.md` success metrics — first-session activation rate ≥ 60%, measured over 30 days |
| "an Invoice belongs to exactly one Order" | `project-spec/` — domain invariant, not a behaviour |
| "onboarding must feel modern" | dropped; no threshold, no unit, no observable |
