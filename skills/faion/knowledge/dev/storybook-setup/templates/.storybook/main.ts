/*
 * purpose: Storybook v9 main config: stories glob, addons, framework.
 * consumes: 01-core-rules.xml
 * produces: code
 * depends-on: content/01-core-rules.xml
 * token-budget-impact: small
 */

import type { StorybookConfig } from "@storybook/react-vite";

const config: StorybookConfig = {
  stories: ["../src/**/*.stories.@(ts|tsx|mdx)"],
  addons: ["@storybook/addon-essentials", "@storybook/addon-a11y"],
  framework: { name: "@storybook/react-vite", options: {} },
  docs: { autodocs: "tag" },
};

export default config;
