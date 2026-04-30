from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from enum import Enum

class BorrowerSegment(str, Enum):
    SALARIED = "SALARIED"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    MSME = "MSME"

class LoanRequest(BaseModel):
    location: str = Field(..., example="Whitefield")
    property_value: float = Field(..., example=8500000)
    loan_amount: float = Field(..., example=6000000)
    monthly_income: float = Field(..., example=150000)
    credit_score: int = Field(..., example=750)
    segment: BorrowerSegment = Field(default=BorrowerSegment.SALARIED)
    stress_market_crash: bool = False
    stress_repo_rate_spike: bool = False
    stress_inflation_spike: bool = False
    stress_sector_crash: bool = False

class SimplifiedExplainability(BaseModel):
    key_risk_factors: List[str]
    # New Structured Explainability (Audit Compliant)
    property_value_change_explanation: str
    ltv_increase_explanation: str
    final_risk_reason: str

class AuditMode(BaseModel):
    triggered_rules: List[str]
    risk_reasoning_chain: List[str]
    compliance_check: str

class LoanResponse(BaseModel):
    # Core Standardized Audit Fields
    market_property_value: float
    stressed_property_value: float
    property_value_drop_percentage: float
    base_ltv: float
    stress_ltv: float
    decision: str
    roi: float
    
    # Metadata
    request_id: UUID
    risk_level: str
    simplified_explainability: SimplifiedExplainability
    audit_mode: AuditMode
    response_time_ms: float
    report_url: Optional[str] = None
