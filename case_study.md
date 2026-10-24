# Case Study: Automated Monitoring & Alerting System

## 1. Project Overview

This project implements a containerized monitoring and alerting system for a Flask-based File Organizer application. It combines application metrics, health checks, infrastructure management, and automated notifications to improve observability and simplify fault detection.

## 2. Problem Statement

Running an application in containers does not automatically provide sufficient visibility into its health or performance. Without monitoring and alerts, application failures may go unnoticed until users experience problems.

The objective was to build a system that collects metrics, checks application availability, evaluates alert conditions, and notifies the operator when a monitored condition occurs.

## 3. Solution

The solution integrates the following components:

* **Prometheus:** Scrapes application metrics and evaluates alert rules.
* **Blackbox Exporter:** Probes the application health endpoint.
* **Grafana:** Visualizes monitoring metrics.
* **Alertmanager:** Routes alert notifications.
* **Python webhook receiver:** Receives webhook notifications.
* **Gmail SMTP:** Delivers email alerts.
* **Docker Compose:** Runs the application and monitoring services.
* **Terraform:** Manages the monitoring Docker network and persistent data volumes.

## 4. Architecture and Workflow

1. The File Organizer application exposes metrics and a health endpoint.
2. Prometheus collects metrics and evaluates alert rules.
3. Blackbox Exporter checks application health.
4. Prometheus sends firing alerts to Alertmanager.
5. Alertmanager routes notifications to email and the webhook receiver.
6. Grafana provides a visual interface for monitoring metrics.

## 5. Implementation and Validation

The following checks were completed:

* All six Docker Compose services were running during verification.
* Prometheus targets and the application health probe were previously confirmed healthy.
* The `FileOrganizerDown` and `FileOrganizerHealthCheckFailed` rules passed Prometheus rule validation.
* Alertmanager configuration validation succeeded.
* Prometheus configuration validation succeeded.
* Terraform reported no changes to the infrastructure resources it manages.
* A test alert was successfully delivered to the configured Gmail inbox.
* The temporary email-test rule was removed after testing.

## 6. Security Considerations

* SMTP credentials are stored locally and excluded from Git.
* Environment files and Terraform state are excluded from Git.
* Monitoring interfaces are bound to localhost.
* The application is published on port 5001.
* Persistent monitoring volumes are retained to protect stored data.

## 7. Results

The project demonstrates an operational monitoring and notification pipeline connecting application metrics and health checks to automated email and webhook alerts.

The successful email test confirmed end-to-end email delivery for the test alert. Configuration checks also confirmed that the original Prometheus alert rules remained valid after the test rule was removed.

## 8. Future Enhancements

Possible next improvements include:

* SMS notifications through AWS SNS or Twilio.
* Additional Grafana dashboards and performance indicators.
* Automated alert-recovery testing.
* More comprehensive failure simulations.
* Improved deployment automation and operational documentation.

## 9. Skills Demonstrated

* Docker and Docker Compose
* Prometheus monitoring and alert rules
* Grafana observability
* Alertmanager notification routing
* Blackbox health monitoring
* Python webhook development
* Terraform infrastructure as code
* SMTP email integration
* Configuration validation and secret management
