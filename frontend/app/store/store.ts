import { create } from 'zustand';

export interface PropertyForm {
  property_address: string;
  property_type: string;
  area_sqft: number;
  age_years: number;
  zone: string;
}

interface AppState {
  form: PropertyForm;
  result: any | null;
  loading: boolean;
  activeScenario: string;
  setForm: (form: Partial<PropertyForm>) => void;
  setResult: (result: any) => void;
  setLoading: (loading: boolean) => void;
  setActiveScenario: (scenario: string) => void;
  evaluateAsset: (scenario?: string) => Promise<void>;
}

const initialForm: PropertyForm = {
  property_address: "Whitefield, Bangalore",
  property_type: "Residential Plot",
  area_sqft: 1200,
  age_years: 5,
  zone: "Whitefield, Bangalore"
};

export const useAppStore = create<AppState>((set, get) => ({
  form: initialForm,
  result: null,
  loading: false,
  activeScenario: "normal",
  setForm: (formUpdates) => set((state) => ({ form: { ...state.form, ...formUpdates } })),
  setResult: (result) => set({ result }),
  setLoading: (loading) => set({ loading }),
  setActiveScenario: (scenario) => set({ activeScenario: scenario }),
  evaluateAsset: async (scenario = "normal") => {
    set({ loading: true, activeScenario: scenario });
    const { form } = get();
    try {
      const payload = { ...form, scenario };
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL?.replace(/\/$/, "") || "";
      const endpoint = backendUrl ? `${backendUrl}/api/evaluate` : "/api/evaluate";
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!response.ok) throw new Error("API Failed");
      const data = await response.json();
      set({ result: data, loading: false });
    } catch (err) {
      console.error(err);
      const fallbackResult = {
        valuation: {
          market_value: 2800000,
          distress_value: 2100000,
          liquidity_days: 45,
        },
        risk: {
          risk_level: "Moderate",
          liquidity_score: 68,
        },
        decision: {
          decision: "APPROVED - AI-Adjusted",
          loan_amount: 1900000,
          interest_rate: 10.5,
          ltv: 0.68,
        },
        roi: {
          annualized_roi: 14.2,
        },
        simulation: {
          impact: {
            scenario: "market_crash_15pc",
            estimated_loss: 0.18,
            roi: { annualized_roi: 9.8 },
          },
        },
        recovery: {
          strategy: "Liquidity Buffer + Speed Sale",
        },
        compliance: {
          rbi_compliant: true,
          audit_id: "demo-fallback-0001",
        },
        executive_summary: {
          decision: "APPROVED - fallback demo result",
          loan_amount: 1900000,
          interest_rate: 10.5,
          roi: 14.2,
          one_line: "Fallback evaluation active because backend was unavailable.",
          worst_case: "Worst-case market crash ROI drops to 9.8%.",
        },
      };
      set({ result: fallbackResult, loading: false });
      // In a real app we'd show an error state, but here we can rely on mock or just let the dashboard handle missing data.
    }
  }
}));
