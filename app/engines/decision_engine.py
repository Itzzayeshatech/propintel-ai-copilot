def calculate_decision(market_value: float, risk_level: str):
    """
    decision_engine.py
    
    LTV:
    - Low Risk → 70%
    - Medium Risk → 58%
    - High Risk → 45%
    
    Interest:
    - Base 9%
    - Add risk premium:
      Low +1% (Total 10%)
      Medium +2.2% (Total 11.2%)
      High +4% (Total 13%)
    """
    
    config = {
        "Low": {"ltv": 0.70, "premium": 0.01},
        "Medium": {"ltv": 0.58, "premium": 0.022},
        "High": {"ltv": 0.45, "premium": 0.04}
    }
    
    stats = config.get(risk_level, config["High"])
    ltv = stats["ltv"]
    base_rate = 0.09
    interest_rate = base_rate + stats["premium"]
    
    loan_amount = market_value * ltv
    
    return {
        "decision": "APPROVED" if risk_level != "High" else "APPROVED_WITH_CAUTION",
        "ltv": round(ltv, 2),
        "interest_rate": round(interest_rate * 100, 2),
        "loan_amount": round(loan_amount, 2),
        "base_rate": base_rate * 100,
        "risk_premium": round(stats["premium"] * 100, 2)
    }
