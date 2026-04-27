"""WCAG contrast ratio checker from Figma REST API node data.

Fetches file, extracts fill colors, computes relative luminance and contrast ratios.
Reports pairs below WCAG AA thresholds (4.5:1 normal text, 3:1 large text).

Requires: FIGMA_TOKEN, FIGMA_FILE_KEY env vars.
"""
import os

import requests


TOKEN = os.environ["FIGMA_TOKEN"]
FILE_KEY = os.environ["FIGMA_FILE_KEY"]


def luminance(r: int, g: int, b: int) -> float:
    def channel(v: int) -> float:
        n = v / 255
        return n / 12.92 if n <= 0.04045 else ((n + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(c1: tuple, c2: tuple) -> float:
    l1, l2 = luminance(*c1), luminance(*c2)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def hex_to_rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def fetch_styles() -> dict:
    resp = requests.get(
        f"https://api.figma.com/v1/files/{FILE_KEY}",
        headers={"X-Figma-Token": TOKEN},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    data = fetch_styles()
    print("File fetched. Implement node traversal to extract fill/text color pairs.")
    # Traverse data["document"] recursively, extract fills from text nodes and
    # their parent backgrounds, then call contrast() on each pair.
