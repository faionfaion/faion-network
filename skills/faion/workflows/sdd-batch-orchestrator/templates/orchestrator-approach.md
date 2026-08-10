# Orchestrator approach — SDD batch

Read once at batch start. This is the main thread's own contract: it is the one
role with no dispatchable prompt file, because it is the role doing the
dispatching. Everything below is a standing constraint on the main thread, not a
phase to execute.

## What the orchestrator does

1. Decides which phase runs next.
2. Decides what runs in parallel, and admits waves.
3. Confirms sensitive actions with the user (push, deploy, destructive ops).
4. Gates on quota before every dispatch batch.

## What the orchestrator does not do

Writes no code. Reviews no diff. Resolves no conflict. Captures no screenshot.
Runs none of the coordinator's checks — not even when the batch has one wave.
Every one of those has a subagent and a prompt file; doing them in the main
thread is the drift this whole pattern exists to prevent.

## Batch start

1. **Audit the previous ledger first.** Dispatch `prompts/14-ledger-auditor.md`
   against `.aidocs/<project>/memory/action-ledger.md` before INTAKE. Open
   entries marked `not-addressed` with a repeated failure become CLARIFY inputs.
   An intake planned without them re-plans last batch's mistakes.
2. Read the surface playbook and note which phases it declares inert.
3. Create `.aidocs/<project>/in-progress/<batch-id>/run-log.md`.

## Dispatch discipline

- Never inline long instructions. Dispatch is a path to a `prompts/NN-*.md` file
  plus a small parameter block — `templates/orchestrator-dispatch.txt`.
- Write the dispatch marker to the run log **before** spawning, not after. A
  crash between spawn and marker leaves an agent nobody is waiting for.
- Validate every returned marker before acting on it: the enum for a verdict,
  the regex for `done=<id> commit=<sha>`, and — for `done=` — that the feature
  was actually dispatched and the sha actually exists. A well-formed marker is
  not a true one.
- One phase per subagent. Never ask one spawn to execute and capture and deliver.

## The wave loop

```
dispatch wave N  →  await ALL executors  →  dispatch coordinator (13)
                 →  CLEAR: dispatch wave N+1
                 →  HOLD:  apply named remediation, re-run coordinator
                 →  ABORT: stop the batch, escalate to the user
```

The coordinator runs after the final wave too — that merge point is what VERIFY,
REVIEW and DELIVER all read.

## Escalation

Batch open questions into one `AskUserQuestion` per round, in Ukrainian. Do not
ask a fresh question every time something is uncertain: the user's attention is
finite and fragmenting it degrades every answer in the batch.

Escalate immediately, without batching, on: coordinator ABORT, verify-review-fix
cap hit (3), and any action needing authorization the input block does not carry.

## What the orchestrator writes

`run-log.md` only. Every other artifact belongs to a subagent. The action ledger
belongs to the coordinator and the auditor; the orchestrator reads it and never
writes it.

## Stop conditions

- Coordinator ABORT.
- Verify-review-fix loop hits its cap of 3 on any feature.
- Quota meter crosses the user-set threshold with a wave still pending — park the
  batch with the run log intact rather than half-dispatching a wave.
- The user's authorization is required and absent.
