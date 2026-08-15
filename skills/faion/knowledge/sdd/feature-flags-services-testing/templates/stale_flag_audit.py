# __faion_header_v1__
# purpose: Stale flag detector: live >90 days AND both branches still present in code
# consumes: see content/02-output-contract.xml
# produces: spec
# depends-on: content/04-procedure.xml + content/01-core-rules.xml#weekly-stale-audit
# token-budget-impact: ~350 tokens when loaded as context
# faion_header_json: {"__faion_header__":{"purpose":"Stale flag detector: live >90 days AND both branches still present in code","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/04-procedure.xml + content/01-core-rules.xml#weekly-stale-audit","token_budget_impact":"~350 tokens when loaded as context"}}
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def days_alive(flag: dict, now: datetime) -> int:
    created = datetime.fromisoformat(flag["created_at"]).replace(tzinfo=timezone.utc)
    return (now - created).days


def both_branches_live(flag_name: str, repo: Path) -> bool:
    out = subprocess.run(["git", "grep", "-l", f"is_enabled(\"{flag_name}\")"], cwd=repo, capture_output=True, text=True)
    return out.returncode == 0


def main() -> int:
    catalog = json.loads(Path("flags.json").read_text())
    repo = Path(".")
    now = datetime.now(tz=timezone.utc)
    stale = [f for f in catalog if days_alive(f, now) > 90 and both_branches_live(f["name"], repo)]
    for f in stale:
        sys.stdout.write(f"STALE: {f['name']} alive {days_alive(f, now)}d\n")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
