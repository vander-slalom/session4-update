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
    FAILING TEST: This test is a placeholder to demonstrate a missing feature.
    
    The current API does not support filtering by 'practice_area'.
    This test expects a filtered list but will receive the full list (or fail differently).
    
    QE/Dev Task: Implement the filtering logic in app.py or update this test to match actual requirements.
    """
    response = client.get("/capabilities?practice_area=Strategy")
    assert response.status_code == 200
    
    data = response.json()
    
    # This assertion will fail because the API ignores the query param and returns everything
    # We expect ONLY 'Strategy' items (e.g., "Digital Strategy")
    for name, details in data.items():
        assert details["practice_area"] == "Strategy", f"Found non-Strategy capability: {name}"
