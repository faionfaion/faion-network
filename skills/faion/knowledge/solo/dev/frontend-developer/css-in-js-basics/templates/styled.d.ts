// types/styled.d.ts — DefaultTheme augmentation for styled-components
// This file is the ONE agents always forget; without it, theme is typed `any`
import 'styled-components';

declare module 'styled-components' {
  export interface DefaultTheme {
    colors: {
      primary: string;
      primaryHover: string;
      primaryForeground: string;
      secondary: string;
      secondaryForeground: string;
      background: string;
      foreground: string;
      muted: string;
      border: string;
      focus: string;
    };
    space: {
      xs: string;
      sm: string;
      md: string;
      lg: string;
      xl: string;
    };
    radii: {
      sm: string;
      md: string;
      lg: string;
      full: string;
    };
  }
}
