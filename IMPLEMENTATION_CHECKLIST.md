# SOCRATES 8.0 - IMPLEMENTATION CHECKLIST

**Quick Reference - All Details in Plan Directory**

---

## CRITICAL REMINDERS

✅ **Read Plan documents in order BEFORE any coding:**
1. README_8_0_INDEX.md
2. SOCRATES_8_0_QUICK_START.md
3. DATABASE_SCHEMA_REFERENCE.md
4. API_ENDPOINTS_REFERENCE.md
5. SERVICE_LAYER_PATTERNS.md
6. SOCRATES_8_0_BUILD_TODO.md

✅ **NO GREEDY PATTERNS** - Implement everything completely, not "will do later"

✅ **NO ASSUMPTIONS** - Only code based on facts from Plan documents

✅ **OLD REPO IS REFERENCE ONLY** - Do NOT copy code from old Socrates project

---

## FACTS FROM PLAN DOCUMENTS

### Database (PostgreSQL)
- **7 Tables:** users, projects, sessions, messages, user_preferences, documents, audit_log
- **All with:** UUIDs (primary keys), timestamps, proper indexes, foreign key constraints
- **Migration Tool:** Alembic (auto-generate from SQLAlchemy models)
- **No raw SQL** - SQLAlchemy ORM only

### API Endpoints (20+ total)
- **Standard Response Format:** `{success, data, message}` or `{success, error, message}`
- **Authentication:** JWT tokens, Bearer scheme
- **All endpoints documented** in API_ENDPOINTS_REFERENCE.md with request/response examples

### Services (Business Logic Layer)
- **Base Pattern:** BaseService with db session, commit/rollback, error handling
- **7 Services:** UserService, ProjectService, SessionService, MessageService, PreferenceService, DocumentService (+ audit)
- **All services:** Use repositories, validate input, handle errors, log operations
- **No business logic in routes** - Routes are thin, Services are thick

### Architecture Layers
```
FastAPI Routes (thin HTTP layer)
    ↓
Service Layer (thick business logic)
    ↓
Repository Layer (data access)
    ↓
SQLAlchemy ORM Models
    ↓
PostgreSQL Database
```

---

## TECHNOLOGY STACK (FROM PLAN)

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | FastAPI | 0.104+ |
| ORM | SQLAlchemy | 2.0+ |
| Database | PostgreSQL | 14+ |
| Migrations | Alembic | 1.12+ |
| Validation | Pydantic | 2.0+ |
| Auth | python-jose + passlib (bcrypt) | Latest |
| Frontend | React | 18+ |
| Frontend Types | TypeScript | 5+ |
| State Mgmt | Redux Toolkit | Latest |
| Real-time | socket.io | Latest |
| UI | Tailwind CSS | 3+ |
| Testing | pytest | 7.4+ |

---

## PHASE BREAKDOWN

| Phase | Focus | Hours | Key Deliverable |
|-------|-------|-------|-----------------|
| 1 | Setup | 2-3 | Project structure, dependencies, DB |
| 2 | Database | 2-3 | 7 SQLAlchemy models, Alembic migration |
| 3 | Repository | 2-3 | 7 repository classes, CRUD operations |
| 4 | Services | 3-4 | 7 service classes, all business logic |
| 5 | Auth | 2-3 | JWT tokens, password hashing (bcrypt) |
| 6 | API | 3-4 | 20+ endpoints, Pydantic schemas |
| 7 | Frontend | 4-5 | React UI, Redux store, API calls |
| 8 | Real-time | 2-3 | WebSocket/socket.io messaging |
| 9 | Testing | 2-3 | Unit + Integration tests, 80%+ coverage |
| 10 | Deploy | 1-2 | Docker, docker-compose, staging test |

**Total: 24-35 hours focused development**

---

## QUALITY CHECKLIST (Before marking any phase COMPLETE)

- [ ] All error cases handled (no silent failures)
- [ ] All inputs validated (no garbage data)
- [ ] All data persists to PostgreSQL (not in-memory)
- [ ] All tests passing (100%, not 90%)
- [ ] No hardcoded values (use config/env)
- [ ] No fake/stub responses (real AI, real database)
- [ ] All code follows layer patterns exactly
- [ ] Security: passwords hashed (bcrypt), JWT tokens valid, SQL injection prevented
- [ ] Type safety: Pydantic schemas on backend, TypeScript on frontend
- [ ] Logging: All operations logged with context
- [ ] Documentation: All functions have docstrings

---

## NO GREEDY PATTERNS - EXAMPLES

❌ **WRONG:**
```python
def create_project(name):
    # TODO: Add validation later
    project = Project(name=name)
    # TODO: Add error handling
    return project
```

✅ **CORRECT:**
```python
def create_project(self, owner_id: UUID, name: str, description: str = None) -> Project:
    """Create new project with validation"""
    # Validate input
    if not name or len(name.strip()) == 0:
        raise ValueError("Project name is required")
    if len(name) > 255:
        raise ValueError("Project name too long")

    # Create and persist
    project = Project(
        owner_id=owner_id,
        name=name,
        description=description,
        status='PLANNING'
    )
    self.db.add(project)
    self.commit()
    return project
```

---

## GIT WORKFLOW

```bash
# After completing each phase, commit:
git add .
git commit -m "feat: Phase X - [specific work]"
git log --oneline  # Verify commit
```

**Example commits:**
- Phase 1: `feat: Initial project setup with folder structure`
- Phase 2: `feat: Add SQLAlchemy models and Alembic migrations`
- Phase 3: `feat: Implement repository layer with CRUD operations`
- etc.

---

## TESTING REQUIREMENT

- **Minimum:** 80% code coverage
- **Framework:** pytest
- **Types:** Unit tests, Integration tests, E2E tests
- **Must pass:** All tests before each phase is complete
- **Command:** `pytest tests/ -v --cov=src`

---

## FACTS TO IMPLEMENT

### Users/Auth
- ✅ Username + Email unique
- ✅ Password hashing with bcrypt
- ✅ JWT tokens (no session tokens, stateless)
- ✅ Token expiration (24 hours default)
- ✅ User can update profile, change password

### Projects
- ✅ Owner has full access, can delete (cascading)
- ✅ Status: PLANNING → DESIGN → DEVELOPMENT → TESTING → COMPLETE
- ✅ Technology stack stored as JSONB array
- ✅ Timestamps: created_at, updated_at

### Sessions
- ✅ Four modes: chat, question, teaching, review
- ✅ Status: ACTIVE, ARCHIVED, PAUSED
- ✅ Can toggle mode, archive session
- ✅ Messages cascade delete when session deleted

### Messages
- ✅ User messages AND assistant responses (not just user)
- ✅ Real Claude API responses (not fake)
- ✅ Stored in PostgreSQL with full history
- ✅ Pagination support on retrieval

### Settings/Preferences
- ✅ Per-user settings (theme, LLM model, temperature, etc.)
- ✅ Auto-created for new users
- ✅ Persist across restarts

### Error Handling
- ✅ All errors return JSON: `{success: false, error: "code", message: "..."}`
- ✅ Consistent HTTP status codes
- ✅ No 500 errors for validation (use 400, 401, 403, 404)
- ✅ All errors logged

---

## WHAT NOT TO DO

❌ Copy code from old Socrates repository (it has security flaws)
❌ Skip validation (implement complete checks)
❌ Use fake/stub AI responses (integrate real Claude API)
❌ Store passwords without hashing (use bcrypt)
❌ Implement authentication without JWT tokens
❌ Put business logic in routes (use services)
❌ Use raw SQL (use SQLAlchemy ORM only)
❌ Skip tests (write as you build)
❌ Hardcode configuration values
❌ Leave error cases unhandled

---

## HELPFUL REFERENCES

| Document | Contains |
|----------|----------|
| DATABASE_SCHEMA_REFERENCE.md | All 7 tables, SQLAlchemy models, migrations |
| API_ENDPOINTS_REFERENCE.md | All 20+ endpoints with request/response examples |
| SERVICE_LAYER_PATTERNS.md | Base service, 5+ service implementations |
| SOCRATES_8_0_BUILD_TODO.md | Detailed checklist for all 10 phases |
| SOCRATES_8_0_QUICK_START.md | Quick setup guide, technology stack |
| README_8_0_INDEX.md | Complete project overview, architecture |

---

## GETTING STARTED NOW

1. **You are here:** Read this checklist
2. **Next:** Read SOCRATES_8_0_BUILD_TODO.md Phase 1 section
3. **Then:** Create project folder structure
4. **Then:** Set up backend dependencies
5. **Then:** Set up frontend
6. **Then:** Create database
7. **Finally:** Start Phase 2 (database models)

---

**Remember:** All answers are in the Plan documents. If uncertain, re-read the relevant section.

**No assumptions. Only facts.**

**Complete implementations. No greedy patterns.**

**Tests as you go. 80%+ coverage minimum.**

---

**Version:** 8.0.0
**Created:** October 17, 2025
**Status:** Ready to implement
