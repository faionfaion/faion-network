// purpose: Storybook stories showing Button across segments
// consumes: inputs declared in AGENTS.md Prerequisites table
// produces: artefact conforming to content/02-output-contract.xml (segment-aware-design-system)
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~150-400 tokens when loaded as context
// Storybook stories showing Button across segments.
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "Primitives/Button",
  component: Button,
  argTypes: {
    segment: { control: "select", options: ["developer", "exec"] },
  },
};
export default meta;

export const Developer: StoryObj<typeof Button> = {
  args: { segment: "developer", children: "Run faion search" },
};

export const Exec: StoryObj<typeof Button> = {
  args: { segment: "exec", children: "Request enterprise demo" },
};
