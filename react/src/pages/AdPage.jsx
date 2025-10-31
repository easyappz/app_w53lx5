import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getById } from '../api/ads';
import { listByAd } from '../api/comments';
import CommentList from '../components/CommentList';
import CommentForm from '../components/CommentForm';
import dayjs from 'dayjs';

export default function AdPage() {
  const { id } = useParams();
  const [ad, setAd] = useState(null);
  const [loading, setLoading] = useState(true);
  const [comments, setComments] = useState([]);

  const load = async () => {
    setLoading(true);
    try {
      const a = await getById(id);
      setAd(a);
      const cs = await listByAd(id);
      setComments(cs);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  if (loading) {
    return (
      <main data-easytag="id1-src/pages/AdPage.jsx" className="mx-auto max-w-6xl px-5 py-10">
        <div data-easytag="id2-src/pages/AdPage.jsx" className="text-neutral-600">Загрузка…</div>
      </main>
    );
  }

  if (!ad) {
    return (
      <main data-easytag="id3-src/pages/AdPage.jsx" className="mx-auto max-w-6xl px-5 py-10">
        <div data-easytag="id4-src/pages/AdPage.jsx" className="text-red-600">Объявление не найдено</div>
        <Link data-easytag="id5-src/pages/AdPage.jsx" to="/" className="btn-ghost mt-4 inline-flex">На главную</Link>
      </main>
    );
  }

  return (
    <main data-easytag="id6-src/pages/AdPage.jsx" className="mx-auto max-w-6xl px-5 py-10 space-y-8">
      <Link data-easytag="id7-src/pages/AdPage.jsx" to="/" className="text-sm text-neutral-600 hover:underline">← На главную</Link>

      <section data-easytag="id8-src/pages/AdPage.jsx" className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div data-easytag="id9-src/pages/AdPage.jsx" className="lg:col-span-3 card overflow-hidden">
          <div data-easytag="id10-src/pages/AdPage.jsx" className="aspect-[16/9] w-full bg-neutral-100" aria-hidden="true" />
        </div>
        <div data-easytag="id11-src/pages/AdPage.jsx" className="lg:col-span-2 space-y-4">
          <h2 data-easytag="id12-src/pages/AdPage.jsx" className="text-2xl font-semibold leading-tight">{ad.title || 'Без названия'}</h2>
          <div data-easytag="id13-src/pages/AdPage.jsx" className="space-y-1 text-sm text-neutral-700">
            <div data-easytag="id14-src/pages/AdPage.jsx"><span data-easytag="id15-src/pages/AdPage.jsx" className="text-neutral-500">Дата публикации:</span> {ad.published_at ? dayjs(ad.published_at).format('DD.MM.YYYY HH:mm') : '—'}</div>
            <div data-easytag="id16-src/pages/AdPage.jsx"><span data-easytag="id17-src/pages/AdPage.jsx" className="text-neutral-500">Категория:</span> {ad.category || '—'}</div>
            <div data-easytag="id18-src/pages/AdPage.jsx"><span data-easytag="id19-src/pages/AdPage.jsx" className="text-neutral-500">Просмотры:</span> {ad.view_count}</div>
            <div data-easytag="id20-src/pages/AdPage.jsx"><span data-easytag="id21-src/pages/AdPage.jsx" className="text-neutral-500">Исходник:</span> <a data-easytag="id22-src/pages/AdPage.jsx" className="text-blue-600 hover:underline" href={ad.source_url} target="_blank" rel="noreferrer">Открыть на Авито</a></div>
          </div>
        </div>
      </section>

      <section data-easytag="id23-src/pages/AdPage.jsx" className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div data-easytag="id24-src/pages/AdPage.jsx" className="lg:col-span-3 space-y-4">
          <h3 data-easytag="id25-src/pages/AdPage.jsx" className="text-lg font-semibold">Комментарии</h3>
          <CommentList items={comments} />
          <CommentForm adId={id} onSubmitted={load} />
        </div>
      </section>
    </main>
  );
}
