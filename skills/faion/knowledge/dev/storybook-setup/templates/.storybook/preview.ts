/*
 * purpose: Global decorators (Theme, Router, ReactQuery).
 * consumes: 01-core-rules.xml
 * produces: code
 * depends-on: content/01-core-rules.xml
 * token-budget-impact: small
 */

import type { Preview } from "@storybook/react";
import "../src/index.css";

const preview: Preview = {
  parameters: {
    controls: { matchers: { color: /(background|color)$/i } },
  },
};

export default preview;
