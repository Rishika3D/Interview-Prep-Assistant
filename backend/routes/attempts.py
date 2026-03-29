from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from backend.models import db, Attempt, Question
from backend.schemas import AttemptCreate
from backend.services.ai_feedback import AIFeedbackService

attempts_bp = Blueprint('attempts', __name__, url_prefix='/api/attempts')
ai_service = AIFeedbackService()

@attempts_bp.route('', methods=['POST'])
@jwt_required()
def submit_attempt():
    user_id = get_jwt_identity()
    try:
        data = AttemptCreate(**request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    question = Question.query.filter_by(id=data.question_id, user_id=user_id).first()
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    # Get AI feedback (category-aware prompt selection)
    feedback_result = ai_service.evaluate_answer(
        question=question.content,
        expected_answer=question.expected_answer or "Not specified",
        user_answer=data.user_answer,
        category=question.category
    )

    attempt = Attempt(
        user_id=user_id,
        question_id=data.question_id,
        user_answer=data.user_answer,
        ai_feedback=feedback_result.get('feedback'),
        score=feedback_result.get('score', 0)
    )
    db.session.add(attempt)
    db.session.commit()

    return jsonify({
        'attempt_id': attempt.id,
        'score': feedback_result.get('score'),
        'feedback': feedback_result.get('feedback'),
        'strengths': feedback_result.get('strengths', []),
        'improvements': feedback_result.get('improvements', [])
    }), 201

@attempts_bp.route('/<int:attempt_id>', methods=['GET'])
@jwt_required()
def get_attempt(attempt_id):
    user_id = get_jwt_identity()
    attempt = Attempt.query.filter_by(id=attempt_id, user_id=user_id).first()

    if not attempt:
        return jsonify({'error': 'Attempt not found'}), 404

    return jsonify(attempt.to_dict()), 200

@attempts_bp.route('/question/<int:question_id>', methods=['GET'])
@jwt_required()
def get_question_attempts(question_id):
    user_id = get_jwt_identity()
    question = Question.query.filter_by(id=question_id, user_id=user_id).first()

    if not question:
        return jsonify({'error': 'Question not found'}), 404

    attempts = Attempt.query.filter_by(question_id=question_id, user_id=user_id).all()
    return jsonify([a.to_dict() for a in attempts]), 200
