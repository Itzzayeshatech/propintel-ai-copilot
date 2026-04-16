import math

def calculate_valuation(area_sqft: float, age_years: int, market_data: dict, zone: str):
    """
    valuation_engine.py
    
    Formula:
    market_value = area_sqft * price_per_sqft * demand_index * (1 - age_decay)
    age_decay = age_years * 0.01 (1% depreciation per year)
    distress_value = market_value * 0.75
    liquidity_score = 1 / (liquidity_days / 365)
    """
    if zone not in market_data["zones"]:
        raise ValueError(f"Zone {zone} not found in market dataset.")
    
    data = market_data["zones"][zone]
    price_per_sqft = data["price_per_sqft"]
    demand_index = data["demand_index"]
    liquidity_days = data["liquidity_days"]
    
    age_decay = age_years * 0.01
    market_value = area_sqft * price_per_sqft * demand_index * (1 - age_decay)
    
    distress_value = market_value * 0.75
    liquidity_score = 1 / (liquidity_days / 365) if liquidity_days > 0 else 1.0
    
    return {
        "market_value": round(market_value, 2),
        "distress_value": round(distress_value, 2),
        "liquidity_score": round(liquidity_score, 2),
        "liquidity_days": liquidity_days,
        "price_per_sqft_applied": price_per_sqft,
        "demand_index_applied": demand_index
    }
