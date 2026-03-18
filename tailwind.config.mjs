export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Macro (NatureForce)
        'cream-primary': '#F5EFE0',
        'cream-dark': '#EDE4D0',
        'forest-deep': '#1A3D2B',
        // Micro (Vive La Palma)
        'void-primary': '#0F1A15',
        'slate-primary': '#2C3330',
        // Shared
        'brass-primary': '#C5B388',
      },
      fontFamily: {
        'fraunces': ['Fraunces', 'serif'],
        'syne': ['Syne', 'sans-serif'],
        'garamond': ['"EB Garamond"', 'serif'],
        'inter': ['Inter', 'sans-serif'],
        'jetbrains': ['"JetBrains Mono"', 'monospace'],
      }
    },
  },
  plugins: [],
}