terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}

resource "docker_network" "monitoring" {
  name   = "monitoring-network"
  driver = "bridge"

  lifecycle {
    prevent_destroy = true
  }
}

output "monitoring_network_name" {
  description = "Name of the Terraform-managed Docker monitoring network"
  value       = docker_network.monitoring.name
}

resource "docker_volume" "grafana_data" {
  name = "fileorganizer_grafana-data"

  labels {
    label = "com.docker.compose.config-hash"
    value = "fccca448401d091817f4cac9b27cd3e0608a269b49805fdf4b65b7b3e1fb9d7b"
  }

  labels {
    label = "com.docker.compose.project"
    value = "fileorganizer"
  }

  labels {
    label = "com.docker.compose.version"
    value = "5.6.0"
  }

  labels {
    label = "com.docker.compose.volume"
    value = "grafana-data"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "docker_volume" "prometheus_data" {
  name = "fileorganizer_prometheus-data"

  labels {
    label = "com.docker.compose.config-hash"
    value = "25ba4c52cc96735c77f4bcb2528f6240a71f3464ac5b51e7f29dfa7932287f4d"
  }

  labels {
    label = "com.docker.compose.project"
    value = "fileorganizer"
  }

  labels {
    label = "com.docker.compose.version"
    value = "5.6.0"
  }

  labels {
    label = "com.docker.compose.volume"
    value = "prometheus-data"
  }

  lifecycle {
    prevent_destroy = true
  }
}

output "grafana_volume_name" {
  description = "Existing persistent Grafana data volume"
  value       = docker_volume.grafana_data.name
}

output "prometheus_volume_name" {
  description = "Existing persistent Prometheus data volume"
  value       = docker_volume.prometheus_data.name
}