class ROIService:
    """
    ROI Engine - Stage 4 of the Underwriting Pipeline.
    Financial intelligence layer.

    Formula:
        ROI = interest_income - (default_probability * loss_given_default)

    Where:
        - interest_income: Repo + Margin (adjusted for rate spikes)
        - PD (default_probability): Base PD x Segment Multiplier x LTV Stress Penalty
        - LGD (loss_given_default): Standard NBFC recovery assumption (45%)
    """
    BASE_REPO_RATE = 0.065
    NBFC_MARGIN = 0.035
    LOSS_GIVEN_DEFAULT = 0.45

    @staticmethod
    def calculate_roi(stress_ltv: float, risk_level: str, repo_spike: bool, segment: str):
        # 1. Interest Income Layer
        interest_income = ROIService.BASE_REPO_RATE + ROIService.NBFC_MARGIN
        if repo_spike:
            interest_income += 0.02 # +200 bps spike

        # 2. Probability of Default (PD) Layer
        # Segment Multipliers: Salaried (1.0), Self-Employed (1.4), MSME (1.8)
        segment_multiplier = 1.0
        if segment == "SELF_EMPLOYED": segment_multiplier = 1.4
        if segment == "MSME": segment_multiplier = 1.8

        base_pd = 0.02 # 2% baseline
        if risk_level == "HIGH": base_pd = 0.10
        elif risk_level == "MEDIUM": base_pd = 0.05

        # LTV Stress Penalty: PD increases as collateral cover thins
        ltv_penalty = 0.0
        if stress_ltv > 85: ltv_penalty = 0.05
        elif stress_ltv > 75: ltv_penalty = 0.02

        final_pd = (base_pd + ltv_penalty) * segment_multiplier

        # 3. Final ROI Calculation
        # ROI = income - (PD * LGD)
        net_roi = interest_income - (final_pd * ROIService.LOSS_GIVEN_DEFAULT)

        return {
            "roi_percentage": round(net_roi * 100, 2),
            "interest_income_base": round(interest_income * 100, 2),
            "probability_of_default": round(final_pd * 100, 2),
            "loss_given_default": round(ROIService.LOSS_GIVEN_DEFAULT * 100, 2)
        }
