# .agents/ Index

Deep reference for `faion-network`. The root `AGENTS.md` states each rule in one line and links here for the detail.

| File | Contents |
|------|----------|
| [docs-convention.md](docs-convention.md) | `CLAUDE.md` / `AGENTS.md` / `.agents/` pattern, the five testable rules, the 20-80 line budget, and the context-file cost evidence that caps submodule stubs |
| [sdd-lifecycle.md](sdd-lifecycle.md) | Feature and task lifecycles, SDD document types, CR / BUG side streams, no-time-estimates rule, `.aidocs/memory/`, token-efficiency shorthand |
| [linting.md](linting.md) | This repo's own `.githooks/` (what each gate runs, the validator scope split, the failure-set baseline), pre-commit policy, per-project tool table, agent rules, ruff quick reference |
| [fragment-shared-blocks.md](fragment-shared-blocks.md) | The sourcing rule and the commit rule for `skills/faion/fragments/`: what each shared block guarantees, which validator asserts it, and the measurements behind both |
| [adapters.md](adapters.md) | Claude Code and Codex adapter files, plugin manifests, `hooks/hooks.json` registrations, external doc links |

Related, outside `.agents/`:

- `docs/directory-structure.md` — full SDD directory documentation
- `docs/skill-authoring.md` — methodology and skill structure spec (mandatory read, see `rules/skill-authoring.md`)
- `docs/methodology-xml-schema.md` — `content/*.xml` schema
- `.aidocs/conventions/` — playbook spec and corpus conventions
