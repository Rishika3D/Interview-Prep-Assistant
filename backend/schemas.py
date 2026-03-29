from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal

VALID_CATEGORIES = {'General', 'System Design', 'Behavioral', 'Technical', 'Leadership'}
VALID_DIFFICULTIES = {'Easy', 'Medium', 'Hard'}

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=255)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class QuestionCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=500)
    content: str = Field(..., min_length=10)
    expected_answer: Optional[str] = None
    category: str = Field(default='General', max_length=100)
    difficulty: str = Field(default='Medium')

    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        if v not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of: {', '.join(sorted(VALID_CATEGORIES))}")
        return v

    @field_validator('difficulty')
    @classmethod
    def validate_difficulty(cls, v):
        if v not in VALID_DIFFICULTIES:
            raise ValueError(f"difficulty must be one of: {', '.join(sorted(VALID_DIFFICULTIES))}")
        return v

class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    expected_answer: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None

    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        if v is not None and v not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of: {', '.join(sorted(VALID_CATEGORIES))}")
        return v

    @field_validator('difficulty')
    @classmethod
    def validate_difficulty(cls, v):
        if v is not None and v not in VALID_DIFFICULTIES:
            raise ValueError(f"difficulty must be one of: {', '.join(sorted(VALID_DIFFICULTIES))}")
        return v

class AttemptCreate(BaseModel):
    question_id: int
    user_answer: str = Field(..., min_length=10)

class AttemptResponse(BaseModel):
    score: int
    feedback: str
    strengths: list
    improvements: list
