"""
Validate JSONL fine-tuning format before upload to any training API.
Input:  path to JSONL file
Output: list of error strings (empty means valid)
Exit:   0 if valid, 1 if errors found
"""
import json
import sys


def validate_ft_jsonl(path: str) -> list[str]:
    errors = []
    with open(path) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"Line {i}: invalid JSON — {e}")
                continue
            if "messages" not in obj:
                errors.append(f"Line {i}: missing 'messages' key")
                continue
            msgs = obj["messages"]
            roles = [m.get("role") for m in msgs]
            if "assistant" not in roles:
                errors.append(f"Line {i}: no assistant turn")
            if not any(m.get("content", "").strip() for m in msgs if m.get("role") == "assistant"):
                errors.append(f"Line {i}: assistant content is empty")
    return errors


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "training_data.jsonl"
    errs = validate_ft_jsonl(path)
    if errs:
        print(f"Found {len(errs)} error(s):")
        for e in errs:
            print(f"  {e}")
        sys.exit(1)
    print("Valid — no format errors found")
