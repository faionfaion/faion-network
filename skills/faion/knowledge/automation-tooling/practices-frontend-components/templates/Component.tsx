// purpose: React functional component with typed props + a11y
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for practices-frontend-components
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import * as React from 'react';
import styles from './Component.module.css';

export interface ComponentProps {
  id: string;
  label: string;
  selected?: boolean;
  onSelect: (id: string) => void;
}

export function Component({ id, label, selected = false, onSelect }: ComponentProps) {
  return (
    <button
      type="button"
      role="option"
      aria-selected={selected}
      className={selected ? styles.selected : styles.row}
      onClick={() => onSelect(id)}
    >
      {label}
    </button>
  );
}
