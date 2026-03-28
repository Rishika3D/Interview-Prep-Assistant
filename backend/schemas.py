from pydantic import BaseModel, EmailStr, Field
from typing import Optional

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

class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    expected_answer: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None

class AttemptCreate(BaseModel):
    question_id: int
    user_answer: str = Field(..., min_length=10)

class AttemptResponse(BaseModel):
    score: int
    feedback: str
    strengths: list
    improvements: list
