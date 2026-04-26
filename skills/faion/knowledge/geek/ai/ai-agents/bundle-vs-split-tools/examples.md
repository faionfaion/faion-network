# Examples — Bundle vs Split Tools

## Example 1: 50→12 tool consolidation

A team had 50 tools (DB CRUD × 10 entities = 40, plus 10 misc). Tool-selection error rate: 18%. Bundling each entity's CRUD into one `entity_ops(entity, mode, ...)` tool reduced to 11 tools. Tool-selection error rate: 4%.

## Example 2: Bad bundle, fixed by splitting

`exec(mode="git"|"npm"|"docker", ...)` — model often picked wrong mode (npm when meaning git). Splitting into `git_ops`, `npm_ops`, `docker_ops` raised correct-mode rate from 72% to 96%.

## Example 3: When split is right (Claude Code default)

Claude Code's tool surface: ~12 tools (Read, Edit, Write, Bash, Grep, Glob, Task, etc.). All distinct audiences. Each description is a tight prompt. No bundle would help.

## Example 4: When bundle is right (filesystem)

OpenAI's Code Interpreter exposes filesystem ops as a single tool with read/write/list/delete modes. Audience is unified, args overlap, model has strong filesystem priors. Bundle works.

## Example 5: Resource as third option

A docs server had 200 endpoints exposed as tools. Tool count exploded, model got lost.

Fix: convert read-only endpoints to Resources (`docs://{section}/{page}`); leave only write/dynamic operations as Tools. Tool count dropped to 8.

## Example 6: Mode enum saves the day

```python
"mode": {"type": "string"}  # before
```
Model emitted "READ", "Read", "read", "fetch" — all invalid. ~12% calls failed.

```python
"mode": {"type": "string", "enum": ["list", "read", "write", "delete"]}  # after
```
0% invalid mode calls.

## Example 7: faion-cli tool surface

Pipeline-orchestration agent exposes ~15 tools. All distinct: schedule_step, mark_done, replan, get_state, etc. Each has clear use-when/NOT-use-when. Below the 25 threshold; no bundling needed.

## Example 8: Anti-pattern — meta_tool

```python
# BAD
def tool(name, args):
    return TOOL_REGISTRY[name](**args)
```

The model has to invent `name` strings, lacks autocomplete from the schema, and tool-arg validation is delayed. Reverts to eval-string nightmare.

Fix: expose each tool individually OR use legitimate bundles.
