# Java RabbitMQ AKS Demo

## Architecture Overview
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ User Service│    │Order Service│    │Analytics    │
│   (Java)    │    │   (Java)    │    │Consumer     │
│             │    │             │    │ (Python)    │
└─────┬───────┘    └─────┬───────┘    └─────┬───────┘
      │                  │                  │
      │                  │                  │
┌─────▼──────────────────▼──────────────────▼───────┐
│              PostgreSQL Database                  │
└───────────────────────────────────────────────────┘
                         │
                         │
┌────────────────────────▼───────────────────────────┐
│                  RabbitMQ                          │
└────────────────────────────────────────────────────┘
                         │
                         │
┌────────────────────────▼───────────────────────────┐
│            Prometheus + Grafana                    │
└────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Local Development
```bash
# Start infrastructure
cd local && docker-compose up -d

# Build and run user-service
cd services/user-service
mvn spring-boot:run

# Build and run order-service  
cd services/order-service
mvn spring-boot:run

# Run analytics consumer
cd services/analytics-consumer
pip install -r requirements.txt
python main.py
```

### 2. Test the Services
```bash
# Create a user
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'

# Create an order (triggers RabbitMQ message)
curl -X POST http://localhost:8081/api/orders \
  -H "Content-Type: application/json" \
  -d '{"userId":1,"total":99.99}'

# Check analytics consumer metrics
curl http://localhost:8082/metrics
```

## Learning Guide for Beginners

### Core Concepts Explained

#### 1. **Microservices Architecture**
- **What it is**: Breaking a large application into small, independent services
- **Why**: Each service can be developed, deployed, and scaled independently
- **In our project**: We have 3 services that each do one thing well

#### 2. **Spring Boot (Java Framework)**
- **What it is**: A framework that makes Java web development easier
- **Key files to understand**:
  - `pom.xml`: Lists dependencies (like libraries your code needs)
  - `Application.java`: The main entry point that starts your service
  - `Controller.java`: Handles HTTP requests (GET, POST, etc.)
  - `Entity.java`: Represents database tables as Java objects
  - `Repository.java`: Provides database operations

#### 3. **Database Integration (JPA/Hibernate)**
- **What it is**: Automatically converts Java objects to database tables
- **How it works**: You define a class, and it creates a table
- **Example**: Our `User` class becomes a `users` table

#### 4. **Message Queues (RabbitMQ)**
- **What it is**: A way for services to communicate asynchronously
- **Why**: Services don't have to wait for each other
- **Flow**: Order Service → RabbitMQ → Analytics Consumer

#### 5. **Containerization (Docker)**
- **What it is**: Packages your app with everything it needs to run
- **Why**: "It works on my machine" → "It works everywhere"
- **Dockerfile**: Instructions for building a container

#### 6. **Kubernetes (Container Orchestration)**
- **What it is**: Manages containers in production
- **Key concepts**:
  - **Pod**: Smallest unit (usually 1 container)
  - **Deployment**: Manages multiple pods
  - **Service**: Network access to pods
  - **Ingress**: External access routing

#### 7. **Monitoring (Prometheus + Grafana)**
- **Prometheus**: Collects metrics from your services
- **Grafana**: Creates dashboards to visualize metrics
- **Metrics**: Things like request count, response time, errors

### Development Workflow

#### 1. **Local Development**
```bash
# 1. Start databases/message queue
docker-compose up -d

# 2. Run your service
mvn spring-boot:run

# 3. Test with curl or Postman
curl http://localhost:8080/api/users
```

#### 2. **Making Changes**
1. Edit Java code
2. Spring Boot auto-reloads (in most cases)
3. Test your changes
4. Commit to git

#### 3. **Deployment Process**
1. Push code to GitHub
2. GitHub Actions builds and tests
3. Creates Docker images
4. Deploys to Kubernetes

### Key Files and Their Purpose

```
services/user-service/
├── pom.xml                 # Dependencies and build config
├── Dockerfile             # Container build instructions
└── src/main/java/
    ├── UserServiceApplication.java  # Main entry point
    ├── User.java                   # Database model
    ├── UserRepository.java         # Database operations
    └── UserController.java         # HTTP endpoints

infra/k8s/                 # Kubernetes deployment files
├── namespace.yml          # Logical grouping
├── user-service.yml       # How to run user-service
└── ingress.yml           # External access rules

.github/workflows/         # CI/CD automation
└── ci.yml                # Build, test, deploy pipeline
```

### Common Commands You'll Use

#### Maven (Java Build Tool)
```bash
mvn clean compile          # Compile code
mvn test                  # Run tests
mvn spring-boot:run       # Run locally
mvn package              # Build JAR file
```

#### Docker
```bash
docker build -t myapp .           # Build image
docker run -p 8080:8080 myapp    # Run container
docker ps                        # List running containers
```

#### Kubernetes
```bash
kubectl get pods                 # List running pods
kubectl logs pod-name           # View logs
kubectl apply -f file.yml       # Deploy/update
kubectl port-forward pod 8080:8080  # Access pod locally
```

### Learning Path Recommendations

#### Week 1: Basics
1. Understand REST APIs (GET, POST, PUT, DELETE)
2. Learn basic Java syntax
3. Understand what Spring Boot does
4. Run the services locally

#### Week 2: Data & Messaging  
1. Learn about databases and SQL
2. Understand JPA/Hibernate basics
3. Learn about message queues
4. Test the complete flow

#### Week 3: Containers & Deployment
1. Learn Docker basics
2. Understand Kubernetes concepts
3. Deploy to local Kubernetes (kind)
4. Set up monitoring

#### Week 4: Production Concerns
1. Learn about CI/CD pipelines
2. Understand monitoring and logging
3. Deploy to cloud (AKS)
4. Learn troubleshooting

### Troubleshooting Common Issues

#### Service Won't Start
1. Check if database is running: `docker ps`
2. Check application logs for errors
3. Verify environment variables are set

#### Can't Connect to Database
1. Check connection string in `application.yml`
2. Verify database credentials
3. Ensure database is accessible from your service

#### RabbitMQ Messages Not Processing
1. Check RabbitMQ management UI: http://localhost:15672
2. Verify queue exists and has messages
3. Check consumer logs for errors

### Next Steps
1. Start with local development
2. Make small changes and see what happens
3. Read Spring Boot documentation
4. Join developer communities (Stack Overflow, Reddit)
5. Practice with small projects

Remember: Everyone starts somewhere. Focus on understanding one concept at a time, and don't hesitate to ask questions!