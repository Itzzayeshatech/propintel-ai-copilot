def calculate_roi(loan_amount: float, interest_rate: float, risk_level: str, distress_value: float):
    """
    roi_engine.py (HERO)
    
    ROI = ((Interest_Income + Recovery_Value) - (Default_Loss + Holding_Cost)) / Loan
    
    Where (over 3 years):
    - Interest_Income = Loan * rate * 3
    - Default_Loss = Loan * default_probability(risk)
    - Recovery_Value = distress_value * 0.9 (assuming a liquidation haircut)
    - Holding_Cost = Loan * 0.02 * 3 (2% per year management/holding cost)
    """
    
    # Yearly rate to decimal
    rate_decimal = interest_rate / 100
    
    # Default probability based on risk
    dp_map = {
        "Low": 0.02,
        "Medium": 0.05,
        "High": 0.15
    }
    default_prob = dp_map.get(risk_level, 0.20)
    
    interest_income = loan_amount * rate_decimal * 3
    default_loss = loan_amount * default_prob
    recovery_value = distress_value * 0.9
    holding_cost = loan_amount * 0.02 * 3
    
    numerator = (interest_income + recovery_value) - (default_loss + holding_cost)
    roi = (numerator / loan_amount) - 1 # Adjusted ROI over investment
    
    # Annualized ROI
    annualized_roi = ((1 + roi) ** (1/3)) - 1
    
    return {
        "total_roi_3yr": round(roi * 100, 2),
        "annualized_roi": round(annualized_roi * 100, 2),
        "interest_income": round(interest_income, 2),
        "default_loss": round(default_loss, 2),
        "recovery_value_potential": round(recovery_value, 2),
        "holding_cost": round(holding_cost, 2),
        "default_probability": default_prob * 100
    }
