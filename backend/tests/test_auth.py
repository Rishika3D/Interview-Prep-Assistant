"""
Tests for /api/auth — signup and login flows.
"""
from .conftest import register, login, auth_header


class TestSignup:
    def test_signup_success(self, client):
        res = register(client)
        assert res.status_code == 201
        assert 'access_token' in res.get_json()

    def test_signup_duplicate_email(self, client):
        register(client)
        res = register(client)  # same email again
        assert res.status_code == 409

    def test_signup_invalid_email(self, client):
        res = client.post('/api/auth/signup', json={
            'email': 'not-an-email',
            'password': 'password123'
        })
        assert res.status_code == 400

    def test_signup_password_too_short(self, client):
        res = client.post('/api/auth/signup', json={
            'email': 'a@b.com',
            'password': '123'  # min is 6
        })
        assert res.status_code == 400

    def test_signup_missing_fields(self, client):
        res = client.post('/api/auth/signup', json={})
        assert res.status_code == 400


class TestLogin:
    def test_login_success(self, client):
        register(client)
        res = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        assert res.status_code == 200
        assert 'access_token' in res.get_json()

    def test_login_wrong_password(self, client):
        register(client)
        res = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        assert res.status_code == 401

    def test_login_unknown_email(self, client):
        res = client.post('/api/auth/login', json={
            'email': 'nobody@example.com',
            'password': 'password123'
        })
        assert res.status_code == 401

    def test_protected_route_requires_token(self, client):
        res = client.get('/api/questions')
        assert res.status_code == 401
