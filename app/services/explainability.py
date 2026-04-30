from typing import List

class ExplainabilityService:
    """
    Explainability Engine - Stage 6 of the Underwriting Pipeline.
    RBI Compliance Layer (Standardized Audit Format).
    """

    @staticmethod
    def generate_simplified_output(
        base_ltv: float,
        stress_ltv: float,
        market_property_value: float,
        stressed_property_value: float,
        decision: str,
        risk_level: str,
        risk_factors: List[str]
    ):
        # 1. Property Value Change Explanation
        drop_amt = market_property_value - stressed_property_value
        drop_pct = (drop_amt / market_property_value) * 100 if market_property_value > 0 else 0
        prop_val_expl = (
            f"Collateral value compresses from INR {market_property_value/10000000:.2f}Cr to "
            f"INR {stressed_property_value/10000000:.2f}Cr, representing a {drop_pct:.1f}% erosion "
            f"under active macro-stress scenarios."
        )

        # 2. LTV Increase Explanation
        ltv_delta = stress_ltv - base_ltv
        ltv_expl = (
            f"Thinning collateral cover pushes LTV from {base_ltv:.1f}% to {stress_ltv:.1f}% "
            f"(+{ltv_delta:.1f}% delta), reducing the bank's recovery margin during default."
        )

        # 3. Final Risk Reason
        final_reason = f"System recommends {decision} status."
        if decision == "REJECT":
            final_reason += " Asset risk exceeds NBFC safety thresholds for this borrower segment."
        elif decision == "CONDITIONAL":
            final_reason += " Approval requires additional collateral or a risk-premium interest rate adjustment."
        else:
            final_reason += " Loan remains resilient under modelled economic shocks."
            
        return {
            "key_risk_factors": risk_factors[:3],
            "property_value_change_explanation": prop_val_expl,
            "ltv_increase_explanation": ltv_expl,
            "final_risk_reason": final_reason
        }

    @staticmethod
    def generate_audit_trace(triggered_rules: List[str], risk_level: str, stress_summary: str):
        reasoning_chain = [
            "Stage 1 - Valuation: Micro-market price index and demand signals applied.",
            "Stage 2 - Stress: Independent macro-economic scenarios simulated; worst-case value selected.",
            f"Stage 3 - Risk: Portfolio risk indexed as {risk_level}.",
            "Stage 4 - ROI: Net risk-adjusted yield computed.",
            "Stage 5 - Decision: Deterministic bank rules applied to stressed LTV and ROI floors."
        ]
        
        return {
            "triggered_rules": triggered_rules,
            "risk_reasoning_chain": reasoning_chain,
            "compliance_check": "FAILED" if risk_level == "HIGH" else "PASSED"
        }
