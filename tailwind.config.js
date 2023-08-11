/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./templates/**/*.html",
      "./static/src/**/*.js",
      "./src/**/*.{html,js}",
  ],
  theme: {
    extend: {
  },
    colors: {
      'oscurito': '#011B35',
      'azul': '#003B57',
      'celeste': '#9DC3D7',
      'celestito': '#D2DFE6',
      'casiwhite': '#FAFEFD',
      'verde': '#D0FDD7'
  },
    fontFamily: {
      sans: ['Signika', 'sans-serif'],
      serif: ['Asap', 'sans-serif'],
      mplus: ['"M PLUS Rounded 1c"', 'sans-serif'],
  },
    plugins: [
      require("@tailwindcss/forms"),
      // require("@tailwindcss/typography"),
      // require("@tailwindcss/aspect-ratio"),
      // require("@tailwindcss/line-clamp")
  ],
  }
}

