# PropIntel AI Copilot
### NBFC-Grade Collateral Evaluation & Risk Intelligence

**PropIntel AI Copilot** is a production-ready decision intelligence system designed for NBFCs. It replaces static, manual collateral checks with an autonomous, formula-driven engine that evaluates property value, risk resilience, and risk-adjusted ROI in real-time.

---

## The Problem
Traditional lending systems fail to account for:
- **Dynamic Market Volatility**: Static valuations don't reflect sudden market crashes.
- **Micro-Market Liquidity**: Property value is meaningless if the asset cannot be liquidated.
- **Explainability**: Black-box AI models don't meet RBI's compliance requirements for auditability.

## The Solution
A **Stress-First Decision Engine** that simulates adverse macro-economic scenarios **before** disbursement, providing structured, explainable rationale for every decision.

---

## Architecture: The Decision Pipeline

```
Input -> Policy Rules -> Valuation -> Stress Engine -> ROI -> Decision -> Explainability
           (DTI, Credit)   (LTV)      (Market/Sector)  (PD)  (Approve)   (Audit Trace)
```

### Core Engines
| Engine | Function |
| :--- | :--- |
| **Valuation** | Derives `market_property_value` using micro-market price index. Calculates `base_ltv`. |
| **Stress** | Simulates Market Crash (-15%), Sector Crisis (-15%), Inflation (-5% + liquidity shock), Repo Rate Spike (+2%). Outputs `stressed_property_value` and `stress_ltv`. |
| **ROI** | Risk-Adjusted Yield: `interest_income - (PD x LGD)`. Segment-specific default probabilities. |
| **Decision** | Hard boundary checks on stress LTV + liquidity + policy rules. |
| **Explainability** | Simplified (3 factors, 1 line) + Audit Trace (5-stage pipeline lineage). |

---

## API Contract

### `POST /api/v1/analyze-loan`

#### Request
```json
{
  "location": "Whitefield",
  "property_value": 8500000,
  "loan_amount": 6000000,
  "monthly_income": 150000,
  "credit_score": 750,
  "segment": "SALARIED",
  "stress_market_crash": true,
  "stress_repo_rate_spike": true,
  "stress_inflation_spike": false,
  "stress_sector_crash": false
}
```

#### Response
```json
{
  "request_id": "bf4e3f79-e5c1-440c-936f-fa54d7720098",
  "decision": "APPROVE",
  "risk_level": "LOW",
  "roi": 11.1,
  "collateral": {
    "market_property_value": 10200000,
    "stressed_property_value": 8670000,
    "property_value_drop_pct": 15.0,
    "base_ltv": 58.82,
    "stress_ltv": 69.2
  },
  "simplified_explainability": {
    "key_risk_factors": [
      "Collateral value erodes by 15% under active stress scenarios"
    ],
    "stress_impact_summary": "Market stress compresses collateral from INR 1.02Cr to INR 0.87Cr, pushing LTV up by +10.4%.",
    "decision_rationale": "Approved - collateral cover remains adequate under all modelled stress scenarios."
  },
  "audit_mode": {
    "triggered_rules": [],
    "risk_reasoning_chain": [
      "Stage 1 - Valuation: Asset valued using micro-market price index.",
      "Stage 2 - Stress: Macro-economic scenarios applied.",
      "Stage 3 - Risk: Portfolio risk classified as 'LOW'.",
      "Stage 4 - ROI: Net yield calculated.",
      "Stage 5 - Decision: Final recommendation issued."
    ],
    "compliance_check": "PASSED - Proceed with standard disbursement workflow."
  },
  "stress_impact": { "..." : "base vs stressed deltas" },
  "response_time_ms": 0.42
}
```

---

## Getting Started

### Backend (FastAPI)
```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

---

## Key Features
- **Collateral Snapshot**: Explicit `market_property_value` vs `stressed_property_value` with drop %.
- **Macro-Stress Simulation**: Market Crash, Sector Crisis, Inflation Shock, Repo Rate Spike.
- **Segment-Based Risk**: Salaried (1.0x PD), Self-Employed (1.4x), MSME (1.8x).
- **Policy Rules Engine**: DTI ceiling, Credit Score floor.
- **RBI Audit Mode**: Full 5-stage decision lineage with compliance verdict.
- **Sub-1ms Response**: Deterministic computation, no external API calls.

---

(c) 2026 PropIntel AI. Built for NBFC Lending Intelligence.
