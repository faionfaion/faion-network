#!/usr/bin/env bash
# check-names.sh — domain and handle availability batch check.
# Usage: check-names.sh names.txt   (one candidate per line)
# Output: CSV: name,com,io,co,gh,x,score
# Score: .com=10, .io=5, .co=3, GitHub=3, X/Twitter=3 (max 24)
set -euo pipefail
NAMES_FILE="${1:?usage: check-names.sh NAMES.txt}"
echo "name,com,io,co,gh,x,score"
while IFS= read -r name; do
    [[ -z "$name" ]] && continue
    s=0
    for tld in com io co; do
        if whois "${name}.${tld}" 2>/dev/null | grep -qiE "no match|not found|no entries"; then
            eval "av_${tld}=1"
            case "$tld" in
                com) s=$((s + 10)) ;;
                io)  s=$((s + 5))  ;;
                co)  s=$((s + 3))  ;;
            esac
        else
            eval "av_${tld}=0"
        fi
    done
    gh_code=$(curl -sLo /dev/null -w "%{http_code}" "https://github.com/${name}")
    [[ "$gh_code" == "404" ]] && av_gh=1 && s=$((s + 3)) || av_gh=0
    x_code=$(curl -sLo /dev/null -w "%{http_code}" "https://x.com/${name}")
    [[ "$x_code" == "404" ]] && av_x=1 && s=$((s + 3)) || av_x=0
    echo "${name},${av_com},${av_io},${av_co},${av_gh},${av_x},${s}"
    sleep 1  # rate-limit politeness
done < "$NAMES_FILE"
