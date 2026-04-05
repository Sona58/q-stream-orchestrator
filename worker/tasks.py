# -*- coding: utf-8 -*-

import os
import time
from celery import Celery
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Configure Celery to use Redis as the Broker and Result Backend
# In K8s, 'redis-service' will be the internal DNS name for our Redis pod
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis-service:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis-service:6379/0")

app = Celery("quantum_tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@app.task(name="execute_quantum_circuit", bind=True)
def execute_quantum_circuit(self, num_qubits: int):
    """
    Simulates a GHZ State (Entanglement) circuit.
    This is the 'Heavy Lifting' that runs asynchronously.
    """
    try:
        # 1. Update status for the user to see
        self.update_state(state='PROGRESS', meta={'status': 'Initializing Simulator'})
        
        # 2. Build the Circuit (The Physics Logic)
        qc = QuantumCircuit(num_qubits)
        qc.h(0)
        for i in range(num_qubits - 1):
            qc.cx(i, i + 1)
        qc.measure_all()

        # 3. Simulate execution time (to mimic real QPU latency)
        # As an architect, we add this to test how our queue handles 'busy' workers
        self.update_state(state='PROGRESS', meta={'status': 'Running Simulation...'})
        time.sleep(5) 

        # 4. Run the simulation
        simulator = AerSimulator()
        job = simulator.run(qc, shots=1024)
        result = job.result()
        counts = result.get_counts()

        # 5. Return the final result to the Redis Backend
        return {
            "num_qubits": num_qubits,
            "counts": counts,
            "status": "COMPLETED",
            "engine": "AerSimulator-V1"
        }

    except Exception as e:
        # Handle failures gracefully so the worker doesn't die
        return {"status": "FAILED", "error": str(e)}