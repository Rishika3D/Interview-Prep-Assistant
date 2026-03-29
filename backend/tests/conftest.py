"""
Shared pytest fixtures for all tests.
Uses an in-memory SQLite DB so tests never touch the real database.
"""
import pytest
from backend.app import create_app
from backend.models import db as _db


@pytest.fixture(scope='session')
def app():
    """Create a Flask app configured for testing."""
    test_app = create_app()
    test_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret',
    })
    with test_app.app_context():
        _db.create_all()
        yield test_app
        _db.drop_all()


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    """Wipe all tables between tests so they don't interfere."""
    yield
    with app.app_context():
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()


# ── helpers ──────────────────────────────────────────────────────────────────

def register(client, email='test@example.com', password='password123'):
    return client.post('/api/auth/signup', json={'email': email, 'password': password})


def login(client, email='test@example.com', password='password123'):
    res = client.post('/api/auth/login', json={'email': email, 'password': password})
    return res.get_json().get('access_token')


def auth_header(token):
    return {'Authorization': f'Bearer {token}'}
