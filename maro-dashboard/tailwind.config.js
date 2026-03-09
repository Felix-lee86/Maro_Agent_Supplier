/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'bg-primary': '#0a0a0c',
                'bg-secondary': '#141416',
                'accent-primary': '#833ab4',
                'border-main': '#27272a',
            },
            backgroundImage: {
                'accent-gradient': 'linear-gradient(135deg, #833ab4 0%, #fd1d1d 50%, #fcb045 100%)',
            }
        },
    },
    plugins: [],
}
