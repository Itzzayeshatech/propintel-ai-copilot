class ValuationService:
    # Micro-market data for Bangalore (Mocking real NBFC insights)
    LOCATION_DATA = {
        "Whitefield": {"price_index": 1.2, "liquidity_score": 0.65, "volatility": 0.15},
        "Koramangala": {"price_index": 1.5, "liquidity_score": 0.85, "volatility": 0.10},
        "Indiranagar": {"price_index": 1.4, "liquidity_score": 0.80, "volatility": 0.12},
        "Electronic City": {"price_index": 0.9, "liquidity_score": 0.45, "volatility": 0.20},
        "Hebbal": {"price_index": 1.1, "liquidity_score": 0.55, "volatility": 0.18},
    }

    @staticmethod
    def get_market_metrics(location: str):
        # Default to a generic baseline if location not found
        return ValuationService.LOCATION_DATA.get(
            location, 
            {"price_index": 1.0, "liquidity_score": 0.50, "volatility": 0.25}
        )

    @staticmethod
    def calculate_ltv(loan_amount: float, property_value: float):
        return (loan_amount / property_value) * 100

    @staticmethod
    def evaluate(location: str, property_value: float, loan_amount: float):
        metrics = ValuationService.get_market_metrics(location)
        ltv = ValuationService.calculate_ltv(loan_amount, property_value)
        
        return {
            "ltv": round(ltv, 2),
            "liquidity_score": metrics["liquidity_score"],
            "volatility": metrics["volatility"],
            "property_value": property_value,
            "loan_amount": loan_amount
        }
