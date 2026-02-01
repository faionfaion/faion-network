---
id: ui-lib-patterns
name: "UI Component Library - Advanced Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# UI Component Library - Advanced Patterns

Advanced component patterns for building scalable UI libraries.

## Compound Component Pattern

```tsx
// components/composite/Card/Card.tsx
import { createContext, useContext, ReactNode } from 'react';
import { clsx } from 'clsx';
import styles from './Card.module.css';

interface CardContextValue {
  variant: 'default' | 'elevated' | 'outlined';
}

const CardContext = createContext<CardContextValue | null>(null);

function useCardContext() {
  const context = useContext(CardContext);
  if (!context) {
    throw new Error('Card compound components must be used within Card');
  }
  return context;
}

// Root component
interface CardProps {
  children: ReactNode;
  variant?: 'default' | 'elevated' | 'outlined';
  className?: string;
}

function CardRoot({ children, variant = 'default', className }: CardProps) {
  return (
    <CardContext.Provider value={{ variant }}>
      <article className={clsx(styles.card, styles[variant], className)}>
        {children}
      </article>
    </CardContext.Provider>
  );
}

// Sub-components
function CardHeader({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <header className={clsx(styles.header, className)}>
      {children}
    </header>
  );
}

function CardTitle({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <h3 className={clsx(styles.title, className)}>
      {children}
    </h3>
  );
}

function CardDescription({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <p className={clsx(styles.description, className)}>
      {children}
    </p>
  );
}

function CardContent({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <div className={clsx(styles.content, className)}>
      {children}
    </div>
  );
}

function CardFooter({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <footer className={clsx(styles.footer, className)}>
      {children}
    </footer>
  );
}

function CardImage({ src, alt, className }: { src: string; alt: string; className?: string }) {
  return (
    <div className={clsx(styles.imageContainer, className)}>
      <img src={src} alt={alt} className={styles.image} />
    </div>
  );
}

// Export compound component
export const Card = Object.assign(CardRoot, {
  Header: CardHeader,
  Title: CardTitle,
  Description: CardDescription,
  Content: CardContent,
  Footer: CardFooter,
  Image: CardImage,
});

// Usage
function ProductCard({ product }: { product: Product }) {
  return (
    <Card variant="elevated">
      <Card.Image src={product.image} alt={product.name} />
      <Card.Header>
        <Card.Title>{product.name}</Card.Title>
        <Card.Description>{product.category}</Card.Description>
      </Card.Header>
      <Card.Content>
        <p>{product.description}</p>
        <p className="price">${product.price}</p>
      </Card.Content>
      <Card.Footer>
        <Button variant="primary">Add to Cart</Button>
        <Button variant="ghost">View Details</Button>
      </Card.Footer>
    </Card>
  );
}
```

## Modal with Portal

```tsx
// components/composite/Modal/Modal.tsx
import { ReactNode, useEffect, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { clsx } from 'clsx';
import { Button } from '../../primitives/Button';
import styles from './Modal.module.css';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: ReactNode;
  footer?: ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
}

export function Modal({
  isOpen,
  onClose,
  title,
  description,
  children,
  footer,
  size = 'md',
  closeOnOverlayClick = true,
  closeOnEscape = true,
}: ModalProps) {
  // Handle escape key
  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (closeOnEscape && event.key === 'Escape') {
        onClose();
      }
    },
    [closeOnEscape, onClose]
  );

  // Lock body scroll when open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      document.addEventListener('keydown', handleKeyDown);

      return () => {
        document.body.style.overflow = '';
        document.removeEventListener('keydown', handleKeyDown);
      };
    }
  }, [isOpen, handleKeyDown]);

  if (!isOpen) return null;

  return createPortal(
    <div className={styles.overlay} onClick={closeOnOverlayClick ? onClose : undefined}>
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        aria-describedby={description ? 'modal-description' : undefined}
        className={clsx(styles.modal, styles[size])}
        onClick={(e) => e.stopPropagation()}
      >
        <header className={styles.header}>
          <h2 id="modal-title" className={styles.title}>
            {title}
          </h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            aria-label="Close modal"
          >
            <CloseIcon />
          </Button>
        </header>

        {description && (
          <p id="modal-description" className={styles.description}>
            {description}
          </p>
        )}

        <div className={styles.content}>{children}</div>

        {footer && <footer className={styles.footer}>{footer}</footer>}
      </div>
    </div>,
    document.body
  );
}

// Usage
function DeleteConfirmModal({ isOpen, onClose, onConfirm, itemName }) {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Delete Item"
      description={`Are you sure you want to delete "${itemName}"? This action cannot be undone.`}
      size="sm"
      footer={
        <>
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button variant="danger" onClick={onConfirm}>
            Delete
          </Button>
        </>
      }
    >
      {/* Additional content if needed */}
    </Modal>
  );
}
```

## Component Documentation

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';
import { ArrowRightIcon, DownloadIcon } from '../icons';

const meta: Meta<typeof Button> = {
  title: 'Primitives/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost', 'danger'],
      description: 'Visual style variant',
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
    },
    isLoading: {
      control: 'boolean',
    },
    disabled: {
      control: 'boolean',
    },
    fullWidth: {
      control: 'boolean',
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    children: 'Primary Button',
    variant: 'primary',
  },
};

export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="danger">Danger</Button>
    </div>
  ),
};

export const WithIcons: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <Button leftIcon={<DownloadIcon />}>Download</Button>
      <Button rightIcon={<ArrowRightIcon />}>Continue</Button>
    </div>
  ),
};

export const Loading: Story = {
  args: {
    children: 'Loading...',
    isLoading: true,
  },
};

export const AsLink: Story = {
  render: () => (
    <Button asChild>
      <a href="/dashboard">Go to Dashboard</a>
    </Button>
  ),
};
```

## References

- [Radix UI](https://www.radix-ui.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Storybook](https://storybook.js.org/)
- [React Aria](https://react-spectrum.adobe.com/react-aria/)

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Fix CSS typo, update Tailwind class, run prettier | haiku | Direct text replacement and formatting |
| Code review component accessibility compliance | sonnet | WCAG standards evaluation |
| Debug responsive layout issues across breakpoints | sonnet | Testing and debugging |
| Design system architecture and token structure | opus | Complex organization and scaling |
| Refactor React component for performance | sonnet | Optimization and code quality |
| Plan design token migration across 50+ components | opus | Large-scale coordination |
| Build storybook automation and interactions | sonnet | Testing and documentation setup |
