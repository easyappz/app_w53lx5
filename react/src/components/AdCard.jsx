import dayjs from 'dayjs';
import { useNavigate } from 'react-router-dom';

export default function AdCard({ ad }) {
  const navigate = useNavigate();
  const open = () => navigate(`/ad/${ad.id}`);

  return (
    <article data-easytag="id1-src/components/AdCard.jsx" className="card overflow-hidden cursor-pointer transition hover:shadow" onClick={open}>
      <div data-easytag="id2-src/components/AdCard.jsx" className="aspect-[16/9] w-full bg-neutral-100" aria-hidden="true">
        {/* image placeholder (no images to be loaded) */}
      </div>
      <div data-easytag="id3-src/components/AdCard.jsx" className="p-4 space-y-2">
        <h3 data-easytag="id4-src/components/AdCard.jsx" className="text-base font-medium leading-tight line-clamp-2">{ad.title || 'Без названия'}</h3>
        <div data-easytag="id5-src/components/AdCard.jsx" className="text-sm text-neutral-600 flex flex-wrap gap-x-3 gap-y-1">
          <span data-easytag="id6-src/components/AdCard.jsx">Категория: {ad.category || '—'}</span>
          <span data-easytag="id7-src/components/AdCard.jsx">Просмотры: {ad.view_count}</span>
          <span data-easytag="id8-src/components/AdCard.jsx">Дата: {ad.published_at ? dayjs(ad.published_at).format('DD.MM.YYYY HH:mm') : '—'}</span>
        </div>
      </div>
    </article>
  );
}
