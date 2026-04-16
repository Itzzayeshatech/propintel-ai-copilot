def calculate_risk(liquidity_score: float, volatility_index: float, age_years: int):
    """
    risk_engine.py
    
    Logic:
    - High risk if: liquidity < 0.5 OR volatility > 0.8
    - Low if strong liquidity (> 0.8) + low volatility (< 0.3)
    - Medium otherwise
    """
    
    risk_level = "Medium"
    risk_score = (1 - liquidity_score) * 0.5 + (volatility_index) * 0.5
    
    if liquidity_score < 0.5 or volatility_index > 0.8:
        risk_level = "High"
    elif liquidity_score > 0.8 and volatility_index < 0.3:
        risk_level = "Low"
        
    # Adjustment for property age
    if age_years > 20:
        risk_score += 0.1
        if risk_level == "Low":
            risk_level = "Medium"
            
    return {
        "risk_level": risk_level,
        "risk_score": round(min(risk_score, 1.0), 2),
        "volatility": volatility_index,
        "is_stress_test": False
    }
