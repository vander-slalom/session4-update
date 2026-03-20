import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_capabilities():
    """
    Test that the capabilities endpoint returns a 200 OK response
    and a non-empty dictionary.
    """
    response = client.get("/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "Cloud Architecture" in data

def test_capability_filter_implementation():
    """
    Test that the /capabilities endpoint supports filtering by practice_area.
    Only capabilities matching the requested practice_area should be returned.
    """
    response = client.get("/capabilities?practice_area=Strategy")
    assert response.status_code == 200

    data = response.json()

    # Verify at least one result is returned for a known practice area
    assert len(data) > 0, "Expected at least one Strategy capability"

    # Every returned capability must match the requested practice_area
    for name, details in data.items():
        assert details["practice_area"] == "Strategy", f"Found non-Strategy capability: {name}"

def test_capabilities_endpoint_structure():
    """
    Test that every capability returned by GET /capabilities contains all
    required fields with the correct types.
    """
    response = client.get("/capabilities")
    assert response.status_code == 200
    data = response.json()

    required_fields = [
        "description",
        "practice_area",
        "skill_levels",
        "certifications",
        "industry_verticals",
        "capacity",
        "consultants",
    ]

    for name, details in data.items():
        for field in required_fields:
            assert field in details, f"Capability '{name}' is missing required field '{field}'"
        assert isinstance(details["skill_levels"], list), (
            f"skill_levels for '{name}' should be a list"
        )
        assert isinstance(details["consultants"], list), (
            f"consultants for '{name}' should be a list"
        )
        assert isinstance(details["capacity"], int), (
            f"capacity for '{name}' should be an int"
        )
        assert details["practice_area"] in ("Technology", "Strategy", "Operations"), (
            f"Unexpected practice_area '{details['practice_area']}' for capability '{name}'"
        )
