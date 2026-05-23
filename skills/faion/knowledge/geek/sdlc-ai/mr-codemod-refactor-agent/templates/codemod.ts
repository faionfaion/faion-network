// purpose: minimum-viable scaffold for the methodology's produces type
// consumes: inputs listed in AGENTS.md Prerequisites table
// produces: playbook-step
// depends-on: content/02-output-contract.xml (schema)
// token-budget-impact: low — ~100-400 tokens when loaded as context
import type { Transform } from 'jscodeshift';

const transform: Transform = (file, api) => {
  const j = api.jscodeshift;
  const root = j(file.source);
  root.find(j.MemberExpression, {
    object: { name: 'User' },
    property: { name: 'id' },
  }).forEach((p) => {
    (p.value.property as any).name = 'uid';
  });
  return root.toSource({ quote: 'single' });
};

export default transform;
