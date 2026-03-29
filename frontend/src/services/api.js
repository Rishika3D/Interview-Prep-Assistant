import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({ baseURL: API_BASE });

// Attach token from localStorage on every request (not just at load time)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token && token !== 'null' && token !== 'undefined') config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Clear stale token automatically on 401/403
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401 || err.response?.status === 422) {
      localStorage.removeItem('token');
      delete api.defaults.headers.Authorization;
    }
    return Promise.reject(err);
  }
);

export const setAuthToken = (token) => {
  if (token && token !== 'null' && token !== 'undefined') {
    api.defaults.headers.Authorization = `Bearer ${token}`;
    localStorage.setItem('token', token);
  } else {
    delete api.defaults.headers.Authorization;
    localStorage.removeItem('token');
  }
};

export const signup = (email, password) =>
  api.post('/auth/signup', { email, password });

export const login = (email, password) =>
  api.post('/auth/login', { email, password });

export const getCurrentUser = () =>
  api.get('/auth/me');

export const listQuestions = () =>
  api.get('/questions');

export const getQuestion = (id) =>
  api.get(`/questions/${id}`);

export const createQuestion = (data) =>
  api.post('/questions', data);

export const updateQuestion = (id, data) =>
  api.put(`/questions/${id}`, data);

export const deleteQuestion = (id) =>
  api.delete(`/questions/${id}`);

export const submitAttempt = (questionId, userAnswer) =>
  api.post('/attempts', { question_id: questionId, user_answer: userAnswer });

export const getAttempt = (id) =>
  api.get(`/attempts/${id}`);

export const getQuestionAttempts = (questionId) =>
  api.get(`/attempts/question/${questionId}`);
