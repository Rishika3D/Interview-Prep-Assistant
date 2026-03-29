import { useState } from 'react';
import PracticeMode from './PracticeMode';
import './QuestionCard.css';

export default function QuestionCard({ question, onDelete }) {
  const [isPracticing, setIsPracticing] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const handlePracticeDone = (result) => {
    setFeedback(result);
    setIsPracticing(false);
  };

  if (isPracticing) {
    return (
      <PracticeMode
        question={question}
        onDone={handlePracticeDone}
        onCancel={() => setIsPracticing(false)}
      />
    );
  }

  return (
    <div className="question-card">
      <div className="card-header">
        <h3>{question.title}</h3>
        <div className="badges">
          <span className="badge category">{question.category}</span>
          <span className="badge difficulty">{question.difficulty}</span>
        </div>
      </div>

      <p className="question-text">{question.content}</p>

      {question.expected_answer && (
        <div className="expected-answer">
          <strong>Key Points:</strong>
          <p>{question.expected_answer}</p>
        </div>
      )}

      {feedback && (
        <div className="feedback-summary">
          <strong>Last Attempt Score: {feedback.score}/100</strong>
          <p>{feedback.feedback}</p>
        </div>
      )}

      <div className="card-actions">
        <button
          onClick={() => setIsPracticing(true)}
          className="primary-btn"
        >
          Practice
        </button>
        {onDelete && (
          <button onClick={onDelete} className="danger-btn">
            Delete
          </button>
        )}
      </div>
    </div>
  );
}
