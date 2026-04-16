def recommend_recovery(liquidity_days: int, zone_type: str, volatility: float):
    """
    recovery_engine.py
    
    Logic:
    - If liquidity_days > 100 → "Sell Now" (Risk of further deterioration)
    - If prime zone + low volatility → "Hold" (High probability of recovery)
    """
    
    strategy = "Hold & Monitor"
    timeline = "12 - 24 Months"
    reason = "Stable zone metrics suggest long-term asset value retention."
    
    if liquidity_days > 100:
        strategy = "Aggressive Liquidation (Sell Now)"
        timeline = "0 - 3 Months"
        reason = "High holding risk due to low liquidity ( > 100 days)."
    
    elif zone_type == "prime" and volatility < 0.3:
        strategy = "Strategic Hold"
        timeline = "24 - 36 Months"
        reason = "Prime asset in stable market; recovery potential is high."
        
    return {
        "strategy": strategy,
        "timeline_months": timeline,
        "rationale": reason,
        "recovery_confidence": "High" if zone_type == "prime" else "Moderate"
    }
