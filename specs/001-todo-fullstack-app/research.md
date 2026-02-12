# Research: Todo Full-Stack Web Application

**Branch**: `001-todo-fullstack-app` | **Date**: 2026-02-09

## Technology Decisions

### 1. Backend Framework: FastAPI

- **Decision**: FastAPI (Python)
- **Rationale**: Required by constitution. Async-native, built-in OpenAPI docs,
  Pydantic validation, excellent performance for Python web frameworks.
- **Alternatives considered**: Django REST Framework (heavier, sync-first),
  Flask (less structured, no built-in validation).

### 2. ORM: SQLModel

- **Decision**: SQLModel
- **Rationale**: Required by constitution. Combines SQLAlchemy + Pydantic,
  reducing boilerplate. Single model definition for both DB and validation.
- **Alternatives considered**: SQLAlchemy alone (more boilerplate, separate
  Pydantic schemas needed), Tortoise ORM (less mature ecosystem).

### 3. Frontend Framework: Next.js 16+ (App Router)

- **Decision**: Next.js 16+ with App Router
- **Rationale**: Required by constitution. Server Components for performance,
  file-based routing, built-in image optimization, streaming/Suspense support.
- **Alternatives considered**: React SPA (no SSR benefits), Remix (smaller
  ecosystem), Vue/Nuxt (different ecosystem).

### 4. Database: Neon Serverless PostgreSQL

- **Decision**: Neon Serverless PostgreSQL
- **Rationale**: Required by constitution. Serverless scaling, built-in connection
  pooling, instant branching for dev/staging, PostgreSQL compatibility.
- **Alternatives considered**: Supabase (also PostgreSQL but different management
  model), PlanetScale (MySQL-based).

### 5. Authentication: Better Auth with JWT

- **Decision**: Better Auth library with JWT token issuance
- **Rationale**: Required by constitution. Modern auth library with built-in JWT
  support, session management, and secure defaults.
- **Alternatives considered**: NextAuth.js (frontend-only), Passport.js (Node.js
  only), custom JWT implementation (more security risk).

### 6. Primary Key Strategy: UUID v4

- **Decision**: UUID v4 generated at database level (`gen_random_uuid()`)
- **Rationale**: Constitution requires UUID or bigint for distributed patterns.
  UUID prevents enumeration attacks and supports future horizontal scaling.
- **Alternatives considered**: Auto-incrementing bigint (simpler but exposes
  creation order, less suitable for distributed systems).

### 7. Password Hashing: bcrypt (cost factor 12)

- **Decision**: bcrypt with cost factor 12
- **Rationale**: Constitution mandates bcrypt >= 12 or argon2id. bcrypt is
  widely supported via `passlib` library, ~250ms per hash at cost 12.
- **Alternatives considered**: argon2id (stronger but requires more config
  tuning for memory/time parameters).

### 8. Token Storage: httpOnly Cookies

- **Decision**: JWT tokens stored in httpOnly, secure, sameSite cookies
- **Rationale**: Prevents XSS token theft (JavaScript cannot access httpOnly
  cookies). Auth agent security principles mandate this approach.
- **Alternatives considered**: localStorage (vulnerable to XSS), sessionStorage
  (lost on tab close, also XSS-vulnerable).

### 9. Styling: Tailwind CSS 4+

- **Decision**: Tailwind CSS 4+ with mobile-first approach
- **Rationale**: Required by constitution. Utility-first, no context switching,
  excellent responsive design support with breakpoint prefixes.
- **Alternatives considered**: CSS Modules (more boilerplate), styled-components
  (runtime overhead), vanilla CSS (less maintainable at scale).

### 10. Database Migrations: Alembic

- **Decision**: Alembic for SQLModel/SQLAlchemy migrations
- **Rationale**: Standard migration tool for SQLAlchemy ecosystem. Supports
  auto-generation from model changes, reversible migrations with up/down.
- **Alternatives considered**: Manual SQL scripts (error-prone, no auto-detect),
  custom migration scripts (reinventing the wheel).

## Integration Patterns

### Frontend ↔ Backend Communication

- Frontend uses `fetch()` wrapper (`lib/api.ts`) with `credentials: 'include'`
  for cookie-based JWT transmission.
- Backend sets JWT in `Set-Cookie` header with `httpOnly`, `secure`, `sameSite=lax`.
- All API responses use consistent JSON envelope format.
- 401 responses trigger automatic redirect to login page.

### Backend ↔ Database Communication

- SQLModel async engine with Neon pooled connection string.
- Connection string from `DATABASE_URL` environment variable (pooled endpoint).
- Session dependency (`get_db`) yields async session per request.
- Alembic uses direct (non-pooled) connection for migrations.

## Open Questions Resolved

All technical questions resolved. No NEEDS CLARIFICATION items remain.
