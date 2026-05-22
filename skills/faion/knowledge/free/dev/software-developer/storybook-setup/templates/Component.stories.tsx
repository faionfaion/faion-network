/*
 * purpose: CSF3 story: Meta + Default + variants + play function.
 * consumes: 01-core-rules.xml
 * produces: code
 * depends-on: content/01-core-rules.xml
 * token-budget-impact: small
 */

import type { Meta, StoryObj } from "@storybook/react";

import { Button } from "./Button";

const meta = {
  title: "Components/Button",
  component: Button,
  tags: ["autodocs"],
  args: { label: "Click me", variant: "primary" },
} satisfies Meta<typeof Button>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const Destructive: Story = { args: { variant: "destructive" } };
