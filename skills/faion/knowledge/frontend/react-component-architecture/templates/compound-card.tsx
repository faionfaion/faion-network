// src/components/ui/Card/Card.tsx
// Compound component pattern: Card.Header, Card.Title, Card.Content, Card.Footer.
// Sub-components share variant context via React Context.
import { createContext, useContext, type ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface CardContextValue {
  variant: 'default' | 'outlined';
}

const CardContext = createContext<CardContextValue | null>(null);

function useCardContext() {
  const ctx = useContext(CardContext);
  if (!ctx) throw new Error('Card sub-components must be used within <Card>');
  return ctx;
}

export interface CardProps {
  variant?: 'default' | 'outlined';
  className?: string;
  children: ReactNode;
}

function Card({ variant = 'default', className, children }: CardProps) {
  return (
    <CardContext.Provider value={{ variant }}>
      <div
        className={cn(
          'rounded-lg bg-card text-card-foreground',
          variant === 'outlined' && 'border',
          variant === 'default' && 'shadow-sm',
          className,
        )}
      >
        {children}
      </div>
    </CardContext.Provider>
  );
}

function CardHeader({ className, children }: { className?: string; children: ReactNode }) {
  return <div className={cn('flex flex-col space-y-1.5 p-6', className)}>{children}</div>;
}

function CardTitle({ className, children }: { className?: string; children: ReactNode }) {
  return (
    <h3 className={cn('text-2xl font-semibold leading-none tracking-tight', className)}>
      {children}
    </h3>
  );
}

function CardContent({ className, children }: { className?: string; children: ReactNode }) {
  return <div className={cn('p-6 pt-0', className)}>{children}</div>;
}

function CardFooter({ className, children }: { className?: string; children: ReactNode }) {
  return <div className={cn('flex items-center p-6 pt-0', className)}>{children}</div>;
}

Card.Header = CardHeader;
Card.Title = CardTitle;
Card.Content = CardContent;
Card.Footer = CardFooter;

export { Card };
