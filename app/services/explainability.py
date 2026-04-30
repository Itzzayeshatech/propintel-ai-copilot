from typing import List

class ExplainabilityService:
    """
    Explainability Engine - Stage 6 of the Underwriting Pipeline.
    RBI Compliance Layer.
    """

    @staticmethod
    def generate_simplified_output(
        base_ltv: float,
        stress_ltv: float,
        decision: str,
        risk_level: str,
        triggered_rules: List[str],
        risk_factors: List[str]
    ):
        # Stress impact line
        stress_impact = f"LTV increased from {base_ltv:.1f}% to {stress_ltv:.1f}% under stress scenarios."
        
        # Final reason
        final_reason = f"Decision = {decision} due to stress-adjusted collateral risk."
        if decision == "REJECT":
            final_reason += " Safety thresholds breached in stress simulation."
            
        return {
            "key_risk_factors": risk_factors[:3],
            "stress_impact": stress_impact,
            "final_reason": final_reason
        }

    @staticmethod
    def generate_audit_trace(triggered_rules: List[str], risk_level: str, stress_summary: str):
        reasoning_chain = [
            f"Stage 1 - Valuation: Micro-market index adjustment applied.",
            f"Stage 2 - Stress: Worst-case scenario simulation executed.",
            f"Stage 3 - Risk: Scored as {risk_level} profile.",
            f"Stage 4 - ROI: Net yield calculated after PD/LGD adjustment.",
            f"Stage 5 - Decision: Deterministic bank rules applied."
        ]
        
        return {
            "triggered_rules": triggered_rules,
            "risk_reasoning_chain": reasoning_chain,
            "compliance_check": "FAILED" if risk_level == "HIGH" else "PASSED"
        }
