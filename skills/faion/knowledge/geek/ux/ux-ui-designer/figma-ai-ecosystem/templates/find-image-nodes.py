# purpose: Pre-existing template carried into the figma-ai-ecosystem methodology
# consumes: See content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml for produces=report
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

"""Find Figma file nodes with raster image fills — candidates for AI image tools.

Input:  FIGMA_TOKEN (env), FILE_KEY (env or arg)
Output: printed list of node name, type, and ID
"""
import os
import requests


FIGMA_TOKEN = os.environ.get("FIGMA_TOKEN", "your_token")
FILE_KEY = os.environ.get("FIGMA_FILE_KEY", "your_file_key")


def find_image_nodes(file_key: str) -> list[dict]:
    """Return nodes that contain raster fills — candidates for AI image tools."""
    url = f"https://api.figma.com/v1/files/{file_key}"
    resp = requests.get(url, headers={"X-Figma-Token": FIGMA_TOKEN})
    resp.raise_for_status()
    data = resp.json()

    candidates: list[dict] = []

    def traverse(node: dict) -> None:
        fills = node.get("fills", [])
        for fill in fills:
            if fill.get("type") == "IMAGE":
                candidates.append({
                    "id": node["id"],
                    "name": node.get("name", "unnamed"),
                    "type": node.get("type"),
                })
        for child in node.get("children", []):
            traverse(child)

    traverse(data["document"])
    return candidates


if __name__ == "__main__":
    nodes = find_image_nodes(FILE_KEY)
    for n in nodes:
        print(f"{n['name']} ({n['type']}) — node ID: {n['id']}")
    print(f"\nTotal candidates: {len(nodes)}")
