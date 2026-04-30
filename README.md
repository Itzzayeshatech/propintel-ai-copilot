# PropIntel AI Copilot 🚀
### NBFC-Grade Collateral Evaluation & Risk Intelligence

**PropIntel AI Copilot** is a production-ready decision intelligence system designed for NBFCs (like Poonawalla Fincorp). It replaces static, manual collateral checks with an autonomous, formula-driven engine that evaluates property value, risk resilience, and risk-adjusted ROI in real-time.

---

## 🎯 The Problem
Traditional lending systems often fail to account for:
- **Dynamic Market Volatility**: Static valuations don't reflect sudden market crashes.
- **Micro-Market Liquidity**: Property value is meaningless if the asset cannot be liquidated.
- **Explainability**: Black-box AI models don't meet RBI's compliance requirements for auditability.

## 💡 The Solution
A "Stress-First" decision engine that simulates adverse scenarios **before** disbursement, providing structured, explainable rationale for every decision.

---

## 🛠️ Architecture: The Decision Pipeline
The system follows a linear, enriched data pipeline:
1. **Valuation Engine**: Calculates baseline LTV and micro-market liquidity.
2. **Stress Engine (Centerpiece)**: Simulates Market Crash (-15%), Rate Spikes (+2%), and Liquidity Drops.
3. **ROI Engine**: Computes Risk-Adjusted ROI: `Interest Income - (Default Probability × Loss)`.
4. **Decision Engine**: Multi-factor risk scoring (APPROVE / CONDITIONAL / REJECT).
5. **Explainability Module**: Generates RBI-compliant structured rationale.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+

### Backend Setup (FastAPI)
```bash
cd app
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Setup (Next.js)
```bash
cd frontend
npm install
npm run dev
```

---

## 📡 API Contract (POST `/api/v1/analyze-loan`)

### Request Body
```json
{
  "location": "Whitefield",
  "property_value": 8500000,
  "loan_amount": 6000000,
  "stress_market_crash": true,
  "stress_rate_spike": false,
  "stress_liquidity_drop": false
}
```

### Sample Response
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "risk_level": "HIGH",
  "ltv": 82.5,
  "roi": 8.4,
  "decision": "CONDITIONAL",
  "explainability": {
    "risk_factors": { "ltv": 70.5, "liquidity": 0.65, "volatility": 0.15 },
    "explanations": ["Under stress, LTV exceeds safety threshold."],
    "scenario_impact": "Market crash pushed LTV from 70% to 82%."
  },
  "stress_impact": {
    "ltv": { "base_value": 70.5, "stressed_value": 82.5, "delta": 12.0 }
  },
  "response_time_ms": 124.5
}
```

---

## 🏆 Hackathon Winning Features
- ✅ **Stress Engine**: Real-time simulation of economic shocks.
- ✅ **RBI Compliant**: Structured "Explainability" rationale for auditors.
- ✅ **Performance**: Decision latency < 200ms.
- ✅ **Premium UI**: Dark-mode dashboard with "Before vs After" impact analysis.

---
© 2026 PropIntel AI. Built for the Future of NBFC Lending.
