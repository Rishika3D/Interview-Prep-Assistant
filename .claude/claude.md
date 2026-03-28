# Interview Prep Assistant - AI Guidance

## Project Overview
A full-stack application for practicing interview questions with AI-powered feedback. Users can:
- Create and manage interview questions
- Practice answering questions
- Receive AI-generated feedback with scores and improvement suggestions

## Architecture
- **Backend**: Python Flask API with SQLAlchemy ORM, SQLite database
- **Frontend**: React SPA with Axios for API calls
- **AI**: Claude API for evaluating interview answers

## Code Standards & Practices

### Backend (Python/Flask)
- Use **type hints** on all function signatures
- Use **Pydantic schemas** for request validation (never trust frontend data)
- All database operations should be wrapped in proper error handling
- Use **JWT tokens** for stateless authentication
- All passwords hashed with bcrypt before storage
- Validate user ownership before returning/modifying any resource

### Frontend (React)
- Use **React hooks** (useState, useEffect, useContext)
- Keep components small and focused (single responsibility)
- Use CSS modules or scoped CSS for styling
- Always set proper error boundaries
- Never store tokens in sessionStorage (use localStorage only)
- Always verify token exists before making authenticated requests

### Database
- Use CASCADE deletes for user data integrity
- All timestamps use UTC (datetime.utcnow)
- Foreign keys must be enforced
- No sensitive data in plain text

## AI Integration Rules

### When Using Claude API:
1. **Always wrap API calls** in try-catch blocks
2. **Parse responses carefully** - Claude's output might not be valid JSON, use fallback values
3. **Never expose raw API responses** to frontend users
4. **Log all API calls** with question context for debugging
5. **Rate limit thoughtfully** - feedback generation costs API calls
6. **Validate feedback** - ensure it's constructive and doesn't change question meaning

### Feedback Generation
The `AIFeedbackService.evaluate_answer()` method:
- Takes: question text, expected answer, user answer
- Returns: score (0-100), feedback text, strengths list, improvements list
- Response format is validated before returning to user
- Fallback values provided if API fails

## Security Checklist
- [ ] All user inputs validated with Pydantic schemas
- [ ] Passwords hashed with bcrypt (never logged)
- [ ] JWT tokens validated on every protected route
- [ ] CORS properly configured (not `*`)
- [ ] Database queries use parameterized statements (SQLAlchemy)
- [ ] User can only see/edit their own questions and attempts
- [ ] Error messages don't leak sensitive information

## Testing Strategy
- Test authentication flows (signup, login, token validation)
- Test CRUD operations on questions (verify ownership)
- Test AI feedback endpoint with mocked Claude responses
- Test validation schemas with invalid inputs
- Test cascade deletes (deleting user removes questions/attempts)

## Extension Points
1. **Analytics**: Track score trends, weak question categories
2. **Question Variations**: AI generates alternative phrasings for practice
3. **Study Guides**: AI creates personalized study guides based on weaknesses
4. **Export**: Generate PDF reports of performance
5. **Collaboration**: Share questions with study groups
6. **Spaced Repetition**: Smart scheduling of question reviews

## AI Usage in This Project
- **Claude API** evaluates interview answers against expected responses
- **Structured prompts** ensure consistent JSON responses
- **Fallback handling** for API failures prevents crashes
- **Cost optimization** - consider caching scores for repeated answers

## Files Structure
```
backend/
  models/          # Database models (User, Question, Attempt)
  routes/          # Flask blueprints (auth, questions, attempts)
  services/        # Business logic (AIFeedbackService)
  schemas.py       # Pydantic validation schemas
  config.py        # Configuration management
  app.py           # Flask app factory

frontend/src/
  components/      # React components (Auth, Dashboard, etc)
  hooks/           # Custom React hooks (useAuth)
  services/        # API client (api.js)
  App.jsx          # Root component
```

## Known Limitations & Trade-offs
1. SQLite for simplicity (not production-ready)
2. No rate limiting on API endpoints
3. AI feedback requires valid API key
4. No caching of feedback responses
5. Simple auth (JWT, no refresh tokens)
