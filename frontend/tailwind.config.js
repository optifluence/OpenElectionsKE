/**
 * Tailwind CSS Configuration for OpenElectionsKe
 * - Comprehensive color palette for trust, calmness, tech, urgency, and accents
 * - Modern, readable typefaces
 * - Easily extendable for future contributors
 */

const defaultTheme = require('tailwindcss/defaultTheme');
const { colors, fontFamily } = require('./theme');

module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx,html}',
    './public/index.html',
  ],
  theme: {
    extend: {
      fontFamily,
      colors,
    },
  },
  plugins: [],
};
