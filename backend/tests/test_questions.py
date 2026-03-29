"""
Tests for /api/questions — CRUD and validation.
"""
from .conftest import register, login, auth_header

VALID_QUESTION = {
    'title': 'Design a URL shortener',
    'content': 'How would you design a scalable URL shortening service?',
    'category': 'System Design',
    'difficulty': 'Medium',
}


def setup_user(client, email='user@example.com'):
    register(client, email=email)
    token = login(client, email=email)
    return auth_header(token)


class TestCreateQuestion:
    def test_create_success(self, client):
        headers = setup_user(client)
        res = client.post('/api/questions', json=VALID_QUESTION, headers=headers)
        assert res.status_code == 201
        data = res.get_json()
        assert data['title'] == VALID_QUESTION['title']
        assert data['category'] == 'System Design'

    def test_create_invalid_category(self, client):
        headers = setup_user(client)
        q = {**VALID_QUESTION, 'category': 'NotARealCategory'}
        res = client.post('/api/questions', json=q, headers=headers)
        assert res.status_code == 400

    def test_create_invalid_difficulty(self, client):
        headers = setup_user(client)
        q = {**VALID_QUESTION, 'difficulty': 'Extreme'}
        res = client.post('/api/questions', json=q, headers=headers)
        assert res.status_code == 400

    def test_create_title_too_short(self, client):
        headers = setup_user(client)
        q = {**VALID_QUESTION, 'title': 'Hi'}  # min 5 chars
        res = client.post('/api/questions', json=q, headers=headers)
        assert res.status_code == 400

    def test_create_requires_auth(self, client):
        res = client.post('/api/questions', json=VALID_QUESTION)
        assert res.status_code == 401


class TestListQuestions:
    def test_list_returns_only_own_questions(self, client):
        # User A creates a question
        headers_a = setup_user(client, email='a@example.com')
        client.post('/api/questions', json=VALID_QUESTION, headers=headers_a)

        # User B should see zero questions
        register(client, email='b@example.com')
        token_b = login(client, email='b@example.com')
        headers_b = auth_header(token_b)
        res = client.get('/api/questions', headers=headers_b)
        assert res.status_code == 200
        assert res.get_json() == []

    def test_list_returns_own_questions(self, client):
        headers = setup_user(client)
        client.post('/api/questions', json=VALID_QUESTION, headers=headers)
        res = client.get('/api/questions', headers=headers)
        assert res.status_code == 200
        assert len(res.get_json()) == 1


class TestUpdateDeleteQuestion:
    def test_update_question(self, client):
        headers = setup_user(client)
        create_res = client.post('/api/questions', json=VALID_QUESTION, headers=headers)
        qid = create_res.get_json()['id']

        res = client.put(f'/api/questions/{qid}', json={'title': 'Updated title here'}, headers=headers)
        assert res.status_code == 200
        assert res.get_json()['title'] == 'Updated title here'

    def test_cannot_update_other_users_question(self, client):
        headers_a = setup_user(client, email='a@example.com')
        create_res = client.post('/api/questions', json=VALID_QUESTION, headers=headers_a)
        qid = create_res.get_json()['id']

        register(client, email='b@example.com')
        token_b = login(client, email='b@example.com')
        headers_b = auth_header(token_b)
        res = client.put(f'/api/questions/{qid}', json={'title': 'Hacked title'}, headers=headers_b)
        assert res.status_code == 404  # appears not found to other user

    def test_delete_question(self, client):
        headers = setup_user(client)
        create_res = client.post('/api/questions', json=VALID_QUESTION, headers=headers)
        qid = create_res.get_json()['id']

        res = client.delete(f'/api/questions/{qid}', headers=headers)
        assert res.status_code == 200

        get_res = client.get(f'/api/questions/{qid}', headers=headers)
        assert get_res.status_code == 404
