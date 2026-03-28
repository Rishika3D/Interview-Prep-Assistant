from backend.models import db
from datetime import datetime

class Attempt(db.Model):
    __tablename__ = 'attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_answer = db.Column(db.Text, nullable=False)
    ai_feedback = db.Column(db.Text)
    score = db.Column(db.Integer)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'user_answer': self.user_answer,
            'ai_feedback': self.ai_feedback,
            'score': self.score,
            'created_at': self.created_at.isoformat()
        }
