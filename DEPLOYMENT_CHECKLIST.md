# Socrates 8.0 - Deployment Checklist

**Version:** 1.0
**Date:** October 17, 2025
**Status:** Production-Ready

## Pre-Deployment Checklist

### Code Quality & Testing (Required)

- [ ] **Unit Tests Passing**
  ```bash
  pytest tests/unit -v --cov=src
  # Expected: All tests pass, coverage > 80%
  ```

- [ ] **Integration Tests Passing**
  ```bash
  pytest tests/integration -v
  # Expected: All tests pass
  ```

- [ ] **API Smoke Tests**
  ```bash
  pytest tests/test_api_endpoints.py -v
  # Expected: All 15+ tests pass
  ```

- [ ] **No Python Errors**
  ```bash
  python -m py_compile src/main.py
  python -m py_compile src/api/routes/*.py
  python -m py_compile src/services/*.py
  # Expected: No errors
  ```

- [ ] **No TypeScript Errors**
  ```bash
  cd frontend && npm run type-check
  # Expected: No type errors
  ```

- [ ] **Linting Passes** (Optional)
  ```bash
  pylint src/
  eslint src/
  ```

### Security Review

- [ ] **No Hardcoded Secrets**
  - Search codebase for hardcoded passwords
  - Verify all secrets in `.env` files
  - Check no API keys in git history

- [ ] **Password Hashing Verified**
  ```bash
  grep -r "bcrypt\|hash_password" src/services/user_service.py
  # Expected: Password hashing implemented
  ```

- [ ] **JWT Tokens Configured**
  - Check JWT_SECRET_KEY is set in .env
  - Verify token expiration (24 hours)
  - Test token refresh flow

- [ ] **CORS Properly Configured**
  - Backend CORS_ORIGINS set to specific domains
  - Not set to "*" for production
  - Verified in main.py

- [ ] **Database Credentials Secure**
  - DB_PASSWORD is strong (12+ chars)
  - Not using default credentials in production
  - Database user has limited privileges

- [ ] **No SQL Injection Vulnerabilities**
  - All queries use parameterized statements
  - Review repository layer for SQL strings
  - Verify use of SQLAlchemy ORM

- [ ] **TLS/SSL Configured** (Production)
  - SSL certificates obtained
  - HTTPS endpoint configured
  - WSS (WebSocket Secure) enabled

### Database Preparation

- [ ] **Database Created**
  ```bash
  docker-compose exec postgres psql -U socrates -d socrates_db -c "\dt"
  # Expected: See all 7 tables
  ```

- [ ] **Schema Initialized**
  ```bash
  docker-compose exec postgres psql -U socrates -d socrates_db -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';"
  # Expected: 7 tables
  ```

- [ ] **All Indexes Created**
  ```bash
  docker-compose exec postgres psql -U socrates -d socrates_db -c "\di"
  # Expected: See all indexes
  ```

- [ ] **Foreign Keys Enabled**
  ```bash
  docker-compose exec postgres psql -U socrates -d socrates_db -c "SELECT constraint_name FROM information_schema.table_constraints WHERE constraint_type='FOREIGN KEY';"
  # Expected: All FK constraints visible
  ```

- [ ] **Backups Scheduled**
  - Backup script in place
  - Tested restore procedure
  - Backup storage configured

- [ ] **Migrations Ready**
  - Alembic migrations current
  - No pending migrations
  - Tested on staging

### Environment Configuration

- [ ] **.env File Configured**
  ```bash
  cat .env | grep -E "^[A-Z_]+=.+$"
  # Expected: All required variables set
  ```

- [ ] **Required Variables Set**
  - [ ] `DATABASE_URL` - PostgreSQL connection
  - [ ] `JWT_SECRET_KEY` - Secure secret (32+ chars)
  - [ ] `CLAUDE_API_KEY` - Valid API key
  - [ ] `ENVIRONMENT` - Set to "production"
  - [ ] `CORS_ORIGINS` - Specific domains only
  - [ ] `REACT_APP_API_URL` - Backend URL
  - [ ] `REACT_APP_WS_URL` - WebSocket URL

- [ ] **.env NOT in Git**
  ```bash
  git status | grep .env
  # Expected: No .env file tracked
  ```

- [ ] **.env.example Up to Date**
  - All variables documented
  - Default values appropriate
  - Committed to git

### Docker Images

- [ ] **Backend Image Builds**
  ```bash
  docker-compose build backend
  # Expected: Build succeeds
  ```

- [ ] **Frontend Image Builds**
  ```bash
  docker-compose build frontend
  # Expected: Build succeeds
  ```

- [ ] **PostgreSQL Image Available**
  ```bash
  docker pull postgres:15-alpine
  # Expected: Image pulls successfully
  ```

- [ ] **Redis Image Available** (Optional)
  ```bash
  docker pull redis:7-alpine
  # Expected: Image pulls successfully
  ```

- [ ] **Images Scanned for Vulnerabilities**
  ```bash
  docker scan socrates-backend:latest
  docker scan socrates-frontend:latest
  # Expected: No critical vulnerabilities
  ```

### Docker Compose Configuration

- [ ] **docker-compose.yml Valid**
  ```bash
  docker-compose config > /dev/null
  # Expected: No errors
  ```

- [ ] **All Services Defined**
  - [ ] postgres (database)
  - [ ] backend (FastAPI)
  - [ ] frontend (React)
  - [ ] redis (cache)

- [ ] **Network Configuration Correct**
  - Network name: socrates-network
  - All services on same network
  - Health checks configured

- [ ] **Volume Mounts Correct**
  - postgres_data volume configured
  - redis_data volume configured
  - No bind mounts for secrets

- [ ] **Environment Variables Passed**
  - All services receive required env vars
  - No hardcoded values in compose file

### Local Testing (Before Deployment)

- [ ] **Containers Start Successfully**
  ```bash
  docker-compose up -d
  docker-compose ps
  # Expected: All services healthy
  ```

- [ ] **Health Checks Pass**
  ```bash
  docker-compose ps | grep -E "postgres|backend|frontend|redis" | grep "healthy"
  # Expected: All show healthy
  ```

- [ ] **Backend API Responds**
  ```bash
  curl -s http://localhost:8000/health | jq .
  # Expected: {"success": true}
  ```

- [ ] **API Documentation Available**
  ```bash
  curl -s http://localhost:8000/docs
  # Expected: HTML response with OpenAPI docs
  ```

- [ ] **Frontend Loads**
  ```bash
  curl -s http://localhost:3000 | head -20
  # Expected: HTML starting with <!DOCTYPE
  ```

- [ ] **Database Connected**
  ```bash
  docker-compose exec postgres psql -U socrates -d socrates_db -c "SELECT 1;"
  # Expected: Output: 1
  ```

- [ ] **All API Endpoints Respond**
  ```bash
  # Test key endpoints
  curl -s http://localhost:8000/health
  curl -s http://localhost:8000/docs
  curl -s http://localhost:8000/openapi.json
  # Expected: All respond with 200
  ```

- [ ] **WebSocket Endpoint Available**
  ```bash
  curl -i http://localhost:8000/ws/sessions/test
  # Expected: 101 Switching Protocols (with token)
  ```

### Staging Deployment (If Applicable)

- [ ] **Deployed to Staging Environment**
  ```bash
  # Deploy to staging URL
  ENVIRONMENT=staging docker-compose --env-file .env.staging up -d
  ```

- [ ] **All Staging Tests Pass**
  - Frontend loads on staging URL
  - Backend API responds
  - Database queries work
  - WebSocket connections established

- [ ] **User Workflows Tested**
  - [ ] Register new user
  - [ ] Login with credentials
  - [ ] Create project
  - [ ] Create session
  - [ ] Send message and receive response
  - [ ] Receive typing indicators
  - [ ] Update preferences

- [ ] **Error Handling Tested**
  - [ ] Invalid credentials rejected
  - [ ] Duplicate email blocked
  - [ ] Invalid input rejected
  - [ ] Database connection failures handled
  - [ ] Missing required fields caught

### Performance Validation

- [ ] **API Response Times Acceptable**
  ```bash
  time curl -s http://localhost:8000/health > /dev/null
  # Expected: < 100ms
  ```

- [ ] **Database Queries Performant**
  ```bash
  docker-compose exec postgres psql -U socrates -d socrates_db << EOF
  EXPLAIN ANALYZE SELECT * FROM users LIMIT 10;
  EOF
  # Expected: Execute time < 10ms
  ```

- [ ] **Container Resource Usage Normal**
  ```bash
  docker stats --no-stream
  # Expected: Memory < 1GB for each service
  ```

- [ ] **Load Testing (Optional)**
  ```bash
  ab -n 100 -c 10 http://localhost:8000/health
  # Expected: All requests succeed
  ```

### Documentation Complete

- [ ] **DEPLOYMENT.md Created**
  - Setup instructions
  - Troubleshooting guide
  - Scaling guidelines

- [ ] **DOCKER_TROUBLESHOOTING.md Created**
  - Common issues documented
  - Solutions provided

- [ ] **API Documentation Available**
  ```bash
  curl -s http://localhost:8000/docs > api-docs.html
  ```

- [ ] **README.md Updated**
  - Project description
  - Quick start guide
  - Architecture overview
  - Contributing guidelines

- [ ] **Docker Compose Comments**
  - Services documented
  - Environment variables explained
  - Health checks documented

### Git Repository

- [ ] **All Code Committed**
  ```bash
  git status
  # Expected: nothing to commit, working tree clean
  ```

- [ ] **Git History Clean**
  ```bash
  git log --oneline | head -20
  # Expected: Meaningful commit messages
  ```

- [ ] **No Secrets in Git History**
  ```bash
  git log -p | grep -i password
  # Expected: No output (no passwords)
  ```

- [ ] **Latest Changes Pushed**
  ```bash
  git push origin main
  # Expected: Everything pushed
  ```

- [ ] **Deployment Tagged**
  ```bash
  git tag -a v1.0.0 -m "Production release"
  git push origin v1.0.0
  ```

---

## Staging Deployment Checklist

### Pre-Staging

- [ ] **Database Backup Created**
  ```bash
  docker-compose exec postgres pg_dump -U socrates socrates_db > backup-prod.sql
  ```

- [ ] **Current Environment Tested**
  - All health checks pass
  - All API endpoints respond
  - Database is responsive

### Staging Deployment Steps

```bash
# 1. Build latest images
docker-compose build --no-cache

# 2. Stop current containers
docker-compose down

# 3. Create staging environment
cp .env.example .env.staging
# Edit .env.staging with staging values

# 4. Deploy to staging
docker-compose --env-file .env.staging up -d

# 5. Wait for health checks
sleep 30
docker-compose ps

# 6. Verify all services healthy
docker-compose ps | grep healthy
```

### Staging Validation

- [ ] **All Containers Running**
  ```bash
  docker-compose ps
  # Expected: All containers "Up" with "healthy"
  ```

- [ ] **Database Migrated Successfully**
  ```bash
  docker-compose exec postgres psql -U socrates -d socrates_db -c "\dt"
  # Expected: All tables present
  ```

- [ ] **Smoke Tests Pass**
  ```bash
  bash test-docker.sh
  # Expected: All tests pass
  ```

- [ ] **API Key Working**
  ```bash
  docker-compose logs backend | grep -i claude
  # Expected: No API key errors
  ```

- [ ] **WebSocket Connections Work**
  - Test real-time message sending
  - Verify typing indicators
  - Check user presence

### Staging Approval

- [ ] **Stakeholder Approval**
  - Product owner signed off
  - QA team tested workflows
  - Security team reviewed

- [ ] **Final Sign-Off**
  - Ready for production
  - No blocking issues
  - All requirements met

---

## Production Deployment Checklist

### Pre-Production

- [ ] **Backup Created**
  ```bash
  docker-compose exec postgres pg_dump -U socrates socrates_db > backup-staging.sql
  ```

- [ ] **Rollback Plan Documented**
  - Backup restoration tested
  - Previous version tagged in git
  - Rollback procedure documented

### Production Deployment

```bash
# 1. Create production environment
cp .env.example .env.production
# Edit .env.production with production values

# 2. Build images with production tag
docker-compose build --no-cache
docker tag socrates-backend:latest socrates-backend:v1.0.0
docker tag socrates-frontend:latest socrates-frontend:v1.0.0

# 3. Stop current services
docker-compose down

# 4. Deploy to production
docker-compose --env-file .env.production up -d

# 5. Monitor startup
docker-compose logs -f --tail=20

# 6. Wait for health checks
sleep 45
docker-compose ps

# 7. Verify all services
bash test-docker.sh
```

### Post-Production Verification

- [ ] **All Services Running**
  ```bash
  docker-compose ps | grep healthy
  # Expected: 4 services healthy
  ```

- [ ] **Production URL Accessible**
  ```bash
  curl -s https://socrates.example.com/health
  # Expected: {"success": true}
  ```

- [ ] **API Endpoints Working**
  - Health check
  - Documentation
  - Authentication
  - Key endpoints

- [ ] **Database Connected**
  ```bash
  docker-compose exec postgres psql -U socrates -d socrates_db -c "SELECT COUNT(*) FROM users;"
  # Expected: User count
  ```

- [ ] **Monitoring Active**
  - Logs being collected
  - Alerts configured
  - Dashboards showing data

- [ ] **Production Smoke Tests**
  ```bash
  # Test critical workflows
  # 1. Register user
  # 2. Login
  # 3. Create project
  # 4. Create session
  # 5. Send message
  ```

### Post-Deployment

- [ ] **Notify Stakeholders**
  - Deployment complete
  - Features available
  - Support contact provided

- [ ] **Monitor for Issues**
  - Check logs for errors
  - Monitor API response times
  - Watch database connections

- [ ] **Document Deployment**
  - Deployment date/time
  - Version deployed
  - Issues encountered/resolved
  - Performance metrics

---

## Rollback Procedure (If Needed)

If production issues occur:

```bash
# 1. Stop current deployment
docker-compose down

# 2. Restore database from backup
docker-compose exec -T postgres psql -U socrates socrates_db < backup-prod.sql

# 3. Deploy previous version
git checkout <previous-version-tag>
docker-compose build --no-cache
docker-compose --env-file .env.production up -d

# 4. Verify rollback successful
docker-compose ps
bash test-docker.sh

# 5. Investigate issue
docker-compose logs > rollback-logs.txt
```

---

## Post-Deployment Monitoring

### Daily Tasks

- [ ] **Check Container Health**
  ```bash
  docker-compose ps
  docker stats --no-stream
  ```

- [ ] **Review Error Logs**
  ```bash
  docker-compose logs | grep -i error
  ```

- [ ] **Verify Backups Completed**
  - Previous day's backup exists
  - Backup file size reasonable
  - Test restoration procedure

### Weekly Tasks

- [ ] **Performance Review**
  - API response times
  - Database query times
  - Resource utilization

- [ ] **Security Review**
  - No unauthorized access attempts
  - All credentials rotated recently
  - No security warnings

- [ ] **Data Quality Check**
  - Database integrity verified
  - No orphaned records
  - Foreign key constraints holding

### Monthly Tasks

- [ ] **Full System Backup**
- [ ] **Disaster Recovery Test**
- [ ] **Security Audit**
- [ ] **Performance Analysis**
- [ ] **Dependency Updates Check**

---

## Document Information

- **Version:** 1.0
- **Date Created:** October 17, 2025
- **Status:** Production-Ready
- **Maintained By:** Development Team
- **Last Review:** October 17, 2025

**Use this checklist for every deployment to ensure consistency and reduce errors.**
