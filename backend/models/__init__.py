from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from backend.models.user import User
from backend.models.question import Question
from backend.models.attempt import Attempt

__all__ = ['db', 'User', 'Question', 'Attempt']
