/**
 * TypeScript API contracts matching FastAPI backend schemas exactly.
 */

export interface HealthLiveResponse {
  status: "alive";
  timestamp: string;
}

export interface HealthReadyResponse {
  status: "ready" | "not_ready";
  models_loaded: boolean;
  datasets_loaded: boolean;
  details: {
    models?: string;
    datasets?: {
      prices_count?: number;
      cost_records_count?: number;
    };
    [key: string]: unknown;
  };
  timestamp: string;
}

export interface CandidateCrop {
  crop: string;
  display_name: string;
  category: string;
  confidence_score: number;
  probability: number;
  description: string;
}

export interface CropRecommendationRequest {
  n: number;
  p: number;
  k: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
  top_k?: number;
}

export interface CropRecommendationResponse {
  primary_crop: string;
  display_name: string;
  confidence_percent: number;
  category: string;
  description: string;
  recommendations: CandidateCrop[];
  soil_advisory_notes: string[];
  model_used: string;
}

export interface SupportedCrop {
  canonical_name: string;
  display_name: string;
  category: string;
  yield_crop?: string | null;
  price_crop?: string | null;
  cost_crop?: string | null;
  default_season: string;
  default_soil: string;
  default_fertilizer: number;
  default_pesticide: number;
  description: string;
}

export interface YieldPredictionRequest {
  crop: string;
  season?: string;
  soil_type?: string;
  state?: string;
  temperature?: number;
  rainfall?: number;
  humidity?: number;
  ph?: number;
  nitrogen?: number;
  phosphorus?: number;
  potassium?: number;
  fertilizer?: number;
  pesticide?: number;
}

export interface YieldPredictionResponse {
  crop: string;
  mapped_yield_crop: string;
  prediction_method: string;
  predicted_yield_kg_ha: number;
  predicted_yield_quintals_ha: number;
  predicted_yield_kg_acre: number;
  predicted_yield_quintals_acre: number;
  historical_min_kg_ha: number;
  historical_median_kg_ha: number;
  historical_max_kg_ha: number;
}

export interface YieldBenchmark {
  crop: string;
  min_kg_ha: number;
  median_kg_ha: number;
  max_kg_ha: number;
}

export interface PriceInfo {
  canonical_name: string;
  matched_crop_name: string;
  modal_rs_per_quintal: number;
  min_rs_per_quintal: number;
  max_rs_per_quintal: number;
  msp_rs_per_quintal: number | null;
  price_per_kg: number;
  source: string;
}

export interface MarketPriceListResponse {
  total_records: number;
  prices: PriceInfo[];
}

export interface CultivationCostRequest {
  crop_name: string;
  state_name?: string | null;
}

export interface CultivationCostResponse {
  canonical_name: string;
  matched_cost_crop: string;
  applied_state: string;
  cul_cost_c2_per_ha: number;
  cul_cost_c2_per_acre: number;
  prod_cost_c2_per_quintal: number;
  seed_cost_per_ha: number;
  fertilizer_cost_per_ha: number;
  labor_cost_per_ha: number;
  machinery_cost_per_ha: number;
  source: string;
}

export interface StatesListResponse {
  states: string[];
}

export interface FinancialAnalysisRequest {
  yield_kg_per_ha: number;
  farm_area: number;
  area_unit?: "acre" | "hectare" | "bigha";
  price_per_quintal?: number;
  cost_per_ha?: number;
}

export interface FinancialAnalysisResponse {
  input_area: number;
  input_unit: string;
  area_hectares: number;
  area_acres: number;
  yield_kg_per_ha: number;
  yield_quintals_per_ha: number;
  yield_kg_per_acre: number;
  yield_quintals_per_acre: number;
  total_production_kg: number;
  total_production_quintals: number;
  price_per_quintal: number;
  price_per_kg: number;
  cost_per_ha: number;
  cost_per_acre: number;
  total_revenue: number;
  total_cost: number;
  net_profit: number;
  profit_per_acre: number;
  profit_per_ha: number;
  roi_percent: number;
  profit_margin_percent: number;
  breakeven_yield_kg_per_ha: number;
  breakeven_price_per_quintal: number;
  formatted_revenue: string;
  formatted_cost: string;
  formatted_profit: string;
  formatted_profit_per_acre: string;
  formatted_profit_per_ha: string;
  formatted_revenue_short: string;
  formatted_cost_short: string;
  formatted_profit_short: string;
}

export interface FullAdvisoryRequest {
  n: number;
  p: number;
  k: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
  state?: string;
  soil_type?: string;
  season?: string;
  farm_area?: number;
  area_unit?: string;
  top_k?: number;
}

export interface FullAdvisoryResponse {
  recommendation: CropRecommendationResponse;
  yield_prediction: YieldPredictionResponse;
  market_price: PriceInfo;
  cultivation_cost: CultivationCostResponse;
  financials: FinancialAnalysisResponse;
  metadata: {
    state: string;
    season: string;
    soil_type: string;
    farm_area: number;
    area_unit: string;
    timestamp: string;
    [key: string]: unknown;
  };
}

export interface ApiErrorResponse {
  error_code: string;
  message: string;
  request_id: string;
  details?: Array<{ field: string; message: string; type: string }> | string | null;
  timestamp?: string;
}

export interface LocationMetadataResponse {
  latitude: number;
  longitude: number;
  locality?: string | null;
  district?: string | null;
  state?: string | null;
  canonical_state?: string | null;
  country?: string | null;
  source: string;
  data_category: string;
}

export interface WeatherDataResponse {
  temperature_c?: number | null;
  humidity_pct?: number | null;
  precipitation_mm?: number | null;
  two_week_rainfall_mm?: number | null;
  observation_time: string;
  source: string;
  data_category: string;
  status: string;
  error_message?: string | null;
}

export interface SoilEstimateDataResponse {
  ph?: number | null;
  soil_type_hint?: string | null;
  source: string;
  data_category: string;
  status: string;
  caveat: string;
  error_message?: string | null;
}

export interface GeoSensingResponse {
  location: LocationMetadataResponse;
  weather: WeatherDataResponse;
  soil: SoilEstimateDataResponse;
  timestamp: string;
  overall_status: string;
}

export interface StressSimulationRequest {
  crop: string;
  season?: string;
  soil_type?: string;
  state?: string;
  farm_area: number;
  area_unit?: "acre" | "hectare" | "bigha";
  base_rainfall_mm: number;
  base_temperature_c?: number;
  base_humidity_pct?: number;
  base_ph?: number;
  base_nitrogen?: number;
  base_phosphorus?: number;
  base_potassium?: number;
  base_fertilizer?: number;
  base_pesticide?: number;
  base_price_per_quintal: number;
  base_cost_per_ha: number;
  rainfall_shock_percent: number;
  price_shock_percent: number;
  cost_shock_percent?: number;
  pmfby_indemnity_level?: number;
}

export interface PMFBYSimulationResponse {
  indemnity_level: number;
  threshold_yield_kg_ha: number;
  actual_simulated_yield_kg_ha: number;
  is_claim_triggered: boolean;
  shortfall_ratio: number;
  sum_insured_inr: number;
  farmer_premium_rate_percent: number;
  farmer_premium_inr: number;
  estimated_claim_inr: number;
  net_position_with_insurance_inr: number;
  formatted_claim_inr: string;
  formatted_premium_inr: string;
  formatted_net_position_inr: string;
  guideline_reference: string;
  caveat: string;
}

export interface ScenarioComparisonResponse {
  base_rainfall_mm: number;
  simulated_rainfall_mm: number;
  rainfall_shock_percent: number;

  base_price_per_quintal: number;
  simulated_price_per_quintal: number;
  price_shock_percent: number;

  base_yield_kg_ha: number;
  simulated_yield_kg_ha: number;
  yield_delta_kg_ha: number;
  yield_delta_percent: number;

  base_total_revenue: number;
  simulated_total_revenue: number;
  revenue_delta: number;

  base_total_cost: number;
  simulated_total_cost: number;

  base_net_profit: number;
  simulated_net_profit: number;
  profit_delta: number;
  profit_delta_percent: number;

  base_roi_percent: number;
  simulated_roi_percent: number;

  pmfby_insurance: PMFBYSimulationResponse;
  data_category: string;
}
