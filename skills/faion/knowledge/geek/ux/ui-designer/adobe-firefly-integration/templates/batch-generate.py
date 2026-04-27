"""Batch Firefly image generation: reads CSV of prompts, downloads outputs.

CSV format: name,prompt
Output: firefly-output/{name}_{variant}.jpg

Requires: FIREFLY_TOKEN env var (OAuth2 machine-to-machine, refresh every 24h).
"""
import csv
import os
import pathlib

import requests

TOKEN = os.environ["FIREFLY_TOKEN"]
API = "https://firefly-api.adobe.io/v2/images/generate"
OUT = pathlib.Path("firefly-output")
OUT.mkdir(exist_ok=True)


def generate(prompt: str, name: str) -> None:
    resp = requests.post(
        API,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "prompt": prompt,
            "size": {"width": 1200, "height": 630},
            "numVariations": 3,
        },
        timeout=30,
    )
    resp.raise_for_status()
    outputs = resp.json().get("outputs", [])
    if not outputs:
        print(f"WARN: {name} — empty outputs (moderation block?)")
        return
    for i, item in enumerate(outputs):
        url = item["image"]["presignedUrl"]
        img = requests.get(url, timeout=30).content  # download immediately; URL expires ~1h
        dest = OUT / f"{name}_{i}.jpg"
        dest.write_bytes(img)
        print(f"Saved {dest}")


with open("assets.csv") as f:
    for row in csv.DictReader(f):
        generate(row["prompt"], row["name"])
