// theme.ts
// Central theme file for OpenElectionsKe (colors, fonts, etc.)
// Extend this file for all design tokens and reuse in both Tailwind and JS/TS code

export const colors = {
  primary: {
    50:  '#e0f2fe',
    100: '#bae6fd',
    200: '#7dd3fc',
    300: '#38bdf8',
    400: '#0ea5e9',
    500: '#2563eb', // Main blue
    600: '#1e40af', // Deep blue
    700: '#1d4ed8',
    800: '#1e3a8a',
    900: '#172554',
  },
  accent: {
    50:  '#fff7ed',
    100: '#ffedd5',
    200: '#fed7aa',
    300: '#fdba74',
    400: '#fb923c',
    500: '#f59e42', // Main accent (orange)
    600: '#ea580c',
    700: '#c2410c',
    800: '#9a3412',
    900: '#7c2d12',
  },
  tech: {
    50:  '#f3f4f6',
    100: '#e5e7eb',
    200: '#d1d5db',
    300: '#9ca3af',
    400: '#6b7280',
    500: '#374151',
    600: '#1f2937',
    700: '#111827',
  },
  success: {
    50:  '#dcfce7',
    100: '#bbf7d0',
    200: '#86efac',
    300: '#4ade80',
    400: '#22c55e', // Emerald
    500: '#16a34a',
    600: '#15803d',
    700: '#166534',
  },
  warning: {
    50:  '#fef9c3',
    100: '#fef08a',
    200: '#fde047',
    300: '#facc15', // Amber
    400: '#eab308',
    500: '#ca8a04',
  },
  error: {
    50:  '#fee2e2',
    100: '#fecaca',
    200: '#fca5a5',
    300: '#f87171',
    400: '#ef4444',
    500: '#dc2626', // Red
    600: '#b91c1c',
  },
};

export const fontFamily = {
  sans: [
    'Inter',
    'Roboto',
    'Open Sans',
    'sans-serif',
  ],
};
