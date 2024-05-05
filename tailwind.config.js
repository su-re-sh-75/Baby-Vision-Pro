/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./Baby_app/templates/**/*.html",
    "./users/templates/**/*.html",
    './node_modules/flowbite/**/*.js'
    ],
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
      primary: {"50":"#faf5ff","100":"#f3e8ff","200":"#e9d5ff","300":"#d8b4fe","400":"#c084fc","500":"#a855f7","600":"#9333ea","700":"#7e22ce","800":"#6b21a8","900":"#581c87","950":"#3b0764"}
      }
    },
      fontFamily: {
        'body': [
      'Montserrat', 
      'ui-sans-serif', 
      'system-ui', 
      '-apple-system', 
      'system-ui', 
      'Segoe UI', 
      'Roboto', 
      'Helvetica Neue', 
      'Arial', 
      'Noto Sans', 
      'sans-serif', 
      'Apple Color Emoji', 
      'Segoe UI Emoji', 
      'Segoe UI Symbol', 
      'Noto Color Emoji'
    ],
        'sans': [
      'Montserrat', 
      'ui-sans-serif', 
      'system-ui', 
      '-apple-system', 
      'system-ui', 
      'Segoe UI', 
      'Roboto', 
      'Helvetica Neue', 
      'Arial', 
      'Noto Sans', 
      'sans-serif', 
      'Apple Color Emoji', 
      'Segoe UI Emoji', 
      'Segoe UI Symbol', 
      'Noto Color Emoji'
        ]
    },
    },
  plugins: [
    require('@tailwindcss/forms'),
    require('flowbite/plugin'),
    'prettier-plugin-tailwindcss'
  ],
}

