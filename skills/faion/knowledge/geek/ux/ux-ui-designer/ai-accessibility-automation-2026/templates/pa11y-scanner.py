"""pa11y-ci batch scanner with JSON output.

Input:  urls_file  — path to a text file with one URL per line
Output: output_file — JSON file with pa11y-ci results and summary count
"""
import subprocess
import json
import sys


def run_pa11y(urls_file: str, output_file: str) -> None:
    config = {
        "defaults": {
            "standard": "WCAG2AA",
            "runners": ["axe", "htmlcs"],
            "timeout": 30000,
            "wait": 2000,
        },
        "urls": open(urls_file).read().splitlines(),
    }
    config_path = "/tmp/pa11y-config.json"
    with open(config_path, "w") as f:
        json.dump(config, f)

    result = subprocess.run(
        ["pa11y-ci", "--config", config_path, "--json"],
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    total = sum(len(v) for v in data.get("results", {}).values())
    print(f"Scanned {len(data.get('results', {}))} URLs, found {total} issues")

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    run_pa11y(sys.argv[1], sys.argv[2])
