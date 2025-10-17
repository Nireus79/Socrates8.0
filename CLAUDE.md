# CLAUDE.md - AI Development Guide for Socrates 8.0

**Version:** 8.0.0
**Created:** October 17, 2025
**Status:** Ready for Implementation
**Estimated Duration:** 24-35 hours of focused development

---

## OVERVIEW

This document guides Claude (AI Assistant) through implementing Socrates 8.0, a complete rebuild of the previous Flask-based system. The project is a modern, production-ready Socratic questioning platform using FastAPI + React + PostgreSQL.

**Key principle:** No greedy patterns. Implement everything completely, not "will do later."

---

## BEFORE YOU START

Claude must read these documents IN ORDER before starting ANY implementation:

1. ✅ `Plan/README_8_0_INDEX.md` - Complete project overview
2. ✅ `Plan/SOCRATES_8_0_QUICK_START.md` - Setup and architecture
3. ✅ `Plan/DATABASE_SCHEMA_REFERENCE.md` - Database design
4. ✅ `Plan/API_ENDPOINTS_REFERENCE.md` - All API endpoints
5. ✅ `Plan/SERVICE_LAYER_PATTERNS.md` - Business logic patterns
6. ✅ `Plan/SOCRATES_8_0_BUILD_TODO.md` - Implementation checklist

**Do not skip these.** Understanding the architecture is critical.

---

## PROJECT STRUCTURE TO CREATE

```
Socrates-8.0/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── middleware/
│   │   ├── utils/
│   │   ├── auth/
│   │   ├── main.py
│   │   ├── config.py
│   │   └── dependencies.py
│   ├── migrations/
│   │   └── versions/
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── requirements.txt
│   ├── .env
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── store/
│   │   │   └── slices/
│   │   ├── services/
│   │   ├── types/
│   │   ├── assets/
│   │   │   └── styles/
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   └── .env
│
├── docs/
│   └── API_DOCUMENTATION.md
│
├── docker-compose.yml
├── CLAUDE.md (this file)
└── Plan/
    ├── README_8_0_INDEX.md
    ├── SOCRATES_8_0_QUICK_START.md
    ├── DATABASE_SCHEMA_REFERENCE.md
    ├── API_ENDPOINTS_REFERENCE.md
    ├── SERVICE_LAYER_PATTERNS.md
    └── SOCRATES_8_0_BUILD_TODO.md
```

---

## 10 IMPLEMENTATION PHASES

### Phase 1: Project Setup (2-3 hours)
- Create complete folder structure
- Set up backend (FastAPI, dependencies, virtual environment)
- Set up frontend (React, TypeScript, Tailwind)
- Initialize PostgreSQL database
- Set up Alembic for migrations
- Create .env configuration files

**Completion Criteria:**
- [ ] All folders exist
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Database created
- [ ] Alembic initialized

### Phase 2: Database Layer (2-3 hours)
- Create 7 SQLAlchemy models (User, Project, Session, Message, UserPreference, Document, AuditLog)
- Set up proper relationships and constraints
- Create initial Alembic migration
- Test database schema with psql
- Seed test data

**Reference:** DATABASE_SCHEMA_REFERENCE.md

**Completion Criteria:**
- [ ] All 7 models created
- [ ] Migration runs successfully
- [ ] All tables created in PostgreSQL
- [ ] Foreign keys working
- [ ] Test data seeded

### Phase 3: Repository Layer (2-3 hours)
- Create BaseRepository with CRUD operations
- Implement 7 repository classes (one for each model)
- Add filtering, pagination, sorting
- Write comprehensive repository tests
- Test all CRUD operations

**Reference:** SERVICE_LAYER_PATTERNS.md (Repository section)

**Completion Criteria:**
- [ ] All repositories implemented
- [ ] CRUD tests passing
- [ ] Filtering working
- [ ] Pagination working
- [ ] 80%+ code coverage for repos

### Phase 4: Service Layer (3-4 hours)
- Create BaseService with common patterns
- Implement 7 service classes (UserService, ProjectService, SessionService, MessageService, PreferenceService, DocumentService, AuditLogService)
- Add business logic (validation, authorization, error handling)
- Write comprehensive service tests
- Test all business logic workflows

**Reference:** SERVICE_LAYER_PATTERNS.md (Service section)

**Completion Criteria:**
- [ ] All services implemented
- [ ] Business logic tests passing
- [ ] Validation working
- [ ] Error handling complete
- [ ] 80%+ code coverage for services

### Phase 5: Authentication Layer (2-3 hours)
- Implement JWT token creation/verification
- Create password hashing utilities (bcrypt)
- Implement get_current_user() dependency
- Set up CORS middleware
- Write authentication tests

**Reference:** API_ENDPOINTS_REFERENCE.md (Auth endpoints)

**Completion Criteria:**
- [ ] JWT tokens working
- [ ] Token expiration working
- [ ] Password hashing working
- [ ] CORS configured
- [ ] Auth tests passing

### Phase 6: API Layer (3-4 hours)
- Create Pydantic schemas for all endpoints
- Implement all 20+ route handlers
- Add proper request/response validation
- Implement error response formats
- Write endpoint tests
- Test all endpoints with sample data

**Reference:** API_ENDPOINTS_REFERENCE.md (All endpoints)

**Completion Criteria:**
- [ ] All routes implemented
- [ ] Request validation working
- [ ] Response formats correct
- [ ] Error handling consistent
- [ ] All endpoints tested

### Phase 7: Frontend (4-5 hours)
- Set up Tailwind CSS
- Create Redux store (auth, projects, sessions, messages slices)
- Implement API client service
- Create 7+ pages (Login, Register, Dashboard, Projects, Session, Profile, Settings)
- Create 5+ components (ProjectCard, SessionCard, MessageList, etc.)
- Connect all frontend forms to backend APIs

**Completion Criteria:**
- [ ] Redux store working
- [ ] All pages created
- [ ] All components created
- [ ] API calls working
- [ ] Frontend can login to backend

### Phase 8: Real-time Features (2-3 hours)
- Set up WebSocket/Socket.io
- Implement real-time message updates
- Implement typing indicators
- Implement user presence
- Test WebSocket connections

**Completion Criteria:**
- [ ] WebSocket connection working
- [ ] Real-time messages flowing
- [ ] Typing indicators working
- [ ] Presence updates working

### Phase 9: Testing (2-3 hours)
- Write comprehensive unit tests (80%+ coverage target)
- Write integration tests
- Write E2E tests for complete workflows
- Run full test suite
- Verify coverage metrics

**Completion Criteria:**
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] All E2E tests passing
- [ ] Coverage > 80%

### Phase 10: Deployment (1-2 hours)
- Create Docker files (backend + frontend)
- Create docker-compose.yml
- Deploy to staging environment
- Test all endpoints on staging
- Document deployment process

**Completion Criteria:**
- [ ] Docker images building
- [ ] docker-compose.yml working
- [ ] Staging deployment successful
- [ ] All endpoints tested on staging

---

## CORE PATTERNS & PRINCIPLES

### 1. No Greedy Patterns
- ✅ Implement EVERYTHING the first time
- ✅ Add proper error handling
- ✅ Add validation everywhere
- ✅ Write tests as you go
- ❌ No "will implement later"
- ❌ No stubbed/fake responses
- ❌ No silent failures

### 2. Clean Architecture
```
Frontend (React)
    ↓ HTTP/WebSocket
API Layer (FastAPI Routes)
    ↓ Dependency Injection
Service Layer (Business Logic)
    ↓ Data Access
Repository Layer (Database Access)
    ↓ SQL Queries
Database (PostgreSQL)
```

### 3. Type Safety
- Backend: Use Pydantic for ALL schemas
- Frontend: Use TypeScript for ALL components
- No `any` or `unknown` types

### 4. Testing First
- Write tests as you implement
- Test each layer independently
- 80%+ code coverage minimum
- All tests must pass before moving to next phase

### 5. Database-First Design
- Database schema drives the entire system
- All migrations automated with Alembic
- Relationships enforced at database level
- Constraints defined in schema

### 6. Error Handling
- All errors return consistent JSON format
- All errors logged with context
- All error codes documented
- All error messages helpful

---

## KEY TECHNOLOGIES

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | FastAPI | 0.104+ |
| ORM | SQLAlchemy | 2.0+ |
| Database | PostgreSQL | 14+ |
| Migrations | Alembic | 1.12+ |
| Validation | Pydantic | 2.0+ |
| Auth | Python-Jose + passlib | Latest |
| Frontend | React | 18+ |
| Frontend Types | TypeScript | 5+ |
| State Mgmt | Redux Toolkit | Latest |
| Real-time | socket.io | Latest |
| Testing | pytest | 7.4+ |
| UI Framework | Tailwind CSS | 3+ |

---

## QUALITY CHECKLIST

Before declaring any phase complete, verify:

- [ ] All code written follows the patterns documented
- [ ] All error cases handled
- [ ] All inputs validated
- [ ] No hardcoded values (use config)
- [ ] No fake/stub responses
- [ ] All data persists to database
- [ ] All tests passing (100%)
- [ ] Code follows Python/TypeScript conventions
- [ ] All endpoints documented
- [ ] Security review passed
- [ ] Performance acceptable
- [ ] Logging working everywhere
- [ ] CORS properly configured
- [ ] Database migrations working

---

## DAILY WORKFLOW FOR CLAUDE

When working on this project:

### Start of Session
1. Review which phase you're on
2. Read the relevant section of SOCRATES_8_0_BUILD_TODO.md
3. Understand all requirements for that phase
4. Create/update TodoWrite items for that phase

### During Development
1. Work on ONE item at a time
2. Mark item as in_progress in TodoWrite
3. Implement completely (no greedy patterns)
4. Write tests for the feature
5. Verify tests pass
6. Mark item as completed

### End of Session
1. Run full test suite
2. Verify no console errors
3. Create git commit
4. Update TodoWrite with progress
5. Document any blockers

---

## GIT WORKFLOW

Commit after completing each major section:

```bash
# Phase 1: Setup
git commit -m "feat: Initial project setup with folder structure"

# Phase 2: Database
git commit -m "feat: Add SQLAlchemy models and migrations"

# Phase 3: Repositories
git commit -m "feat: Implement repository layer with CRUD"

# Phase 4: Services
git commit -m "feat: Implement service layer with business logic"

# Phase 5: Auth
git commit -m "feat: Add JWT authentication"

# Phase 6: API
git commit -m "feat: Implement FastAPI routes and endpoints"

# Phase 7: Frontend
git commit -m "feat: Create React UI with all pages"

# Phase 8: Real-time
git commit -m "feat: Add WebSocket support for real-time messaging"

# Phase 9: Testing
git commit -m "feat: Add comprehensive test suite"

# Phase 10: Deploy
git commit -m "feat: Add Docker and deployment configuration"
```

---

## COMMON PATTERNS

### Backend: Service Layer Example
```python
class UserService(BaseService):
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, email: str, password: str, name: str):
        # Validate input
        if await self.user_repo.get_by_email(email):
            raise ValueError("Email already exists")

        # Hash password
        hashed_password = hash_password(password)

        # Create user
        user = User(email=email, password=hashed_password, name=name)
        return await self.user_repo.create(user)
```

### Frontend: Redux Slice Example
```typescript
const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    token: null,
    loading: false,
    error: null,
  },
  reducers: {
    // Actions here
  },
});
```

### API Route Example
```python
@router.post("/register")
async def register(
    request: RegisterRequest,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.register_user(
        email=request.email,
        password=request.password,
        name=request.name
    )
    return UserResponse.model_validate(user)
```

---

## IMPORTANT RULES

1. **Read all documentation first** - Do not start coding before reading all Plan/*.md files
2. **No skipping phases** - Each phase depends on previous ones
3. **Test after each phase** - Run pytest to verify
4. **Commit frequently** - One commit per major feature
5. **No greedy patterns** - Complete everything the first time
6. **Type safety** - All backend schemas are Pydantic, all frontend is TypeScript
7. **Error handling** - Every function handles errors appropriately
8. **Database transactions** - Use transactions for multi-step operations
9. **Security** - No hardcoded secrets, passwords hashed, SQL injection prevention
10. **Documentation** - Document all new functions with docstrings

---

## SUCCESS CRITERIA

Project is COMPLETE when:

- [x] All 10 phases implemented
- [x] All endpoints responding correctly
- [x] All tests passing (100%)
- [x] No console errors
- [x] Database properly normalized
- [x] Authentication working
- [x] Messaging working end-to-end
- [x] Settings persist across restarts
- [x] UI is responsive
- [x] Code well-documented
- [x] Deployed to staging
- [x] Ready for production

---

## REFERENCES

Quick links to key sections:

- **Database Design:** `Plan/DATABASE_SCHEMA_REFERENCE.md`
- **API Endpoints:** `Plan/API_ENDPOINTS_REFERENCE.md`
- **Service Patterns:** `Plan/SERVICE_LAYER_PATTERNS.md`
- **Build Checklist:** `Plan/SOCRATES_8_0_BUILD_TODO.md`
- **Quick Start:** `Plan/SOCRATES_8_0_QUICK_START.md`
- **Full Index:** `Plan/README_8_0_INDEX.md`

---

## NEXT STEPS FOR CLAUDE

1. ✅ You've read this file (CLAUDE.md)
2. → Now read `Plan/README_8_0_INDEX.md` (complete overview)
3. → Then read `Plan/SOCRATES_8_0_QUICK_START.md` (setup details)
4. → Then read `Plan/DATABASE_SCHEMA_REFERENCE.md` (data model)
5. → Then read `Plan/API_ENDPOINTS_REFERENCE.md` (all endpoints)
6. → Then read `Plan/SERVICE_LAYER_PATTERNS.md` (business logic)
7. → Finally, start `Plan/SOCRATES_8_0_BUILD_TODO.md` (begin Phase 1)

**Total reading time: ~4-5 hours**
**Total implementation time: ~24-35 hours**
**Expected completion: 6-7 days full-time, 2-3 weeks part-time**

---

## DOCUMENT METADATA

- **Version:** 8.0.0
- **Created:** October 17, 2025
- **Technology:** FastAPI + React + PostgreSQL
- **Architecture:** Clean Architecture with proper separation of concerns
- **Status:** Ready for Implementation
- **Timeline:** 24-35 hours of focused development
- **Quality Standard:** Production-Ready, 80%+ test coverage
- **No Greedy Patterns:** Everything implemented completely

**Let's build something great!**
