"""
purpose: Service function fully typed with PEP 695 generics.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Item:
    id: int
    name: str


def find_by_id[T](items: list[T], pred) -> T | None:
    for item in items:
        if pred(item):
            return item
    return None


def first_with_name(items: list[Item], name: str) -> Item | None:
    return find_by_id(items, lambda i: i.name == name)
