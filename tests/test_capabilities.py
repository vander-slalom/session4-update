import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, capabilities

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_capabilities_state():
    original_state = copy.deepcopy(capabilities)
    yield
    capabilities.clear()
    capabilities.update(original_state)

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


def test_root_redirects_to_static_index():
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"

def test_capabilities_filter_by_practice_area():
    response = client.get("/capabilities?practice_area=Strategy")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0
    assert "Digital Strategy" in data

    for name, details in data.items():
        assert details["practice_area"] == "Strategy", f"Found non-Strategy capability: {name}"


def test_capabilities_filter_is_case_insensitive():
    response = client.get("/capabilities?practice_area=strategy")
    assert response.status_code == 200

    data = response.json()
    assert "Digital Strategy" in data
    for details in data.values():
        assert details["practice_area"] == "Strategy"


def test_register_consultant_for_capability():
    email = "new.consultant@slalom.com"

    response = client.post(
        "/capabilities/Cloud Architecture/register",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Registered {email} for Cloud Architecture"}
    assert email in capabilities["Cloud Architecture"]["consultants"]


def test_register_duplicate_consultant_returns_400():
    email = "alice.smith@slalom.com"

    response = client.post(
        "/capabilities/Cloud Architecture/register",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Consultant is already registered for this capability"


def test_unregister_consultant_from_capability():
    email = "alice.smith@slalom.com"

    response = client.delete(
        "/capabilities/Cloud Architecture/unregister",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Cloud Architecture"}
    assert email not in capabilities["Cloud Architecture"]["consultants"]


def test_unregister_non_registered_consultant_returns_400():
    response = client.delete(
        "/capabilities/Cloud Architecture/unregister",
        params={"email": "not.registered@slalom.com"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Consultant is not registered for this capability"


def test_register_unknown_capability_returns_404():
    response = client.post(
        "/capabilities/Unknown Capability/register",
        params={"email": "someone@slalom.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Capability not found"
