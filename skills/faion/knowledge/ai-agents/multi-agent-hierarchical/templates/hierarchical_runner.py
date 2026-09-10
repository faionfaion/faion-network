# purpose: Template fixture for multi-agent-hierarchical: hierarchical_runner.py
# consumes: content/01-core-rules.xml
# produces: executable script
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
"""Manager-worker hierarchical runner (anthropic>=1.0, synchronous). Env: ANTHROPIC_API_KEY.
Manager plans (JSON) -> plan-time cycle check -> stateless workers in topological order,
routed only through this orchestrator -> manager synthesises."""
from __future__ import annotations

import json
from collections import deque

import anthropic

client = anthropic.Anthropic()
MANAGER_MODEL = "claude-opus-5"
MANAGER_SYSTEM = (
    "Decompose tasks and coordinate workers. You never implement, write code or research yourself. "
    "Reply with ONLY a JSON object: {schema_version:'v1', task, failure_policy:'abort'|'degrade'|'retry', "
    "assignments:[{id:'a1'.., worker_name, subtask (>=16 chars), deps:[ids], timeout_s (>=5)}]}"
)
MAX_RETRIES = 2  # rule r5: retry policy caps at N<=2

# Worker roster: name -> {role, model, system_prompt}. Workers hold no state between calls.
WORKERS = {
    "researcher": {"model": "claude-sonnet-5", "system_prompt": "You list facts and code paths. Return findings as bullet points."},
    "security_reviewer": {"model": "claude-sonnet-5", "system_prompt": "You score findings against OWASP ASVS. Return a table."},
    "writer": {"model": "claude-sonnet-5", "system_prompt": "You draft markdown documents from supplied findings."},
}


def _text(resp) -> str:
    return next(b.text for b in resp.content if b.type == "text")


def _validate_plan(plan: dict) -> str | None:
    """Structural check mirroring plan-schema.json; returns an error string or None."""
    if plan.get("schema_version") != "v1" or plan.get("failure_policy") not in ("abort", "degrade", "retry"):
        return "schema_version must be 'v1'; failure_policy must be abort|degrade|retry"
    ids = {a.get("id") for a in plan.get("assignments", [])}
    for a in plan.get("assignments", []):
        if a.get("worker_name") not in WORKERS:
            return f"unknown worker {a.get('worker_name')!r}; roster = {sorted(WORKERS)}"
        if len(a.get("subtask", "")) < 16 or int(a.get("timeout_s", 0)) < 5:
            return f"assignment {a.get('id')}: subtask < 16 chars or timeout_s < 5"
        if not set(a.get("deps", [])) <= ids:
            return f"assignment {a.get('id')}: deps reference unknown ids"
    return None if ids else "assignments must be non-empty"


def plan_task(task: str, usage: dict) -> dict:
    """Rule r1: one repair attempt on parse/validation failure, then abort."""
    messages = [{"role": "user", "content": f"Task: {task}\nRoster: {json.dumps({k: v['system_prompt'] for k, v in WORKERS.items()})}"}]
    for attempt in range(2):
        resp = client.messages.create(model=MANAGER_MODEL, max_tokens=4096, system=MANAGER_SYSTEM, messages=messages)
        usage["tokens"] += resp.usage.input_tokens + resp.usage.output_tokens
        try:
            plan = json.loads(_text(resp))
            err = _validate_plan(plan)
        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            plan, err = None, f"JSON parse error: {exc}"
        if err is None:
            return plan
        messages += [{"role": "assistant", "content": _text(resp)}, {"role": "user", "content": f"Plan rejected: {err}. Emit a corrected JSON plan."}]
    raise RuntimeError(f"manager plan invalid after repair attempt: {err}")


def topo_order(plan: dict) -> list[dict]:
    """Rule r2: Kahn's algorithm; raises with the cycle members before any dispatch."""
    by_id = {a["id"]: a for a in plan["assignments"]}
    indeg = {i: len(a["deps"]) for i, a in by_id.items()}
    queue, order = deque(i for i, d in indeg.items() if d == 0), []
    while queue:
        cur = queue.popleft()
        order.append(by_id[cur])
        for i, a in by_id.items():
            if cur in a["deps"]:
                indeg[i] -= 1
                if indeg[i] == 0:
                    queue.append(i)
    if len(order) != len(by_id):
        raise ValueError(f"cycle in plan among {sorted(i for i, d in indeg.items() if d > 0)}")
    return order


def run_worker(a: dict, dep_results: dict, usage: dict) -> dict:
    """Rule r4: fresh call per subtask; dependency payloads are injected by the orchestrator only."""
    w, context = WORKERS[a["worker_name"]], "\n".join(f"[{d}] {json.dumps(dep_results[d])}" for d in a["deps"] if d in dep_results)
    try:
        resp = client.with_options(timeout=float(a["timeout_s"]), max_retries=0).messages.create(
            model=w["model"], max_tokens=4096, system=w["system_prompt"],
            messages=[{"role": "user", "content": f"Subtask: {a['subtask']}\n\nInputs from prior workers:\n{context or '(none)'}"}])
    except anthropic.APITimeoutError:
        return {"schema_version": "v1", "assignment_id": a["id"], "worker_name": a["worker_name"], "status": "timeout", "payload": None, "error": f"> {a['timeout_s']}s"}
    except anthropic.APIError as exc:
        return {"schema_version": "v1", "assignment_id": a["id"], "worker_name": a["worker_name"], "status": "error", "payload": None, "error": str(exc)}
    usage["tokens"] += resp.usage.input_tokens + resp.usage.output_tokens
    return {"schema_version": "v1", "assignment_id": a["id"], "worker_name": a["worker_name"], "status": "ok", "payload": {"text": _text(resp)}, "error": None}


def run(task: str) -> dict:
    usage = {"tokens": 0}
    plan = plan_task(task, usage)
    order = topo_order(plan)
    policy, results, trace = plan["failure_policy"], {}, []
    for a in order:
        result = run_worker(a, {k: v["payload"] for k, v in results.items() if v["status"] == "ok"}, usage)
        tries = 1
        while result["status"] != "ok" and policy == "retry" and tries <= MAX_RETRIES:
            result, tries = run_worker(a, {k: v["payload"] for k, v in results.items() if v["status"] == "ok"}, usage), tries + 1
        trace.append({**result, "attempts": tries})
        if result["status"] != "ok" and policy == "abort":
            raise RuntimeError(f"assignment {a['id']} {result['status']}: {result['error']} (policy=abort)")
        results[a["id"]] = result  # degrade: keep the row, downstream workers see it as missing input
    resp = client.messages.create(
        model=MANAGER_MODEL, max_tokens=8192,
        system="Decompose tasks and coordinate workers. Now synthesise worker results into the final answer for the task. Reply with ONLY a JSON object.",
        messages=[{"role": "user", "content": f"Task: {task}\nResults: {json.dumps(trace)}"}])
    usage["tokens"] += resp.usage.input_tokens + resp.usage.output_tokens
    return {"schema_version": "v1", "task": task, "used_tokens": usage["tokens"], "trace": trace,
            "final_result": {"payload": json.loads(_text(resp)), "partial": any(r["status"] != "ok" for r in trace)}}


if __name__ == "__main__":
    print(json.dumps(run("Audit the auth subsystem in <repo> and produce a tightening plan"), indent=2))
