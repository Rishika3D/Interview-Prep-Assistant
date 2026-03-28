# Interview Prep Assistant

An AI-powered interview preparation tool built with Python Flask, React, and Claude API. Users can create interview questions, practice answering them, and receive personalized AI-generated feedback.

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Anthropic API key

### Setup

1. **Clone and enter directory**
```bash
cd /Users/ashi/interview-prep-assessment
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
cp ../.env.example ../.env
# Edit .env and add your ANTHROPIC_API_KEY
python app.py
```

Backend runs on `http://localhost:5000`

3. **Frontend Setup** (in new terminal)
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

## Features

✅ **User Authentication**
- Sign up / Login with email
- JWT-based session management
- Password hashing with bcrypt

✅ **Question Management**
- Create interview questions with categories and difficulty levels
- Store expected answer key points
- Edit and delete questions

✅ **Practice Mode**
- Answer interview questions in real-time
- Get AI-powered feedback instantly
- Receive score, strengths, and improvement areas

✅ **Progress Tracking**
- View attempt history
- See feedback from previous attempts
- Track performance trends

## Technical Decisions

### Backend: Flask + SQLAlchemy
- **Why**: Lightweight, easy to understand, great for rapid prototyping
- **Trade-off**: Simple but not production-scaled; suitable for this assessment

### Database: SQLite
- **Why**: Zero setup, works locally, good for demos
- **Trade-off**: Not suitable for concurrent users or production; would migrate to PostgreSQL

### Authentication: JWT Tokens
- **Why**: Stateless, scalable, works well with SPAs
- **Implementation**: Tokens stored in localStorage, verified on each protected request
- **Trade-off**: No refresh token mechanism (fine for 24h assessment)

### AI Integration: Claude API
- **Why**: Superior reasoning ability for evaluating interview answers
- **Prompt Design**: Structured JSON output ensures reliable parsing
- **Fallback Handling**: Default values if API fails prevents crashes
- **Cost Control**: Direct API calls (no caching, potential optimization point)

### Validation: Pydantic Schemas
- **Why**: Type-safe request validation, clear error messages
- **Implementation**: All endpoints validate input before touching database
- **Benefit**: Prevents invalid states, clear contracts between frontend/backend

### Frontend: React + Vite
- **Why**: Modern, fast dev server, great DX
- **Styling**: CSS modules for component scoping
- **State**: React hooks for simplicity

## API Endpoints

### Auth
- `POST /api/auth/signup` - Create account
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Questions
- `GET /api/questions` - List user's questions
- `POST /api/questions` - Create question
- `GET /api/questions/<id>` - Get question
- `PUT /api/questions/<id>` - Update question
- `DELETE /api/questions/<id>` - Delete question

### Practice
- `POST /api/attempts` - Submit answer, get feedback
- `GET /api/attempts/<id>` - Get attempt details
- `GET /api/attempts/question/<id>` - Get all attempts for question

## AI Usage

### Feedback Generation Flow
1. User submits answer to a question
2. Backend sends to Claude: question + expected answer + user answer
3. Claude evaluates and returns: score (0-100), feedback, strengths, improvements
4. Response validated and stored
5. Formatted feedback returned to frontend

### Prompt Design
```
You are an expert interview coach evaluating a candidate's answer.

Question: [question text]
Expected/Ideal Answer Points: [key points]
Candidate's Answer: [user answer]

Evaluate the answer and respond with ONLY valid JSON:
{
    "score": <0-100>,
    "feedback": "<assessment>",
    "strengths": ["<strength 1>", "<strength 2>"],
    "improvements": ["<improvement 1>", "<improvement 2>"]
}
```

**Why this design**: Forces Claude into structured output, easy to parse, fallback handling for JSON errors.

## Security & Data Protection

- ✅ Passwords hashed with bcrypt before storage
- ✅ JWT tokens validated on protected routes
- ✅ User can only access their own questions/attempts
- ✅ CORS configured (not wildcard)
- ✅ Input validated with Pydantic schemas
- ✅ SQLAlchemy prevents SQL injection
- ✅ Error messages don't leak sensitive info

## Testing

Run backend tests:
```bash
cd backend
pytest tests/
```

Test coverage:
- Authentication flows
- Question CRUD operations
- Attempt submission and feedback
- Input validation
- User isolation

## Known Limitations

1. **SQLite**: Not suitable for concurrent users (would use PostgreSQL in production)
2. **No refresh tokens**: JWT tokens expire after 30 days
3. **No rate limiting**: API endpoints unlimited (should add in production)
4. **Sync-only**: No real-time updates (would use WebSockets)
5. **Simple auth**: No email verification or password recovery
6. **No AI response caching**: Every identical question re-evaluated (could optimize)

## Potential Extensions

1. **Analytics Dashboard**: Track score trends, weak categories
2. **AI-Generated Variations**: Ask Claude to create question variants for practice
3. **Study Guides**: Generate personalized study materials based on weaknesses
4. **Peer Learning**: Share questions, discuss answers
5. **Scheduled Reviews**: Spaced repetition of difficult questions
6. **Export to PDF**: Download performance reports

## AI Guidance Files

See `.claude/claude.md` for:
- Code standards and practices
- AI integration rules
- Security checklist
- Testing strategy
- Extension points

## File Structure

```
interview-prep-assessment/
├── backend/
│   ├── models/                # Database models
│   │   ├── user.py
│   │   ├── question.py
│   │   └── attempt.py
│   ├── routes/                # API endpoints
│   │   ├── auth.py
│   │   ├── questions.py
│   │   └── attempts.py
│   ├── services/              # Business logic
│   │   └── ai_feedback.py
│   ├── schemas.py             # Pydantic validation
│   ├── config.py
│   ├── app.py                 # Flask app factory
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── hooks/             # Custom hooks
│   │   ├── services/          # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── .claude/
│   └── claude.md              # AI guidance
├── .env.example
└── README.md
```

## Demo Flow

1. Sign up with test email
2. Create 2-3 interview questions
3. Click "Practice" on a question
4. Answer the question
5. View AI feedback with score and suggestions
6. Try again to improve score

## Attribution

This project demonstrates:
- Clean code architecture with separation of concerns
- Proper authentication and authorization
- AI integration with proper error handling
- Full-stack development with Python/React
- Type safety and validation
- Clear technical documentation

All code written specifically for this assessment.
