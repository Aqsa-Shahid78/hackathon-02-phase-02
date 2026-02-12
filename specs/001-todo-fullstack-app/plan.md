# Implementation Plan: Todo Full-Stack Web Application

**Branch**: `001-todo-fullstack-app` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-fullstack-app/spec.md`

## Summary

Build a multi-user todo web application with JWT-based authentication
(Better Auth), RESTful API (FastAPI + SQLModel), responsive frontend
(Next.js 16+ App Router), and Neon Serverless PostgreSQL storage. The
system supports 6 core operations: signup, signin, create/read/update/delete
tasks, and task completion toggling — all with strict per-user data isolation.

## Technical Context

**Language/Version**: Python 3.12+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Better Auth, Next.js 16+, Tailwind CSS 4+
**Storage**: Neon Serverless PostgreSQL (pooled connections)
**Testing**: pytest + pytest-asyncio (backend), Vitest (frontend)
**Target Platform**: Web (modern browsers: Chrome, Firefox, Safari, Edge — latest 2 versions)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: < 200ms p95 single-resource API, < 500ms p95 list API, < 2s page load
**Constraints**: < 200ms p95 API latency, JWT auth required on all task endpoints, mobile-first responsive
**Scale/Scope**: Up to 1000 tasks per user, multi-user with row-level data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| I. User-Centered Design | Visual feedback on all actions, inline validation, WCAG 2.1 AA | PASS — loading states, error messages, validation in spec |
| II. Security-First | Better Auth + JWT, bcrypt >= 12, data isolation, rate limiting, no hardcoded secrets | PASS — auth via Better Auth, per-user filtering, .env for secrets |
| III. Scalability | Connection pooling, UUID/bigint PKs, timestamps, pagination, reversible migrations | PASS — Neon pooler, UUID PKs, timestamptz columns, pagination-ready |
| IV. Mobile-First | 320px-first, 44px touch targets, Tailwind mobile-first | PASS — Next.js + Tailwind, mobile-first class ordering |
| V. High Performance | Async endpoints, Server Components default, loading.tsx, < 200ms p95 | PASS — FastAPI async, Next.js RSC, skeleton screens |

**Gate result: ALL PASS** — Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-fullstack-app/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── api.md           # REST API contracts
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry, CORS, middleware, exception handlers
│   ├── config.py            # Settings via pydantic-settings (DATABASE_URL, JWT_SECRET, etc.)
│   ├── database.py          # SQLModel async engine, session factory
│   ├── dependencies.py      # Shared deps (get_db, get_current_user, verify_ownership)
│   ├── models.py            # User + Task SQLModel models (single file)
│   ├── schemas.py           # All request/response Pydantic schemas (single file)
│   ├── security.py          # Password hashing (bcrypt), JWT encode/decode
│   ├── exceptions.py        # Custom exception hierarchy + global handlers
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # POST /auth/signup, POST /auth/signin, POST /auth/signout
│       └── tasks.py         # Task CRUD + completion toggle endpoints
├── migrations/              # Alembic migrations
│   ├── env.py
│   └── versions/
├── tests/
│   ├── conftest.py          # Fixtures (test DB, test client, auth helpers)
│   ├── test_auth.py         # Auth endpoint tests
│   └── test_tasks.py        # Task CRUD endpoint tests
├── alembic.ini
├── requirements.txt
└── .env.example

frontend/
├── app/
│   ├── layout.tsx           # Root layout (fonts, providers)
│   ├── page.tsx             # Landing / redirect to dashboard
│   ├── loading.tsx          # Root loading skeleton
│   ├── error.tsx            # Root error boundary
│   ├── not-found.tsx        # 404 page
│   ├── (auth)/
│   │   ├── layout.tsx       # Auth layout (centered card)
│   │   ├── login/
│   │   │   └── page.tsx     # Login form
│   │   └── signup/
│   │       └── page.tsx     # Signup form
│   └── (dashboard)/
│       ├── layout.tsx       # Dashboard layout (nav bar, protected)
│       ├── page.tsx         # Task list / dashboard
│       └── tasks/
│           └── [id]/
│               └── page.tsx # Task detail / edit view
├── components/
│   ├── ui/                  # Button, Input, Card, Dialog primitives
│   ├── forms/               # TaskForm, AuthForm
│   └── tasks/               # TaskList, TaskItem, TaskToggle
├── lib/
│   ├── api.ts               # Fetch wrapper with JWT injection
│   ├── auth.ts              # Auth helpers (getToken, isAuthenticated)
│   └── utils.ts             # cn() helper, formatDate
├── types/
│   └── index.ts             # Shared TypeScript interfaces
├── package.json
├── tailwind.config.ts
├── tsconfig.json
├── next.config.ts
└── .env.local.example
```

**Structure Decision**: Web application (Option 2) selected. Backend is a
Python FastAPI service with SQLModel ORM using a **flat module layout**
(single `models.py`, single `schemas.py`, `routes/` for endpoints). Frontend
is a Next.js 16+ App Router application. Both are separate projects in
`backend/` and `frontend/` directories at the repository root.

## Architecture Overview

### System Layers

```text
┌─────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ Auth     │  │ Dashboard│  │ Task Detail/Edit  │  │
│  │ Pages    │  │ Page     │  │ Page              │  │
│  └────┬─────┘  └────┬─────┘  └────────┬──────────┘  │
│       │              │                 │             │
│  ┌────▼──────────────▼─────────────────▼──────────┐  │
│  │           lib/api.ts (JWT-attached fetcher)    │  │
│  └────────────────────┬───────────────────────────┘  │
└───────────────────────┼─────────────────────────────┘
                        │ HTTP (JSON)
┌───────────────────────┼─────────────────────────────┐
│                    Backend (FastAPI)                 │
│  ┌────────────────────▼───────────────────────────┐  │
│  │          API Router (v1)                       │  │
│  │    /auth/signup  /auth/signin                  │  │
│  │    /users/{id}/tasks (CRUD + complete)         │  │
│  └────┬───────────────────────────────┬───────────┘  │
│       │                               │             │
│  ┌────▼─────────┐          ┌──────────▼──────────┐  │
│  │ Auth Service │          │   Task Service      │  │
│  │ (Better Auth)│          │   (CRUD + toggle)   │  │
│  └────┬─────────┘          └──────────┬──────────┘  │
│       │                               │             │
│  ┌────▼───────────────────────────────▼──────────┐  │
│  │          SQLModel / Database Layer            │  │
│  └────────────────────┬───────────────────────────┘  │
└───────────────────────┼─────────────────────────────┘
                        │ SQL (pooled)
┌───────────────────────┼─────────────────────────────┐
│           Neon Serverless PostgreSQL                 │
│           ┌───────────▼───────────┐                 │
│           │  users  │  tasks     │                 │
│           └─────────────────────┘                  │
└─────────────────────────────────────────────────────┘
```

### Authentication Flow

1. **Signup**: Frontend form → `POST /api/v1/auth/signup` → hash password →
   create user → return JWT tokens (access + refresh)
2. **Signin**: Frontend form → `POST /api/v1/auth/signin` → verify password →
   return JWT tokens
3. **Authenticated requests**: Frontend attaches JWT in `Authorization: Bearer <token>`
   header → FastAPI dependency `get_current_user` validates token → extracts user_id
4. **Data isolation**: Task service always filters by `user_id = current_user.id`
5. **Signout**: Frontend clears stored tokens, optionally calls signout endpoint

### Key Design Decisions

1. **Separate backend/frontend projects**: FastAPI backend and Next.js frontend
   are independent deployable units. Backend serves JSON API; frontend consumes it.
   This enables independent scaling and deployment.

2. **SQLModel for ORM**: Combines SQLAlchemy and Pydantic in a single model definition.
   Reduces boilerplate vs. separate SQLAlchemy models + Pydantic schemas. Still
   requires separate Create/Update/Response schemas for API boundaries.

3. **UUID primary keys**: Supports distributed patterns per constitution. Uses
   `uuid4` generated at the database level via `gen_random_uuid()`.

4. **JWT stored in httpOnly cookies**: Prevents XSS token theft. Frontend's
   `lib/api.ts` reads from cookies automatically via `credentials: 'include'`.
   Backend sets `Set-Cookie` headers on auth responses.

5. **User-scoped URL pattern**: `/api/v1/users/{user_id}/tasks` — the `user_id`
   in the path MUST match the authenticated user's JWT `sub` claim. This provides
   defense-in-depth alongside the service-layer filtering.

## Implementation Phases

### Phase 1: Setup (Foundation)

- Initialize `backend/` with FastAPI project structure, `requirements.txt`
- Initialize `frontend/` with Next.js 16+, Tailwind CSS 4+, TypeScript
- Configure Neon PostgreSQL connection via `DATABASE_URL` environment variable
- Set up SQLModel async engine with Neon pooled connection string
- Configure Alembic for database migrations
- Create `.env.example` files for both projects
- Set up CORS on FastAPI to allow frontend origin

### Phase 2: Database & Models

- Define `User` SQLModel (id: UUID, email, hashed_password, created_at, updated_at)
- Define `Task` SQLModel (id: UUID, title, description, is_completed, user_id FK, created_at, updated_at)
- Create initial Alembic migration
- Add indexes: `users.email` (unique), `tasks.user_id`, `tasks.created_at`
- Create database session dependency (`get_db`)

### Phase 3: Authentication (Backend)

- Implement password hashing with bcrypt (cost factor 12) in `security.py`
- Implement JWT token encode/decode in `security.py`
- Create `POST /api/v1/auth/signup` endpoint in `routes/auth.py` (validate input, hash password, create user, return JWT)
- Create `POST /api/v1/auth/signin` endpoint in `routes/auth.py` (validate credentials, return JWT)
- Create `get_current_user` dependency in `dependencies.py` (extract + validate JWT, return User)
- Implement rate limiting middleware for auth endpoints
- Create custom exceptions in `exceptions.py` (AuthenticationError, AuthorizationError, NotFoundError)

### Phase 4: Task CRUD (Backend)

- Create task schemas in `schemas.py` (TaskCreate, TaskUpdate, TaskResponse)
- Implement task CRUD logic directly in `routes/tasks.py` (create, list, get, update, delete, toggle_complete)
- Create `GET /api/v1/users/{user_id}/tasks` — list tasks (user-scoped, sorted by created_at DESC)
- Create `POST /api/v1/users/{user_id}/tasks` — create task
- Create `GET /api/v1/users/{user_id}/tasks/{task_id}` — get single task
- Create `PUT /api/v1/users/{user_id}/tasks/{task_id}` — update task
- Create `DELETE /api/v1/users/{user_id}/tasks/{task_id}` — delete task
- Create `PATCH /api/v1/users/{user_id}/tasks/{task_id}/complete` — toggle completion
- Enforce user_id path param matches authenticated user on all endpoints

### Phase 5: Frontend Authentication

- Build auth layout with centered card design (`app/(auth)/layout.tsx`)
- Build signup page with email/password form, validation, error handling
- Build login page with email/password form, validation, error handling
- Create `lib/api.ts` — fetch wrapper that attaches JWT and handles 401 redirects
- Create `lib/auth.ts` — auth state helpers, token storage
- Implement protected route middleware (redirect to login if unauthenticated)

### Phase 6: Frontend Task Management

- Build dashboard layout with navigation bar and sign-out button
- Build task list component with empty state
- Build create task form (title + optional description)
- Build task item with completion toggle (checkbox + strikethrough)
- Build task edit view (inline or separate page)
- Build delete confirmation dialog
- Implement loading skeletons for all data-fetching pages
- Implement error boundaries for all route segments
- Ensure mobile-first responsive design (320px → 1440px)

### Phase 7: Testing & Polish

- Backend: Test auth endpoints (signup, signin, invalid credentials, duplicate email)
- Backend: Test task CRUD endpoints (create, list, get, update, delete, toggle)
- Backend: Test data isolation (User A cannot access User B's tasks)
- Frontend: Test auth forms (validation, submission, error display)
- Frontend: Test task list (render, empty state, toggle, delete)
- Cross-cutting: Verify all error states show user-friendly messages
- Cross-cutting: Verify responsive layout at 320px, 768px, 1024px, 1440px

## Testing Strategy

### Backend Testing (pytest + pytest-asyncio)

| Area | Test Type | Key Scenarios |
|------|-----------|---------------|
| Auth | Integration | Signup success, duplicate email (409), signin success, wrong password (401) |
| Tasks CRUD | Integration | Create (201), list (200 + user-scoped), get (200), update (200), delete (204) |
| Data Isolation | Integration | User A cannot GET/PUT/DELETE User B's tasks (403) |
| Validation | Unit | Empty title rejected (422), email format validated, password min length |
| Security | Integration | No token → 401, expired token → 401, invalid token → 401 |

### Frontend Testing (Vitest)

| Area | Test Type | Key Scenarios |
|------|-----------|---------------|
| Auth Forms | Component | Validation errors, successful submission, error display |
| Task List | Component | Renders tasks, empty state, toggle completion |
| API Client | Unit | JWT attachment, 401 redirect handling |

## Complexity Tracking

> No Constitution Check violations. No complexity justification needed.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |
