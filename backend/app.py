from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
import logging

load_dotenv()

from backend.config import Config
from backend.models import db
from backend.routes.auth import auth_bp
from backend.routes.questions import questions_bp
from backend.routes.attempts import attempts_bp

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(attempts_bp)

    # Log every request
    @app.before_request
    def log_request():
        logger.info(f"→ {request.method} {request.path}")

    @app.after_request
    def log_response(response):
        logger.info(f"← {response.status_code} {request.method} {request.path}")
        return response

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404 Not Found: {request.path}")
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 Internal Error: {error}", exc_info=True)
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

    # Create tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables ready")

    return app

if __name__ == '__main__':
    app = create_app()
    logger.info("Starting Interview Prep API on port 5005")
    app.run(debug=True, port=5005)
