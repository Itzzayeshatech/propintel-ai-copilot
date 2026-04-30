class ROIService:
    BASE_REPO_RATE = 0.065  # 6.5% standard
    NBFC_MARGIN = 0.035     # 3.5% margin
    LOSS_GIVEN_DEFAULT = 0.45

    @staticmethod
    def calculate_roi(ltv: float, risk_level: str, repo_spike: bool, segment: str):
        # 1. Base Interest = Repo Rate + Margin
        repo_rate = ROIService.BASE_REPO_RATE
        if repo_spike:
            repo_rate += 0.02 # +200 bps
            
        interest_rate = repo_rate + ROIService.NBFC_MARGIN
            
        # 2. Segment-Adjusted Default Probability (PD)
        # MSME and Self-Employed have higher volatility multipliers
        segment_multiplier = 1.0
        if segment == "SELF_EMPLOYED": segment_multiplier = 1.4
        if segment == "MSME": segment_multiplier = 1.8
        
        base_pd = 0.02
        if risk_level == "HIGH": base_pd = 0.10
        elif risk_level == "MEDIUM": base_pd = 0.05
            
        # LTV sensitivity
        if ltv > 85: base_pd += 0.05
        
        final_pd = base_pd * segment_multiplier
        
        # 3. ROI = Interest Income - (PD * LGD)
        net_roi = interest_rate - (final_pd * ROIService.LOSS_GIVEN_DEFAULT)
        
        return {
            "roi_percentage": round(net_roi * 100, 2),
            "interest_rate": round(interest_rate * 100, 2),
            "pd": round(final_pd * 100, 2)
        }
