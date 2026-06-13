# Discussion Forum

A Reddit/StackOverflow-style discussion forum built with FastAPI, React, and PostgreSQL.

---

## Daily Development

One command starts everything — database, backend, and frontend with hot reload:

```bash
docker compose up -d
```

| URL | What |
|---|---|
| `http://localhost:5173` | Frontend app (hot reload) |
| `http://localhost:8080/docs` | API docs (Swagger) |

Stop everything at the end of the day:

```bash
docker compose down
```

The only times you need extra commands on top of this:

| Situation | Extra command |
|---|---|
| First time ever | Run migrations once — see Quick Start below |
| Changed `requirements.txt` | `docker compose build backend` before `up` |
| Added a new DB migration | `docker exec forum_backend python -m alembic upgrade head` |

---

## Quick Start (First Time)

Follow these steps once to set up the project from scratch.

### Step 1 — Copy the environment files

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

The default values work out of the box for local development. No changes needed.

### Step 2 — Start everything

```bash
docker compose up -d --build
```

Wait about 10 seconds for the database to become healthy.

### Step 3 — Run database migrations

This must be done once before first use (and again after any schema change):

```bash
docker exec forum_backend python -m alembic upgrade head
```

### Step 4 — Open the app

| Service | URL |
|---|---|
| Frontend | `http://localhost:5173` (or `5174`) |
| API docs (Swagger) | `http://localhost:8080/docs` |

---

## Service Ports

| Service | Host port | Container port |
|---|---|---|
| FastAPI backend | `8080` | `8000` |
| PostgreSQL | `5433` | `5432` |
| Frontend (Vite dev) | `5173` | `5173` |

---

## Environment Files

### `backend/.env`

```env
# FastAPI
APP_ENV=development
APP_SECRET_KEY=dev-fastapi-secret-key-not-for-production

# Database — use localhost:5433 for local dev; Docker backend overrides to db:5432 internally
DATABASE_URL=postgresql+asyncpg://forum_user:forum_password@localhost:5433/forum_db
DATABASE_HOST=localhost
DATABASE_PORT=5433
DATABASE_NAME=forum_db
DATABASE_USER=forum_user
DATABASE_PASSWORD=forum_password

# JWT
JWT_SECRET_KEY=dev-jwt-secret-key-not-for-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Cookie
COOKIE_SECURE=False
COOKIE_SAMESITE=lax

# CORS — JSON array of allowed frontend origins
CORS_ALLOWED_ORIGINS=["http://localhost:5173","http://localhost:5174","http://localhost:3000"]
```

### `frontend/.env`

```env
VITE_API_BASE_URL=http://localhost:8080
VITE_APP_NAME=Discussion Forum
```

---

## Daily Development Workflow

Once the first-time setup is done, the daily workflow is:

```bash
docker compose up -d
```

The backend has hot reload enabled — Python file changes apply automatically without restarting. The frontend has Vite HMR — React/TS changes apply instantly in the browser.

---

## Docker Commands

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Reset database (wipes all data)
docker compose down -v

# Rebuild backend image (after requirements.txt changes)
docker compose build backend
docker compose up -d backend

# View live backend logs
docker compose logs -f backend

# Open a shell inside the backend container
docker exec -it forum_backend bash
```

---

## Database Migrations

```bash
# Apply all pending migrations (run inside the Docker container)
docker exec forum_backend python -m alembic upgrade head

# Check current migration version
docker exec forum_backend python -m alembic current

# Create a new migration after changing models
docker exec forum_backend python -m alembic revision --autogenerate -m "describe_change"
```

> Always run migrations inside the Docker container — it uses the internal DB connection (`db:5432`), not the host-exposed port.

---

## Running Tests

### Backend (Pytest)

```bash
# Using the venv (Windows)
cd backend
.\venv\Scripts\python.exe -m pytest fastapi_app/tests/ -v

# Or inside Docker
docker exec forum_backend python -m pytest fastapi_app/tests/ -v
```

### Frontend (Vitest)

```bash
cd frontend
npx vitest run          # single run
npx vitest              # watch mode
npx vitest run --coverage
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI + SQLAlchemy 2 (async) + Pydantic v2 |
| Auth | JWT in HttpOnly cookies, bcrypt password hashing |
| Database | PostgreSQL 16, Alembic migrations |
| Frontend | React 19, TypeScript 5, Material UI 6 |
| Forms | React Hook Form + Zod |
| Data fetching | TanStack Query v5 |
| Testing | Pytest (backend), Vitest (frontend) |
| Infrastructure | Docker, Docker Compose |

---

## Project Structure

```
├── CLAUDE.md              # Coding rules (read before writing any code)
├── DOCUMENTATION.md       # API tracker, component tracker, feature status
├── docker-compose.yml
├── backend/
│   ├── .env               # Local environment (not committed)
│   ├── .env.example       # Template to copy from
│   ├── requirements.txt
│   ├── alembic/           # Migration scripts
│   └── fastapi_app/
│       ├── main.py
│       ├── enums.py        # UserRole enum
│       ├── core/           # Config, security, database, dependencies
│       ├── api/v1/         # Endpoints + service providers
│       ├── models/         # SQLAlchemy models
│       ├── schemas/        # Pydantic request/response schemas
│       ├── services/       # Business logic
│       ├── repositories/   # Database access
│       └── tests/          # Pytest test suite
└── frontend/
    ├── .env               # Local environment (not committed)
    ├── .env.example       # Template to copy from
    └── src/
        ├── api/            # Axios client + centralized ApiService
        ├── components/     # Reusable UI components
        ├── hooks/          # Custom React hooks (useAuth)
        ├── pages/          # Route-level page components
        ├── router/         # React Router + route constants
        ├── services/       # Auth, user, post API services
        ├── store/          # AuthContext, QueryProvider
        ├── types/          # TypeScript interfaces
        └── utils/          # Error handler, notification service
```

---

## Coding Standards

See [CLAUDE.md](./CLAUDE.md) for the full rules. Key points:

- All API calls go through `ApiService` — never raw `axios` in components.
- No `try/catch` for API calls in components or pages.
- TypeScript strict mode — no `any`, no inline interface definitions.
- All forms use React Hook Form + Zod.
- Backend: services extend `BaseService`, repositories extend `BaseRepository`.
- Every feature needs: backend + frontend + tests + documentation update.
