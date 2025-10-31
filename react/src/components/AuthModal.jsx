import { useEffect, useRef, useState } from 'react';
import { login, register } from '../api/auth';

export default function AuthModal({ mode = 'login', onClose, onSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const dialogRef = useRef(null);

  useEffect(() => {
    const onEsc = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', onEsc);
    return () => window.removeEventListener('keydown', onEsc);
  }, [onClose]);

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    const u = (username || '').trim();
    const p = (password || '').trim();
    if (u.length < 3 || p.length < 6) {
      setError('Проверьте логин и пароль');
      return;
    }
    setLoading(true);
    try {
      const fn = mode === 'register' ? register : login;
      const data = await fn({ username: u, password: p });
      if (data && data.token) {
        localStorage.setItem('token', data.token);
      }
      if (onSuccess) onSuccess(data);
    } catch (err) {
      setError('Ошибка авторизации');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div data-easytag="id1-src/components/AuthModal.jsx" className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" onClick={onClose}>
      <div data-easytag="id2-src/components/AuthModal.jsx" className="card w-full max-w-md p-6" onClick={(e) => e.stopPropagation()} ref={dialogRef}>
        <div data-easytag="id3-src/components/AuthModal.jsx" className="mb-4">
          <h2 data-easytag="id4-src/components/AuthModal.jsx" className="text-xl font-semibold tracking-tight">{mode === 'register' ? 'Регистрация' : 'Вход'}</h2>
          <p data-easytag="id5-src/components/AuthModal.jsx" className="mt-1 text-sm text-neutral-500">Введите данные для {mode === 'register' ? 'регистрации' : 'входа'}.</p>
        </div>
        <form data-easytag="id6-src/components/AuthModal.jsx" onSubmit={submit} className="space-y-3">
          <div data-easytag="id7-src/components/AuthModal.jsx" className="space-y-1">
            <label data-easytag="id8-src/components/AuthModal.jsx" className="text-sm text-neutral-700">Логин</label>
            <input data-easytag="id9-src/components/AuthModal.jsx" className="input" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Ваш логин" />
          </div>
          <div data-easytag="id10-src/components/AuthModal.jsx" className="space-y-1">
            <label data-easytag="id11-src/components/AuthModal.jsx" className="text-sm text-neutral-700">Пароль</label>
            <input data-easytag="id12-src/components/AuthModal.jsx" type="password" className="input" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Минимум 6 символов" />
          </div>
          {error && <div data-easytag="id13-src/components/AuthModal.jsx" className="text-sm text-red-600">{error}</div>}
          <div data-easytag="id14-src/components/AuthModal.jsx" className="flex items-center gap-2 pt-2">
            <button data-easytag="id15-src/components/AuthModal.jsx" type="submit" className="btn-primary" disabled={loading}>{loading ? 'Подождите…' : (mode === 'register' ? 'Зарегистрироваться' : 'Войти')}</button>
            <button data-easytag="id16-src/components/AuthModal.jsx" type="button" className="btn-ghost" onClick={onClose}>Отмена</button>
          </div>
        </form>
      </div>
    </div>
  );
}
