# Automated Monitoring & Alerting System

A containerized monitoring and alerting solution for a Dockerized Flask application, built using Prometheus, Grafana, Alertmanager, Blackbox Exporter, and Terraform.

The project demonstrates application health monitoring, metrics collection, alert rule evaluation, webhook notifications, email alerts, and infrastructure management.

## Features

* **Application monitoring:** Collects metrics from the File Organizer Flask application.
* **Health checks:** Uses Blackbox Exporter to probe the application's health endpoint.
* **Prometheus:** Scrapes metrics and evaluates alert rules.
* **Grafana:** Provides dashboards for monitoring and visualization.
* **Alertmanager:** Routes alerts to configured notification receivers.
* **Email notifications:** Sends alert notifications through Gmail SMTP.
* **Webhook notifications:** Receives alerts through a custom Python webhook service.
* **Docker Compose:** Runs the monitoring stack as containers.
* **Terraform:** Manages the monitoring Docker network and persistent data volumes.

## Architecture

The monitoring workflow is:

1. The File Organizer application exposes metrics and a health endpoint.
2. Prometheus collects application metrics and evaluates alert rules.
3. Blackbox Exporter probes the application health endpoint.
4. Prometheus sends firing alerts to Alertmanager.
5. Alertmanager routes notifications to the configured email and webhook receivers.
6. Grafana visualizes the available monitoring metrics.

## Technology Stack

* Python and Flask
* Docker and Docker Compose
* Prometheus
* Grafana
* Alertmanager
* Prometheus Blackbox Exporter
* Terraform
* Gmail SMTP
* Python webhook receiver

## Services

| Service           | Local address         |
| ----------------- | --------------------- |
| File Organizer    | http://localhost:5001 |
| Prometheus        | http://localhost:9090 |
| Grafana           | http://localhost:3000 |
| Alertmanager      | http://localhost:9093 |
| Blackbox Exporter | http://localhost:9115 |
| Alert Webhook     | http://localhost:8000 |

The monitoring interfaces are bound to localhost. The application is currently published on port 5001.

## Prerequisites

* Docker Desktop with the Linux container engine
* Docker Compose
* Terraform
* Git

## Getting Started

1. Clone this repository.

2. Open the project directory.

3. Configure any required environment variables and notification credentials using local, untracked files.

4. Review the Docker Compose, Prometheus, and Alertmanager configurations.

5. Start the services:

   ```powershell
   docker compose up -d
   ```

6. Check the container status:

   ```powershell
   docker compose ps
   ```

7. Open the service URLs listed above.

**Security:** Never commit `.env` files, SMTP passwords, private keys, or Terraform state containing sensitive values. Review the configuration before starting the stack.

## Alerting

The project includes two Prometheus alert rules:

* `FileOrganizerDown`
* `FileOrganizerHealthCheckFailed`

Alertmanager is configured to route notifications through email and a custom webhook receiver.

The email delivery pipeline was tested successfully: a test alert was received in the configured Gmail inbox. The temporary test rule was subsequently removed.

## Terraform

The Terraform configuration is located in the `terraform/` directory.

Validate the configuration with:

```powershell
Set-Location .\terraform
terraform init
terraform plan
```

The validated plan reported that the tracked Docker network and persistent Prometheus and Grafana volumes matched the configuration.

Review any proposed changes before considering an apply operation. Do not destroy persistent volumes when restarting or maintaining the monitoring stack.

## Validation Performed

* Alertmanager configuration validation passed.
* Prometheus configuration validation passed.
* Both original alert rules passed `promtool check rules`.
* Prometheus targets and the application health probe were previously verified.
* All six Docker Compose services were running during final checks.
* Terraform plan reported no infrastructure changes.
* Gmail alert delivery was confirmed by receiving the test email.

## Repository Structure

```text
.
├── monitoring/
│   ├── alerts/
│   ├── blackbox/
│   ├── alertmanager.yml
│   ├── alertmanager.yml.template
│   ├── prometheus.yml
│   └── webhook_receiver.py
├── terraform/
│   ├── main.tf
│   └── .terraform.lock.hcl
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── README.md
└── case_study.md
```

## Future Improvements

Potential improvements include SMS notifications, expanded dashboards, automated recovery testing, and additional infrastructure resilience checks.

## Project Purpose

This project demonstrates practical skills in containerization, infrastructure as code, observability, application health monitoring, alert management, and notification integration.
