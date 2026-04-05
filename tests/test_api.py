# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
from api.main import app
import pytest
from unittest.mock import patch

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"service": "Q-Stream API", "status": "Online"}

@patch("api.main.execute_quantum_circuit.delay")
def test_submit_job(mock_delay):
    # Mocking the delay() call so it returns fake job object
    mock_delay.return_value.id = "fake-job-id"
    # This tests if the API can successfully hand a job to the (mocked) broker
    response = client.post("/run-simulation?qubits=2")
    assert response.status_code == 200
    assert response.json()["job_id"] == "fake-job-id"
    assert response.json["status"] == "QUEUED"

@patch("api.main.AsyncResult")
def test_get_nonexistent_job(mock_async_result):
    # Mock the Celery result object
    mock_async_result.return_value.state = "PENDING"
    mock_async_result.return_value.result = None
    
    response = client.get("/results/invalid_id")
    # Celery returns PENDING for IDs it doesn't know yet
    assert response.status_code == 200
    assert response.json()["state"] == "PENDING"