# Quickstart: Todo Full-Stack Web Application

**Branch**: `001-todo-fullstack-app` | **Date**: 2026-02-09

## Prerequisites

- Python 3.12+
- Node.js 20+ and npm/pnpm
- A Neon PostgreSQL account with a database provisioned
- Git

## 1. Clone and Setup

```bash
git clone <repository-url>
cd phase-02
git checkout 001-todo-fullstack-app
```

## 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your values:
#   DATABASE_URL=postgresql+asyncpg://<user>:<pass>@<host>/<db>?sslmode=require
#   JWT_SECRET=<your-secret-key-min-32-chars>
#   FRONTEND_URL=http://localhost:3000

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`.
API docs at `http://localhost:8000/docs`.

## 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install  # or pnpm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with your values:
#   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Start frontend dev server
npm run dev  # or pnpm dev
```

Frontend will be available at `http://localhost:3000`.

## 4. Verify Setup

1. Open `http://localhost:3000` in your browser
2. Click "Sign Up" and create an account
3. After signup, you should be redirected to the task dashboard
4. Create a task by entering a title and clicking "Add Task"
5. Verify the task appears in your list
6. Toggle the task as complete
7. Edit the task title
8. Delete the task

## Environment Variables

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon PostgreSQL connection string (pooled) | `postgresql+asyncpg://user:pass@host/db` |
| `DATABASE_URL_DIRECT` | Direct connection for migrations | `postgresql+asyncpg://user:pass@host/db` |
| `JWT_SECRET` | Secret key for JWT signing (min 32 chars) | `your-super-secret-key-at-least-32-chars` |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT access token lifetime | `30` |
| `FRONTEND_URL` | Frontend origin for CORS | `http://localhost:3000` |

### Frontend (.env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000/api/v1` |

## Common Issues

- **CORS errors**: Ensure `FRONTEND_URL` in backend `.env` matches the
  frontend's actual URL (including port).
- **Database connection failures**: Verify your Neon connection string uses
  the pooled endpoint (contains `-pooler` in hostname).
- **Migration errors**: Use the direct (non-pooled) connection string for
  Alembic migrations.
