import axios from 'axios';

const API_BASE = '/api';
const token = localStorage.getItem('token');

const api = axios.create({
  baseURL: API_BASE,
  headers: token ? { Authorization: `Bearer ${token}` } : {}
});

export const setAuthToken = (token) => {
  if (token) {
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
