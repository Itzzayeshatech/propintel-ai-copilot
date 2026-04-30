class ValuationService:
    """
    Valuation Engine — Core Stage 1 of the Underwriting Pipeline.

    Computes:
    - Market Property Value: price_index-adjusted valuation of the asset.
    - Base LTV: using market property value (not raw input).
    - Liquidity & Volatility: micro-market sensitivity indices.

    Formula:
        market_property_value = property_value * price_index
        base_ltv = (loan_amount / market_property_value) * 100
    """

    LOCATION_DATA = {
        "Whitefield":     {"price_index": 1.20, "liquidity_score": 0.65, "volatility": 0.15},
        "Koramangala":    {"price_index": 1.50, "liquidity_score": 0.85, "volatility": 0.10},
        "Indiranagar":    {"price_index": 1.40, "liquidity_score": 0.80, "volatility": 0.12},
        "Electronic City":{"price_index": 0.90, "liquidity_score": 0.45, "volatility": 0.20},
        "Hebbal":         {"price_index": 1.10, "liquidity_score": 0.55, "volatility": 0.18},
    }

    @staticmethod
    def get_market_metrics(location: str) -> dict:
        return ValuationService.LOCATION_DATA.get(
            location,
            {"price_index": 1.00, "liquidity_score": 0.50, "volatility": 0.25}
        )

    @staticmethod
    def evaluate(location: str, raw_property_value: float, loan_amount: float) -> dict:
        metrics = ValuationService.get_market_metrics(location)

        # Step 1: Derive Market Property Value via price_index adjustment
        market_property_value = raw_property_value * metrics["price_index"]

        # Step 2: Base LTV = loan_amount / market_property_value
        base_ltv = round((loan_amount / market_property_value) * 100, 2)

        return {
            # Core valuation fields
            "raw_property_value":    round(raw_property_value, 2),
            "market_property_value": round(market_property_value, 2),
            "loan_amount":           round(loan_amount, 2),
            "base_ltv":              base_ltv,

            # Micro-market attributes
            "price_index":      metrics["price_index"],
            "liquidity_score":  metrics["liquidity_score"],
            "volatility":       metrics["volatility"],

            # Backwards-compatible alias used by stress engine
            "ltv":              base_ltv,
            "property_value":   market_property_value,
        }
