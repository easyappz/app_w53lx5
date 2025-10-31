import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { resolve as resolveAd } from '../api/ads';

export default function SearchBar() {
  const [value, setValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const validateUrl = (url) => {
    try {
      const u = new URL(url);
      return !!u.href;
    } catch (_) {
      return false;
    }
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const v = (value || '').trim();
    if (!validateUrl(v)) {
      setError('Введите корректную ссылку');
      return;
    }
    setLoading(true);
    try {
      const ad = await resolveAd(v);
      if (ad && ad.id) navigate(`/ad/${ad.id}`);
    } catch (err) {
      setError('Не удалось распознать объявление');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form data-easytag="id1-src/components/SearchBar.jsx" onSubmit={onSubmit} className="w-full max-w-3xl mx-auto mt-6 flex gap-2">
      <input data-easytag="id2-src/components/SearchBar.jsx" className="input flex-1" placeholder="Вставьте ссылку на объявление Авито" value={value} onChange={(e) => setValue(e.target.value)} />
      <button data-easytag="id3-src/components/SearchBar.jsx" type="submit" className="btn-primary" disabled={loading}>{loading ? 'Поиск…' : 'Найти'}</button>
      {error && <div data-easytag="id4-src/components/SearchBar.jsx" className="w-full text-sm text-red-600 mt-2">{error}</div>}
    </form>
  );
}
