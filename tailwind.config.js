/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./templates/**/*.html",
      "./static/src/**/*.js",
      "./node_modules/flowbite/**/*.js",
      "./src/**/*.{html,js}",
  ],
  theme: {
    extend: {},
  },
  colors: {
    'darkblue': '#011b35',
    'blue': '#003b57',
    'cian': '#9dc3d7',
    'lightblue': '#d2dfe6',
    'casiwhite': '#fafefd',

  },
  fontFamily: {
    sans: ['Graphik', 'sans-serif'],
    serif: ['Merriweather', 'serif'],
  },
  plugins: [
    require("flowbite/plugin"),
    require('@tailwindcss/forms'),
  ],
}

