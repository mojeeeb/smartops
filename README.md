# SmartOps Kubernetes Project

This project implements a security scanning and automation solution using Kubernetes, Trivy, and n8n.

## Components

1. **Python Bot (`bot.py`)**
   - Reads Trivy scan results from a shared volume
   - Sends results to n8n webhook
   - Monitored by Prometheus

2. **Trivy Scanner**
   - Runs as a Kubernetes CronJob
   - Scans the bot image regularly
   - Stores results in a shared volume

3. **Monitoring**
   - Prometheus for metrics collection
   - Grafana for visualization
   - ServiceMonitor for automatic discovery

## Prerequisites

- Kubernetes cluster
- ArgoCD installed
- n8n running locally (outside Kubernetes)
- Helm 3.x

## Installation

1. Clone the repository:
   ```bash
   git clone __REPO_URL__
   ```

2. Update the ArgoCD application manifest with your repository URL:
   ```bash
   sed -i 's/__REPO_URL__/your-repo-url/' argocd-app.yaml
   ```

3. Apply the ArgoCD application:
   ```bash
   kubectl apply -f argocd-app.yaml
   ```

## Configuration

The project can be configured through the `values.yaml` file:

- Bot configuration (image, replicas, n8n webhook URL)
- Trivy scan schedule
- Prometheus and Grafana settings
- Resource limits and requests
- Storage configuration

## Accessing Services

- Grafana: `http://localhost:3000` (default credentials: admin/admin)
- Prometheus: `http://localhost:9090`
- Bot metrics: Available through Prometheus

## Development

To build the bot image:

```bash
docker build -t smartops-bot:latest .
```

## License

MIT 