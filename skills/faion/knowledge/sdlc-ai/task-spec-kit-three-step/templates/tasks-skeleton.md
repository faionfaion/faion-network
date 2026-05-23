<!-- purpose: tasks.md skeleton with [P] tag column and file-overlap proof column. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml + content/04-procedure.xml -->
<!-- token-budget-impact: ~200-1200 tokens when loaded as context -->

# Tasks: <feature-name>

> Generated from `plan.md`. Do NOT edit by hand — re-run `/speckit.tasks`.
> `[P]` marks tasks safe to run in parallel (no shared write paths).

## Anchors

- spec: `spec.md`
- plan: `plan.md`
- tracker: ENG-NNNN
- merge anchor: `Closes #NNNN`

## Tasks

- [ ] T-001 Write failing test for AC-1 in `tests/test_auth.py::test_oauth_callback_persists_user`.
- [ ] T-002 Write failing test for AC-2 in `tests/test_auth.py::test_oauth_rejects_unverified_email`.
- [ ] T-003 [P] Add `Idempotency-Key` parser in `auth/headers.py`.
- [ ] T-004 [P] Add Authlib client config in `auth/clients/google.py`.
- [ ] T-005 Implement `auth/views.py::OAuthCallbackView` to make T-001 green.
- [ ] T-006 Add VCR-backed integration test against Google sandbox.
- [ ] T-007 [P] Update `docs/api.md` with new endpoints.

## Verification

```bash
pytest tests/ -k oauth
ruff check auth/
mypy auth/
```

## Out of scope (re-stated from spec)

- DB migrations
- Frontend integration
