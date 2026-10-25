---
name: farmer-first-ui
description: "Guidelines and verification rules for user interfaces designed for agricultural producers and field workers. Enforces minimal UI, absence of engineering jargon, high-contrast readable layouts, multi-language accessibility, and honest data presentation."
---

# Farmer-First UI Standard

This skill establishes the user experience, language, accessibility, and visual guidelines for the Karpo frontend and presentation layers.

## 1. Core Farmer-First Design Principles
1. **Decision Utility**: Every visual component must directly help the farmer make a practical decision (what to plant, expected yield, anticipated costs, expected mandi return, risk factors). If an element does not aid decision-making, remove it.
2. **Plain Agronomic Language**: Use vocabulary familiar to cultivators (e.g., "Recommended Crop", "Expected Harvest", "Wholesale Mandi Rate", "Total Cultivation Cost", "Net Profit").
3. **Strict Ban on Developer & Engineering Jargon**:
   - Never show HTTP status codes, routes (`/api/v1/...`), curl commands, or JSON responses in user screens.
   - Never show raw machine learning terms like `XGBRegressor`, `hyperparameters`, `tree depth`, `feature vector`, or pickle file paths.
   - Never show raw traceback errors. Instead show: `"Unable to fetch current market rates. Please check your connection or enter price manually."`

## 2. Information Hierarchy
- **Primary Hero**: Clear recommendation badge with primary crop name, localized name, and season compatibility.
- **Secondary Decision Drivers**:
  - Projected Yield (quintals/acre or tonnes/ha).
  - Economic Breakdown: Estimated Cost vs Expected Revenue = Net Profit/Loss (in ₹).
- **Actionable Agronomic Guidance**: Key field actions (e.g., recommended sowing window, basal fertilizer requirement).
- **Contextual Signals**: Clear badges distinguishing whether inputs came from live GPS/Weather or manual entry.

## 3. High-Contrast and Mobile Usability in Field Conditions
- Field workers and farmers often operate devices under direct sunlight.
- Ensure minimum contrast ratios (WCAG AAA for primary text, AA for secondary).
- Large touch targets (minimum 44x44px for buttons, inputs, and selectors).
- Accessible keyboard and screen-reader navigable controls.

## 4. Multilingual & Localization Standards
- Support English, Hindi, and Marathi seamlessly across labels, crop names, units, and currency.
- Use regional currency symbols (`₹`) with Indian numbering conventions (lakhs/thousands where appropriate via `format_inr`).
- Ensure layout handles longer script expansion (Devanagari scripts often occupy 20-30% more horizontal width than English).

## 5. State Handling
- **Empty States**: Explain clearly what action is required (e.g., `"Enter your soil test values or use auto-detect to generate recommendations"`).
- **Loading States**: Purposeful, non-distracting loading indicators with plain explanation (e.g., `"Analyzing soil & weather parameters..."`).
- **Error States**: Non-blaming, non-technical recovery instructions with manual fallback options.
- **Unavailable Data States**: Honest indicators when specific third-party data is missing, allowing the rest of the application to function.
