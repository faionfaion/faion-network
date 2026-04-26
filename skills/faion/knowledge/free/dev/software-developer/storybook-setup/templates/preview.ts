import type { Preview } from '@storybook/react';
import '../src/styles/globals.css';

const withTheme = (Story: any, context: any) => {
  const theme = context.globals.theme ?? 'light';
  return (
    <ThemeProvider defaultTheme={theme}>
      <Story />
    </ThemeProvider>
  );
};

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1a1a1a' },
      ],
    },
    viewport: {
      viewports: {
        mobile: { name: 'Mobile', styles: { width: '375px', height: '667px' } },
        tablet: { name: 'Tablet', styles: { width: '768px', height: '1024px' } },
        desktop: { name: 'Desktop', styles: { width: '1280px', height: '800px' } },
      },
    },
  },
  decorators: [withTheme],
  globalTypes: {
    theme: {
      name: 'Theme',
      defaultValue: 'light',
      toolbar: { icon: 'circlehollow', items: ['light', 'dark'], showName: true },
    },
  },
};

export default preview;
