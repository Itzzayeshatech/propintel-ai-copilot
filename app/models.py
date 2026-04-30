from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from uuid import UUID
from enum import Enum

class BorrowerSegment(str, Enum):
    SALARIED = "SALARIED"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    MSME = "MSME"

class LoanRequest(BaseModel):
    # Core Loan Data
    location: str = Field(..., example="Whitefield")
    property_value: float = Field(..., example=8500000)
    loan_amount: float = Field(..., example=6000000)
    
    # Borrower Profile (New Bank-Grade Fields)
    monthly_income: float = Field(..., example=150000)
    credit_score: int = Field(..., example=750)
    segment: BorrowerSegment = Field(default=BorrowerSegment.SALARIED)
    
    # Stress Scenarios (Upgraded to Macro-Realism)
    stress_market_crash: bool = False
    stress_repo_rate_spike: bool = False  # +2% Repo Rate
    stress_inflation_spike: bool = False  # Impact on disposable income
    stress_sector_crash: bool = False     # Sector-specific (e.g., IT/Real Estate)

class MetricComparison(BaseModel):
    base_value: float
    stressed_value: float
    delta: float

class AuditMode(BaseModel):
    triggered_rules: List[str]
    risk_reasoning_chain: List[str]
    compliance_check: str

class SimplifiedExplainability(BaseModel):
    key_risk_factors: List[str]  # Max 3
    stress_impact_summary: str   # 1 line
    decision_rationale: str      # 1 line

class LoanResponse(BaseModel):
    request_id: UUID
    risk_level: str
    ltv: float
    roi: float
    decision: str
    simplified_explainability: SimplifiedExplainability
    audit_mode: AuditMode
    stress_impact: Dict[str, MetricComparison]
    response_time_ms: float
    report_url: Optional[str] = None
