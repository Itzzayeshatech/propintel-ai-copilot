from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from uuid import UUID
from enum import Enum


class BorrowerSegment(str, Enum):
    SALARIED      = "SALARIED"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    MSME          = "MSME"


# ── Request ────────────────────────────────────────────────────────────────────
class LoanRequest(BaseModel):
    # Core asset & loan
    location:       str   = Field(..., example="Whitefield")
    property_value: float = Field(..., example=8500000,
                                  description="Raw declared property value by borrower (INR)")
    loan_amount:    float = Field(..., example=6000000)

    # Borrower profile
    monthly_income: float          = Field(..., example=150000)
    credit_score:   int            = Field(..., example=750)
    segment:        BorrowerSegment = Field(default=BorrowerSegment.SALARIED)

    # Stress scenario flags
    stress_market_crash:    bool = Field(default=False, description="-15% on property value")
    stress_repo_rate_spike: bool = Field(default=False, description="+2% on repo / interest rates")
    stress_inflation_spike: bool = Field(default=False, description="-5% additional value, -40% liquidity")
    stress_sector_crash:    bool = Field(default=False, description="-15% additional on property value")


# ── Shared sub-models ──────────────────────────────────────────────────────────
class MetricComparison(BaseModel):
    base_value:     float
    stressed_value: float
    delta:          float


class AuditMode(BaseModel):
    triggered_rules:     List[str]
    risk_reasoning_chain: List[str]
    compliance_check:    str


class SimplifiedExplainability(BaseModel):
    key_risk_factors:     List[str]  # max 3
    stress_impact_summary: str       # 1 line
    decision_rationale:   str        # 1 line


# ── Collateral Valuation snapshot (new) ────────────────────────────────────────
class CollateralSnapshot(BaseModel):
    market_property_value:   float  # price_index-adjusted market value
    stressed_property_value: float  # after all stress multipliers applied
    property_value_drop_pct: float  # (market - stressed) / market * 100
    base_ltv:                float  # loan / market_property_value * 100
    stress_ltv:              float  # loan / stressed_property_value * 100


# ── Response ───────────────────────────────────────────────────────────────────
class LoanResponse(BaseModel):
    request_id:  UUID
    decision:    str   # APPROVE | CONDITIONAL | REJECT
    risk_level:  str   # LOW | MEDIUM | HIGH
    roi:         float

    # New: explicit collateral analysis
    collateral:  CollateralSnapshot

    simplified_explainability: SimplifiedExplainability
    audit_mode:                AuditMode
    stress_impact:             Dict[str, MetricComparison]

    response_time_ms: float
    report_url:       Optional[str] = None
