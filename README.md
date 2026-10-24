# SentinelOps — Kubernetes Application Monitoring & Reliability

SentinelOps is a containerized application and observability project built to practise DevOps and Site Reliability Engineering (SRE) concepts. It combines Docker, Kubernetes, Prometheus, and Grafana to demonstrate application deployment, health monitoring, metrics collection, and self-healing.

## Architecture

```text
Developer
   |
   v
Flask Application
   |
   v
Docker Image
   |
   v
Kubernetes Deployment
   |
   +---- SentinelOps Pod 1
   |
   +---- SentinelOps Pod 2
   |
   v
Kubernetes Service
   |
   +---- /health
   +---- /metrics
   |
   v
Prometheus
   |
   +---- Metrics collection
   +---- Alert rules
   |
   v
Grafana
   |
   +---- Monitoring dashboards
```

## Technology Stack

- Python and Flask
- Docker
- Kubernetes and kind
- Prometheus
- Grafana
- YAML configuration
- PowerShell

## Key Features

- Containerized Flask application.
- Kubernetes Deployment configured for two replicas.
- Kubernetes Service for stable application access.
- Readiness and liveness HTTP probes.
- CPU and memory requests and limits.
- Custom Prometheus request counters and latency histograms.
- Prometheus scraping of the Kubernetes application.
- Alert rules for unavailable targets and high request latency.
- Self-healing validation by deleting a Pod and observing its replacement.

## Application Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Application status |
| `/health` | Health check |
| `/info` | Application information |
| `/metrics` | Prometheus metrics |

## Run Locally

Prerequisites: Docker Desktop, kubectl, and kind.

Start the Docker Compose stack:

```bash
docker compose up -d --build
```

Application: http://localhost:5000

Prometheus: http://localhost:9090

Grafana: http://localhost:3000

## Deploy to Kubernetes

Create the cluster if it does not already exist:

```bash
kind create cluster --name sentinelops --image kindest/node:v1.32.0
```

Build the image:

```bash
docker compose build app
```

Load the image into kind:

```bash
kind load docker-image sentinelops-app:v2 --name sentinelops
```

Apply the Kubernetes resources:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/prometheus-config.yaml
kubectl apply -f k8s/alert-rules.yaml
kubectl apply -f k8s/prometheus.yaml
kubectl apply -f k8s/grafana.yaml
```

Check the resources:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

Port-forward the application:

```bash
kubectl port-forward service/sentinelops 8080:5000
```

Open http://localhost:8080/health.

## Reliability Validation

- Confirm both application replicas become Ready.
- Delete one application Pod and observe Kubernetes create a replacement.
- Verify application health through the Service.
- Confirm Prometheus can scrape the application metrics endpoint.
- Verify alert rules are loaded and evaluated.

## Future Improvements

- Automated CI/CD pipeline using AWS developer tools.
- Terraform-based infrastructure provisioning.
- Persistent Grafana storage and secure credentials.
- Additional alerts and service-level indicators.
- Centralized logging and deployment rollback tests.
- Cloud deployment on AWS.

## Project Status

Local containerization, Kubernetes deployment, and self-healing have been exercised. Monitoring and alerting should be considered verified only after confirming target health, dashboard data, and rule evaluation in the running environment.
