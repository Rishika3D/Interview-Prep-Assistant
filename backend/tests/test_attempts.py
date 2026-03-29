"""
Tests for /api/attempts — submission, scoring, and user isolation.
AI calls are mocked so tests run without a real Groq API key.
"""
from unittest.mock import patch, MagicMock
from .conftest import register, login, auth_header

VALID_QUESTION = {
    'title': 'Design a URL shortener',
    'content': 'How would you design a scalable URL shortening service?',
    'category': 'System Design',
    'difficulty': 'Medium',
}

MOCK_FEEDBACK = {
    'score': 82,
    'feedback': 'Good answer covering key components.',
    'strengths': ['Clear architecture', 'Mentioned caching'],
    'improvements': ['Add scale estimation', 'Discuss database sharding'],
}


def create_question(client, headers):
    res = client.post('/api/questions', json=VALID_QUESTION, headers=headers)
    return res.get_json()['id']


def setup_user(client, email='user@example.com'):
    register(client, email=email)
    token = login(client, email=email)
    return auth_header(token)


class TestSubmitAttempt:
    @patch('backend.services.ai_feedback.AIFeedbackService.evaluate_answer', return_value=MOCK_FEEDBACK)
    def test_submit_returns_feedback(self, mock_ai, client):
        headers = setup_user(client)
        qid = create_question(client, headers)

        res = client.post('/api/attempts', json={
            'question_id': qid,
            'user_answer': 'I would use a hash function to shorten URLs and store them in Redis.'
        }, headers=headers)

        assert res.status_code == 201
        data = res.get_json()
        assert data['score'] == 82
        assert len(data['strengths']) == 2
        assert len(data['improvements']) == 2

    @patch('backend.services.ai_feedback.AIFeedbackService.evaluate_answer', return_value=MOCK_FEEDBACK)
    def test_answer_too_short_rejected(self, mock_ai, client):
        headers = setup_user(client)
        qid = create_question(client, headers)

        res = client.post('/api/attempts', json={
            'question_id': qid,
            'user_answer': 'Short'  # under 10 chars
        }, headers=headers)
        assert res.status_code == 400

    @patch('backend.services.ai_feedback.AIFeedbackService.evaluate_answer', return_value=MOCK_FEEDBACK)
    def test_cannot_attempt_other_users_question(self, mock_ai, client):
        # User A creates the question
        headers_a = setup_user(client, email='a@example.com')
        qid = create_question(client, headers_a)

        # User B tries to attempt it
        register(client, email='b@example.com')
        token_b = login(client, email='b@example.com')
        headers_b = auth_header(token_b)

        res = client.post('/api/attempts', json={
            'question_id': qid,
            'user_answer': 'This is my answer to your question which is long enough.'
        }, headers=headers_b)
        assert res.status_code == 404  # question not visible to user B

    def test_submit_requires_auth(self, client):
        res = client.post('/api/attempts', json={
            'question_id': 1,
            'user_answer': 'Some answer here that is long enough.'
        })
        assert res.status_code == 401


class TestGetAttempts:
    @patch('backend.services.ai_feedback.AIFeedbackService.evaluate_answer', return_value=MOCK_FEEDBACK)
    def test_get_question_attempts_only_own(self, mock_ai, client):
        headers = setup_user(client)
        qid = create_question(client, headers)

        # Submit an attempt
        client.post('/api/attempts', json={
            'question_id': qid,
            'user_answer': 'Here is my detailed answer to this system design question.'
        }, headers=headers)

        res = client.get(f'/api/attempts/question/{qid}', headers=headers)
        assert res.status_code == 200
        assert len(res.get_json()) == 1

    @patch('backend.services.ai_feedback.AIFeedbackService.evaluate_answer', return_value=MOCK_FEEDBACK)
    def test_get_attempt_by_id(self, mock_ai, client):
        headers = setup_user(client)
        qid = create_question(client, headers)

        submit_res = client.post('/api/attempts', json={
            'question_id': qid,
            'user_answer': 'Here is my detailed answer to this system design question.'
        }, headers=headers)
        attempt_id = submit_res.get_json()['attempt_id']

        res = client.get(f'/api/attempts/{attempt_id}', headers=headers)
        assert res.status_code == 200
        assert res.get_json()['id'] == attempt_id
