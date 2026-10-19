/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        obsidian: {
          950: "#060709",
          900: "#0A0C10",
          850: "#101319",
          800: "#161A22",
          750: "#1D222E",
          700: "#262C3A",
          650: "#31384A",
          600: "#414A60",
          500: "#606D8A",
          400: "#8694B0",
          300: "#AEBAD1",
        },
        ink: {
          950: "#060709",
          900: "#0A0C10",
          850: "#101319",
          800: "#161A22",
          700: "#262C3A",
          600: "#414A60",
          500: "#606D8A",
          400: "#8694B0",
        },
        chalk: {
          50: "#FFFFFF",
          100: "#F5F4EF",
          200: "#EAE8E1",
          300: "#DCD9CE",
          400: "#B8B4A5",
          500: "#8C887A",
        },
        paper: {
          100: "#F5F3EC",
          200: "#EAE7DD",
          300: "#DDD9CC",
          ink: "#08090C",
        },
        signal: {
          red: "#FF2A2A",
          darkred: "#D41919",
          amber: "#F59E0B",
          green: "#22C55E",
          blue: "#3B82F6",
        },
        borderMuted: "#1F2432",
        borderLight: "#2E3648",
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
        brutal: "3px 3px 0px 0px #000000",
        "brutal-red": "3px 3px 0px 0px #FF2A2A",
        "brutal-chalk": "3px 3px 0px 0px #EAE8E1",
        "brutal-subtle": "2px 2px 0px 0px rgba(0, 0, 0, 0.7)",
      },
    },
  },
  plugins: [],
};
