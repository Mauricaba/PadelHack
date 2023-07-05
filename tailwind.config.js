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
  plugins: [
    require("flowbite/plugin"),
    require('@tailwindcss/forms'),
  ],
}

