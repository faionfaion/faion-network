"""
Run axe-core via Playwright against a URL and return violation JSON.
Input: URL as command-line argument.
Output: prints violation summary to stdout.
Usage: python axe-playwright-runner.py https://example.com
Requires: playwright, axe-core (npm install axe-core)
"""
import json
import subprocess
import sys


def run_axe(url: str) -> dict:
    script = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('{url}', {{ waitUntil: 'networkidle' }});
  // Dismiss common cookie consent banners
  try {{ await page.click('[id*=accept], [class*=accept-cookie]', {{ timeout: 2000 }}); }} catch {{}}
  await page.addScriptTag({{ path: require.resolve('axe-core') }});
  const results = await page.evaluate(() => axe.run());
  console.log(JSON.stringify(results));
  await browser.close();
}})();
"""
    result = subprocess.run(
        ["node", "-e", script],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"axe-core failed: {result.stderr}")
    return json.loads(result.stdout)


def summarize(data: dict) -> None:
    violations = data.get("violations", [])
    print(f"Found {len(violations)} violation(s)\n")
    for v in violations:
        impact = v.get("impact", "unknown").upper()
        print(f"[{impact}] {v['id']}: {v['description']}")
        print(f"  WCAG: {', '.join(t['id'] for t in v.get('tags', []) if t['id'].startswith('wcag'))}")
        nodes = v.get("nodes", [])
        if nodes:
            print(f"  Example: {nodes[0].get('html', '')[:100]}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python axe-playwright-runner.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    data = run_axe(url)
    summarize(data)

    # Save full results for agent processing
    with open("axe-results.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Full results saved to axe-results.json")
