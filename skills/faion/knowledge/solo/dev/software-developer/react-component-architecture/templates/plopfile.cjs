// purpose: Plop generator config: scaffold a feature folder from CLI.
// consumes: see content/02-output-contract.xml inputs for react-component-architecture
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
// plopfile.cjs — Plop generator for React component folders
// Usage: npx plop component
// Generates: Component.tsx + Component.test.tsx + Component.stories.tsx + index.ts
module.exports = (plop) => {
  plop.setGenerator('component', {
    description: 'UI primitive or feature component',
    prompts: [
      { type: 'input', name: 'name', message: 'PascalCase component name' },
      { type: 'list',  name: 'kind', choices: ['ui', 'feature'], message: 'Kind' },
      { type: 'input', name: 'feature', message: 'Feature slug (if feature)',
        when: (a) => a.kind === 'feature' },
    ],
    actions: (data) => {
      const base = data.kind === 'ui'
        ? 'src/components/ui/{{name}}'
        : `src/features/${data.feature}/components/{{name}}`;
      return [
        { type: 'add', path: `${base}/{{name}}.tsx`,
          template: `export function {{name}}() {\n  return <div>{{name}}</div>;\n}\n` },
        { type: 'add', path: `${base}/{{name}}.test.tsx`,
          template: `import { render } from '@testing-library/react';\nimport { {{name}} } from './{{name}}';\n\ndescribe('{{name}}', () => {\n  it('renders', () => {\n    render(<{{name}} />);\n  });\n});\n` },
        { type: 'add', path: `${base}/{{name}}.stories.tsx`,
          template: `import type { Meta, StoryObj } from '@storybook/react';\nimport { {{name}} } from './{{name}}';\n\nconst meta: Meta<typeof {{name}}> = { component: {{name}} };\nexport default meta;\n\nexport const Default: StoryObj<typeof {{name}}> = {};\n` },
        { type: 'add', path: `${base}/index.ts`,
          template: `export { {{name}} } from './{{name}}';\n` },
      ];
    },
  });
};
