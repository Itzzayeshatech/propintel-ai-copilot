class StressService:
    """
    Stress Engine - Stage 2 of the Underwriting Pipeline.
    The signature innovation layer.

    Each scenario independently computes a stressed property value.
    The final stressed_property_value = min(all active scenarios).
    This is the WORST-CASE approach - the most conservative and financially sound method.

    Scenario multipliers:
        Market Crash  -> 0.85 (- 15%)
        Liquidity Drop-> 0.60 (- 40%, fire-sale scenario)
        Sector Crisis -> 0.85 (- 15%, sector-specific shock)
        Inflation     -> reduces liquidity, -5% additional on value
    """

    SCENARIO_MULTIPLIERS = {
        "crash":     0.85,
        "liquidity": 0.60,
        "sector":    0.85,
        "inflation": 0.95,  # -5% on value, -40% on liquidity_score separately
    }

    @staticmethod
    def apply_stress(
        base_data: dict,
        crash: bool,
        repo_spike: bool,
        inflation_spike: bool,
        sector_crash: bool,
    ) -> dict:
        import copy
        stressed = copy.deepcopy(base_data)
        market_value = base_data["market_property_value"]
        loan_amount  = base_data["loan_amount"]

        # Compute each active scenario's stressed value independently
        scenario_values = []

        if crash:
            scenario_values.append(market_value * StressService.SCENARIO_MULTIPLIERS["crash"])

        if sector_crash:
            scenario_values.append(market_value * StressService.SCENARIO_MULTIPLIERS["sector"])

        if inflation_spike:
            scenario_values.append(market_value * StressService.SCENARIO_MULTIPLIERS["inflation"])
            # Inflation also hits liquidity hard
            stressed["liquidity_score"] = round(max(0.10, base_data["liquidity_score"] * 0.60), 3)

        # If no value-impacting scenario is active, stressed value = market value
        if scenario_values:
            # WORST-CASE: take the minimum stressed value across all active scenarios
            stressed_property_value = min(scenario_values)
        else:
            stressed_property_value = market_value

        # Sector crash also hits liquidity
        if sector_crash:
            stressed["liquidity_score"] = round(max(0.10, stressed.get("liquidity_score", base_data["liquidity_score"]) * 0.75), 3)

        stressed_property_value = round(stressed_property_value, 2)

        # Stress LTV = loan / stressed_property_value
        stress_ltv = round((loan_amount / stressed_property_value) * 100, 2)

        # Property value drop %
        drop_pct = round((1 - stressed_property_value / market_value) * 100, 2)

        # Volatility bump
        vol_bump = (0.10 if crash else 0) + (0.08 if inflation_spike else 0) + (0.12 if sector_crash else 0)
        stressed["volatility"] = round(min(base_data["volatility"] + vol_bump, 1.0), 3)

        # Write final stressed fields
        stressed["stressed_property_value"] = stressed_property_value
        stressed["stress_ltv"]              = stress_ltv
        stressed["property_value_drop_pct"] = drop_pct

        # Backwards-compatible aliases
        stressed["ltv"]            = stress_ltv
        stressed["property_value"] = stressed_property_value

        return stressed

    @staticmethod
    def get_impact(base: dict, stressed: dict) -> dict:
        """Side-by-side delta for each key financial metric - shown in UI 'Before vs After'."""
        metrics = {
            "market_property_value":   ("market_property_value", "market_property_value"),
            "stressed_property_value": ("market_property_value", "stressed_property_value"),
            "base_ltv":                ("base_ltv",              "base_ltv"),
            "stress_ltv":              ("base_ltv",              "stress_ltv"),
            "liquidity_score":         ("liquidity_score",       "liquidity_score"),
        }
        impact = {}
        for label, (bk, sk) in metrics.items():
            b = base.get(bk, 0)
            s = stressed.get(sk, base.get(sk, b))
            impact[label] = {
                "base_value":     round(b, 2),
                "stressed_value": round(s, 2),
                "delta":          round(s - b, 2),
            }
        return impact
