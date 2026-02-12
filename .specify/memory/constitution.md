<!--
  Sync Impact Report
  ===================
  Version change: 0.0.0 (template) → 1.0.0 (initial ratification)
  Modified principles: N/A (all new — template placeholders replaced)
  Added sections:
    - Core Principles (5 principles: User-Centered Design, Security-First,
      Scalability, Mobile-First Responsiveness, High Performance)
    - Technology Stack & Constraints
    - Development Workflow & Quality Gates
    - Governance
  Removed sections: None (template placeholders replaced)
  Templates requiring updates:
    - .specify/templates/plan-template.md        ✅ compatible (Constitution Check generic)
    - .specify/templates/spec-template.md         ✅ compatible (no constitution-specific refs)
    - .specify/templates/tasks-template.md        ✅ compatible (web app path convention matches)
  Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### I. User-Centered Design

All features MUST prioritize intuitive user experience. Every UI element
MUST be self-explanatory and require minimal learning curve.

- Every user-facing feature MUST include clear visual feedback for actions
  (loading states, success confirmations, error messages).
- Navigation MUST be consistent and predictable across all pages.
- Form interactions MUST provide inline validation with helpful error messages.
- The todo management workflow (create, read, update, delete, complete)
  MUST be achievable in the fewest possible clicks.
- Accessibility standards (WCAG 2.1 AA) MUST be met for all interactive elements.

### II. Security-First

All user data MUST be securely handled and isolated. Authentication and
authorization MUST use industry-standard practices.

- Authentication MUST be implemented via Better Auth with JWT token issuance.
- Passwords MUST be hashed with bcrypt (cost factor >= 12) or argon2id; plaintext
  storage is strictly forbidden.
- All API endpoints serving user data MUST require valid authentication tokens.
- User data MUST be isolated: users MUST NOT access, modify, or view other
  users' todos under any circumstance.
- Secrets, tokens, and credentials MUST NOT be hardcoded; all MUST be stored
  in environment variables (`.env`) and documented.
- All authentication endpoints MUST implement rate limiting to prevent brute-force
  attacks.
- Error responses MUST NOT leak internal system details, stack traces, or
  database structure.

### III. Scalability

The system MUST leverage Neon Serverless PostgreSQL and be architected for
horizontal scaling without code changes.

- Database access MUST use connection pooling (Neon built-in pooler) for all
  application connections.
- Database schema MUST use UUIDs or bigint for primary keys to support
  distributed patterns.
- All database tables MUST include `created_at` and `updated_at` timestamp
  columns with timezone support (`timestamptz`).
- API endpoints MUST support pagination for list operations to prevent
  unbounded result sets.
- Database queries MUST be optimized with appropriate indexes on frequently
  queried columns (user_id, status, created_at).
- Migrations MUST be reversible with explicit up/down scripts.

### IV. Mobile-First Responsiveness

The frontend MUST be designed mobile-first and deliver a seamless experience
across all device sizes.

- All UI components MUST be designed for 320px viewport first, then enhanced
  for larger breakpoints (sm: 640px, md: 768px, lg: 1024px, xl: 1280px).
- Touch targets MUST be at least 44x44px on mobile viewports.
- The todo list interface MUST be fully functional on mobile without
  horizontal scrolling.
- Layout MUST use CSS Grid and Flexbox; no floats or absolute positioning
  for layout purposes.
- Tailwind CSS MUST be the primary styling solution with mobile-first
  class ordering (base -> sm: -> md: -> lg: -> xl:).

### V. High Performance

The backend API and database queries MUST be optimized for fast response
times and efficient resource usage.

- API responses for single-resource endpoints MUST target < 200ms p95 latency.
- List endpoints MUST target < 500ms p95 latency with pagination.
- All FastAPI endpoints performing I/O MUST use async/await patterns.
- Frontend pages MUST use Next.js Server Components by default; Client
  Components MUST only be used when interactivity or browser APIs are required.
- Images MUST use `next/image` for automatic optimization.
- Database queries MUST avoid N+1 patterns; use eager loading where appropriate.
- Frontend MUST implement loading states (skeleton screens) for all data-fetching
  routes via `loading.tsx`.

## Technology Stack & Constraints

### Mandatory Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | Next.js (App Router) | 16+ |
| Backend | Python FastAPI | Latest stable |
| ORM | SQLModel | Latest stable |
| Database | Neon Serverless PostgreSQL | Managed |
| Authentication | Better Auth | Latest stable |
| Styling | Tailwind CSS | 4+ |
| Spec-Driven | Claude Code + Spec-Kit Plus | Current |

### API Contract Requirements

All API endpoints MUST follow RESTful conventions:

- `GET /api/v1/users/{user_id}/tasks` — List all tasks for a user (paginated)
- `POST /api/v1/users/{user_id}/tasks` — Create a new task
- `GET /api/v1/users/{user_id}/tasks/{task_id}` — Get a specific task
- `PUT /api/v1/users/{user_id}/tasks/{task_id}` — Update a task
- `DELETE /api/v1/users/{user_id}/tasks/{task_id}` — Delete a task
- `POST /api/v1/auth/signup` — User registration
- `POST /api/v1/auth/signin` — User login

All endpoints MUST return consistent JSON response format with appropriate
HTTP status codes (200, 201, 204, 400, 401, 403, 404, 409, 422, 429).

### Data Isolation Constraint

Every task query MUST be scoped to the authenticated user. The `user_id` in
the URL path MUST match the authenticated user's identity. Mismatched access
MUST return 403 Forbidden.

## Development Workflow & Quality Gates

### Code Quality Standards

- All Python code MUST include type hints on function signatures.
- All TypeScript code MUST use strict mode with no `any` types.
- Pydantic/SQLModel schemas MUST separate Create, Update, and Response models.
- All API endpoints MUST have proper error handling with custom exception
  classes and consistent error response format.
- All database operations MUST be wrapped in transactions for multi-step writes.

### Testing Requirements

- Backend: pytest with pytest-asyncio for async endpoint testing.
- Frontend: Component tests for critical UI flows.
- All authentication endpoints MUST have tests covering happy path, validation
  errors, and authorization failures.

### Agent Delegation

- **Auth Agent** (`auth-flow-handler`): All authentication/authorization work.
- **Backend Agent** (`fastapi-backend`): All API endpoints and business logic.
- **Frontend Agent** (`nextjs-frontend-builder`): All UI pages and components.
- **DB Agent** (`neon-database-ops`): All schema design, migrations, and queries.

Work spanning multiple layers MUST be coordinated: DB schema first, then
Backend API, then Frontend UI.

## Governance

This constitution is the authoritative source for all development decisions
in the Todo Full-Stack Web Application project. All code changes, architectural
decisions, and feature implementations MUST comply with these principles.

- **Compliance**: All code reviews and PRs MUST verify adherence to these principles.
- **Amendments**: Any change to this constitution MUST be documented with rationale,
  approved by the project owner, and include a migration plan for affected code.
- **Versioning**: Constitution versions follow semantic versioning (MAJOR.MINOR.PATCH).
  MAJOR for principle removals/redefinitions, MINOR for new principles/sections,
  PATCH for clarifications and wording fixes.
- **Conflict resolution**: When principles conflict, Security-First (II) takes
  precedence, followed by User-Centered Design (I), then remaining principles
  in order.
- **Complexity justification**: Any deviation from simplicity or introduction
  of additional abstractions MUST be justified in writing with a specific
  problem statement.

**Version**: 1.0.0 | **Ratified**: 2026-02-09 | **Last Amended**: 2026-02-09
