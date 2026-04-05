# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
from api.main import app
import pytest

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"service": "Q-Stream API", "status": "Online"}

def test_submit_job():
    # This tests if the API can successfully hand a job to the (mocked) broker
    response = client.post("/run-simulation?qubits=2")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "QUEUED"

def test_get_nonexistent_job():
    response = client.get("/results/invalid_id")
    # Celery returns PENDING for IDs it doesn't know yet
    assert response.json()["state"] == "PENDING"