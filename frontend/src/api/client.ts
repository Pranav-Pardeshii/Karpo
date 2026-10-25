import {
  ApiErrorResponse,
  CropRecommendationRequest,
  CropRecommendationResponse,
  CropRotationResponse,
  CultivationCostRequest,
  CultivationCostResponse,
  FinancialAnalysisRequest,
  FinancialAnalysisResponse,
  FullAdvisoryRequest,
  FullAdvisoryResponse,
  GeoSensingResponse,
  HealthLiveResponse,
  HealthReadyResponse,
  IntercropOptionItem,
  LensInspectionResponse,
  MarketPriceListResponse,
  PriceInfo,
  RotationPlanRequest,
  ScenarioComparisonResponse,
  StatesListResponse,
  StressSimulationRequest,
  SupportedCrop,
  VoiceQueryRequest,
  VoiceQueryResponse,
  YieldBenchmark,
  YieldPredictionRequest,
  YieldPredictionResponse,
} from "../types/api";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "";
const API_PREFIX = `${BASE_URL}/api/v1`;

export class ApiError extends Error {
  errorCode: string;
  statusCode: number;
  requestId: string;
  details?: unknown;

  constructor(
    statusCode: number,
    errorCode: string,
    message: string,
    requestId: string,
    details?: unknown
  ) {
    super(message);
    this.name = "ApiError";
    this.statusCode = statusCode;
    this.errorCode = errorCode;
    this.requestId = requestId;
    this.details = details;
  }
}

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_PREFIX}${endpoint}`;
  const headers: Record<string, string> = {
    Accept: "application/json",
    ...((options?.headers as Record<string, string>) || {}),
  };

  if (!(options?.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 20000); // 20s timeout

  try {
    const response = await fetch(url, {
      ...options,
      headers,
      signal: options?.signal || controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      let errorData: ApiErrorResponse;
      try {
        errorData = await response.json();
      } catch {
        errorData = {
          error_code: `HTTP_${response.status}`,
          message: response.statusText || "An unexpected network error occurred.",
          request_id: "unknown",
        };
      }
      throw new ApiError(
        response.status,
        errorData.error_code || `HTTP_${response.status}`,
        errorData.message || "Request failed",
        errorData.request_id || "unknown",
        errorData.details
      );
    }

    return (await response.json()) as T;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error instanceof ApiError) {
      throw error;
    }
    if ((error as Error).name === "AbortError") {
      throw new ApiError(
        408,
        "REQUEST_TIMEOUT",
        "The operation timed out while waiting for inference calculation.",
        "timeout"
      );
    }
    throw new ApiError(
      500,
      "NETWORK_ERROR",
      (error as Error).message || "Unable to communicate with the agricultural intelligence backend.",
      "client-network"
    );
  }
}

export const api = {
  // Diagnostics
  getHealthLive: () => request<HealthLiveResponse>("/health/live"),
  getHealthReady: () => request<HealthReadyResponse>("/health/ready"),

  // Crop Recommendation
  recommendCrops: (payload: CropRecommendationRequest) =>
    request<CropRecommendationResponse>("/crops/recommend", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getSupportedCrops: () => request<SupportedCrop[]>("/crops/supported"),

  getCropByName: (cropName: string) =>
    request<SupportedCrop>(`/crops/${encodeURIComponent(cropName)}`),

  // Yield Forecasting
  predictYield: (payload: YieldPredictionRequest) =>
    request<YieldPredictionResponse>("/yield/predict", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getYieldBenchmarks: () => request<YieldBenchmark[]>("/yield/benchmarks"),

  // Market Pricing
  getMarketPrices: (params?: { query?: string; limit?: number; offset?: number }) => {
    const searchParams = new URLSearchParams();
    if (params?.query) searchParams.set("query", params.query);
    if (params?.limit !== undefined) searchParams.set("limit", String(params.limit));
    if (params?.offset !== undefined) searchParams.set("offset", String(params.offset));
    const queryStr = searchParams.toString();
    return request<MarketPriceListResponse>(`/market/prices${queryStr ? `?${queryStr}` : ""}`);
  },

  getMarketPriceForCrop: (cropName: string) =>
    request<PriceInfo>(`/market/prices/${encodeURIComponent(cropName)}`),

  // Cultivation Costs
  estimateCultivationCosts: (payload: CultivationCostRequest) =>
    request<CultivationCostResponse>("/cultivation-costs/estimate", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getCultivationStates: () => request<StatesListResponse>("/cultivation-costs/states"),

  // Financial Analysis
  calculateFinancials: (payload: FinancialAnalysisRequest) =>
    request<FinancialAnalysisResponse>("/financial-analysis", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // Integrated Full Advisory
  getFullAdvisory: (payload: FullAdvisoryRequest) =>
    request<FullAdvisoryResponse>("/advisory/full", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // Geo-Sensing Weather & Soil
  getGeoSensing: (latitude: number, longitude: number) =>
    request<GeoSensingResponse>(
      `/geo/climate-soil?latitude=${encodeURIComponent(latitude)}&longitude=${encodeURIComponent(
        longitude
      )}`
    ),

  // Climate & Market Stress Simulator
  simulateStress: (payload: StressSimulationRequest) =>
    request<ScenarioComparisonResponse>("/stress/simulate", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // Kisan Voice Copilot
  queryVoiceCopilot: (payload: VoiceQueryRequest) =>
    request<VoiceQueryResponse>("/voice/query", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // Karpo Lens: Crop Disease Assistance
  inspectCropImage: (formData: FormData) =>
    request<LensInspectionResponse>("/lens/inspect", {
      method: "POST",
      body: formData,
    }),

  // Crop Rotation & Intercropping Optimizer
  getRotationPlan: (payload: RotationPlanRequest) =>
    request<CropRotationResponse>("/rotation/plan", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getIntercroppingOptions: (crop: string) =>
    request<IntercropOptionItem[]>(`/rotation/intercropping/${encodeURIComponent(crop)}`),
};
