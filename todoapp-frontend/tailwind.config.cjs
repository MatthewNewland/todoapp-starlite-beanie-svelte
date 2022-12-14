/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{ts,js,css,svelte,html}"],
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/forms")
  ],
}
