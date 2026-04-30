from fastapi import APIRouter, HTTPException
from app.models import (
    LoanRequest, LoanResponse,
    MetricComparison, AuditMode, SimplifiedExplainability, CollateralSnapshot
)
from app.services.valuation     import ValuationService
from app.services.stress        import StressService
from app.services.roi           import ROIService
from app.services.decision      import DecisionService
from app.services.explainability import ExplainabilityService
import time, uuid, traceback

router = APIRouter()


@router.post("/analyze-loan", response_model=LoanResponse)
async def analyze_loan(request: LoanRequest):
    t0 = time.perf_counter()
    request_id = uuid.uuid4()

    try:
        # ── Stage 0: Policy Pre-checks ─────────────────────────────────────
        triggered_rules = DecisionService.run_policy_rules(
            request.monthly_income,
            request.loan_amount,
            request.credit_score,
            request.segment,
        )

        # ── Stage 1: Valuation (market_property_value + base_ltv) ──────────
        base = ValuationService.evaluate(
            request.location,
            request.property_value,
            request.loan_amount,
        )

        # ── Stage 2: Stress (stressed_property_value + stress_ltv) ─────────
        stressed = StressService.apply_stress(
            base,
            request.stress_market_crash,
            request.stress_repo_rate_spike,
            request.stress_inflation_spike,
            request.stress_sector_crash,
        )
        stress_impact = StressService.get_impact(base, stressed)

        # ── Stage 3: Risk & Decision ────────────────────────────────────────
        risk_level = DecisionService.evaluate_risk(
            stressed["stress_ltv"],
            stressed["liquidity_score"],
            triggered_rules,
            request.segment,
        )
        decision = DecisionService.get_decision(
            risk_level, stressed["stress_ltv"], triggered_rules
        )

        # ── Stage 4: ROI ────────────────────────────────────────────────────
        roi_data = ROIService.calculate_roi(
            stressed["stress_ltv"],
            risk_level,
            request.stress_repo_rate_spike,
            request.segment,
        )

        # ── Stage 5: Explainability ─────────────────────────────────────────
        simplified_data = ExplainabilityService.generate_simplified_output(
            base, stressed, decision, risk_level, triggered_rules
        )
        audit_data = ExplainabilityService.generate_audit_trace(
            triggered_rules, risk_level, simplified_data["stress_impact_summary"]
        )

        # ── Build CollateralSnapshot ────────────────────────────────────────
        collateral = CollateralSnapshot(
            market_property_value   = base["market_property_value"],
            stressed_property_value = stressed["stressed_property_value"],
            property_value_drop_pct = stressed["property_value_drop_pct"],
            base_ltv                = base["base_ltv"],
            stress_ltv              = stressed["stress_ltv"],
        )

        # ── Build MetricComparison dict ─────────────────────────────────────
        stress_impact_models = {
            k: MetricComparison(**v) for k, v in stress_impact.items()
        }

        return LoanResponse(
            request_id               = request_id,
            decision                 = decision,
            risk_level               = risk_level,
            roi                      = roi_data["roi_percentage"],
            collateral               = collateral,
            simplified_explainability= SimplifiedExplainability(**simplified_data),
            audit_mode               = AuditMode(**audit_data),
            stress_impact            = stress_impact_models,
            response_time_ms         = (time.perf_counter() - t0) * 1000,
            report_url               = f"/api/v1/report/{request_id}",
        )

    except Exception:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
