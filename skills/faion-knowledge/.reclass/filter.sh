#!/usr/bin/env bash
# Filter candidates.tsv to high-confidence moves only.
# Rule: downgrade to free is almost always a false positive
# (X-basics in geek/pro tier means "intro to X", not "free tier material").
# Apply only upgrades AND adjacent-tier downgrades with explicit keyword.

set -eu
cd "$(dirname "$0")"

SRC=candidates.tsv
SAFE=candidates.safe.tsv
SKIP=candidates.skip.tsv
AMBIG=candidates.ambiguous.tsv

: >"$SAFE"
: >"$SKIP"
: >"$AMBIG"

tier_rank() {
  case "$1" in
    free) echo 0 ;;
    solo) echo 1 ;;
    pro)  echo 2 ;;
    geek) echo 3 ;;
  esac
}

while IFS=$'\t' read -r current guess verdict path; do
  if [[ "$verdict" == "keep" ]]; then
    continue
  fi
  if [[ "$verdict" == "ambiguous" ]]; then
    printf '%s\t%s\t%s\t%s\n' "$current" "$guess" "$verdict" "$path" >>"$AMBIG"
    continue
  fi
  # verdict == move
  cur_rank=$(tier_rank "$current")
  new_rank=$(tier_rank "$guess")
  name=${path##*/}

  # Keep geek-tier material in geek regardless of name suffix
  if [[ "$current" == "geek" ]]; then
    printf '%s\t%s\t%s\t%s\t%s\n' "$current" "$guess" "SKIP_geek_stays" "$path" "$name" >>"$SKIP"
    continue
  fi

  # Never downgrade to free on heuristic alone — too many false positives
  # (fundamentals/basics of niche subjects are still tier-specific).
  # Content-review tick handles these case by case.
  if [[ "$guess" == "free" ]]; then
    printf '%s\t%s\t%s\t%s\t%s\n' "$current" "$guess" "SKIP_downgrade_to_free" "$path" "$name" >>"$SKIP"
    continue
  fi

  # Upgrades (free→solo, free→pro, free→geek, solo→pro, solo→geek, pro→geek) are fine
  if (( new_rank > cur_rank )); then
    printf '%s\t%s\t%s\t%s\n' "$current" "$guess" "MOVE" "$path" >>"$SAFE"
    continue
  fi

  # Remaining: downgrades within non-free (pro→solo, solo→free handled above, pro→free handled above)
  # Pro→solo: allow if it has SOLO-keyword (server-craft, docker-compose, etc.)
  if [[ "$current" == "pro" && "$guess" == "solo" ]]; then
    lc=$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]')
    if [[ "$lc" =~ (mvp|roadmap|docker-compose|pwa|landing-page|openapi|graphql-api|tailwind|nextjs) ]]; then
      printf '%s\t%s\t%s\t%s\n' "$current" "$guess" "MOVE" "$path" >>"$SAFE"
    else
      printf '%s\t%s\t%s\t%s\t%s\n' "$current" "$guess" "SKIP_downgrade_weak" "$path" "$name" >>"$SKIP"
    fi
    continue
  fi

  printf '%s\t%s\t%s\t%s\t%s\n' "$current" "$guess" "SKIP_other" "$path" "$name" >>"$SKIP"
done <"$SRC"

echo "=== Safe moves: $(wc -l <"$SAFE") ==="
awk -F'\t' '{print $1" -> "$2}' "$SAFE" | sort | uniq -c | sort -rn
echo "=== Skipped: $(wc -l <"$SKIP") ==="
awk -F'\t' '{print $3}' "$SKIP" | sort | uniq -c | sort -rn
echo "=== Ambiguous: $(wc -l <"$AMBIG") ==="
