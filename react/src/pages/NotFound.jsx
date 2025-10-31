import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <main data-easytag="id1-src/pages/NotFound.jsx" className="mx-auto max-w-6xl px-5 py-16 text-center">
      <h1 data-easytag="id2-src/pages/NotFound.jsx" className="text-4xl font-semibold">404</h1>
      <p data-easytag="id3-src/pages/NotFound.jsx" className="mt-2 text-neutral-600">Страница не найдена</p>
      <Link data-easytag="id4-src/pages/NotFound.jsx" to="/" className="btn-primary mt-6 inline-flex">На главную</Link>
    </main>
  );
}
