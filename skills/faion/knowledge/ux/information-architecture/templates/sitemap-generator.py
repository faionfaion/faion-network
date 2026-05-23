"""
Generate a Mermaid graph diagram from a structured IA definition.

Input: list of node dicts with 'label' and optional 'children' list.
Output: Mermaid graph TD string, suitable for rendering in GitHub, Notion, Miro.

Usage:
    ia = [
        {"label": "Shop", "children": [
            {"label": "By Category"},
            {"label": "By Brand"},
            {"label": "Sale Items"},
        ]},
        {"label": "Learn", "children": [
            {"label": "Buying Guides"},
            {"label": "Reviews"},
        ]},
        {"label": "Get Help"},
    ]
    print(sitemap_diagram(ia))
"""


def _safe_id(label: str) -> str:
    """Convert a label to a safe Mermaid node ID."""
    return label.lower().replace(" ", "_").replace("&", "and").replace("/", "_")


def _to_mermaid(nodes: list, parent_id: str, lines: list) -> None:
    for node in nodes:
        node_id = _safe_id(node["label"])
        lines.append(f'  {parent_id} --> {node_id}["{node["label"]}"]')
        children = node.get("children", [])
        if children:
            _to_mermaid(children, node_id, lines)


def sitemap_diagram(ia: list) -> str:
    """Render the IA definition as a Mermaid graph TD diagram."""
    lines = ["graph TD", '  root["Home"]']
    _to_mermaid(ia, "root", lines)
    return "\n".join(lines)


# Max recommended depth: 3 levels (root → L1 → L2 → L3)
# Above 3 levels the diagram becomes unreadable; split into sub-diagrams.
