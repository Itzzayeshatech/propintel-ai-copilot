from fastapi import APIRouter, HTTPException
from app.models import LoanRequest, LoanResponse, AuditMode, SimplifiedExplainability
from app.services.valuation import ValuationService
from app.services.stress import StressService
from app.services.roi import ROIService
from app.services.decision import DecisionService
from app.services.explainability import ExplainabilityService
import time
import uuid

router = APIRouter()

@router.post("/analyze-loan", response_model=LoanResponse)
async def analyze_loan(request: LoanRequest):
    start_time = time.perf_counter()
    request_id = uuid.uuid4()
    
    try:
        # 1. Valuation
        base_valuation = ValuationService.evaluate(
            request.location, 
            request.property_value, 
            request.loan_amount
        )
        
        # 2. Stress Test
        stressed_valuation = StressService.apply_stress(
            base_valuation,
            request.stress_market_crash,
            request.stress_repo_rate_spike,
            request.stress_inflation_spike,
            request.stress_sector_crash
        )
        
        # 3. Policy Rules
        triggered_rules = DecisionService.run_policy_rules(
            request.monthly_income,
            request.loan_amount,
            request.credit_score,
            request.segment
        )
        
        # 4. Risk Scoring
        risk_level = DecisionService.evaluate_risk(
            stressed_valuation["stress_ltv"], 
            stressed_valuation["liquidity_score"],
            triggered_rules,
            request.segment
        )
        
        # 5. ROI
        roi_results = ROIService.calculate_roi(
            stressed_valuation["stress_ltv"],
            risk_level,
            request.stress_repo_rate_spike,
            request.segment
        )
        
        # 6. Decision (Standardized logic)
        decision = DecisionService.get_decision(
            stressed_valuation["stress_ltv"],
            roi_results["roi_percentage"],
            request.credit_score
        )
        
        # 7. Explainability
        risk_factors = []
        if stressed_valuation["stress_ltv"] > 75: risk_factors.append("High Collateral Exposure")
        if roi_results["roi_percentage"] < 8: risk_factors.append("Compressed Net Margin")
        if triggered_rules: risk_factors.append("Policy Rule Violations")
        if not risk_factors: risk_factors.append("Stable Asset Performance")

        simplified = ExplainabilityService.generate_simplified_output(
            base_valuation["base_ltv"],
            stressed_valuation["stress_ltv"],
            base_valuation["market_property_value"],
            stressed_valuation["stressed_property_value"],
            decision,
            risk_level,
            risk_factors
        )
        
        audit_trace = ExplainabilityService.generate_audit_trace(
            triggered_rules,
            risk_level,
            simplified["property_value_change_explanation"]
        )
        
        end_time = time.perf_counter()
        response_time_ms = (end_time - start_time) * 1000
        
        return LoanResponse(
            market_property_value=base_valuation["market_property_value"],
            stressed_property_value=stressed_valuation["stressed_property_value"],
            property_value_drop_percentage=stressed_valuation["property_value_drop_pct"],
            base_ltv=base_valuation["base_ltv"],
            stress_ltv=stressed_valuation["stress_ltv"],
            decision=decision,
            roi=roi_results["roi_percentage"],
            request_id=request_id,
            risk_level=risk_level,
            simplified_explainability=SimplifiedExplainability(**simplified),
            audit_mode=AuditMode(**audit_trace),
            response_time_ms=response_time_ms
        )
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
