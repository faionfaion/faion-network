#!/usr/bin/env bash
# new-component.sh <ComponentName>
# Story-first scaffold: creates story → impl placeholder → index
set -euo pipefail

name="${1:?Usage: new-component.sh <ComponentName>}"
dir="src/primitives/${name}"
mkdir -p "$dir"

cat > "$dir/${name}.stories.tsx" <<EOF
import type { Meta, StoryObj } from '@storybook/react';
import { ${name} } from './${name}';

const meta: Meta<typeof ${name}> = {
  title: 'Primitives/${name}',
  component: ${name},
  tags: ['autodocs'],
};
export default meta;
type Story = StoryObj<typeof ${name}>;

export const Default: Story = { args: {} };
EOF

echo "// TODO: implement ${name} after story is finalized" > "$dir/${name}.tsx"
echo "export * from './${name}';" > "$dir/index.ts"
echo "Scaffolded $dir — write the story first, then implement."
