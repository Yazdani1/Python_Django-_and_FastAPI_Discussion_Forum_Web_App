# DOCUMENTATION.md — Project Memory

> This document is the **living reference** for the Discussion Forum project.
> Always update this file when adding features, endpoints, components, or schema changes.
> Always read this file before scanning the codebase.

---

## 1. Project Overview

A Reddit/StackOverflow-style discussion forum with:
- Threaded posts and replies
- Voting system
- User profiles and roles
- Tag/category organization
- Admin moderation

**Current Phase:** Auth + User Profiles + Discussion Posts + Answers + Voting + Admin Moderation + Search (author filter) implemented.

---

## 2. Technology Stack

### Backend
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13+ | Runtime |
| FastAPI | Latest | REST API framework |
| PostgreSQL | 16+ | Primary database |
| SQLAlchemy | 2+ | Async ORM |
| Alembic | Latest | Database migrations |
| Pydantic | v2 | Request/response validation |
| Pytest | Latest | Testing |
| Uvicorn | Latest | ASGI server |
| python-jose | Latest | JWT handling |
| bcrypt | 5.x | Password hashing (direct, no passlib) |
| email-validator | 2.x | EmailStr validation |

### Frontend
| Tool | Version | Purpose |
|---|---|---|
| React | 19+ | UI framework |
| TypeScript | 5+ | Type safety |
| Material UI | 6+ | Component library |
| React Router | 6+ | Client-side routing |
| TanStack Query | 5+ | Server state management |
| Axios | Latest | HTTP client |
| React Hook Form | Latest | Form management |
| Zod | Latest | Schema validation |
| Vitest | Latest | Unit testing |

### Infrastructure
| Tool | Purpose |
|---|---|
| Docker | Containerization |
| Docker Compose | Local orchestration |
| Redis | Response caching (posts list + detail) |
| Nginx | Reverse proxy (production) |

---

## 3. Folder Structure

```
Discussion_Forum/
├── CLAUDE.md
├── DOCUMENTATION.md
├── README.md
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       ├── 0001_create_users_and_posts.py
│   │       ├── 0002_add_answers.py
│   │       ├── 0003_add_votes.py
│   │       └── 0004_add_moderation_logs.py
│   └── fastapi_app/
│       ├── main.py
│       ├── enums.py              # UserRole, VoteType, ModerationAction enums + ROLE_LEVELS
│       ├── core/
│       │   ├── config.py
│       │   ├── security.py       # JWT + password handlers
│       │   ├── database.py       # SQLAlchemy engine
│       │   ├── cache.py          # Redis async helpers (cache_get/set/delete/delete_pattern)
│       │   └── dependencies.py   # get_current_user, require_role, get_optional_current_user
│       ├── api/
│       │   └── v1/
│       │       ├── router.py
│       │       ├── dependencies.py   # Service provider factories
│       │       └── endpoints/
│       │           ├── health.py
│       │           ├── auth.py
│       │           ├── users.py
│       │           ├── posts.py      # Includes vote endpoints
│       │           ├── answers.py    # Answer CRUD + answer vote endpoints
│       │           └── admin.py      # Block/unblock users, moderation logs
│       ├── models/
│       │   ├── user.py           # User model
│       │   ├── post.py           # Post model
│       │   ├── answer.py         # Answer model
│       │   ├── vote.py           # Vote model (polymorphic: post or answer)
│       │   └── moderation_log.py # ModerationLog model
│       ├── schemas/
│       │   ├── auth.py           # RegisterRequest, LoginRequest
│       │   ├── user.py           # UserRead, UserUpdate, UserPublic
│       │   ├── post.py           # PostCreate, PostRead, PostUpdate, PostListItem
│       │   ├── answer.py         # AnswerCreate, AnswerUpdate, AnswerRead
│       │   └── vote.py           # VoteRequest, VoteResult
│       ├── services/
│       │   ├── base.py
│       │   ├── auth_service.py
│       │   ├── user_service.py
│       │   ├── post_service.py
│       │   ├── answer_service.py
│       │   ├── vote_service.py
│       │   └── moderation_service.py  # Includes ModerationRepository inline
│       ├── repositories/
│       │   ├── base.py
│       │   ├── user_repository.py
│       │   ├── post_repository.py
│       │   ├── answer_repository.py
│       │   └── vote_repository.py
│       └── tests/
│           ├── conftest.py
│           ├── test_health.py
│           ├── test_security.py
│           ├── test_responses.py
│           ├── test_auth.py
│           ├── test_users.py
│           ├── test_posts.py
│           ├── test_answers.py
│           ├── test_votes.py
│           └── test_admin.py
└── frontend/
    └── src/
        ├── api/
        │   ├── client.ts
        │   ├── service.ts
        │   └── types.ts
        ├── components/
        │   ├── auth/
        │   │   ├── LoginForm.tsx
        │   │   └── RegisterForm.tsx
        │   ├── layout/
        │   │   ├── Layout.tsx
        │   │   ├── Navbar.tsx    # Auth-aware, shows AvatarDropdown
        │   │   └── Footer.tsx
        │   ├── common/
        │   │   └── PageContainer.tsx
        │   ├── guards/
        │   │   ├── ProtectedRoute.tsx  # Uses useAuth() internally
        │   │   └── RoleGuard.tsx       # Uses useAuth() internally
        │   ├── posts/
        │   │   ├── PostCard.tsx
        │   │   ├── PostForm.tsx
        │   │   ├── SearchBar.tsx       # Text + author + date range search
        │   │   └── VoteButtons.tsx     # Up/down vote UI with toggle logic
        │   ├── answers/
        │   │   ├── AnswerCard.tsx      # Single answer with inline edit + vote buttons
        │   │   ├── AnswerForm.tsx      # RHF+Zod form for posting/editing answers
        │   │   └── AnswerList.tsx      # Full answer section with mutations
        │   └── user/
        │       └── AvatarDropdown.tsx
        ├── hooks/
        │   └── useAuth.ts         # Thin wrapper around useAuthContext
        ├── pages/
        │   ├── HomePage.tsx       # Post listing + search
        │   ├── LoginPage.tsx
        │   ├── RegisterPage.tsx
        │   ├── ProfilePage.tsx
        │   ├── PostDetailPage.tsx # Now includes votes, answers, admin actions
        │   ├── CreatePostPage.tsx
        │   ├── EditPostPage.tsx
        │   └── NotFoundPage.tsx
        ├── router/
        │   ├── index.tsx
        │   └── routes.ts
        ├── services/
        │   ├── authService.ts
        │   ├── userService.ts
        │   ├── postService.ts
        │   ├── answerService.ts
        │   ├── voteService.ts
        │   └── adminService.ts
        ├── store/
        │   ├── AuthContext.tsx    # Auth state + login/logout
        │   ├── QueryProvider.tsx
        │   └── NotificationProvider.tsx
        ├── types/
        │   ├── api.types.ts
        │   ├── auth.types.ts      # IAuthUser, ILoginRequest, IRegisterRequest
        │   ├── user.types.ts      # IUserProfile, IUserUpdateRequest
        │   ├── post.types.ts      # IPost (+vote_count,answer_count,user_vote), IPostListItem, IPostSearchParams (+author)
        │   ├── answer.types.ts    # IAnswer, IAnswerCreateRequest, IAnswerUpdateRequest
        │   └── vote.types.ts      # IVoteRequest, IVoteResult
        └── utils/
            ├── errorHandler.ts
            └── notificationService.ts
```

---

## 4. Architecture Decisions

| Decision | Choice | Reason |
|---|---|---|
| Backend framework | FastAPI | Async-first, fast, type-safe REST API with native Pydantic integration |
| JWT in HttpOnly cookies | Cookies, not localStorage | XSS protection — JS cannot access HttpOnly cookies |
| SQLAlchemy for FastAPI | Not Django ORM | FastAPI is async-first; SQLAlchemy async is a better fit |
| Separate Alembic migrations | Not Django migrations | SQLAlchemy models managed by Alembic, not Django |
| React Query for state | Not Redux | Server state is separate from UI state; React Query handles caching, refetch, and sync |
| Zod + RHF | Not Formik / Yup | Zod integrates natively with TypeScript inference; RHF is performant |
| Auth via Context | Not Redux | Auth state is simple enough for Context; avoids Redux overhead |
| Service DI via dependency overrides | FastAPI providers | Enables clean mocking in tests without DB |

---

## 5. Authentication Strategy

- JWT tokens issued on login.
- `access_token` stored as `HttpOnly` `Secure` cookie (15 min default).
- `refresh_token` stored as `HttpOnly` `Secure` cookie (7 days default).
- Frontend sends cookies automatically via `withCredentials: true`.
- Token refresh handled transparently by Axios response interceptor in `client.ts`.
- Logout clears both cookies server-side.
- `AuthProvider` calls `/api/v1/users/me` on mount to restore session.

### Role System
| Role | Level | Description |
|---|---|---|
| `guest` | 0 | Unauthenticated visitor |
| `user` | 1 | Registered member |
| `moderator` | 2 | Can manage others' posts |
| `admin` | 3 | Full system access |

---

## 6. API Design Standards

- Base URL: `/api/v1/`
- All responses use `ApiResponse` envelope.
- HTTP status codes used correctly.
- Pagination via `page` and `page_size` query params.

---

## 7. Frontend Standards

- All routes defined in `router/routes.ts` as constants.
- All API calls through `ApiService` only — never raw axios in components.
- Forms: always `React Hook Form` + `zodResolver`.
- Styling: MUI `sx` prop or `theme` — no inline style objects.
- No `any` in TypeScript.
- Component files: one component per file.
- Interface naming: `IComponentNameProps`.
- `ProtectedRoute` / `RoleGuard` use `useAuth()` internally — do not pass `user` prop.

---

## 8. Backend Standards

- All endpoints return `ApiResponse` or raise `ApiError`.
- Service providers defined in `api/v1/dependencies.py` (injectable and mockable).
- Endpoint functions thin — only call service methods.
- Service methods contain business logic.
- Repository methods contain data access logic.
- Pydantic v2 schemas for all request/response types.
- No ORM queries in services — only repository method calls.

---

## 9. Security Standards

- Passwords hashed with bcrypt (direct, no passlib).
- JWT signed with HS256.
- CORS restricted to allowed origins.
- SQL injection prevented by ORM.
- XSS prevented by HttpOnly cookies.
- CSRF protection via SameSite cookie attribute.
- All secrets via environment variables.
- Avatar uploads: only JPEG/PNG/GIF/WebP, max 5 MB.
- Post deletion/edit: only owner or moderator/admin.

---

## 10. Feature Status Tracker

| Feature | Backend | Frontend | Tests | Docs |
|---|---|---|---|---|
| Project Foundation | ✅ | ✅ | ✅ | ✅ |
| User Registration | ✅ | ✅ | ✅ | ✅ |
| User Login | ✅ | ✅ | ✅ | ✅ |
| User Logout | ✅ | ✅ | ✅ | ✅ |
| Token Refresh | ✅ | ✅ | ✅ | ✅ |
| User Profile | ✅ | ✅ | ✅ | ✅ |
| Avatar Upload | ✅ | ✅ | ⬜ | ✅ |
| Forum Posts (CRUD) | ✅ | ✅ | ✅ | ✅ |
| Post Search | ✅ | ✅ | ✅ | ✅ |
| Author Filter (Search) | ✅ | ✅ | ✅ | ✅ |
| Redis Caching (posts) | ✅ | N/A | ✅ | ✅ |
| Answers (CRUD) | ✅ | ✅ | ✅ | ✅ |
| Voting (posts + answers) | ✅ | ✅ | ✅ | ✅ |
| Admin Moderation (block/unblock) | ✅ | ✅ | ✅ | ✅ |
| Tags/Categories | ⬜ | ⬜ | ⬜ | ⬜ |

---

## 11. Database Schema Tracker

| Table | Status | Description |
|---|---|---|
| `users` | ✅ Done | User accounts (id, email, username, hashed_password, role, avatar_url, bio, is_active, created_at, updated_at) |
| `posts` | ✅ Done | Forum threads (id, title, content, author_id FK→users, created_at, updated_at) |
| `answers` | ✅ Done | Answers to posts (id, content, author_id FK→users, post_id FK→posts, created_at, updated_at) |
| `votes` | ✅ Done | Votes on posts or answers — polymorphic via nullable post_id/answer_id, vote_type enum (up/down), UniqueConstraints per (user,post) and (user,answer) |
| `moderation_logs` | ✅ Done | Admin actions (id, admin_id FK→users nullable, action enum, target_user_id, reason, created_at) |
| `tags` | ⬜ Pending | Post tags |
| `post_tags` | ⬜ Pending | Many-to-many join |

**Migrations:**
- `0001_create_users_and_posts.py`
- `0002_add_answers.py`
- `0003_add_votes.py` — also creates `vote_type` PostgreSQL enum
- `0004_add_moderation_logs.py` — also creates `moderation_action` PostgreSQL enum

Run migrations: `cd backend && alembic upgrade head`

---

## 12. API Endpoint Tracker

| Method | Path | Auth | Status | Description |
|---|---|---|---|---|
| GET | `/api/v1/health` | None | ✅ | Health check |
| POST | `/api/v1/auth/register` | None | ✅ | Register new user |
| POST | `/api/v1/auth/login` | None | ✅ | Login — sets HttpOnly cookies |
| POST | `/api/v1/auth/logout` | None | ✅ | Logout — clears cookies |
| POST | `/api/v1/auth/refresh` | Cookie | ✅ | Refresh access token |
| GET | `/api/v1/users/me` | Cookie | ✅ | Get own profile + post_count |
| PATCH | `/api/v1/users/me` | Cookie | ✅ | Update username/bio |
| POST | `/api/v1/users/me/avatar` | Cookie | ✅ | Upload avatar image |
| GET | `/api/v1/posts` | None | ✅ | List posts (paginated, searchable, Redis cached) |
| POST | `/api/v1/posts` | Cookie | ✅ | Create post |
| GET | `/api/v1/posts/{id}` | Optional | ✅ | Get single post (Redis cached for anon; user_vote for auth) |
| PUT | `/api/v1/posts/{id}` | Cookie | ✅ | Update post (owner or mod+) |
| DELETE | `/api/v1/posts/{id}` | Cookie | ✅ | Delete post (owner or mod+) |
| POST | `/api/v1/posts/{id}/vote` | Cookie | ✅ | Vote on post (toggle: same type removes vote) |
| DELETE | `/api/v1/posts/{id}/vote` | Cookie | ✅ | Remove vote from post |
| GET | `/api/v1/posts/{id}/answers` | None | ✅ | List answers for a post |
| POST | `/api/v1/posts/{id}/answers` | Cookie | ✅ | Add answer to post |
| PUT | `/api/v1/answers/{id}` | Cookie | ✅ | Update answer (owner only) |
| DELETE | `/api/v1/answers/{id}` | Cookie | ✅ | Delete answer (owner or mod+) |
| POST | `/api/v1/answers/{id}/vote` | Cookie | ✅ | Vote on answer |
| DELETE | `/api/v1/answers/{id}/vote` | Cookie | ✅ | Remove vote from answer |
| POST | `/api/v1/admin/users/{id}/block` | Cookie (admin) | ✅ | Block user |
| POST | `/api/v1/admin/users/{id}/unblock` | Cookie (admin) | ✅ | Unblock user |
| GET | `/api/v1/admin/logs` | Cookie (admin) | ✅ | List moderation logs |

### Query Params for `GET /api/v1/posts`
| Param | Type | Description |
|---|---|---|
| `search` | string | Text search in title + content (ILIKE) |
| `author` | string | Filter by author username (ILIKE) |
| `date_from` | date (YYYY-MM-DD) | Filter posts created on or after |
| `date_to` | date (YYYY-MM-DD) | Filter posts created on or before |
| `page` | int (≥1) | Page number (default: 1) |
| `page_size` | int (1–100) | Items per page (default: 20) |

### Response Headers
| Header | Endpoints | Value |
|---|---|---|
| `X-Cache` | GET /posts, GET /posts/{id} | `HIT` or `MISS` |
| `X-Response-Time` | All | Duration in ms (e.g. `12.3ms`) |

---

## 13. Component Tracker

| Component | Path | Status | Description |
|---|---|---|---|
| `Layout` | `components/layout/Layout.tsx` | ✅ | Main page wrapper |
| `Navbar` | `components/layout/Navbar.tsx` | ✅ | Auth-aware top nav |
| `Footer` | `components/layout/Footer.tsx` | ✅ | Page footer |
| `PageContainer` | `components/common/PageContainer.tsx` | ✅ | Centered content wrapper |
| `ProtectedRoute` | `components/guards/ProtectedRoute.tsx` | ✅ | Auth gate (uses useAuth internally) |
| `RoleGuard` | `components/guards/RoleGuard.tsx` | ✅ | Role gate (uses useAuth internally) |
| `LoginForm` | `components/auth/LoginForm.tsx` | ✅ | Email+password login form |
| `RegisterForm` | `components/auth/RegisterForm.tsx` | ✅ | Registration form |
| `AvatarDropdown` | `components/user/AvatarDropdown.tsx` | ✅ | Profile/logout avatar menu |
| `PostCard` | `components/posts/PostCard.tsx` | ✅ | Post list card |
| `PostForm` | `components/posts/PostForm.tsx` | ✅ | Create/edit post form |
| `SearchBar` | `components/posts/SearchBar.tsx` | ✅ | Text + author + date range search |
| `VoteButtons` | `components/posts/VoteButtons.tsx` | ✅ | Up/down vote buttons with toggle, score display |
| `AnswerCard` | `components/answers/AnswerCard.tsx` | ✅ | Single answer: content, author, inline edit, vote buttons |
| `AnswerForm` | `components/answers/AnswerForm.tsx` | ✅ | RHF+Zod form for adding/editing answers |
| `AnswerList` | `components/answers/AnswerList.tsx` | ✅ | Fetches + displays all answers; manages mutations |

---

## 14. Reusable Utilities Tracker

### Backend
| Utility | Path | Description |
|---|---|---|
| `ApiResponse` | `fastapi_app/utils/responses.py` | Standard success response |
| `ApiError` | `fastapi_app/utils/responses.py` | Standard error response |
| `BaseService` | `fastapi_app/services/base.py` | Abstract service base |
| `BaseRepository` | `fastapi_app/repositories/base.py` | Abstract repository base |
| `JWTHandler` | `fastapi_app/core/security.py` | JWT create/verify |
| `PasswordHandler` | `fastapi_app/core/security.py` | bcrypt hash/verify |
| `ExceptionMiddleware` | `fastapi_app/middleware/exception.py` | Global error handler |
| `cache_get/set/delete` | `fastapi_app/core/cache.py` | Redis async cache helpers |
| `UserRole` / `ROLE_LEVELS` | `fastapi_app/enums.py` | Role enum + level map |

### Frontend
| Utility | Path | Description |
|---|---|---|
| `ApiClient` | `src/api/client.ts` | Axios instance + auto-refresh interceptor |
| `ApiService` | `src/api/service.ts` | Centralized API wrapper |
| `authService` | `src/services/authService.ts` | Auth API calls |
| `userService` | `src/services/userService.ts` | Profile API calls |
| `postService` | `src/services/postService.ts` | Post API calls |
| `answerService` | `src/services/answerService.ts` | Answer CRUD API calls |
| `voteService` | `src/services/voteService.ts` | Vote/remove-vote API calls for posts and answers |
| `adminService` | `src/services/adminService.ts` | Admin block/unblock API calls |
| `useAuth` | `src/hooks/useAuth.ts` | Hook for auth context |
| `AuthContext` | `src/store/AuthContext.tsx` | Auth state + provider |
| `errorHandler` | `src/utils/errorHandler.ts` | Parse + format errors |
| `notificationService` | `src/utils/notificationService.ts` | Toast notifications |

---

## 15. Deployment Notes

- Backend runs on port `8080` (host) → `8000` (container).
- Frontend dev server: port `5173` (Vite) or `3001` (Docker).
- PostgreSQL: port `5432` (container) → `5433` (host).
- Static files served from `backend/static/` at `/static/`.
- Avatars stored at `backend/static/avatars/{user_id}.{ext}`.
- All secrets via `.env` file (never committed).
- **Run DB migrations before starting API:** `alembic upgrade head`

### Environment Variables Required
| Variable | Example |
|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://user:pass@localhost:5432/forum_db` |
| `JWT_SECRET_KEY` | Random 32+ char string |
| `APP_SECRET_KEY` | Random 32+ char string |
| `CORS_ALLOWED_ORIGINS` | `["http://localhost:5173"]` (JSON array) |
| `REDIS_URL` | `redis://localhost:6379/0` |
