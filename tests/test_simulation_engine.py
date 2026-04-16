import pytest
import json
import os
from app.engines.simulation_engine import run_simulation
from app.engines.valuation_engine import calculate_valuation
from app.engines.risk_engine import calculate_risk
from app.engines.decision_engine import calculate_decision

MARKET_DATA = {
    "zones": {
        "Test Zone": {
            "price_per_sqft": 1000,
            "demand_index": 1.0,
            "liquidity_days": 100,
            "volatility_index": 0.5,
            "oversupply_pct": 5,
            "appreciation_rate": 0.1,
            "type": "mid"
        }
    }
}

def test_market_crash_simulation():
    # Baseline input
    base_input = {
        "property_address": "123 Test St",
        "property_type": "Residential",
        "area_sqft": 1000,
        "age_years": 5,
        "zone": "Test Zone"
    }

    sim = run_simulation(base_input, MARKET_DATA, "market_crash_15pc")
    
    # In market crash, volatility goes up by 0.3 (0.5 -> 0.8), price_per_sqft drops by 15%
    # Valuation market_value should be 1000 * 850 * 1.0 * (1 - 0.05) = 807,500
    assert sim["valuation"]["market_value"] == 807500.0
    
    # Risk should explicitly evaluate to High
    assert sim["risk"]["risk_level"] == "High"
    
    # LTV for High Risk should be 0.45
    assert sim["decision"]["ltv"] == 0.45
    
    # ROI should exist and be recalculated
    assert "annualized_roi" in sim["roi"]

def test_demand_drop_simulation():
    base_input = {
        "property_address": "123 Test St",
        "property_type": "Residential",
        "area_sqft": 1000,
        "age_years": 5,
        "zone": "Test Zone"
    }

    sim = run_simulation(base_input, MARKET_DATA, "demand_drop")
    
    # In demand drop, liquidity days doubles (100 -> 200)
    assert sim["valuation"]["liquidity_days"] == 200

if __name__ == "__main__":
    pytest.main([__file__])
