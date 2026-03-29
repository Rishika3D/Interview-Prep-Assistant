# Interview Prep Assistant

An AI-powered interview preparation platform where users build a personal question bank, practice answering questions, and receive instant structured feedback — scored 0–100 with strengths and improvement areas — powered by Groq (Llama 3.3 70B).

**Stack:** Python · Flask · SQLite · React · Vite · JWT · Pydantic · Groq AI · Pytest

---

## What It Does

| Feature | Description |
|---|---|
| Question Bank | Create, edit, delete questions across 5 categories |
| Practice Mode | Type your answer and get AI feedback in seconds |
| Category-Aware AI | System Design questions evaluated on architecture; Behavioral on STAR method |
| Score History | Every attempt saved — track improvement over time |
| User Isolation | Each user sees only their own questions and attempts |
| Seed Questions | 9 pre-built questions across System Design, Behavioral, and Technical |

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- [Groq API key](https://console.groq.com) (free)

### 1. Clone & configure

```bash
git clone <repo-url>
cd interview-prep-assessment

cp .env.example .env
# Open .env and fill in your GROQ_API_KEY and a JWT_SECRET_KEY
```

### 2. Backend

```bash
python3.11 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r backend/requirements.txt
python -m backend.app         # starts on http://localhost:5005
```

### 3. Seed sample questions (optional)

```bash
python -m backend.seed
# Creates demo@example.com / demo123 with 9 pre-built questions
```

### 4. Frontend

```bash
cd frontend
npm install
npm run dev                   # starts on http://localhost:3000
```

Open `http://localhost:3000` — the Vite proxy forwards all `/api` calls to Flask on 5005.

---

## Running Tests

```bash
source venv/bin/activate
pytest backend/tests/ -v
```

Tests use an **in-memory SQLite database** and **mock the Groq API** — no real API key needed. 20 tests covering auth, CRUD, user isolation, and feedback submission.

```
backend/tests/
├── conftest.py        # fixtures, in-memory DB, helper functions
├── test_auth.py       # signup, login, token validation, edge cases
├── test_questions.py  # CRUD, category/difficulty validation, user isolation
└── test_attempts.py   # feedback submission, cross-user access denied
```

---

## Architecture

```
React (port 3000)
    │  /api/* → Vite proxy
    ▼
Flask (port 5005)
    ├── routes/auth.py        POST /api/auth/signup|login   GET /api/auth/me
    ├── routes/questions.py   GET|POST /api/questions        GET|PUT|DELETE /api/questions/<id>
    └── routes/attempts.py    POST /api/attempts             GET /api/attempts/<id|question/id>
         │
         ├── schemas.py       Pydantic validates every request before DB touch
         ├── models/          SQLAlchemy ORM (User → Questions → Attempts)
         └── services/
              └── ai_feedback.py   Groq API call, category-aware prompt, JSON parse + fallback
                   │
                   ▼
              Groq API (Llama 3.3 70B)
```

### Database Schema

```
users         (id, email, password_hash, created_at)
  └── questions (id, user_id→FK, title, content, expected_answer, category, difficulty, timestamps)
        └── attempts (id, user_id→FK, question_id→FK, user_answer, ai_feedback, score, created_at)
```

Cascade deletes: removing a user removes their questions; removing a question removes its attempts.

---

## Key Technical Decisions

### 1. Flask App Factory Pattern
`create_app()` in `app.py` initialises extensions, registers blueprints, and wires error handlers in one place. Makes testing easy — the test suite creates a fresh app instance with an in-memory DB.

### 2. Pydantic Schemas at the Boundary
Every POST/PUT request is validated by a Pydantic schema before touching the database. `category` and `difficulty` are validated against allowed value sets. Invalid requests fail fast with a clear 400 error — the database never sees bad data.

```python
VALID_CATEGORIES = {'General', 'System Design', 'Behavioral', 'Technical', 'Leadership'}
VALID_DIFFICULTIES = {'Easy', 'Medium', 'Hard'}
```

### 3. Category-Aware AI Prompts
The AI evaluation strategy changes based on question category:

| Category | Evaluation focus |
|---|---|
| System Design | Requirements, scale estimation, architecture, DB choices, caching, trade-offs |
| Behavioral | STAR method, specificity, quantified impact |
| General/Technical | Accuracy, completeness, clarity |

This is a single `if/elif` branch in `AIFeedbackService.evaluate_answer()` — easy to extend with new categories.

### 4. User Isolation Enforced at Every Query
Every query that reads or mutates data includes `filter_by(user_id=user_id)`. There is no way for User A to read, edit, or delete User B's questions or attempts — even with a valid JWT token.

```python
question = Question.query.filter_by(id=question_id, user_id=user_id).first()
# Returns 404 if question exists but belongs to a different user
```

### 5. SQLite → PostgreSQL in One Line
The database URI comes from an env var. Switching to Postgres in production is:
```bash
DATABASE_URL=postgresql://user:pass@host/db
```
No code changes needed.

### 6. AI Decoupled in a Service Layer
`AIFeedbackService` is the only file that knows about Groq. Routes call `ai_service.evaluate_answer(...)` and get back a plain dict. Swapping Groq for any other LLM means changing one file, nothing else.

### 7. Axios Interceptors for Token Management
The frontend uses an Axios request interceptor to attach the JWT token on every request (reading fresh from localStorage, not stale from module load). A response interceptor clears the token automatically on 401/422 to prevent infinite auth loops.

---

## AI Usage in This Project

### How AI was used
Claude (Claude Code) was used to scaffold components, write boilerplate routes, and generate test fixtures. All generated code was reviewed before use.

### What was caught and fixed in review
- **User isolation bug**: Generated `get_question_attempts()` returned all attempts for a question without filtering by `user_id`. Fixed by adding `filter_by(user_id=user_id)`.
- **Stale token bug**: Generated `api.js` read the JWT token once at module load — stale after login. Fixed by moving to a request interceptor.
- **Silent AI failures**: Generated fallback returned a hardcoded score with no logging. Fixed by adding `logger.error()` with the raw response for diagnosis.

### AI guidance file
`.claude/claude.md` constrains the AI with explicit rules:
- Always validate with Pydantic before touching the DB
- Always filter by `user_id` on every query
- Always log errors with context before returning fallbacks
- Never expose password hashes in API responses

---

## Observability

Every request and response is logged:

```
2026-03-29 14:22:01 [INFO]  → POST /api/attempts
2026-03-29 14:22:01 [INFO]  Requesting AI evaluation — category=System Design model=llama-3.3-70b-versatile
2026-03-29 14:22:03 [INFO]  AI evaluation complete — score=78
2026-03-29 14:22:03 [INFO]  ← 201 POST /api/attempts
```

AI failures log the raw response for diagnosis:
```
2026-03-29 14:22:03 [ERROR] Failed to parse AI response as JSON: ... Raw response: ...
```

---

## Security Checklist

- [x] Passwords hashed with bcrypt (never stored plain)
- [x] JWT tokens verified on every protected route
- [x] User isolation enforced at every DB query
- [x] Pydantic rejects invalid input before DB access
- [x] SQLAlchemy ORM prevents SQL injection
- [x] CORS enabled (not wildcard)
- [x] Error responses never leak stack traces or internal details
- [x] `.env` excluded from git via `.gitignore`

---

## API Reference

### Auth
```
POST  /api/auth/signup     { email, password }           → { access_token, user }
POST  /api/auth/login      { email, password }           → { access_token, user }
GET   /api/auth/me         [JWT required]                → { user }
```

### Questions
```
GET   /api/questions              [JWT]  → [ questions ]
POST  /api/questions              [JWT]  { title, content, category, difficulty, expected_answer }
GET   /api/questions/<id>         [JWT]  → question
PUT   /api/questions/<id>         [JWT]  { ...fields to update }
DELETE /api/questions/<id>        [JWT]
```

### Attempts
```
POST  /api/attempts               [JWT]  { question_id, user_answer }  → { score, feedback, strengths, improvements }
GET   /api/attempts/<id>          [JWT]  → attempt
GET   /api/attempts/question/<id> [JWT]  → [ attempts ]
```

---

## Known Limitations & Production Path

| Limitation | Production fix |
|---|---|
| SQLite (no concurrent writes) | Switch `DATABASE_URL` to PostgreSQL |
| No rate limiting | Add Flask-Limiter on `/api/attempts` |
| JWT only (no refresh tokens) | Add refresh token endpoint |
| No email verification | Add SendGrid/Resend on signup |
| AI responses not cached | Cache identical question+answer pairs in Redis |
| No DB migrations | Add Alembic for schema versioning |

---

## Potential Extensions

1. **Spaced Repetition** — resurface questions where score < 70 after N days
2. **Mock Interview Sessions** — timed sessions with multiple questions in sequence
3. **Analytics Dashboard** — score trends by category, weakest topics
4. **AI Question Generator** — generate question variants from a seed question
5. **Export to PDF** — download performance report for a session

---

## Project Structure

```
interview-prep-assessment/
├── backend/
│   ├── models/
│   │   ├── __init__.py        SQLAlchemy db instance
│   │   ├── user.py            User model, bcrypt hashing
│   │   ├── question.py        Question model
│   │   └── attempt.py         Attempt model (stores AI feedback + score)
│   ├── routes/
│   │   ├── auth.py            Signup, login, /me
│   │   ├── questions.py       Question CRUD + auto-seed on first login
│   │   └── attempts.py        Submit answer, get AI feedback
│   ├── services/
│   │   └── ai_feedback.py     Groq API, category-aware prompts, fallback handling
│   ├── tests/
│   │   ├── conftest.py        Fixtures, in-memory DB, helpers
│   │   ├── test_auth.py       Auth flow tests
│   │   ├── test_questions.py  CRUD + isolation tests
│   │   └── test_attempts.py   Feedback + isolation tests (AI mocked)
│   ├── app.py                 Flask factory, logging, error handlers
│   ├── config.py              Config from env vars
│   ├── schemas.py             Pydantic request schemas + validators
│   ├── seed.py                Demo user + 9 sample questions
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── Auth.jsx       Login / signup forms
│       │   ├── Dashboard.jsx  Question list, filters
│       │   ├── QuestionCard.jsx
│       │   ├── QuestionForm.jsx
│       │   └── PracticeMode.jsx  Answer input, system design guide, feedback display
│       ├── hooks/useAuth.js   Auth state management
│       ├── services/api.js    Axios client with JWT interceptors
│       └── App.jsx
├── .claude/
│   └── claude.md              AI coding constraints and standards
├── .env.example
└── README.md
```

---

## Demo

Log in as the demo user (after running `python -m backend.seed`):

```
Email:    demo@example.com
Password: demo123
```

Then: pick any System Design question → click Practice → write a rough answer → see the AI evaluate it across architecture, scalability, and trade-offs.
