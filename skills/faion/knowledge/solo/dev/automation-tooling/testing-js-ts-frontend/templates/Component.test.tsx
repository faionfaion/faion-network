// purpose: Vitest + Testing Library + userEvent + jest-axe
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for testing-js-ts-frontend
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe } from 'jest-axe';
import { Component } from './Component';

describe('Component', () => {
  it('reports selection on click', async () => {
    const user = userEvent.setup();
    const onSelect = vi.fn();
    render(<Component id="o1" label="Order #1" onSelect={onSelect} />);

    const btn = screen.getByRole('option', { name: /order #1/i });
    await user.click(btn);

    expect(onSelect).toHaveBeenCalledWith('o1');
  });

  it('has no a11y violations', async () => {
    const { container } = render(<Component id="o1" label="Order #1" onSelect={() => {}} />);
    expect(await axe(container)).toHaveNoViolations();
  });
});
