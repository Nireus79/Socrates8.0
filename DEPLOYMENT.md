# Socrates 8.0 - Deployment Guide

**Version:** 1.0
**Last Updated:** October 17, 2025
**Status:** Production-Ready

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Docker Setup](#docker-setup)
4. [Local Development](#local-development)
5. [Staging Deployment](#staging-deployment)
6. [Production Deployment](#production-deployment)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Overview

Socrates 8.0 is a containerized, full-stack AI-powered Socratic questioning platform built with:

- **Backend:** FastAPI (Python 3.11)
- **Frontend:** React 18 with TypeScript
- **Database:** PostgreSQL 15
- **Caching:** Redis 7 (optional)
- **Containerization:** Docker & Docker Compose
- **Orchestration:** docker-compose.yml

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Internet/Users                        │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│              Docker Network (socrates-network)          │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │   Frontend   │  │   Backend    │  │ PostgreSQL  │ │
│  │   :3000      │  │   :8000      │  │   :5432     │ │
│  │   (React)    │  │   (FastAPI)  │  │ (Database)  │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
│                                                         │
│  ┌──────────────┐                                       │
│  │    Redis     │                                       │
│  │   :6379      │                                       │
│  │  (Cache)     │                                       │
│  └──────────────┘                                       │
│                                                         │
└────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### System Requirements

- **OS:** macOS, Linux, or Windows (WSL2)
- **Docker:** 20.10+ ([Install](https://docs.docker.com/get-docker/))
- **Docker Compose:** 2.0+ (included with Docker Desktop)
- **RAM:** Minimum 4GB available for containers
- **Disk:** Minimum 5GB free space
- **Network:** Ports 3000, 5432, 6379, 8000 available

### API Requirements

- **Claude API Key:** Required for AI features (get from [Anthropic Console](https://console.anthropic.com))
- **Environment:** Development, Staging, or Production

### Optional Tools

- **PostgreSQL Client:** `psql` for database debugging
- **Redis CLI:** `redis-cli` for cache debugging
- **cURL:** For API endpoint testing

---

## Docker Setup

### 1. Clone and Prepare

```bash
# Clone the repository
git clone <repo-url>
cd Socrates-8.0

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file with your settings:

```bash
# Essential
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
JWT_SECRET_KEY=your-strong-random-secret-key

# Optional (defaults provided)
DB_PASSWORD=socrates123
ENVIRONMENT=development
```

### 3. Build Docker Images

```bash
# Build all images
docker-compose build

# Output: Successfully built socrates-backend, socrates-frontend
```

### 4. Verify Docker Setup

```bash
# Check images were built
docker images | grep socrates

# Expected output:
# socrates-8.0-backend          latest    abc123...   10 seconds ago   250MB
# socrates-8.0-frontend         latest    def456...   15 seconds ago   180MB
```

---

## Local Development

### Starting the Application

```bash
# Start all services in background
docker-compose up -d

# Watch logs
docker-compose logs -f

# Or start specific service
docker-compose up -d backend
docker-compose logs backend
```

### Accessing Services

Once containers are running:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Database:** localhost:5432 (psql)
- **Redis:** localhost:6379 (redis-cli)

### Health Checks

```bash
# Check all services
docker-compose ps

# Expected output:
# NAME                COMMAND             STATUS
# socrates-backend    uvicorn src.main    Up (healthy)
# socrates-frontend   serve -s dist       Up (healthy)
# socrates-db         postgres            Up (healthy)
# socrates-redis      redis-server        Up (healthy)

# Test specific service
curl -s http://localhost:8000/health | jq .
```

### Stopping Services

```bash
# Stop all containers (data preserved)
docker-compose down

# Stop and remove volumes (CAREFUL: deletes data)
docker-compose down -v

# Stop specific service
docker-compose stop backend
```

### Viewing Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Follow logs (real-time)
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend

# With timestamps
docker-compose logs -t backend
```

### Database Access

```bash
# Connect to PostgreSQL container
docker-compose exec postgres psql -U socrates -d socrates_db

# Common psql commands
\dt                    -- List tables
\d users              -- Describe table
SELECT * FROM users;  -- Query data
\q                    -- Quit
```

### Debugging

```bash
# Execute command in running container
docker-compose exec backend bash

# View environment variables
docker-compose exec backend env | grep DATABASE

# Check network connectivity
docker-compose exec backend curl -s postgres:5432

# Test API endpoint
docker-compose exec frontend curl http://backend:8000/health
```

---

## Staging Deployment

### Staging Environment Setup

```bash
# Create staging .env
cp .env.example .env.staging

# Configure for staging
cat > .env.staging << EOF
ENVIRONMENT=staging
JWT_SECRET_KEY=staging-secret-key-12345
CLAUDE_API_KEY=<your-staging-key>
DB_PASSWORD=strong-password-here
CORS_ORIGINS=https://staging.socrates.example.com
EOF
```

### Deploy to Staging

```bash
# Using environment file
docker-compose --env-file .env.staging up -d

# Or with specific file name
export COMPOSE_FILE=docker-compose.yml
export COMPOSE_PROJECT_NAME=socrates-staging
docker-compose up -d
```

### Staging Validation

```bash
# Check all containers running
docker-compose ps

# Test API endpoints
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"TestPass123"}'

# Test frontend
curl -s http://localhost:3000 | head -20

# Check database
docker-compose exec postgres psql -U socrates -d socrates_db -c "SELECT COUNT(*) FROM users;"
```

### Staging Backup

```bash
# Backup database before updates
docker-compose exec postgres pg_dump -U socrates socrates_db > backup-staging-$(date +%Y%m%d).sql

# Restore from backup
docker-compose exec -T postgres psql -U socrates socrates_db < backup-staging-20251017.sql
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] All tests passing: `pytest tests/ -v --cov=src`
- [ ] Environment variables configured securely
- [ ] Database backups enabled
- [ ] SSL/TLS certificates obtained
- [ ] Monitoring and logging configured
- [ ] Disaster recovery plan documented

### Production Environment Setup

```bash
# Create production .env
cp .env.example .env.production

# Configure for production (SECURE!)
cat > .env.production << EOF
ENVIRONMENT=production
JWT_SECRET_KEY=$(openssl rand -base64 32)
CLAUDE_API_KEY=<your-production-key>
DB_PASSWORD=$(openssl rand -base64 16)
REACT_APP_API_URL=https://api.socrates.example.com
REACT_APP_WS_URL=wss://api.socrates.example.com
CORS_ORIGINS=https://socrates.example.com,https://www.socrates.example.com
EOF

# Restrict permissions
chmod 600 .env.production
```

### Production Deployment

```bash
# Update to latest code
git pull origin main

# Rebuild images for production
docker-compose -f docker-compose.yml build --no-cache

# Stop staging/dev containers
docker-compose down

# Deploy production
docker-compose --env-file .env.production up -d

# Verify all services
docker-compose ps
```

### SSL/TLS Setup (Nginx Reverse Proxy)

Create `nginx.conf`:

```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:3000;
}

server {
    listen 443 ssl http2;
    server_name socrates.example.com;

    ssl_certificate /etc/nginx/certs/cert.pem;
    ssl_certificate_key /etc/nginx/certs/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
    }
}

server {
    listen 80;
    server_name socrates.example.com;
    return 301 https://$server_name$request_uri;
}
```

### Production Verification

```bash
# Health check
curl -s https://api.socrates.example.com/health | jq .

# Check response times
time curl -s https://api.socrates.example.com/health > /dev/null

# Monitor logs
docker-compose logs -f --tail=50
```

---

## Monitoring & Maintenance

### Container Monitoring

```bash
# Resource usage
docker stats

# Container logs
docker-compose logs -f backend

# Docker events
docker events
```

### Database Maintenance

```bash
# Backup schedule (add to crontab)
0 2 * * * docker-compose exec -T postgres pg_dump -U socrates socrates_db > /backups/db-$(date +\%Y\%m\%d).sql

# Analyze query performance
docker-compose exec postgres psql -U socrates -d socrates_db -c "EXPLAIN ANALYZE SELECT * FROM sessions LIMIT 10;"

# Vacuum database
docker-compose exec postgres psql -U socrates -d socrates_db -c "VACUUM ANALYZE;"
```

### Log Management

```bash
# Centralize logs
docker-compose logs --no-color > /var/log/socrates.log

# Rotate logs (add to logrotate)
/var/log/socrates.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
}
```

### Alerting

Configure monitoring for:
- Container restart count
- Memory usage > 80%
- Database connection count > threshold
- API response time > 1s
- Error rate > 1%

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
BACKEND_PORT=8001 docker-compose up -d
```

#### 2. Database Connection Failed

```bash
# Check if postgres is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Verify network
docker network ls
docker network inspect socrates-network

# Restart database
docker-compose restart postgres
```

#### 3. Frontend Can't Connect to Backend

```bash
# Check API URL
docker-compose exec frontend env | grep REACT_APP

# Test connectivity from frontend container
docker-compose exec frontend curl http://backend:8000/health

# Check CORS headers
curl -i http://localhost:8000/health
```

#### 4. Out of Memory

```bash
# Check memory usage
docker stats

# Increase Docker memory
# Edit Docker Desktop settings or systemd config

# Prune unused images/containers
docker system prune -a
```

#### 5. Database Locked

```bash
# Check active connections
docker-compose exec postgres psql -U socrates -d socrates_db -c "SELECT * FROM pg_stat_activity;"

# Kill specific connection
docker-compose exec postgres psql -U socrates -d socrates_db -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = 'socrates';"
```

### Emergency Recovery

```bash
# Reset everything
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d

# Restore from backup
docker-compose exec -T postgres psql -U socrates socrates_db < backup.sql
```

---

## Security Best Practices

1. **Secrets Management**
   - Never commit `.env` to git
   - Use `.env.example` for templates
   - Rotate JWT secrets regularly
   - Store API keys in secure vaults

2. **Network Security**
   - Use HTTPS/WSS in production
   - Enable firewall rules
   - Restrict Docker socket access
   - Use network policies

3. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups
   - Apply security patches

4. **API Security**
   - Rate limiting
   - Request validation
   - CORS properly configured
   - JWT token expiration

---

## Performance Optimization

### Database Performance

```bash
# Check slow queries
docker-compose exec postgres psql -U socrates -d socrates_db << EOF
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();
EOF
```

### Cache Configuration

```bash
# Redis optimization
docker-compose exec redis redis-cli CONFIG SET maxmemory 256mb
docker-compose exec redis redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### Scaling Considerations

For production scaling:
- Use load balancer (nginx, HAProxy)
- Multiple backend instances
- Database replication
- Redis cluster
- CDN for frontend assets

---

## Documentation Links

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Production Build](https://create-react-app.dev/docs/production-build/)

---

## Support & Escalation

For issues:

1. Check logs: `docker-compose logs -f`
2. Verify health: `docker-compose ps`
3. Test connectivity: `curl http://localhost:8000/health`
4. Check resources: `docker stats`
5. Review this guide's Troubleshooting section
6. Contact DevOps team or open GitHub issue

---

**Last Updated:** October 17, 2025
**Maintained By:** Development Team
**Version:** 1.0 (Production-Ready)
