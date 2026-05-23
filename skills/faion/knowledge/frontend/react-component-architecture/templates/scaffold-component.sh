#!/bin/bash
# scaffold-component.sh — Create a component folder with all required files.
# Usage: ./scaffold-component.sh <ComponentName> [group]
# Example: ./scaffold-component.sh Badge ui
# Example: ./scaffold-component.sh LoginForm forms
# Runs from project root. Creates files under src/components/<group>/<ComponentName>/

set -euo pipefail

NAME="${1:?Usage: scaffold-component.sh <ComponentName> [group]}"
GROUP="${2:-ui}"
DIR="src/components/$GROUP/$NAME"

if [ -d "$DIR" ]; then
    echo "ERROR: $DIR already exists"
    exit 1
fi

mkdir -p "$DIR"

# Main component file (stub)
cat > "$DIR/$NAME.tsx" << EOF
// $DIR/$NAME.tsx
import { forwardRef, type ComponentPropsWithoutRef } from 'react';
import { cn } from '@/lib/utils';

export interface ${NAME}Props extends ComponentPropsWithoutRef<'div'> {
  // add props here
}

export const $NAME = forwardRef<HTMLDivElement, ${NAME}Props>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('', className)} {...props} />
  ),
);

$NAME.displayName = '$NAME';
EOF

# Test file stub
cat > "$DIR/$NAME.test.tsx" << EOF
// $DIR/$NAME.test.tsx
import { render, screen } from '@testing-library/react';
import { $NAME } from './$NAME';

describe('$NAME', () => {
  it('renders without errors', () => {
    render(<$NAME data-testid="$NAME" />);
    expect(screen.getByTestId('$NAME')).toBeInTheDocument();
  });
});
EOF

# Storybook story stub
cat > "$DIR/$NAME.stories.tsx" << EOF
// $DIR/$NAME.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { $NAME } from './$NAME';

const meta: Meta<typeof $NAME> = {
  title: 'UI/$NAME',
  component: $NAME,
};
export default meta;

type Story = StoryObj<typeof $NAME>;

export const Default: Story = {};
EOF

# Barrel file
cat > "$DIR/index.ts" << EOF
export { $NAME } from './$NAME';
export type { ${NAME}Props } from './$NAME';
EOF

echo "Scaffolded: $DIR"
echo "Files: $NAME.tsx  $NAME.test.tsx  $NAME.stories.tsx  index.ts"
