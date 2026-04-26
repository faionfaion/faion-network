"""JSONL fine-tuning dataset validator with deduplication check."""
import hashlib
import json
import sys
from pathlib import Path


def validate_jsonl(
    path: str,
    required_roles: tuple[str, ...] = ("user", "assistant"),
    min_examples: int = 100,
    check_duplicates: bool = True,
) -> dict:
    """
    Validate fine-tuning JSONL dataset.
    Returns stats dict or raises ValueError on critical errors.
    """
    errors: list[str] = []
    warnings: list[str] = []
    seen_hashes: set[str] = set()
    stats = {"total": 0, "valid": 0, "duplicates": 0, "errors": 0}

    with open(path) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            stats["total"] += 1

            # Parse JSON
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"Line {line_num}: invalid JSON: {e}")
                stats["errors"] += 1
                continue

            # Check required structure
            if "messages" not in obj:
                errors.append(f"Line {line_num}: missing 'messages' key")
                stats["errors"] += 1
                continue

            messages = obj["messages"]
            if not isinstance(messages, list) or len(messages) < 2:
                errors.append(f"Line {line_num}: 'messages' must be a list with 2+ items")
                stats["errors"] += 1
                continue

            # Check required roles
            roles = {m.get("role") for m in messages}
            for role in required_roles:
                if role not in roles:
                    errors.append(f"Line {line_num}: missing required role '{role}'")

            # Check for empty content
            for j, msg in enumerate(messages):
                if not str(msg.get("content", "")).strip():
                    errors.append(f"Line {line_num}, message {j}: empty content")

            # Deduplication
            if check_duplicates:
                content_hash = hashlib.md5(line.encode()).hexdigest()
                if content_hash in seen_hashes:
                    warnings.append(f"Line {line_num}: duplicate example")
                    stats["duplicates"] += 1
                else:
                    seen_hashes.add(content_hash)
                    stats["valid"] += 1
            else:
                stats["valid"] += 1

    # Aggregate errors
    if len(errors) > 0:
        raise ValueError(
            f"Dataset validation failed ({len(errors)} errors):\n"
            + "\n".join(f"  {e}" for e in errors[:20])
            + (f"\n  ... and {len(errors)-20} more" if len(errors) > 20 else "")
        )

    if stats["valid"] < min_examples:
        raise ValueError(
            f"Insufficient valid examples: {stats['valid']} < minimum {min_examples}"
        )

    if warnings:
        print(f"Warnings ({len(warnings)}):", file=sys.stderr)
        for w in warnings[:10]:
            print(f"  {w}", file=sys.stderr)

    return stats


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate fine-tuning JSONL dataset")
    parser.add_argument("path", help="Path to JSONL file")
    parser.add_argument("--min-examples", type=int, default=100)
    args = parser.parse_args()

    stats = validate_jsonl(args.path, min_examples=args.min_examples)
    print(f"Validation passed: {stats}")
