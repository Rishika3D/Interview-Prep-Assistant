import { useState, useEffect } from 'react';
import * as api from '../services/api';
import QuestionForm from './QuestionForm';
import QuestionCard from './QuestionCard';
import './Dashboard.css';

export default function Dashboard({ onLogout }) {
  const [questions, setQuestions] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const res = await api.listQuestions();
      setQuestions(res.data);
    } catch (err) {
      setError('Failed to load questions');
    } finally {
      setLoading(false);
    }
  };

  const handleAddQuestion = async (data) => {
    try {
      await api.createQuestion(data);
      setShowForm(false);
      loadQuestions();
    } catch (err) {
      setError('Failed to create question');
    }
  };

  const handleDeleteQuestion = async (id) => {
    if (!window.confirm('Delete this question?')) return;
    try {
      await api.deleteQuestion(id);
      loadQuestions();
    } catch (err) {
      setError('Failed to delete question');
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Interview Prep Assistant</h1>
        <button onClick={onLogout} className="logout-btn">Logout</button>
      </header>

      <div className="dashboard-content">
        {error && <div className="error-banner">{error}</div>}

        <div className="add-question-section">
          {!showForm && (
            <button onClick={() => setShowForm(true)} className="primary-btn">
              + Add Question
            </button>
          )}
          {showForm && (
            <>
              <QuestionForm onSubmit={handleAddQuestion} />
              <button onClick={() => setShowForm(false)} className="secondary-btn">
                Cancel
              </button>
            </>
          )}
        </div>

        {questions.length === 0 ? (
          <p className="empty-state">No questions yet. Create one to get started!</p>
        ) : (
          <div className="questions-grid">
            {questions.map(q => (
              <QuestionCard
                key={q.id}
                question={q}
                onDelete={() => handleDeleteQuestion(q.id)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
