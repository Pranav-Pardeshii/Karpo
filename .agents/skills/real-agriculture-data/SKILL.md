---
name: real-agriculture-data
description: "Guidelines and verification rules for agricultural, climate, and economic data integrity in Karpo. Enforces provenance, unit validation, distinction of estimates/predictions, and zero tolerance for fabricated fallback data."
---

# Real Agriculture Data Integrity Standard

This skill establishes the strict operational requirements for handling agricultural, climatic, geographic, and economic data across Karpo.

## 1. Data Classification and Provenance
Every piece of data processed or presented to users must have an explicit classification:
- **Observed**: Direct sensor or field measurements with recorded timestamp, sensor/provider ID, and geographic coordinates.
- **Historical**: Retrospective statistical records from verified datasets (e.g., CACP, Agmarknet, DES India) with explicit year/range bounds.
- **Forecast**: Predictive forecasts from verified atmospheric agencies (e.g., Open-Meteo, IMD, ECMWF) tagged with issuance timestamp and valid horizon.
- **Estimated**: Deterministic computations derived from validated agronomic formulas with documented parameters.
- **Predicted**: Outputs from loaded, serialized machine learning models (e.g., Random Forest Classifier, XGBoost Regressor) with explicit confidence or error bounds.
- **Simulated**: Scenario models based on explicit user-specified "what-if" parameters, explicitly tagged as hypothetical.
- **Unavailable**: Values that cannot currently be resolved from live providers or validated local datasets.

## 2. Mandatory Provenance Attributes
Whenever external data is ingested or stored:
1. **Source / Provider**: Identity of the provider (e.g., `Open-Meteo`, `Agmarknet`, `CACP C2`, `ISRIC SoilGrids`).
2. **Retrieval Timestamp**: UTC timestamp of retrieval.
3. **Reference Period**: Date, month, or season to which the data applies.
4. **Geographic Coverage**: Latitude/longitude, District, or State level resolution.
5. **Physical Units**: Explicit SI/agricultural units (e.g., `mm`, `°C`, `kg/ha`, `₹/quintal`, `₹/acre`).

## 3. Physical Plausibility and Agronomic Bounds Validation
Reject or flag out-of-bounds inputs:
- Soil Nitrogen ($N$): $0 \le N \le 300\text{ kg/ha}$
- Soil Phosphorus ($P$): $0 \le P \le 200\text{ kg/ha}$
- Soil Potassium ($K$): $0 \le K \le 350\text{ kg/ha}$
- Soil pH: $3.5 \le \text{pH} \le 10.0$
- Temperature: $0 \le T \le 55\text{ °C}$
- Relative Humidity: $5\% \le H \le 100\%$
- Rainfall: $0 \le R \le 4000\text{ mm}$
- Land Area: $A > 0\text{ acres or ha}$

## 4. Zero Fabricated Fallback Policy
- **Never replace API failures with fake numbers.** If weather or soil APIs timeout or fail, surface an `Unavailable` state and prompt the farmer for manual input.
- **Never show mock data as real.** Test fixtures and mocks must stay strictly inside test suites (`tests/`).
- **Never fabricate pesticide dosages, chemical treatments, or guaranteed insurance payouts.** Only cite authoritative agronomic advisory guidelines (e.g., ICAR, State Agricultural Universities).

## 5. Stale Data and Freshness Checks
- Market prices: Consider stale if older than 7 calendar days. Display freshness notice.
- Weather forecasts: Cache for up to 3 hours. Check freshness before display.
- Offline mode: If using cached data, explicitly label: `"Cached from [Date] - Reconnect for live rates"`.
