import React, { Suspense, lazy } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Layout } from "./components/layout/Layout";

const OverviewPage = lazy(() =>
  import("./pages/OverviewPage").then((m) => ({ default: m.OverviewPage }))
);
const CropRecommendationPage = lazy(() =>
  import("./pages/CropRecommendationPage").then((m) => ({
    default: m.CropRecommendationPage,
  }))
);
const YieldPredictionPage = lazy(() =>
  import("./pages/YieldPredictionPage").then((m) => ({
    default: m.YieldPredictionPage,
  }))
);
const MarketIntelligencePage = lazy(() =>
  import("./pages/MarketIntelligencePage").then((m) => ({
    default: m.MarketIntelligencePage,
  }))
);
const FinancialAnalysisPage = lazy(() =>
  import("./pages/FinancialAnalysisPage").then((m) => ({
    default: m.FinancialAnalysisPage,
  }))
);
const CompositeAdvisoryPage = lazy(() =>
  import("./pages/CompositeAdvisoryPage").then((m) => ({
    default: m.CompositeAdvisoryPage,
  }))
);

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const RouteFallback: React.FC = () => (
  <div className="py-24 text-center font-mono text-xs text-ink-500 tracking-technical uppercase">
    <div className="inline-block p-4 border border-ink-900 bg-chalk-200 shadow-brutal-sm">
      SYNCHRONIZING ANALYTICAL SUBSYSTEM...
    </div>
  </div>
);

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Suspense fallback={<RouteFallback />}>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<OverviewPage />} />
              <Route path="recommend" element={<CropRecommendationPage />} />
              <Route path="yield" element={<YieldPredictionPage />} />
              <Route path="market" element={<MarketIntelligencePage />} />
              <Route path="financials" element={<FinancialAnalysisPage />} />
              <Route path="advisory" element={<CompositeAdvisoryPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </Suspense>
      </BrowserRouter>
    </QueryClientProvider>
  );
};
