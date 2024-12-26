/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#121212", // Deep Gray/Black for background
        textPrimary: "#E0E0E0", // Soft white for text
        textSecondary: "#A0A0A0", // Dim gray for secondary text
        inputBg: "#2E2E2E", // Input and chat box background
        buttonPrimary: "#3B82F6", // Blue for primary buttons
        buttonHover: "#0056B3", // Darker blue for hover states
        chatBubble: "#3A3A3A", // Chat bubble background
        border: "#4A4A4A",
      },
      animation: {
        bounceSmooth: "smoother end",
      },
      keyframes: {
        bounceSmooth: {
          "0%": { transform: "translateY(0)", opacity: "1" },
          "50%": { transform: "translateY(-10px)", opacity: "1" }, // Move up a bit
          "100%": { transform: "translateY(0)", opacity: "1" }, // Return to original position
        },
      },
    },
  },
  darkMode: "class", // or 'media'
  plugins: [],
};
