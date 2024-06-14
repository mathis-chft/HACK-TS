/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      boxShadow: {
        'YOWL' : '0px 0px 44px 4px rgba(0,0,0,0.09)',
        'YOWL-dark' : '0px 0px 44px 4px rgba(0,0,0,0.18)',
      }
    },
  },
}
