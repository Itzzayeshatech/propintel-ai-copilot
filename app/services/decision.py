class DecisionService:
    """
    Decision Engine — Stage 3 of the Underwriting Pipeline.

    Uses STRESSED metrics (not base) as the final arbiter — because an NBFC must
    survive the worst case, not just today's market.

    Decision Thresholds (Stress LTV):
        > 90%  → REJECT  (Hard floor — principal at risk)
        > 75%  → CONDITIONAL
        ≤ 75%  → APPROVE

    Risk Classification (Stress LTV + Liquidity + Policy):
        HIGH   → stress_ltv > 85  OR  hard credit violation
        MEDIUM → stress_ltv > 75  OR  liquidity < 0.40  OR  any policy flag
        LOW    → All clear
    """

    @staticmethod
    def run_policy_rules(
        income: float,
        loan_amount: float,
        credit_score: int,
        segment: str,
    ) -> list:
        triggered = []

        # ── DTI check (uses estimated EMI at 12% flat) ────────────────────
        estimated_monthly_emi = (loan_amount * 0.12) / 12
        dti = (estimated_monthly_emi / max(income, 1)) * 100
        dti_ceiling = 50 if segment == "SALARIED" else 40   # MSME / Self-Employed: tighter

        if dti > dti_ceiling:
            triggered.append(
                f"DTI ratio {dti:.1f}% exceeds {dti_ceiling}% policy ceiling for {segment}"
            )

        # ── Credit score floor ────────────────────────────────────────────
        if credit_score < 650:
            triggered.append(
                f"Credit score {credit_score} is below the minimum threshold of 650"
            )
        elif credit_score < 700:
            triggered.append(
                f"Credit score {credit_score} in caution band (650–700) — conditional approval mandatory"
            )

        return triggered

    @staticmethod
    def evaluate_risk(
        stress_ltv: float,
        liquidity_score: float,
        triggered_rules: list,
        segment: str,
    ) -> str:
        # Hard failures → HIGH
        hard_credit_fail = any("below the minimum" in r for r in triggered_rules)
        if stress_ltv > 85 or hard_credit_fail:
            return "HIGH"

        # Soft flags → MEDIUM
        segment_penalty = segment in ("SELF_EMPLOYED", "MSME")
        if stress_ltv > 75 or liquidity_score < 0.40 or triggered_rules or segment_penalty:
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def get_decision(
        risk_level: str,
        stress_ltv: float,
        triggered_rules: list,
    ) -> str:
        # Hard reject boundary
        if risk_level == "HIGH" or stress_ltv > 90:
            return "REJECT"

        # Conditional zone
        if risk_level == "MEDIUM" or stress_ltv > 75 or triggered_rules:
            return "CONDITIONAL"

        return "APPROVE"
