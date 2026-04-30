from typing import List, Dict

class ExplainabilityService:
    @staticmethod
    def generate_audit_trace(triggered_rules: List[str], risk_level: str, scenario_impact: str):
        reasoning_chain = [
            f"Asset evaluation identified {risk_level} risk baseline.",
            f"Policy engine flagged {len(triggered_rules)} compliance violations/warnings.",
            scenario_impact
        ]
        
        return {
            "triggered_rules": triggered_rules,
            "risk_reasoning_chain": reasoning_chain,
            "compliance_check": "FAILED" if risk_level == "HIGH" else "PASSED WITH CONDITIONS" if risk_level == "MEDIUM" else "PASSED"
        }

    @staticmethod
    def generate_simplified_output(
        base_data: dict, 
        stressed_data: dict, 
        decision: str, 
        risk_level: str,
        triggered_rules: List[str]
    ):
        # 1. Top 3 Risk Factors
        factors = []
        if base_data["ltv"] > 75: factors.append("Elevated LTV Ratio")
        if base_data["liquidity_score"] < 0.5: factors.append("Low Micro-Market Liquidity")
        if len(triggered_rules) > 0: factors.append("Policy Rule Violations")
        if not factors: factors.append("Standard Risk Profile")
        
        # 2. Stress Impact Summary (1 line)
        ltv_delta = stressed_data["ltv"] - base_data["ltv"]
        stress_line = f"Market volatility reduces collateral cover by {ltv_delta:.1f}% under stress scenarios."
        
        # 3. Final Decision Rationale (1 line)
        if decision == "REJECT":
            rationale = "Application rejected due to safety threshold breach or high policy non-compliance."
        elif decision == "CONDITIONAL":
            rationale = "Approval subject to risk premium adjustment and additional income verification."
        else:
            rationale = "Loan meets all standard bank-grade underwriting criteria."
            
        return {
            "key_risk_factors": factors[:3],
            "stress_impact_summary": stress_line,
            "decision_rationale": rationale
        }
