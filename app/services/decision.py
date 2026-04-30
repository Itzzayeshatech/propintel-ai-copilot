class DecisionService:
    """
    Decision Engine - Stage 5 of the Underwriting Pipeline.
    Core BANK RULE ENGINE.

    Deterministic logic using:
    - Stressed LTV (Safety Floor)
    - Net ROI (Yield Floor)
    - Credit Score (Borrower Quality)
    """

    @staticmethod
    def run_policy_rules(income: float, loan_amount: float, credit_score: int, segment: str):
        triggered_rules = []
        
        # Policy: Debt-to-Income (DTI) Check
        estimated_monthly_emi = (loan_amount * 0.12) / 12
        dti = (estimated_monthly_emi / max(income, 1)) * 100
        dti_ceiling = 50 if segment == "SALARIED" else 40

        if dti > dti_ceiling:
            triggered_rules.append(f"DTI ratio {dti:.1f}% exceeds bank limit for {segment}")
            
        if credit_score < 650:
            triggered_rules.append(f"Credit score {credit_score} is below standard threshold")

        return triggered_rules

    @staticmethod
    def evaluate_risk(stress_ltv: float, liquidity_score: float, triggered_rules: list, segment: str):
        # Risk classification for internal scoring
        if stress_ltv > 85 or any("below standard" in r for r in triggered_rules):
            return "HIGH"
        elif stress_ltv > 75 or liquidity_score < 0.4 or triggered_rules:
            return "MEDIUM"
        else:
            return "LOW"

    @staticmethod
    def get_decision(stress_ltv: float, roi: float, credit_score: int):
        """
        Main Bank Decision Rule Engine (10/10 Logic)
        Input units: stress_ltv (decimal, e.g. 75.0), roi (decimal, e.g. 8.0), credit_score (int)
        """
        # Normalize inputs for logic
        ltv_ratio = stress_ltv / 100.0
        roi_ratio = roi / 100.0

        # Primary LTV Logic
        if ltv_ratio <= 0.70:
            decision = "APPROVE"
        elif ltv_ratio <= 0.85:
            decision = "CONDITIONAL"
        else:
            decision = "REJECT"

        # ROI Yield Logic Override
        if roi_ratio < 0.05:
            decision = "REJECT"

        # Credit Quality Override
        if credit_score < 650:
            decision = "CONDITIONAL"

        return decision
