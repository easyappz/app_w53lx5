import { useEffect, useMemo, useState } from 'react';
import { list as listAds } from '../api/ads';
import { getSettings } from '../api/settings';
import SearchBar from '../components/SearchBar';
import AdCard from '../components/AdCard';

export default function Home() {
  const [sort, setSort] = useState('popular');
  const [category, setCategory] = useState('Все');
  const [data, setData] = useState({ results: [], count: 0, limit: 20, offset: 0 });
  const [loading, setLoading] = useState(true);
  const [headerTitle, setHeaderTitle] = useState('Авитолог');

  const categories = useMemo(() => {
    const set = new Set(['Все']);
    for (const item of (data.results || [])) {
      if (item && item.category) set.add(item.category);
    }
    return Array.from(set);
  }, [data.results]);

  const load = async () => {
    setLoading(true);
    try {
      const effectiveCategory = category === 'Все' ? '' : category;
      const res = await listAds({ sort, category: effectiveCategory, limit: 20, offset: 0 });
      setData(res);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sort, category]);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const settings = await getSettings();
        if (active && settings && typeof settings.header_title === 'string') {
          setHeaderTitle(settings.header_title);
        }
      } catch (_) {
        // ignore
      }
    })();
    return () => { active = false; };
  }, []);

  return (
    <main data-easytag="id1-src/pages/Home.jsx" className="mx-auto max-w-6xl px-5 pb-16">
      <section data-easytag="id2-src/pages/Home.jsx" className="pt-10 text-center">
        <h1 data-easytag="id3-src/pages/Home.jsx" className="text-3xl sm:text-4xl font-semibold tracking-tight">{headerTitle}</h1>
        <p data-easytag="id4-src/pages/Home.jsx" className="mt-2 text-neutral-600">Вставьте ссылку на объявление Авито — мы найдём и покажем детали.</p>
        <SearchBar />
      </section>

      <section data-easytag="id5-src/pages/Home.jsx" className="mt-10">
        <div data-easytag="id6-src/pages/Home.jsx" className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div data-easytag="id7-src/pages/Home.jsx" className="flex items-center gap-2">
            <label data-easytag="id8-src/pages/Home.jsx" className="text-sm text-neutral-600">Сортировка</label>
            <select data-easytag="id9-src/pages/Home.jsx" className="input !py-2 !h-10" value={sort} onChange={(e) => setSort(e.target.value)}>
              <option data-easytag="id10-src/pages/Home.jsx" value="popular">Популярность</option>
              <option data-easytag="id11-src/pages/Home.jsx" value="date">Дата</option>
            </select>
          </div>
          <div data-easytag="id12-src/pages/Home.jsx" className="flex items-center gap-2">
            <label data-easytag="id13-src/pages/Home.jsx" className="text-sm text-neutral-600">Категория</label>
            <select data-easytag="id14-src/pages/Home.jsx" className="input !py-2 !h-10" value={category} onChange={(e) => setCategory(e.target.value)}>
              {categories.map((c) => (
                <option data-easytag="id15-src/pages/Home.jsx" key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>
        </div>

        <div data-easytag="id16-src/pages/Home.jsx" className="mt-6">
          {loading ? (
            <div data-easytag="id17-src/pages/Home.jsx" className="text-center text-neutral-600">Загрузка…</div>
          ) : (
            <div data-easytag="id18-src/pages/Home.jsx" className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {(data.results || []).map((ad) => (
                <AdCard key={ad.id} ad={ad} />
              ))}
            </div>
          )}
        </div>
      </section>
    </main>
  );
}
