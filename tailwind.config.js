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
        },
        'maroon-flush': {
          '50': '#fcf3f6',
          '100': '#fae9ef',
          '200': '#f6d4e0',
          '300': '#efb2c6',
          '400': '#e581a0',
          '500': '#d95b7e',
          '600': '#be3857',
          '700': '#aa2c45',
          '800': '#8d273a',
          '900': '#762534',
          '950': '#47101a',
      },
      
      }
    },
  },
  plugins: ['prettier-plugin-tailwindcss'],
}

