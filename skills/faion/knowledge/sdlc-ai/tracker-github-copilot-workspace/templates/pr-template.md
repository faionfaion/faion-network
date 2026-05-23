<!-- purpose: PR description template embedding Workspace metadata + snapshot link. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-1200 tokens when loaded as context -->

<!-- .github/pull_request_template.md -->
<!-- CI fails if either Closes-N line or Workspace snapshot URL is missing. -->

Closes #<issue-number>

## Summary

<one to three sentences: the change>

## Workspace snapshot

Workspace snapshot: https://github.com/copilot/spaces/<snapshot-id>

## Spec

<from .copilot/spec.md — current state vs desired state>

## Plan

<from .copilot/plan.md — file-level change list>

## Test plan

- [ ] Unit test added or updated
- [ ] Regression test for the original bug (if applicable)
- [ ] CI green

<!-- CI grep:
       grep -E "^(Closes|Fixes) #[0-9]+" PR_BODY  || exit 1
       grep -E "^Workspace snapshot:"     PR_BODY || exit 1
-->
