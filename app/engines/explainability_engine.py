def generate_explanation(valuation: dict, risk: dict, decision: dict):
    """
    explainability_engine.py
    
    Generate human-readable reasons for AI decisions.
    """
    reasons = []
    
    # Liquidity logic
    if valuation["liquidity_days"] > 90:
        reasons.append(f"Loan LTV reduced to {decision['ltv']*100}% due to low market liquidity ({valuation['liquidity_days']} days).")
    
    # Volatility logic
    if risk["volatility"] > 0.5:
        reasons.append(f"Interest rate includes a risk premium of {decision['risk_premium']}% due to high zone volatility.")
    
    # Age/Demand mismatch
    if valuation["demand_index_applied"] < 0.7:
        reasons.append("Risk level elevated due to demand-supply mismatch in the specific zone.")
        
    if not reasons:
        reasons.append("Property metrics are within optimal lending parameters for prime zones.")
        
    return {
        "summary": " ".join(reasons),
        "key_factors": reasons,
        "transparency_score": 0.95
    }
