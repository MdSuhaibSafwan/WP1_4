/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')
module.exports = {
  content: [
      './**/templates/**/*.html',
      './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      colors : {
        red:colors.red,
        green:colors.green,
        blue:colors.blue,
        gray:colors.gray,
        sky:colors.sky,
        },
    },
  },
  plugins: [
  require('flowbite/plugin')
    ],
  
  safelist: 
[
    'bg-red-500',
    'text-3xl',
    'lg:text-4xl',
    'text-green-800',
    'border-green-300',
    'bg-green-50',
    'bg-gray-800',
    'dark:text-green-400',
    'dark:border-green-8000',
    'text-red-800',
    'border-red-300',
    'bg-red-50',
    'dark:bg-gray-800',
    'dark:text-red-400',
    'dark:border-red-800',
    'bg-white border', 
    'border-gray-200',
    'bg-gradient-to-r',
    'from-teal-200',
    'to-lime-200',
    'bg-gray-400',
    'from-purple-600',
    'to-blue-500',
    'bg-sky-200',
 ]
}

