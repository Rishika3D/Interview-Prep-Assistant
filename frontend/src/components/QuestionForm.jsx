import { useState } from 'react';
import './QuestionForm.css';

export default function QuestionForm({ onSubmit }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [expectedAnswer, setExpectedAnswer] = useState('');
  const [category, setCategory] = useState('General');
  const [difficulty, setDifficulty] = useState('Medium');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!title || !content) {
      setError('Title and question are required');
      return;
    }

    try {
      await onSubmit({
        title,
        content,
        expected_answer: expectedAnswer,
        category,
        difficulty
      });
      setTitle('');
      setContent('');
      setExpectedAnswer('');
      setCategory('General');
      setDifficulty('Medium');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form className="question-form" onSubmit={handleSubmit}>
      <h3>Add Interview Question</h3>

      <input
        type="text"
        placeholder="Question Title (e.g., 'Tell me about yourself')"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        maxLength="500"
        required
      />

      <textarea
        placeholder="Full Question"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        rows="4"
        required
      />

      <textarea
        placeholder="Expected Answer / Key Points (optional)"
        value={expectedAnswer}
        onChange={(e) => setExpectedAnswer(e.target.value)}
        rows="3"
      />

      <div className="form-row">
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="General">General</option>
          <option value="Behavioral">Behavioral</option>
          <option value="Technical">Technical</option>
          <option value="System Design">System Design</option>
        </select>

        <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
          <option value="Easy">Easy</option>
          <option value="Medium">Medium</option>
          <option value="Hard">Hard</option>
        </select>
      </div>

      {error && <p className="error">{error}</p>}

      <button type="submit" className="primary-btn">Create Question</button>
    </form>
  );
}
