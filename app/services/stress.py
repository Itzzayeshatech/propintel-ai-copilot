class StressService:
    """
    Stress Engine — Core Stage 2 of the Underwriting Pipeline.

    Takes base valuation context and applies macro-economic shock multipliers.

    Scenarios & Stress Impact Factors:
    ┌─────────────────────┬──────────────────────────────────────────────┐
    │ Scenario            │ Effect                                       │
    ├─────────────────────┼──────────────────────────────────────────────┤
    │ Market Crash        │ -15% on market_property_value                │
    │ Sector Crisis       │ -30% on market_property_value (stacks)       │
    │ Inflation Spike     │ -10% additional on stressed value,           │
    │                     │ -40% hit to liquidity_score                  │
    └─────────────────────┴──────────────────────────────────────────────┘

    Core Formula:
        stressed_property_value = market_property_value * (1 - total_stress_factor)
        stress_ltv              = loan_amount / stressed_property_value * 100
        property_value_drop_pct = (1 - stressed/market) * 100
    """

    @staticmethod
    def apply_stress(
        base_data: dict,
        crash: bool,
        repo_spike: bool,
        inflation_spike: bool,
        sector_crash: bool
    ) -> dict:
        import copy
        stressed = copy.deepcopy(base_data)

        market_property_value = base_data["market_property_value"]
        loan_amount           = base_data["loan_amount"]

        # ── Build cumulative property value stress factor ──────────────────
        value_stress_factor = 0.0
        if crash:        value_stress_factor += 0.15   # Market Crash: -15%
        if sector_crash: value_stress_factor += 0.15   # Sector Crisis: additional -15% (total -30%)
        if inflation_spike: value_stress_factor += 0.05 # Inflation: additional -5%

        # Apply: stressed_property_value = market_property_value × (1 - factor)
        stressed_property_value = market_property_value * (1.0 - value_stress_factor)
        stressed_property_value = round(max(stressed_property_value, 1.0), 2)

        # ── Derive Stress LTV ─────────────────────────────────────────────
        stress_ltv = round((loan_amount / stressed_property_value) * 100, 2)

        # ── Property Value Drop % ─────────────────────────────────────────
        property_value_drop_pct = round(value_stress_factor * 100, 2)

        # ── Liquidity Shock ───────────────────────────────────────────────
        liquidity = base_data["liquidity_score"]
        if inflation_spike:
            liquidity = max(0.10, liquidity * 0.60)   # -40% liquidity
        if sector_crash:
            liquidity = max(0.10, liquidity * 0.75)   # additional -25%
        stressed["liquidity_score"] = round(liquidity, 3)

        # ── Volatility Bump ───────────────────────────────────────────────
        vol_bump = (0.10 if crash else 0) + (0.08 if inflation_spike else 0) + (0.12 if sector_crash else 0)
        stressed["volatility"] = round(min(base_data["volatility"] + vol_bump, 1.0), 3)

        # ── Write enriched stress fields ──────────────────────────────────
        stressed["stressed_property_value"]  = stressed_property_value
        stressed["stress_ltv"]               = stress_ltv
        stressed["property_value_drop_pct"]  = property_value_drop_pct
        stressed["ltv"]                      = stress_ltv   # alias for downstream engines
        stressed["property_value"]           = stressed_property_value  # alias

        return stressed

    @staticmethod
    def get_impact(base: dict, stressed: dict) -> dict:
        """
        Computes a side-by-side delta for every key financial metric.
        Used directly by the API response and the UI 'Before vs After' visualizer.
        """
        comparisons = {}

        metrics = {
            "market_property_value":  ("market_property_value",  "market_property_value"),
            "stressed_property_value":("market_property_value",  "stressed_property_value"),
            "base_ltv":               ("base_ltv",                "base_ltv"),
            "stress_ltv":             ("base_ltv",                "stress_ltv"),
            "liquidity_score":        ("liquidity_score",         "liquidity_score"),
        }

        for label, (base_key, stressed_key) in metrics.items():
            b_val = base.get(base_key, 0)
            s_val = stressed.get(stressed_key, base.get(stressed_key, b_val))
            comparisons[label] = {
                "base_value":     round(b_val, 2),
                "stressed_value": round(s_val, 2),
                "delta":          round(s_val - b_val, 2),
            }

        return comparisons
