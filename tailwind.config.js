/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./Baby_app/templates/**/*.html"],
  theme: {
    extend: {
      colors:{
        'baby-red':{
          900:"#BE3857",
          800:"#C89099",
          700:"#E3BFC4"
        }
      }
    },
  },
  plugins: [],
}

