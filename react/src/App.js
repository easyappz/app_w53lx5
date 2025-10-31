import { useEffect, useMemo, useState } from 'react';
import ErrorBoundary from './ErrorBoundary';
import './App.css';
import { listAds, resolveAd, getAd, getComments, postComment } from './api/ads';

function useHashRoute() {
  const parse = () => {
    const hash = window.location.hash || '#/';
    const parts = hash.replace('#', '').split('/').filter(Boolean);
    if (parts.length === 0) return { name: 'home' };
    if (parts[0] === 'ad' && parts[1]) return { name: 'detail', id: parts[1] };
    return { name: 'home' };
  };
  const [route, setRoute] = useState(parse());
  useEffect(() => {
    const onChange = () => setRoute(parse());
    window.addEventListener('hashchange', onChange);
    return () => window.removeEventListener('hashchange', onChange);
  }, []);
  return route;
}

function SearchByLink({ onResolved }) {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!url || !/^https?:\/\//i.test(url)) {
      setError('Enter a valid URL');
      return;
    }
    setLoading(true);
    try {
      const ad = await resolveAd(url.trim());
      onResolved(ad);
    } catch (err) {
      setError('Failed to resolve the ad.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="search" onSubmit={handleSubmit}>
      <input
        type="url"
        placeholder="Paste Avito link"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button type="submit" disabled={loading}>{loading ? 'Resolving…' : 'Find by link'}</button>
      {error && <div className="error">{error}</div>}
    </form>
  );
}

function Toolbar({ sort, setSort, category, setCategory, onRefresh }) {
  return (
    <div className="toolbar">
      <div className="field">
        <label>Sort</label>
        <select value={sort} onChange={(e) => setSort(e.target.value)}>
          <option value="popular">Popular</option>
          <option value="date">Date</option>
        </select>
      </div>
      <div className="field">
        <label>Category</label>
        <input value={category} onChange={(e) => setCategory(e.target.value)} placeholder="e.g. Смартфоны or Все" />
      </div>
      <button onClick={onRefresh}>Refresh</button>
    </div>
  );
}

function AdCard({ ad }) {
  const open = () => {
    window.location.hash = `#/ad/${ad.id}`;
  };
  return (
    <div className="ad-card" onClick={open} role="button" tabIndex={0}>
      <div className="thumb">
        {ad.image_url ? (
          <img src={ad.image_url} alt={ad.title || 'Ad image'} />
        ) : (
          <div className="placeholder" />
        )}
      </div>
      <div className="ad-info">
        <div className="ad-title">{ad.title || 'No title'}</div>
        <div className="ad-meta">
          <span>Category: {ad.category || '—'}</span>
          <span>Views: {ad.view_count}</span>
          <span>Published: {ad.published_at ? new Date(ad.published_at).toLocaleString() : '—'}</span>
        </div>
      </div>
    </div>
  );
}

function HomePage() {
  const [sort, setSort] = useState('popular');
  const [category, setCategory] = useState('');
  const [limit, setLimit] = useState(20);
  const [offset, setOffset] = useState(0);
  const [data, setData] = useState({ results: [], count: 0 });
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      // Treat empty or "Все" as no category filter
      const cat = (category || '').trim();
      const effectiveCategory = cat && cat.toLowerCase() !== 'все' ? cat : '';
      const res = await listAds({ sort, category: effectiveCategory, limit, offset });
      setData(res);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sort, category, limit, offset]);

  const onResolved = (ad) => {
    window.location.hash = `#/ad/${ad.id}`;
  };

  const next = () => {
    if (offset + limit < (data.count || 0)) setOffset(offset + limit);
  };
  const prev = () => {
    if (offset - limit >= 0) setOffset(offset - limit);
  };

  return (
    <div className="container">
      <h1>Most viewed ads</h1>
      <SearchByLink onResolved={onResolved} />
      <Toolbar sort={sort} setSort={setSort} category={category} setCategory={setCategory} onRefresh={load} />
      {loading ? (
        <div className="loading">Loading…</div>
      ) : (
        <>
          <div className="grid">
            {data.results.map((ad) => (
              <AdCard key={ad.id} ad={ad} />
            ))}
          </div>
          <div className="pager">
            <button onClick={prev} disabled={offset === 0}>Prev</button>
            <span>
              {data.count > 0 ? `${Math.floor(offset / limit) + 1} / ${Math.max(1, Math.ceil(data.count / limit))}` : '0 / 0'}
            </span>
            <button onClick={next} disabled={offset + limit >= (data.count || 0)}>Next</button>
          </div>
        </>
      )}
    </div>
  );
}

function Comments({ adId }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [text, setText] = useState('');
  const [error, setError] = useState('');
  const [posting, setPosting] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const list = await getComments(adId);
      setItems(list);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [adId]);

  const isLoggedIn = !!localStorage.getItem('token');

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    const payload = (text || '').trim();
    if (!payload) {
      setError('Enter your comment');
      return;
    }
    setPosting(true);
    try {
      await postComment(adId, payload);
      setText('');
      await load();
    } catch (err) {
      setError('Failed to post comment. Make sure you are logged in.');
    } finally {
      setPosting(false);
    }
  };

  return (
    <div className="comments">
      <h3>Comments</h3>
      {loading ? (
        <div className="loading">Loading…</div>
      ) : (
        <div className="comments-list">
          {items.length === 0 ? (
            <div className="muted">No comments yet</div>
          ) : (
            items.map((c) => (
              <div key={c.id} className="comment">
                <div className="comment-header">
                  <strong>{c.username}</strong>
                  <span className="time">{new Date(c.created_at).toLocaleString()}</span>
                </div>
                <div className="comment-text">{c.text}</div>
              </div>
            ))
          )}
        </div>
      )}

      <div className="comment-form">
        {isLoggedIn ? (
          <form onSubmit={submit}>
            <textarea
              placeholder="Write a comment…"
              value={text}
              onChange={(e) => setText(e.target.value)}
              maxLength={2000}
            />
            <div className="row">
              <button type="submit" disabled={posting}>{posting ? 'Posting…' : 'Post comment'}</button>
              {error && <span className="error" style={{ marginLeft: 8 }}>{error}</span>}
            </div>
          </form>
        ) : (
          <div className="muted">Login to post a comment.</div>
        )}
      </div>
    </div>
  );
}

function DetailPage({ id }) {
  const [ad, setAd] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await getAd(id);
        if (!cancelled) setAd(data);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [id]);

  if (loading) return <div className="container"><div className="loading">Loading…</div></div>;
  if (!ad) return <div className="container"><div className="error">Not found</div></div>;

  return (
    <div className="container">
      <button className="link" onClick={() => (window.location.hash = '#/')}>← Back</button>
      <div className="detail">
        <div className="detail-image">
          {ad.image_url ? (
            <img src={ad.image_url} alt={ad.title || 'Ad image'} />
          ) : (
            <div className="placeholder large" />
          )}
        </div>
        <div className="detail-info">
          <h2>{ad.title || 'No title'}</h2>
          <div className="ad-meta">
            <div><strong>Category:</strong> {ad.category || '—'}</div>
            <div><strong>Published:</strong> {ad.published_at ? new Date(ad.published_at).toLocaleString() : '—'}</div>
            <div><strong>Views:</strong> {ad.view_count}</div>
            <div><strong>Source:</strong> <a href={ad.source_url} target="_blank" rel="noreferrer">Open Avito</a></div>
          </div>
        </div>
      </div>
      <Comments adId={id} />
    </div>
  );
}

function App() {
  const route = useHashRoute();
  return (
    <ErrorBoundary>
      <div className="App">
        {route.name === 'detail' ? (
          <DetailPage id={route.id} />
        ) : (
          <HomePage />
        )}
      </div>
    </ErrorBoundary>
  );
}

export default App;
