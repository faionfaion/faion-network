#!/usr/bin/env bash
# springboot-pr-gate.sh
# Runs after every Spring Boot PR. Fails if any gate is violated.
# Usage: ./templates/springboot-pr-gate.sh
set -euo pipefail

./mvnw -B -q -ntp verify -Dspotless.check.skip=false
./mvnw -B -q -ntp test jacoco:report

# Fail if @Transactional appears in controller layer
grep -RIn --include='*.java' \
  'org.springframework.transaction.annotation.Transactional' \
  src/main/java/**/controller/**/*.java && {
    echo "ERROR: @Transactional in controller layer"; exit 1; } || true

# Enforce LAZY fetch on all collection associations
grep -RIn --include='*.java' \
  '@OneToMany\|@ManyToMany\|@OneToOne' src/main/java |
  while read -r line; do
    f=${line%%:*}
    grep -A1 "@OneToMany\|@ManyToMany\|@OneToOne" "$f" |
      grep -q 'fetch = FetchType.LAZY' || {
        echo "ERROR: eager/default fetch in $f"; exit 1; }
  done

# Ban System.out / printStackTrace in main code
grep -RIn --include='*.java' \
  'System\.out\|printStackTrace' src/main && {
    echo "ERROR: stdout/printStackTrace usage"; exit 1; } || true

echo "Spring Boot gate OK"
