import pytest
import json
import os
from app.engines.valuation_engine import calculate_valuation
from app.engines.risk_engine import calculate_risk
from app.engines.decision_engine import calculate_decision
from app.engines.roi_engine import calculate_roi

# Mock market data for testing
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

def test_valuation_engine():
    # area=1000, age=0, price=1000, demand=1.0 -> 1000 * 1000 * 1.0 * (1-0) = 1,000,000
    res = calculate_valuation(1000, 0, MARKET_DATA, "Test Zone")
    assert res["market_value"] == 1000000.0
    assert res["distress_value"] == 750000.0
    # liquidity_score = 1 / (100/365) = 3.65
    assert res["liquidity_score"] == 3.65

def test_risk_engine():
    # Liquidity score 3.65 (High), volatility 0.5 (Mid) -> Medium
    res = calculate_risk(3.65, 0.5, 5)
    assert res["risk_level"] == "Medium"
    
    # Low liquidity < 0.5 -> High
    res = calculate_risk(0.4, 0.5, 5)
    assert res["risk_level"] == "High"

def test_decision_engine():
    # Medium Risk -> 58% LTV, 11.2% Rate
    res = calculate_decision(1000000, "Medium")
    assert res["loan_amount"] == 580000.0
    assert res["interest_rate"] == 11.2

def test_roi_engine():
    # Loan 580,000, Rate 11.2%, Risk Medium, Distress 750,000
    res = calculate_roi(580000, 11.2, "Medium", 750000)
    assert res["annualized_roi"] > 0
    assert "total_roi_3yr" in res

if __name__ == "__main__":
    pytest.main([__file__])
