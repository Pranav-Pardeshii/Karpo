"""
Unit tests for CACP cultivation cost service.
"""

from crop_advisory.services.cultivation_cost_service import (
    get_available_states,
    get_cultivation_cost,
)


def test_cost_lookup_paddy(cost_service):
    cost_info = cost_service.get_cultivation_cost("rice")
    assert cost_info["cul_cost_c2_per_ha"] > 10000.0
    assert cost_info["cul_cost_c2_per_acre"] > 0
    assert cost_info["prod_cost_c2_per_quintal"] > 0
    assert cost_info["seed_cost_per_ha"] >= 0


def test_cost_lookup_state_specific():
    cost_info = get_cultivation_cost("cotton", state_name="Gujarat")
    assert cost_info["cul_cost_c2_per_ha"] > 0
    assert "Gujarat" in cost_info["applied_state"] or "National" in cost_info["applied_state"]


def test_available_states_list():
    states = get_available_states()
    assert len(states) >= 15
    assert "Maharashtra" in states or "Punjab" in states or "Gujarat" in states


def test_horticultural_cost_fallback(cost_service):
    cost_info = cost_service.get_cultivation_cost("banana")
    assert cost_info["cul_cost_c2_per_ha"] > 0
    assert "NHB" in cost_info["source"]
