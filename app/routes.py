from fastapi import APIRouter, HTTPException
from app.models import LoanRequest, LoanResponse, MetricComparison, AuditMode, SimplifiedExplainability
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
        # 1. Pipeline Stage: Policy Rules Engine (Pre-check)
        triggered_rules = DecisionService.run_policy_rules(
            request.monthly_income,
            request.loan_amount,
            request.credit_score,
            request.segment
        )
        
        # 2. Pipeline Stage: Valuation
        base_valuation = ValuationService.evaluate(
            request.location, 
            request.property_value, 
            request.loan_amount
        )
        
        # 3. Pipeline Stage: Stress Test (Macro-Realism)
        stressed_valuation = StressService.apply_stress(
            base_valuation,
            request.stress_market_crash,
            request.stress_repo_rate_spike,
            request.stress_inflation_spike,
            request.stress_sector_crash
        )
        
        stress_impact_metrics = StressService.get_impact(base_valuation, stressed_valuation)
        
        # 4. Pipeline Stage: Risk & Decision
        risk_level = DecisionService.evaluate_risk(
            stressed_valuation["ltv"], 
            stressed_valuation["liquidity_score"],
            triggered_rules,
            request.segment
        )
        decision = DecisionService.get_decision(risk_level, stressed_valuation["ltv"], triggered_rules)
        
        # 5. Pipeline Stage: ROI
        roi_results = ROIService.calculate_roi(
            stressed_valuation["ltv"],
            risk_level,
            request.stress_repo_rate_spike,
            request.segment
        )
        
        # 6. Pipeline Stage: Explainability (Simplified + Audit)
        simplified = ExplainabilityService.generate_simplified_output(
            base_valuation,
            stressed_valuation,
            decision,
            risk_level,
            triggered_rules
        )
        
        audit_trace = ExplainabilityService.generate_audit_trace(
            triggered_rules,
            risk_level,
            simplified["stress_impact_summary"]
        )
        
        end_time = time.perf_counter()
        response_time_ms = (end_time - start_time) * 1000
        
        return LoanResponse(
            request_id=request_id,
            risk_level=risk_level,
            ltv=stressed_valuation["ltv"],
            roi=roi_results["roi_percentage"],
            decision=decision,
            simplified_explainability=SimplifiedExplainability(**simplified),
            audit_mode=AuditMode(**audit_trace),
            stress_impact=stress_impact_metrics,
            response_time_ms=response_time_ms,
            report_url=f"/api/v1/report/{request_id}" # Placeholder for report generation
        )
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
