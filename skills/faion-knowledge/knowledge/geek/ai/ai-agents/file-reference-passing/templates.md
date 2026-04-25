# Templates — File-Reference Passing

## Two-stage scan + load (Pydantic + Anthropic)

```python
from pathlib import Path
from pydantic import BaseModel

class ScanResult(BaseModel):
    rationale: str
    relevant_paths: list[str]    # paths into a fixed manifest

def scan(manifest: list[Path], goal: str) -> ScanResult:
    # cheap LLM call: see only the manifest, not the contents
    listing = "\n".join(f"- {p}" for p in manifest)
    return haiku.parse(goal=goal, manifest=listing)   # returns ScanResult

def load_and_reason(scan: ScanResult, goal: str) -> str:
    # validate
    valid = [Path(p) for p in scan.relevant_paths if Path(p).exists()]
    contents = {p: p.read_text() for p in valid}
    # strong LLM call: now sees only what was selected
    return sonnet.process(goal=goal, files=contents)
```

## Subagent returns refs + summary (Claude Code style)

```python
# Inside the subagent's response shape:
class SubagentReport(BaseModel):
    summary: str                    # 3-5 sentences for parent context
    interesting_refs: list[str]     # paths/URLs the parent might want
    follow_up_questions: list[str]  # if any
```

The parent context never grows by more than ~500 tokens regardless of how much the subagent read.

## Manifest-then-pick

```python
class Pick(BaseModel):
    rationale: str
    chosen_id: int     # must be from the manifest

manifest = [{"id": 1, "title": "..."}, {"id": 2, "title": "..."}]
pick = llm.pick(manifest=manifest)
chosen = next(m for m in manifest if m["id"] == pick.chosen_id)
result = llm.use(chosen)   # now full content is loaded
```

## Recursive descent (file tree)

```python
def descend(path: Path, goal: str) -> Path:
    if path.is_file():
        return path
    children = list(path.iterdir())
    pick = llm.pick_dir(children=children, goal=goal)   # ref-only
    return descend(pick, goal)

target = descend(repo_root, goal)
content = target.read_text()
answer = llm.answer(content=content, goal=goal)
```

## Python schema with constrained refs

```python
from typing import Annotated
from pydantic import StringConstraints

PathRef = Annotated[str, StringConstraints(pattern=r"^[a-z0-9_/.-]+\.(md|py|ts)$")]

class Out(BaseModel):
    rationale: str
    refs: list[PathRef]
```

## Tool-call shape (LLM emits a tool call to load by ref)

```json
{
  "type": "tool_use",
  "name": "read_file",
  "input": {"path": "src/agent/loop.py"}
}
```

The LLM emits refs THROUGH tools — the loop validates and runs the read. The next LLM turn sees only what was asked for.
