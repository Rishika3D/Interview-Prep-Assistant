import { useState } from 'react';
import * as api from '../services/api';
import './PracticeMode.css';

const SYSTEM_DESIGN_FRAMEWORK = [
  { step: '1. Clarify Requirements', hint: 'Functional (what it does) + Non-functional (scale, latency, availability)' },
  { step: '2. Estimate Scale', hint: 'DAU, QPS, storage per day/year, bandwidth' },
  { step: '3. High-Level Design', hint: 'Draw major components: clients, load balancers, services, DBs, caches' },
  { step: '4. Database Design', hint: 'SQL vs NoSQL, schema, indexing, sharding strategy' },
  { step: '5. Core Components Deep Dive', hint: 'Pick 1-2 critical components and explain internals' },
  { step: '6. Scalability & Reliability', hint: 'Horizontal scaling, replication, CDN, caching (Redis), rate limiting' },
  { step: '7. Trade-offs', hint: 'CAP theorem, consistency vs availability, cost vs performance' },
];

function SystemDesignGuide() {
  const [open, setOpen] = useState(false);
  return (
    <div className="sd-guide">
      <button type="button" className="sd-toggle" onClick={() => setOpen(!open)}>
        {open ? '▾' : '▸'} System Design Framework
      </button>
      {open && (
        <ol className="sd-steps">
          {SYSTEM_DESIGN_FRAMEWORK.map(({ step, hint }) => (
            <li key={step}>
              <strong>{step}</strong>
              <span>{hint}</span>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}

export default function PracticeMode({ question, onDone, onCancel }) {
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (answer.trim().length < 10) {
      setError('Answer must be at least 10 characters');
      setLoading(false);
      return;
    }

    try {
      const res = await api.submitAttempt(question.id, answer);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to get feedback');
    } finally {
      setLoading(false);
    }
  };

  if (result) {
    return (
      <div className="practice-modal">
        <div className="practice-content">
          <h2>Feedback</h2>

          <div className="score-display">
            <div className="score-circle">
              <span className="score-number">{result.score}</span>
              <span className="score-label">/100</span>
            </div>
          </div>

          <p className="feedback-text">{result.feedback}</p>

          <div className="feedback-lists">
            {result.strengths.length > 0 && (
              <div className="strengths">
                <h4>✓ Strengths</h4>
                <ul>
                  {result.strengths.map((s, i) => <li key={i}>{s}</li>)}
                </ul>
              </div>
            )}

            {result.improvements.length > 0 && (
              <div className="improvements">
                <h4>→ Areas to Improve</h4>
                <ul>
                  {result.improvements.map((i, idx) => <li key={idx}>{i}</li>)}
                </ul>
              </div>
            )}
          </div>

          <div className="practice-actions">
            <button onClick={() => { setAnswer(''); setResult(null); }} className="primary-btn">
              Try Again
            </button>
            <button onClick={() => onDone(result)} className="secondary-btn">
              Done
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="practice-modal">
      <div className="practice-content">
        <h2>Practice: {question.title}</h2>

        <div className="question-box">
          <p>{question.content}</p>
        </div>

        {question.category === 'System Design' && (
          <SystemDesignGuide />
        )}

        <form onSubmit={handleSubmit}>
          <textarea
            placeholder="Type your answer here..."
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            rows="8"
            disabled={loading}
          />

          {error && <p className="error">{error}</p>}

          <div className="practice-actions">
            <button type="submit" disabled={loading} className="primary-btn">
              {loading ? 'Evaluating...' : 'Get Feedback'}
            </button>
            <button type="button" onClick={onCancel} className="secondary-btn">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
