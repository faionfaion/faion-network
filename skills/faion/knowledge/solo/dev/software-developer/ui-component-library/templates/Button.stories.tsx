// purpose: Storybook story covering all required states for a Button primitive.
// consumes: see content/02-output-contract.xml inputs for ui-component-library
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from '../Button';

const meta: Meta<typeof Button> = {
  title: 'primitives/Button',
  component: Button,
  parameters: { a11y: { config: { rules: [{ id: 'color-contrast', enabled: true }] } } },
};
export default meta;

type Story = StoryObj<typeof Button>;

export const Default: Story = { args: { children: 'Save' } };
export const Hover: Story = { ...Default, parameters: { pseudo: { hover: true } } };
export const Focus: Story = { ...Default, parameters: { pseudo: { focusVisible: true } } };
export const Disabled: Story = { args: { children: 'Save', disabled: true } };
export const Loading: Story = { args: { children: 'Saving…', loading: true } };
export const Empty: Story = { args: { children: '' } };
export const Error: Story = { args: { children: 'Retry', variant: 'destructive' } };
