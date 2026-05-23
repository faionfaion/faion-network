"""
audit-pipeline.py — async content audit scoring pipeline.

Flow: read inventory CSV → extract main content → score via Claude API → write scored.jsonl

Usage:
  pip install anthropic trafilatura
  python audit-pipeline.py inventory.csv rubric.yaml scored.jsonl

Columns expected in inventory CSV: url, gsc_clicks_90d, ga4_sessions_90d, has_images, age_days
"""
import asyncio, csv, json, sys, yaml
from pathlib import Path
import anthropic
from trafilatura import fetch_url, extract

CONCURRENCY = 20  # parallel requests; stay within API rate limits


def load_rubric(path: str) -> str:
    return Path(path).read_text()


async def score_url(client, url: str, metrics: dict, rubric: str) -> dict:
    html = fetch_url(url)
    text = (extract(html) or "")[:6000]  # cap at 6k chars
    if not text:
        return {"url": url, "action": "remove", "reason": "empty page", "scored_by": "guard"}

    msg = await client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=400,
        temperature=0,
        messages=[{
            "role": "user",
            "content": (
                f"Rubric:\n{rubric}\n"
                f"URL: {url}\n"
                f"Metrics: {json.dumps(metrics)}\n"
                f"Page text:\n{text}\n\n"
                "Return JSON only: "
                "{accuracy: 1-5, relevance: 1-5, quality: 1-5, "
                "action: keep|update|consolidate|remove, reason: string}"
            ),
        }],
    )
    data = json.loads(msg.content[0].text)
    data["url"] = url
    data["scored_by"] = "llm-haiku"
    return data


async def main(inventory_csv: str, rubric_yaml: str, output_jsonl: str) -> None:
    rubric = load_rubric(rubric_yaml)
    rows = list(csv.DictReader(open(inventory_csv)))
    client = anthropic.AsyncAnthropic()
    sem = asyncio.Semaphore(CONCURRENCY)

    async def bounded(row: dict) -> dict:
        async with sem:
            metrics = {
                "gsc_clicks_90d": row.get("gsc_clicks_90d", 0),
                "ga4_sessions_90d": row.get("ga4_sessions_90d", 0),
            }
            return await score_url(client, row["url"], metrics, rubric)

    results = await asyncio.gather(*[bounded(r) for r in rows], return_exceptions=True)
    with open(output_jsonl, "w") as f:
        for r in results:
            if isinstance(r, Exception):
                continue
            f.write(json.dumps(r) + "\n")
    print(f"Scored {len(results)} URLs → {output_jsonl}")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3]))
