# Java Microservices on Azure Kubernetes Service

[![Build Status](https://github.com/Simodalstix/java-rabbitmq-aks/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/Simodalstix/java-rabbitmq-aks/actions)
[![Release](https://img.shields.io/github/v/release/Simodalstix/java-rabbitmq-aks)](https://github.com/Simodalstix/java-rabbitmq-aks/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Java](https://img.shields.io/badge/Java-17-orange.svg)](https://openjdk.java.net/projects/jdk/17/)
[![Terraform](https://img.shields.io/badge/Terraform-1.6+-blue.svg)](https://www.terraform.io/)

A production-style microservices application demonstrating Java Spring Boot services with RabbitMQ messaging, deployed on Azure Kubernetes Service using Terraform-managed infrastructure.

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ User Service│    │Order Service│    │Analytics    │
│   (Java)    │────│   (Java)    │────│Consumer     │
│             │    │             │    │ (Python)    │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                  ┌────────▼────────┐
                  │   PostgreSQL    │
                  │   + RabbitMQ    │
                  └─────────────────┘
```

**Services:**
- **User Service** (Java/Spring Boot): CRUD operations with PostgreSQL
- **Order Service** (Java/Spring Boot): Order processing with RabbitMQ publishing  
- **Analytics Consumer** (Python/FastAPI): Event processing with Prometheus metrics

**Infrastructure:**
- **Azure Kubernetes Service** (AKS): Container orchestration
- **Azure PostgreSQL**: Managed database with firewall rules
- **RabbitMQ**: Message broker for async communication
- **Terraform**: Infrastructure as Code

## Quick Start

### Local Development

```bash
# 1. Start infrastructure
cd local && docker-compose up -d

# 2. Run services
cd services/user-service && mvn spring-boot:run &
cd services/order-service && mvn spring-boot:run &
cd services/analytics-consumer && pip install -r requirements.txt && python main.py &

# 3. Test the API
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'
```

### Azure Deployment

```bash
# 1. Deploy infrastructure
cd infra/terraform
terraform init
terraform plan
terraform apply

# 2. Configure kubectl
az aks get-credentials --resource-group rg-java-rabbitmq-aks --name aks-java-rabbitmq

# 3. Deploy applications (automated via GitHub Actions)
git push origin main
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Java 17 + Spring Boot | REST APIs and business logic |
| **Database** | PostgreSQL (Azure) | Data persistence |
| **Messaging** | RabbitMQ | Async service communication |
| **Container** | Docker + Kubernetes | Application packaging and orchestration |
| **Infrastructure** | Terraform + Azure | Cloud resource management |
| **CI/CD** | GitHub Actions | Automated build and deployment |

## Cost Considerations

**Estimated monthly cost (Australia Southeast):**
- AKS cluster (2 B2s nodes): ~$70 AUD
- PostgreSQL Flexible Server: ~$15 AUD  
- **Total: ~$85 AUD/month**

**Cost optimizations:**
- Single NAT Gateway (vs. per-AZ)
- B-series VMs (burstable performance)
- Terraform destroy when not needed

## Project Structure

```
├── services/
│   ├── user-service/          # Java Spring Boot CRUD API
│   ├── order-service/         # Java Spring Boot with RabbitMQ
│   └── analytics-consumer/    # Python FastAPI consumer
├── infra/
│   ├── terraform/            # Azure infrastructure
│   └── k8s/                  # Kubernetes manifests
├── local/
│   └── docker-compose.yml    # Local development setup
└── .github/workflows/        # CI/CD pipelines
```

## Development

**Prerequisites:**
- Java 17+
- Maven 3.6+
- Docker & Docker Compose
- Azure CLI (for deployment)

**Build and test:**
```bash
# Java services
mvn clean verify

# Python service  
pip install -r requirements.txt
python -m pytest

# Infrastructure
terraform fmt -check
terraform validate
```

## Why This Matters

This project demonstrates real-world patterns for:
- **Microservices architecture** with proper service boundaries
- **Event-driven communication** using message queues
- **Cloud-native deployment** on managed Kubernetes
- **Infrastructure as Code** with Terraform
- **Production concerns** like health checks, metrics, and auto-scaling

Perfect for understanding how modern distributed systems work in practice.

## License

MIT License - see [LICENSE](LICENSE) file for details.