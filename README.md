# 🌌 Q-Stream: Distributed Quantum Orchestrator

**Q-Stream** is a high-concurrency, asynchronous task engine designed to bridge the gap between modern web applications and heavy Quantum simulations. By decoupling the API from the execution engine, Q-Stream allows for massive horizontal scaling of Quantum workloads.

---

## 🏗 System Architecture

Unlike a monolithic app, Q-Stream uses a **Distributed Task Queue** pattern. This ensures that long-running Quantum simulations (Qiskit) never block the user interface.

1.  **FastAPI Gateway:** A non-blocking REST API that accepts simulation parameters.
2.  **Redis Broker:** The high-speed "Message Bus" that manages the job queue.
3.  **Celery Workers:** Independent "Quantum Engines" that pull jobs from Redis and execute circuits using the `qiskit-aer` simulator.
4.  **Kubernetes & ArgoCD:** The orchestration layer that ensures self-healing, automated rollouts, and resource management.

---

## 🚀 Getting Started (Local Development)

The entire stack is containerized for a "One-Command" setup.

### Prerequisites
* Docker & Docker Compose V2
* Python 3.11+ (for local testing)

### Quick Start
```bash
# Spin up the API, Worker, and Redis
docker compose up --build

# In a new terminal, submit a 4-qubit Quantum job
curl -X POST "http://localhost:8000/run-simulation?qubits=4"

---

### 🛠 Tech Stack & Engineering Choices

| Component | Technology | Architectural Rationale |
| :--- | :--- | :--- |
| **API** | **FastAPI** | High-performance, asynchronous, and auto-generates OpenAPI docs. |
| **Worker** | **Celery + Qiskit** | Industry standard for distributed task processing and Quantum SDK. |
| **Broker** | **Redis** | In-memory data store for ultra-fast message throughput. |
| **Orchestration** | **Kubernestes** | Ensures 99.9% availability and allows horizontal pod autoscaling. |
| **CI/CD** | **GitHub Actions** | Automated multi-image builds and Minikube integration testing. |

---

### 🔐 Security & Production Readiness

* **Secret Management:** IBM Quantum API tokens are never hardcoded; they are injected via Kubernetes Secrets and GitHub Encrypted Secrets.

* **Resource Guardrails:** Kubernetes `resource.limits` are set to prevent "Circuit Bloat" (OOM errors) from crashing the entire cluster.

* **Asynchronous Flow:** Users receive a `job_id` immediately, allowing for a smooth UX even if the Quantum hardware has a long queue.

---

### 🧪 Testing Suite

We utilize a multi-tier testing strategy to ensure system stability:

```bash
# Run unit tests and API integration tests
PYTHONPATH=. pytest tests/ -v
Unit Tests: Validate the mathematical accuracy of the Quantum GHZ state generation.

Integration Tests: Verify the connectivity between the API gateway and the Redis broker.

📈 Future Roadmap
[ ] Implement WebSockets for real-time simulation progress updates.

[ ] Add PostgreSQL for persistent long-term storage of Quantum results.

[ ] Integrate Grafana/Prometheus for monitoring worker CPU utilization.