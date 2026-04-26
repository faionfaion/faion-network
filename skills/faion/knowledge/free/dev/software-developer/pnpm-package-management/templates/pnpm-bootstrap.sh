#!/usr/bin/env bash
# pnpm-bootstrap.sh — initialise a pnpm-pinned project safely.
# Usage: PNPM_VERSION=9.12.0 NODE_VERSION=20 ./pnpm-bootstrap.sh
set -euo pipefail
PNPM_VERSION="${PNPM_VERSION:-9.12.0}"
NODE_VERSION="${NODE_VERSION:-20}"

corepack enable
corepack prepare "pnpm@${PNPM_VERSION}" --activate

[ -f package.json ] || pnpm init

# Pin the toolchain
node -e "
  const fs=require('fs'); const p=JSON.parse(fs.readFileSync('package.json'));
  p.packageManager='pnpm@${PNPM_VERSION}';
  p.engines={node:'>=${NODE_VERSION}.0.0', pnpm:'>=${PNPM_VERSION%.*}.0'};
  p.scripts={...(p.scripts||{}), preinstall:'npx only-allow pnpm'};
  fs.writeFileSync('package.json', JSON.stringify(p,null,2)+'\n');
"

cat > .npmrc <<'EOF'
strict-peer-dependencies=true
auto-install-peers=true
shamefully-hoist=false
engine-strict=true
prefer-frozen-lockfile=true
EOF

# Workspace marker (update packages list as needed)
[ -f pnpm-workspace.yaml ] || printf 'packages:\n  - "apps/*"\n  - "packages/*"\n' > pnpm-workspace.yaml

pnpm install
echo "pnpm workspace initialized with pnpm@${PNPM_VERSION}"
