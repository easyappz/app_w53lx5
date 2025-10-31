import { useState } from 'react';
import { create as createComment } from '../api/comments';

export default function CommentForm({ adId, onSubmitted }) {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  const canPost = !!token;

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    const payload = (text || '').trim();
    if (!payload) {
      setError('Введите текст комментария');
      return;
    }
    if (!canPost) {
      setError('Необходимо войти');
      return;
    }
    setLoading(true);
    try {
      await createComment(adId, payload);
      setText('');
      if (onSubmitted) onSubmitted();
    } catch (err) {
      if (err && err.response && err.response.status === 401) {
        setError('Необходимо войти');
      } else {
        setError('Не удалось отправить комментарий');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form data-easytag="id1-src/components/CommentForm.jsx" onSubmit={submit} className="space-y-2">
      <textarea
        data-easytag="id2-src/components/CommentForm.jsx"
        className="input min-h-28"
        placeholder={canPost ? 'Напишите комментарий…' : 'Войдите, чтобы комментировать'}
        value={text}
        onChange={(e) => setText(e.target.value)}
        maxLength={2000}
      />
      <div data-easytag="id3-src/components/CommentForm.jsx" className="flex items-center gap-2">
        <button data-easytag="id4-src/components/CommentForm.jsx" type="submit" className="btn-primary" disabled={!canPost || loading}>
          {loading ? 'Отправка…' : 'Отправить'}
        </button>
        {error && <span data-easytag="id5-src/components/CommentForm.jsx" className="text-sm text-red-600">{error}</span>}
      </div>
    </form>
  );
}
