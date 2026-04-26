"""
belief_update.py — weekly belief-update loop.
Schedule via Dagster/cron or NERO 'schedule' skill.
Reads events.ndjson (7-day rolling window), calls Claude belief-updater,
writes versioned beliefs.yaml. Run 'git commit beliefs.yaml' after.
"""
import json
import pathlib
import yaml
import datetime
import anthropic

EVENTS = pathlib.Path("events.ndjson")     # 7-day rolling window, one JSON per line
BELIEFS = pathlib.Path("beliefs.yaml")     # versioned via git
HISTORY = pathlib.Path("beliefs.history.ndjson")

client = anthropic.Anthropic()


def load_window(days: int = 7) -> list[dict]:
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    out = []
    for line in EVENTS.read_text().splitlines():
        if not line.strip():
            continue
        ev = json.loads(line)
        if datetime.datetime.fromisoformat(ev["ts"].rstrip("Z")) >= cutoff:
            out.append(ev)
    return out


def run() -> None:
    events = load_window()
    prompt = f"""<role>belief-updater</role>
<current_beliefs>{BELIEFS.read_text()}</current_beliefs>
<events>{json.dumps(events, indent=2)}</events>
<rules>Mutate a belief only if &gt;=3 independent events agree OR 1 high-severity
contradicting event with cited source. Cite event_id per change. JSON only.</rules>"""

    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )
    delta = json.loads(resp.content[0].text)
    beliefs = yaml.safe_load(BELIEFS.read_text()) or {}

    for change in delta.get("changed", []):
        beliefs[change["belief_id"]] = change["after"]
        HISTORY.open("a").write(
            json.dumps({**change, "ts": datetime.datetime.utcnow().isoformat() + "Z"}) + "\n"
        )

    BELIEFS.write_text(yaml.safe_dump(beliefs, sort_keys=True))
    print(
        f"changed={len(delta.get('changed', []))} "
        f"pressure={len(delta.get('unchanged_with_pressure', []))}"
    )


if __name__ == "__main__":
    run()
