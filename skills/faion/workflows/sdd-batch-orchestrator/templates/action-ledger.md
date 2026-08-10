# Action ledger — <project>

Append-only. Entries are added and their `status` is re-marked; nothing is
rewritten or deleted. Written by the coordinator at wave boundaries and at batch
close; re-marked by the ledger auditor before the next batch's INTAKE.

An entry qualifies only if it recurred across ≥2 features or waves, cost a
verify-review-fix iteration, or was caught by the coordinator rather than by the
phase that should have caught it. Every entry cites evidence — a sha, a path, or
a failing command with its output. No evidence, no entry.

`class`: `process` | `prompt` | `methodology` | `tooling`
`status`: `open` | `done` | `not-addressed`

---

## AL-001

- **batch:** <batch-id>
- **class:** prompt
- **observation:** <one line — what happened>
- **evidence:** <sha | path | command + output>
- **action:** <what to change, concrete enough to diff>
- **status:** open

## AL-002

- **batch:** <batch-id>
- **class:** process
- **observation:** <one line>
- **evidence:** <sha | path | command + output>
- **action:** <what to change>
- **status:** done
- **resolved:** <citation from the batch that closed it>
