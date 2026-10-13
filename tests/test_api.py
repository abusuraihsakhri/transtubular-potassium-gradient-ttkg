"""Smoke tests for the container entry point and operations console."""
from fastapi.testclient import TestClient
from agents.api import app

client = TestClient(app)


def test_server_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"


def test_console_loads_and_does_not_fake_responses():
    response = client.get("/console/")
    assert response.status_code == 200
    assert "runAudit()" in response.text
    assert "DOSSIER-SIM-" not in response.text


def test_root_redirects_to_console():
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/console/"


def test_api_audit_smoke():
    response = client.post("/api/audit", json={
        "task_id": "TEST-001",
        "target_identifier": "SPECIMEN-001",
        "primary_metric": 10,
        "secondary_metric": 5,
        "status_descriptor": "NOMINAL"
    })
    assert response.status_code == 200
    assert response.json()["audit_hash"]


def test_api_rejects_missing_required_fields():
    assert client.post("/api/audit", json={"task_id": "TEST"}).status_code == 422
