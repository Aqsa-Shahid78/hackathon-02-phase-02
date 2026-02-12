# API Contracts: Todo Full-Stack Web Application

**Branch**: `001-todo-fullstack-app` | **Date**: 2026-02-09
**Base URL**: `/api/v1`

## Authentication Endpoints

### POST /auth/signup

Register a new user account.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Validation**:
- `email`: Required, valid email format, max 255 chars
- `password`: Required, min 8 chars, max 128 chars

**Responses**:

| Status | Description | Body |
|--------|-------------|------|
| 201 | Account created, JWT issued | `{ "user": { "id": "uuid", "email": "..." }, "access_token": "jwt..." }` |
| 409 | Email already registered | `{ "error": { "code": "CONFLICT", "message": "Account creation failed" } }` |
| 422 | Validation error | `{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }` |
| 429 | Rate limited | `{ "error": { "code": "RATE_LIMITED", "message": "Too many requests" } }` |

**Cookie set**: `access_token` (httpOnly, secure, sameSite=lax)

---

### POST /auth/signin

Authenticate an existing user.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Responses**:

| Status | Description | Body |
|--------|-------------|------|
| 200 | Signed in, JWT issued | `{ "user": { "id": "uuid", "email": "..." }, "access_token": "jwt..." }` |
| 401 | Invalid credentials | `{ "error": { "code": "UNAUTHORIZED", "message": "Invalid credentials" } }` |
| 422 | Validation error | `{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }` |
| 429 | Rate limited | `{ "error": { "code": "RATE_LIMITED", "message": "Too many requests" } }` |

**Cookie set**: `access_token` (httpOnly, secure, sameSite=lax)

---

### POST /auth/signout

Sign out the current user.

**Headers**: `Cookie: access_token=<jwt>`

**Responses**:

| Status | Description | Body |
|--------|-------------|------|
| 204 | Signed out | (no body) |
| 401 | Not authenticated | `{ "error": { "code": "UNAUTHORIZED", "message": "Not authenticated" } }` |

**Cookie cleared**: `access_token`

---

## Task Endpoints

All task endpoints require authentication via JWT cookie.

**Common auth error responses** (apply to all task endpoints):

| Status | Description | Body |
|--------|-------------|------|
| 401 | Missing or invalid token | `{ "error": { "code": "UNAUTHORIZED", "message": "Not authenticated" } }` |
| 403 | User ID mismatch | `{ "error": { "code": "FORBIDDEN", "message": "Access denied" } }` |

---

### GET /users/{user_id}/tasks

List all tasks for the authenticated user, sorted by creation date (newest first).

**Path Parameters**: `user_id` (UUID) — must match authenticated user's ID

**Query Parameters** (future pagination support):
- `limit` (int, default 50, max 100) — number of tasks to return
- `offset` (int, default 0) — number of tasks to skip

**Responses**:

| Status | Description | Body |
|--------|-------------|------|
| 200 | Task list | `{ "tasks": [TaskResponse], "total": 42 }` |

**TaskResponse**:
```json
{
  "id": "uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "created_at": "2026-02-09T10:00:00Z",
  "updated_at": "2026-02-09T10:00:00Z"
}
```

---

### POST /users/{user_id}/tasks

Create a new task for the authenticated user.

**Path Parameters**: `user_id` (UUID) — must match authenticated user's ID

**Request**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Validation**:
- `title`: Required, non-empty, max 255 chars
- `description`: Optional, max 2000 chars

**Responses**:

| Status | Description | Body |
|--------|-------------|------|
| 201 | Task created | `TaskResponse` |
| 422 | Validation error | `{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }` |

---

### GET /users/{user_id}/tasks/{task_id}

Get a specific task by ID.

**Path Parameters**:
- `user_id` (UUID) — must match authenticated user's ID
- `task_id` (UUID) — task identifier

**Responses**:

| Status | Description | Body |
|--------|-------------|------|
| 200 | Task found | `TaskResponse` |
| 404 | Task not found | `{ "error": { "code": "NOT_FOUND", "message": "Task not found" } }` |

---

### PUT /users/{user_id}/tasks/{task_id}

Update a task's title and/or description.

**Path Parameters**:
- `user_id` (UUID) — must match authenticated user's ID
- `task_id` (UUID) — task identifier

**Request**:
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Validation**:
- `title`: Optional but if provided must be non-empty, max 255 chars
- `description`: Optional, max 2000 chars (null to clear)

**Responses**:

| Status | Description | Body |
|--------|-------------|------|
| 200 | Task updated | `TaskResponse` |
| 404 | Task not found | `{ "error": { "code": "NOT_FOUND", "message": "Task not found" } }` |
| 422 | Validation error | `{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }` |

---

### DELETE /users/{user_id}/tasks/{task_id}

Delete a task permanently.

**Path Parameters**:
- `user_id` (UUID) — must match authenticated user's ID
- `task_id` (UUID) — task identifier

**Responses**:

| Status | Description | Body |
|--------|-------------|------|
| 204 | Task deleted | (no body) |
| 404 | Task not found | `{ "error": { "code": "NOT_FOUND", "message": "Task not found" } }` |

---

### PATCH /users/{user_id}/tasks/{task_id}/complete

Toggle task completion status. Flips `is_completed` from `false` to `true`
or from `true` to `false`.

**Path Parameters**:
- `user_id` (UUID) — must match authenticated user's ID
- `task_id` (UUID) — task identifier

**Request**: No body required.

**Responses**:

| Status | Description | Body |
|--------|-------------|------|
| 200 | Completion toggled | `TaskResponse` |
| 404 | Task not found | `{ "error": { "code": "NOT_FOUND", "message": "Task not found" } }` |

---

## Error Response Format

All error responses follow this consistent format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": null
  }
}
```

**Error codes**:
- `VALIDATION_ERROR` — Input validation failed (422)
- `UNAUTHORIZED` — Missing or invalid authentication (401)
- `FORBIDDEN` — Insufficient permissions / user mismatch (403)
- `NOT_FOUND` — Resource does not exist (404)
- `CONFLICT` — Resource conflict (e.g., duplicate email) (409)
- `RATE_LIMITED` — Too many requests (429)
- `INTERNAL_ERROR` — Unexpected server error (500)
