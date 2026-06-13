# CLAUDE.md — Project Rules & Conventions

This file is the **single source of truth** for how code is written and structured in this project.
Read this file **and** `DOCUMENTATION.md` before writing any new code or feature.

---

## 1. No Code Duplication

- Never duplicate logic. If you see the same code in two places, extract it.
- Reusable backend logic → `services/` or `repositories/`.
- Reusable frontend logic → `hooks/` or `utils/`.

---

## 2. Reusability Rules

| Layer | Rule |
|---|---|
| Backend logic | Must live in a `BaseService` or `BaseRepository` subclass |
| Frontend UI | Must be a reusable component in `components/` |
| API logic | Must go through the centralized `ApiService` |
| Validation | Must use shared Pydantic schemas (backend) or Zod schemas (frontend) |

---

## 3. File Size Limit

- **Maximum 1000 lines per file.**
- If a file approaches 1000 lines, split it into smaller focused modules immediately.
- This applies to both backend and frontend files.

---

## 4. SOLID Principles

- **S** — Single Responsibility: one class/function, one job.
- **O** — Open/Closed: extend behavior without modifying existing code.
- **L** — Liskov Substitution: subclasses must be substitutable for their base.
- **I** — Interface Segregation: small, focused interfaces only.
- **D** — Dependency Inversion: depend on abstractions, not concretions.

---

## 5. Clean Architecture

Layers (inner → outer):

```
Domain (models, schemas)
  ↑
Application (services, use cases)
  ↑
Infrastructure (repositories, DB, external APIs)
  ↑
Presentation (API endpoints, React components)
```

- Inner layers must never depend on outer layers.
- Dependencies always point inward.

---

## 6. TypeScript Strict Mode

- `strict: true` is enforced in `tsconfig.json`.
- No `any` types unless absolutely unavoidable and explicitly commented.
- No inline interface definitions inside component props.

### Component Declaration Rules

**Rule 1 — Components with props:** define a named `IComponentNameProps` interface and annotate with `FC<IProps>`.

❌ WRONG (inline interface):
```tsx
const UserCard: FC<{ name: string }> = ({ name }) => { ... }
```

✅ CORRECT:
```tsx
interface IUserCardProps {
  name: string;
}

const UserCard: FC<IUserCardProps> = ({ name }) => { ... }
```

**Rule 2 — Components with NO props:** use a plain arrow function — do NOT add `: FC`.

❌ WRONG:
```tsx
const Navbar: FC = () => { ... }
```

✅ CORRECT:
```tsx
const Navbar = () => { ... }
```

**Rule 3 — Page components** (files inside `pages/`) must use `export default`.

❌ WRONG:
```tsx
export const HomePage = () => { ... }
```

✅ CORRECT:
```tsx
const HomePage = () => { ... }
export default HomePage;
```

**Rule 4 — Non-page components** (layout, common, guards, store) use named exports (`export const`).

All interfaces must be named with the `I` prefix (e.g., `IUserCardProps`, `IApiResponse`).

---

## 7. API Requests — Centralized Only

- **All** API calls must go through the centralized `ApiClient` → `ApiService`.
- Pages and components must **never** import or call `axios` directly.
- Pages and components must **never** contain `try/catch` blocks for API calls.

**WRONG:**
```ts
// Inside a page component
const response = await axios.get('/api/users');
```

**CORRECT:**
```ts
// Inside a page component
const { data } = useQuery({ queryKey: ['users'], queryFn: () => userService.getAll() });
```

---

## 8. Centralized Error & Success Handling

- All error handling lives in `utils/errorHandler.ts`.
- All success notifications live in `utils/notificationService.ts`.
- The `ApiClient` wrapper handles `try/catch`, error parsing, and toast messages automatically.
- Custom error messages are supported via the `ApiService` options parameter.
- Components and pages must never handle API errors directly.

---

## 9. Feature Completeness Requirement

Every feature must include **all** of the following before being considered done:

- [ ] Backend implementation (service + repository + endpoint)
- [ ] Frontend implementation (page + components + service call)
- [ ] API tests (Pytest)
- [ ] Documentation update in `DOCUMENTATION.md`

---

## 10. Pre-Feature Checklist

Before writing code for any new feature:

1. Read `CLAUDE.md` (this file).
2. Read `DOCUMENTATION.md`.
3. Check `DOCUMENTATION.md` → Feature Status Tracker.
4. Check `DOCUMENTATION.md` → API Endpoint Tracker.
5. Check `DOCUMENTATION.md` → Component Tracker.
6. **Never scan the whole codebase** if documentation contains the needed information.

---

## 11. Backend Standards

- All endpoints return `ApiResponse` or `ApiError`.
- Services extend `BaseService`.
- Repositories extend `BaseRepository`.
- Pydantic schemas live in `schemas/`.
- No business logic in endpoints — only in services.
- No raw SQL in services — only in repositories.

---

## 12. Frontend Standards

- No inline styles (use MUI `sx` prop or `theme`).
- No magic strings for routes — use route constants from `router/routes.ts`.
- No direct `localStorage` / `sessionStorage` access outside `utils/storage.ts`.
- All forms use `React Hook Form` + `Zod` schemas.
- All data fetching uses `React Query`.

---

## 13. Security Rules

- JWT stored in `HttpOnly` cookies only — never `localStorage`.
- Never log sensitive data (passwords, tokens).
- All inputs validated on both frontend (Zod) and backend (Pydantic).
- CORS configured strictly — no wildcard in production.

---

## 14. Naming Conventions

| Context | Convention | Example |
|---|---|---|
| Python files | snake_case | `user_service.py` |
| Python classes | PascalCase | `UserService` |
| TS/TSX files | PascalCase for components | `UserCard.tsx` |
| TS utility files | camelCase | `errorHandler.ts` |
| TS interfaces | IPascalCase | `IUserCardProps` |
| TS types | TPascalCase | `TApiResponse` |
| CSS class names | kebab-case | `user-card` |
| API routes | kebab-case | `/api/v1/forum-posts` |
| DB table names | snake_case plural | `forum_posts` |
