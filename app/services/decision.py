class DecisionService:
    @staticmethod
    def run_policy_rules(income: float, loan_amount: float, credit_score: int, segment: str):
        triggered_rules = []
        
        # 1. Debt-to-Income (DTI) Check - Assuming 50% limit for Salaried, 40% for MSME
        # Monthly EMI estimation (rough)
        estimated_emi = (loan_amount * 0.12) / 12 # 12% interest
        dti = (estimated_emi / income) * 100
        
        dti_limit = 50 if segment == "SALARIED" else 40
        if dti > dti_limit:
            triggered_rules.append(f"DTI ratio ({dti:.1f}%) exceeds policy limit of {dti_limit}%")
            
        # 2. Credit Score Floor
        if credit_score < 650:
            triggered_rules.append(f"Credit Score ({credit_score}) below standard threshold of 650")
        elif credit_score < 700:
            triggered_rules.append(f"Low-Tier Credit Score ({credit_score}) - Conditional Approval Mandatory")
            
        return triggered_rules

    @staticmethod
    def evaluate_risk(ltv: float, liquidity_score: float, triggered_rules: list, segment: str):
        # Segment-based baseline risk
        base_risk_weight = 0
        if segment == "SELF_EMPLOYED": base_risk_weight += 1
        if segment == "MSME": base_risk_weight += 2
        
        # Risk scoring
        if ltv > 85 or len([r for r in triggered_rules if "below standard" in r]) > 0:
            return "HIGH"
        elif ltv > 75 or liquidity_score < 0.4 or len(triggered_rules) > 0:
            return "MEDIUM"
        else:
            return "LOW"

    @staticmethod
    def get_decision(risk_level: str, ltv: float, triggered_rules: list):
        if risk_level == "HIGH" or ltv > 90:
            return "REJECT"
        elif risk_level == "MEDIUM" or ltv > 75 or len(triggered_rules) > 0:
            return "CONDITIONAL"
        else:
            return "APPROVE"
