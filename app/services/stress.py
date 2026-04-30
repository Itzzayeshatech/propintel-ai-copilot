class StressService:
    @staticmethod
    def apply_stress(
        base_data: dict, 
        crash: bool, 
        repo_spike: bool, 
        inflation_spike: bool, 
        sector_crash: bool
    ):
        stressed_data = base_data.copy()
        
        # 1. Market/Sector Crash (Collateral Impact)
        if crash or sector_crash:
            # Sector crash is more aggressive in specific zones
            multiplier = 0.70 if sector_crash else 0.85
            stressed_data["property_value"] *= multiplier
            stressed_data["ltv"] = (stressed_data["loan_amount"] / stressed_data["property_value"]) * 100
        
        # 2. Repo Rate Spike (Interest Income/Cost Impact)
        # Handled in ROI calculation, but track stress state here
        
        # 3. Inflation Spike (Disposable Income Shock)
        if inflation_spike:
            stressed_data["liquidity_score"] = max(0.1, stressed_data["liquidity_score"] * 0.6)
            stressed_data["volatility"] += 0.15
            
        return stressed_data

    @staticmethod
    def get_impact(base_metrics: dict, stressed_metrics: dict):
        impact = {}
        for key in ["ltv", "liquidity_score", "property_value"]:
            base = base_metrics[key]
            stressed = stressed_metrics[key]
            impact[key] = {
                "base_value": round(base, 2),
                "stressed_value": round(stressed, 2),
                "delta": round(stressed - base, 2)
            }
        return impact
