// purpose: Storybook sibling story with 3 variants
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for practices-frontend-components
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import type { Meta, StoryObj } from '@storybook/react';
import { Component } from './Component';

const meta: Meta<typeof Component> = { title: 'Orders/Component', component: Component };
export default meta;

type Story = StoryObj<typeof Component>;
export const Default: Story = { args: { id: 'o1', label: 'Order #1', onSelect: () => {} } };
export const Selected: Story = { args: { ...Default.args!, selected: true } };
export const LongLabel: Story = { args: { ...Default.args!, label: 'Order #1 — very long descriptive label' } };
