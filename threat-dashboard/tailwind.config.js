/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          dark: '#0a0a0f',
          panel: '#151520',
          accent: '#00f0ff',
          alert: '#ff003c',
          text: '#e0e0e0',
          muted: '#8e8e9f'
        }
      }
    },
  },
  plugins: [],
}
