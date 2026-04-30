class ValuationService:
    """
    Valuation Engine - Stage 1 of the Underwriting Pipeline.

    Formula:
        market_property_value = base_value * micro_market_index * demand_factor

    Where:
        - micro_market_index: location-specific price adjustment
        - demand_factor: real-time demand signal (absorption rate proxy)
    """

    LOCATION_DATA = {
        "Whitefield":      {"micro_market_index": 1.18, "demand_factor": 1.04, "liquidity_score": 0.65, "volatility": 0.15},
        "Koramangala":     {"micro_market_index": 1.45, "demand_factor": 1.10, "liquidity_score": 0.85, "volatility": 0.10},
        "Indiranagar":     {"micro_market_index": 1.38, "demand_factor": 1.08, "liquidity_score": 0.80, "volatility": 0.12},
        "Electronic City": {"micro_market_index": 0.88, "demand_factor": 0.92, "liquidity_score": 0.45, "volatility": 0.20},
        "Hebbal":          {"micro_market_index": 1.08, "demand_factor": 0.97, "liquidity_score": 0.55, "volatility": 0.18},
    }

    @staticmethod
    def get_market_metrics(location: str) -> dict:
        return ValuationService.LOCATION_DATA.get(
            location,
            {"micro_market_index": 1.00, "demand_factor": 1.00, "liquidity_score": 0.50, "volatility": 0.25}
        )

    @staticmethod
    def evaluate(location: str, raw_property_value: float, loan_amount: float) -> dict:
        m = ValuationService.get_market_metrics(location)

        # Core formula: market_value = base * micro_market_index * demand_factor
        market_property_value = raw_property_value * m["micro_market_index"] * m["demand_factor"]
        market_property_value = round(market_property_value, 2)

        base_ltv = round((loan_amount / market_property_value) * 100, 2)

        return {
            "raw_property_value":    round(raw_property_value, 2),
            "market_property_value": market_property_value,
            "loan_amount":           round(loan_amount, 2),
            "base_ltv":              base_ltv,
            "micro_market_index":    m["micro_market_index"],
            "demand_factor":         m["demand_factor"],
            "liquidity_score":       m["liquidity_score"],
            "volatility":            m["volatility"],
            # Aliases for downstream pipeline
            "ltv":          base_ltv,
            "property_value": market_property_value,
        }
