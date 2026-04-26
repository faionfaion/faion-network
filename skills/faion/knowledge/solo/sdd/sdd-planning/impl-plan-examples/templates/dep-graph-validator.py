"""
dep-graph-validator.py

Validate that a task dependency graph has no cycles using topological sort.

Usage:
    python dep-graph-validator.py

Modify the TASKS dict below with your actual task dependencies, then run.
Format: {"TASK-003": ["TASK-001", "TASK-002"]}  (TASK-003 depends on TASK-001 and TASK-002)

Returns:
    Valid execution order if no cycles found.
    Raises ValueError if a cycle is detected.
"""

from collections import defaultdict, deque


def validate_no_cycles(tasks: dict[str, list[str]]) -> list[str]:
    """
    Topological sort to detect cycles in task dependency graph.
    tasks = {"TASK-003": ["TASK-001", "TASK-002"], ...}
    Returns list of tasks in valid execution order.
    Raises ValueError if a cycle is detected.
    """
    in_degree: dict[str, int] = defaultdict(int)
    graph: dict[str, list[str]] = defaultdict(list)
    all_tasks: set[str] = set(tasks.keys())

    for task, deps in tasks.items():
        for dep in deps:
            graph[dep].append(task)
            in_degree[task] += 1
            all_tasks.add(dep)

    queue: deque[str] = deque(t for t in all_tasks if in_degree[t] == 0)
    order: list[str] = []

    while queue:
        task = queue.popleft()
        order.append(task)
        for dependent in graph[task]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    if len(order) != len(all_tasks):
        remaining = all_tasks - set(order)
        raise ValueError(f"Cycle detected involving: {remaining}")

    return order


# Example usage — replace with actual task dependencies
TASKS = {
    "TASK-002": ["TASK-001"],
    "TASK-003": ["TASK-001"],
    "TASK-004": ["TASK-002", "TASK-003"],
    "TASK-005": ["TASK-004"],
}

if __name__ == "__main__":
    try:
        order = validate_no_cycles(TASKS)
        print("Valid execution order:")
        for i, task in enumerate(order, 1):
            print(f"  {i}. {task}")
    except ValueError as e:
        print(f"ERROR: {e}")
        raise SystemExit(1)
