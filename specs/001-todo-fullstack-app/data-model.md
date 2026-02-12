# Data Model: Todo Full-Stack Web Application

**Branch**: `001-todo-fullstack-app` | **Date**: 2026-02-09

## Entities

### User

Represents a registered account in the system.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default `gen_random_uuid()` | Unique identifier |
| email | text | UNIQUE, NOT NULL, indexed | User email address |
| hashed_password | text | NOT NULL | bcrypt-hashed password (cost >= 12) |
| created_at | timestamptz | NOT NULL, default `now()` | Account creation time |
| updated_at | timestamptz | NOT NULL, default `now()` | Last update time |

**Indexes**:
- `ix_users_email` — UNIQUE index on `email`

**Triggers**:
- `updated_at` auto-updates on row modification

---

### Task

Represents a to-do item belonging to a single user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default `gen_random_uuid()` | Unique identifier |
| title | varchar(255) | NOT NULL | Task title (max 255 chars) |
| description | text | nullable, max 2000 chars | Optional task description |
| is_completed | boolean | NOT NULL, default `false` | Completion status |
| user_id | UUID | FK → users.id, NOT NULL, indexed | Owner reference |
| created_at | timestamptz | NOT NULL, default `now()` | Task creation time |
| updated_at | timestamptz | NOT NULL, default `now()` | Last update time |

**Indexes**:
- `ix_tasks_user_id` — index on `user_id` (primary query filter)
- `ix_tasks_created_at` — index on `created_at` (sort order)
- `ix_tasks_user_id_created_at` — composite index on `(user_id, created_at DESC)` (covers the primary list query)

**Foreign Keys**:
- `user_id` → `users.id` ON DELETE CASCADE

**Triggers**:
- `updated_at` auto-updates on row modification

## Relationships

```text
User (1) ──────< Task (many)
  │                 │
  │ id ◄────────── user_id (FK)
  │                 │
  └─ ON DELETE CASCADE (deleting user removes all their tasks)
```

- A **User** has zero or more **Tasks**.
- A **Task** belongs to exactly one **User**.
- Deleting a User cascades to delete all their Tasks.

## Validation Rules

### User
- `email`: Valid email format, unique across all users, case-insensitive
  (stored lowercase).
- `hashed_password`: Never exposed in API responses. Original password must
  be minimum 8 characters.

### Task
- `title`: Required, non-empty, maximum 255 characters. Trimmed of leading/
  trailing whitespace.
- `description`: Optional, maximum 2000 characters.
- `is_completed`: Boolean, defaults to `false` on creation.
- `user_id`: Must match the authenticated user's ID on all operations.

## State Transitions

### Task Completion

```text
┌──────────────┐     toggle      ┌──────────────┐
│  Incomplete  │ ──────────────► │   Complete   │
│ is_completed │                 │ is_completed │
│   = false    │ ◄────────────── │   = true     │
└──────────────┘     toggle      └──────────────┘
```

- Toggle is idempotent: `PATCH /complete` flips the current boolean value.
- No intermediate states; completion is binary.

## Migration Strategy

- **Tool**: Alembic (auto-generate from SQLModel definitions)
- **Naming**: `YYYY_MM_DD_HHMM_<description>.py`
- **Reversibility**: All migrations include `upgrade()` and `downgrade()` functions
- **Connection**: Migrations use direct (non-pooled) Neon connection string
