#!/usr/bin/env bash
# Usage: ./new-component.sh <layer> <ComponentName>
# Example: ./new-component.sh primitives Toast
# Creates component folder with tsx, module.css, stories, and updates barrel.
set -euo pipefail

LAYER=${1:?First arg: layer (primitives|composite|patterns|layout)}
NAME=${2:?Second arg: ComponentName (PascalCase)}
DIR="src/components/$LAYER/$NAME"

mkdir -p "$DIR"

cat > "$DIR/$NAME.tsx" <<EOF
import { forwardRef } from 'react';
import { clsx } from 'clsx';
import styles from './$NAME.module.css';

export interface ${NAME}Props extends React.HTMLAttributes<HTMLDivElement> {}

export const $NAME = forwardRef<HTMLDivElement, ${NAME}Props>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={clsx(styles.root, className)} {...props} />
  )
);
$NAME.displayName = '$NAME';
EOF

cat > "$DIR/$NAME.module.css" <<EOF
.root {
  display: block;
}
EOF

cat > "$DIR/$NAME.stories.tsx" <<EOF
import type { Meta, StoryObj } from '@storybook/react';
import { $NAME } from './$NAME';

const meta: Meta<typeof $NAME> = {
  component: $NAME,
  title: '$LAYER/$NAME',
};
export default meta;

export const Default: StoryObj<typeof $NAME> = { args: {} };
EOF

cat > "$DIR/$NAME.test.tsx" <<EOF
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { $NAME } from './$NAME';

expect.extend(toHaveNoViolations);

describe('$NAME', () => {
  it('has no axe violations', async () => {
    const { container } = render(<$NAME />);
    expect(await axe(container)).toHaveNoViolations();
  });
});
EOF

cat > "$DIR/index.ts" <<EOF
export { $NAME } from './$NAME';
export type { ${NAME}Props } from './$NAME';
EOF

# Update layer barrel
BARREL="src/components/$LAYER/index.ts"
echo "export * from './$NAME';" >> "$BARREL"

echo "Created $DIR"
echo "Updated $BARREL"
