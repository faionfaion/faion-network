/*
 * purpose: CSF3 story skeleton with autodocs + args + variants
 * consumes: content/01-core-rules.xml
 * produces: config
 * depends-on: content/01-core-rules.xml
 * token-budget-impact: small
 */
// Replace Component and ComponentProps with actual names.
import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { within, userEvent, expect } from '@storybook/test';
import { Component } from './Component';

const meta = {
  title: 'Components/Component',
  component: Component,
  tags: ['autodocs'],
  parameters: { layout: 'centered' },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary'],
      description: 'Visual variant',
    },
    disabled: { control: 'boolean' },
    onClick: { action: 'clicked' },
  },
  args: { onClick: fn() },
} satisfies Meta<typeof Component>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { variant: 'primary', children: 'Label' },
};

export const Secondary: Story = {
  args: { variant: 'secondary', children: 'Label' },
};

export const Interaction: Story = {
  args: { children: 'Click Me' },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);
    await userEvent.click(canvas.getByRole('button'));
    await expect(args.onClick).toHaveBeenCalled();
  },
};
