from app.engines.valuation_engine import calculate_valuation
from app.engines.risk_engine import calculate_risk
from app.engines.decision_engine import calculate_decision
from app.engines.roi_engine import calculate_roi
import copy

def run_simulation(base_input: dict, market_data: dict, scenario: str):
    """
    simulation_engine.py
    
    Scenarios:
    1. market_crash_15pc: price *= 0.85, recalc risk/valuation
    2. demand_drop: liquidity_days *= 2
    3. rate_spike: base_rate += 2% (handled in decision logic)
    """
    
    # Deep copy market data to avoid side effects
    sim_market_data = copy.deepcopy(market_data)
    sim_input = copy.deepcopy(base_input)
    zone = sim_input["zone"]
    
    if scenario == "market_crash_15pc":
        sim_market_data["zones"][zone]["price_per_sqft"] *= 0.85
        sim_market_data["zones"][zone]["volatility_index"] = min(sim_market_data["zones"][zone]["volatility_index"] + 0.3, 1.0)
    
    elif scenario == "demand_drop":
        sim_market_data["zones"][zone]["liquidity_days"] *= 2
        sim_market_data["zones"][zone]["demand_index"] *= 0.7
        
    elif scenario == "rate_spike":
        # We handle this by adding to the calculated interest rate later or by modifying a global 'base_rate' if we had one.
        # For simulation impact, we'll just manually bump the risk premium or mock the rate increase.
        pass

    # Re-evaluate everything
    valuation = calculate_valuation(
        sim_input["area_sqft"], 
        sim_input["age_years"], 
        sim_market_data, 
        zone
    )
    
    risk = calculate_risk(
        valuation["liquidity_score"],
        sim_market_data["zones"][zone]["volatility_index"],
        sim_input["age_years"]
    )
    
    # Add a manual override for scenario if needed
    if scenario == "market_crash_15pc":
        risk["risk_level"] = "High"
        
    decision = calculate_decision(valuation["market_value"], risk["risk_level"])
    
    if scenario == "rate_spike":
        decision["interest_rate"] += 2.0
    
    roi = calculate_roi(
        decision["loan_amount"],
        decision["interest_rate"],
        risk["risk_level"],
        valuation["distress_value"]
    )
    
    return {
        "scenario": scenario,
        "valuation": valuation,
        "risk": risk,
        "decision": decision,
        "roi": roi
    }
