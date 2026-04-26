#!/usr/bin/env python3
"""CPM forward/backward pass using networkx.

Input YAML: activities list with id, effort_days, predecessors [{id, type, lag_days}].
Output: per-activity ES/EF/LS/LF/float/critical flag, project finish, critical path list.
"""
import sys
import yaml
import networkx as nx


def critical_path(activities):
    G = nx.DiGraph()
    act_map = {a["id"]: a for a in activities}
    for a in activities:
        G.add_node(a["id"], dur=a["effort_days"])
        for p in a.get("predecessors", []):
            lag = p.get("lag_days", 0)
            G.add_edge(p["id"], a["id"], lag=lag)

    if not nx.is_directed_acyclic_graph(G):
        raise ValueError(f"Cycle detected: {list(nx.find_cycle(G))}")

    # Forward pass
    es = {n: 0 for n in G}
    for n in nx.topological_sort(G):
        ef = es[n] + G.nodes[n]["dur"]
        for s in G.successors(n):
            lag = G[n][s]["lag"]
            es[s] = max(es[s], ef + lag)

    finish = max(es[n] + G.nodes[n]["dur"] for n in G)

    # Backward pass
    lf = {n: finish for n in G}
    for n in reversed(list(nx.topological_sort(G))):
        ls = lf[n] - G.nodes[n]["dur"]
        for p in G.predecessors(n):
            lag = G[p][n]["lag"]
            lf[p] = min(lf[p], ls - lag)

    results = []
    for n in nx.topological_sort(G):
        dur = G.nodes[n]["dur"]
        ef_n = es[n] + dur
        ls_n = lf[n] - dur
        total_float = lf[n] - ef_n
        results.append({
            "id": n,
            "ES": es[n], "EF": ef_n,
            "LS": ls_n, "LF": lf[n],
            "total_float": total_float,
            "critical": total_float == 0,
        })

    critical = [r["id"] for r in results if r["critical"]]
    return finish, critical, results


def main(path):
    data = yaml.safe_load(open(path))
    finish, crit, details = critical_path(data["activities"])
    print(f"Project finish: {finish} days")
    print(f"Critical path: {' -> '.join(crit)}")
    print("\nActivity details:")
    print(f"{'ID':<10} {'ES':>4} {'EF':>4} {'LS':>4} {'LF':>4} {'Float':>6} {'Critical'}")
    for r in details:
        print(f"{r['id']:<10} {r['ES']:>4} {r['EF']:>4} {r['LS']:>4} {r['LF']:>4} "
              f"{r['total_float']:>6} {'*' if r['critical'] else ''}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: critical-path.py activities.yaml")
    main(sys.argv[1])
