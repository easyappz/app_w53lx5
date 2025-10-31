import instance from './axios';

let schemaLoaded = false;
let schemaText = '';

async function ensureSchemaLoaded() {
  if (schemaLoaded) return;
  try {
    const resp = await fetch('/api_schema.yaml', { cache: 'no-cache' });
    schemaText = await resp.text();
    const required = ['/api/ads:', '/api/ads/resolve:', '/api/ads/{id}:', '/api/ads/{id}/comments:'];
    for (const p of required) {
      if (schemaText.indexOf(p) === -1) {
        console.warn('api_schema.yaml is missing expected path:', p);
      }
    }
    if (typeof window !== 'undefined') {
      window.__API_SCHEMA_YAML__ = schemaText;
    }
  } catch (e) {
    console.error('Failed to load api_schema.yaml', e);
  } finally {
    schemaLoaded = true;
  }
}

export async function list({ sort = 'popular', category = '', limit = 20, offset = 0 } = {}) {
  await ensureSchemaLoaded();
  const params = { sort, limit, offset };
  const cat = (category || '').trim();
  if (cat && cat.toLowerCase() !== 'все') params.category = cat;
  const res = await instance.get('/api/ads', { params });
  return res.data;
}

export async function resolve(url) {
  await ensureSchemaLoaded();
  const res = await instance.post('/api/ads/resolve', { url });
  return res.data;
}

export async function getById(id) {
  await ensureSchemaLoaded();
  const res = await instance.get(`/api/ads/${id}`);
  return res.data;
}
