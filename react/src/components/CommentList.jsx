import dayjs from 'dayjs';

export default function CommentList({ items }) {
  if (!Array.isArray(items) || items.length === 0) {
    return <div data-easytag="id1-src/components/CommentList.jsx" className="text-sm text-neutral-500">Пока нет комментариев</div>;
  }
  return (
    <ul data-easytag="id2-src/components/CommentList.jsx" className="space-y-3">
      {items.map((c) => (
        <li data-easytag="id3-src/components/CommentList.jsx" key={c.id} className="border border-black/10 rounded-xl p-3">
          <div data-easytag="id4-src/components/CommentList.jsx" className="flex items-center justify-between text-sm">
            <span data-easytag="id5-src/components/CommentList.jsx" className="font-medium">{c.username}</span>
            <span data-easytag="id6-src/components/CommentList.jsx" className="text-neutral-500">{dayjs(c.created_at).format('DD.MM.YYYY HH:mm')}</span>
          </div>
          <p data-easytag="id7-src/components/CommentList.jsx" className="mt-1 text-sm leading-relaxed">{c.text}</p>
        </li>
      ))}
    </ul>
  );
}
