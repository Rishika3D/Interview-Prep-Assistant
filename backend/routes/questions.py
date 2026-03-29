from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from backend.models import db, Question
from backend.schemas import QuestionCreate, QuestionUpdate

questions_bp = Blueprint('questions', __name__, url_prefix='/api/questions')

from backend.seed import SAMPLE_QUESTIONS

@questions_bp.route('', methods=['GET'])
@jwt_required()
def list_questions():
    user_id = get_jwt_identity()
    user_questions = Question.query.filter_by(user_id=user_id).all()
    
    mock_questions_data = []
    for q in SAMPLE_QUESTIONS:
        mock = dict(q)
        if not mock['title'].startswith('Mock Question: '):
            mock['title'] = "Mock Question: " + mock['title']
        mock_questions_data.append(mock)

    mock_titles = [m['title'] for m in mock_questions_data]
    existing_mock_titles = {q.title for q in user_questions if q.title in mock_titles}
    
    new_mocks_added = False
    for mock in mock_questions_data:
        if mock['title'] not in existing_mock_titles:
            q = Question(user_id=user_id, **mock)
            db.session.add(q)
            new_mocks_added = True
            
    if new_mocks_added:
        db.session.commit()
        user_questions = Question.query.filter_by(user_id=user_id).all()
        
    return jsonify([q.to_dict() for q in user_questions]), 200

@questions_bp.route('', methods=['POST'])
@jwt_required()
def create_question():
    user_id = get_jwt_identity()
    try:
        data = QuestionCreate(**request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    question = Question(
        user_id=user_id,
        title=data.title,
        content=data.content,
        expected_answer=data.expected_answer,
        category=data.category,
        difficulty=data.difficulty
    )
    db.session.add(question)
    db.session.commit()

    return jsonify(question.to_dict()), 201

@questions_bp.route('/<int:question_id>', methods=['GET'])
@jwt_required()
def get_question(question_id):
    user_id = get_jwt_identity()
    question = Question.query.filter_by(id=question_id, user_id=user_id).first()

    if not question:
        return jsonify({'error': 'Question not found'}), 404

    return jsonify(question.to_dict()), 200

@questions_bp.route('/<int:question_id>', methods=['PUT'])
@jwt_required()
def update_question(question_id):
    user_id = get_jwt_identity()
    question = Question.query.filter_by(id=question_id, user_id=user_id).first()

    if not question:
        return jsonify({'error': 'Question not found'}), 404

    try:
        data = QuestionUpdate(**request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    if data.title:
        question.title = data.title
    if data.content:
        question.content = data.content
    if data.expected_answer:
        question.expected_answer = data.expected_answer
    if data.category:
        question.category = data.category
    if data.difficulty:
        question.difficulty = data.difficulty

    db.session.commit()
    return jsonify(question.to_dict()), 200

@questions_bp.route('/<int:question_id>', methods=['DELETE'])
@jwt_required()
def delete_question(question_id):
    user_id = get_jwt_identity()
    question = Question.query.filter_by(id=question_id, user_id=user_id).first()

    if not question:
        return jsonify({'error': 'Question not found'}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted'}), 200
