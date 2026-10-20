
# Configuration du Provider Docker
provider "docker" {
}

# Réseau Docker dédié à notre application
resource "docker_network" "crm_network" {
  name   = "neofacto-mlops-network"
  driver = "bridge"
}

