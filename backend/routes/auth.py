from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from pydantic import ValidationError
from backend.models import db, User
from backend.schemas import SignupRequest, LoginRequest

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = SignupRequest(**request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    if User.query.filter_by(email=data.email).first():
        return jsonify({'error': 'Email already registered'}), 409

    user = User(email=data.email)
    user.set_password(data.password)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'Signup successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = LoginRequest(**request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    user = User.query.filter_by(email=data.email).first()
    if not user or not user.check_password(data.password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user.to_dict()), 200
