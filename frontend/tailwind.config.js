/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        obsidian: {
          950: "#F7F5EF", // Page background: warm ivory
          900: "#FFFFFF", // Cards and panels: white
          850: "#EAF0E6", // Soft green backgrounds / elevated cards
          800: "#E3E6DF", // Borders and dividers
          750: "#E3E6DF", // Distinct borders
          700: "#D6DAD1", // Interactive borders / subtle outline
          650: "#CBD2C5", // Accent borders
          600: "#789477", // Muted sage / secondary green
          500: "#789477", // Secondary green / icons
          400: "#647568", // Secondary text / muted labels
          300: "#647568", // Secondary text
        },
        ink: {
          950: "#202820",
          900: "#202820",
          850: "#202820",
          800: "#202820",
          700: "#202820",
          600: "#354238",
          500: "#647568",
          400: "#647568",
        },
        chalk: {
          50: "#202820", // Main text
          100: "#202820", // Main text
          200: "#202820", // Main text
          300: "#354238", // Slightly softer text
          400: "#647568", // Secondary text
          500: "#647568", // Secondary text
        },
        paper: {
          100: "#FFFFFF",
          200: "#EAF0E6",
          300: "#E3E6DF",
          ink: "#202820",
        },
        signal: {
          red: "#244B35", // Primary green (forest green)
          darkred: "#193A28", // Primary hover
          lime: "#789477", // Secondary green (muted sage)
          mint: "#EAF0E6", // Soft green background
          amber: "#A66B18", // Warning
          green: "#357A4A", // Success
          blue: "#244B35",
          error: "#B54747", // Error
        },
        borderMuted: "#E3E6DF",
        borderLight: "#E3E6DF",
      },
      fontFamily: {
        display: ['"Space Grotesk"', "Inter", "-apple-system", "sans-serif"],
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
        mono: ['"JetBrains Mono"', "ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
      },
      letterSpacing: {
        tighter: "-0.05em",
        tight: "-0.025em",
        technical: "0.08em",
        broadcast: "0.15em",
        widecode: "0.18em",
      },
      borderRadius: {
        none: "0px",
      },
      boxShadow: {
        brutal: "2px 2px 0px 0px rgba(32, 40, 32, 0.08)",
        "brutal-red": "2px 2px 0px 0px #244B35",
        "brutal-neon": "2px 2px 0px 0px #789477",
        "brutal-chalk": "2px 2px 0px 0px #E3E6DF",
        "brutal-subtle": "1px 1px 0px 0px rgba(32, 40, 32, 0.06)",
        neon: "0 0 10px rgba(36, 75, 53, 0.12)",
        "neon-sm": "0 0 5px rgba(36, 75, 53, 0.08)",
      },
    },
  },
  plugins: [],
};
