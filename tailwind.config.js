/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./templates/**/*.html",
      "./static/src/**/*.js",
      "./node_modules/flowbite/**/*.js",
      "./src/**/*.{html,js}",
  ],
  theme: {
    extend: {,
  },
    colors: {
      'oscurito': '#011b35',
      'azul': '#003b57',
      'celeste': '#9dc3d7',
      'celestito': '#d2dfe6',
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
}

