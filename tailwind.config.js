/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js",
    // set path to list css classes at forms.py
    "./src/**/forms.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [
      require('flowbite/plugin')
  ]
}
