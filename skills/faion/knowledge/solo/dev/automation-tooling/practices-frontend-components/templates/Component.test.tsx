// purpose: Testing Library sibling test
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for practices-frontend-components
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Component } from './Component';

test('renders label and reports selection', async () => {
  const onSelect = jest.fn();
  render(<Component id="o1" label="Order #1" onSelect={onSelect} />);
  const btn = screen.getByRole('option', { name: /order #1/i });
  await userEvent.click(btn);
  expect(onSelect).toHaveBeenCalledWith('o1');
});
