# Tasks: Todo Full-Stack Web Application

**Input**: Design documents from `/specs/001-todo-fullstack-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/api.md

**Tests**: Tests are included in Phase 8 (Testing & Polish) as the spec mentions testing requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/app/`, `frontend/app/`
- Paths follow plan.md structure decisions

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize both projects with dependencies and configuration

- [x] T001 Create backend project directory structure per plan.md at `backend/` with `backend/app/` and `backend/app/routes/`
- [x] T002 Create `backend/requirements.txt` with FastAPI, SQLModel, uvicorn, asyncpg, python-jose, passlib[bcrypt], pydantic-settings, alembic, httpx (test)
- [x] T003 [P] Create `backend/.env.example` with DATABASE_URL, DATABASE_URL_DIRECT, JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, FRONTEND_URL
- [x] T004 [P] Create `backend/app/__init__.py` and `backend/app/routes/__init__.py`
- [x] T005 Initialize frontend Next.js 16+ project with TypeScript and Tailwind CSS 4+ at `frontend/` using `npx create-next-app@latest`
- [x] T006 [P] Create `frontend/.env.local.example` with NEXT_PUBLIC_API_URL
- [x] T007 [P] Create shared TypeScript types in `frontend/types/index.ts` (User, Task, AuthResponse, ErrorResponse interfaces)
- [x] T008 [P] Create `frontend/lib/utils.ts` with cn() utility (clsx + tailwind-merge) and formatDate helper

**Checkpoint**: Both projects initialized, dependencies installed, env templates ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Create `backend/app/config.py` with pydantic-settings Settings class (DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, FRONTEND_URL)
- [x] T010 Create `backend/app/database.py` with async SQLModel engine, async session factory using Neon pooled connection string
- [x] T011 Create User SQLModel in `backend/app/models.py` (id: UUID, email: str unique indexed, hashed_password: str, created_at: datetime, updated_at: datetime)
- [x] T012 Add Task SQLModel to `backend/app/models.py` (id: UUID, title: str max 255, description: Optional[str] max 2000, is_completed: bool default False, user_id: UUID FK users.id, created_at: datetime, updated_at: datetime) with indexes on user_id and created_at
- [x] T013 Initialize Alembic in `backend/` with `alembic.ini` and `backend/migrations/env.py` configured for async SQLModel
- [x] T014 Generate initial Alembic migration for users and tasks tables in `backend/migrations/versions/`
- [x] T015 Create custom exception hierarchy in `backend/app/exceptions.py` (AppException, NotFoundError, ConflictError, AuthenticationError, AuthorizationError, ValidationError) with global exception handlers
- [x] T016 [P] Create `backend/app/security.py` with password hashing (bcrypt cost 12) and JWT encode/decode functions using python-jose
- [x] T017 Create `backend/app/dependencies.py` with get_db session dependency
- [x] T018 Create `backend/app/main.py` with FastAPI app, CORS middleware (allow FRONTEND_URL origin, credentials=True), register exception handlers, include route routers
- [x] T019 Create `backend/app/routes/__init__.py` aggregating auth and tasks sub-routers
- [x] T020 [P] Create `frontend/lib/api.ts` with fetch wrapper that includes credentials ('include' for cookies), handles 401 redirects to /login, parses JSON responses and error format
- [x] T021 [P] Create reusable UI primitives in `frontend/components/ui/` (Button, Input, Card, Label, Dialog components with Tailwind styling)
- [x] T022 Create `frontend/app/layout.tsx` root layout with HTML lang, fonts, Tailwind base styles, metadata
- [x] T023 [P] Create `frontend/app/loading.tsx` root loading skeleton
- [x] T024 [P] Create `frontend/app/error.tsx` root error boundary with retry button
- [x] T025 [P] Create `frontend/app/not-found.tsx` 404 page

**Checkpoint**: Foundation ready — database connected, models defined, migration created, shared infrastructure in place. User story implementation can now begin.

---

## Phase 3: User Story 1 — User Registration and Login (Priority: P1) MVP

**Goal**: Users can sign up, sign in, sign out with email/password. JWT tokens issued in httpOnly cookies.

**Independent Test**: Register a new account, sign out, sign back in. Verify redirect to dashboard on success and generic error on failure.

### Implementation for User Story 1

- [ ] T026 [US1] Create auth schemas in `backend/app/schemas.py` (SignupRequest: email + password with validators, SigninRequest: email + password, AuthResponse: user id + email + access_token)
- [ ] T027 [US1] Create auth route handlers in `backend/app/routes/auth.py` (create_user: hash password + save + return JWT, authenticate_user: verify credentials + return JWT, generate tokens: create access token with user_id as sub claim)
- [ ] T028 [US1] Create auth endpoints in `backend/app/routes/auth.py` (POST /auth/signup → 201 with JWT cookie, POST /auth/signin → 200 with JWT cookie, POST /auth/signout → 204 clear cookie)
- [ ] T029 [US1] Create get_current_user dependency in `backend/app/dependencies.py` (extract JWT from cookie, decode, fetch user from DB, return User or raise 401)
- [ ] T030 [US1] Add rate limiting middleware for auth endpoints in `backend/app/main.py`
- [ ] T031 [US1] Create `frontend/lib/auth.ts` with auth helpers (checkAuth server-side, signOut client-side)
- [ ] T032 [US1] Create auth layout in `frontend/app/(auth)/layout.tsx` (centered card layout for login/signup pages)
- [ ] T033 [US1] Create signup page in `frontend/app/(auth)/signup/page.tsx` (email + password form, validation, error display, submit to POST /auth/signup, redirect to dashboard on success)
- [ ] T034 [US1] Create login page in `frontend/app/(auth)/login/page.tsx` (email + password form, validation, generic error message on failure, redirect to dashboard on success)
- [ ] T035 [US1] Create `frontend/app/page.tsx` root page (redirect authenticated users to dashboard, unauthenticated to login)

**Checkpoint**: Users can register and sign in. Auth cookie is set. Protected routes redirect to login. US1 is fully functional and testable independently.

---

## Phase 4: User Story 2 — Create a New Task (Priority: P1)

**Goal**: Signed-in users can create tasks with title and optional description. Tasks appear immediately in their list.

**Independent Test**: Sign in, create a task with a title, verify it appears in the list with "incomplete" status.

### Implementation for User Story 2

- [ ] T036 [US2] Create task schemas in `backend/app/schemas.py` (TaskCreate: title required max 255 + description optional max 2000, TaskUpdate: title optional + description optional, TaskResponse: id + title + description + is_completed + created_at + updated_at, TaskListResponse: tasks list + total count)
- [ ] T037 [US2] Create task create handler in `backend/app/routes/tasks.py` (create_task: validate user_id matches auth user, create Task with user_id, return TaskResponse)
- [ ] T038 [US2] Create POST /users/{user_id}/tasks endpoint in `backend/app/routes/tasks.py` (validate user_id matches current_user.id → 403 if mismatch, create task, return 201)
- [ ] T039 [US2] Implement user_id path validation dependency in `backend/app/dependencies.py` (verify_user_ownership: compare path user_id with JWT user_id, raise 403 on mismatch)
- [ ] T040 [US2] Create dashboard layout in `frontend/app/(dashboard)/layout.tsx` (nav bar with app title and sign-out button, protected route check — redirect to /login if no auth cookie)
- [ ] T041 [US2] Create TaskForm component in `frontend/components/forms/TaskForm.tsx` (title input required + description textarea optional, validation, submit handler, loading state)
- [ ] T042 [US2] Create dashboard page with create task form in `frontend/app/(dashboard)/page.tsx` (display TaskForm at top, call POST /users/{user_id}/tasks on submit, show success/error feedback)

**Checkpoint**: Users can create tasks. Created tasks are stored in database with user_id association. US2 is functional.

---

## Phase 5: User Story 3 — View All Tasks (Priority: P1)

**Goal**: Signed-in users see their task list with title, status, and creation date. Only their own tasks are shown.

**Independent Test**: Create tasks as User A, sign in as User B, verify only User B's tasks appear (or empty state if none).

### Implementation for User Story 3

- [ ] T043 [US3] Create task list handler in `backend/app/routes/tasks.py` (list_tasks: query tasks WHERE user_id = current_user.id ORDER BY created_at DESC, return TaskListResponse with total count)
- [ ] T044 [US3] Create GET /users/{user_id}/tasks endpoint in `backend/app/routes/tasks.py` (validate user_id ownership, list tasks, support limit/offset query params, return 200)
- [ ] T045 [US3] Create task get_by_id handler in `backend/app/routes/tasks.py` (get_task: query task WHERE id = task_id AND user_id = current_user.id, return TaskResponse or raise 404)
- [ ] T046 [US3] Create GET /users/{user_id}/tasks/{task_id} endpoint in `backend/app/routes/tasks.py` (validate user_id ownership, get task, return 200 or 404)
- [ ] T047 [US3] Create TaskItem component in `frontend/components/tasks/TaskItem.tsx` (display title, completion status checkbox, created_at date, action buttons for edit/delete)
- [ ] T048 [US3] Create TaskList component in `frontend/components/tasks/TaskList.tsx` (render list of TaskItem components, show empty state message when no tasks exist)
- [ ] T049 [US3] Update dashboard page `frontend/app/(dashboard)/page.tsx` to fetch and display task list (call GET /users/{user_id}/tasks, render TaskList, show loading skeleton while fetching)
- [ ] T050 [P] [US3] Create dashboard loading skeleton in `frontend/app/(dashboard)/loading.tsx`

**Checkpoint**: Task list displays user-scoped tasks. Empty state shown for new users. Data isolation enforced. US1 + US2 + US3 form the MVP.

---

## Phase 6: User Story 4 — Update an Existing Task (Priority: P2)

**Goal**: Signed-in users can edit their task's title and description. Updated timestamp refreshes.

**Independent Test**: Create a task, edit its title, verify the updated title displays.

### Implementation for User Story 4

- [ ] T051 [US4] Create task update handler in `backend/app/routes/tasks.py` (update_task: find task by id + user_id, update provided fields, refresh updated_at, return TaskResponse or 404)
- [ ] T052 [US4] Create PUT /users/{user_id}/tasks/{task_id} endpoint in `backend/app/routes/tasks.py` (validate user_id ownership, update task, return 200 or 404/422)
- [ ] T053 [US4] Create task detail/edit page in `frontend/app/(dashboard)/tasks/[id]/page.tsx` (fetch task by id, display editable form with title and description, save button calls PUT endpoint, show success/error feedback, back navigation to dashboard)

**Checkpoint**: Users can edit task details. Updated_at timestamp refreshes. US4 is functional.

---

## Phase 7: User Story 5 — Delete a Task (Priority: P2)

**Goal**: Signed-in users can delete tasks with confirmation. Task permanently removed.

**Independent Test**: Create a task, delete it with confirmation, verify it no longer appears in the list.

### Implementation for User Story 5

- [ ] T054 [US5] Create task delete handler in `backend/app/routes/tasks.py` (delete_task: find task by id + user_id, delete, return None or raise 404)
- [ ] T055 [US5] Create DELETE /users/{user_id}/tasks/{task_id} endpoint in `backend/app/routes/tasks.py` (validate user_id ownership, delete task, return 204 or 404)
- [ ] T056 [US5] Create ConfirmDialog component in `frontend/components/ui/ConfirmDialog.tsx` (modal with message, confirm and cancel buttons, accessible with proper ARIA attributes)
- [ ] T057 [US5] Add delete button and confirmation flow to TaskItem in `frontend/components/tasks/TaskItem.tsx` (delete button opens ConfirmDialog, confirm calls DELETE endpoint, remove from list on success)

**Checkpoint**: Users can delete tasks with confirmation. Deleted tasks removed from list. US5 is functional.

---

## Phase 8: User Story 6 — Toggle Task Completion (Priority: P2)

**Goal**: Signed-in users can toggle tasks between complete and incomplete. Visual distinction for completed tasks.

**Independent Test**: Create a task, toggle it complete (verify strikethrough), toggle back to incomplete (verify normal styling).

### Implementation for User Story 6

- [ ] T058 [US6] Create task toggle handler in `backend/app/routes/tasks.py` (toggle_complete: find task by id + user_id, flip is_completed boolean, refresh updated_at, return TaskResponse or 404)
- [ ] T059 [US6] Create PATCH /users/{user_id}/tasks/{task_id}/complete endpoint in `backend/app/routes/tasks.py` (validate user_id ownership, toggle completion, return 200 or 404)
- [ ] T060 [US6] Add completion toggle to TaskItem in `frontend/components/tasks/TaskItem.tsx` (checkbox that calls PATCH /complete endpoint, apply strikethrough/muted styling for completed tasks, optimistic UI update)

**Checkpoint**: Completion toggle works end-to-end. Visual feedback on status change. All 6 user stories are functional.

---

## Phase 9: Testing & Polish

**Purpose**: Tests, error handling, responsive validation, cross-cutting concerns

- [ ] T061 [P] Create test fixtures in `backend/tests/conftest.py` (test database session, async test client via httpx, helper functions to create test users and get auth cookies)
- [ ] T062 [P] Write auth endpoint tests in `backend/tests/test_auth.py` (test signup success 201, duplicate email 409, signin success 200, wrong password 401, signout 204, missing fields 422)
- [ ] T063 [P] Write task CRUD endpoint tests in `backend/tests/test_tasks.py` (test create 201, list 200 user-scoped, get 200, update 200, delete 204, toggle complete 200, not found 404, validation errors 422)
- [ ] T064 Write data isolation tests in `backend/tests/test_tasks.py` (test User A cannot GET/PUT/DELETE/PATCH User B's tasks → 403, user_id path mismatch → 403)
- [ ] T065 [P] Verify all error responses match the consistent JSON error format from contracts/api.md across all endpoints
- [ ] T066 [P] Verify responsive layout of dashboard at 320px, 768px, 1024px, 1440px viewports — no horizontal scroll, touch targets >= 44px on mobile
- [ ] T067 Verify all edge cases: expired token redirects to login, 404 for deleted tasks shows user-friendly message, long text validation enforced (255 title, 2000 description)
- [ ] T068 Create `backend/.env.example` and `frontend/.env.local.example` with all required environment variables documented

**Checkpoint**: All tests pass. Error handling verified. Responsive design confirmed. Application is production-ready.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories
- **US1 Auth (Phase 3)**: Depends on Phase 2 — BLOCKS US2, US3, US4, US5, US6 (auth is required for all task operations)
- **US2 Create (Phase 4)**: Depends on Phase 3 (needs auth)
- **US3 View (Phase 5)**: Depends on Phase 4 (needs tasks to exist to view)
- **US4 Update (Phase 6)**: Depends on Phase 5 (needs task list + detail view infrastructure)
- **US5 Delete (Phase 7)**: Depends on Phase 5 (needs task list rendering to add delete button)
- **US6 Toggle (Phase 8)**: Depends on Phase 5 (needs task list rendering to add toggle)
- **Testing (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Foundation only — gateway to all other stories
- **US2 (P1)**: Depends on US1 (needs auth to create tasks)
- **US3 (P1)**: Depends on US2 (needs tasks to exist for listing)
- **US4 (P2)**: Depends on US3 (needs task list + detail page infrastructure), can run parallel with US5 and US6
- **US5 (P2)**: Depends on US3 (needs TaskItem component), can run parallel with US4 and US6
- **US6 (P2)**: Depends on US3 (needs TaskItem component), can run parallel with US4 and US5

### Within Each User Story

- Backend schemas before services
- Backend services before endpoints
- Backend endpoints before frontend pages that consume them
- Frontend components before pages that use them

### Parallel Opportunities

- Phase 1: T003, T004, T006, T007, T008 can run in parallel
- Phase 2: T016 can run parallel with T015; T020, T021, T023, T024, T025 can run in parallel
- Phase 5: T050 can run parallel with other US3 tasks
- Phase 6-8: US4, US5, US6 can run in parallel once US3 is complete (different files, independent features)
- Phase 9: T061, T062, T063, T065, T066 can run in parallel

---

## Parallel Example: P2 User Stories (After US3 Complete)

```bash
# These three story phases can run in parallel (different files, independent features):

# Developer A — US4 Update:
Task: T051 "Create task update handler in backend/app/routes/tasks.py"
Task: T052 "Create PUT endpoint in backend/app/routes/tasks.py"
Task: T053 "Create task detail/edit page in frontend/app/(dashboard)/tasks/[id]/page.tsx"

# Developer B — US5 Delete:
Task: T054 "Create task delete handler in backend/app/routes/tasks.py"
Task: T055 "Create DELETE endpoint in backend/app/routes/tasks.py"
Task: T056 "Create ConfirmDialog in frontend/components/ui/ConfirmDialog.tsx"
Task: T057 "Add delete flow to TaskItem in frontend/components/tasks/TaskItem.tsx"

# Developer C — US6 Toggle:
Task: T058 "Create task toggle handler in backend/app/routes/tasks.py"
Task: T059 "Create PATCH endpoint in backend/app/routes/tasks.py"
Task: T060 "Add toggle to TaskItem in frontend/components/tasks/TaskItem.tsx"
```

**Note**: US4, US5, and US6 all add handlers to `backend/app/routes/tasks.py` — if running in parallel, coordinate to avoid merge conflicts. US5 and US6 both modify TaskItem.tsx (US5 adds delete button, US6 adds checkbox toggle — different sections of the component).

---

## Implementation Strategy

### MVP First (US1 + US2 + US3)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: US1 — Registration & Login
4. Complete Phase 4: US2 — Create Task
5. Complete Phase 5: US3 — View All Tasks
6. **STOP and VALIDATE**: Test US1 + US2 + US3 independently — users can register, create, and view tasks
7. Deploy/demo if ready (MVP!)

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Auth) → Test independently → Users can register/login
3. Add US2 (Create) → Test independently → Users can add tasks
4. Add US3 (View) → Test independently → Deploy/Demo (MVP!)
5. Add US4 (Update) → Test independently → Users can edit tasks
6. Add US5 (Delete) → Test independently → Users can remove tasks
7. Add US6 (Toggle) → Test independently → Users can track progress
8. Testing & Polish → Production-ready

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Agent delegation: T009-T019, T026-T030, T036-T046, T051-T055, T058-T059 → Backend Agent; T020-T025, T031-T035, T040-T042, T047-T050, T053, T056-T057, T060 → Frontend Agent; T026-T030 auth logic → Auth Agent; T011-T014 schema/model design → DB Agent
- Backend file layout: flat structure — `models.py`, `schemas.py`, `security.py`, `exceptions.py`, `routes/auth.py`, `routes/tasks.py` (no nested packages)
