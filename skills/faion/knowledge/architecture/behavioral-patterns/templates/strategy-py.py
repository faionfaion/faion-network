# purpose: Strategy pattern template (Python).
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a behavioral-patterns artefact validating against scripts/validate-behavioral-patterns.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
"""
Strategy pattern in Python using Protocol for duck typing.

Use when: multiple algorithms for the same task, swappable at runtime.
Apply when: 3+ algorithm variants growing into if/else chains.
Skip when: 2 variants unlikely to change — use a simple conditional.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


# ---------------------------------------------------------------------------
# Strategy interface (Protocol = duck typing, no inheritance required)
# ---------------------------------------------------------------------------
class SortStrategy(Protocol):
    def sort(self, data: list[int]) -> list[int]:
        ...


# ---------------------------------------------------------------------------
# Concrete strategies
# ---------------------------------------------------------------------------
class BubbleSortStrategy:
    def sort(self, data: list[int]) -> list[int]:
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result


class QuickSortStrategy:
    def sort(self, data: list[int]) -> list[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        mid  = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + mid + self.sort(right)


class BuiltinSortStrategy:
    def sort(self, data: list[int]) -> list[int]:
        return sorted(data)


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------
@dataclass
class Sorter:
    strategy: SortStrategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self.strategy = strategy

    def sort(self, data: list[int]) -> list[int]:
        return self.strategy.sort(data)


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sorter = Sorter(strategy=BuiltinSortStrategy())
    result = sorter.sort([5, 3, 1, 4, 2])
    print(f"Builtin:  {result}")

    sorter.set_strategy(QuickSortStrategy())
    result = sorter.sort([5, 3, 1, 4, 2])
    print(f"Quicksort: {result}")

    # Functional variant — a plain function also satisfies the Protocol
    sorter.set_strategy(type("Reverse", (), {"sort": lambda self, d: sorted(d, reverse=True)})())
    result = sorter.sort([5, 3, 1, 4, 2])
    print(f"Reverse:  {result}")
