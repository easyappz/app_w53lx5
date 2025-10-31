import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { me } from '../api/auth';
import AuthModal from './AuthModal';

export default function Header() {
  const [user, setUser] = useState(null);
  const [open, setOpen] = useState(null); // 'login' | 'register' | null
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;
    (async () => {
      try {
        const data = await me();
        if (data && data.username) setUser({ username: data.username });
      } catch (_) {
        // ignore
      }
    })();
  }, []);

  const onLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    navigate('/');
  };

  return (
    <header data-easytag="id1-src/components/Header.jsx" className="w-full border-b border-black/10 bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
      <div data-easytag="id2-src/components/Header.jsx" className="mx-auto max-w-6xl px-5 py-4 flex items-center justify-between">
        <Link data-easytag="id3-src/components/Header.jsx" to="/" className="flex items-center gap-2 select-none">
          <div data-easytag="id4-src/components/Header.jsx" className="h-8 w-8 rounded-lg bg-black" aria-hidden="true" />
          <span data-easytag="id5-src/components/Header.jsx" className="text-lg font-semibold tracking-tight">Авитолог</span>
        </Link>
        <nav data-easytag="id6-src/components/Header.jsx" className="flex items-center gap-2">
          {user ? (
            <div data-easytag="id7-src/components/Header.jsx" className="flex items-center gap-2">
              <span data-easytag="id8-src/components/Header.jsx" className="hidden sm:inline text-sm text-neutral-600">{user.username}</span>
              <button data-easytag="id9-src/components/Header.jsx" className="btn-ghost" onClick={onLogout}>Выйти</button>
            </div>
          ) : (
            <div data-easytag="id10-src/components/Header.jsx" className="flex items-center gap-2">
              <button data-easytag="id11-src/components/Header.jsx" className="btn-ghost" onClick={() => setOpen('login')}>Войти</button>
              <button data-easytag="id12-src/components/Header.jsx" className="btn-primary" onClick={() => setOpen('register')}>Зарегистрироваться</button>
            </div>
          )}
        </nav>
      </div>
      {open && (
        <AuthModal
          mode={open}
          onClose={() => setOpen(null)}
          onSuccess={(payload) => {
            if (payload && payload.username) setUser({ username: payload.username });
            setOpen(null);
          }}
        />
      )}
    </header>
  );
}
