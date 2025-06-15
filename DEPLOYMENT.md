# 🚀 Deployment Guide - Disaster Ready: Earthquake Response Simulator

This guide covers multiple deployment options for the Disaster Ready earthquake response simulator.

## 📋 Prerequisites

### Required
- Python 3.8 or higher
- AWS Account with Bedrock access
- AWS credentials configured

### Optional for Docker deployment
- Docker and Docker Compose
- Nginx (for production)

## 🔧 Environment Setup

### 1. AWS Credentials
```bash
# Option 1: Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1

# Option 2: AWS CLI
aws configure

# Option 3: IAM role (for EC2/ECS deployment)
```

### 2. Environment Variables
Copy `env.example` to `.env` and configure:
```bash
cp env.example .env
# Edit .env with your AWS credentials
```

## 🖥️ Local Development

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Start both API and Streamlit
python run.py
```

### Manual Start
```bash
# Terminal 1: Start API
python main.py

# Terminal 2: Start Streamlit
streamlit run app.py
```

### Access Points
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs  
- **Web Interface**: http://localhost:8501

## 🐳 Docker Deployment

### Single Container (API only)
```bash
# Build image
docker build -t disaster-ready .

# Run container
docker run -p 8000:8000 \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  disaster-ready
```

### Multi-Container with Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- **API**: http://localhost:8000
- **Streamlit**: http://localhost:8501
- **Nginx**: http://localhost:80

## ☁️ AWS Deployment

### Option 1: AWS EC2

#### 1. Launch EC2 Instance
```bash
# Amazon Linux 2 recommended
# Instance type: t3.medium or larger
# Security group: Allow ports 80, 443, 8000, 8501
```

#### 2. Install Dependencies
```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 3. Deploy Application
```bash
# Clone repository
git clone <your-repo-url>
cd disaster_response_simulator

# Set environment variables
cp env.example .env
nano .env  # Configure AWS credentials

# Start services
docker-compose up -d
```

### Option 2: AWS ECS (Elastic Container Service)

#### 1. Create Task Definition
```json
{
  "family": "disaster-ready",
  "taskRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskRole",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "your-account.dkr.ecr.region.amazonaws.com/disaster-ready:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "AWS_DEFAULT_REGION",
          "value": "us-east-1"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/disaster-ready",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 2. Create ECS Service
```bash
# Create cluster
aws ecs create-cluster --cluster-name disaster-ready-cluster

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster disaster-ready-cluster \
  --service-name disaster-ready-service \
  --task-definition disaster-ready:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Option 3: AWS App Runner
```yaml
# apprunner.yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - pip install -r requirements.txt
run:
  runtime-version: 3.9
  command: python main.py
  network:
    port: 8000
    env: PORT
  env:
    - name: AWS_DEFAULT_REGION
      value: us-east-1
```

## 🌐 Production Configuration

### 1. Security Considerations
```bash
# Use HTTPS in production
# Configure CORS appropriately
# Use environment variables for secrets
# Enable rate limiting
# Set up monitoring and logging
```

### 2. Scaling
```bash
# Horizontal scaling with load balancer
# Database for persistent storage
# Redis for session management
# CDN for static assets
```

### 3. Monitoring
```bash
# CloudWatch for AWS deployments
# Application logs
# Health check endpoints
# Performance metrics
```

## 🔍 Testing Deployment

### Health Checks
```bash
# API health
curl http://your-domain:8000/health

# Test endpoints
curl http://your-domain:8000/scenarios
curl -X POST http://your-domain:8000/ask/direct \
  -H "Content-Type: application/json" \
  -d '{"question": "What should I do in an earthquake?"}'
```

### Load Testing
```bash
# Install Apache Bench
sudo yum install httpd-tools

# Basic load test
ab -n 100 -c 10 http://your-domain:8000/health
```

## 🚨 Troubleshooting

### Common Issues

#### 1. AWS Credentials Error
```bash
# Check credentials
aws sts get-caller-identity

# Verify Bedrock access
aws bedrock list-foundation-models --region us-east-1
```

#### 2. Port Issues
```bash
# Check if ports are in use
sudo netstat -tlnp | grep :8000
sudo netstat -tlnp | grep :8501

# Kill processes if needed
sudo pkill -f "python main.py"
sudo pkill -f "streamlit"
```

#### 3. Docker Issues
```bash
# Check Docker status
sudo systemctl status docker

# View container logs
docker logs disaster-ready-api-1
docker logs disaster-ready-streamlit-1
```

#### 4. Memory Issues
```bash
# Check memory usage
free -h
docker stats

# Increase instance size if needed
```

## 📊 Performance Optimization

### API Optimization
```python
# Use async endpoints where possible
# Implement caching for static data
# Optimize database queries
# Use connection pooling
```

### Frontend Optimization
```python
# Cache Streamlit components
# Optimize data loading
# Use session state efficiently
# Implement lazy loading
```

### Infrastructure Optimization
```bash
# Use CDN for static assets
# Enable gzip compression
# Implement Redis caching
# Use read replicas for databases
```

## 🔒 Security Best Practices

### Application Security
- Input validation and sanitization
- Rate limiting on API endpoints  
- HTTPS/TLS encryption
- Security headers
- Regular dependency updates

### AWS Security
- IAM roles with minimal permissions
- VPC with private subnets
- Security groups with least privilege
- Enable CloudTrail logging
- Use AWS Secrets Manager for credentials

### Container Security
- Use non-root users in containers
- Scan images for vulnerabilities
- Use minimal base images
- Update base images regularly

## 📈 Monitoring and Logging

### Application Monitoring
```python
# Add structured logging
import logging
logging.basicConfig(level=logging.INFO)

# Add metrics collection
# Monitor response times
# Track error rates
# Monitor resource usage
```

### AWS Monitoring
```bash
# CloudWatch metrics
# Application logs
# Custom dashboards
# Alerts and notifications
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy Disaster Ready
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to AWS
        run: |
          # Build and deploy steps
```

### Deployment Strategy
- Blue-green deployments
- Rolling updates
- Automated testing
- Rollback procedures

---

## 📞 Support

For deployment issues:
1. Check logs first
2. Verify AWS credentials and permissions
3. Ensure all required ports are open
4. Check system resources (CPU, memory, disk)
5. Review security group and firewall settings

**Emergency Contacts (for real emergencies):**
- Thailand: 191
- Myanmar: 999 