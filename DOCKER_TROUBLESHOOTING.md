# Docker Troubleshooting Guide for Socrates 8.0

**Version:** 1.0
**Last Updated:** October 17, 2025

## Quick Diagnostics

Run this immediately if something isn't working:

```bash
# Check if containers are running
docker-compose ps

# View logs for all services
docker-compose logs

# Check resource usage
docker stats

# Test connectivity
docker-compose exec backend curl http://postgres:5432
docker-compose exec frontend curl http://backend:8000/health
```

---

## Common Issues & Solutions

### Issue 1: "Address already in use" Error

**Error Message:**
```
ERROR: for socrates-backend  Cannot start service backend: driver failed programming external port 8000:
Error starting userland proxy: listen tcp 0.0.0.0:8000: bind: address already in use
```

**Solution:**

```bash
# Find what's using the port
lsof -i :8000

# Kill the process (if it's safe)
kill -9 <PID>

# Or use a different port
BACKEND_PORT=8001 docker-compose up -d backend

# Check what's listening
netstat -tuln | grep LISTEN
```

---

### Issue 2: PostgreSQL Not Starting / Not Healthy

**Error Message:**
```
socrates-db    "docker-entrypoint..."   Restarting (1) 2 seconds ago
```

**Solution:**

```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Common reasons:
# 1. Insufficient disk space
df -h

# 2. Volume permission issues
sudo chown -R 999:999 ./postgres_data

# 3. Corrupt data - start fresh
docker-compose down -v
docker-compose up -d postgres
sleep 10
docker-compose ps postgres

# 4. Check initialization script
docker-compose exec postgres ls -la /docker-entrypoint-initdb.d/

# 5. Verify database exists
docker-compose exec postgres psql -U socrates -d socrates_db -c "\dt"
```

---

### Issue 3: Backend Service Won't Start

**Error Message:**
```
ImportError: cannot import name 'HTTPAuthorizationCredentials' from 'fastapi.security'
ModuleNotFoundError: No module named 'sqlalchemy'
```

**Solution:**

```bash
# Check Python dependencies
docker-compose exec backend pip list | grep -E "fastapi|sqlalchemy|pydantic"

# Rebuild the backend image (clear cache)
docker-compose build --no-cache backend

# Check Python version
docker-compose exec backend python --version

# Review startup logs
docker-compose logs backend --tail=50

# Check if requirements.txt is valid
docker-compose exec backend pip install -r requirements.txt

# Validate the main.py file
docker-compose exec backend python -m py_compile src/main.py
```

---

### Issue 4: Frontend Can't Connect to Backend

**Symptoms:**
- Frontend loads but shows connection error
- API calls fail with CORS error
- "Failed to fetch" messages in browser console

**Solution:**

```bash
# 1. Verify backend is running
curl -s http://localhost:8000/health | jq .

# 2. Check CORS configuration
docker-compose exec backend env | grep CORS

# 3. Test connectivity from frontend container
docker-compose exec frontend curl http://backend:8000/health

# 4. Check frontend environment variables
docker-compose exec frontend env | grep REACT_APP

# 5. Verify both are on same network
docker network inspect socrates-network

# 6. Check backend logs
docker-compose logs backend | grep -i cors
docker-compose logs backend | grep -i error

# 7. Rebuild frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

---

### Issue 5: Database Connection Issues

**Error Message:**
```
"could not connect to server: Connection refused"
"fe_sendauth: no password supplied"
```

**Solution:**

```bash
# 1. Verify PostgreSQL container is running and healthy
docker-compose ps postgres

# 2. Check database credentials
cat .env | grep DB_

# 3. Test connection directly
docker-compose exec postgres psql -U socrates -d socrates_db -c "SELECT 1;"

# 4. Check backend connection string
docker-compose exec backend env | grep DATABASE_URL

# 5. Verify network connectivity
docker-compose exec backend ping postgres

# 6. Check PostgreSQL logs
docker-compose logs postgres | tail -30

# 7. Restart PostgreSQL
docker-compose restart postgres
sleep 5
docker-compose ps postgres
```

---

### Issue 6: Redis Connection Issues

**Error Message:**
```
"Error: connect ECONNREFUSED 127.0.0.1:6379"
```

**Solution:**

```bash
# 1. Check if Redis is running
docker-compose ps redis

# 2. Test Redis connectivity
docker-compose exec redis redis-cli ping

# 3. Check Redis logs
docker-compose logs redis

# 4. Verify Redis network
docker-compose exec backend redis-cli -h redis ping

# 5. Restart Redis
docker-compose restart redis

# 6. Check Redis memory
docker-compose exec redis redis-cli info memory
```

---

### Issue 7: Health Checks Failing

**Error Message:**
```
unhealthy
```

**Solution:**

```bash
# 1. Check which service is failing
docker-compose ps

# 2. Inspect health check logs
docker inspect socrates-backend --format='{{.State.Health}}'

# 3. Check backend health endpoint
curl -v http://localhost:8000/health

# 4. Check frontend health
curl -v http://localhost:3000

# 5. Increase health check timeout (edit docker-compose.yml)
# Change "start_period: 40s" to 60s or 90s

# 6. Restart service after changes
docker-compose up -d backend
```

---

### Issue 8: Out of Memory / High Resource Usage

**Symptoms:**
- Containers crashing randomly
- System running very slowly
- "Cannot allocate memory" errors

**Solution:**

```bash
# 1. Check resource usage
docker stats

# 2. Identify high-memory service
docker stats --no-stream | sort -k4 -rh

# 3. Check memory limits
docker inspect socrates-backend --format='{{.HostConfig.Memory}}'

# 4. Set memory limits (edit docker-compose.yml)
# Add to service:
# deploy:
#   resources:
#     limits:
#       memory: 1G

# 5. Prune unused containers and images
docker system prune
docker system prune -a

# 6. Restart Docker daemon
sudo systemctl restart docker  # Linux
# Or restart Docker Desktop

# 7. Check disk space
du -sh ./*
df -h
```

---

### Issue 9: Network Issues

**Error Message:**
```
"Cannot assign requested address"
"Network timeout"
```

**Solution:**

```bash
# 1. Check network status
docker network ls
docker network inspect socrates-network

# 2. Verify all containers on same network
docker-compose ps
docker inspect socrates-backend --format='{{.HostConfig.NetworkMode}}'

# 3. Test container-to-container communication
docker-compose exec backend ping postgres
docker-compose exec backend ping redis
docker-compose exec backend ping frontend

# 4. Check DNS resolution
docker-compose exec backend nslookup postgres
docker-compose exec backend getent hosts postgres

# 5. Recreate network
docker network rm socrates-network
docker-compose up -d

# 6. Check firewall rules
sudo iptables -L -n
```

---

### Issue 10: Docker Build Failures

**Error Message:**
```
"failed to solve with frontend dockerfile.v0"
"pip: command not found"
```

**Solution:**

```bash
# 1. Check Docker build logs
docker-compose build --no-cache backend 2>&1 | tail -30

# 2. Rebuild with verbose output
docker build -t socrates-backend:test ./Socrates-8.0/backend --no-cache -v

# 3. Verify base image availability
docker pull python:3.11-slim
docker pull node:18-alpine

# 4. Check for typos in Dockerfile
cat ./Socrates-8.0/backend/Dockerfile | grep -E "RUN|COPY|FROM"

# 5. Ensure requirements.txt exists
ls -la ./Socrates-8.0/backend/requirements.txt

# 6. Clean Docker cache
docker builder prune -a

# 7. Verify disk space (builds need space)
df -h
```

---

## Debugging Techniques

### Accessing Container Shell

```bash
# Access backend bash
docker-compose exec backend bash

# Access frontend bash
docker-compose exec frontend bash

# Access PostgreSQL
docker-compose exec postgres bash
```

### Viewing Container Files

```bash
# Check if files exist
docker-compose exec backend ls -la /app/src/

# View file contents
docker-compose exec backend cat /app/src/main.py

# Check environment setup
docker-compose exec backend env
```

### Testing Network Connectivity

```bash
# Ping between containers
docker-compose exec backend ping postgres

# Test TCP port connection
docker-compose exec backend nc -zv postgres 5432

# Test HTTP endpoint
docker-compose exec backend curl -v http://backend:8000/health

# Test with timeout
docker-compose exec backend timeout 5 curl http://postgres:5432
```

### Inspecting Logs

```bash
# Detailed backend logs
docker-compose logs backend -f --tail=100

# Search for errors
docker-compose logs | grep -i error

# Follow logs with timestamp
docker-compose logs -t -f backend

# Logs from specific time
docker-compose logs --since 2024-01-01 backend
```

---

## Advanced Debugging

### Database Query Inspection

```bash
# Connect to database
docker-compose exec postgres psql -U socrates -d socrates_db

# Useful commands
\d users              -- Describe users table
\dt                   -- List all tables
SELECT * FROM users;  -- Query data
\q                    -- Quit
```

### Redis CLI Access

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# Useful commands
PING                  -- Check connection
KEYS *               -- List all keys
GET key_name         -- Get value
FLUSHDB              -- Clear database (careful!)
QUIT                 -- Exit
```

### Process Inspection

```bash
# Check running processes in container
docker-compose exec backend ps aux

# Monitor process activity
docker-compose exec backend top

# Check open ports
docker-compose exec backend netstat -tuln
```

---

## Recovery Procedures

### Full Container Reset

```bash
# Stop and remove everything
docker-compose down

# Remove volumes (delete all data)
docker volume prune -a

# Remove unused images
docker image prune -a

# Start fresh
docker-compose up -d
```

### Database Recovery

```bash
# Backup current state
docker-compose exec postgres pg_dump -U socrates socrates_db > backup.sql

# Drop and recreate
docker-compose exec postgres psql -U socrates << EOF
DROP DATABASE IF EXISTS socrates_db;
CREATE DATABASE socrates_db;
EOF

# Restore from backup
docker-compose exec -T postgres psql -U socrates socrates_db < backup.sql
```

### Rebuild Specific Service

```bash
# Rebuild without cache
docker-compose build --no-cache backend

# Remove and recreate container
docker-compose rm -f backend
docker-compose up -d backend

# Force full restart
docker-compose stop backend
docker system prune -a
docker-compose up -d backend
```

---

## Performance Tuning

### Database Optimization

```bash
# Increase work_mem for queries
docker-compose exec postgres psql -U socrates -d socrates_db << EOF
ALTER SYSTEM SET work_mem = '256MB';
SELECT pg_reload_conf();
EOF

# Analyze query performance
docker-compose exec postgres psql -U socrates -d socrates_db << EOF
EXPLAIN ANALYZE SELECT * FROM sessions;
EOF
```

### Resource Limits

Edit `docker-compose.yml` to add limits:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## Checking System Requirements

```bash
# Docker version
docker --version

# Docker Compose version
docker-compose --version

# Available memory
free -h
docker stats --no-stream | head -5

# Disk space
df -h

# Network interfaces
docker network ls
```

---

## Getting Help

If you're still stuck:

1. **Check all logs:**
   ```bash
   docker-compose logs > full-logs.txt
   ```

2. **Verify configuration:**
   ```bash
   cat .env | sort
   docker-compose config
   ```

3. **Isolate the problem:**
   - Test backend separately: `curl http://localhost:8000/health`
   - Test frontend separately: `curl http://localhost:3000`
   - Test database separately: `docker-compose exec postgres psql -U socrates -d socrates_db -c "\dt"`

4. **Search GitHub Issues** for similar problems

5. **Review Docker best practices** in official documentation

---

## Document Info

- **Version:** 1.0
- **Last Updated:** October 17, 2025
- **Scope:** Socrates 8.0 Docker Deployment
- **Status:** Production-Ready
